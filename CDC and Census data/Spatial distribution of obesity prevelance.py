#################
# Madison Lowenstein #
# mlowenstein@usf.edu #
# 11/22/2026 #
# Creating a spatial distribiton visual for adult obesity prevelance in Hillsborough #

# imports
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from pygris import counties, zctas

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

  #  Filter ZCTAs strictly to Hillsborough County to remove  any exterior spillover
  fl_counties = counties(state="FL", cb=True, year=2020)
  hillsborough = fl_counties[fl_counties["NAME"] == "Hillsborough"].to_crs(
      fl_zctas.crs
  )
  hillsborough_zctas = fl_zctas[
      fl_zctas.intersects(hillsborough.unary_union)
  ].copy()

  # Load data
  df = load_data(path)

  # Use left join so all Hillsborough ZCTAs are kept to prevent white whols
  spatial_df = hillsborough_zctas.merge(
      df, left_on="ZCTA5CE20", right_on="zcta", how="left"
  )

  # Plot map
  fig, ax = plt.subplots(1, 1, figsize=(8, 8))

 # Plot excluded/no-data ZCTAs in light gray to fill interior gaps
  spatial_df[spatial_df["data_value"].isna()].plot(
      ax=ax, color="white", edgecolor="black", linewidth=0.4
  )

  # Plot your regression data ZCTAs on top
  spatial_df[spatial_df["data_value"].notna()].plot(
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