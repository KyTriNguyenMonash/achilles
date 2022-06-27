import pandas as pd

if __name__ == "__main__":
    p_atts = ['PERSID', 'AGE', 'SEX', 'FULLTIMEWORK', 'PARTTIMEWORK', 'CASUALWORK', 'ANYWORK', 'HHID']
    h_atts = ['HHID', 'HHSIZE', 'CARS', 'CW_ADHHWGT_SA3','HomeSA3']
    
    # import data
    p_original_df = pd.read_csv("./data/source/VISTA_2012_16_v1_SA1_CSV/P_VISTA12_16_SA1_V1.csv")
    h_original_df = pd.read_csv("./data/source/VISTA_2012_16_v1_SA1_CSV/H_VISTA12_16_SA1_V1.csv")

    p_test_seed = p_original_df[p_atts]
    h_test_seed = h_original_df[h_atts]

    print(p_test_seed)
    print(h_test_seed)
