import streamlit as st
import math

def calculate_mortgage(home_price, down_payment_percent, mortgage_years, interest_rate, property_tax_rate, home_insurance, current_savings, months_to_buy):
    down_payment_percent /= 100

    down_payment_amount = home_price * down_payment_percent
    closing_costs = home_price * 0.03
    total_cash_needed = down_payment_amount + closing_costs

    months = mortgage_years * 12
    monthly_interest_rate = interest_rate / (12 * 100)
    monthly_property_tax = (property_tax_rate / 100) * home_price / 12
    monthly_home_insurance = home_insurance / 12

    monthly_payment = (home_price - down_payment_amount) * (monthly_interest_rate * pow(1 + monthly_interest_rate, months)) / (pow(1 + monthly_interest_rate, months) - 1)
    total_monthly_payment = monthly_payment + monthly_property_tax + monthly_home_insurance

    cash_needed_per_month = (total_cash_needed - current_savings) / months_to_buy

    return int(total_cash_needed), months, total_monthly_payment, cash_needed_per_month


def calculate_pmi_price(home_price, down_payment_percent, loan_term_years, credit_score):
    # Calculate loan amount based on purchase price and down payment percentage
    loan_amount = home_price * (1 - down_payment_percent/100)

    # Set PMI rate to 0 if down payment is 20% or more
    if down_payment_percent >= 20:
        pmi_rate = 0
    else:
        # Calculate PMI rate based on loan-to-value (LTV) ratio and credit score
        ltv_ratio = loan_amount / home_price
        if ltv_ratio > 0.9:
            if credit_score >= 760:
                pmi_rate = 0.0045 # PMI rate for LTV ratio > 90% and credit score >= 760
            elif 740 <= credit_score < 760:
                pmi_rate = 0.0075 # PMI rate for LTV ratio > 90% and credit score between 740 and 759
            elif 720 <= credit_score < 740:
                pmi_rate = 0.0075 # PMI rate for LTV ratio > 90% and credit score between 720 and 739
            else:
                pmi_rate = 0.0075 # PMI rate for LTV ratio > 90% and credit score < 720
        elif ltv_ratio > 0.85:
            if credit_score >= 760:
                pmi_rate = 0.0035 # PMI rate for LTV ratio > 85% and credit score >= 760
            elif 740 <= credit_score < 760:
                pmi_rate = 0.0055 # PMI rate for LTV ratio > 85% and credit score between 740 and 759
            elif 720 <= credit_score < 740:
                pmi_rate = 0.0075 # PMI rate for LTV ratio > 85% and credit score between 720 and 739
            else:
                pmi_rate = 0.0075 # PMI rate for LTV ratio > 85% and credit score < 720
        else:
            if credit_score >= 760:
                pmi_rate = 0.0023 # PMI rate for LTV ratio <= 85% and credit score >= 760
            elif 740 <= credit_score < 760:
                pmi_rate = 0.0036 # PMI rate for LTV ratio <= 85% and credit score between 740 and 759
            elif 720 <= credit_score < 740:
                pmi_rate = 0.0050 # PMI rate for LTV ratio <= 85% and credit score between 720 and 739
            else:
                pmi_rate = 0.0075 # PMI rate for LTV ratio <= 85% and credit score < 720

    # Calculate monthly PMI payment
    pmi_price = loan_amount * pmi_rate / 12
    return pmi_price


st.title("Mortgage Calculator")

# Input variables
home_price = st.number_input("Enter the price of the home:", min_value=100000.0, value=250000.0, step=1000.0)
down_payment_percent = st.slider("Down payment percentage:", min_value=0.0, max_value=100.0, value=20.0, step=1.0)
mortgage_years = st.number_input("Enter the length of mortgage in years:", min_value=1, max_value=50, value=30, step=1)
interest_rate = st.number_input("Enter the interest rate (as a percentage):", min_value=0.0, value=5.0, step=0.1)
property_tax_rate = st.number_input("Enter the annual property tax rate (as a percentage):", min_value=0.0, value=1.0, step=0.1)
home_insurance = st.number_input("Enter the annual home insurance premium:", min_value=0.0, value=1000.0, step=100.0)
current_savings = st.number_input("Enter the current amount of savings:", min_value=0.0, value=20000.0, step=100.0)
monthly_contribution = st.number_input("Enter your monthly savings contribution:", min_value=0.0, value=2000.0, step=100.0)
credit_score = st.number_input("Enter your credit score:", min_value=0.0, max_value=850.0, value=780.0, step=10.0)
months_to_buy = st.number_input("How many months until you plan to purchase a home:", min_value=0, value=12, step=1)

# Calculate results
total_cash_needed, months, total_monthly_payment, cash_needed_per_month = calculate_mortgage(home_price, down_payment_percent, mortgage_years, interest_rate, property_tax_rate, home_insurance, current_savings, months_to_buy)
pmi_price = calculate_pmi_price(home_price, down_payment_percent, mortgage_years, credit_score)
total_monthly_payment += pmi_price
months_to_target = math.ceil((total_cash_needed - current_savings) / monthly_contribution)

on_track = 1 if (monthly_contribution * months_to_buy) + current_savings >= total_cash_needed else 0

if on_track:
    st.write("You are on track with your savings!")
   
st.write("House Price: ${:,.2f}".format(home_price))
st.write("{}% down payment + closing costs: ${:,}".format(int(down_payment_percent), total_cash_needed))
if pmi_price == 0.0:
    st.write("Monthly payment amount: ${:,.2f} | Interest rate: {}% | {} year fixed mortgage.".format(total_monthly_payment, interest_rate, mortgage_years))
else:
    st.write("Monthly payment amount: ${:,.2f} | Monthly PMI: {:,.2f} | Interest rate: {}%  |   {} year fixed mortgage.".format(total_monthly_payment, pmi_price, interest_rate, mortgage_years))
st.write("You will need to save ${:,.2f} per month for the next {} months to hit your target. Otherwise, it will take you {} months to hit your target with your current savings.".format(cash_needed_per_month, months_to_buy, months_to_target))

    
# property tax and HOA