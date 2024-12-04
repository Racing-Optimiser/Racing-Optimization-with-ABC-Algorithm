# Race Strategy Optimization Using Artificial Bee Colony Algorithm

This project implements a simulation to optimize race strategies using the Artificial Bee Colony (ABC) algorithm. The program is designed to minimize total race time by determining the optimal pitstop timing, tire selection, and fuel strategy under varying weather and track conditions.

---

## Features

- **Artificial Bee Colony (ABC) Algorithm**:
  - Utilizes exploration and exploitation to find the best race strategy.
  - Dynamically adapts to weather changes, tire wear, and other conditions.

- **Dynamic Simulation**:
  - Simulates real-world racing scenarios including wet and dry tracks.
  - Models tire performance degradation and fuel consumption.

- **Configurable Parameters**:
  - Adjust bee count, iteration limits, and race-specific configurations for experimentation.

- **Visualization**:
  - Provides visual feedback on optimization progress and results.

---

## Getting Started

### Prerequisites

Generate Race Data to optimize: 
```bash
python racegenerator.py
```

### Algorithm usage

To start algorithm on generated data use:
```bash
python ABCalgorithm2.py
```
 
