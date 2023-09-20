生データから酸化物判定・価数判定を行うためには、以下のファイルが必要となります。

なお、**ファイル名の先頭には、データ識別番号を各自でつけてください**。

例えば、A.txt / A.tsvではなく、**001_A.txt / 001_A.tsv**等としてください。

(自動的につけるコードは別途配布できます。詳しくは、以下の**Part2-1**のコードを参照してください)。

----------------------------------------------------------------------

・**生データのtxtファイル** (第1列：X線のエネルギー (スペクトルの横軸) 、第2列：吸収係数 (スペクトルの縦軸) )
> [!NOTE]
> ※吸収係数については、規格化する前でも、規格化した後でもどちらでも構いません。
> 
> ※X線のエネルギーが「分光器の角度」、吸収係数が「入射光と透過光の各値(つまり、吸収係数計算前)」の場合(**9809フォーマット**)は、以下の**Part2-2**のコードを利用し、それぞれX線のエネルギーと吸収係数を算出してください。

・**分析に関する詳細情報を含んだ、tsvファイル** (少なくとも、「分析対象元素と吸収端名のペア」と「予想物質名」が含まれていること)
> [!NOTE]
> ※「Fe K」→分析対象元素がFeで、K吸収端 / 「Cu L21」→分析対象元素がCuで、L21吸収端

----------------------------------------------------------------------

## Part2-1 <自動的に各データに対して識別番号をつけることができるコード>
各データのtxtファイルとtsvファイルが、同じzipファイルに含まれていることを前提とします。

```
import os

# 番号をつけたいzipファイルが含まれているフォルダのパスを指定
# 利用者は、A_folder_pathの''内を適宜変更してください。
A_folder_path = '/home/miyasaka/M1_Research/F11.Code_Summary/01.RawData_Package/D.Group4(dat_ex3_txt_20210724-21_Spring_0658-2239)'

zip_paths = [(os.path.join(A_folder_path, file), os.path.getmtime(os.path.join(A_folder_path, file))) for file in os.listdir(A_folder_path) if file.endswith('.zip')]

# Modificate_Dateでソート (各zipファイルが指定フォルダに追加された順に識別番号を付与)
zip_paths_sorted = sorted(zip_paths, key=lambda x: x[1])

for i, (zip_patha, _) in enumerate(zip_paths_sorted):
    new_name = os.path.join(A_folder_path, str(i) + '.zip')
    os.rename(zip_path, new_name)
```
上のコードを実行すると、zipファイルの名前が識別番号のみ (001.zip等)に変わります。

次に、このzipファイルの名前を利用して、txt(tsv)ファイルも変更します。

改めて以下のコードを入力して下さい
```
import os

# 名前変更後のzipファイルが含まれているフォルダのパスを指定
# 利用者は、A_folder_pathの''内を適宜変更してください。
A_folder_path = '/home/miyasaka/M1_Research/F11.Code_Summary/01.RawData_Package/A.Group1(ex3_txt_20220620_Hokkaido_0209-0313)'

folder_paths = [os.path.join(A_folder_path, folder) for folder in os.listdir(A_folder_path) if os.path.isdir(os.path.join(A_folder_path, folder)) and folder.isdigit()]

for folder_path in folder_paths:
    for file in os.listdir(folder_path):
        if file.endswith('.txt'): #'.tsv'と変えても良い
            old_path = os.path.join(folder_path, file)
            new_path = os.path.join(folder_path, folder_path.split('/')[-1] + '_' + file)
            os.rename(old_path, new_path)
```
このコードにより、各フォルダ内の.txt, .tsvファイルの名前を変更できます。

具体的には、もとのファイル名の先頭にデータ識別番号が付け加わります。

-----------------------------------

## Part2-2 <9809フォーマットで、生データからX線のエネルギーと吸収係数を算出するコード>

9809フォーマットの場合は、以下のコードを実施し、**X線のエネルギー**と**吸収係数**を求めてください。

このコードにより、生データからXAFSスペクトルに必要な2列目(Energy)・4列目・5列目(μt)の値を抽出します。
```
import os
import numpy as np

#Before_folderには、抽出前のデータ(生データ)が含まれているフォルダのパスを記入してください。
#Middle_folderには、抽出後のデータが含まれているフォルダのパスを記入してください。
#つまり、2つのフォルダを作成しておく必要があります。

Before_folder = '/home/miyasaka/M1_Research/F11.Code_Summary/05.Raw_Data_for_Test/NIMS_Data(Photon_Factory)/GroupB_only_txt_Part1' #利用者が適宜変更
Middle_folder = '/home/miyasaka/M1_Research/F11.Code_Summary/05.Raw_Data_for_Test/NIMS_Data(Photon_Factory)/GroupB_only_txt_Part2' #利用者が適宜変更

file_list = [f for f in os.listdir(Before_folder) if f.endswith('.txt')]

for file_name in file_list:
    input_file_path = os.path.join(Before_folder, file_name)
    output_file_path = os.path.join(Middle_folder, file_name)
    
    with open(input_file_path, 'r') as f:
        lines = f.readlines()
    
    data = []
    for line in lines[2:]:
        values = line.split()
        if len(values) >= 5:
            data.append([float(values[1]), float(values[3]), float(values[4])])
    
    data = np.array(data)
    
    np.savetxt(output_file_path, data, fmt='%.6f')
```

---------------------------------------------------------------------------------------------------
次に、抽出されたデータをもとに、X線のエネルギーと吸収係数を求めます。

> [!NOTE]
> **分光結晶**や**測定法**によって、数値を変える必要があります。

```
import os
import numpy as np
import math

#Middle_folderには、抽出後のデータが含まれているフォルダのパスを記入してください。(上のC_folderと同じパス)
#After_folderには、#計算後のデータが含まれているフォルダ(いわゆる、従来の規格化前のデータ)のパスを記入してください。
#つまり、2つのフォルダを作成しておく必要があります。

Middle_folder = '/home/miyasaka/M1_Research/F11.Code_Summary/05.Raw_Data_for_Test/NIMS_Data(Photon_Factory)/GroupB_only_txt_Part2_111' #利用者が適宜変更
After_folder = '/home/miyasaka/M1_Research/F11.Code_Summary/05.Raw_Data_for_Test/NIMS_Data(Photon_Factory)/GroupB_only_txt_Part3' #利用者が適宜変更

file_list = [f for f in os.listdir(Middle_folder) if f.endswith('.txt')]

for file_name in file_list:
    input_file_path = os.path.join(Middle_folder, file_name)
    output_file_path = os.path.join(After_folder, file_name)
    
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
