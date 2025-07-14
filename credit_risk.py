# Import libraries and set dimensions for data

import numpy as np

import pandas as pd

import random

from datetime import datetime, timedelta

from faker import Faker

fake = Faker()

product_types = ['Mortgage', 'Auto Loan', 'Personal Loan', 'Business Loan', 'Credit Card']

credit_grades = ['AAA', 'AA', 'A', 'BBB', 'BB', 'B', 'CCC', 'CC', 'C', 'D']

num_rows = 1000

# 1. Loan Master Table

# Create base values
loan_ids = [f"LN{100000 + i}" for i in range(num_rows)]
customer_ids = [f"CUST{1000 + i}" for i in range(num_rows)]
origination_dates = [fake.date_between(start_date='-5y', end_date='-1y') for _ in range(num_rows)]
maturity_dates = [orig_date + timedelta(days=random.randint(365*1, 365*10)) for orig_date in origination_dates]
loan_amounts = np.round(np.random.uniform(5000, 500000, size=num_rows), 2)
interest_rates = np.round(np.random.uniform(2.5, 15.0, size=num_rows), 2)
product_types_sample = [random.choice(product_types) for _ in range(num_rows)]
credit_grades_sample = [random.choice(credit_grades) for _ in range(num_rows)]
risk_scores = np.round(np.random.uniform(300, 850, size=num_rows), 0).astype(int)

# Assemble the data
data = {
    'Loan_ID': loan_ids,
    'Customer_ID': customer_ids,
    'Origination_Date': origination_dates,
    'Maturity_Date': maturity_dates,
    'Loan_Amount': loan_amounts,
    'Interest_Rate': interest_rates,
    'Product_Type': product_types_sample,
    'Credit_Grade': credit_grades_sample,
    'Risk_Score': risk_scores
}

# Create DataFrame and export as CSV
loan_master_df = pd.DataFrame(data)
file_path = "/mnt/data/loan_master_table_sample.csv"
loan_master_df.to_csv(file_path, index=False)

file_path

# 2. Customer Demographics
regions = ['North America', 'Europe', 'Asia', 'South America', 'Africa']
countries = {
    'North America': ['USA', 'Canada'],
    'Europe': ['UK', 'Germany', 'France'],
    'Asia': ['India', 'China', 'Japan'],
    'South America': ['Brazil', 'Argentina'],
    'Africa': ['South Africa', 'Nigeria']
}
segments = ['Retail', 'SME', 'Corporate']
industries = ['Manufacturing', 'Finance', 'Healthcare', 'Retail', 'Technology', 'Logistics']

customer_data = {
    'Customer_ID': customer_ids,
    'Region': [random.choice(regions) for _ in range(num_rows)],
    'Segment': [random.choice(segments) for _ in range(num_rows)],
    'Industry': [random.choice(industries) for _ in range(num_rows)]
}
# Assign countries based on region
customer_data['Country'] = [random.choice(countries[region]) for region in customer_data['Region']]

customer_df = pd.DataFrame(customer_data)
customer_path = "/mnt/data/customer_demographics.csv"
customer_df.to_csv(customer_path, index=False)

# 3. Exposure Data
ead_current = np.round(np.random.uniform(1000, 500000, size=num_rows), 2)
ead_projected = ead_current + np.round(np.random.uniform(100, 10000, size=num_rows), 2)
collateral_value = np.round(ead_current * np.random.uniform(0.5, 1.5, size=num_rows), 2)
utilization_rate = np.round(np.random.uniform(0.2, 1.0, size=num_rows), 2)

exposure_data = {
    'Loan_ID': loan_ids,
    'EAD_Current': ead_current,
    'EAD_Projected': ead_projected,
    'Collateral_Value': collateral_value,
    'Utilization_Rate': utilization_rate
}

exposure_df = pd.DataFrame(exposure_data)
exposure_path = "/mnt/data/exposure_data.csv"
exposure_df.to_csv(exposure_path, index=False)

# 4. Default & Delinquency Data
days_past_due = [random.choice([0, 30, 60, 90, 120]) for _ in range(num_rows)]
default_flags = [1 if days > 90 else 0 for days in days_past_due]
default_dates = [fake.date_between(start_date='-1y', end_date='today') if flag else None for flag in default_flags]
recovery_amount = [round(random.uniform(0, ead) if flag else 0, 2) for flag, ead in zip(default_flags, ead_current)]
recovery_dates = [fake.date_between(start_date=dd, end_date='today') if dd else None for dd in default_dates]

default_data = {
    'Loan_ID': loan_ids,
    'Days_Past_Due': days_past_due,
    'Default_Flag': default_flags,
    'Default_Date': default_dates,
    'Recovery_Amount': recovery_amount,
    'Recovery_Date': recovery_dates
}

default_df = pd.DataFrame(default_data)
default_path = "/mnt/data/default_delinquency_data.csv"
default_df.to_csv(default_path, index=False)

# 5. Expected Credit Loss Table
stages = [random.choices([1, 2, 3], weights=[0.7, 0.2, 0.1])[0] for _ in range(num_rows)]
pd_vals = np.round(np.random.uniform(0.01, 0.5, size=num_rows), 4)
lgd_vals = np.round(np.random.uniform(0.1, 0.9, size=num_rows), 2)
ecl_12m = np.round(ead_current * pd_vals * lgd_vals, 2)
ecl_lifetime = np.round(ecl_12m * np.random.uniform(1.5, 3.0, size=num_rows), 2)

ecl_data = {
    'Loan_ID': loan_ids,
    'Stage': stages,
    '12M_ECL': ecl_12m,
    'Lifetime_ECL': ecl_lifetime,
    'PD': pd_vals,
    'LGD': lgd_vals
}

ecl_df = pd.DataFrame(ecl_data)
ecl_path = "/mnt/data/ecl_table.csv"
ecl_df.to_csv(ecl_path, index=False)

# 6. Payment History
num_payments = 5
payment_history = []
for i in range(num_rows):
    base_date = origination_dates[i]
    for j in range(num_payments):
        pay_date = base_date + timedelta(days=30 * j)
        scheduled = round(loan_amounts[i] / num_payments, 2)
        actual = scheduled if random.random() > 0.1 else 0  # 10% chance of missed payment
        missed = 1 if actual == 0 else 0
        payment_history.append([
            loan_ids[i], pay_date, scheduled, actual, missed
        ])

payment_df = pd.DataFrame(payment_history, columns=[
    'Loan_ID', 'Payment_Date', 'Scheduled_Payment', 'Actual_Payment', 'Missed_Payment_Flag'
])
payment_path = "/mnt/data/payment_history.csv"
payment_df.to_csv(payment_path, index=False)

# Return file paths
{
    "Customer Demographics": customer_path,
    "Exposure Data": exposure_path,
    "Default & Delinquency": default_path,
    "ECL Table": ecl_path,
    "Payment History": payment_path
}
