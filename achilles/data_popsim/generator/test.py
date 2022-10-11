import geopandas as gpd
import matplotlib.pyplot as plt

zipfile = '../source/1270055001_sa4_2016_aust_shape.zip'
gdf = gpd.read_file(zipfile)
gdf = gdf.loc[gdf['SA4_CODE16'].astype('int') > 200]
gdf = gdf.loc[gdf['SA4_CODE16'].astype('int') < 220]

gdf['centroid'] = gdf.centroid
print(gdf)

gdf['coords'] = gdf['geometry'].representative_point()
gdf['coords'] = gdf['coords'].apply(lambda x: x.coords[:])
gdf['coords'] = [coords[0] for coords in gdf['coords']]
# ax = gdf["geometry"].plot()
# gdf["centroid"].plot(ax=ax, color="black")
gdf.plot("AREASQKM16", legend=True)
for idx, row in gdf.iterrows():
    plt.annotate(text=row['SA4_CODE16'], xy=row['coords'],
                 horizontalalignment='center')
plt.show()
