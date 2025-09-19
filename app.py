import streamlit as st
import numpy as np
import pandas as pd
from scipy.optimize import linprog

st.title("TV Delivery Optimizer")

st.markdown("""
**A company wishes to minimise its costs of delivering televisions from three depots (D1, D2 and D3) to three stores (Store 1, Store 2, and Store 3). The cost of delivering one TV is £5 per mile.
[Source](https://www.accaglobal.com/uk/en/student/exam-support-resources/professional-exams-study-resources/strategic-business-leader/technical-articles/big-data-sbl.html)**
""")

# -----------------------------
# Problem data
# -----------------------------
depot_labels = ["D1", "D2", "D3"]
depot_supply = [2500, 3100, 1250]

store_labels = ["Store 1", "Store 2", "Store 3"]
store_caps   = [2000, 3000, 2000]

distances = np.array([
    [22, 33, 40],  # D1 -> Stores 1–3
    [27, 30, 22],  # D2 -> Stores 1–3
    [36, 20, 25],  # D3 -> Stores 1–3
])

cost_per_mile = 5
c = (distances * cost_per_mile).flatten()

# -----------------------------
# Problem Setup (text only)
# -----------------------------
st.markdown("## Problem Setup")

dep_sentence = (
    f"There are {depot_supply[0]:,} TVs to be delivered from {depot_labels[0]}, "
    f"{depot_supply[1]:,} from {depot_labels[1]}, and "
    f"{depot_supply[2]:,} from {depot_labels[2]}."
)
store_sentence = (
    f"Store capacity limits are {store_caps[0]:,} for {store_labels[0]}, "
    f"{store_caps[1]:,} for {store_labels[1]}, and "
    f"{store_caps[2]:,} for {store_labels[2]}."
)

st.write(dep_sentence)
st.write(store_sentence)
st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------
# Build LP constraints
# -----------------------------
# Store (capacity) constraints: sum over depots to each store <= capacity
A_store = np.zeros((3, 9))
for j in range(3):
    for i in range(3):
        A_store[j, 3*i + j] = 1
b_store = store_caps

# Depot (supply) constraints: sum to all stores = supply
A_depot = np.zeros((3, 9))
for i in range(3):
    A_depot[i, 3*i:3*i+3] = 1
b_depot = depot_supply

bounds = [(0, None) for _ in range(9)]

# Solve
res = linprog(
    c=c,
    A_ub=A_store, b_ub=b_store,
    A_eq=A_depot, b_eq=b_depot,
    bounds=bounds,
    method="highs"
)

# -----------------------------
# Show Distance vs Plan side-by-side
# -----------------------------
st.markdown("## Plan")

def _centered_table_html(df: pd.DataFrame) -> str:
    return df.style.set_table_styles([
        {'selector': 'th', 'props': [('text-align', 'center')]},
        {'selector': 'td', 'props': [('text-align', 'center')]}
    ]).to_html()

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 🗺️ Distance Matrix (miles)")
    distance_df = pd.DataFrame(distances, index=depot_labels, columns=store_labels)
    st.markdown(_centered_table_html(distance_df), unsafe_allow_html=True)

with col_right:
    st.markdown("### ✅ Optimized TV Shipment Plan")
    if res.success:
        # reshape to 3x3 and round to integers for display
        x = np.round(res.x).astype(int).reshape(3, 3)
        shipment_df = pd.DataFrame(x, index=depot_labels, columns=store_labels)
        st.markdown(_centered_table_html(shipment_df), unsafe_allow_html=True)
    else:
        st.error("Optimization failed: " + res.message)

# Total cost
if res.success:
    total_cost = float(res.fun)
    st.write(f"### 💰 Total Delivery Cost: £{total_cost:,.0f}")


