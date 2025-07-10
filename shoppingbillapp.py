# shopping_bill_app.py

import streamlit as st

st.title("🛒 Shopping Bill Calculator")

st.write("Enter the prices of 3 items and tax percentage to calculate total bill.")

# Inputs
item1 = st.number_input("Price of Item 1 (₹)", min_value=0.0, step=0.5)
item2 = st.number_input("Price of Item 2 (₹)", min_value=0.0, step=0.5)
item3 = st.number_input("Price of Item 3 (₹)", min_value=0.0, step=0.5)
tax = st.slider("Tax Percentage (%)", 0.0, 100.0, 5.0)

# Calculate
subtotal = item1 + item2 + item3
tax_amount = (tax / 100) * subtotal
total = subtotal + tax_amount

# Display
st.write(f"### 🧾 Subtotal: ₹{subtotal:.2f}")
st.write(f"### 🧾 Tax @ {tax:.1f}%: ₹{tax_amount:.2f}")
st.success(f"💵 **Total Bill: ₹{total:.2f}**")
