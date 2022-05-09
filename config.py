# path to directory that contains the patient, patient_year, practice, practice_year folders
data_dir = "data" 
# categorical features that will be one-hot encoded
cat_vars = ["X1", "X2", "X3", "X4", "X5", "V2", "V3", "V5", "lag_1_V2", "lag_2_V2", "lag_3_V2", "lag_1_V5", "lag_2_V5", "lag_3_V5"]
# id variables that won't be used as model features
id_vars = ["id.practice", "id.patient", "year"]
treatment_var = "Z"
outcome_var = "Y"
individual_results_dir = "individual_results"
practice_results_dir = "practice_results"
submissions_dir = "submissions"

# file name format for final submissions
import time
timestr = time.strftime("%Y%m%d-%H%M%S")
individual_submissions_filename = f"adam_true_bendorf_individual_estimates_{timestr}.csv"
practice_submissions_filename = f"adam_true_bendorf_practice_estimates_{timestr}.csv"


