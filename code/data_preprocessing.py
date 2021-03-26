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

#### Read script data that we want to classify 
df_script = datatable.fread(os.path.join(WORK_PATH, "data/endo_biopsy_2008to2020.csv"), 
                            na_strings=['', 'NA'], encoding='utf-8-sig').to_pandas()

#### Change data type to datetime64 from object
column_mask = ['처방일자#5', '시행일시#6']
df_script[['SM_DATE', 'EXEC_TIME']] = df_script[column_mask].astype('datetime64')
print("Number of case = {}".format(len(df_script)))
display(df_script.head())


#### Read label data
df_results = datatable.fread(os.path.join(WORK_PATH, "data/heli_results_2008to2020.csv"),
                             na_strings=['', 'NA'], encoding='utf-8-sig').to_pandas()
#### Change data type to datetime64 from object
df_results['SM_DATE'] = df_results['처방일자#2'].astype('datetime64')
print("Number of case = {}".format(len(df_results)))
display(df_results.head())

# %% Data Sample 
#### Print sample data
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

# %% Selct necessary columns
col_to_select = ['ID', 'SM_DATE', 'EXEC_TIME','처방코드', 'result_text', 'h_pyl_positive']
df_select = df_all[col_to_select].copy()
df_select.head()

# %% Strip the unnecessary patterns
#### Define pattern to remove
rm_pattern = r"[=]|[-]|[▣]|[가-힣]|[\n]|[\r]|[(\d)]"
tmp = df_script['검사결과내용#9'].head(1).values[0]
print(tmp)
#### Check pattern works
print(re.sub(r'\s+', ' ', re.sub(rm_pattern, '', tmp)))

def remove_pattern(x):
    rm_pattern = re.compile("[=]|[-]|[▣]|[가-힣]|[\n]|[\r]|[()]")
    if x == 'nan':
        return np.nan
    else:
        #### remove special characters
        x = re.sub(rm_pattern, ' ', x)
        #### subsitute multiple white space to single white space
        x = re.sub(r'\s+', ' ', x)
        return x

print(remove_pattern(df_script['검사결과내용#9'].head(1).values[0]))
# %% Preprocessing the data

df_select['text_processed'] = df_select['result_text'].apply(lambda x: remove_pattern(str(x)))
display(df_select.head())

# %% Save Data
df_select.to_csv(os.path.join(WORK_PATH, 'prepro_data/helico_preprocessed.csv'), index=False, encoding='utf-8-sig')
# %%
