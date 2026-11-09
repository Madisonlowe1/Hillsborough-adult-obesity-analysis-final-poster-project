###################################
#    Madison Lowenstein    #
# income_obesity_education OLS Regression #
####################################

import pandas as pd
import statsmodels.api as sm

df = pd.read_csv('hillsborough_obesity_income_merged.csv')

df_obesity = df[df['measure'].str.contains('obesity', case=False, na=False)].copy()

model_vars = ['data_value', 'median_income', 'pct_hs_or_higher']
df_clean = df_obesity.dropna(subset=model_vars)

print(f"Number of observations in regression model: {len(df_clean)}")

y = df_clean['data_value']
X = df_clean[['median_income', 'pct_hs_or_higher']]

X = sm.add_constant(X)

model = sm.OLS(y, X).fit()

print(model.summary())
