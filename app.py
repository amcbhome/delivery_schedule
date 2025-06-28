import streamlit as st
import numpy as np
import pandas as pd
from scipy.optimize import linprog
import matplotlib.pyplot as plt
import plotly.graph_objects as go

st.title("TV Delivery Optimizer")

st.markdown("""
**A company wishes to minimise its costs of delivering televisions from three depots (D1, D2 and D3) to three stores (Store 1, Store 2, and Store 3). [Source](https://www.accaglobal.com/uk/en/student/exam-support-resources/professional-exams-study-resources/strategic-business-leader/technical-articles/big-data-sbl.html)**
""")

st.markdown("## Problem Setup")

# Depot and Store Data
depot_labels = ["D1", "D2", "D3"]
depot_supply = [2500, 3100, 1250]
store_labels = ["Store 1", "Store 2", "Store 3"]
store_caps = [2000, 3000, 2000]

st.markdown("### TV Delivery Data")
st.write("**TVs available at each depot:**")
st.table(pd.DataFrame({"Depot": depot_labels, "TVs Available": depot_supply}))

st.write("**Store capacity constraints:**")
st.table(pd.DataFrame({"Store": store_labels, "Capacity": store_caps}))

# Cost per mile
cost_per_mile = 5

# Distance Matrix
distances = np.array([
    [22, 33, 40],  # D1 to Stores 1–3
    [27, 30, 22],  # D2 to Stores 1–3
    [36, 20, 25],  # D3 to Stores 1–3
])

st.write("### Distance Matrix (miles)")
st.dataframe(pd.DataFrame(distances, index=depot_labels, columns=store_labels))

# Flatten distance matrix and apply cost multiplier
c = (distances * cost_per_mile).flatten()

# Constraints for stores (upper bounds)
A_store = np.zeros((3, 9))
for j in range(3):  # for each store
    for i in range(3):  # for each depot
        A_store[j, 3*i + j] = 1
b_store = store_caps

# Constraints for depots (equality)
A_depot = np.zeros((3, 9))
for i in range(3):  # for each depot
    A_depot[i, 3*i : 3*i+3] = 1
b_depot = depot_supply

# Bounds (x >= 0)
bounds = [(0, None) for _ in range(9)]

# Solve using SciPy linprog
res = linprog(
    c=c,
    A_ub=A_store,
    b_ub=b_store,
    A_eq=A_depot,
    b_eq=b_depot,
    bounds=bounds,
    method="highs"
)

st.markdown("## Optimization Results")

if res.success:
    x = np.round(res.x).astype(int).reshape(3, 3)
    shipment_df = pd.DataFrame(x, index=depot_labels, columns=store_labels)
    st.write("### Optimized TV Shipment Plan")
    st.dataframe(shipment_df)

    total_cost = res.fun
    st.write(f"### Total Delivery Cost: £{total_cost:,.2f}")

    # Sankey Diagram
    st.markdown("### 🔄 Shipment Flow Diagram (Sankey)")

    labels = depot_labels + store_labels
    source = []
    target = []
    value = []

    for i in range(3):  # depots
        for j in range(3):  # stores
            flow = x[i][j]
            if flow > 0:
                source.append(i)
                target.append(3 + j)
                value.append(flow)

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color="blue"
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            color="lightblue"
        ))])

    fig.update_layout(title_text="TV Shipments: Depot to Store Flow", font_size=12)
    st.plotly_chart(fig, use_container_width=True)

else:
    st.error("Optimization failed: " + res.message)

# LP Model Explanation
with st.expander("📐 Show Linear Programming Model"):
    st.latex(r"\text{Minimize:} \quad Z = \sum_{i=1}^{3} \sum_{j=1}^{3} x_{ij} \cdot d_{ij} \cdot 5")
    st.markdown("Where:")
    st.markdown("- \( x_{ij} \): Number of TVs delivered from depot \( i \) to store \( j \)")
    st.markdown("- \( d_{ij} \): Distance in miles between depot \( i \) and store \( j \)")
    st.markdown("- Cost per mile = £5")
    st.latex(r"\text{Subject to:}")
    st.latex(r"\sum_{i=1}^{3} x_{ij} \leq \text{Capacity}_j \quad \text{for each store } j")
    st.latex(r"\sum_{j=1}^{3} x_{ij} = \text{Supply}_i \quad \text{for each depot } i")
    st.latex(r"x_{ij} \geq 0 \quad \text{and continuous}")

# Constraint Check
with st.expander("📦 Store Capacity Constraints & Deliveries"):
    st.markdown("The delivery plan respects the store capacity limits:")

