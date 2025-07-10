import streamlit as st

st.set_page_config(page_title="Number Comparison", page_icon="🔢")
st.title("🔢 Number Comparison App")

st.markdown("""
Compare two numbers and find out:
- Which is larger
- Which is smaller
- Or if they're equal
""")

# Input fields
num1 = st.number_input("Enter the first number:", format="%g")
num2 = st.number_input("Enter the second number:", format="%g")

# Compare button
if st.button("Compare"):
    if num1 > num2:
        st.success(f"✅ {num1} is greater than {num2}")
    elif num1 < num2:
        st.info(f"ℹ️ {num1} is smaller than {num2}")
    else:
        st.warning("⚖️ Both numbers are equal")

st.markdown("---")
st.caption("Made for Day 6/50 - AI Python Challenge 🧠")
