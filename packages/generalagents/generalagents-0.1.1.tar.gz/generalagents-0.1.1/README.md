# General Agents Python API client

[![Release](https://img.shields.io/github/v/release/generalagents/generalagents-python)](https://img.shields.io/github/v/release/generalagents/generalagents-python)
[![Build status](https://img.shields.io/github/actions/workflow/status/generalagents/generalagents-python/main.yml?branch=main)](https://github.com/generalagents/generalagents-python/actions/workflows/main.yml?query=branch%3Amain)
[![License](https://img.shields.io/github/license/generalagents/generalagents-python)](https://img.shields.io/github/license/generalagents/generalagents-python)

# Documentation

The REST API documentation: https://docs.generalagents.com/

# Installation

General Agents Python API client is available as a python package on PyPI:

```bash
pip install generalagents
```

# Usage

This client includes both an interface for calling the agent, and a simple computer controller. An example execution
loop:

```python
from generalagents import Agent
from generalagents.macos import Computer

agent = Agent(model="ace-small", api_key='your-api-key-here')
computer = Computer()

instruction = "Star the generalagents-python github repository"
session = agent.start(instruction)
observation = computer.observe()

for _ in range(25):  # max actions
    action = session.plan(observation)
    print(f"Executing: {action}")
    if action.kind == "stop":
        break
    observation = computer.execute(action)
```

# Contributing

See [the contributing documentation](CONTRIBUTING.md).
