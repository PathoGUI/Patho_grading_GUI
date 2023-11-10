## Python library installation for GUI_pyqt5.py
Create new environement name CSE583 and install specific python version: 
```
conda create --name CSE583 python=3.9.13
```
Activate the environment: 
```
conda activate CSE583
```
Install all the necessary library: pandas, matplotlib, and pyqt (numpy will be installed when matplotlib is installed)
```
conda install pandas=1.4.4
```
```
conda install matplotlib=3.5.2
```
```
conda install pyqt=5.15.7
```
### Alternately

Run: 
```
conda create env create -f CSE583.yml
```