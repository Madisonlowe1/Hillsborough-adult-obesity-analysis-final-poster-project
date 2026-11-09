#################
# adding physical inactivity variable #

import pandas as pd


cdc_df = pd.read_csv('cdc_hillsborough_zctas.csv')

cdc_pivoted = cdc_df.pivot(
    index='locationname',
    columns='measureid',
    values='data_value'
).reset_index()

cdc_pivoted = cdc_pivoted.rename(columns={
    'OBESITY': 'obesity_prevalence',
    'LPA': 'physical_inactivity',
})

cdc_pivoted['locationname'] = cdc_pivoted['locationname'].astype(str).str.zfill(5)

cdc_pivoted.to_csv('cdc_hillsborough_pivoted.csv', index=False)
print("CDC data pivoted and saved successfully. Shape:", cdc_pivoted.shape)