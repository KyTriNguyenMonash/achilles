import pandas as pd
import numpy as np
import logging as log
import click
import os

log.basicConfig(level=log.DEBUG, format="%(asctime)s %(message)s")

SOURCE_FILE_NAME = "MB_2016_VIC.csv"
REQUIRED_ATTS = [
    "SA1_MAINCODE_2016", # Match with the 'HomeSA1' in the household file
    "SA2_NAME_2016", # Match with the 'HomeSA2' in the household file
    "SA3_NAME_2016" # Match with the 'HomeSA3' in the household file
]

# func to check the all the names in the seed file match with the ones in the geo cross walk

# generate the geo cross walk 

# save the file

# A main func to combine all and take the user cmd arguments

if __name__ == '__main__':
    df = pd.read_csv('./data/source/' + SOURCE_FILE_NAME)
    print(df[REQUIRED_ATTS])
