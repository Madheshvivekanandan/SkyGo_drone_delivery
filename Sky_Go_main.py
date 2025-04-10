import streamlit as st
import json
import pandas as pd

# Function to calculate distance from origin (0, 0) to (x, y)
def distance(x, y):
    return abs(x) + abs(y)  # Sum of the absolute differences in x and y coordinates

# Main function to assign drones to orders
def assign_drones(data):
    drones = sorted(data["drones"]["fleet"], key=lambda d: (-d["speed"], -d["max_payload"], -d["max_distance"]))
    orders = sorted(data["orders"], key=lambda o: (-(o["delivery_x"] + o["delivery_y"])))

    assignments = []

    for drone in drones:
        if not drone["available"]:
            continue

        assigned_orders = []
        total_distance = 0
        remaining_payload = drone["max_payload"]
        remaining_distance = drone["max_distance"]

        for order in orders[:]:
            order_distance = distance(order["delivery_x"], order["delivery_y"])
            round_trip_distance = 2 * order_distance

            if (
                order["package_weight"] <= remaining_payload and
                round_trip_distance <= remaining_distance
            ):
                assigned_orders.append(order["id"])
                if total_distance == 0:
                    total_distance += round_trip_distance
                remaining_payload -= order["package_weight"]
                remaining_distance -= round_trip_distance
                orders.remove(order)

        if assigned_orders:
            assignments.append({
                "drone": drone["id"],
                "orders": assigned_orders,
                "total_distance": total_distance
            })

    assignments = sorted(assignments, key=lambda x: x["drone"])
    return {"assignments": assignments}

# Streamlit App
st.title("🚁 Drone Assignment System")
st.markdown("Upload your JSON file to assign drones to orders.")

# File uploader
uploaded_file = st.file_uploader("Upload JSON file", type=["json"])

if uploaded_file is not None:
    try:
        # Read JSON data
        data = json.load(uploaded_file)

        # Process the data
        result = assign_drones(data)

        # Convert assignments to DataFrame for display
        df = pd.json_normalize(result['assignments'], sep='_')

        st.subheader("📋 Assignment Results")
        st.dataframe(df)

        # Prepare downloadable JSON
        output_json = json.dumps(result, indent=4)
        st.download_button(
            label="📥 Download Output JSON",
            data=output_json,
            file_name="output.json",
            mime="application/json"
        )

    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("Please upload a JSON file to get started.")
