Here is the exact, updated specification you can feed to your coding agent. It dictates the dynamic execution environment and explicitly bounds the hyperparameter mutation space so the agent conducts a focused, Bayesian search rather than guessing blindly.

autoresearch_dynamic_spec.md
Objective
Build the autoresearch.py mutation engine to wrap the v1 DIAL train.py script. The engine must handle dynamic execution boundaries, early stopping, and a specifically bounded hyperparameter mutation space to optimize the latent communication protocol through continuous empirical updates.

1. Dynamic Execution & CLI Arguments
Do not hardcode execution limits. The script must accept the following arguments using argparse to allow both rapid testing and overnight convergence runs:

--max_time_sec: Maximum duration for a single training run (default: 300).

--max_epochs: Maximum epochs per run (default: 50).

--target_acc: Early termination threshold if the protocol solves the game (default: 0.98).

--patience: The number of evaluation cycles to tolerate plateauing or increasing validation loss before aborting the run (default: 3).

2. State Management (Warm Starting)
The script must load the most recent best_architecture.json and best_weights.pt files upon launch. It must mutate the best-known state, rather than initializing randomly, to ensure belief updates compound over multiple sessions.

3. The Mutation Space (Specific Hyperparameters)
The autoresearch.py script will parse train.py and mutate variables using Abstract Syntax Tree (AST) modification or regex. Constrain the agent to mutate only the following specific spaces:

Latent Bridge Dimensions:

Base: nn.Linear(hidden_size, hidden_size)

Mutation: MLP(hidden_size, bottleneck_size, hidden_size)

bottleneck_size options: [128, 256, 512]

Activation function options: [nn.GELU(), nn.SiLU()]

Signal Regularization (Noise):

Apply GaussianNoise(std) or nn.Dropout(p) directly to the continuous vector before Agent B receives it.

std options: [0.01, 0.05, 0.1]

p options: [0.0, 0.1, 0.2]

Optimization & Learning Rate:

Base LR options: [1e-5, 5e-5, 1e-4]

Schedulers: [ConstantLR, CosineAnnealingLR]

Environment (Referential Game):

Target concept sequence length: [5, 10, 15] tokens.

Batch size: [2, 4, 8] (dependent on local VRAM).

4. The Evaluation Protocol

Select a single random mutation from the defined space.

Inject the mutation into train.py.

Execute train.py.

Monitor validation loss. If patience reaches 0, terminate the subprocess immediately.

If the final validation accuracy exceeds the historical baseline, save the new weights and architecture state.

If the run fails, crashes, or underperforms, discard the mutation and load the previous best state.

Repeat continuously.