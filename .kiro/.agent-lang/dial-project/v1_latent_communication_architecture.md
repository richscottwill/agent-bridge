Here is the complete design specification for the v1 environment. You can save this text directly as a .md file and provide it to a frontier coding agent to execute the build.

The document frames the architecture explicitly around continuous belief updating, forcing the agent to rely on empirical results rather than assumed best practices.

v1_latent_communication_architecture.md
Objective
Build a Differentiable Inter-Agent Learning (DIAL) environment. Two distinct language models must develop an emergent, non-linguistic communication protocol to solve a cooperative task. You will establish a fully differentiable pipeline and an autoresearch loop to optimize the architecture.

1. System Architecture: The Differentiable Pipeline
You must construct the environment in PyTorch to retain the computational graph across multiple models simultaneously.

Agent A (The Sender): Instantiate a sub-1-billion parameter model (e.g., Qwen/Qwen2.5-0.5B). Bypass the Language Modeling (LM) head. The agent reads a target concept and outputs its final hidden state—a raw, continuous vector.

The Latent Bridge: Construct a mutable neural layer (starting as a simple nn.Linear projection). This layer receives Agent A's vector and transforms it. This is the primary component the autoresearch loop will mutate.

Agent B (The Receiver): Instantiate a second, identical model. Inject the transformed vector from the Latent Bridge directly into Agent B's input embedding space, prepended to a list of multiple-choice options. Agent B uses its LM head to output a discrete prediction (the index of the correct choice).

2. The Environment: The Referential Game
Design a strict, partially observable cooperative task to force communication.

Generate a synthetic dataset of target concepts (random token sequences).

Provide Agent A with the target concept.

Provide Agent B with a list of five choices (one correct concept, four distractors). Agent B does not see the target concept.

Agent B must select the correct concept based entirely on the mathematical vector it receives from Agent A.

3. Optimization: Continuous Belief Updating
Do not freeze any weights during the initial discovery phase.

Define a shared Cross-Entropy Loss function based on Agent B's final prediction.

Backpropagate the error backward continuously through Agent B, through the Latent Bridge, and entirely through Agent A.

Both agents must update their internal weights simultaneously. Agent A learns to generate better vectors; Agent B learns to interpret them accurately.

4. The Autoresearch Loop (The Mutation Engine)
Do not attempt to write the perfect architecture manually. You will build an evolutionary loop to discover it.

Write a master execution script (autoresearch.py) that performs the following sequence continuously:

Mutate: Alter one variable in the train.py script. Introduce noise to the Latent Bridge, change the learning rate, alter the projection layer dimensions, or adjust the batch size.

Execute: Run train.py. Hardcode the training script to terminate after exactly 300 seconds (5 minutes).

Evaluate: Read the final validation accuracy.

Update: Update the system's structural beliefs based entirely on the empirical evidence. If the validation accuracy improves the baseline, commit the change to the repository. If the accuracy drops, run git reset --hard HEAD to revert the mutation.

5. Convergence Standard
The v1 build is complete when the autoresearch loop discovers an architecture that consistently achieves >95% validation accuracy on the referential game. At this point, the agents possess a functional, highly optimized latent protocol.