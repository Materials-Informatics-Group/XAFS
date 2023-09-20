このコードを走らせるためには、次のファイルが必要となります。

なお、**ファイル名の先頭には、データ識別番号を各自でつけてください**。

例えば、A.txt / A.tsvではなく、001_A.txt / 001_A.tsv等としてください。

(自動的につけるコードは別途配布できます。詳しくは、以下の**Part2-1**のコードを参照してください)。

----------------------------------------------------------------------

・**生データのtxtファイル** (第1列：X線のエネルギー(スペクトルの横軸)、第2列：吸収係数(スペクトルの縦軸))

※吸収係数については、規格化する前でも、規格化した後でもどちらでも構いません。

※X線のエネルギーが「分光器の角度」、吸収係数が「入射光と透過光の各値(つまり、吸収係数計算前)」の場合(**9809フォーマット**)は、以下の**Part2-2**のコードを利用し、それぞれX線のエネルギーと吸収係数を算出してください。

・**分析に関する詳細情報を含んだ、tsvファイル** (少なくとも、分析対象元素と吸収端名が含まれていること)

※「Fe K」→分析対象元素がFeで、K吸収端 / 「Cu L21」→分析対象元素がCuで、L21吸収端

## Part2-1
#<自動的に各データに対して識別番号をつけることができるコード>
#各データのtxtファイルとtsvファイルが、同じzipファイルに含まれていることが望ましい

import os

\# 番号をつけたいzipファイルが含まれているフォルダのパスを指定
A_folder_path = '/home/miyasaka/M1_Research/F11.Code_Summary/01.RawData_Package/D.Group4(dat_ex3_txt_20210724-21_Spring_0658-2239)'

# 指定したフォルダ内のzipファイルのパスとModificate_Dateを取得
zip_paths = [(os.path.join(A_folder_path, file), os.path.getmtime(os.path.join(A_folder_path, file))) for file in os.listdir(A_folder_path) if file.endswith('.zip')]

# Modificate_Dateでソート (各zipファイルが指定フォルダに追加された順に識別番号を付与)
zip_paths_sorted = sorted(zip_paths, key=lambda x: x[1])

# zipファイル名を変更
for i, (zip_patha, _) in enumerate(zip_paths_sorted):
    new_name = os.path.join(A_folder_path, str(i) + '.zip')
    os.rename(zip_path, new_name)

#------------------------------------------------------------------------------
#改めて以下のコードを入力して下さい

import os

# Aフォルダのパスを指定
A_folder_path = '/home/miyasaka/M1_Research/F11.Code_Summary/01.RawData_Package/A.Group1(ex3_txt_20220620_Hokkaido_0209-0313)'

# Aフォルダ内のフォルダのパスを取得
folder_paths = [os.path.join(A_folder_path, folder) for folder in os.listdir(A_folder_path) if os.path.isdir(os.path.join(A_folder_path, folder)) and folder.isdigit()]

# 各フォルダ内の.txt, .tsvファイルの名前を変更
for folder_path in folder_paths:
    for file in os.listdir(folder_path):
        if file.endswith('.txt'): #.tsvと変えても良い
            old_path = os.path.join(folder_path, file)
            new_path = os.path.join(folder_path, folder_path.split('/')[-1] + '_' + file)
            os.rename(old_path, new_path)


## Part2-2
#9809フォーマットの場合は、以下のコードを実施し、X線のエネルギーと吸収係数を求めてください。

#XAFSスペクトルに必要な2列目(Energy)・4列目・5列目(μt)を抽出

import os
import numpy as np

A_folder = '/home/miyasaka/M1_Research/F11.Code_Summary/05.Raw_Data_for_Test/NIMS_Data(Photon_Factory)/GroupB_only_txt_Part1' #抽出前のデータ(生データ)が含まれているフォルダ
C_folder = '/home/miyasaka/M1_Research/F11.Code_Summary/05.Raw_Data_for_Test/NIMS_Data(Photon_Factory)/GroupB_only_txt_Part2' #抽出後のデータが含まれているフォルダ

file_list = [f for f in os.listdir(A_folder) if f.endswith('.txt')]

for file_name in file_list:
    input_file_path = os.path.join(A_folder, file_name)
    output_file_path = os.path.join(C_folder, file_name)
    
    with open(input_file_path, 'r') as f:
        lines = f.readlines()
    
    data = []
    for line in lines[2:]:
        values = line.split()
        if len(values) >= 5:
            data.append([float(values[1]), float(values[3]), float(values[4])])
    
    data = np.array(data)
    
    np.savetxt(output_file_path, data, fmt='%.6f')

---------------------------------------------------------------------------------------------------
#分光結晶や測定法によって、数値を変える必要があります。

import os
import numpy as np
import math

A_folder = '/home/miyasaka/M1_Research/F11.Code_Summary/05.Raw_Data_for_Test/NIMS_Data(Photon_Factory)/GroupB_only_txt_Part2_111' #抽出後のデータが含まれているフォルダ(上のC_folderと同じパス)
C_folder = '/home/miyasaka/M1_Research/F11.Code_Summary/05.Raw_Data_for_Test/NIMS_Data(Photon_Factory)/GroupB_only_txt_Part3' #計算後のデータが含まれているフォルダ(いわゆる、従来の規格化前のデータ)

file_list = [f for f in os.listdir(A_folder) if f.endswith('.txt')]

for file_name in file_list:
    input_file_path = os.path.join(A_folder, file_name)
    output_file_path = os.path.join(C_folder, file_name)
    
    with open(input_file_path, 'r') as f:
        lines = f.readlines()
    
    data = []
    for line in lines:
        values = line.split()
        if len(values) >= 3:
            value1 = 12398.42436 * (1 / (2 * 3.13551 * math.sin(math.radians(float(values[0]))))) #分光結晶にSi(111)を用いたならば、3.13551。Si(311)ならば1.63747。
            value2 = math.log(float(values[1]) / float(values[2])) #測定法が透過法ならば、math.log(float(values[1]) / float(values[2]))。蛍光法ならば、float(values[2]) / float(values[1])。
            data.append([value1, value2])
    
    data = np.array(data)
    
    np.savetxt(output_file_path, data, fmt='%.6f')
