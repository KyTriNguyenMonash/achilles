import pandas as pd


if __name__ == "__main__":
    df_geo = pd.read_csv("geo_cross_walk.csv")
    df_h = pd.read_csv("h_test_seed.csv")
    exist_vals = df_h['HomeSA3'].unique()
    all_vals = df_geo['SA3_CODE_2016'].unique()
    for v in all_vals:
        if v not in exist_vals:
            df_geo = df_geo.drop(df_geo[df_geo['SA3_CODE_2016']==v].index)
    df_geo.to_csv("geo_cross_walk.csv")