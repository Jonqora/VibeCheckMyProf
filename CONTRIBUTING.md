<p align="center">
  <img src="https://github.com/Jonqora/VibeCheckMyProf/blob/main/scratch/image_files/vcmp_logo.png" />
</p>

# Linting

We have configured a python linter, flake8, to run on all pull requests. Your files will need to pass these tests to be approved in a PR.

If your files are within the `/scratch` folder, the linter will ignore them. 

Set up **flake8** locally by doing the following:

```
pip install flake8
```

Run flake8 on all files in a folder by navigating to the folder and using
```
flake8 .
```

You will see an output with error messages and locations for all linter errors. Correct the errors or, in special cases, add a comment to direct flake8 to ignore a rule for that location. (Google for how to do this for a certain error.)

# Repository Structure

## /web folder
Holds files relating to hosting the app webpage. There is a missing `config.js` folder that you will need to create following the setup guide in README.

## /scratch folder
This folder holds scratch work files; good for ideating and sharing but not part of the final project setup (yet). Please organize files inside folders according to their topic.

Linters are set to ignore this folder. Watch out when moving work out of the `/scratch` folder to make sure it passes linter checks.
