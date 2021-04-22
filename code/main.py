# %% Import module for preprocessing
import numpy as np
import pandas as pd
import datatable
import os
import re
from IPython.display import display
from data_preprocessing import *
pd.set_option("display.max_columns", None)
# %% Define workpath
WORK_PATH = "/Users/lkh256/Studio/Endo_Helico"
SAVE_PATH = "/Users/lkh256/Studio/Endo_Helico/prepro_data"
# %% Load and preprocessing data 1
input_file_name_1 = 'endo_biopsy_2000to2009.csv'
input_file_name_2 = "endo_biopsy_outcome_prepro.csv"
output_file_name = 'endo_preprocessed_00to09.csv'
df_init_1 = preprocessing_2(WORK_PATH, SAVE_PATH, input_file_name_1, input_file_name_2, output_file_name)
# %% Load and preprocessing data 2
input_file_name_1 = 'endo_biopsy_2008to2020.csv'
input_file_name_2 = "endo_biopsy_outcome_prepro.csv"
output_file_name = 'endo_preprocessed_08to20.csv'
df_init_2 = preprocessing_2(WORK_PATH, SAVE_PATH, input_file_name_1, input_file_name_2, output_file_name)
# %% Concatenate multiple dataframes
df_preprocessed = pd.concat((df_init_1, df_init_2), axis=0)

# impute missing columns
df_preprocessed[df_preprocessed.columns[5:-1]] = df_preprocessed[df_preprocessed.columns[5:-1]].fillna(0)

# drop missing script data
df_preprocessed = df_preprocessed[df_preprocessed['result_text'].notnull()].reset_index(drop=True)

display(df_preprocessed.head())
# %%
#### Save preprocessed data
df_preprocessed.to_csv('../prepro_data/nlp_endo_set.csv', index=False, encoding='utf-8-sig')
# %%
