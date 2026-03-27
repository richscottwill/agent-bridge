import torch
import torch.nn as nn
import time
import argparse
from transformers import AutoModelForCausalLM, AutoConfig

# Import the semantic environment
from data.game_environment import ReferentialGameEnvironment

MODEL_NAME = "Qwen/Qwen2.5-0.5B"

class LatentBridge(nn.Module):
    def __init__(self, hidden_dim):
        super().__init__()
        # Target block for the autoresearch mutation engine
        self.projection = nn.Linear(hidden_dim, hidden_dim)

    def forward(self, x):
        return self.projection(x)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max_time_sec", type=int, default=300) 
    args = parser.parse_args()

    # The standard build requires a GPU
    device = "cuda" if torch.cuda.is_available() else "cpu"

    print("Loading Agent A (Fully Trainable Sender)...")
    agent_a = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME, 
        torch_dtype=torch.bfloat16,
        attn_implementation="flash_attention_2"
    ).to(device)
    # Note: We do NOT freeze Agent A's parameters here.

    config = AutoConfig.from_pretrained(MODEL_NAME)
    bridge = LatentBridge(config.hidden_size).to(device).to(torch.bfloat16)

    print("Loading Agent B (Fully Trainable Receiver)...")
    agent_b = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME, 
        torch_dtype=torch.bfloat16,
        attn_implementation="flash_attention_2"
    ).to(device)

    # Establish the joint optimizer across ALL parameters
    # We use a lower learning rate (1e-5) because full finetuning is highly sensitive
    optimizer = torch.optim.AdamW(
        list(agent_a.parameters()) + list(bridge.parameters()) + list(agent_b.parameters()),
        lr=1e-5 
    )
    loss_fn = nn.CrossEntropyLoss()

    print("Loading semantic environment...")
    env = ReferentialGameEnvironment(model_name=MODEL_NAME, device=device)

    start_time = time.time()
    correct_guesses = 0
    total_guesses = 0

    agent_a.train()
    bridge.train()
    agent_b.train()

    print("Starting full latent convergence loop.")
    while time.time() - start_time < args.max_time_sec:
        optimizer.zero_grad()

        batch_size = 4
        target_concepts, choices, labels = env.generate_batch(
            batch_size=batch_size, 
            num_choices=5, 
            seq_len=10
        )

        # Forward pass: Agent A generates the latent vector
        outputs_a = agent_a(input_ids=target_concepts, output_hidden_states=True)
        message_vector = outputs_a.hidden_states[-1][:, -1:, :] 

        # The Bridge transforms the vector
        bridged_message = bridge(message_vector)

        # Forward pass: Agent B receives the vector and choices
        choices_embeds = agent_b.model.embed_tokens(choices)
        
        combined_inputs = torch.cat([bridged_message, choices_embeds], dim=1)
        outputs_b = agent_b(inputs_embeds=combined_inputs)
        
        final_state = outputs_b.logits[:, -1, :]
        guess_logits = final_state[:, :5] 

        # Full Backpropagation
        # The loss flows seamlessly through Agent B, the Bridge, and entirely through Agent A
        loss = loss_fn(guess_logits, labels)
        loss.backward()
        optimizer.step()

        predictions = torch.argmax(guess_logits, dim=1)
        correct_guesses += (predictions == labels).sum().item()
        total_guesses += batch_size

    accuracy = correct_guesses / total_guesses if total_guesses > 0 else 0
    print(f"Validation Accuracy: {accuracy:.4f}")

if __name__ == "__main__":
    main()