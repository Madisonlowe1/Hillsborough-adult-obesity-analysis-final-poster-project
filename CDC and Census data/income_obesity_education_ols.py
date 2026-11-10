###################################
#    Madison Lowenstein    #
# mlowenstein@usf.edu #
# 11/22/2026
# income_obesity_education OLS Regression #
####################################

# imports
import pandas as pd
import statsmodels.api as sm

# load dataset
df = pd.read_csv('hillsborough_obesity_income_merged.csv')

# filter the obesity rows
df_obesity = df[df['measure'].str.contains('obesity', case=False, na=False)].copy()

# specify variables/ drop missing rows
model_vars = ['data_value', 'median_income', 'pct_hs_or_higher']
df_clean = df_obesity.dropna(subset=model_vars)

print(f"Number of observations in regression model: {len(df_clean)}")

# define variables
y = df_clean['data_value']
X = df_clean[['median_income', 'pct_hs_or_higher']]

X = sm.add_constant(X)

# fit OLS model
model = sm.OLS(y, X).fit()

print(model.summary())
