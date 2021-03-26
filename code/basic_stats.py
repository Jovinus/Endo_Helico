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
df_init['num_case_year'] = df_init.groupby(['year'])['year'].transform(lambda x: len(x))
df_init.head()
# %% Yearly pylori occurence
stat_1 = df_init.groupby(['year', 'num_case_year'])['h_pyl_positive'].value_counts(dropna=False)
stat_2 = df_init.groupby(['year', 'num_case_year'])['h_pyl_positive'].value_counts(dropna=False, normalize=True)

display(stat_1, stat_2)
# %% Save stats
stat_1.reset_index(name='count').to_csv('../prepro_data/stat_1.csv', encoding='utf-8-sig', index=False)
stat_2.reset_index(name='percent').to_csv('../prepro_data/stat_2.csv', encoding='utf-8-sig', index=False)
# %%
