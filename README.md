# Ph2_ACF_GUI
Grading GUI for CMS Tracker Phase2 Acquisition &amp; Control Framework

Uses the following python packages: PyQt5 (https://pypi.org/project/PyQt5/), pyqt-darktheme (https://pypi.org/project/pyqt-darktheme/)


################################
Set up the software environment:
################################

ANACONDA (RECOMMANDED) 

1. Install the ANACONDA:
https://docs.anaconda.com/anaconda/install/

run "conda --version" to check if the  installation is succesful

2. Create environment for GUI:
Run:
conda create --name GUI python=3.9   # Create the new environment
conda activate GUI                   # Use the environment "GUI"

3. Install PyQt5:
pip install PyQt5

4. Install MySQL connector:
pip install mysql-connector-python

5. Install Pillow:
pip install Pillow

6. Install NumPy:
pip install numpy

7. Install Matplotlib
pip install matplotlib

8. Install lxml
pip install lxml

With each new ternimal for GUI, run "conda activate GUI" to activate the environment

################################
Run the GUI
################################

```
source Setup.sh
cd Gui
python3 runApplication
```

















--------------------------- OLD RECIPE --------------------
Recipe for running pixel gui:
```
cd Gui && python setupDatabase.py
python acfGui.py
```

Add your working area to python PATH:
export PYTHONPATH=$PYTHONPATH:/PATH/TO/YOUR/WORKAREA
