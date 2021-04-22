# %% Import module for preprocessing
import numpy as np
import pandas as pd
import datatable
import os
import re
from IPython.display import display
pd.set_option("display.max_columns", None)
# %%
WORK_PATH = "/Users/lkh256/Studio/Endo_Helico"
df_orig = datatable.fread(os.path.join(WORK_PATH, "data/outcome/endo_biopsy_outcome_all.csv"), 
                          na_strings=['NA', '']).to_pandas()
df_orig['value'] = 1
display(df_orig.head())
# %%
df_proc = pd.pivot_table(index=['환자번호#1', '처방일자#2'], columns=['건강검진결과명#6'], 
                         values='value', data=df_orig).reset_index()
df_proc.rename(columns={df_proc.columns[-1]:'etc'}, inplace=True)
df_proc.fillna(0, inplace=True)
df_proc.columns.name = None
display(df_proc.head())

# %%
df_proc.to_csv(os.path.join(WORK_PATH, "data/outcome/endo_biopsy_outcome_prepro.csv"), index=False, encoding='utf-8-sig')
# %%
