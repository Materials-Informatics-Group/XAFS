#ユーザーが各自で調整すべき部分は以下の通りです。

#32・33行目のfolder_pathとoutput_folderのパス部分
#91行目の「XANES極小値」を示すデータポイントの最小値 (index部分で調整可能、デフォルトは1)
#155-170行目の、tsvファイルを読み込む部分で、分析対象元素(Elemnt)と吸収端(基本的にK)がペアとなっている行番号 (入力する値は、行番号-1)

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

# Aフォルダ内の.txtファイルに対して処理を行う
folder_path = '/home/miyasaka/M1_Research/F11.Code_Summary/05.Raw_Data_for_Test/NIMS_Data(Photon_Factory)/Practice' #規格化前の生データが入っているフォルダをパス表示で入力してください。
output_folder = '/home/miyasaka/M1_Research/F11.Code_Summary/05.Raw_Data_for_Test/NIMS_Data(Photon_Factory)/Practice2'  # 規格化後の生データを収集できるフォルダをパス表示で入力してください。

# Aフォルダ内の.txtファイルに対して処理を行う
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(folder_path, filename)
        output_path = os.path.join(output_folder, f'{os.path.splitext(filename)[0]}_flattened.txt')

        # データの読み込みと規格化
        dat = io.read_ascii(file_path, labels="energy mu")
        pre_edge(dat, _larch=session)

        # データの結合
        combined_list = list(zip(dat.energy, dat.flat))

        # テキストファイルにデータを書き込む
        with open(output_path, 'w') as file:
            for item in combined_list:
                file.write(f'{item[0]}\t{item[1]}\n')

#規格化後のデータに対して、スペクトルを作成していきます。
folder_path = output_folder
file_list = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.txt')]

slash_count = folder_path.count('/')
peak_list=[]
smallpeak_list=[]
peak_xpositions_list=[]
peak_ypositions_list=[]

for file_name in file_list:
    with open(file_name, 'r') as f:
        file_name1 = file_name
        file_name1 = file_name1.split('/')[int(slash_count)+1]
        file_name1 = file_name1.split('_')[0]
        file_name2 = file_name
        file_name2 = file_name2.split('/')[int(slash_count)+1]
        file_name2 = file_name2.split('_')[-2]

    if file_name2 not in ('001', '002', '003', '004', '005', '006', '007', '008', '009', '010'):
        file_name2 = '000'
    data = io.read_ascii(file_name, labels="energy mu")
    larch.xafs.pre_edge(data, _larch=session)
    
    ######################################################################
    #XANES Peak
    ######################################################################
    
    # データ点の座標を表すndarray
    x = data.energy
    y = data.mu
    df = pd.DataFrame({'energy': x, 'mu': y})
    
    #あえて、小数第1位に平滑化することで簡易化している。
    df["mu_3"]=df["mu"].rolling(3).mean().round(1)
    threshold = 0.1  # 閾値
    min_energy_point = pd.DataFrame(columns=df.columns)  # 空のDataFrameを作成
    for index, row in df.iterrows():
        if index >= 1 and row['mu_3'] >= threshold: #index >= 内の数値は、各自で設定してください。吸収端前のノイズを除去することができます。
            min_energy_point = df[index:].nsmallest(1, 'energy')
            break
    
    # 極大点の抽出
    max_points = df[(df['mu'].shift(1) < df['mu']) & (df['mu'].shift(-1) < df['mu'])]
    # 上に凸となる極大点を取得
    max_energy_points = max_points[(max_points['mu'].shift(1) < max_points['mu']) & (max_points['mu'].shift(-1) < max_points['mu'])]
    # 上に凸となる極大値のうち、吸収端よりも右側で最もエネルギーが小さいもの = 吸収端ピークの極大値
    max_energy_point = max_energy_points[max_energy_points['mu'] >= data.mu[data.energy == data.e0][0]].nsmallest(1, 'energy')
    # もしmax_energy_pointが検出されなかった場合、max_pointsで最も大きい値をmax_energy_pointとする
    if max_energy_point.empty:
        max_energy_point = max_points.nlargest(1, 'mu')
   
    peak_width = max_energy_point['energy'].values[0] - min_energy_point['energy'].values[0]
    
    peak_list.append([file_name1, file_name2, data.mu[data.energy == data.e0][0], max_energy_point['mu'].values[0], peak_width])
    
    ######################################################################
    #EXAFS Peak
    ######################################################################
    #EXAFS振動の中心線を引く
    larch.xafs.autobk(data, _larch=session)
    
    #フーリエ変換
    larch.xafs.xftf(data, kweight=3, kmin=2, kmax=16, dk=0.7, window="hanning", _larch=session)
    x = data.r
    y = data.chir_mag
    # 範囲の条件を作成します
    condition = (1 <= x) & (x <= 6)
    # 範囲内のデータを取得します
    x_range = x[condition]
    y_range = y[condition]
    
    # ピークを見つけます
    peaks, _ = find_peaks(y_range)
    
    # ピークの数と位置の表示
    peak_xpositions = [x_range[i] for i in peaks]
    peak_ypositions = [y_range[i] for i in peaks]

    # 最大のpeak_ypositionsに対応するx_rangeの値を取得します
    max_peak_index = np.argmax(peak_ypositions)
    max_peak_xposition = peak_xpositions[max_peak_index]
    
    # ピークの位置をグラフにプロット
    smallpeak_list.append([file_name1, file_name2, max(peak_ypositions), max_peak_xposition])

df = pd.DataFrame(peak_list, columns=['Data_Number', 'Block', 'Peak_E0_μt', 'Peak_Max_μt', 'Peak_Width'])
df = df.sort_values(['Data_Number', 'Block'])

df3 = pd.DataFrame(smallpeak_list, columns=['Data_Number', 'Block', 'Max_y', 'Max_y_xposition'])
df3 = df3.sort_values(['Data_Number', 'Block'])

df4 = pd.merge(df, df3, on=["Data_Number", "Block"], how="inner")

#######################################################
#Detail of Data
#######################################################

folder_path1 = '/home/miyasaka/M1_Research/F11.Code_Summary/05.Raw_Data_for_Test/NIMS_Data(Photon_Factory)/GroupB_only_tsv/Group1'
file_list1 = [os.path.join(folder_path1, f) for f in os.listdir(folder_path1) if f.endswith('.tsv')]
slash_count1 = folder_path1.count('/')

################################################################
#以下のfor文はtsvファイルの'Element'が位置する行によって、各自で適宜調整してください。
################################################################
result_list = []
for file_name in file_list1:
    with open(file_name, 'r') as f:
        file_name1 = file_name.split('/')[int(slash_count1)+1]
        file_name1 = file_name1.split('_')[0]
        # .tsvファイルを読み込みます
        with open(file_name, 'r') as tsvfile:
            reader = csv.reader(tsvfile, delimiter='\t')
            for i, row in enumerate(reader):
                if i == 29 :  #i ==の数値部分は、ユーザーが各自で設定してください。
                    cell_value = row[1]
                    parts = cell_value.split(' ')
                    element = parts[0] #基本的にこの部分は0でよいです。
                    
                    # 結果をリストに追加します
                    result_list.append([file_name1, element])

# 結果をDataFrameに変換します
result_df1 = pd.DataFrame(result_list, columns=['Data_Number', 'Element'])
result_df1 = result_df1.sort_values('Data_Number')
df6 = pd.merge(result_df1, df4, on=["Data_Number"], how="inner")

df12 = pd.read_csv('periodictable.csv')
df13 = pd.merge(df6, df12, on=["Element"], how="inner")
df13 = df13.sort_values(['Data_Number', 'Block'])
columns_to_extract = ['Data_Number', 'Peak_E0_μt', 'Peak_Max_μt', 'Max_y_xposition', 'Max_y', 'vdw_radius_alvarez', 'Peak_Width', 'gs_energy', 'fusion_enthalpy', 'num_unfilled']

df14 = df13[columns_to_extract]
df14_reset = df14.reset_index(drop=True)
df14 = df14_reset

##############################################################################
#価数判定008
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
# Corrected code
results_8['Oxide'] = result_8
results_8 = pd.concat([results_8.iloc[:, 0], results_8.iloc[:, -1], results_8.iloc[:, 1:-1]], axis=1)

#########################################
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
#ユーザーに分かりやすいような表示にするなら、以下のコードも実行すること！
replace_dict = {3: '1 - 3', 4: '4 - 6'}
df_result2_8['Predict_Valence(0, 1-3, 4-6)'] = df_result2_8['Predict_Valence(0, 1-3, 4-6)'].replace(replace_dict)
#############################################################

results_8 = pd.concat([pred_8, df_result_8, df_result2_8], axis=1)
results_8.to_csv('PredictData_for_Oxide&Valence_008.csv', index=False)

#print('Oxide & Valence0, 1-3, 4-6')
#display(pd.concat([results_8.iloc[:, 0], results_8.iloc[:, -2:]], axis=1))
df008 = pd.concat([results_8.iloc[:, 0], results_8.iloc[:, -2:]], axis=1)

##############################################################################
#価数判定006
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

#########################################
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

#print('Oxide & Valence0, 1, 2, 3, 4, 5, 6')
#display(pd.concat([results_6.iloc[:, 0], results_6.iloc[:, -2:]], axis=1))
df006 = pd.concat([results_6.iloc[:, 0], results_6.iloc[:, -2:]], axis=1)

df_all = pd.concat([df008, df006.iloc[:, -1]], axis=1)
df_all2 = pd.merge(result_df1, df_all, on=["Data_Number"], how="inner")
display(df_all2)
df_all2.to_csv('PredictData_for_Oxide&Valence_all.csv', index=False)

end_time = time.time()

# Calculate the total execution time
execution_time = end_time - start_time
print("Total execution time:", execution_time, "seconds")