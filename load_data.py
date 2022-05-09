from config import *
from pathlib import Path
import pandas as pd
from tqdm import tqdm


def load_raw_data(number):

    practice = pd.read_csv(Path(data_dir, "practice", f"acic_practice_{number}.csv"))
    practice_year = pd.read_csv(
        Path(data_dir, "practice_year", f"acic_practice_year_{number}.csv")
    )
    patient = pd.read_csv(Path(data_dir, "patient", f"acic_patient_{number}.csv"))
    patient_year = pd.read_csv(
        Path(data_dir, "patient_year", f"acic_patient_year_{number}.csv")
    )

    return practice, practice_year, patient, patient_year


def join_data(practice, practice_year, patient, patient_year):

    practice_joined = pd.merge(practice, practice_year, how="left", on=["id.practice"])
    # As explained in data merging instructions, the "Y" column from the practice_year file should
    # be dropped by anyone taking track 1.
    practice_joined = practice_joined.drop(columns=["Y"])
    practice_joined_patient = pd.merge(
        practice_joined, patient, how="left", on=["id.practice"]
    )
    all_joined = pd.merge(
        practice_joined_patient, patient_year, how="left", on=["id.patient", "year"]
    )

    # Come back to this to check that this is correct -- but appears to be b/c some patients otherwise lack outcomes for some years
    all_joined = all_joined.dropna()
    return all_joined


def lag_variables(df):
    df = df.sort_values(["id.patient", "year"])
    for col_name in tqdm(df.columns):
        # Only the "V" covariates  and "n.patients" vary from year to year.
        if (
            col_name not in id_vars
            and col_name != "Z"
            and (col_name == "Y" or "V" in col_name or col_name == "n.patients")
        ):
            for i in range(1, 4):
                df[f"lag_{i}_{col_name}"] = df.groupby("id.patient")[col_name].shift(i)
    return df


def load_data(number):
    practice, practice_year, patient, patient_year = load_raw_data(number)
    joined_data = join_data(practice, practice_year, patient, patient_year)
    final_data = lag_variables(joined_data)
    return final_data


if __name__ == "__main__":
    # Save some example joined datasets for debugging purposes
    df = load_data("0001")
    print(df.shape)
    df.to_csv("example.csv")
    df.head(1000).to_csv("example_head.csv")
    df = load_data("0002")
    print(df.shape)
    df.to_csv("example2.csv")
    df.head(1000).to_csv("example2_head.csv")
