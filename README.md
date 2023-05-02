# XAFS

https://xraypy.github.io/xraylarch/installation.html#install-lin
Larchとは、XAFS解析をpythonのコードで行う方法である。
デフォルトではlarchはインストールされていないため、
自分でインストールをする必要がある。

上記のサイトに、Larchのインストールの仕方(English.ver)が載っているため、
参考にしながら各操作を行う。

1. Linux上でターミナルを開く

2. pyenv install -l を入力し、利用できるversionの一覧を表示する。

3. pyenv install <version> で、希望するversionをインストールする。
    (今回は、3.9.7を使用)

4. pyenv versions でインストールされているversionを表示させる。
    *とあるものが、現在利用している環境(version)である。

5. https://xraypy.github.io/xraylarch/installation.html#install-lin
   このサイトの”GetLarch.sh”スクリプトを、Text Editorにコピー&ペーストする。
   Downloadsフォルダに作成し、ファイル名は”GetLarch.sh”とする。
　　※自動的にダウンロードできないため、注意が必要。

6. cd Downloads と入力する。(操作がDownloads上で行われる)

7. sh GetLarch.sh と入力し、処理を待つ。

以下、https://xraypy.github.io/xraylarch/installation.html#install-lin　　　　　　　　　　　　　　　　　　　　　　　　　　
の1.3 Installing into an existing Anaconda Python environmentに書いてある操作を行う。

8. conda activate と入力する。(base)と表示されたら正しい。

9. conda update -y conda python pip と入力する。処理が終わるまで待つ。

10. conda create -y –name xraylarch python=>3.9.10 と入力する。

11. conda activate xraylarchと入力する。
      (xraylarch)と表示されたら正しい。

12. conda install -y "numpy=>1.20" "scipy=>1.6" "matplotlib=>3.0" scikit-learn pandas
     と入力する。

13. conda install -y -c conda-forge wxpython pymatgen tomopy pycifrw と入力する。
     処理が終わるまでに少し時間がかかる場合もある。
      Errorが起こる場合もあるため、その場合は最初からやり直す。

14. pip install xraylarch と入力する。

15. larch -m で最終確認する。

16. pip install notebook と入力し、仮想環境とJupyter notebookの環境を同期させる。

17. from larch import Interpreter をJupyter Notebookに入力し、
     正しくImportできるか確かめる。

(17. でErrorが出た場合...)
python と入力した後に、from larch import Interpreterと入力する。
正しくImportされていたら、>>>と出力される。→pip install notebook を改めて入力。
Errorとなったら正しくインストールできていないため、最初からやり直す。

※やり直す場合は、xraylarchを削除してから各操作を行う。

############################################################
https://qiita.com/inashiro/items/f1c10440618cf73a2d81
は、Larchに関する日本語サイトです。
このサイトが書かれたときとは、Larchのバージョンが異なるので注意が必要です。

import larch_plugins as lp は、動きません。
(この部分だけ変更されているみたいです)

利用できるモジュールは以下のサイトのとおりです。
https://xraypy.github.io/xraylarch/python.html
