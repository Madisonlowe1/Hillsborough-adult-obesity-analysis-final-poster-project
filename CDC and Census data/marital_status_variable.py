#####################
# Madison Lowenstein #
# Marital staus variable csv cleanup #

import pandas as pd

df = pd.read_csv('marital_status.csv')

total_col = [c for c in df.columns if 'Total!!Estimate' in c]
married_cols = [c for c in df.columns if 'Now married (except separated)!!Estimate' in c]

rows = []

for t_col, m_col in zip(total_col, married_cols):
    zcta = t_col.split('!!')[0].replace('ZCTA5', '').strip().zfill(5)

    married_str = str(df.loc[0, m_col]).replace('%', '').replace(',', '').strip()
    pct_married = pd.to_numeric(married_str, errors='coerce')

    rows.append({
        'locationname': zcta,
        'pct_married': round(pct_married, 2)
    })

df_marital = pd.DataFrame(rows)
df_marital['pct_married'] = df_marital['pct_married'].fillna(0.0)

# Save the final cleaned 2-column result (or save to a master/clean filename if preferred)
output_filename = 'marital_status_clean.csv'
df_marital.to_csv(output_filename, index=False)

print(f"Marital status parsed successfully: {len(df_marital)} ZCTAs")
print(df_marital.head())

