import pandas as pd
import os
import matplotlib.pyplot as plt

if __name__ == '__main__':
    path_input = '../../popsim/synthesis/data'
    path_output = '../../popsim/synthesis/output'

    input_tot_SA2_file = 'SA2_controls.csv'
    output_hh_file = 'synthetic_households.csv'
    output_p_file = 'synthetic_persons.csv'

    df_tot_SA2 = pd.read_csv(os.path.join(path_input, input_tot_SA2_file))
    df_output_hh = pd.read_csv(os.path.join(path_output, output_hh_file))
    df_output_p = pd.read_csv(os.path.join(path_output, output_p_file))
    # print(df_output_hh['HHSIZE'].value_counts())
    chosen_att_tot = 'Age_25_34_yr_P'
    related_att_seed = 'AGE'
    test_df = df_output_p[(df_output_p[related_att_seed] >= 25) & (df_output_p[related_att_seed] <= 34)]
    zone_seed = 'SA2'
    zone_tot = 'SA2_MAINCODE_2016'
    ls_zones = test_df[zone_seed]
    a = ls_zones.value_counts()
    x = []
    y = []
    for zone, num in zip(df_tot_SA2[zone_tot], df_tot_SA2[chosen_att_tot]):
        x.append(a[zone] if zone in a else 0)
        y.append(num)
    base_line = [min(x), min(y), max(x), max(y)]
    plt.plot(base_line, base_line, color='orange', label='Base line')
    plt.scatter(x, y, alpha=0.5)
    plt.xlabel('Synthetic')
    plt.ylabel('Actual')
    plt.legend()
    plt.show()
