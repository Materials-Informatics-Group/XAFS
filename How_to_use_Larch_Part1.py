####ここでは、生データをフーリエ変換して、変換後のデータファイルを作ります。
####Larchのモジュールについても簡単に紹介しています。

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

#txtファイルの場合、labelがないため、第1列をenergy, 第2列(μt)をmuとする
dat = io.read_ascii("658_Pt-L1_PtO2_Si111_50ms_150611.txt", labels="energy mu")

###ただの測定結果です###
###フーリエ変換前のデータです###

fig = plt.figure(figsize=(8, 4))
plt.plot(dat.energy, dat.mu)
#plt.plot(dat.e0, dat.mu[dat.energy == dat.e0], 'o', color='r')
plt.xlabel("Photon energy / eV")
plt.ylabel("Absorbance")
plt.show()

###以下のコードで、バッググラウンド除去や規格化を自動的に行える###
larch.xafs.pre_edge(dat, _larch=session)

######pre_edgeモジュールでできること#################################

#e0 → 吸収端(μtの一次微分の最初のピーク)

#edge_step → Δμ(吸収端のジャンプの値) 規格化前のものなので使わない

#dmude → dμ/dE (array)

#norm → normalized mu(E) (array) μtを規格化した値

#flat → flattened, normalized mu(E) (array)
#吸収端より高エネルギー側について，規格化されたスペクトルからプレエッジの線とポストエッジの線の差分を差し引いた値
#normを使うか、flatを使うかはどちらでも良い。
#しかし、Athenaはflatを推奨している

#edge → ○○吸収端 (○には、L1や Kなど)

#pre_edge → pre-edge curve (array) 吸収端前の領域

#post_edge → post-edge curve (array) 吸収端後の領域

################################################################

###バックグランド除去・規格化後でないと実行できません###
##次のコードは、post_edgeとpre_edgeが現れます

fig = plt.figure(figsize=(8, 4))
plt.plot(dat.energy, dat.pre_edge, linestyle=":", color="k", label="pre edge line")
plt.plot(dat.energy, dat.mu, label="raw $\mu t$")
plt.plot(dat.e0, dat.mu[dat.energy == dat.e0], 'o', color='r')
plt.plot(dat.energy, dat.post_edge,linestyle="--", color="k", label="post edge line")
plt.xlabel("Photon energy / eV"); plt.ylabel("$\mu t$"); plt.legend()
plt.show()

##各データの値です

print('e0(吸収端)は', dat.e0)
print('edge_stepは', dat.edge_step)
print('edgeの種類は', dat.edge)

print('dμ/dEは')
print(dat.dmude)

print('規格化μtは')
print(dat.norm)

print('規格化・畳み込みμtは')
print(dat.flat)

print('吸収端前の規格化前μtは')
print(dat.pre_edge)

print('吸収端後の規格化前μtは')
print(dat.post_edge)

###energyとflatのデータ数が同じかどうか確かめる###

print(len(dat.energy))
print(len(dat.flat))

####energyと規格後flatデータを新たに作る###

combined_list = list(zip(dat.energy, dat.flat))

# テキストファイルにデータを書き込む
with open('output.txt', 'w') as file:
    for item in combined_list:
        file.write(f'{item[0]}\t{item[1]}\n')

#############################################################
#生データは、(energy, フーリエ変換前μt)でしたが、
#output.txtは、(energy, フーリエ変換後μt)となっています。