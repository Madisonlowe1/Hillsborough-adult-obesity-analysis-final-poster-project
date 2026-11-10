#####################
# Madison Lowenstein #
# mlowenstein@usf.edu
# 11/22/2026 #
# Clean up health insurance variable csv #

# import
import pandas as pd

# Load the health insurance dataset
df = pd.read_csv('health_insurance.csv')

# replace missing values
df['pct_uninsured'] = df['pct_uninsured'].fillna(0.0)

# export cleaned csv
output_filename = 'health_insurance.csv'
df.to_csv(output_filename, index=False)

print("Health insurance parsed successfully:", len(df))