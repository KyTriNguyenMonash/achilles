import pandas as pd

SOURCE_FILE_NAME = "MB_2016_VIC.csv"
REQUIRED_ATTS = [
    "SA1_MAINCODE_2016", # Match with the 'HomeSA1' in the household file
    "SA1_7DIGITCODE_2016", 
    "SA2_NAME_2016", # Match with the 'HomeSA2' in the household file
    "SA2_MAINCODE_2016",
    "SA3_NAME_2016", # Match with the 'HomeSA3' in the household file
    "SA3_CODE_2016",
    "SA4_NAME_2016", # Match with "HomeSA4"
    "SA4_CODE_2016"
]

PATH_HTS_PERSONS_12_16_SA1_V1 = "P_VISTA12_16_SA1_V1.csv"
PATH_HTS_HOUSEHOLDS_12_16_SA1_V1 = "H_VISTA12_16_SA1_V1.csv"

PERSONS_ATTRIBUTES = [
    "PERSID",
    "AGE",
    "SEX",
    "FULLTIMEWORK",
    "PARTTIMEWORK",
    "CASUALWORK",
    "ANYWORK",
    "HHID",
    "HomeSA1", "HomeSA2", "HomeSA3", "HomeSA4"
]

HOUSEHOLDS_ATTRIBUTES = ["HHID", "HHSIZE", "CARS", "CW_ADHHWGT_SA3","HomeSA1", "HomeSA2", "HomeSA3", "HomeSA4"]

MATCHING_NAME_CROSS = [
    # (name in seed, name in geo, code in geo and in ABS)
    ("HomeSA1", "SA1_MAINCODE_2016", "SA1_7DIGITCODE_2016"),
    ("HomeSA2", "SA2_NAME_2016", "SA2_MAINCODE_2016"),
    ("HomeSA3", "SA3_NAME_2016", "SA3_CODE_2016"),
    ("HomeSA4", "SA4_NAME_2016", "SA4_CODE_2016")
]

def replace_name_in_seed(df_seed, df_geo, match_ref):
    for match in match_ref:
        src_seed, src_geo, target_geo = match
        hold = df_geo.astype('str').set_index(src_geo)[target_geo].drop_duplicates()
        df_seed[src_seed] = df_seed[src_seed].map(hold).fillna("Wrong")
    return df_seed

if __name__ == '__main__':
    folder_path = r'C:\Users\dlaa0001\Documents\Work\PhD\achilles\popsim\data\source' + "\\"

    df_geo = pd.read_csv(folder_path + SOURCE_FILE_NAME)
    df_fi_geo = df_geo[REQUIRED_ATTS]
    
    df_hh = pd.read_csv(folder_path + "VISTA_2012_16_v1_SA1_CSV\\" + PATH_HTS_HOUSEHOLDS_12_16_SA1_V1)
    df_p = pd.read_csv(folder_path + "VISTA_2012_16_v1_SA1_CSV\\" + PATH_HTS_PERSONS_12_16_SA1_V1)
    df_fi_hh = df_hh[HOUSEHOLDS_ATTRIBUTES]
    df_fi_p = df_p[PERSONS_ATTRIBUTES]

    df_fi_hh = replace_name_in_seed(df_fi_hh, df_fi_geo, MATCHING_NAME_CROSS)
    print(df_fi_hh["HomeSA1"].unique())