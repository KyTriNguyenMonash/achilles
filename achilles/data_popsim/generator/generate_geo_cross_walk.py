import pandas as pd
import numpy as np
import logging as log
import click
import os

log.basicConfig(level=log.DEBUG, format="%(asctime)s %(message)s")

SOURCE_FILE_NAME = "MB_2016_VIC.csv"
REQUIRED_ATTS = [
    "SA1_MAINCODE_2016", # Match with the 'HomeSA1' in the household file
    "SA1_7DIGITCODE_2016", 
    "SA2_NAME_2016", # Match with the 'HomeSA2' in the household file
    "SA2_MAINCODE_2016",
    "SA3_NAME_2016", # Match with the 'HomeSA3' in the household file
    "SA3_CODE_2016",
    "SA4_NAME_2016", # Match with "HomeSA4"
    "SA4_CODE_2016",
    "STATE_CODE_2016"
]

# func to check the all the names in the seed file match with the ones in the geo cross walk
@click.command()
@click.option("-l", "--local-dir", required=True, help="Local data directory")
@click.option("-o", "--output-dir", required=True, help="Directory for generated data")
def main(local_dir, output_dir):
    df = running_final(local_dir, output_dir)
    # save the file
    log.info("Generate geo cross walk")
    df.to_csv(os.path.join(output_dir, "geo_cross_walk.csv"), index=False)

def mod(local_dir, output_dir):
    log.info("Begin generating geo cross walk data")
    return running_final(local_dir, output_dir)

def running_final(local_dir, output_dir):
    log.info("THIS ONLY WORK AFTER WE GOT THE SEED DATA")
    log.info("Load data into memory ....")
    geo_df = pd.read_csv(os.path.join(local_dir, SOURCE_FILE_NAME))

    # generate the geo cross walk 
    log.info("Filter out the only needed attributes")
    final_df = geo_df[REQUIRED_ATTS]
    # NOTE: we have to remove code that does not exist in seed data
    log.info("Drop values that not exist in seed at SA3 level")
    # final_df = final_df.drop(final_df[final_df['SA1_MAINCODE_2016']==29999949999].index)
    HH_FILE = 'h_test_seed.csv'
    df_h = pd.read_csv(os.path.join(output_dir, HH_FILE))
    exist_vals = df_h['HomeSA3'].unique()
    all_vals = final_df['SA3_CODE_2016'].unique()
    for v in all_vals:
        if v not in exist_vals:
            final_df = final_df.drop(final_df[final_df['SA3_CODE_2016']==v].index)
    # TOBE: check the matching of data
    return final_df

def check_matching(ser_source, ser_des):
    ls_vals = ser_source.unique()
    for val in ls_vals:
        if val not in ser_des:
            return False
    return True

def check_2_df_match(df_source, df_des, ls_pairs):
    NotImplemented

if __name__ == '__main__':
    main()
