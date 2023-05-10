###この章では、吸収端の大きなピークを取り扱う(小さいピークはDetail_Detect_SmallPeak.ipynb)###
###小さなピークの検出方法とは異なるので注意が必要です###

from larch import Interpreter
session = Interpreter()
import larch
from larch import io
from larch import xafs
from larch.io import read_ascii
from larch.xafs import pre_edge
from larch.xafs import mback

import matplotlib.pyplot as plt
import numpy as np

data = io.read_ascii("output.txt", labels="energy mu")
larch.xafs.pre_edge(data, _larch=session)


# データ点の座標を表すndarray
x = data.energy
y = data.mu

# 変曲点の座標を表すndarray
e0 = np.array([data.e0, np.interp(data.e0, x, y)])

# e0から最も近い極大値・極小値の座標を求める
distances = np.sqrt((x - e0[0]) ** 2 + (y - e0[1]) ** 2)
maxima = (y[1:-1] > y[:-2]) & (y[1:-1] > y[2:])
minima = (y[1:-1] < y[:-2]) & (y[1:-1] < y[2:])
extrema = np.where(maxima | minima)[0] + 1
nearest_extrema = extrema[np.argsort(distances[extrema])[:2]]
nearest_extrema_coords = np.array([[x[i], y[i]] for i in nearest_extrema])

#この時点では、nearest_extrema_coordsのうち、どちらが極小値・極大値かはわからない
#nearest_extrema_coordsは変曲点からの距離の近さによって変動する

#まずは空リストを作る。
max_peak_energy=[]
min_peak_energy=[]
max_peak_mu=[]
min_peak_mu=[]
peak_width=[]
peak_height=[]
peak_slope=[]

if nearest_extrema_coords[0, 0] > nearest_extrema_coords[1, 0]:
    nearest_extrema_coords1 = np.array([[nearest_extrema_coords[0], nearest_extrema_coords[0]]])
    nearest_extrema_coords2 = np.array([[nearest_extrema_coords[1], nearest_extrema_coords[1]]])                                    
    for coord in nearest_extrema_coords1:
        max_peak_energy.append(coord[0, 0])
        max_peak_mu.append([coord[0, 1]])
    for coord in nearest_extrema_coords2:
        min_peak_energy.append(coord[1, 0])
        min_peak_mu.append([coord[1, 1]])
        
else:
    nearest_extrema_coords1 = np.array([[nearest_extrema_coords[0], nearest_extrema_coords[0]]])
    nearest_extrema_coords2 = np.array([[nearest_extrema_coords[1], nearest_extrema_coords[1]]])                                    
    for coord in nearest_extrema_coords1:
        min_peak_energy.append(coord[0, 0])
        min_peak_mu.append([coord[0, 1]])
    for coord in nearest_extrema_coords2:
        max_peak_energy.append(coord[1, 0])
        max_peak_mu.append([coord[1, 1]])

#ピークの幅・高さ・傾きを求める
#なお、それぞれ負の値になった場合は、絶対値で正の値に戻すようにする

peak_width1 = nearest_extrema_coords[0, 0] - nearest_extrema_coords[1, 0]
peak_height1 = nearest_extrema_coords[0, 1] - nearest_extrema_coords[1, 1]
peak_slope1 = peak_height1 / peak_width1

if peak_width1 < 0:
    peak_width1 = abs(peak_width1)
    
if peak_height1 < 0:
    peak_height1 = abs(peak_height1)
    
if peak_slope1 < 0:
    peak_slope1 = abs(peak_slope1)

peak_width.append(peak_width1)
peak_height.append(peak_height1)
peak_slope.append(peak_slope1)