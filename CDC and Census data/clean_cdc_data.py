#####################
# Madison Lowenstein #
# mlowenstein@usf.edu #
# 11/22/2026 #
# Final Poster Project #
# Filter out the Hillsborough ZCTAs #

import pandas as pd

#  Load the dataset from the same directory
df = pd.read_csv('cdc_places_zcta.csv')

#  Inspect shape and missing values
print(df.shape, df.isna().sum(), sep="\n")

#  Clean up columns and drop rows without data values
df = df.dropna(axis=1, how='all')
df = df.dropna(subset=["Data_Value"])
df.columns = df.columns.str.lower().str.replace(' ', '_')

# Define Hillsborough County ZCTAs
hillsborough_zctas = [
    '33503', '33510', '33511', '33513', '33514', '33521', '33523', '33525', '33527', '33530', '33534', '33538', '33540',
    '33541', '33542', '33543', '33544', '33545', '33547', '33548', '33549', '33550', '33556', '33558',
    '33559', '33563', '33565', '33566', '33567', '33569', '33570', '33572', '33573', '33574', '33576', '33578', '33579',
    '33584', '33585', '33592', '33594', '33596', '33597', '33598', '33602', '33603', '33604', '33605', '33606', '33607',
    '33609', '33610', '33611', '33612', '33613', '33614', '33615', '33616', '33617', '33618', '33619', '33620', '33621',
    '33624', '33625', '33626', '33629', '33634', '33635', '33637', '33647'
]

# extract clean dataset
df['locationname'] = df['locationname'].astype(str).str.zfill(5)
df_filtered = df[
    (df['locationname'].isin(hillsborough_zctas)) &
    (df['measureid'].isin(['OBESITY', 'LPA']))
].copy()

print(f"Filtered down to {len(df_filtered)} target rows for Hillsborough County")

df_filtered.to_csv('cdc_hillsborough_zctas.csv', index=False)
print("Cleaned file saved")



