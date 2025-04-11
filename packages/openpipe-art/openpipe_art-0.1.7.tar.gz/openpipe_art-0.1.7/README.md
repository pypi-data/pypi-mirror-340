<div align="center">

<a href="https://openpipe.ai"><picture>
<img alt="ART header" src="https://github.com/user-attachments/assets/d5441604-59fe-415d-a90a-9e9e2cbd5c2c" width="100%">
</picture></a>

<a href="https://colab.research.google.com/github/OpenPipe/ART/blob/main/examples/tic_tac_toe/tic-tac-toe.ipynb"><img src="https://github.com/user-attachments/assets/8d655cbd-6498-4ef0-a4bb-c6c353c63c0e" height="48"></a>
<a href="https://discord.gg/openpipe"><img src="https://github.com/user-attachments/assets/9d257702-a4a5-4824-901a-5155aa032a27" height="48"></a>
<a href="https://docs.openpipe.ai"><img src="https://github.com/user-attachments/assets/33acfb02-6920-4636-b66f-38dacdbe59ca" height="48"></a>

### Train free-range RL agents with minimal code changes and maximal performance!

![](https://github.com/user-attachments/assets/13eae0af-a7bf-4fd3-9e13-20847438cd66)

</div>

# The OpenPipe Agent Reinforcement Trainer (ART)

ART is an open-source reinforcement training library for improving LLM performance in agentic workflows. Unlike existing RL libraries, ART allows you to execute agent runs **in your existing codebase** while offloading all the complexity of the RL training loop to the ART backend. Read about the [ training loop](#training-loop-overview). Then try out one of the notebooks below!

## Notebooks

| Agent Task | Example Notebook                                                                                                     | Description                     | Comparative Performance |
| ---------- | -------------------------------------------------------------------------------------------------------------------- | ------------------------------- | ----------------------- |
| **2048**   | [🏋️ Train your agent](https://colab.research.google.com/github/openpipe/art/blob/notebooks/examples/2048/2048.ipynb) | Qwen 2.5 7B learns to play 2048 | [Link coming soon]      |

## Training Loop Overview

ART's functionality is divided into a **client** and a **server**. The OpenAI-compatible client is responsible for interfacing between ART and your codebase. Using the client, you can pass messages and get completions from your LLM as it improves. The server runs independently on any machine with a GPU. It abstracts away the complexity of the inference and training portions of the RL loop while allowing for some custom configuration. An outline of the training loop is shown below:

1. **Inference**

   1. Your code uses the ART client to perform an agentic workflow (usually executing several rollouts in parallel to gather data faster).
   2. Completion requests are routed to the ART server, which runs the model's latest LoRA in vLLM.
   3. As the agent executes, each `system`, `user`, and `assistant` message is stored in a Trajectory.
   4. When a rollout finishes, your code assigns a `reward` to its Trajectory, indicating the performance of the LLM.

2. **Training**
   1. When each rollout has finished, Trajectories are grouped and sent to the server. Inference is blocked while training executes.
   2. The server trains your model using GRPO, initializing from the latest checkpoint (or an empty LoRA on the first iteration).
   3. The server saves the newly trained LoRA to a local directory and loads it into vLLM.
   4. Inference is unblocked and the loop resumes at step 1.

This training loop runs until a specified number of inference and training iterations have completed.

## Contributing

ART is in very active development, and contributions are most welcome! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for more information.
