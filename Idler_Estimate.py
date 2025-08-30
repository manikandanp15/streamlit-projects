import streamlit as st
import pandas as pd
import math
from io import BytesIO

# Densities in g/cm³
MATERIAL_DENSITY = {
    "Mild Steel": 7.85,
    "Stainless Steel": 8.0
}

# Weight Calculations
def calc_pipe_weight(od, thickness, length, density):
    outer_radius = od / 2
    inner_radius = outer_radius - thickness
    volume_mm3 = math.pi * ((outer_radius**2 - inner_radius**2)) * length
    volume_cm3 = volume_mm3 / 1000
    weight_kg = (volume_cm3 * density) / 1000
    return round(weight_kg, 2)

def calc_shaft_weight(dia, length, density):
    radius = dia / 2
    volume_mm3 = math.pi * (radius**2) * length
    volume_cm3 = volume_mm3 / 1000
    weight_kg = (volume_cm3 * density) / 1000
    return round(weight_kg, 2)

# Session state
if "idler_data" not in st.session_state:
    st.session_state.idler_data = []

st.title("🔩 STEADFAST Idler/Roller Cost Estimator")

# RAG Placeholder
use_rag = st.checkbox("🔍 Use RAG to auto-fetch weights/prices (placeholder only)")

# Inputs
st.subheader("🧱 Material Selection")
material_type = st.selectbox("Select Material", ["Mild Steel", "Stainless Steel"])
density = MATERIAL_DENSITY[material_type]

st.subheader("🧮 Idler Dimensions")
idler_type = st.selectbox("Idler Type", ["Carrying", "Return", "Impact"])
pipe_od = st.number_input("Pipe Outside Diameter (mm)", min_value=10.0)
pipe_thickness = st.number_input("Pipe Thickness (mm)", min_value=1.0)
pipe_length = st.number_input("Pipe Length (mm)", min_value=50.0)
shaft_dia = st.number_input("Shaft Diameter (mm)", min_value=10.0)
shaft_length = st.number_input("Shaft Length (mm)", min_value=50.0)

st.subheader("📦 Raw Material Prices (₹/kg)")
pipe_price = st.number_input("Pipe Price", min_value=1.0)
shaft_price = st.number_input("Shaft Price", min_value=1.0)

pipe_weight = calc_pipe_weight(pipe_od, pipe_thickness, pipe_length, density)
shaft_weight = calc_shaft_weight(shaft_dia, shaft_length, density)

pipe_cost = pipe_weight * pipe_price
shaft_cost = shaft_weight * shaft_price

st.subheader("🛒 Bought-out Components (Auto x2)")
bearing_price = st.number_input("Bearing Price (each)", min_value=0.0)
cup_price = st.number_input("Cup Price (each)", min_value=0.0)
dustcover_price = st.number_input("Dust Cover Price (each)", min_value=0.0)
seal_price = st.number_input("Labyrinth Seal Price (each)", min_value=0.0)
circlip_price = st.number_input("Circlip Price (each)", min_value=0.0)

bought_out_cost = 2 * (bearing_price + cup_price + dustcover_price + seal_price + circlip_price)

rubber_ring_cost = 0
rubber_fixing_cost = 0
if idler_type == "Impact":
    st.subheader("🧩 Rubber Ring Details")
    num_rings = st.number_input("Number of Rubber Rings", min_value=0)
    cost_per_ring = st.number_input("Cost per Ring (₹)", min_value=0.0)
    rubber_fixing_cost = st.number_input("Fixing Charges (₹)", min_value=0.0)
    rubber_ring_cost = num_rings * cost_per_ring

st.subheader("⚙️ Conversion Costs")
machining_cost = st.number_input("Machining", min_value=0.0)
painting_cost = st.number_input("Painting", min_value=0.0)
testing_cost = st.number_input("Testing", min_value=0.0)

conversion_cost = machining_cost + painting_cost + testing_cost
base_cost = pipe_cost + shaft_cost + bought_out_cost + rubber_ring_cost + rubber_fixing_cost + conversion_cost

# Overhead and Profit
st.subheader("📈 Overhead & Profit")
profit_pct = st.slider("Select Profit Margin (%)", min_value=15, max_value=20, value=15)
overhead_cost = base_cost * 0.10
profit_cost = (base_cost + overhead_cost) * (profit_pct / 100)
final_cost = base_cost + overhead_cost + profit_cost

# Save entry
if st.button("➕ Add Idler"):
    label = f"{pipe_od}mmOD x {pipe_length}LG {idler_type} Idler ({material_type})"
    st.session_state.idler_data.append({
        "Company": "STEADFAST",
        "Material": material_type,
        "Idler Type": idler_type,
        "Pipe OD": pipe_od,
        "Pipe Length": pipe_length,
        "Pipe Weight (kg)": pipe_weight,
        "Shaft Weight (kg)": shaft_weight,
        "Pipe Cost (₹)": round(pipe_cost, 2),
        "Shaft Cost (₹)": round(shaft_cost, 2),
        "Bought-out Cost (₹)": round(bought_out_cost, 2),
        "Rubber Ring Cost (₹)": round(rubber_ring_cost, 2),
        "Rubber Fixing Cost (₹)": round(rubber_fixing_cost, 2),
        "Conversion Cost (₹)": round(conversion_cost, 2),
        "Overhead (10%) (₹)": round(overhead_cost, 2),
        "Profit Margin (%)": profit_pct,
        "Profit Cost (₹)": round(profit_cost, 2),
        "Final Cost (₹)": round(final_cost, 2),
        "Idler Label": label,
        "RAG Used": use_rag
    })
    st.success(f"✅ Added: {label} → ₹{round(final_cost, 2)}")

# Display & Export
if st.session_state.idler_data:
    st.subheader("📊 Estimation Summary")
    df = pd.DataFrame(st.session_state.idler_data)
    st.dataframe(df)

    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    st.download_button(
        label="📥 Download Excel",
        data=buffer.getvalue(),
        file_name="STEADFAST_idler_estimation.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
