# tic-tac-toe

This repository contains the project code for a tic-tac-toe game engine implemented using Deep Reinforcement Learning.

## Setup

To get started, follow the [GitHub instructions](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account) to generate an SSH key and clone the repo. Once the repo has been successfully cloned, open a command line terminal window, navigate to the repository, and enter the following commands:
1. Run `conda env create -f environment.yml` to create the environment.
2. Run `conda env list` to check that the environment was sucessfully created. You should see the environment `tic_tac_toe` listed.
3. Run `conda activate tic_tac_toe` to install necessary packages and dependencies, and activate the enviornment.
4. Run `pip install .` to import the necessary modules.

To update the environment after making changes to the `environment.yml` file, run `conda env update --file environment.yml --prune`.