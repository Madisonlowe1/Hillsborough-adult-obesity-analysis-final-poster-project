#####################
# Madison Lowenstein #
# mlowenstein@usf.edu #
# 11/22/2026 #
# Marital staus variable csv cleanup #

# import
import pandas as pd

# load the marital statis dataset
df = pd.read_csv('marital_status.csv')

# identify total population and married estimate columns
total_col = [c for c in df.columns if 'Total!!Estimate' in c]
married_cols = [c for c in df.columns if 'Now married (except separated)!!Estimate' in c]

rows = []

# loop columns
for t_col, m_col in zip(total_col, married_cols):
    zcta = t_col.split('!!')[0].replace('ZCTA5', '').strip().zfill(5)

    married_str = str(df.loc[0, m_col]).replace('%', '').replace(',', '').strip()
    pct_married = pd.to_numeric(married_str, errors='coerce')

    rows.append({
        'locationname': zcta,
        'pct_married': round(pct_married, 2)
    })

# convert parsed records into dataframe and fix missing values
df_marital = pd.DataFrame(rows)
df_marital['pct_married'] = df_marital['pct_married'].fillna(0.0)

# Save the final dataset
output_filename = 'marital_status_clean.csv'
df_marital.to_csv(output_filename, index=False)

print(f"Marital status parsed successfully: {len(df_marital)} ZCTAs")
print(df_marital.head())

