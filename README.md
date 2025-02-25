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
- **Multiprocess testing**:
  - Better CPU utilization through parallel processing. Reduced time for tests.
    | **Parameters (Number of tests, Iterations, Bees, Food)** | **Previous Time (Single-threaded)** | **New Time (Multiprocessing)** |
    |-----------------------------------------|-------------------------------------|--------------------------------|
    | `50, 30, 30, 30`                            | 🕰️ 55 minutes 50 seconds                       | ⚡ 26 minutes 48 seconds                   |
    
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

## Objective Function

Minimization of the total race time:

$T_{total} = \sum_{lap=1}^{N} \left( T_{lap}(lap) + T_{pitstop}(lap) \right)$

### Definitions:
- **Tlap(lap)**: Lap time, dependent on various parameters such as tire wear, weather conditions, engine power, and failures.
- **Tpitstop(lap)**: Time spent in the pit stop per lap, determined by decisions on repairs, tire changes, and refueling.

---

## Lap Time Calculation

$T_{lap} = T_{base} \cdot \left( 1 + R_{failures} + R_{weather} + R_{tires} + R_{parts} \right)$

### Components:
1. **Tbase**: Base lap time (modified based on the set engine power).
2. **Rfailures**: Additional time due to failures
3. **Rweather**: Time due to weather conditions, proportional to the difference between track wetness and tire performance
5. **Rtires**: Time due to tire grip loss
6. **Rparts**: Time due to part wear
   


---

## Pit Stop Time Calculation

$T_{pitstop} = T_{base\_pitstop} + T_{fuel} + T_{tires\_change} + T_{repairs}$

### Components:
1. **Tbase_pitstop**: Base time for entering and exiting the pit stop.
2. **Tfuel**: Refueling time, proportional to the amount of fuel added.
3. **Ttires change**: Time for tire changes (constant value).
4. **Trepairs**: Repair time

---

## Optimization

Objective function to optimize:

$\min T_{total}$

### Strategy Parameters for Optimization:
- **fuel_pitstop**: Minimum fuel level to trigger a pit stop.
- **tire_wear_str**: Minimum tire wear level to trigger a pit stop.
- **engine_wear_strat**: Minimum engine wear level to trigger a pit stop.
- **brakes_wear_strat**: Minimum brake wear level to trigger a pit stop.
- **suspension_wear_strat**: Minimum suspension wear level to trigger a pit stop.
- **car_power**: Engine power (trade-off between speed and part wear).
- **tires**: Type of tire used.

---


 
