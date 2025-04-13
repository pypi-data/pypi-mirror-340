# NEUROVORTEX OPTIMIZER

An AI Optimizer Module for improving of AI Models and managing system resources.

## Features
- Model format Detection and loading
- System resource monitoring (CPU, memory, GPU)
- AI Model optimization techniques

## Installation
```Bash
pip install neurovortex
```

## Usage
```Python
from ai_optimizer import AIOptimizer, load_model, ResourceManager

model = load_model("example_model.pth")
optimizer = AIOptimizer(model)
optimized_model = optimizer.optimize_model()

print("CPU Usage:", ResourceManager.get_cpu_usage(), "%")
```