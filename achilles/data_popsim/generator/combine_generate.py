import logging as log
import click
import os
import generate_geo_cross_walk, generate_popsim_seeds, generate_totals, extra_steps

log.basicConfig(level=log.DEBUG, format="%(asctime)s %(message)s")

ls_geo_levels = [
    'SA1', 'SA2', 'SA3', 'SA4'
]

@click.command()
@click.option("-l", "--local-dir", required=True, help="Local data directory")
@click.option("-o", "--output-dir", required=True, help="Directory for generated data")
def main(local_dir, output_dir):
    log.info("Starting the generating")

    h_seed, p_seed = generate_popsim_seeds.mod(local_dir)
    log.info("Generate households seed")
    h_seed.to_csv(os.path.join(output_dir, f"h_test_seed.csv"), index=False)
    log.info("Generate persons seed")
    p_seed.to_csv(os.path.join(output_dir, f"p_test_seed.csv"), index=False)

    geo_df = generate_geo_cross_walk.mod(local_dir, output_dir)
    log.info("Generate geo cross walk")
    geo_df.to_csv(os.path.join(output_dir, "geo_cross_walk.csv"), index=False)

    path_file_tot = "2016_GCP_all_for_VIC_short-header/2016 Census GCP All Geographies for VIC/"
    for lev in ls_geo_levels:
        tot_file = generate_totals.mod(os.path.join(local_dir, path_file_tot), lev)
        tot_file.to_csv(os.path.join(output_dir ,f'{lev}_controls.csv'), index=False)

    extra_steps.getting_sum_totals(output_dir, export_csv=True)
    # extra_steps.refactor_weights_both(output_dir, export_csv=True)
    # extra_steps.adding_dummy_data(output_dir, export_csv=True)
    # extra_steps.process_geo_match_with_seed(output_dir, export_csv=True)

if __name__ == "__main__":
    #  python combine_generate.py -l ../source/ -o ../../../popsim/synthesis/data/
    main()
