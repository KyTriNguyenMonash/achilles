import pandas as pd
import logging as log
import click
import os

log.basicConfig(level=log.DEBUG, format="%(asctime)s %(message)s")

@click.command()
@click.option("-o", "--output-dir", required=True, help="Directory for generated data")
def main(output_dir):
    getting_sum_totals(output_dir, export_csv=True)
    refactor_weights_both(output_dir, export_csv=True)

def process_geo_match_with_seed(output_dir, export_csv=True):
     # NOTE: we have to remove code that does not exist in seed data
    log.info("Drop values that not exist in seed at SA3 level in seed data")
    # final_df = final_df.drop(final_df[final_df['SA1_MAINCODE_2016']==29999949999].index)
    file_geo = 'geo_cross_walk.csv'
    final_df = pd.read_csv(os.path.join(output_dir, file_geo))
    HH_FILE = 'h_test_seed.csv'
    df_h = pd.read_csv(os.path.join(output_dir, HH_FILE))
    exist_vals = df_h['HomeSA3'].unique()
    all_vals = final_df['SA3_CODE_2016'].unique()
    for v in all_vals:
        if v not in exist_vals:
            final_df = final_df.drop(final_df[final_df['SA3_CODE_2016']==v].index)
    if export_csv:
        log.info("Output the new geo cross file, replacing old one")
        final_df.to_csv(os.path.join(output_dir, file_geo), index=False)
    return final_df

def getting_sum_totals(output_dir, export_csv=False, csv_file_name="STATE_all_control.csv"):
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
    if export_csv:
        log.info("Generating the csv file for STATE")
        fi.to_csv(os.path.join(output_dir, csv_file_name), index=False)
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
    df_hh = reweighting(df_hh, "CW_ADHHWGT_SA3", df_state["Total_dwelings"])
    log.info("Start to reweight persons")
    df_p = reweighting(df_p, "CW_ADPERSWGT_SA3", df_state["Tot_P_P"])
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

def adding_dummy_data(output_dir, export_csv=False):
    log.info("Temp step of adding more data to fit with the missing zones in the seed in SA3")
    log.info("Loading data into memories")
    file_control_SA3 = 'SA3_controls.csv'
    file_hh = 'h_test_seed.csv'
    file_p = 'p_test_seed.csv'
    file_geo = 'geo_cross_walk.csv'
    df_hh = pd.read_csv(os.path.join(output_dir, file_hh))
    df_p = pd.read_csv(os.path.join(output_dir, file_p))
    df_SA3 = pd.read_csv(os.path.join(output_dir, file_control_SA3))
    df_geo = pd.read_csv(os.path.join(output_dir, file_geo))
    log.info("Set up default values")
    map_SA3_SA4 = {}
    for SA3_code, SA4_code in zip(df_geo['SA3_CODE_2016'], df_geo['SA4_CODE_2016']):
        if SA3_code not in map_SA3_SA4:
            map_SA3_SA4[SA3_code] = SA4_code
    dict_hh = {
        'HHID': ["Nope"],
        'HHSIZE': [1],
        'CARS': [1],
        'TOTALVEHS': [1],
        'ReportingPeriod': ["NA"],
        'RP_ADHHWGT_SA3': [0.00000000001],
        'CW_ADHHWGT_SA3': [0.000000000001],
        'HomeSA1': ['NA'],
        'HomeSA2': ['NA'],
        'HomeSA3': [],
        'HomeSA4': [],
        'hhnum': []
    }
    dict_p = {
        'PERSID': ["NOPE"],
        'AGE': [30],
        'SEX': ['Male'],
        'ANYWORK': ['CASUALWORK'],
        'HHID': ["Nope"],
        'ReportingPeriod': ["NA"],
        'RP_ADPERSWGT_SA3': [0.000001],
        'CW_ADPERSWGT_SA3': [0.0000001],
        'HomeSA1': ['NA'],
        'HomeSA2': ['NA'],
        'HomeSA3': [],
        'HomeSA4': [],
        'hhnum': []
    }
    count = 0
    base_hh_num = max(df_hh['hhnum'])
    white_ls = ['HomeSA3', 'HomeSA4', 'hhnum']
    print(base_hh_num)
    log.info("Identify missing data")
    for code_SA3, num_h in zip(df_SA3['SA3_CODE_2016'], df_SA3['Total_dwelings']):
        if num_h > 0 and code_SA3 not in df_hh['HomeSA3']:
            log.info(f"Missing data for SA3 code {code_SA3} with {num_h} households")
            code_SA4 = map_SA3_SA4[code_SA3]
            count += 1
            base_hh_num += 1
            dict_hh['HomeSA3'].append(code_SA3)
            dict_hh['HomeSA4'].append(code_SA4)
            dict_hh['hhnum'].append(base_hh_num)
            dict_p['HomeSA3'].append(code_SA3)
            dict_p['HomeSA4'].append(code_SA4)
            dict_p['hhnum'].append(base_hh_num)
    for k in dict_hh:
        if k not in white_ls: dict_hh[k] = dict_hh[k]*count
    for k in dict_p:
        if k not in white_ls: dict_p[k] = dict_p[k]*count
    log.info("Done adding dummies")
    extra_df_hh = pd.DataFrame(data=dict_hh)
    extra_df_p = pd.DataFrame(data=dict_p)
    new_df_hh = pd.concat([df_hh, extra_df_hh])
    new_df_p = pd.concat([df_p, extra_df_p])
    if export_csv:
        log.info("Generating the csv file for new households, default replacing")
        new_df_hh.to_csv(os.path.join(output_dir, file_hh), index=False)
        log.info("Generating the csv file for new persons, default replacing")
        new_df_p.to_csv(os.path.join(output_dir, file_p), index=False)
    return new_df_hh, new_df_p

if __name__ == "__main__":
    adding_dummy_data('../../../popsim/synthesis/data/', export_csv=True)