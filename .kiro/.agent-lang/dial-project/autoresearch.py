import os
import re
import random
import subprocess
import argparse
import time

def execute_git_command(command):
    subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def apply_mutation(filepath):
    """
    Reads the target file and applies a single regex-based mutation to the hyperparameter space.
    """
    with open(filepath, 'r') as file:
        content = file.read()

    # Define the mutation space
    mutations = [
        (r'lr=([0-9e.-]+)', lambda m: f"lr={random.choice(['1e-3', '5e-4', '1e-4', '5e-5'])}"),
        (r'hidden_dim = (\d+)', lambda m: f"hidden_dim = {random.choice([16, 32, 64, 128])}"),
        (r'vector_dim = (\d+)', lambda m: f"vector_dim = {random.choice([8, 16, 32])}")
    ]

    # Select and apply one random mutation
    target_regex, replacement_func = random.choice(mutations)
    mutated_content = re.sub(target_regex, replacement_func, content, count=1)

    with open(filepath, 'w') as file:
        file.write(mutated_content)
        
    return target_regex

def run_evaluation(filepath, max_time_sec):
    """
    Executes the training script and parses the stdout for validation accuracy.
    """
    try:
        result = subprocess.run(
            ['python', filepath, f'--max_time_sec={max_time_sec}'],
            capture_output=True, text=True, timeout=max_time_sec + 10
        )
        
        # Parse the output for the accuracy metric
        match = re.search(r'Validation Accuracy:\s*([0-9.]+)', result.stdout)
        if match:
            return float(match.group(1))
        return 0.0
    except subprocess.TimeoutExpired:
        return 0.0
    except Exception:
        return 0.0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=str, default="src/train_toy.py")
    parser.add_argument("--max_time_sec", type=int, default=30)
    parser.add_argument("--patience", type=int, default=5)
    args = parser.parse_args()

    # Ensure the repository has a clean Git state before starting
    execute_git_command("git add .")
    try:
        execute_git_command('git commit -m "Autoresearch init"')
    except subprocess.CalledProcessError:
        pass # Already committed

    best_accuracy = 0.0
    stagnant_epochs = 0
    iteration = 0

    print(f"Starting Autoresearch Loop on {args.target}")
    
    while stagnant_epochs < args.patience:
        iteration += 1
        print(f"\n--- Iteration {iteration} ---")
        
        # 1. Mutate
        apply_mutation(args.target)
        
        # 2. Execute and Evaluate
        print(f"Running {args.target} for {args.max_time_sec} seconds...")
        current_accuracy = run_evaluation(args.target, args.max_time_sec)
        print(f"Resulting Accuracy: {current_accuracy:.4f} (Best: {best_accuracy:.4f})")
        
        # 3. Update Beliefs (Git commit or rollback)
        if current_accuracy > best_accuracy:
            print("Empirical improvement detected. Committing changes.")
            best_accuracy = current_accuracy
            stagnant_epochs = 0
            execute_git_command("git add .")
            execute_git_command(f'git commit -m "Autoresearch improvement: Acc {best_accuracy:.4f}"')
        else:
            print("Hypothesis failed. Reverting to baseline.")
            stagnant_epochs += 1
            execute_git_command("git reset --hard HEAD")

    print(f"\nOptimization complete. Best accuracy achieved: {best_accuracy:.4f}")

if __name__ == "__main__":
    main()