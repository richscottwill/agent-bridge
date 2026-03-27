import torch
import torch.nn as nn
import time
import argparse

# 1. Architecture: The Sender (Agent A)
class ToyAgentA(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, vector_dim):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.fc1 = nn.Linear(embed_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, vector_dim)
        self.relu = nn.ReLU()

    def forward(self, x):
        # Pool the token sequence into a single representation
        embedded = self.embedding(x).mean(dim=1) 
        hidden = self.relu(self.fc1(embedded))
        # Output the raw, continuous latent vector
        return self.fc2(hidden) 

# 2. Architecture: The Channel (The Bridge)
class ToyBridge(nn.Module):
    def __init__(self, vector_dim):
        super().__init__()
        # This is the target block for the autoresearch mutation engine
        self.projection = nn.Linear(vector_dim, vector_dim)

    def forward(self, x):
        return self.projection(x)

# 3. Architecture: The Receiver (Agent B)
class ToyAgentB(nn.Module):
    def __init__(self, vocab_size, embed_dim, vector_dim, hidden_dim):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        # Input size = incoming vector + flattened embeddings of 5 choices
        self.fc1 = nn.Linear(vector_dim + (5 * embed_dim), hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, 5) 
        self.relu = nn.ReLU()

    def forward(self, message_vector, choices):
        choices_embedded = self.embedding(choices).view(choices.size(0), -1)
        # Concatenate the mathematical message with the environment choices
        combined = torch.cat([message_vector, choices_embedded], dim=1)
        hidden = self.relu(self.fc1(combined))
        # Output prediction logits for the 5 choices
        return self.fc2(hidden) 

# 4. The Execution Loop
def main():
    parser = argparse.ArgumentParser()
    # Default to 30 seconds for rapid logic validation testing
    parser.add_argument("--max_time_sec", type=int, default=30) 
    args = parser.parse_args()

    device = "cpu" 
    
    # Toy model hyperparameters
    vocab_size = 100
    embed_dim = 16
    hidden_dim = 32
    vector_dim = 16

    # Instantiate the multi-agent graph
    agent_a = ToyAgentA(vocab_size, embed_dim, hidden_dim, vector_dim).to(device)
    bridge = ToyBridge(vector_dim).to(device)
    agent_b = ToyAgentB(vocab_size, embed_dim, vector_dim, hidden_dim).to(device)

    # Establish the joint optimizer
    optimizer = torch.optim.AdamW(
        list(agent_a.parameters()) + list(bridge.parameters()) + list(agent_b.parameters()),
        lr=1e-3
    )
    loss_fn = nn.CrossEntropyLoss()

    start_time = time.time()
    correct_guesses = 0
    total_guesses = 0

    agent_a.train()
    bridge.train()
    agent_b.train()

    # The 30-second empirical belief-updating loop
    while time.time() - start_time < args.max_time_sec:
        optimizer.zero_grad()

        # Generate the synthetic referential game
        batch_size = 32
        seq_len = 5
        target_concepts = torch.randint(0, vocab_size, (batch_size, seq_len)).to(device)
        choices = torch.randint(0, vocab_size, (batch_size, 5)).to(device)
        labels = torch.randint(0, 5, (batch_size,)).to(device)

        # Ensure the correct answer exists in the choices at the label index
        for i in range(batch_size):
            choices[i, labels[i]] = target_concepts[i, 0] 

        # Forward pass (The Latent Transfer)
        message = agent_a(target_concepts)
        bridged_message = bridge(message)
        logits = agent_b(bridged_message, choices)

        # Backpropagation (The Belief Update)
        loss = loss_fn(logits, labels)
        loss.backward()
        optimizer.step()

        # Track validation metrics
        predictions = torch.argmax(logits, dim=1)
        correct_guesses += (predictions == labels).sum().item()
        total_guesses += batch_size

    # The critical output for autoresearch.py to parse
    accuracy = correct_guesses / total_guesses
    print(f"Validation Accuracy: {accuracy:.4f}")

if __name__ == "__main__":
    main()