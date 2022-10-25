import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import logging as log
import click

log.getLogger('PIL').setLevel(log.WARNING)
log.getLogger('matplotlib.font_manager').setLevel(log.WARNING)
log.basicConfig(level=log.DEBUG, format="%(asctime)s %(message)s")
@click.command()
@click.option("-l", "--local-dir", required=True, help="Local directory that contains popsim")
@click.option("-o", "--output-dir", required=True, help="Directory for generated images")

def main(local_dir, output_dir):
    log.info("Starting the scatter plot for each zones")
    log.info("Loading the data into the memory...")
    controls_file = 'configs/controls.csv'
    output_hh_file = 'output/synthetic_households.csv'
    output_p_file = 'output/synthetic_persons.csv'

    to_df = lambda f: pd.read_csv(os.path.join(local_dir, f))
    df_controls = to_df(controls_file)
    # it may look like they are not used but they actually are using the 'expession' from controls.csv
    households = to_df(output_hh_file)
    persons = to_df(output_p_file)

    spec_ls = ['Total_dwelings', 'Tot_P_P'] # These are generated using the weights
    skip_ls = ['TOTALVEHS'] #Because it does not exist in the synthetic data

    ls_zones_lev = {
        # 'SA1': 'SA1_7DIGITCODE_2016',
        'SA2': 'SA2_MAINCODE_2016'
        # 'SA3': 'SA3_CODE_2016'
    }

    for zone_lev in ls_zones_lev:
        log.info(f"Load the controls file into memory of zone {zone_lev}\n")
        zone_tot = ls_zones_lev[zone_lev]
        tot_file = f'data/{zone_lev}_controls.csv'
        df_tot = to_df(tot_file)
        for name, df, att, exp in zip(df_controls['target'], df_controls['seed_table'], df_controls['control_field'],  df_controls['expression']):
            log.info(f"Start to process the att {name} of zone {zone_lev}")
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
            log.info(f"Plotting the scatter plot for att {name} at zone {zone_lev}")
            plt.plot(base_line, base_line, color='orange', label='Base line')
            plt.scatter(x, y, alpha=0.5)
            plt.xlabel('Synthetic')
            plt.ylabel('Census')
            plt.title(f'Level: {zone_lev} - Att: {name}')
            plt.legend()
            log.info(f"Generate .png image for plot: Level: {zone_lev} - Att: {name}\n")
            plt.savefig(os.path.join(output_dir, f'scatter_compare_{zone_lev}_{name}.png'))
            plt.close()


if __name__ == '__main__':
    # python utils.py -l ../../popsim/synthesis/ -o ./output/
    main()
  