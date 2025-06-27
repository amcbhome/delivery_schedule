import streamlit as st
import numpy as np
import pandas as pd
from scipy.optimize import linprog

st.title("TV Delivery Optimizer (using SciPy)")

st.markdown("## Problem Setup")

cost_per_mile = 5

# Distances in miles from depots (rows) to stores (columns)
distances = np.array([
    [22, 33, 40],  # D1 to Stores 1–3
    [27, 30, 20],  # D2
    [36, 20, 25],  # D3
])
st.write("### Distance Matrix (miles)")
st.dataframe(pd.DataFrame(distances, index=["D1", "D2", "D3"], columns=["Store 1", "Store 2", "Store 3"]))

# Flatten distance matrix and apply cost multiplier
c = (distances * cost_per_mile).flatten()

# Store capacity constraints (upper bounds)
store_caps = [2000, 3000, 2000]  # S1, S2, S3

A_store = np.zeros((3, 9))
for j in range(3):  # for each store
    for i in range(3):  # for each depot
        A_store[j, 3*i + j] = 1
b_store = store_caps

# Depot supply constraints (equality)
depot_supply = [2500, 3100, 1250]  # D1, D2, D3

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
    shipment_df = pd.DataFrame(x, index=["D1", "D2", "D3"], columns=["Store 1", "Store 2", "Store 3"])
    st.write("### Optimized TV Shipment Plan")
    st.dataframe(shipment_df)

    total_cost = res.fun
    st.write(f"### Total Delivery Cost: £{total_cost:,.2f}")

else:
    st.error("Optimization failed: " + res.message)
