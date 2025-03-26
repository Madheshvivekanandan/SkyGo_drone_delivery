import json

def distance(x, y):
    return abs(x - 0) + abs(y - 0)

def assign_drones(input_file, output_file):
    # Load input JSON
    with open(input_file, "r") as f:
        data = json.load(f)

    drones = sorted(data["drones"]["fleet"], key=lambda d: (-d["speed"], -d["max_payload"], -d["max_distance"]))  # Prioritize faster drones
    orders = sorted(data["orders"], key=lambda o: o["deadline"])  # Prioritize earlier deadlines
    assignments = []
    for drone in drones:
        if not drone["available"]:
            print(f"Drone {drone['id']} is not available.")
            continue  # Skip unavailable drones

        assigned_orders = []
        total_distance = 0
        remaining_payload = drone["max_payload"]
        remaining_distance = drone["max_distance"]

        for order in orders[:]:  # Copy to allow modification
            order_distance = distance(order["delivery_x"], order["delivery_y"])
            round_trip_distance = 2 * order_distance

            # Check constraints
            if (
                order["package_weight"] <= remaining_payload and
                round_trip_distance <= remaining_distance
            ):
                assigned_orders.append(order["id"])
                total_distance += round_trip_distance
                remaining_payload -= order["package_weight"]
                remaining_distance -= round_trip_distance
                orders.remove(order)  # Remove assigned order

        if assigned_orders:
            assignments.append({
                "drone": drone["id"],
                "orders": assigned_orders,
                "total_distance": total_distance
            })

    # Save output JSON
    with open(output_file, "w") as f:
        json.dump({"assignments": assignments}, f, indent=4)

# Example usage
assign_drones(r"C:\Users\m_vivekanandan\OneDrive - INFOTEL CONSEIL\Desktop\madmi\python\sample.json", "output.json")
