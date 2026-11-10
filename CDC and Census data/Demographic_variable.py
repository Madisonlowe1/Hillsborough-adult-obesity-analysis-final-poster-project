#####################
# Madison Lowenstein
# mlowenstein@usf.edu #
# 11/22/2026 #
# Demographic variable cleanup #

# import
import pandas as pd

# load dataset
df = pd.read_csv('Race_Ethnicity_Variable.csv')

# clean and convert census data
def clean_census_val(val):
    if pd.isnull(val):
        return 0.0
    val_str = str(val).replace(',', '').replace('±', '').strip()
    try:
        return float(val_str)
    except ValueError:
        return 0.0

# filter columns to only include whats needed
zcta_estimate_cols = [c for c in df.columns if '!!Estimate' in c]

parsed_rows = []

# get demographic percentages
for col in zcta_estimate_cols:
    zcta_str = col.split('!!')[0].replace('ZCTA5','').strip().zfill(5)

    try:
        total_row = df[df['Label (Grouping)'].str.contains('Total', na=False)]
        total_pop = clean_census_val(total_row[col].values[0])

        hisp_row = df[df['Label (Grouping)'].str.strip() == 'Hispanic or Latino:']
        hisp_pop = clean_census_val(hisp_row[col].values[0])

        black_row = df[df['Label (Grouping)'].str.contains('Black or African American alone', na=False)]
        black_pop = clean_census_val(black_row[col].values[0])

        pct_hisp = (hisp_pop / total_pop * 100) if total_pop > 0 else 0.0
        pct_black = (black_pop / total_pop * 100) if total_pop > 0 else 0.0

        parsed_rows.append({
            'locationname': zcta_str,
            'total_population': total_pop,
            'pct_hispanic': round(pct_hisp, 2),
            'pct_black': round(pct_black, 2),
            'pct_non_hisp_black': round(pct_black, 2),
        })
    except Exception as e:
        print(f"Skipping {zcta_str}: {e}")

# convert passed rows into the final dataframe to be exported into new csv
df_demographics = pd.DataFrame(parsed_rows)
df_demographics.to_csv('hillsborough_demographics_parsed.csv', index=False)

print(f"Demographics parsed successfully. {len(df_demographics)}")
print(df_demographics.head())
