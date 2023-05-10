###次に、上に凸・下に凸である(極大値または極小値を持つ)ピークの数を調べる###
###ただし、隣り合うピークの差が0.04以上のもののみ###

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# ピークの検出
peaks, _ = find_peaks(y)

# 上に凸・下に凸のピークのみを抽出
convex_peaks = []
for i in range(1, len(peaks)-1):
    if (y[peaks[i]] > y[peaks[i-1]] and y[peaks[i]] > y[peaks[i+1]]) or (y[peaks[i]] < y[peaks[i-1]] and y[peaks[i]] < y[peaks[i+1]]):
        convex_peaks.append(peaks[i])

# 隣り合うピークのy座標の差が0.04以上となるピークのみを抽出
filtered_peaks = [convex_peaks[0]]  # 最初のピークを追加
for i in range(1, len(convex_peaks)):
    if abs(y[convex_peaks[i]] - y[convex_peaks[i-1]]) >= 0.04:
        filtered_peaks.append(convex_peaks[i])

## ピークの数と位置の表示
## ただし、μが0.5超のもの(つまり、吸収端よりも右側領域)のみとする

#ピークの位置(Energy)
peak_positions = [x[i] for i in filtered_peaks if y[i] > 0.5]

#ピークの位置(μt)
peak_positions_y = [y[i] for i in filtered_peaks if y[i] > 0.5]

#ピークの差異(Energy)(減少も含む)
differences = [peak_positions[i+1] - peak_positions[i] for i in range(len(peak_positions)-1)]

#ピークの差異(μt)(減少も含む)
differences_y = [peak_positions_y[i+1] - peak_positions_y[i] for i in range(len(peak_positions_y)-1)]

#ピークの幅(=ピークの差異(μt)が増加しているもののみを抽出 →if文の意味(1以上は吸収端ピークの可能性があるので除外))
filtered_differences = [differences[i] for i in range(len(differences)) if 0 < differences_y[i] < 1]

#ピークの高さ(=ピークの差異(μt)が増加しているもののみを抽出 →if文の意味(1以上は吸収端ピークの可能性があるので除外))
filtered_differences_y = [diff for diff in differences_y if 0 < diff < 1]

#ピークの傾き
small_peak_slope = [filtered_differences_y[i] / filtered_differences[i] for i in range(len(filtered_differences_y))]

#ピークの個数は、len(filtered_differences)と表せる。

print("小ピークの位置x:", peak_positions)
print("小ピークの位置y:", peak_positions_y)
print("小ピークの差異x:", differences)
print("小ピークの差異y:", differences_y)
print("小ピークの幅Δx:", filtered_differences)
print("小ピークの高さΔy:", filtered_differences_y)
print("小ピークの傾き", small_peak_slope)
print("小ピークの数:", len(filtered_differences_y))

# ピークの位置をグラフにプロット
plt.plot(x, y)
plt.plot(peak_positions, peak_positions_y, 'ro')
plt.show()