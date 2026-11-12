#################
# Madison Lowenstein #
# mlowenstein@usf.edu #
# 11/22/2026 #
# Creating a spatial distribiton visual for adult obesity prevelance in Hillsborough #

# imports
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from pygris import zctas

# Load dataset
def load_data(path):
  df = pd.read_csv(path)

  # Standardize the location ID column to a 5-digit string for ZCTA matching
  df["zcta"] = df["locationid"].astype(str).str.zfill(5)
  return df


# Create spatial map
def generate_obesity_map(path, save_name="hillsborough_obesity_map.png"):
  print("Downloading national ZCTA boundaries...")
  fl_zctas = zctas(cb=True, year=2020)
  fl_zctas["ZCTA5CE20"] = fl_zctas["ZCTA5CE20"].astype(str).str.zfill(5)

  # Load data
  df = load_data(path)

  # Merge boundaries with the data
  spatial_df = fl_zctas.merge(df, left_on="ZCTA5CE20", right_on="zcta")

  # Plot map
  fig, ax = plt.subplots(1, 1, figsize=(8, 8))

  spatial_df.plot(
      column="data_value",
      ax=ax,
      legend=True,
      cmap="OrRd",
      edgecolor="black",
      linewidth=0.4,
      legend_kwds={
          "label": "Adult Obesity Prevalence (%)",
          "orientation": "horizontal",
          "shrink": 0.6,
          "pad": 0.05,
      },
  )

  ax.set_title(
      "Figure 1. Adult Obesity Prevalence Across Hillsborough County ZCTAs",
      fontsize=12,
      fontweight="bold",
  )
  ax.axis("off")

  # Save and display
  plt.tight_layout()
  plt.savefig(save_name, dpi=300, bbox_inches="tight")
  plt.show()


if __name__ == "__main__":
  generate_obesity_map("hillsborough_obesity_income_merged.csv")