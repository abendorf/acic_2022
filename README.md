This repository contains code for my submission to the 2022 American Causal Inference Conference data challenge.
For more information about the data challenge, see https://acic2022.mathematica.org/

If you happen to look at this code and have any questions or comments, please direct those to abendorf at <insert name of google's popular email service here>.  I am not a causal inference researcher, just an interested layman, so I would greatly appreciate any feedback from more knowledgeable folks.   

HOW TO RUN THE CODE:

0. Download and unzip the *Track 1* datasets from https://acic2022.mathematica.org/data
1. Fill out the configuration settings in config.py
2. Install poetry, which this repo uses for dependency management.  Instructions here: https://python-poetry.org/docs/   
3. Create a poetry environment and install required packages by running *poetry install*
4. Run the main.py script using the command *poetry run python main.py*.  Individual-level and practice-level estimates will be saved in the individual_results_dir and practice_results_dir directories specified in config.py.  
5. Run the combine_submission_files.py script using the command *poetry run python combine_submission_files.py* to generate the final submissions, which will be saved in the submissions_dir directory specified in config.py.
