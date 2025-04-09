import streamlit as st
import json
import matplotlib.pyplot as plt
from io import BytesIO
from itertools import groupby

# --- Helper Functions ---

# Function to calculate Manhattan distance from (0,0)
def distance(x, y):
    return abs(x) + abs(y)

# Function to calculate Manhattan distance between two points
def distance_points(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)

# Visualization function
def visualize_assignments(assignments, orders_data):
    plt.figure(figsize=(6, 6))
    plt.title("Drone Assignments Visualization")

    # Draw origin
    plt.scatter(0, 0, color='blue', s=100, label='Origin (0,0)')

    # Prepare order points
    order_points = {order['id']: (order['delivery_x'], order['delivery_y']) for order in orders_data}

    # Plot orders
    for order_id, (x, y) in order_points.items():
        plt.scatter(x, y, color='green', s=50)
        plt.text(x + 0.2, y + 0.2, order_id, fontsize=8)

    # Draw lines from origin to assigned orders
    colors = ['red', 'purple', 'orange', 'cyan', 'magenta', 'brown']
    for idx, assignment in enumerate(assignments):
        color = colors[idx % len(colors)]
        for order_id in assignment['orders']:
            x, y = order_points[order_id]
            plt.plot([0, x], [0, y], linestyle='--', color=color, alpha=0.7)

    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    return buf

# Main assignment function
def assign_drones(data):
    drones = sorted(data["drones"]["fleet"], key=lambda d: (-d["speed"], -d["max_payload"], -d["max_distance"]))
    assignments = []
    flattened = data["orders"][:]

    for drone in drones:
        if not drone["available"]:
            continue

        assigned_orders = []
        total_distance = 0
        remaining_payload = drone["max_payload"]
        remaining_distance = drone["max_distance"]
        x_cordinate, y_cordinate = 0, 0

        orders_sorted = sorted(flattened, key=lambda o: -distance(o["delivery_x"], o["delivery_y"]))

        for order in orders_sorted[:]:
            order_distance = distance_points(x_cordinate, y_cordinate, order["delivery_x"], order["delivery_y"])
            if (order["package_weight"] <= remaining_payload and order_distance <= remaining_distance):
                assigned_orders.append(order["id"])
                total_distance += (order_distance * 2)
                remaining_payload -= order["package_weight"]
                remaining_distance -= order_distance
                x_cordinate, y_cordinate = order["delivery_x"], order["delivery_y"]
                flattened.remove(order)
                orders_sorted = sorted(flattened, key=lambda o: distance_points(x_cordinate, y_cordinate, o["delivery_x"], o["delivery_y"]))
            elif order == orders_sorted[-1]:
                total_distance += distance_points(order["delivery_x"], order["delivery_y"], 0, 0)

        if assigned_orders:
            assignments.append({
                "drone_id": drone["id"],
                "orders": assigned_orders,
                "total_distance": total_distance
            })

    return assignments

# --- Streamlit App ---
st.set_page_config(page_title="Drone Delivery Optimizer", layout="wide")
st.title("🚁 Drone Delivery Assignment Tool")

uploaded_file = st.file_uploader("Upload Input JSON", type="json")

if uploaded_file:
    data = json.load(uploaded_file)
    output = assign_drones(data)

    # Display in columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Assignment Output Table")
        st.dataframe(output)

        output_json = json.dumps(output, indent=4)
        st.download_button("Download Output JSON", output_json, file_name="output.json", mime="application/json")

    with col2:
        st.subheader("📈 Assignment Visualization")
        buf = visualize_assignments(output, data["orders"])
        st.image(buf)

else:
    st.info("Please upload a JSON file to get started!")
