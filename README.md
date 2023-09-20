# 自身のPCにLarchをインストールする方法！

https://xraypy.github.io/xraylarch/installation.html#install-lin をご覧ください。

なお、2023年9月現在、Larchの最新バージョンは**0.9.71**となります。

また、Pythonの実行環境である**Anaconda**は、事前にインストールしてください。

## Windowsの場合

1.https://xraypy.github.io/xraylarch/installation.html#install-lin を開く。

2.「1.1. Installing from a Binary installers」を見て、「Larch for Windows」をクリックし、Larch Binary Installersをダウンロードする。その後、Larchを各自でインストールする。
   C:∕Users∕YourName∕AppData∕Local∕xraylarchにインストールされています。

　この時点で、あなたの端末にLarchのパッケージが自動的にインストールできています。

------------------------------------------------------------------------------
> [!NOTE]
> うまくダウンロード・インストールできなかった場合は、次の操作を行ってください。

2-1. 「1.1.1. Windows Notes」の GetLarch.bat scriptをクリックし、ダウンロードする。

2-2. コマンドプロンプトを開き、以下のコマンドを入力する。
```     
cd C:\Users\<YOURNAME>\Downloads
GetLarch
```    
------------------------------------------------------------------------------

3.コマンドプロンプトを開き、conda activate と入力する。(base)と表示されたら正しい。

4.conda update -y conda python pip と入力する。処理が終わるまで待つ。(全てのパッケージが最新バージョンになります)

5.conda install -yc conda-forge xraylarchと入力する。

6.正しく環境構築されたか、larch -m で確認する。

7.pip install notebook と入力し、仮想環境とJupyter notebookの環境を同期させる。

8.from larch import Interpreter をJupyter Notebookに入力し、 正しくImportできるか確かめる。

以下、コマンド集です。
```
conda activate
conda update -y conda python pip
conda install -yc conda-forge xraylarch
larch -m
pip install notebook
from larch import Interpreter
```

## Macの場合
1.https://xraypy.github.io/xraylarch/installation.html#install-lin を開く。

2.「1.1. Installing from a Binary installers」を見て、「Larch for MacOSX」をクリックし、Larch Binary Installersをダウンロードする。
　　その後、Larchを各自でインストールする。

------------------------------------------------------------------------------------------------------------------------------------------------
> [!NOTE]
以下のエラーが発生した場合は、対処法がありますので、次のように操作してください。

・MacOS 10.15（Catalina）の場合、Appleは署名されていないサードパーティパッケージを、デフォルトではインストールしません。

→システム環境設定の「セキュリティとプライバシー」の「一般設定」で、このパッケージのインストールの許可をする(管理者パスワードの入力が必要)。

・インストール中に「自分のみにインストールする」をクリックする必要がある。
　
→管理者パスワードの入力を求められたら、もう一度戻って「自分のみにインストール」を選択。

> [!NOTE]
> うまくダウンロード・インストールできなかった場合は、次の操作を行ってください。

2-1. GetLarch.sh scriptをダウンロードする。
　　　
     ダウンロードできない場合は、GetLarch.sh script中のスクリプトをメモ帳にコピー&ペーストし、GetLarch.shという名前のファイル名をダウンロードフォルダ上に作成する。

2-2. ターミナルを開き、以下のコマンドを入力する。
```
cd Downloads
sh GetLarch.sh
```   
------------------------------------------------------------------------------------------------------------------------------------------------

3.ターミナルを開き、conda activate と入力する。(base)と表示されたら正しい。

4.conda update -y conda python pip と入力する。処理が終わるまで待つ。(全てのパッケージが最新バージョンになります)

5.conda install -yc conda-forge xraylarchと入力する。

6.正しく環境構築されたか、larch -m で確認する。

7.pip install notebook と入力し、仮想環境とJupyter notebookの環境を同期させる。

8.from larch import Interpreter をJupyter Notebookに入力し、 正しくImportできるか確かめる。

以下、コマンド集です。
```
conda activate
conda update -y conda python pip
conda install -yc conda-forge xraylarch
larch -m
pip install notebook
from larch import Interpreter
```

## Linuxの場合
1.https://xraypy.github.io/xraylarch/installation.html#install-lin を開く。

2.GetLarch.sh scriptをダウンロードする。
  
  ダウンロードできない場合は、GetLarch.sh script中のスクリプトをメモ帳にコピー&ペーストし、GetLarch.shという名前のファイル名をダウンロードフォルダ上に作成する。

3.ターミナルを開き、以下のコマンドを入力する。
``` 
cd Downloads
sh GetLarch.sh
``` 
4.ターミナルを開き、conda activate と入力する。(base)と表示されたら正しい。

5.conda update -y conda python pip と入力する。処理が終わるまで待つ。(全てのパッケージが最新バージョンになります)

6.conda install -yc conda-forge xraylarchと入力する。

7.正しく環境構築されたか、larch -m で確認する。

8.pip install notebook と入力し、仮想環境とJupyter notebookの環境を同期させる。

9.from larch import Interpreter をJupyter Notebookに入力し、 正しくImportできるか確かめる。

以下、コマンド集です。
```
conda activate
conda update -y conda python pip
conda install -yc conda-forge xraylarch
larch -m
pip install notebook
from larch import Interpreter
```

## conda install -yc conda-forge xraylarchがうまく行かない場合 (全てのOSに共通)

以下のコマンドを1行ずつ打つ。

ただし、4行目の epicsapps はインストールできない場合があるので、その場合は除外しても良い。
```
conda create -y --name xraylarch python=>3.10
conda activate xraylarch
conda install -y -c conda-forge wxpython pymatgen scipy h5py matplotlib
conda install -y -c conda-forge openbabel tomopy epicsapps
pip install xraylarch
```
