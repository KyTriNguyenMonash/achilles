import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

def get_missing_SA4():
    df_hh = pd.read_csv('..\source\VISTA_2012_16_v1_SA1_CSV\H_VISTA12_16_SA1_V1.csv')
    exist_in_seed = df_hh['HomeSA4'].unique()
    df_geo = pd.read_csv('..\source\MB_2016_VIC.csv')
    all_SA4 = df_geo['SA4_NAME_2016'].unique()
    missing_SA4 = []
    # for zone in all_SA4:
    #     if zone not in exist_in_seed: missing_SA4.append(zone)
    for zone, code in zip(df_geo['SA4_NAME_2016'], df_geo['SA4_CODE_2016']):
        if zone not in exist_in_seed and code not in missing_SA4:
            missing_SA4.append(code)
    assert len(exist_in_seed) + len(missing_SA4) == len(all_SA4)
    return missing_SA4

def get_gdf(missing_zones, plot=False):
    zipfile = '../source/1270055001_sa4_2016_aust_shape.zip'
    gdf = gpd.read_file(zipfile)
    gdf = gdf.loc[gdf['SA4_CODE16'].astype('int') > 200]
    gdf = gdf.loc[gdf['SA4_CODE16'].astype('int') < 220]

    gdf['centroid'] = gdf.centroid

    gdf['coords'] = gdf['geometry'].representative_point()
    gdf['coords'] = gdf['coords'].apply(lambda x: x.coords[:])
    gdf['coords'] = [coords[0] for coords in gdf['coords']]

    gdf_missing = gdf.loc[gdf['SA4_CODE16'].astype('int').isin(missing_zones)]
    gdf_exist = gdf.loc[~gdf['SA4_CODE16'].astype('int').isin(missing_zones)]

    if plot:
        ax = gdf_missing["geometry"].plot()
        gdf_exist.plot(ax=ax, color="orange")
        # gdf.plot("AREASQKM16", legend=True)
        for idx, row in gdf.iterrows():
            plt.annotate(text=row['SA4_CODE16'], xy=row['coords'],
                        horizontalalignment='center')
        plt.show()
    return gdf_exist, gdf_missing

if __name__ == "__main__":
    missing = get_missing_SA4()
    get_gdf(missing_zones=missing ,plot=True)
