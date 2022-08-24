import pandas as pd
import numpy as np
import logging as log
import click
import os

log.basicConfig(level=log.DEBUG, format="%(asctime)s %(message)s")

MATCHING_NAME_CROSS = [
    # (name in seed, name in geo, code in geo and in ABS)
    ("HomeSA1", "SA1_MAINCODE_2016", "SA1_7DIGITCODE_2016"),
    ("HomeSA2", "SA2_NAME_2016", "SA2_MAINCODE_2016"),
    ("HomeSA3", "SA3_NAME_2016", "SA3_CODE_2016"),
    ("HomeSA4", "SA4_NAME_2016", "SA4_CODE_2016")
]

PATH_HTS_PERSONS_12_16_SA1_V1 = "VISTA_2012_16_v1_SA1_CSV/P_VISTA12_16_SA1_V1.csv"
PATH_HTS_HOUSEHOLDS_12_16_SA1_V1 = "VISTA_2012_16_v1_SA1_CSV/H_VISTA12_16_SA1_V1.csv"
GEO_FILE = "MB_2016_VIC.csv"

PERSONS_ATTRIBUTES = [
        "PERSID",
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
        "HomeSA1", "HomeSA2", "HomeSA3", "HomeSA4"
    ]
HOUSEHOLDS_ATTRIBUTES = [
    "HHID", 
    "HHSIZE", 
    "CARS", 
    "TOTALVEHS", 
    "ReportingPeriod", 
    "RP_ADHHWGT_SA3",
    "CW_ADHHWGT_SA3",
    "HomeSA1", "HomeSA2", "HomeSA3", "HomeSA4"
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
    h_test_seed = running_hh(local_dir)
    p_test_seed = running_pp(local_dir)

    log.info("Process households")
    h_test_seed = process_households(h_test_seed)
    h_test_seed = replace_name_in_seed(h_test_seed, geo_df, MATCHING_NAME_CROSS)
    # Create a new idea using numbering
    h_test_seed = h_test_seed.reset_index(drop=True)
    h_test_seed['hhnum'] = h_test_seed.index + 1

    log.info("Process persons")
    p_test_seed = process_persons(p_test_seed)
    p_test_seed = replace_name_in_seed(p_test_seed, geo_df, MATCHING_NAME_CROSS)
    p_test_seed = match_hhid_to_p(p_test_seed, h_test_seed)
    return h_test_seed, p_test_seed

def running_pp(local_dir):
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

def running_hh(local_dir):
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
    return h_test_seed


def replace_name_in_seed(df_seed, df_geo, match_ref):
    # NOTE: some data got drop after the mapping, prob some from 2012 is not match with 2016 ABS, like 9k data
    #process geo file
    for match in match_ref:
        src_seed, src_geo, target_geo = match
        df_geo[src_geo] = df_geo[src_geo].astype('str').str.replace(' ', '', regex=False).str.upper()
        df_seed[src_seed] = df_seed[src_seed].astype('str').str.replace(' ', '', regex=False).str.upper()
        hold = df_geo.astype('category').set_index(src_geo)[target_geo].drop_duplicates()
        hold_d = hold.to_dict()
        df_seed[src_seed] = df_seed[src_seed].astype('category').replace(hold_d)
    return df_seed

if __name__ == '__main__':
    main()
