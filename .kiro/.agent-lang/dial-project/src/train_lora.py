import torch
import torch.nn as nn
import time
import argparse
from transformers import AutoModelForCausalLM, AutoConfig, BitsAndBytesConfig
from peft import get_peft_model, LoraConfig, TaskType

# Import the new semantic environment
from data.game_environment import ReferentialGameEnvironment

# 1. Architecture Setup & Quantization
MODEL_NAME = "Qwen/Qwen2.5-0.5B"

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

class LoraBridge(nn.Module):
    def __init__(self, hidden_dim):
        super().__init__()
        self.projection = nn.Linear(hidden_dim, hidden_dim)

    def forward(self, x):
        return self.projection(x)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max_time_sec", type=int, default=300) 
    args = parser.parse_args()

    # Load Agent A (Frozen Sender)
    agent_a = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME, quantization_config=bnb_config, device_map="auto"
    )
    for param in agent_a.parameters():
        param.requires_grad = False 

    # Initialize the Latent Bridge
    config = AutoConfig.from_pretrained(MODEL_NAME)
    hidden_dim = config.hidden_size
    bridge = LoraBridge(hidden_dim).to(agent_a.device)

    # Load Agent B (LoRA Receiver)
    base_agent_b = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME, quantization_config=bnb_config, device_map="auto"
    )
    
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=8,
        lora_alpha=16,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05
    )
    agent_b = get_peft_model(base_agent_b, lora_config)

    # Establish the joint optimizer
    optimizer = torch.optim.AdamW(
        list(bridge.parameters()) + list(agent_b.parameters()),
        lr=1e-4 
    )
    loss_fn = nn.CrossEntropyLoss()

    # --- NEW: Initialize the Semantic Environment ---
    print("Loading semantic environment...")
    env = ReferentialGameEnvironment(model_name=MODEL_NAME, device=agent_a.device)
    print("Environment loaded. Starting training loop.")

    start_time = time.time()
    correct_guesses = 0
    total_guesses = 0

    bridge.train()
    agent_b.train()

    # The empirical belief-updating loop
    while time.time() - start_time < args.max_time_sec:
        optimizer.zero_grad()

        # --- NEW: Generate semantic batch ---
        # Returns target concepts and choices mapped to real LLM tokens
        batch_size = 4
        target_concepts, choices, labels = env.generate_batch(
            batch_size=batch_size, 
            num_choices=5, 
            seq_len=10
        )

        # Forward pass: Agent A generates the latent vector
        with torch.no_grad():
            outputs_a = agent_a(input_ids=target_concepts, output_hidden_states=True)
            message_vector = outputs_a.hidden_states[-1][:, -1:, :] 

        # The Bridge transforms the vector
        bridged_message = bridge(message_vector)

        # Forward pass: Agent B receives the vector and choices
        choices_embeds = agent_b.get_base_model().model.embed_tokens(choices)
        
        combined_inputs = torch.cat([bridged_message, choices_embeds], dim=1)
        outputs_b = agent_b(inputs_embeds=combined_inputs)
        
        final_state = outputs_b.logits[:, -1, :]
        guess_logits = final_state[:, :5] 

        # Backpropagation
        loss = loss_fn(guess_logits, labels)
        loss.backward()
        optimizer.step()

        # Track validation metrics
        predictions = torch.argmax(guess_logits, dim=1)
        correct_guesses += (predictions == labels).sum().item()
        total_guesses += batch_size

    # Output for autoresearch.py
    accuracy = correct_guesses / total_guesses if total_guesses > 0 else 0
    print(f"Validation Accuracy: {accuracy:.4f}")

if __name__ == "__main__":
    main()