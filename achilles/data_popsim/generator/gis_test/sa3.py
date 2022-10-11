import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

def get_missing():
    df_hh = pd.read_csv('..\..\source\VISTA_2012_16_v1_SA1_CSV\H_VISTA12_16_SA1_V1.csv')
    exist_in_seed = df_hh['HomeSA3'].unique()
    df_geo = pd.read_csv('..\..\source\MB_2016_VIC.csv')
    all = df_geo['SA3_NAME_2016'].unique()
    missing = []
    for zone, code in zip(df_geo['SA3_NAME_2016'], df_geo['SA3_CODE_2016']):
        if zone not in exist_in_seed and code not in missing:
            missing.append(code)
    assert len(exist_in_seed) + len(missing) == len(all)
    return missing

def get_gdf(missing_zones, plot=False):
    zipfile = '../../source/1270055001_sa3_2016_aust_shape.zip'
    gdf = gpd.read_file(zipfile)
    gdf = gdf.loc[gdf['SA3_CODE16'].astype('int') > 20000]
    gdf = gdf.loc[gdf['SA3_CODE16'].astype('int') < 22000]

    gdf['centroid'] = gdf.centroid

    gdf_missing = gdf.loc[gdf['SA3_CODE16'].astype('int').isin(missing_zones)]
    gdf_exist = gdf.loc[~gdf['SA3_CODE16'].astype('int').isin(missing_zones)]

    if plot:
        ax = gdf_missing["geometry"].plot()
        gdf_exist.plot(ax=ax, color="orange")
        # gdf.plot("AREASQKM16", legend=True)
        plt.show()
    return gdf_exist, gdf_missing

if __name__ == "__main__":
    missing = get_missing()
    get_gdf(missing_zones=missing ,plot=True)
