import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def format_autopct(pct, allvals):
    absolute_value = int(round(pct/100.*np.sum(allvals)))
    return "${:,.2f}\n({:.1f}%)".format(absolute_value, pct)

def calculate_monthly_mortgage_payment(principal, months, monthly_interest_rate):
    return principal * (monthly_interest_rate * (1 + monthly_interest_rate) ** months) / ((1 + monthly_interest_rate) ** months - 1)

def calculate_monthly_pmi(home_price, down_payment_amount):
    down_payment_percentage = down_payment_amount / home_price
    
    if down_payment_percentage < 0.10:
        pmi_rate = 0.008
    elif down_payment_percentage < 0.15:
        pmi_rate = 0.0065
    elif down_payment_percentage < 0.20:
        pmi_rate = 0.005
    else:
        return 0.0, 0.0  # Return 0 for both PMI and rate if down payment is 20% or more

    monthly_pmi = pmi_rate * (home_price - down_payment_amount) / 12
    
    # Set a cap on PMI
    max_pmi = 300.0
    return min(monthly_pmi, max_pmi), pmi_rate * 100  # Multiplying by 100 to get the rate in percentage

def calculate_mortgage(home_price, down_payment_amount, mortgage_years, interest_rate, property_tax_rate, home_insurance, hoa_fee, maintenance_budget):
    closing_costs = home_price * 0.03
    total_cash_needed = down_payment_amount + closing_costs

    months = mortgage_years * 12
    monthly_interest_rate = interest_rate / 1200  # Dividing by (12*100) for monthly percentage

    monthly_mortgage = calculate_monthly_mortgage_payment(home_price - down_payment_amount, months, monthly_interest_rate)
    monthly_property_tax = (property_tax_rate / 100) * home_price / 12
    monthly_home_insurance = home_insurance / 12
    monthly_maintenance = maintenance_budget / 12
    monthly_pmi, pmi_rate = calculate_monthly_pmi(home_price, down_payment_amount)  # Capturing both PMI and rate
    
    total_monthly_payment = monthly_mortgage + monthly_property_tax + monthly_home_insurance + hoa_fee + monthly_maintenance + monthly_pmi

    return total_cash_needed, months, total_monthly_payment, monthly_pmi, pmi_rate  # Added pmi_rate to the return values

def create_pie_chart(total_monthly_payment_breakdown):
    labels = ['Mortgage', 'Property Tax', 'Home Insurance', 'HOA Fee', 'Maintenance', 'PMI']
    colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FFD700', '#D8BFD8']
    
    fig, ax = plt.subplots()
    ax.pie(total_monthly_payment_breakdown, labels=labels, colors=colors, autopct=lambda pct: format_autopct(pct, total_monthly_payment_breakdown), startangle=90)
    ax.axis('equal')
    ax.set_title("Monthly Costs Breakdown")
    
    st.pyplot(fig)
    
def create_horizontal_bar_chart_with_annotations(breakdown, labels):
    """
    Create a horizontal bar chart visualization of the monthly payment breakdown with annotations.
    """
    import matplotlib.pyplot as plt

    # Sort the data
    sorted_indices = sorted(range(len(breakdown)), key=lambda k: breakdown[k])
    sorted_breakdown = [breakdown[i] for i in sorted_indices]
    sorted_labels = [labels[i] for i in sorted_indices]
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Create the horizontal bar chart
    bars = ax.barh(sorted_labels, sorted_breakdown, color=plt.cm.Paired.colors)
    
    # Add annotations to the bars
    for bar in bars:
        width = bar.get_width()
        ax.text(width + (0.015 * max(sorted_breakdown)),  # + 1.5% of max value for padding
                bar.get_y() + bar.get_height() / 2, 
                '${:,.2f}'.format(width),
                ha='center', va='center', fontsize=9, color='black')
        
    ax.set_xlabel('Amount ($)')
    ax.set_title('Monthly Costs Breakdown')
    plt.tight_layout()
    st.pyplot(fig)


st.title("Mortgage Calculator")

# Create two columns for input
col1, col2 = st.columns(2)

# Inputs in the first column
with col1:
    home_price = st.number_input("Price of home:", min_value=100000.0, value=250000.0, step=1000.0)
    down_payment_amount = st.number_input("Down payment amount:", min_value=0.0, value=50000.0, step=1000.0)
    mortgage_years = st.selectbox("Mortgage length:", options=[15, 30], index=1)
    interest_rate = st.number_input("Interest rate %:", min_value=0.0, value=7.0, step=0.1)

# Inputs in the second column
with col2:
    property_tax_rate = st.number_input("Annual property tax rate:", min_value=0.0, value=1.25, step=0.1)
    home_insurance = st.number_input("Annual home insurance premium:", min_value=0.0, value=1200.0, step=100.0)
    maintenance_budget = st.number_input("Annual maintenance costs:", min_value=0.0, value=1500.0, step=100.0)
    hoa_fee = st.number_input("Monthly HOA fee:", min_value=0.0, value=60.0, step=10.0)

# Call the calculate_mortgage function after gathering user inputs
total_cash_needed, months, total_monthly_payment, monthly_pmi, pmi_rate = calculate_mortgage(
    home_price, down_payment_amount, mortgage_years, interest_rate, 
    property_tax_rate, home_insurance, hoa_fee, maintenance_budget)

# Create two columns for the Mortgage Details and Monthly Costs Breakdown
col3, col4 = st.columns(2)

# Display Mortgage Details in the first column
with col3:
    col3.markdown("### 🔑 **Mortgage Details**")
    
    # Create a markdown table with aligned values
    mortgage_details = f"""
    |                           |                         |
    |:--------------------------|------------------------:|
    | **Home Purchase Price:**  | `${home_price:,.0f}`    |
    | Down Payment:             | `${down_payment_amount:,.0f}` |
    | Closing Costs (3%):         | `${home_price * 0.03:,.0f}`   |
    | **Total Down Payment:**   | `${total_cash_needed:,.0f}`   |
    """
    col3.markdown(mortgage_details)

# Display Monthly Costs Breakdown in the second column
with col4:
    col4.markdown("### 💰 Monthly Costs")
    
    # Create a list of rows to be displayed in the table
    rows = [
        ("Mortgage:", calculate_monthly_mortgage_payment(home_price - down_payment_amount, months, interest_rate / 1200)),
        (f"Property Tax ({property_tax_rate}%):", (property_tax_rate / 100) * home_price / 12),
        ("Home Insurance:", home_insurance / 12),
        ("HOA Fee:", hoa_fee)
    ]
    
    # Check if PMI needs to be added
    if monthly_pmi > 0:
        rows.append((f"PMI costs ({pmi_rate:.2f}%):", monthly_pmi))
        
    rows.append(("Monthly Maintenance:", maintenance_budget / 12))
    
    # Construct the table
    table_header = "|                                  |                               |\n|:---------------------------------|------------------------------:|"
    table_rows = "\n".join([f"| {label} | `${value:,.2f}` |" for label, value in rows])
    
    # Combine the header and rows to form the full table
    monthly_costs = f"{table_header}\n{table_rows}"
    
    col4.markdown(monthly_costs)

# Display Monthly Payment and Pie Chart beneath the two columns
st.markdown("***")  # Horizontal line for visual break
st.markdown(f"### 🧾 Monthly Payment: `${total_monthly_payment:,.2f}`")

# Add the pie chart for the costs breakdown
total_monthly_payment_breakdown = [
    calculate_monthly_mortgage_payment(home_price - down_payment_amount, months, interest_rate / 1200),
    (property_tax_rate / 100) * home_price / 12,
    home_insurance / 12,
    hoa_fee,
    maintenance_budget / 12,
    monthly_pmi
]

# create_pie_chart(total_monthly_payment_breakdown)

# Labels for the horizontal bar chart
breakdown_labels = [
    "Mortgage",
    "Property Tax",
    "Home Insurance",
    "HOA Fee",
    "Maintenance",
    "PMI"
]

# Call the function to create a horizontal bar chart with annotations
create_horizontal_bar_chart_with_annotations(total_monthly_payment_breakdown, breakdown_labels)
