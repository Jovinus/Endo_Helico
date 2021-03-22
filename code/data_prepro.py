# %% Import module for preprocessing
import pandas as pd
import datatable
import os
from IPython.display import display
pd.set_option("display.max_columns", None)
# %%
WORK_PATH = "/Users/lkh256/Studio/Endo_Helico"
df_script = datatable.fread(os.path.join(WORK_PATH, "data/endo_biopsy_2020.csv"), 
                            na_strings=['', 'NA'], encoding='utf-8-sig').to_pandas()
df_script['SM_DATE'] = df_script['처방일자#5'].astype('datetime64')
df_script['EXEC_TIME'] = df_script['시행일시#6'].astype('datetime64')
print("Number of case = {}".format(len(df_script)))
display(df_script.head())

df_results = datatable.fread(os.path.join(WORK_PATH, "data/heli_results_2020.csv"),
                             na_strings=['', 'NA'], encoding='utf-8-sig').to_pandas()
df_results['SM_DATE'] = df_results['처방일자#2'].astype('datetime64')
print("Number of case = {}".format(len(df_results)))
display(df_results.head())
# %% Data Sample 
print(df_script['검사결과내용#9'].head(1).values)
# %% Check result dataset
df_results['건강검진결과명#6'].value_counts()
# %% Merge script data with results
df_all = pd.merge(df_script, df_results, how='left', left_on=['환자번호#1', 'SM_DATE'],
                  right_on=['환자번호#1', 'SM_DATE'])

#### Assign 1 if h.pylori is present from biopsy, 0 for less
df_all['h_pyl_positive'] = df_all['건강검진결과명#6'].notnull().astype(int)
display(df_all.head())
# %% Drop the unnesseary columns
col_to_drop = ['처방일자#2', '검사코드#3', '검사코드명#4', '건강검진결과코드#5', '건강검진결과명#6', '결론진단내용#10', '처방일자#5']
df_all.drop(columns=col_to_drop, inplace=True)
display(df_all.head())
# %% Change column order and name
col_nm_to_ch = {'환자번호#1':'ID', '검사결과내용#9':'result_text', '처방코드#3':'처방코드'}
df_all.rename(columns=col_nm_to_ch, inplace=True)
# %%
col_to_select = ['ID', 'SM_DATE', 'EXEC_TIME','처방코드', 'result_text', 'h_pyl_positive']
df_select = df_all[col_to_select].copy()
df_select.head()
# %% Strip the unnecessary patterns
df_select['result_text'] = df_select['result_text'].apply(lambda x: x.split(sep='▣ 결론 및 진단')[1])
display(df_select.head())
# %% Save Data
df_select.to_csv(os.path.join(WORK_PATH, 'prepro_data/helico_sample.csv'), index=False, encoding='utf-8-sig')
# %%
