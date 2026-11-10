#################
# Madison Lowenstein #
# mlowenstein@usf.edu #
# 11/22/2026 #
# adding physical inactivity variable #

# import
import pandas as pd

# load the filtered dataset
cdc_df = pd.read_csv('cdc_hillsborough_zctas.csv')

# reshape dataframe
cdc_pivoted = cdc_df.pivot(
    index='locationname',
    columns='measureid',
    values='data_value'
).reset_index()

# rename columns
cdc_pivoted = cdc_pivoted.rename(columns={
    'OBESITY': 'obesity_prevalence',
    'LPA': 'physical_inactivity',
})

cdc_pivoted['locationname'] = cdc_pivoted['locationname'].astype(str).str.zfill(5)

# export pivoted dataset
cdc_pivoted.to_csv('cdc_hillsborough_pivoted.csv', index=False)
print("CDC data pivoted and saved successfully. Shape:", cdc_pivoted.shape)