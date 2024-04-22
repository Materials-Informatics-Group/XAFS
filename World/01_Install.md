## An easy way for anyone to perform XAFS analysis (oxide and valence determination)!

If you haven't set up the Larch environment, please check https://xraypy.github.io/xraylarch/installation.html

======================(Windowsの場合)======================
1.https://xraypy.github.io/xraylarch/installation.html#install-linを開く。

2.「1.1. Installing from a Binary installers」を見て、「Larch for Windows」をクリックし、Larch Binary Installersをダウンロードする。
　　その後、Larchを各自でインストールする。
   C:∕Users∕YourName∕AppData∕Local∕xraylarchにインストールされています。

　この時点で、あなたの端末にLarchのパッケージが自動的にインストールできています。

------------------------------------------------------------------------------
※うまくダウンロード・インストールできなかった場合は、次の操作を行ってください。
2-1. 「1.1.1. Windows Notes」の GetLarch.bat scriptをクリックし、ダウンロードする。
2-2. コマンドプロンプトを開き、以下のコマンドを入力する。
     cd C:\Users\<YOURNAME>\Downloads
     GetLarch
------------------------------------------------------------------------------

3.コマンドプロンプトを開き、conda activate と入力する。(base)と表示されたら正しい。

4.conda update -y conda python pip と入力する。処理が終わるまで待つ。(全てのパッケージが最新バージョンになります)

5.conda install -yc conda-forge xraylarchと入力する。

6.正しく環境構築されたか、larch -m で確認する。

7.pip install notebook と入力し、仮想環境とJupyter notebookの環境を同期させる。

8.from larch import Interpreter をJupyter Notebookに入力し、 正しくImportできるか確かめる。

======================(Macの場合)======================
1.https://xraypy.github.io/xraylarch/installation.html#install-linを開く。

2.「1.1. Installing from a Binary installers」を見て、「Larch for MacOSX」をクリックし、Larch Binary Installersをダウンロードする。
　　その後、Larchを各自でインストールする。

------------------------------------------------------------------------------------------------------------------------------------------------
※以下のエラーが発生した場合は、対処法がありますので、操作してください。
・MacOS 10.15（Catalina）の場合、Appleは署名されていないサードパーティパッケージを、デフォルトではインストールしません。
　→システム環境設定の「セキュリティとプライバシー」の「一般設定」で、このパッケージのインストールの許可をする(管理者パスワードの入力が必要)。

・インストール中に「自分のみにインストールする」をクリックする必要がある。
　→管理者パスワードの入力を求められたら、もう一度戻って「自分のみにインストール」を選択。

※うまくダウンロード・インストールできなかった場合は、次の操作を行ってください。
2-1. GetLarch.sh scriptをダウンロードする。
　　　ダウンロードできない場合は、GetLarch.sh script中のスクリプトをメモ帳にコピー&ペーストし、GetLarch.shという名前のファイル名をダウンロードフォルダ上に作成する。

2-2. ターミナルを開き、以下のコマンドを入力する。
　　　cd Downloads
　　　sh GetLarch.sh
------------------------------------------------------------------------------------------------------------------------------------------------

3.ターミナルを開き、conda activate と入力する。(base)と表示されたら正しい。

4.conda update -y conda python pip と入力する。処理が終わるまで待つ。(全てのパッケージが最新バージョンになります)

5.conda install -yc conda-forge xraylarchと入力する。

6.正しく環境構築されたか、larch -m で確認する。

7.pip install notebook と入力し、仮想環境とJupyter notebookの環境を同期させる。

8.from larch import Interpreter をJupyter Notebookに入力し、 正しくImportできるか確かめる。


======================(Linuxの場合)======================
1.https://xraypy.github.io/xraylarch/installation.html#install-linを開く。

2. GetLarch.sh scriptをダウンロードする。
   ダウンロードできない場合は、GetLarch.sh script中のスクリプトをメモ帳にコピー&ペーストし、GetLarch.shという名前のファイル名をダウンロードフォルダ上に作成する。

3. ターミナルを開き、以下のコマンドを入力する。
   cd Downloads
   sh GetLarch.sh

4.ターミナルを開き、conda activate と入力する。(base)と表示されたら正しい。

5.conda update -y conda python pip と入力する。処理が終わるまで待つ。(全てのパッケージが最新バージョンになります)

6.conda install -yc conda-forge xraylarchと入力する。

7.正しく環境構築されたか、larch -m で確認する。

8.pip install notebook と入力し、仮想環境とJupyter notebookの環境を同期させる。

9.from larch import Interpreter をJupyter Notebookに入力し、 正しくImportできるか確かめる。
