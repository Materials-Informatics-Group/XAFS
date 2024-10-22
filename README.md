This script follows an algorithm that predicts and classifies "whether a material is an oxide or not" and "how many valence it has" based on the raw data obtained from the XAS measurement and the physical quantity of the material used in the measurement.
There are 3 variables that can be changed by the user: the line with detailed information about the XAS measurement (#1), the folder path containing the raw and normalized data (#2), and the minimum number of data to be recognized as the minimum point at the absorption edge (#3).
Please click [here for details](/World/SampleData/Code_for_Linux.py). 
XANES and EXAFS analysis is automatically performed by Larch, and some feature values are output as csv files.

The XAFS code is written in Python3 and uses the Larch, numpy, pandas and scikit-learn libraries for its calculations. 
This script requires "raw data of XAS measurement (.txt file)" and "detailed information about XAS analysis (.tsv file)" as input data sets. 
Please click [here for details](/World/02-1_Required_files.md). 
The output data set mainly includes "prediction of whether the measured substance is an oxide or not and how many valence values it has (csv file)" and "a table summarizing the numerical values of each characteristic (csv file)" as auxiliary information. 
Please click [here for details](/World/SampleData/Output_Example.md). 

Please cite the paper if you use this code for publication.
Miyasaka, Naotoshi, Fernando Gracia-Escobar, and Keisuke Takahashi. "Automatic Identification of X-ray Absorption Fine Structure Spectra via Machine Learning." The Journal of Physical Chemistry C (2024).
