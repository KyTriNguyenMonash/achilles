import pandas as pd
import numpy as np

def is_unique_att(df, unique_att):
    N = df.shape[0]
    test_N = len(df[unique_att].unique())
    return True if N==test_N else False

if __name__ == "__main__":
    p_atts = ['PERSID', 'AGE', 'SEX', 'FULLTIMEWORK', 'PARTTIMEWORK', 'CASUALWORK', 'ANYWORK', 'HHID']
    h_atts = ['HHID', 'HHSIZE', 'CARS', 'CW_ADHHWGT_SA3','HomeSA3']
    
    # import data
    p_original_df = pd.read_csv("./data/source/VISTA_2012_16_v1_SA1_CSV/P_VISTA12_16_SA1_V1.csv")
    h_original_df = pd.read_csv("./data/source/VISTA_2012_16_v1_SA1_CSV/H_VISTA12_16_SA1_V1.csv")

    p_test_seed = p_original_df[p_atts]
    h_test_seed = h_original_df[h_atts]

    # Checking the unique atts
    if not is_unique_att(p_test_seed, 'PERSID'):
        raise Exception("THE ID OF PERSON IS NOT UNIQUE")
    if not is_unique_att(h_test_seed, 'HHID'):
        raise Exception("THE ID OF THE HOUSEHOLD IS NOT UNIQUE")

    # Further processing
    p_test_seed.loc[p_test_seed['CASUALWORK'] == 'Yes', 'ANYWORK'] = 'CASUALWORK'
    p_test_seed.loc[p_test_seed['PARTTIMEWORK'] == 'Yes', 'ANYWORK'] = 'PARTTIMEWORK'
    p_test_seed.loc[p_test_seed['FULLTIMEWORK'] == 'Yes', 'ANYWORK'] = 'FULLTIMEWORK'
    p_test_seed = p_test_seed.drop(columns=['FULLTIMEWORK', 'PARTTIMEWORK', 'CASUALWORK'])

    h_test_seed['CARS'] = np.where(h_test_seed['CARS'] == 0, 'No', 'Yes')

    p_test_seed.to_csv('./data/p_test_seed.csv', index=False)
    h_test_seed.to_csv('./data/h_test_seed.csv', index=False)
