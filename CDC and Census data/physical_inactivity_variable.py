#####################
# Madison Lowenstein #
# physical inactivity variable #

import pandas as pd

cdc_df = pd.read_csv('cdc_hillsborough_zctas.csv')

cdc_pivoted = cdc_df.pivot(
    index='locationname',
    columns='measureid',
    values='data_value'
).reset_index()

cdc_pivoted = cdc_pivoted.rename(columns={
    'OBESITY': 'obesity_prevelance',
    'LPA': 'physical_inactivity',
})

print(cdc_pivoted.head())