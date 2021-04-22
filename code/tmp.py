# %% Import module for preprocessing
import numpy as np
import pandas as pd
import datatable
import os
import re
from IPython.display import display
from data_preprocessing import *
pd.set_option("display.max_columns", None)
# %%
WORK_PATH = "/Users/lkh256/Studio/Endo_Helico"
SAVE_PATH = "/Users/lkh256/Studio/Endo_Helico/prepro_data"
# %%
input_file_name_1 = 'endo_biopsy_2019to2020_ehp.csv'
input_file_name_2 = "heli_results_2000to2009.csv"
output_file_name = 'helico_preprocessed_19to20_ehp.csv'
df_init_1 = preprocessing(WORK_PATH, SAVE_PATH, input_file_name_1, input_file_name_2, output_file_name)
# %%
df_init_1.drop(columns='h_pyl_positive', inplace=True)
df_init_1.to_csv(os.path.join(SAVE_PATH, 'helico_preprocessed_19to20_ehp.csv'), index=False, encoding='utf-8-sig')
# %%
