##################################
# Madison Lowenstein #
# 11/22/2026 #
# Merge CDC adult obesity and median income data with other variables #
# creates ols regression model #
# mlowenstein@usf.edu #
##################################

# imports
import pandas as pd
import statsmodels.api as sm
from matplotlib import pyplot as plt

CDC_PATH = "cdc_hillsborough_pivoted.csv"
INCOME_OBESITY_PATH = "hillsborough_obesity_income_merged.csv"
EDU_PATH = "Education_Attainment.csv"
DEMO_PATH = "hillsborough_demographics_parsed.csv"
INS_PATH = "health_insurance.csv"
MAR_PATH = "marital_status_clean.csv"

# filter the obesity and income data
df_io = pd.read_csv(INCOME_OBESITY_PATH)
df_obesity_income = df_io[df_io['measure'].str.contains('Obesity among adults', case=False, na=False)].copy()
df_obesity_income['locationname'] = df_obesity_income['locationname'].astype(str).str.zfill(5)

df_obesity_income = df_obesity_income[['locationname', 'data_value', 'median_income']].rename(columns={'data_value': 'obesity_prevalence'})

# analyze education data
raw_edu = pd.read_csv(EDU_PATH)
edu_records = []
for col in raw_edu.columns:
    if 'ZCTA5' in col and 'Percent!!Estimate' in col:
        zcta = col.split('ZCTA5 ')[-1].split('!')[0].strip()
        try:
            bach_val = float(str(raw_edu.loc[12, col]).replace('%', '').strip())
        except (ValueError, TypeError):
            bach_val = 0.0
        try:
            grad_val = float(str(raw_edu.loc[13, col]).replace('%', '').strip())
        except (ValueError, TypeError):
            grad_val = 0.0
        pct_bach_higher = bach_val + grad_val
        edu_records.append({'locationname': str(zcta).zfill(5), 'pct_bach_higher': pct_bach_higher})

df_edu = pd.DataFrame(edu_records)

# load data into three dataframes
df_demo = pd.read_csv(DEMO_PATH)
df_demo['locationname'] = df_demo['locationname'].astype(str).str.zfill(5)

df_ins = pd.read_csv(INS_PATH)
df_ins['locationname'] = df_ins['locationname'].astype(str).str.zfill(5)

df_mar = pd.read_csv(MAR_PATH)
df_mar['locationname'] = df_mar['locationname'].astype(str).str.zfill(5)

df_master = df_obesity_income.merge(df_edu, how='inner', on='locationname')\
                              .merge(df_demo, how='inner', on='locationname')\
                              .merge(df_ins, how='inner', on='locationname')\
                              .merge(df_mar, how='inner', on='locationname')

master_filename = 'hillsborough_master_regression_data.csv'
df_master.to_csv(master_filename, index=False)
print(f"Master file saved at {master_filename} ({len(df_master)} rows)")

# Define parameters and create ols regression
Y_COL = "obesity_prevalence"
PREDICTOR_COLS = [
    "median_income",
    "pct_bach_higher",
    "pct_uninsured",
    "pct_married"
]

model_data = df_master[[Y_COL] + PREDICTOR_COLS].dropna()

X = sm.add_constant(model_data[PREDICTOR_COLS])
model = sm.OLS(model_data[Y_COL], X).fit()

print("\nMultivariate OLS Regression Summary:")
print(model.summary())

# Create plot figure
fig, ax = plt.subplots(figsize=(8, 6))
predicted_vals = model.fittedvalues
ax.scatter(predicted_vals, model_data[Y_COL], alpha=0.7, edgecolor="k", linewidth=0.3, color="blue", label="ZCTAs")

ax.set_xlabel("Predicted Obesity Prevalence (%)")
ax.set_ylabel("Actual Obesity Prevalence (%)")
ax.set_title(f"Actual vs. Predicted Obesity Prevalence (R² = {model.rsquared:.3f}, n = {len(model_data)})")
ax.grid(alpha=0.3, zorder=1)
ax.legend()
fig.tight_layout()

plot_filename = "hillsborough_obesity_actual_vs_predicted.png"
fig.savefig(plot_filename, dpi=300)
print(f"saved plot to {plot_filename}")

plt.show()
