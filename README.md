# Predictive Process Monitoring of Temporal Logic Specifications with Statistical Guarantees

This repository contains all the code for the submitted paper "Predictive Process Monitoring of Temporal Logic Specifications with Statistical Guarantees" at the conference [BPM 2025](https://www.bpm2025seville.org/). 

## Instruction for reviewer
### File structure

The repository contains two folders:

- **/mitl**: contains all the code necessary for offline monitoring of Boolean Semantics and Time Robustness of MITL formulae.
- **/dataset** an empty folder (that you need to create) where save the [BPIC Challenge 2017](https://ais.win.tue.nl/bpi/2017/challenge.html) dataset available [here](https://data.4tu.nl/articles/dataset/BPI%20Challenge%202017/12696884).
- **/remove_partial**: contains the generated files and models. 

and 4 numered Jupyter notebooks that you can execute in order to retrieve results. Please refer to papers and notebook comments for detailed pipeline explaination.

### Dependencies
You need to install dependencies available in requirements.txt (if you use pip) or environment.yml (if you are using conda).