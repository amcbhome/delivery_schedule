# TV Delivery Schedule Optimizer

This Streamlit web app uses Linear Programming to optimize the delivery schedule of TVs from depots to stores, minimizing the total transportation cost.

## 🚀 Features

- Uses default depot-store distance matrix and logistics values
- Defines depot supply and store demand constraints
- Solves with `pulp` (Python Linear Programming library)
- Outputs:
  - Optimized shipment matrix
  - Total cost of delivery

## 📊 Problem Description

- You must deliver TVs from 3 depots to 3 stores.
- Each store has a fixed demand.
- Each depot has a maximum supply.
- Delivery cost is calculated as:  
  `TVs shipped × Distance × £5 per mile`

This setup is inspired by the ACCA Strategic Business Leader technical article on cost forecasting and optimization.

## 📦 How to Run the App

1. **Clone this repository**:
   ```bash
   git clone https://github.com/yourusername/tv-delivery-optimizer.git
   cd tv-delivery-optimizer
