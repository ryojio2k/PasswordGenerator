# Password Generator
パスワードを自動生成するスクリプト

# ファイル内訳


# 環境設定

(Windows準拠 別OSの場合は適宜読み替えてください)

## 仮想環境の作成と起動

  ルートディレクトリで下記を実施し仮想環境を作成し、仮想環境を起動してください。
  
  `python -m venv .venv`
  
  ### Windows
  `./.venv/Scripts/activate`

  ### Mac OS
  `source ./.venv/Scripts/activate`

  ### Linux
  `source ./.venv/bin/activate`
  
## モジュールのインストール
  下記を実施し必要なモジュールをインストールしてください。
  
  `pip install -U pip`
  
  `pip install pyinstaller`
  
  `pip install TkEasyGUI`

  VirtualBoxなどのLinux仮想環境の場合は以下を追加で実行ください。
  (tkinterがnot foundになる場合)

  `sudo apt-get install python3-tk`

# 実行

## コマンドラインでの実行
  コマンドラインから下記を実行すると、デフォルト状態でパスワードが生成されます。
  
  `python pwg.py`

# GUIアプリケーション

## 実行
  コマンドラインから下記を実行すると、開発環境上でGUIアプリが開きます。

  `python gui_pwg.py`

## 作成
  コマンドラインから下記を実行することでGUIのexeを作成することが可能です。
  
  `pyInstaller -wF ./gui_pwg.py`

## 設定ファイルについて
  初回起動時はデフォルトですが、一度実行完了すると下記ディレクトリに設定ファイルが生成されます。
  ./settings/settings_gui_pwg.json
  保存内容は「前回実行時の検索対象親ディレクトリ」です。
