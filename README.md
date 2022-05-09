This repository contains code for my submission to the 2022 American Causal Inference Conference data challenge.
For more information about the data challenge, see https://acic2022.mathematica.org/

If you happen to look at this code and have any questions or comments, please direct those to abendorf at <insert name of google's popular email service here>.  I am not a causal inference researcher, just an interested data person trying to learn more about causal inference, so I would greatly appreciate any feedback from more knowledgeable people.

SUMMARY OF MY APPROACH:

After loading the data and joining it, I lag all time-varying covariates (creating columns with names like lag_1_Y, lag_2_Y, etc.).  I then split the data into two folds, making sure that all data for each practice ends up in the same fold (to prevent leakage).  I then train a LightGBM model on one fold and generate predictions for the other fold by first setting Z = 0 and then setting Z = 1.  I take the difference between those predictions for each pair of individual and year and aggregate those estimates appropriately to get individual-level and practice-level estimates.

HOW TO RUN THE CODE:

0. Download and unzip the *Track 1* datasets from https://acic2022.mathematica.org/data
1. Fill out the configuration settings in config.py
2. Install poetry, which this repo uses for dependency management.  Instructions here: https://python-poetry.org/docs/   
3. Create a poetry environment and install required packages by running *poetry install*
4. Run the main.py script using the command *poetry run python main.py*.  Individual-level and practice-level estimates will be saved in the individual_results_dir and practice_results_dir directories specified in config.py.  Note that this step takes about 24 hours on my desktop (Intel 9600K, NVIDIA GeForce RTX 2060, data on a solid state drive).
5. Run the combine_submission_files.py script using the command *poetry run python combine_submission_files.py* to generate the final submissions, which will be saved in the submissions_dir directory specified in config.py.
