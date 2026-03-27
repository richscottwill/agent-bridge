import torch
import random
from transformers import AutoTokenizer

class ReferentialGameEnvironment:
    def __init__(self, model_name="Qwen/Qwen2.5-0.5B", device="cpu"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.device = device
        
        # A curated list of distinct semantic categories to force robust communication
        self.concept_pool = [
            "dog", "cat", "car", "tree", "house", "water", "fire", "sun", "moon", "star",
            "computer", "phone", "book", "chair", "table", "door", "window", "wall", "floor", "roof",
            "run", "walk", "jump", "sleep", "eat", "drink", "read", "write", "speak", "listen",
            "red", "blue", "green", "yellow", "black", "white", "big", "small", "hot", "cold",
            "happy", "sad", "angry", "fear", "love", "hate", "time", "space", "mind", "body"
        ]
        
        # Pre-tokenize the pool and ensure they map to single tokens for tensor stability
        self.token_pool = []
        for concept in self.concept_pool:
            tokens = self.tokenizer.encode(concept, add_special_tokens=False)
            if len(tokens) == 1:
                self.token_pool.append(tokens[0])

    def generate_batch(self, batch_size=4, num_choices=5, seq_len=10):
        """
        Generates a batch of semantic targets and distractors.
        Returns: target_sequences, choices_tensor, labels_tensor
        """
        targets = []
        choices_list = []
        labels = []

        for _ in range(batch_size):
            # 1. Sample the target and distractors
            sampled_tokens = random.sample(self.token_pool, num_choices)
            target_token = sampled_tokens[0]
            
            # 2. Shuffle to randomize the target's position
            random.shuffle(sampled_tokens)
            label_idx = sampled_tokens.index(target_token)
            
            # 3. Create a target sequence (padding the target token to match seq_len)
            # In a true semantic game, this represents the "context" the sender sees
            target_seq = [self.tokenizer.pad_token_id or 0] * (seq_len - 1) + [target_token]
            
            targets.append(target_seq)
            choices_list.append(sampled_tokens)
            labels.append(label_idx)

        # Convert to PyTorch tensors and move to the target device
        target_tensor = torch.tensor(targets, dtype=torch.long, device=self.device)
        choices_tensor = torch.tensor(choices_list, dtype=torch.long, device=self.device)
        labels_tensor = torch.tensor(labels, dtype=torch.long, device=self.device)

        return target_tensor, choices_tensor, labels_tensor

# Quick validation test
if __name__ == "__main__":
    env = ReferentialGameEnvironment()
    targets, choices, labels = env.generate_batch(batch_size=2)
    print(f"Targets shape: {targets.shape}")
    print(f"Choices shape: {choices.shape}")
    print(f"Labels shape: {labels.shape}")