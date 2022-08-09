import pandas as pd
import numpy as np
import logging as log
import click
import os

log.basicConfig(level=log.DEBUG, format="%(asctime)s %(message)s")

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
]

HOUSEHOLDS_ATTRIBUTES = ["HHID", "HHSIZE", "CARS", "CW_ADHHWGT_SA3", "HomeSA3"]


@click.command()
@click.option("-l", "--local-dir", required=True, help="Local data directory")
@click.option("-o", "--output-dir", required=True, help="Directory for generated data")
def main(local_dir, output_dir):

    log.info("Load data into memory ....")
    p_original_df = pd.read_csv(os.path.join(local_dir, PATH_HTS_PERSONS_12_16_SA1_V1))
    h_original_df = pd.read_csv(
        os.path.join(local_dir, PATH_HTS_HOUSEHOLDS_12_16_SA1_V1)
    )

    log.info("Filter persons and households with attributes")
    p_test_seed = p_original_df[PERSONS_ATTRIBUTES]
    h_test_seed = h_original_df[HOUSEHOLDS_ATTRIBUTES]

    log.info("Check unique id for persons and households")
    validate_hts_data(p_test_seed, h_test_seed)

    log.info("Process persons")
    p_test_seed = process_persons(p_test_seed)

    log.info("Process households")
    h_test_seed = process_households(h_test_seed)

    log.info("Generate persons seed")
    p_test_seed.to_csv(os.path.join(output_dir, f"p_test_seed.csv"), index=False)

    log.info("Generate households seed")
    h_test_seed.to_csv(os.path.join(output_dir, f"h_test_seed.csv"), index=False)


def is_unique_att(df, unique_att):
    N = df.shape[0]
    test_N = len(df[unique_att].unique())
    return True if N == test_N else False


def validate_hts_data(p_test_seed, h_test_seed):
    if not is_unique_att(p_test_seed, "PERSID"):
        raise Exception("THE ID OF PERSON IS NOT UNIQUE")
    if not is_unique_att(h_test_seed, "HHID"):
        raise Exception("THE ID OF THE HOUSEHOLD IS NOT UNIQUE")


def process_persons(p_test_seed):
    p_test_seed.loc[p_test_seed["CASUALWORK"] == "Yes", "ANYWORK"] = "CASUALWORK"
    p_test_seed.loc[p_test_seed["PARTTIMEWORK"] == "Yes", "ANYWORK"] = "PARTTIMEWORK"
    p_test_seed.loc[p_test_seed["FULLTIMEWORK"] == "Yes", "ANYWORK"] = "FULLTIMEWORK"
    p_test_seed = p_test_seed.drop(
        columns=["FULLTIMEWORK", "PARTTIMEWORK", "CASUALWORK"]
    )
    return p_test_seed


def process_households(h_test_seed):
    h_test_seed["CARS"] = np.where(h_test_seed["CARS"] == 0, "No", "Yes")
    return h_test_seed

if __name__ == '__main__':
    main()
