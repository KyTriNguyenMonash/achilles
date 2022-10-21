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

# Running instruction

1. Download `source.zip` from [here](https://drive.google.com/drive/folders/16-MSqeFtMXx843kdyICShRKSMSDlWKLQ) and extract the foler `source`. 

2. Put the folder `source` into the `data_popsim`
```
cd achilles\data_popsim
```

3. Run the scripts inside the `generator` folder to get the data. You can run each file seperately or the easiest would be running the `combine_generate.py` to get all the needed data for PopSim. For example:
```
cd achilles\data_popsim\generator
python combine_generate.py -l ../source/ -o ../../../popsim/synthesis/data/
```

4. By this steps you should have all the files you need to run PopSim in the `popsim\synthesis\data`. If the folder `data` does not exist creat one then run step 3.
```
cd popsim\synthesis
mkdir data
```
5. Run the PopSim. The current configuration is for the complex run (with many control atts) and you should expect a run around 1 hour or more. For simple testing you can change the *control_file_name* in `setting.yaml` (line 102) to `control_simple.csv`.
```
cd popsim\synthesis
python run_popsim.py
```

6. If everything goes right, you will have all the needed results (especially the synthetic data) in the `output` folder
```
cd popsim\synthesis\output
```

7. After that, you can run the validation as well to check the results. There is the Jupyter Notebook `validation.ipynb` that is based from the source code example. You may have to install the jupyter notebook.
```
cd validation
jupyter notebook validation.ipynb
```

8. To create the scatter plots, run the below code
```
cd validation\custom
python utils.py -l ../../popsim/synthesis/ -o ./output/
```

9. You can view the plots in the `output` folder, if the `output` folder does not exist yet, create one and run step 8.
```
cd validation\custom
mkdir output
```
