# achilles
This directory is set up and managed by poetry dependencies management. Please refer to [this](https://python-poetry.org/docs/) to ensure
you have Poetry installed. 

# Getting started
Clone and create the virtual environment:
```
git clone <REPOSITORY-URL>
cd achilles
poetry install
```

1. Please down-load VISTA data for persons `P_VISTA12_16_SA1_V1.csv` and `H_VISTA12_16_SA1_V1.csv` [here](https://drive.google.com/drive/folders/16-MSqeFtMXx843kdyICShRKSMSDlWKLQ) and put it in popsim-input folder.

3. Generate the persons and households seeds by execute the following command line.
```
poertry run generate-popsim-seeds -l popsim-input -o popsim-output
```


