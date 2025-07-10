import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Steadfast Salary App", layout="wide")
st.title("💼 Steadfast Super Salary & Expense App")

# Initialize session state
if 'salary_data' not in st.session_state:
    st.session_state.salary_data = []
if 'fixed_expenses' not in st.session_state:
    st.session_state.fixed_expenses = []

# Tabs for structure
tab1, tab2, tab3 = st.tabs(["🧑‍🏭 Salaries", "🏪 Expenses", "📤 Export"])

# --- Tab 1: Salary Entry ---
with tab1:
    st.subheader("🧾 Add Salary Entry")
    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input("Employee Name")
        salary_type = st.selectbox("Salary Type", ["Daily Wage", "Fixed Salary"])
    with col2:
        per_day = st.number_input("Per Day Rate", value=0.0, step=10.0) if salary_type == "Daily Wage" else 0.0
        fixed_salary = st.number_input("Fixed Salary", value=0.0, step=100.0) if salary_type == "Fixed Salary" else 0.0
    with col3:
        days_worked = st.number_input("Days Worked", value=0.0, step=1.0) if salary_type == "Daily Wage" else 0.0
        ot_hours = st.number_input("OT Hours", value=0.0, step=0.5) if salary_type == "Daily Wage" else 0.0
        advance = st.number_input("Advance Paid", value=0.0, step=100.0)

    if st.button("➕ Add Salary Entry"):
        ot_days = ot_hours / 8 if salary_type == "Daily Wage" else 0.0
        total_days = days_worked + ot_days
        total_amount = per_day * total_days if salary_type == "Daily Wage" else fixed_salary
        net_amount = total_amount - advance
        st.session_state.salary_data.append({
            'Name': name,
            'Type': salary_type,
            'Per Day': per_day,
            'Days Worked': days_worked,
            'OT Hours': ot_hours,
            'Advance': advance,
            'Total Amount': total_amount,
            'Net Amount': net_amount
        })
        st.success(f"Added {name}'s salary details.")

    if st.session_state.salary_data:
        st.markdown("### 👥 Salary Summary")
        st.dataframe(pd.DataFrame(st.session_state.salary_data))

# --- Tab 2: Fixed Expenses Entry ---
with tab2:
    st.subheader("🏪 Add Monthly Expense")
    col1, col2, col3 = st.columns(3)
    with col1:
        vendor = st.text_input("Vendor / Supplier Name")
        category = st.selectbox("Category", ["Rent", "Tea & Snacks", "Grocery", "Water Supply", "Cleaning", "Misc"])
    with col2:
        amount = st.number_input("Amount", value=0.0, step=50.0)
        remarks = st.text_input("Remarks")
    with col3:
        expense_date = st.date_input("Date", value=date.today())

    if st.button("➕ Add Expense Entry"):
        st.session_state.fixed_expenses.append({
            'Vendor': vendor,
            'Category': category,
            'Amount': amount,
            'Date': expense_date,
            'Remarks': remarks
        })
        st.success(f"Added expense for {vendor}.")

    if st.session_state.fixed_expenses:
        st.markdown("### 🧾 Expense Summary")
        st.dataframe(pd.DataFrame(st.session_state.fixed_expenses))

# --- Tab 3: Export Data ---
with tab3:
    st.subheader("📤 Export Monthly Report")
    if st.button("📥 Download Excel Report"):
        salary_df = pd.DataFrame(st.session_state.salary_data)
        expense_df = pd.DataFrame(st.session_state.fixed_expenses)

        with pd.ExcelWriter("Steadfast_Monthly_Report.xlsx") as writer:
            salary_df.to_excel(writer, sheet_name='Salaries', index=False)
            expense_df.to_excel(writer, sheet_name='Expenses', index=False)

        with open("Steadfast_Monthly_Report.xlsx", "rb") as f:
            st.download_button("📥 Click to Download", f, file_name="Steadfast_Monthly_Report.xlsx")
