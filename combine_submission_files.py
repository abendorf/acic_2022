from config import *
import os
import pandas as pd
from pathlib import Path
from tqdm import tqdm

# Individual-level submission

file_list = os.listdir(individual_results_dir)
df_list = []
for file_name in file_list:
    df_list.append(pd.read_csv(Path(individual_results_dir, file_name)))
df = pd.concat(df_list)

print(df.shape)
print(df.columns)
df["dataset.num"] = df["dataset.num"].astype('str')
df["dataset.num"] = df["dataset.num"].str.zfill(4)
print(df.columns)
df.sort_values(["dataset.num", "variable", "level", "year"], na_position="first").fillna("NA").to_csv(Path(submissions_dir, individual_submissions_filename), index=False)

# Practice-level submission

file_list = os.listdir(practice_results_dir)
df_list = []
for file_name in file_list:
    df_list.append(pd.read_csv(Path(practice_results_dir, file_name)))
df = pd.concat(df_list)
df["dataset.num"] = df["dataset.num"].astype('str')
df["dataset.num"] = df["dataset.num"].str.zfill(4)

practice_year_dir = Path(data_dir, "practice_year")
file_list = os.listdir(practice_year_dir)
practice_rows = []
for file_name in tqdm(file_list):
    py_df = pd.read_csv(Path(practice_year_dir, file_name))
    row = py_df.query("Z==1")[['id.practice']].drop_duplicates()
    number = file_name.split("_")[-1].split('.')[0]
    row['dataset.num'] = number
    practice_rows.append(row)
py_df = pd.concat(practice_rows).sort_values(['dataset.num', 'id.practice'])
df = pd.merge(df, py_df, how='inner', on=['dataset.num', 'id.practice'])

df.sort_values(['dataset.num', 'id.practice']).to_csv(Path(submissions_dir, practice_submissions_filename), index=False)
