# Improving self-reflective prompt optimization with weak-driven learning.
## Research question
Recently it was found that:
1. Prompt optimization can outperform reinforcement learning in domain-specific application of LLMs - both much cheaper and much faster: https://arxiv.org/abs/2507.19457
2. Reinforcement learning of smart (e.g. gpt-5-xhigh) models can achieve higher performance when trained on weak agents rollouts (e.g. gpt-5-mini); breaking through RL saturation: https://arxiv.org/abs/2602.08222

Can we optimize domain-specific agents (e.g. math, coding) further by iterating on prompts via Generic Pareto Optimization (paper 1) using rollouts from smaller models?


## Research Design
We will use DSPy with a GEPA optimizer (paper 1), and will test in the following stages:
1. We establish a baseline - a large model optimizing a large model (itself) with prompts on math and coding challenges;
2. We then take that prompt and further "train" the prompt to work on a smaller model.
3. We experiment if the second prompt performs better on the larger model.

The hypothesis is that it will improve the performance of the larger model because it will cover more edgecases and embed more important/relevant information into the prompt.

## Expected outcomes:
This attacks a very relevant problem - how can we optimize agents; cost-efficiently and without fine-tuning the models? How can we improve the performance of agents using frontier models without having access to their weights; or without expense of fine-tuning?
(Note: the feature is a hypothesis. We can't validate that it is so without running an experiment first (the experiment is also relatively costly.)

