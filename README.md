# Patho_grading_GUI

A GUI for pathology image visualization. 
[CSE583 Project (AUT 2023)]
## Contents
- [System requirements](#system-requirements)
- [Installation](#installation)
- [Data](#data)
- [Run example](#run-example)

## System requirements
This GUI is written in Python. Users should install Anaconda (tested on Conda 4.12.0, Python 3.9.13, Window 10)

In addition, the following packages are required, many of which come with Python/Anaconda. This code has been tested with the version number indicated, though other versions may also work.
 - pandas=1.4.4
  - matplotlib=3.5.2
  - pyqt=5.15.7

## Installation
After installing the required packages above, run the following command in Anaconda to clone this repository:
```bash
git clone git@github.com:PathoGUI/Patho_grading_GUI.git
```
To set up the environment, you can run the following: 
```
python setup.py install
```
Alternatively, run:
```
conda env create -f environment.yml

conda activate patho_gui_env
```
Look at requirements.txt, or 

## Data
Prostate cancer dataset is used for for testing out this GUI visualization tool. In total there are 182 pathology images (prostate biopsy), which come from a cohort of 56 patients. The format of the images are `.TIF` files. These prostate cancer image has an agressiveness of Gleason pattern 3 to 5. 


**Example of pathology image:**

<img src="./Data/Image_readme.png" alt="Sample data" width="300"/>

## Run example:

To run the GUI:

```bash
python pathogradinggui/GUI_pyqt5.py
```
To run unitest: 
```bash
python pathogradinggui/test_GUI_pyqt5.py
```


