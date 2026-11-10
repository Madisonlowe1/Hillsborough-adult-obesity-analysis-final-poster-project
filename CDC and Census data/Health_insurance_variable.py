#####################
# Madison Lowenstein #
# Clean up health insurance variable csv #

import pandas as pd

df = pd.read_csv('health_insurance.csv')

df['pct_uninsured'] = df['pct_uninsured'].fillna(0.0)


output_filename = 'health_insurance.csv'
df.to_csv(output_filename, index=False)

print("Health insurance parsed successfully:", len(df))