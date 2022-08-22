import pandas as pd
import logging as log
import click
import os

log.basicConfig(level=log.DEBUG, format="%(asctime)s %(message)s")

@click.command()
@click.option("-o", "--output-dir", required=True, help="Directory for generated data")
def main(output_dir):
    df = getting_sum_totals(output_dir)
    log.info("Generating the csv file for STATE")
    df.to_csv(os.path.join(output_dir, "STATE_all_control.csv"), index=False)
    refactor_weights_both(output_dir, export_csv=True)

def getting_sum_totals(output_dir):
    log.info("Beginning generating the sums of controls for STATE using SA4 level data")
    only_to_sum = [
        'Num_Psns_UR_1_Total',
        'Num_Psns_UR_2_Total',
        'Num_Psns_UR_3_Total',
        'Num_Psns_UR_4_Total',
        'Num_Psns_UR_5_Total',
        'Num_Psns_UR_6mo_Total',
        'Num_MVs_per_dweling_0_MVs', 
        'Num_MVs_per_dweling_1_MVs', 
        'Num_MVs_per_dweling_2_MVs', 
        'Num_MVs_per_dweling_3_MVs', 
        'Num_MVs_per_dweling_4mo_MVs', 
        'Num_MVs_NS', 
        'Total_dwelings',
        'Tot_P_M', 
        'Tot_P_F', 
        'Tot_P_P', 
        'Age_0_4_yr_P', 
        'Age_5_14_yr_P', 
        'Age_15_19_yr_P', 
        'Age_20_24_yr_P', 
        'Age_25_34_yr_P', 
        'Age_35_44_yr_P', 
        'Age_45_54_yr_P', 
        'Age_55_64_yr_P', 
        'Age_65_74_yr_P', 
        'Age_75_84_yr_P', 
        'Age_85ov_P',
        'P_Emp_FullT_Tot',
        'P_Emp_PartT_Tot',
        'P_Emp_awy_f_wrk_Tot',
        'P_Hours_wkd_NS_Tot',
        'P_Tot_Unemp_Tot',
        "P_Emp_Guess_Casual_Tot"
    ]
    log.info("Load resulted data of SA4 controls")
    SA4_file = "SA4_controls.csv"
    df_sa4 = pd.read_csv(os.path.join(output_dir, SA4_file))
    log.info("Processing to get the final sum")
    s = df_sa4[only_to_sum].sum()
    s["STATE_CODE_2016"] = 2
    fi = pd.DataFrame(s).T
    return fi

def refactor_weights_both(output_dir, export_csv=False):
    log.info("Reweighting the seed based factoring to controls")
    log.info("NOTE this needs to run after got the final seed and state/region file")
    log.info("Loading the needed files into memomy ...")
    hh_file = "h_test_seed.csv"
    p_file = "p_test_seed.csv"
    state_file = "STATE_all_control.csv"
    df_hh = pd.read_csv(os.path.join(output_dir, hh_file))
    df_p = pd.read_csv(os.path.join(output_dir, p_file))
    df_state = pd.read_csv(os.path.join(output_dir, state_file))

    log.info("Start to reweight households")
    df_hh = reweighting(df_hh, "RP_ADHHWGT_SA3", df_state["Total_dwelings"])
    log.info("Start to reweight persons")
    df_p = reweighting(df_p, "RP_ADPERSWGT_SA3", df_state["Tot_P_P"])
    if export_csv:
        log.info("Exporting to csv, default is to replace the previous seed files")
        log.info("Households ...")
        df_hh.to_csv(os.path.join(output_dir, hh_file), index=False)
        log.info("Persons ...")
        df_p.to_csv(os.path.join(output_dir, p_file), index=False)
    return df_hh, df_p

def reweighting(df_seed, name_weight, target_total):
    seed_tot = df_seed[name_weight].sum()
    factor = float(target_total) / float(seed_tot)
    df_seed[name_weight] = df_seed[name_weight] * factor
    return df_seed


if __name__ == "__main__":
    main()