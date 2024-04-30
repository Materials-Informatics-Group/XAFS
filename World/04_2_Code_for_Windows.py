from larch import Interpreter
session = Interpreter()
import larch
from larch import io
from larch import xafs
from larch.io import read_ascii
from larch.xafs import pre_edge
from larch.xafs import mback
from statistics import stdev, variance, median
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import pandas as pd
import numpy as np
import os
import re
import math
import csv
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.neural_network import MLPClassifier
import time

start_time = time.time()

##########################################################
# The following three sections (#1-#3) are where users need to set parameters individually.
##########################################################
#1. Please verify the sections in each tsv file where the elements to be analyzed (element) and the expected substance name (substance) are recorded.
# Please change the folder_path1 and the value of i in the for loop according to your own data.
# The parts to be changed are indicated in the comments(#).
# Make sure that the tsv file names start with a data identification number (a number).
# Example: 0073_A.tsv

# Please enter the folder path where the tsv files are located into folder_path1.
# Please do not change "folder_path1 = r".
folder_path1 = r'C:\Users\naoto\Videos\input'
file_list1 = [os.path.join(folder_path1, f) for f in os.listdir(folder_path1) if f.endswith('.tsv')]
slash_count1 = folder_path1.count('\\')

result_list = []
for file_name in file_list1:
    with open(file_name, 'r') as f:
        file_name1 = file_name.split('\\')[int(slash_count1) + 1]
        file_name1 = file_name1.split('_')[0]
        
        element = None
        substance = None
        
        with open(file_name, 'r') as tsvfile:
            reader = csv.reader(tsvfile, delimiter='\t')
            for i, row in enumerate(reader):
                if i == 29: #The number here corresponds to the line number where the elements to be analyzed are recorded minus 1.
                    cell_value = row[1]
                    parts = cell_value.split(' ')
                    element = parts[0]
                    
                if i == 25: #The number here corresponds to the line number where the expected substance name are recorded minus 1.
                    substance = row[1]
                    
            result_list.append([file_name1, element, substance])

result_df1 = pd.DataFrame(result_list, columns=['Data_Number', 'Element', 'Substance'])
result_df1 = result_df1.sort_values('Data_Number')

###############################################################
#2. Set input_folder to the folder containing the txt files (raw data) for each dataset,
# and output_folder to the folder where the normalized data will be stored.
# Please input the folder paths accordingly.
# The output_folder can be used when inspecting the spectra.
# Make sure that the txt file names start with a data identification number (a number).
# Example: 0073_A.txt

input_folder  = '/home/yourname/XAFS/Raw_Data'
output_folder = '/home/yourname/XAFS/Normalized_Data'

###############################################################

for filename in os.listdir(input_folder):
    if filename.endswith('.txt'):
        file_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, f'{os.path.splitext(filename)[0]}_flattened.txt')

        dat = io.read_ascii(file_path, labels="energy mu")
        pre_edge(dat, _larch=session)

        combined_list = list(zip(dat.energy, dat.flat))

        with open(output_path, 'w') as file:
            for item in combined_list:
                file.write(f'{item[0]}\t{item[1]}\n')


folder_path = output_folder
file_list = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.txt')]

slash_count = folder_path.count('\\')
peak_list=[]
smallpeak_list=[]
peak_xpositions_list=[]
peak_ypositions_list=[]

for file_name in file_list:
    with open(file_name, 'r') as f:
        file_name1 = file_name
        file_name1 = file_name1.split('\\')[int(slash_count)+1]
        file_name1 = file_name1.split('_')[0]
        file_name2 = file_name
        file_name2 = file_name2.split('\\')[int(slash_count)+1]
        file_name2 = file_name2.split('_')[-2]

    if file_name2 not in ('001', '002', '003', '004', '005', '006', '007', '008', '009', '010'):
        file_name2 = '000'
    data = io.read_ascii(file_name, labels="energy mu")
    larch.xafs.pre_edge(data, _larch=session)
    
    ######################################################################
    #XANES Peak
    ######################################################################
    
    x = data.energy
    y = data.mu
    df = pd.DataFrame({'energy': x, 'mu': y})
    
###############################################################
#3. Users can set the data point to be the minimum point of the XANES absorption edge peak.
# The minimum point is defined as the point where the average of three consecutive data points first exceeds 0.05.
# Typically, min_data_option >= 1 is acceptable, indicating that the average of the first three consecutive data points exceeds 0.05.
# However, if there is noise in the pre-edge region before the absorption edge, it may lead to incorrect peak detection.
# Therefore, setting min_data_option >= 15 or 20 may also be appropriate.
# However, ensure that the number of data points in the pre-edge region is greater than the value of min_data_option.
    
    # Extract the minimum point
    df["mu_3"]=df["mu"].rolling(3).mean().round(1)
    threshold = 0.1
    min_energy_point = pd.DataFrame(columns=df.columns)
    
    min_data_option = 20 #Please change the value here.

    for index, row in df.iterrows():
        if index >= min_data_option and row['mu_3'] >= threshold:
            min_energy_point = df[index:].nsmallest(1, 'energy')
            break
###############################################################

    # Extract the maximum point
    max_points = df[(df['mu'].shift(1) < df['mu']) & (df['mu'].shift(-1) < df['mu'])]
    max_energy_points = max_points[(max_points['mu'].shift(1) < max_points['mu']) & (max_points['mu'].shift(-1) < max_points['mu'])]
    max_energy_point = max_energy_points[max_energy_points['mu'] >= data.mu[data.energy == data.e0][0]].nsmallest(1, 'energy')
    if max_energy_point.empty:
        max_energy_point = max_points.nlargest(1, 'mu')
   
    peak_width = max_energy_point['energy'].values[0] - min_energy_point['energy'].values[0]
    
    peak_list.append([file_name1, file_name2, data.mu[data.energy == data.e0][0], max_energy_point['mu'].values[0], peak_width])
    
    ######################################################################
    #EXAFS Peak
    ######################################################################
    larch.xafs.autobk(data, _larch=session)
    
    # Fourier Transform
    larch.xafs.xftf(data, kweight=3, kmin=2, kmax=16, dk=0.7, window="hanning", _larch=session)
    x = data.r
    y = data.chir_mag
    
    condition = (1 <= x) & (x <= 6)
    x_range = x[condition]
    y_range = y[condition]
    
    peaks, _ = find_peaks(y_range)
    
    peak_xpositions = [x_range[i] for i in peaks]
    peak_ypositions = [y_range[i] for i in peaks]

    max_peak_index = np.argmax(peak_ypositions)
    max_peak_xposition = peak_xpositions[max_peak_index]
    
    smallpeak_list.append([file_name1, file_name2, max(peak_ypositions), max_peak_xposition])

df = pd.DataFrame(peak_list, columns=['Data_Number', 'Block', 'Peak_E0_μt', 'Peak_Max_μt', 'Peak_Width'])
df = df.sort_values(['Data_Number', 'Block'])

df3 = pd.DataFrame(smallpeak_list, columns=['Data_Number', 'Block', 'Max_y', 'Max_y_xposition'])
df3 = df3.sort_values(['Data_Number', 'Block'])

df4 = pd.merge(df, df3, on=["Data_Number", "Block"], how="inner")

df6 = pd.merge(result_df1, df4, on=["Data_Number"], how="inner")

df12 = pd.read_csv('periodictable.csv')
df13 = pd.merge(df6, df12, on=["Element"], how="inner")
df13 = df13.sort_values(['Data_Number', 'Block'])
columns_to_extract = ['Data_Number', 'Peak_E0_μt', 'Peak_Max_μt', 'Max_y_xposition', 'Max_y', 'vdw_radius_alvarez', 'Peak_Width', 'gs_energy', 'fusion_enthalpy', 'num_unfilled']

df14 = df13[columns_to_extract]
df14_reset = df14.reset_index(drop=True)
df14 = df14_reset

##############################################################################
# Valence Classification (0, 1-3, 4-6)
##############################################################################
df008 = pd.read_csv('TrainData_for_Oxide&Valence_008.csv')

#########Oxide#################
target_A_8 = df008.iloc[:, 1]
targets_A_8 = np.array(target_A_8)
data1_8 = df008.iloc[:, 3:8]
datas1_8 = np.array(data1_8)
model_8 = RandomForestClassifier(random_state=0, n_estimators=80)
model_8.fit(datas1_8, targets_A_8)
pred_8 = df14
pred1_8 = pred_8.iloc[:, 1:6]
pred_data_8 = np.array(pred1_8)
predictionlist_8 = []
result_8 = model_8.predict(pred_data_8)
predictionlist_8.extend(result_8)
df_result_8 = pd.DataFrame(predictionlist_8, columns=['Predict_Oxide'])
results_8 = pd.concat([pred_8, df_result_8], axis=1)
results_8['Oxide'] = result_8
results_8 = pd.concat([results_8.iloc[:, 0], results_8.iloc[:, -1], results_8.iloc[:, 1:-1]], axis=1)

###########Valence##########################
target_B_8 = df008.iloc[:, 2]
targets_B_8 = np.array(target_B_8)
data2_A_8 = df008.iloc[:, 1]
data2_B_8 = df008.iloc[:, 3:7]
data2_C_8 = df008.iloc[:, 8:]
data2_8 = pd.concat([data2_A_8, data2_B_8, data2_C_8], axis=1)
datas2_8 = np.array(data2_8)
model_8V = RandomForestClassifier(random_state=0, n_estimators=80)
model_8V.fit(datas2_8, targets_B_8)
pred3_8 = results_8.iloc[:, 1:6]
pred4_8 = results_8.iloc[:, 7:-1]
pred5_8 = pd.concat([pred3_8, pred4_8], axis=1)
pred_data2_8 = np.array(pred5_8)
predictionlist_A_8 = []
result2_8 = model_8V.predict(pred_data2_8)
predictionlist_A_8.extend(result2_8)
df_result2_8 = pd.DataFrame(predictionlist_A_8, columns=['Predict_Valence(0, 1-3, 4-6)'])

#############################################################
# If you want to represent valence states 1-3 as 3 and valence states 4-6 as 4 to make it more user-friendly, please apply the following code as well.
replace_dict = {3: '1 - 3', 4: '4 - 6'}
df_result2_8['Predict_Valence(0, 1-3, 4-6)'] = df_result2_8['Predict_Valence(0, 1-3, 4-6)'].replace(replace_dict)
#############################################################

results_8 = pd.concat([pred_8, df_result_8, df_result2_8], axis=1)
results_8.to_csv('PredictData_for_Oxide&Valence_008.csv', index=False)

#display(pd.concat([results_8.iloc[:, 0], results_8.iloc[:, -2:]], axis=1)) # Please do not remove this comment.
df008 = pd.concat([results_8.iloc[:, 0], results_8.iloc[:, -2:]], axis=1)

##############################################################################
# Valence Classification (0, 1, 2, 3, 4, 5, 6)
##############################################################################
df006 = pd.read_csv('TrainData_for_Oxide&Valence_006.csv')

#########Oxide#################
target_A_6 = df006.iloc[:, 1]
targets_A_6 = np.array(target_A_6)
data1_6 = df006.iloc[:, 3:8]
datas1_6 = np.array(data1_6)
model_6 = RandomForestClassifier(random_state=0, n_estimators=80)
model_6.fit(datas1_6, targets_A_6)
pred_6 = df14
pred1_6 = pred_6.iloc[:, 1:6]
pred_data_6 = np.array(pred1_6)
predictionlist_6 = []
result_6 = model_6.predict(pred_data_6)
predictionlist_6.extend(result_6)
df_result_6 = pd.DataFrame(predictionlist_6, columns=['Predict_Oxide'])
results_6 = pd.concat([pred_6, df_result_6], axis=1)
# Corrected code
results_6['Oxide'] = result_6
results_6 = pd.concat([results_6.iloc[:, 0], results_6.iloc[:, -1], results_6.iloc[:, 1:-1]], axis=1)

###########Valence##########################
target_B_6 = df006.iloc[:, 2]
targets_B_6 = np.array(target_B_6)
data2_A_6 = df006.iloc[:, 1]
data2_B_6 = df006.iloc[:, 3:7]
data2_C_6 = df006.iloc[:, 8:]
data2_6 = pd.concat([data2_A_6, data2_B_6, data2_C_6], axis=1)
datas2_6 = np.array(data2_6)
model1_6V = RandomForestClassifier(random_state=0, n_estimators=80)
model2_6V = MLPClassifier(random_state=0, solver='lbfgs', alpha=0.4, activation='tanh', max_iter=800)
model_6V  = VotingClassifier(estimators=[('rf', model1_6V), ('mlp', model2_6V)], voting='soft', weights=[0.85, 0.15])
model_6V.fit(datas2_6, targets_B_6)
pred3_6 = results_6.iloc[:, 1:6]
pred4_6 = results_6.iloc[:, 7:-1]
pred5_6 = pd.concat([pred3_6, pred4_6], axis=1)
pred_data2_6 = np.array(pred5_6)
predictionlist_A_6 = []
result2_6 = model_6V.predict(pred_data2_6)
predictionlist_A_6.extend(result2_6)
df_result2_6 = pd.DataFrame(predictionlist_A_6, columns=['Predict_Valence(0, 1, 2, 3, 4, 5, 6)'])
results_6 = pd.concat([pred_6, df_result_6, df_result2_6], axis=1)
results_6.to_csv('PredictData_for_Oxide&Valence_006.csv', index=False)

#display(pd.concat([results_6.iloc[:, 0], results_6.iloc[:, -2:]], axis=1)) # Please do not remove this comment.
df006 = pd.concat([results_6.iloc[:, 0], results_6.iloc[:, -2:]], axis=1)

df_all = pd.concat([df008, df006.iloc[:, -1]], axis=1)
df_all2 = pd.merge(result_df1, df_all, on=["Data_Number"], how="inner")
display(df_all2)
df_all2.to_csv('PredictData_for_Oxide&Valence_all.csv', index=False)

# Calculate the total execution time
end_time = time.time()
execution_time = end_time - start_time
print("Total execution time:", execution_time, "seconds")
