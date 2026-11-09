####################
# Madison Lowenstein #
# merging the education variable #

import pandas as pd
import re

df_master = pd.read_csv('hillsborough_obesity_income_merged.csv')

# Clean up any old columns
for col in ['pct_hs_or_higher', 'pct_hs_or_higher_x', 'pct_hs_or_higher_y']:
    if col in df_master.columns:
        df_master = df_master.drop(columns=[col])

df_edu_raw = pd.read_csv('Education_Attainment.csv')

row_hs = df_edu_raw.iloc[14]

edu_data = []

for col in df_edu_raw.columns:
    if 'Percent!!Estimate' in col and 'Male' not in col:
        zcta_match = re.search(r'ZCTA5? (\d{5})', col)
        if zcta_match:
            zcta = zcta_match.group(1)
            val_str = str(row_hs[col]).replace('%', '').strip()
            try:
                pct_hs = float(val_str)
                edu_data.append({'ZCTA': zcta, 'pct_hs_or_higher': pct_hs})
            except ValueError:
                continue

df_edu_clean = pd.DataFrame(edu_data)
print("DEBUG: Number of education rows parsed:", len(df_edu_clean))
if len(df_edu_clean) > 0:
    print("DEBUG: Sample education ZCTAs:", df_edu_clean['ZCTA'].head(3).tolist())

# Fixed: Directly convert locationname to string and pad to 5 digits
df_master['clean_zcta'] = df_master['locationname'].astype(str).str.zfill(5)
print("DEBUG: Sample master clean_zctas:", df_master['clean_zcta'].head(3).tolist())

df_edu_clean['ZCTA'] = df_edu_clean['ZCTA'].astype(str).str.zfill(5)

df_merged = pd.merge(df_master, df_edu_clean, left_on='clean_zcta', right_on='ZCTA', how='inner')

if 'ZCTA' in df_merged.columns:
    df_merged = df_merged.drop(columns=['ZCTA'])
if 'clean_zcta' in df_merged.columns:
    df_merged = df_merged.drop(columns=['clean_zcta'])

df_merged.to_csv('hillsborough_obesity_income_merged.csv', index=False)

print("Education data successfully merged.")
print("New dataset shape:", df_merged.shape)
print(df_merged.head())