import pandas as pd
import numpy as np
import logging as log
import click
import os

log.basicConfig(level=log.DEBUG, format="%(asctime)s %(message)s")

@click.command()
@click.option("-l", "--local-dir", required=True, help="Local data directory, should be till GCP_all")
@click.option("-o", "--output-dir", required=True, help="Directory for generated data")
@click.option("-a", "--area-lev", required=True, help="The level of controls")
def main(local_dir, output_dir, area_lev):
    log.info("Begin process")
    final_df = running_get_final(local_dir, area_lev)
    log.info("Export to csv file")
    final_df.to_csv(os.path.join(output_dir, f'{area_lev}_controls.csv'), index=False)

def mod(local_dir, area_lev):
    log.info(f"Begin generating controls for {area_lev}")
    # This for combination
    return running_get_final(local_dir, area_lev)

def running_get_final(local_dir, area_lev):
    log.info("Please note that this is designed for 2016 data of VIC")
    log.info("Loading data into memory")

    file_name_tot_hh = f'2016Census_G30_VIC_{area_lev}.csv' #hh, vel
    file_name_tot_pp = f'2016Census_G01_VIC_{area_lev}.csv' #genders, pp, age gr
    file_name_tot_work = f'2016Census_G43B_VIC_{area_lev}.csv' #work
    file_name_tot_hh2 = f'2016Census_G31_VIC_{area_lev}.csv' #hh size

    mid_folder = f'{area_lev}/VIC/'

    df_hh = pd.read_csv(local_dir + mid_folder + file_name_tot_hh)
    df_hh2 = pd.read_csv(local_dir + mid_folder + file_name_tot_hh2)
    df_pp = pd.read_csv(local_dir + mid_folder + file_name_tot_pp)
    df_work = pd.read_csv(local_dir + mid_folder + file_name_tot_work)

    # Assuming that this position will always have the ID name
    id_name = df_hh.columns[0]
    return filter_and_combine(df_hh, df_hh2, df_pp, df_work, id_name)

def filter_and_combine(df_hh, df_hh2, df_pp, df_work, id_name):
    log.info("Select only the wanted data")
    df_hh_select = df_hh[[
        id_name, 
        'Num_MVs_per_dweling_0_MVs', 
        'Num_MVs_per_dweling_1_MVs', 
        'Num_MVs_per_dweling_2_MVs', 
        'Num_MVs_per_dweling_3_MVs', 
        'Num_MVs_per_dweling_4mo_MVs', 
        'Num_MVs_NS', 
        'Total_dwelings'
        ]]
    df_hh_select2 = df_hh2[[
        id_name, 
        'Num_Psns_UR_1_Total',
        'Num_Psns_UR_2_Total',
        'Num_Psns_UR_3_Total',
        'Num_Psns_UR_4_Total',
        'Num_Psns_UR_5_Total',
        'Num_Psns_UR_6mo_Total'
        ]]
    df_pp_select = df_pp[[
        id_name, 
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
        'Age_85ov_P'
        ]]
    df_work_select = df_work[[
        id_name,
        'P_Emp_FullT_Tot',
        'P_Emp_PartT_Tot',
        'P_Emp_awy_f_wrk_Tot',
        'P_Hours_wkd_NS_Tot',
        'P_Tot_Unemp_Tot'
        ]]
    log.info("Combine to produce the final dataset")
    df_final = df_hh_select2.merge(df_hh_select.merge(df_pp_select.merge(df_work_select, how='inner', on=id_name), how='inner', on=id_name), how='inner', on=id_name)
    df_final["STATE_CODE_2016"] = 2
    df_final["P_Emp_Guess_Casual_Tot"] = df_final[["P_Emp_awy_f_wrk_Tot", "P_Hours_wkd_NS_Tot"]].sum(axis=1)
    df_final["P_Emp_Fixed_Unemp_Tot"] = df_final["Tot_P_P"] - df_final["P_Emp_FullT_Tot"] - df_final["P_Emp_PartT_Tot"] - df_final["P_Emp_Guess_Casual_Tot"]
    return df_final

if __name__ == '__main__':
    main()
