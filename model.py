from config import *
from lightgbm import LGBMClassifier, LGBMRegressor
import numpy as np
import pandas as pd
import pickle
import statsmodels.stats.api as sms
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import GroupKFold
from sklearn.compose import ColumnTransformer
import time
from tqdm import tqdm


def impute_po(
    df,
    cat_vars,
    treatment_var,
    outcome_var,
    n_folds=5,
    drop_cols=[],
    n_estimators=500,
    learning_rate=0.05,
    reg_objective="regression_l1",
    groups=None,
):

    column_trans = ColumnTransformer(
        [("categories", OneHotEncoder(handle_unknown="ignore"), cat_vars)],
        remainder="passthrough",
    )

    reg_model = LGBMRegressor(objective=reg_objective)

    reg_pipe = Pipeline([("encoder", column_trans), ("reg_model", reg_model)])

    # When splitting data into folds, we need to make sure all data for a given practice shows up in
    # a single split, otherwise we'll have leakage.  This code was written to allow other group
    # parameters to be passed because I was re-using some of this code for checking performance on
    # the 2016 ACIC datasets
    group_kfold = GroupKFold(n_splits=n_folds)
    splits = group_kfold.split(
        df.drop(columns=[outcome_var]), df[outcome_var], groups=groups
    )

    test_po = []
    split_list = []
    for train_index, test_index in splits:
        X_train = (
            df.drop(columns=[outcome_var])
            .drop(columns=drop_cols)
            .copy()
            .iloc[train_index, :]
        )
        print(f"{X_train.columns=}")
        y_train = df[outcome_var].copy().iloc[train_index]
        X_test = (
            df.drop(columns=[outcome_var])
            .drop(columns=drop_cols)
            .copy()
            .iloc[test_index, :]
        )
        y_test = df[outcome_var].copy().iloc[test_index]

        reg_pipe.fit(X_train, y_train)
        X_test[treatment_var] = 1
        test_treated_po = reg_pipe.predict(X_test)
        X_test[treatment_var] = 0
        test_untreated_po = reg_pipe.predict(X_test)

        test_po.append((test_treated_po, test_untreated_po))
        split_list.append((train_index, test_index))

    df["treated_po"] = 0
    df["untreated_po"] = 0
    df = df.reset_index(drop=True)

    for i in range(n_folds):
        pos = test_po[i]
        indices = split_list[i]
        df.loc[indices[1], "treated_po"] = pos[0]
        df.loc[indices[1], "untreated_po"] = pos[1]

    return df


def get_conf_int(diffs):
    # This is... not the right way to do this.
    conf_int = sms.DescrStatsW(diffs).tconfint_mean(alpha=0.1)
    return conf_int
