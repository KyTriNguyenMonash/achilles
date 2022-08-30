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

    SA2_tot_file = 'data/SA2_controls.csv'
    df_tot_SA2 = to_df(SA2_tot_file)
    spec_ls = ['Total_dwelings', 'Tot_P_P']
    skip_ls = ['TOTALVEHS']
    for df, att, exp in zip(df_controls['seed_table'], df_controls['control_field'],  df_controls['expression']):
        if att in skip_ls: continue
        if att in spec_ls: continue
        df = eval(df)
        filtered_df = df[eval(exp)]
        zone_lev = 'SA2'
        zone_tot = 'SA2_MAINCODE_2016'
        dict_vals_syn = filtered_df[zone_lev].value_counts()
        x, y = [], []
        for zone, num in zip(df_tot_SA2[zone_tot], df_tot_SA2[att]):
            x.append(dict_vals_syn[zone] if zone in dict_vals_syn else 0)
            y.append(num)
        base_line = [min(x), min(y), max(x), max(y)]
        plt.plot(base_line, base_line, color='orange', label='Base line')
        plt.scatter(x, y, alpha=0.5)
        plt.xlabel('Synthetic')
        plt.ylabel('Actual')
        plt.title(f'Level: {zone_lev} - Att: {att}')
        plt.legend()
        plt.show()
  