import pandas as pd


file_name_tot_hh = '2016Census_G30_VIC_SA1.csv' #hh, vel
file_name_tot_pp = '2016Census_G01_VIC_SA1.csv' #genders, pp, age gr
file_name_tot_work = '2016Census_G43B_VIC_SA1.csv' #work

if __name__ == '__main__':
    folder_path = r'C:\Users\dlaa0001\Documents\Work\PhD\achilles\popsim\data\source\2016_GCP_all_for_VIC_short-header\2016 Census GCP All Geographies for VIC\SA1\VIC' + "\\"

    df_hh = pd.read_csv(folder_path + file_name_tot_hh)
    df_pp = pd.read_csv(folder_path + file_name_tot_pp)
    df_work = pd.read_csv(folder_path + file_name_tot_work)

    df_hh_select = df_hh[[
        'SA1_7DIGITCODE_2016', 
        'Num_MVs_per_dweling_0_MVs', 
        'Num_MVs_per_dweling_1_MVs', 
        'Num_MVs_per_dweling_2_MVs', 
        'Num_MVs_per_dweling_3_MVs', 
        'Num_MVs_per_dweling_4mo_MVs', 
        'Num_MVs_NS', 
        'Total_dwelings'
        ]]
    df_pp_select = df_pp[[
        'SA1_7DIGITCODE_2016', 
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
        'SA1_7DIGITCODE_2016',
        'P_Emp_FullT_Tot',
        'P_Emp_PartT_Tot',
        'P_Emp_awy_f_wrk_Tot',
        'P_Hours_wkd_NS_Tot',
        'P_Tot_Unemp_Tot'
        ]]

    df_final = df_hh_select.merge(df_pp_select.merge(df_work_select, how='inner', on='SA1_7DIGITCODE_2016'), how='inner', on='SA1_7DIGITCODE_2016')
    # print(df_final)
    df_final.to_csv('SA1_controls.csv', index=False)
