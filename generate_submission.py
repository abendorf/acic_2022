from model import *
import numpy as np
import pandas as pd
from pathlib import Path
from tqdm import tqdm

def generate_summary_row_po(df, outcome_var, variable, level, year, number):
    df = df.query("year == 3 or year == 4")
    diffs = df['treated_po'] - df['untreated_po']
    mean_diffs = np.mean(diffs)
    print(f"{mean_diffs=}")
    print(f"diffs example: {diffs[:5]}")
    conf_int = get_conf_int(diffs)
    return pd.DataFrame({'dataset.num': [number], 'variable': [variable], 'level': [level], 'year': [year], 'satt': [mean_diffs], 'lower90': [conf_int[0]], 'upper90': [conf_int[1]]})

def generate_practice_summary_row_po(df, number):
    df = df.query("year == 3 or year == 4")
    diffs = df['treated_po'] - df['untreated_po']
    df['diffs'] = diffs
    practice_rows = []
    for i in tqdm(range(1, 501)):
        practice_diffs = df[df['id.practice']==i]['diffs'] 
        conf_int = get_conf_int(practice_diffs)
        practice_rows.append(pd.DataFrame({'dataset.num': [number], 'id.practice': [i], 'satt': [np.mean(practice_diffs)], 'lower90': [conf_int[0]], 'upper90': [conf_int[1]]}))
    summary = pd.concat(practice_rows)
    summary.to_csv(Path(practice_results_dir, f"practice_summary_{number}.csv"), index=False)

def generate_file_summary_df_po(df, treatment_var, outcome_var, number):

    summary_df_rows = []
    
    df_treated = df.query(f"{treatment_var}==1").copy()

    naive_est = df.query(f'{treatment_var}==1')[outcome_var].mean() - df.query(f'{treatment_var}==0')[outcome_var].mean()
    print(naive_est)

    # Generate required rows: https://acic2022.mathematica.org/submissions
    summary_df_rows.append(generate_summary_row_po(df_treated, outcome_var, "Overall", "NA", "NA", number))
    for year in [3, 4]:
        summary_df_rows.append(generate_summary_row_po(df_treated.query(f"year=={year}"), "Y", "Overall", "NA", year, number))
    for level in [0, 1]:
        summary_df_rows.append(generate_summary_row_po(df_treated.query(f"X1=={level}"), "Y", "X1", level, "NA", number))
    for level in ["A", "B", "C"]:
        summary_df_rows.append(generate_summary_row_po(df_treated.query(f"X2=='{level}'"), "Y", "X2", level, "NA", number))
    for level in [0, 1]:
        summary_df_rows.append(generate_summary_row_po(df_treated.query(f"X3=={level}"), "Y", "X3", level, "NA", number))
    for level in ["A", "B", "C"]:
        summary_df_rows.append(generate_summary_row_po(df_treated.query(f"X4=='{level}'"), "Y", "X4", level, "NA", number))
    for level in [0, 1]:
        summary_df_rows.append(generate_summary_row_po(df_treated.query(f"X5=={level}"), "Y", "X5", level, "NA", number))

    return pd.concat(summary_df_rows)

def save_file_summary_po(df, treatment_var, outcome_var, number):
    generate_file_summary_df(df, treatment_var, outcome_var, number).to_csv(Path(individual_results_dir, f"summary_{number}.csv"), index=False)
   
