import streamlit as st
import pandas as pd
import math
from io import BytesIO
import os

# Constants
MATERIAL_DENSITY = {"Mild Steel": 7.85, "Stainless Steel": 8.0}
MASTER_FILE = "idler_master.xlsx"

# Load master sheet
def load_master():
    if os.path.exists(MASTER_FILE):
        return pd.read_excel(MASTER_FILE)
    else:
        return pd.DataFrame()

# Save new entry to master
def save_to_master(entry):
    df = load_master()
    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    df.to_excel(MASTER_FILE, index=False)

# Match pipe size
def match_pipe(pipe_od, shaft_dia):
    df = load_master()
    match = df[(df["Pipe OD"] == pipe_od) & (df["Shaft Dia"] == shaft_dia)]
    return match.iloc[0] if not match.empty else None

# Weight calculations
def calc_pipe_weight(od, thickness, length, density):
    outer_radius = od / 2
    inner_radius = outer_radius - thickness
    volume_mm3 = math.pi * ((outer_radius**2 - inner_radius**2)) * length
    volume_cm3 = volume_mm3 / 1000
    return round((volume_cm3 * density) / 1000, 2)

def calc_shaft_weight(dia, length, density):
    radius = dia / 2
    volume_mm3 = math.pi * (radius**2) * length
    volume_cm3 = volume_mm3 / 1000
    return round((volume_cm3 * density) / 1000, 2)

# UI
st.title("🔩 STEADFAST Intelligent Idler Estimator")

use_rag = st.checkbox("Use RAG to auto-fetch component costs")

material = st.selectbox("Material", ["Mild Steel", "Stainless Steel"])
density = MATERIAL_DENSITY[material]

st.subheader("📂 Upload Existing Idler Specs")
uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file:
    uploaded_df = pd.read_excel(uploaded_file, header=None)  # Read without headers
    data_dict = dict(zip(uploaded_df.iloc[:, 1], uploaded_df.iloc[:, 2]))

# Access values safely (or handle missing ones gracefully)
pipe_od = data_dict.get("Pipe OD")
shaft_dia = data_dict.get("Shaft Dia")

# Construct a DataFrame to use for matching
new_entry_df = pd.DataFrame([{
    "Pipe OD": pipe_od,
    "Shaft Dia": shaft_dia
}])

 
idler_type = st.selectbox("Idler Type", ["Carrying", "Return", "Impact"])
pipe_od = st.number_input("Pipe OD (mm)", min_value=10.0)
pipe_thickness = st.number_input("Pipe Thickness (mm)", min_value=1.0)
pipe_length = st.number_input("Pipe Length (mm)", min_value=50.0)
shaft_dia = st.number_input("Shaft Dia (mm)", min_value=10.0)
shaft_length = st.number_input("Shaft Length (mm)", min_value=50.0)

pipe_price = st.number_input("Pipe Price (₹/kg)", min_value=1.0)
shaft_price = st.number_input("Shaft Price (₹/kg)", min_value=1.0)

pipe_weight = calc_pipe_weight(pipe_od, pipe_thickness, pipe_length, density)
shaft_weight = calc_shaft_weight(shaft_dia, shaft_length, density)
pipe_cost = pipe_weight * pipe_price
shaft_cost = shaft_weight * shaft_price

# RAG or manual entry
if use_rag:
    match = match_pipe(pipe_od, shaft_dia)
    if match is not None:
        bearing_cost = match["Bearing Cost"] * 2
        cup_cost = match["Cup Cost"] * 2
        seal_cost = match["Seal Cost"] * 2
        circlip_cost = match["Circlip Cost"] * 2
        painting = match["Painting"]
        welding = match["Welding"]
        handling = match["Handling"]
        pipe_machining = match["Pipe Machining"]
        rod_machining = match["Rod Machining"]
        rod_milling = match["Rod Milling"]
        assembly = match["Assembly"]
    else:
        st.warning("Pipe size not found. Please enter manually.")
        bearing_cost = st.number_input("Bearing Cost (each)", min_value=0.0) * 2
        cup_cost = st.number_input("Cup Cost (each)", min_value=0.0) * 2
        seal_cost = st.number_input("Seal Set Cost (each)", min_value=0.0) * 2
        circlip_cost = st.number_input("Circlip Cost (each)", min_value=0.0) * 2
        painting = st.number_input("Painting Cost", min_value=0.0)
        welding = st.number_input("Welding Cost", min_value=0.0)
        handling = st.number_input("Handling Cost", min_value=0.0)
        pipe_machining = st.number_input("Pipe Machining Cost", min_value=0.0)
        rod_machining = st.number_input("Rod Machining Cost", min_value=0.0)
        rod_milling = st.number_input("Rod Milling Cost", min_value=0.0)
        assembly = st.number_input("Assembly Cost", min_value=0.0)

        # Save new entry
        new_entry = {
            "Pipe OD": pipe_od,
            "Shaft Dia": shaft_dia,
            "Bearing Cost": bearing_cost / 2,
            "Cup Cost": cup_cost / 2,
            "Seal Cost": seal_cost / 2,
            "Circlip Cost": circlip_cost / 2,
            "Painting": painting,
            "Welding": welding,
            "Handling": handling,
            "Pipe Machining": pipe_machining,
            "Rod Machining": rod_machining,
            "Rod Milling": rod_milling,
            "Assembly": assembly
        }
        save_to_master(new_entry)
else:
    bearing_cost = st.number_input("Bearing Cost (each)", min_value=0.0) * 2
    cup_cost = st.number_input("Cup Cost (each)", min_value=0.0) * 2
    seal_cost = st.number_input("Seal Set Cost (each)", min_value=0.0) * 2
    circlip_cost = st.number_input("Circlip Cost (each)", min_value=0.0) * 2
    painting = st.number_input("Painting Cost", min_value=0.0)
    welding = st.number_input("Welding Cost", min_value=0.0)
    handling = st.number_input("Handling Cost", min_value=0.0)
    pipe_machining = st.number_input("Pipe Machining Cost", min_value=0.0)
    rod_machining = st.number_input("Rod Machining Cost", min_value=0.0)
    rod_milling = st.number_input("Rod Milling Cost", min_value=0.0)
    assembly = st.number_input("Assembly Cost", min_value=0.0)

rubber_cost = 0
fixing_cost = 0
if idler_type == "Impact":
    num_rings = st.number_input("Number of Rubber Rings", min_value=0)
    cost_per_ring = st.number_input("Cost per Ring", min_value=0.0)
    fixing_cost = st.number_input("Fixing Charges", min_value=0.0)
    rubber_cost = num_rings * cost_per_ring

profit_pct = st.slider("Profit Margin (%)", min_value=15, max_value=20, value=15)

# Final cost calculation
base = pipe_cost + shaft_cost + bearing_cost + cup_cost + seal_cost + circlip_cost + \
       painting + welding + handling + pipe_machining + rod_machining + rod_milling + \
       assembly + rubber_cost + fixing_cost

overhead = base * 0.10
profit = (base + overhead) * (profit_pct / 100)
final = base + overhead + profit

if st.button("➕ Add to Estimation"):
    label = f"{pipe_od}mmOD x {pipe_length}LG {idler_type} Idler ({material})"
    entry = {
    "Label": label,
    "Pipe Cost": round(pipe_cost, 2),
    "Shaft Cost": round(shaft_cost, 2),
    "Component Cost": round(bearing_cost + cup_cost + seal_cost + circlip_cost, 2),
    "Rubber Cost": round(rubber_cost + fixing_cost, 2),
    "Conversion Cost": round(painting + welding + handling + pipe_machining + 
                             rod_machining + rod_milling + assembly, 2),
    "Overhead": round(overhead, 2),
    "Profit": round(profit, 2),
    "Final Cost": round(final, 2)
}
