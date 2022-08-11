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
    log.info("Load data into memory ....")
    original_df = pd.read_csv(os.path.join(local_dir, SOURCE_FILE_NAME))

    # generate the geo cross walk 
    log.info("Filter out the only needed attributes")
    df = original_df[REQUIRED_ATTS]
    # check the matching of data
    # save the file
    log.info("Generate geo cross walk")
    df.to_csv(os.path.join(output_dir, "geo_cross_walk.csv"), index=False)

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
