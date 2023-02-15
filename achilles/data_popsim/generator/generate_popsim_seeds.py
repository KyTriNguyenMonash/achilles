import pandas as pd
import numpy as np
import logging as log
import click
import os

log.basicConfig(level=log.DEBUG, format="%(asctime)s %(message)s")

PATH_HTS_PERSONS_12_16_SA1_V1 = "VISTA_2012_16_v1_SA1_CSV/P_VISTA12_16_SA1_V1.csv"
PATH_HTS_HOUSEHOLDS_12_16_SA1_V1 = "VISTA_2012_16_v1_SA1_CSV/H_VISTA12_16_SA1_V1.csv"
GEO_FILE = "MB_2016_VIC.csv"

PERSONS_ATTRIBUTES = [
        "PERSID",
        "AGEGROUP",
        "CARLICENCE",
        "PERSINC",
        "AGE",
        "SEX",
        "FULLTIMEWORK",
        "PARTTIMEWORK",
        "CASUALWORK",
        "ANYWORK",
        "HHID",
        "ReportingPeriod",
        "RP_ADPERSWGT_SA3", #Person weight for the given year, not used for anything for now
        "CW_ADPERSWGT_SA3",
        "HomeSA1",
        'STUDYING'
    ]
HOUSEHOLDS_ATTRIBUTES = [
    "HHID", 
    "HHSIZE", 
    "CARS", 
    "TOTALVEHS", 
    "ReportingPeriod", 
    "RP_ADHHWGT_SA3",
    "CW_ADHHWGT_SA3",
    "HomeSA1"
    ]
   

@click.command()
@click.option("-l", "--local-dir", required=True, help="Local data directory")
@click.option("-o", "--output-dir", required=True, help="Directory for generated data")
def main(local_dir, output_dir):
    h_test_seed, p_test_seed = running_final(local_dir)
    log.info("Generate persons seed")
    p_test_seed.to_csv(os.path.join(output_dir, f"p_test_seed.csv"), index=False)

    log.info("Generate households seed")
    h_test_seed.to_csv(os.path.join(output_dir, f"h_test_seed.csv"), index=False)

def mod(local_dir):
    log.info("Begin generating seed data")
    h_test_seed, p_test_seed = running_final(local_dir)
    return h_test_seed, p_test_seed

def running_final(local_dir):
    log.info("NOTE: this run is very specific to VIC data")
    geo_df = pd.read_csv(
        os.path.join(local_dir, GEO_FILE)
    )
    mapping_file = 'CG_SA1_2011_SA1_2016.xls'
    mapping_sheet_in_file = 'Table 3'
    df_map_raw  = pd.read_excel(os.path.join(local_dir, mapping_file), sheet_name=mapping_sheet_in_file)

    h_test_seed = init_hh(local_dir)
    p_test_seed = init_pp(local_dir)

    log.info("Process households")
    h_test_seed = process_households(h_test_seed)
    h_test_seed = mapping_SA1_2012_2016(h_test_seed, df_map_raw)
    h_test_seed = mapping_SA1_to_rest(h_test_seed, geo_df)

    log.info("Process persons")
    p_test_seed = process_persons(p_test_seed)
    p_test_seed = match_hhid_to_p(p_test_seed, h_test_seed)
    p_test_seed = mapping_SA1_2012_2016(p_test_seed, df_map_raw)
    p_test_seed = mapping_SA1_to_rest(p_test_seed, geo_df)
    return h_test_seed, p_test_seed

def init_pp(local_dir):
    log.info("Load data people into memory ....")
    p_original_df = pd.read_csv(
        os.path.join(local_dir, PATH_HTS_PERSONS_12_16_SA1_V1)
    )
    log.info("Filter persons with attributes")
    p_test_seed = p_original_df[PERSONS_ATTRIBUTES]
    log.info("Check unique id for persons")
    if not is_unique_att(p_test_seed, "PERSID"):
        raise Exception("THE ID OF PERSON IS NOT UNIQUE")
    return p_test_seed

def init_hh(local_dir):
    log.info("Load data household into memory ....")
    h_original_df = pd.read_csv(
        os.path.join(local_dir, PATH_HTS_HOUSEHOLDS_12_16_SA1_V1)
    )
    log.info("Filter households with attributes")
    h_test_seed = h_original_df[HOUSEHOLDS_ATTRIBUTES]
    log.info("Check unique id for households")
    if not is_unique_att(h_test_seed, "HHID"):
        raise Exception("THE ID OF THE HOUSEHOLD IS NOT UNIQUE")
    return h_test_seed

def is_unique_att(df, unique_att):
    N = df.shape[0]
    test_N = len(df[unique_att].unique())
    return True if N == test_N else False

def process_persons(p_test_seed):
    # Filter to only get 2016 data
    # p_test_seed = p_test_seed[p_test_seed["ReportingPeriod"] == '2014-16']
    # Process work
    p_test_seed.loc[p_test_seed["CASUALWORK"] == "Yes", "ANYWORK"] = "CASUALWORK"
    p_test_seed.loc[p_test_seed["PARTTIMEWORK"] == "Yes", "ANYWORK"] = "PARTTIMEWORK"
    p_test_seed.loc[p_test_seed["FULLTIMEWORK"] == "Yes", "ANYWORK"] = "FULLTIMEWORK"
    p_test_seed = p_test_seed.drop(
        columns=["FULLTIMEWORK", "PARTTIMEWORK", "CASUALWORK"]
    )
    # p_test_seed['HHID'] = p_test_seed['HHID'].str.slice(start=1).str.replace('H', '0')
    # p_test_seed['PERSID'] = p_test_seed['PERSID'].str.slice(start=1).str.replace('H', '0').str.replace('P', '1')
    return p_test_seed


def match_hhid_to_p(df_p, df_h):
    src_h, target_h = 'HHID', 'hhnum'
    hold = df_h.set_index(src_h)[target_h].drop_duplicates()
    df_p['hhnum'] = df_p[src_h].map(hold)
    return df_p


def process_households(h_test_seed):
    # Filter to only get 2016 data
    # h_test_seed = h_test_seed[h_test_seed["ReportingPeriod"] == '2014-16']
    # Replace CARS to boolean
    h_test_seed["CARS"] = np.where(h_test_seed["CARS"] == 0, "No", "Yes")
    # h_test_seed['HHID'] = h_test_seed['HHID'].str.slice(start=1).str.replace('H', '0')
    # Create a new id using numbering
    h_test_seed = h_test_seed.reset_index(drop=True)
    h_test_seed['hhnum'] = h_test_seed.index + 1
    return h_test_seed


def mapping_SA1_2012_2016(df_target, df_map_raw):
    log.info("Mapping the old SA1 of 2011 to new SA1 2016")
    df_mapping = df_map_raw.rename(columns=df_map_raw.loc[4])[6:-3]
    dict_map = {}
    for name_2011, name_2016 in zip(df_mapping['SA1_MAINCODE_2011'], df_mapping['SA1_MAINCODE_2016']):
        dict_map[name_2011] = name_2016
    log.info("Begin the mapping...")
    df_target['HomeSA1'].replace(dict_map, inplace=True)
    return df_target


def mapping_SA1_to_rest(df_target, geo_df):
    log.info("Using the SA1 from geo file to map to the rest")
    zip_from_geo = zip(
        geo_df['SA1_MAINCODE_2016'],
        geo_df['SA1_7DIGITCODE_2016'],
        geo_df['SA2_MAINCODE_2016'],
        geo_df['SA3_CODE_2016'],
        geo_df['SA4_CODE_2016']
    )

    log.info("Preparing the mapping dict from geo file")
    dict_map = {}
    for sa1_full, sa1_7digit, sa2, sa3, sa4 in zip_from_geo:
        dict_map[sa1_full] = {
            'SA1': sa1_7digit,
            'SA2': sa2,
            'SA3': sa3,
            'SA4': sa4
        }

    log.info("Loop through the SA1 in the target dataframe")
    SA1_arr, SA2_arr, SA3_arr, SA4_arr = [], [], [], []
    for sa1_full in df_target['HomeSA1']:
        if sa1_full in dict_map:
            val = dict_map[sa1_full]
            SA1_arr.append(val['SA1'])
            SA2_arr.append(val['SA2'])
            SA3_arr.append(val['SA3'])
            SA4_arr.append(val['SA4'])
        else:
            log.warning(f"ERR: this SA1: {sa1_full} does not exist in geo file")
            SA1_arr.append(None)
            SA2_arr.append(None)
            SA3_arr.append(None)
            SA4_arr.append(None)

    log.info("Adding new collumns")
    df_target['SA1'] = SA1_arr
    df_target['SA2'] = SA2_arr
    df_target['SA3'] = SA3_arr
    df_target['SA4'] = SA4_arr
    return df_target

if __name__ == '__main__':
    # A way now, is to replace all SA1 then map from SA1 up using geo_cross_walk instead of replacing directly with name (this make sure the mapping more consistent tho not objective)
    a = running_final('../source/')
