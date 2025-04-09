import json
import matplotlib.pyplot as plt
from itertools import groupby

# Function to calculate Manhattan distance from (0,0)
def distance(x, y):
    return abs(x) + abs(y)

# Function to calculate Manhattan distance between two points
def distance_points(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)

# Main assignment function
def assign_drones(input_file, output_file):
    with open(input_file, "r") as f:
        data = json.load(f)

    drones = sorted(data["drones"]["fleet"], key=lambda d: (-d["speed"], -d["max_payload"], -d["max_distance"]))

    assignments = []
    for drone in drones:
        if not drone["available"]:
            continue

        assigned_orders = []
        total_distance = 0
        remaining_payload = drone["max_payload"]
        remaining_distance = drone["max_distance"]
        x_cordinate, y_cordinate = 0, 0

        if not assignments:
            orders_sorted = sorted(data["orders"], key=lambda o: -distance(o["delivery_x"], o["delivery_y"]))
        else:
            orders_sorted = sorted(flattened, key=lambda o: -distance(o["delivery_x"], o["delivery_y"]))

        flattened = orders_sorted

        for order in flattened[:]:  # Copy of list for safe removal
            order_distance = distance_points(x_cordinate, y_cordinate, order["delivery_x"], order["delivery_y"])
            if (order["package_weight"] <= remaining_payload and order_distance <= remaining_distance):
                assigned_orders.append(order["id"])
                total_distance += (order_distance*2)  # Round trip distance
                remaining_payload -= order["package_weight"]
                remaining_distance -= order_distance
                x_cordinate, y_cordinate = order["delivery_x"], order["delivery_y"]
                flattened.remove(order)

                # Sort remaining orders based on proximity to current position
                flattened = sorted(flattened, key=lambda o: distance_points(x_cordinate, y_cordinate, o["delivery_x"], o["delivery_y"]))
            elif order == flattened[-1]:
                total_distance += distance_points(order["delivery_x"], order["delivery_y"], 0, 0)

        if assigned_orders:
            assignments.append({
                "drone_id": drone["id"],
                "orders": assigned_orders,
                "total_distance": total_distance
            })

    # Write results to output file
    with open(output_file, "w") as f:
        json.dump(assignments, f, indent=4)

# Example usage
assign_drones("sample.json", "output.json")
