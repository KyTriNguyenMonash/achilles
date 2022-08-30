from unittest import skip
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    path_files = '../../popsim/synthesis'

    controls_file = 'configs/controls.csv'
    output_hh_file = 'output/synthetic_households.csv'
    output_p_file = 'output/synthetic_persons.csv'

    to_df = lambda f: pd.read_csv(os.path.join(path_files, f))
    df_controls = to_df(controls_file)
    households = to_df(output_hh_file)
    persons = to_df(output_p_file)

    spec_ls = ['Total_dwelings', 'Tot_P_P'] # These are generated using the weights
    skip_ls = ['TOTALVEHS'] #Because it does not exist in the synthetic data

    ls_zones_lev = {
        'SA1': 'SA1_7DIGITCODE_2016',
        'SA2': 'SA2_MAINCODE_2016',
        'SA3': 'SA3_CODE_2016'
    }
    
    for zone_lev in ls_zones_lev:
        zone_tot = ls_zones_lev[zone_lev]
        tot_file = f'data/{zone_lev}_controls.csv'
        df_tot = to_df(tot_file)
        for name, df, att, exp in zip(df_controls['target'], df_controls['seed_table'], df_controls['control_field'],  df_controls['expression']):
            if att in skip_ls: continue
            df = eval(df)
            if att in spec_ls:
                dict_vals_syn = df[zone_lev].value_counts()
            else:
                filtered_df = df[eval(exp)]
                dict_vals_syn = filtered_df[zone_lev].value_counts()
            x, y = [], []
            for zone, num in zip(df_tot[zone_tot], df_tot[att]):
                x.append(dict_vals_syn[zone] if zone in dict_vals_syn else 0)
                y.append(num)
            base_line = [min(x), min(y), max(x), max(y)]
            plt.plot(base_line, base_line, color='orange', label='Base line')
            plt.scatter(x, y, alpha=0.5)
            plt.xlabel('Synthetic')
            plt.ylabel('Actual')
            plt.title(f'Level: {zone_lev} - Att: {name}')
            plt.legend()
            plt.savefig(f'output/scatter_compare_{zone_lev}_{name}.png')
            plt.close()
            print(f"Done saving files: Level: {zone_lev} - Att: {name}")
  