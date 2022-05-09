from config import *
from generate_submission import *
from load_data import *
from model import *
import os
from tqdm import tqdm

for i in [individual_results_dir, practice_results_dir, submissions_dir]:
    os.makedirs(i, exist_ok=True)

for n in tqdm(range(1, 3401)):
    number = str(n).zfill(4)
    print(f"on file number {number}")
    df = load_data(number)
    print(df.head())

    df = impute_po(
        df,
        cat_vars,
        treatment_var,
        outcome_var,
        drop_cols=["id.practice", "id.patient", "post"],
        n_folds=2,
        reg_objective="regression_l1",
        groups=df["id.practice"],
    )

    summary_df = generate_file_summary_df_po(df, treatment_var, outcome_var, number)
    summary_df.to_csv(
        Path(individual_results_dir, f"summary_{number}.csv"), index=False
    )
    print(summary_df)
    practice_summary_df = generate_practice_summary_row_po(df, number)
