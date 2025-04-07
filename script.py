import json  # Importing the JSON module to handle reading and writing JSON files

# Function to calculate distance from origin (0, 0) to (x, y)
def distance(x, y):
    return abs(x - 0) + abs(y - 0)  # Sum of the absolute differences in x and y coordinates

# Main function to assign drones to orders
def assign_drones(input_file, output_file):
    # Load input JSON data from the given file
    with open(input_file, "r") as f:
        data = json.load(f)

    # Sort drones based on priority: speed (descending), then max_payload (descending), then max_distance (descending)
    drones = sorted(data["drones"]["fleet"], key=lambda d: (-d["speed"], -d["max_payload"], -d["max_distance"]))

    # Sort orders based on delivery coordinates (sum of x and y), to prioritize farther orders
    orders = sorted(data["orders"], key=lambda o: (-(o["delivery_x"] + o["delivery_y"])))

    assignments = []  # List to store the final drone-to-order assignments

    # Iterate over each drone
    for drone in drones:
        if not drone["available"]:
            continue  # Skip drones that are not available

        assigned_orders = []  # List to store orders assigned to the current drone
        total_distance = 0  # Total distance drone will travel
        remaining_payload = drone["max_payload"]  # Initialize drone's payload capacity
        remaining_distance = drone["max_distance"]  # Initialize drone's travel distance capacity

        # Iterate over a copy of orders list, so we can modify the original list safely
        for order in orders[:]:
            order_distance = distance(order["delivery_x"], order["delivery_y"])  # Calculate distance to order
            round_trip_distance = 2 * order_distance  # Round-trip distance to deliver the order

            # Check if drone can carry this order and make the round trip
            if (
                order["package_weight"] <= remaining_payload and
                round_trip_distance <= remaining_distance
            ):
                assigned_orders.append(order["id"])  # Assign order to the drone
                if total_distance == 0:
                    total_distance += round_trip_distance  # Add the distance only once during the first assignment, as the orders are sorted in descending order by their distance from the origin.
                remaining_payload -= order["package_weight"]  # Update remaining payload capacity
                remaining_distance -= round_trip_distance  # Update remaining travel distance
                orders.remove(order)  # Remove the order from the available orders list

        # If any orders were assigned to the drone, record the assignment
        if assigned_orders:
            assignments.append({
                "drone": drone["id"],  # Drone ID
                "orders": assigned_orders,  # List of order IDs assigned to this drone
                "total_distance": total_distance  # Total distance travelled by this drone
            })

    # Sort the assignments list by drone ID for cleaner output
    assignments = sorted(assignments, key=lambda x: x["drone"])

    # Save the assignments to the output JSON file
    with open(output_file, "w") as f:
        json.dump({"assignments": assignments}, f, indent=4)

# Example usage of the function with input and output file paths
assign_drones(r"input.json", "output.json")
