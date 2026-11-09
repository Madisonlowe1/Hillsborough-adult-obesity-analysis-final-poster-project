#################
# Madison Lowenstein #
# Combine Median income and Obesity #

import pandas as pd
import statsmodels.api as sm


cdc_df = pd.read_csv('cdc_hillsborough_zctas.csv')
census_df = pd.read_csv('cdc_and_census_data.csv', header=0, low_memory=False)


income_row = census_df[census_df.iloc[:, 0].astype(str).str.contains('Median income', case=False, na=False)]

income_records = []
for col in census_df.columns:
    if 'Estimate' in col and 'ZCTA5' in col:
        zcta = col.split('ZCTA5 ')[-1].split('!')[0].strip()
        val_str = income_row[col].values[0] if len(income_row) > 0 else None
        try:
            val = float(str(val_str).replace('$', '').replace(',', '').strip())
        except ValueError:
            val = None
        income_records.append({'LocationName': int(zcta), 'median_income': val})

income_df = pd.DataFrame(income_records).drop_duplicates(subset=['LocationName'])
cdc_df['locationname'] = cdc_df['locationname'].astype(int)


merged_df = pd.merge(cdc_df, income_df, left_on='locationname', right_on='LocationName', how='inner')


obesity_df = merged_df[merged_df['measureid'] == 'OBESITY'].dropna(subset=['data_value', 'median_income'])

X = sm.add_constant(obesity_df['median_income'])
y = obesity_df['data_value']

model = sm.OLS(y, X).fit()
print(model.summary())

merged_df.to_csv('hillsborough_obesity_income_merged.csv', index=False)
print("\nMerged dataset successfully saved to 'hillsborough_obesity_income_merged.csv'!")