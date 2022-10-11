import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

def get_missing():
    df_hh = pd.read_csv('h_test_seed.csv')
    exist_in_seed = df_hh['SA2'].unique()
    df_geo = pd.read_csv('..\..\source\MB_2016_VIC.csv')
    all = df_geo['SA2_MAINCODE_2016'].unique()
    missing = []
    for zone in all:
        if zone not in exist_in_seed: missing.append(zone)
    assert len(exist_in_seed) + len(missing) == len(all)
    return missing

def get_gdf(missing_zones, plot=False):
    zipfile = '../../source/1270055001_sa2_2016_aust_shape.zip'
    gdf = gpd.read_file(zipfile)
    gdf = gdf.loc[gdf['SA2_MAIN16'].astype('int') > 200000000]
    gdf = gdf.loc[gdf['SA2_MAIN16'].astype('int') < 220000000]

    gdf['centroid'] = gdf.centroid

    gdf_missing = gdf.loc[gdf['SA2_MAIN16'].astype('int').isin(missing_zones)]
    gdf_exist = gdf.loc[~gdf['SA2_MAIN16'].astype('int').isin(missing_zones)]

    if plot:
        ax = gdf_missing["geometry"].plot()
        gdf_exist.plot(ax=ax, color="orange")
        # gdf.plot("AREASQKM16", legend=True)
        plt.show()
    return gdf_exist, gdf_missing

if __name__ == "__main__":
    missing = get_missing()
    get_gdf(missing_zones=missing ,plot=True)
