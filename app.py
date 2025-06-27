from pathlib import Path

# Create content for app.py
app_py = '''
import streamlit as st
import pandas as pd
import numpy as np
from pulp import LpMinimize, LpProblem, LpVariable, lpSum, value

st.title("TV Delivery Cost Optimiser")

st.markdown("### Input Data")

# Distance matrix
stores = ["Store 1", "Store 2", "Store 3"]
depots = ["D1", "D2", "D3"]

distance_data = {
    "Store 1": [22, 27, 36],
    "Store 2": [33, 30, 20],
    "Store 3": [40, 20, 25]
}
distances = pd.DataFrame(distance_data, index=depots)

# Demand and supply
store_demand = {"Store 1": 2000, "Store 2": 2850, "Store 3": 2100}
depot_supply = {"D1": 2500, "D2": 3100, "D3": 1250}

cost_per_mile = 5

st.write("### Distance Matrix (miles)")
st.dataframe(distances)

st.write("### Store Demand")
st.write(store_demand)

st.write("### Depot Supply")
st.write(depot_supply)

# Linear programming model
model = LpProblem("TV_Delivery_Optimization", LpMinimize)

# Decision variables
x = LpVariable.dicts("x", [(d, s) for d in depots for s in stores], lowBound=0, cat='Integer')

# Objective function
model += lpSum([x[(d, s)] * distances.loc[d, s] * cost_per_mile for d in depots for s in stores])

# Constraints
for s in stores:
    model += lpSum(x[(d, s)] for d in depots) == store_demand[s], f"Demand_{s}"

for d in depots:
    model += lpSum(x[(d, s)] for s in stores) <= depot_supply[d], f"Supply_{d}"

# Solve
model.solve()

# Output results
st.markdown("### Optimized Shipment Plan")
shipment_matrix = pd.DataFrame(0, index=depots, columns=stores)
for d in depots:
    for s in stores:
        shipment_matrix.loc[d, s] = int(x[(d, s)].varValue)

st.dataframe(shipment_matrix)

total_cost = value(model.objective)
st.markdown(f"### Total Delivery Cost: £{total_cost:,.2f}")
'''

# Create content for requirements.txt
requirements_txt = '''
streamlit
pulp
pandas
numpy
'''

# Create content for README.md
readme_md = '''
# TV Delivery Schedule Optimizer

This Streamlit web app uses Linear Programming to optimize the delivery schedule of TVs from depots to stores, minimizing the total transportation cost.

## Features

- Upload or use default depot-store distance matrix
- Define depot supply and store demand
- Optimized shipment plan using `pulp` LP solver
- Total transportation cost calculation

## How to Run

1. Clone this repository:
