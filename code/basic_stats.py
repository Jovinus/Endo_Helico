#%% Import package to use
import pandas as pd
import datatable
from IPython.display import display
import matplotlib.pyplot as plt
import seaborn as sns
pd.set_option("display.max_columns", None)
# %%
df_init = datatable.fread('../prepro_data/h_pylori_tmp.csv', na_strings=['NA', ''], encoding='utf-8-sig').to_pandas()
df_init['SM_DATE'] = df_init['SM_DATE'].astype('datetime64')
df_init['year'] = df_init['SM_DATE'].dt.year
df_init.head()
# %%
display(df_init.groupby(['year'])['h_pyl_positive'].value_counts(dropna=False))
display(df_init.groupby(['year'])['h_pyl_positive'].value_counts(dropna=False, normalize=True))
# %%
