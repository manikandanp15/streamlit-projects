import pandas as pd
import streamlit as st

st.set_page_config(page_title="Price Extractor - Fits Engineering", page_icon="📦")

# 🏢 Company Title
st.title("📦 Fits Engineering Products Pvt Ltd, Coimbatore")
st.subheader("Price Extractor")

# 📥 Upload Excel File
uploaded_file = st.file_uploader("Upload your pricing sheet", type=["xlsx", "xls"])

if uploaded_file:
    # Read Excel & Normalize Column Names
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip().str.lower()

    # 🔍 Enter Spec Size
    spec_input = st.text_input("Enter the Size (e.g., 8M NUT)").strip().lower()

    # Clean the 'size' column
    df['size'] = df['size'].astype(str).str.strip().str.lower()

    if spec_input:
        matched_rows = df[df['size'] == spec_input]

        if not matched_rows.empty:
            row = matched_rows.iloc[0]
            length = row.get('length inch', 'N/A')
            moq = row.get('moq', 'N/A')
            price_raw = row.get('final price', 'N/A')

            # Format price: round to 2 decimals
            try:
                price = round(float(price_raw), 2)
            except:
                price = "N/A"

            # 🟢 Display Results
            st.success(f"✅ Match found for `{spec_input}`:")
            st.write(f"**📏 Length:** {length} inch")
            st.write(f"**📦 MOQ:** {moq}")
            st.write(f"**💰 Final Price:** ₹{price}")
        else:
            st.error("❌ Spec not found. Please check the spelling or try another input.")
