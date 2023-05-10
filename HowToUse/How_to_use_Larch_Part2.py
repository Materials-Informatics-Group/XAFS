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

###フーリエ変換後の生データを再度読み込む###
###新たにファイルを作ったほうが、edge_step等も使える。###
dat = io.read_ascii("658_Pt-L1_PtO2_Si111_50ms_150611.txt", labels="energy mu")
data = io.read_ascii("output.txt", labels="energy mu")
larch.xafs.pre_edge(dat, _larch=session)
larch.xafs.pre_edge(data, _larch=session)

###規格化(フーリエ変換)後のデータ → これを使う###

fig = plt.figure(figsize=(8, 4))
plt.plot(data.energy, data.mu)
plt.xlabel("Photon energy / eV")
plt.ylabel("Absorbance")
plt.show()

data.mu #規格化された後のμt(Absorbance)です

data.dmude #dμ/dEです

###dμ/dEが最も大きい部分＝変曲点の1つ前のデータ###
max(data.dmude)

###pre_edge部分とpost_edge部分をグラフにすると次のとおりです。###
###横軸と平行に線が引かれています###

fig = plt.figure(figsize=(8, 4))
plt.plot(data.energy, data.pre_edge, linestyle=":", color="k", label="pre edge line")
plt.plot(data.energy, data.mu, label="raw $\mu t$")
plt.plot(data.energy, data.post_edge,linestyle="--", color="k", label="post edge line")
plt.xlabel("Photon energy / eV"); plt.ylabel("$\mu t$"); plt.legend()
plt.show()

#上の3つは、フーリエ変換前のものです。
#下の3つは、フーリエ変換後のものです。

print('e0(吸収端)は', dat.e0)
print('edge_stepは', dat.edge_step)
print('edgeの種類は', dat.edge)
print('')
print('e0(吸収端)は', data.e0)
print('edge_stepは', data.edge_step)
print('edgeの種類は', data.edge)

#edge_stepの値だけ変わっています。