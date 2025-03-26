# SkyGo_drone_delivery

## Overview
This project implements a **Drone Fleet Optimization** system to assign delivery orders to available drones efficiently. It prioritizes drones based on speed, payload capacity, and range while ensuring orders are fulfilled within constraints.

## Features
✅ Load drone and order data from a JSON file.  
✅ Sort and prioritize drones based on their capabilities.  
✅ Assign orders while considering payload and distance constraints.  
✅ Save optimized assignments to an output JSON file.  

## Prerequisites
- Python 3.x  
- JSON file with structured data  

## Installation
Clone the repository and navigate to the project directory:
```sh
git clone https://github.com/your-username/drone-fleet-optimization.git
cd drone-fleet-optimization
```
## Usage
Modify the function call in script.py to specify input and output file paths:
```Python
assign_drones("path/to/input.json", "path/to/output.json")
```
Run the script using:
```sh
python script.py
```

