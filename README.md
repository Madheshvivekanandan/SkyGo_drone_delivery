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
git clone https://github.com/Madheshvivekanandan/SkyGo_drone_delivery.git
cd SkyGo_drone_delivery
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
## Example
Modify script.py:
```Python
assign_drones("path/to/input.json", "path/to/output.json")
```
Then execute:
```sh
python script.py
```
## Input JSON Format
```json
{
    "drones": {
        "fleet": [
            {
                "id": "drone_1",
                "speed": 50,
                "max_payload": 10,
                "max_distance": 100,
                "available": true
            }
        ]
    },
    "orders": [
        {
            "id": "order_1",
            "delivery_x": 5,
            "delivery_y": 5,
            "package_weight": 5,
            "deadline": "2025-03-27T10:00:00"
        }
    ]
}
```
## Output JSON Example
```json
{
    "assignments": [
        {
            "drone": "drone_1",
            "orders": ["order_1"],
            "total_distance": 20
        }
    ]
}
```
## Notes
- Drones are assigned based on speed, payload, and max range.
- Orders are prioritized by deadline.
- Ensures that payload and distance constraints are met.
## Author
Madhesh Vivekanandan
