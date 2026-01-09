import os
import json
import TkEasyGUI as teg
import fec

# 設定ファイル
setting_json_file = "./settings/settings_gui_fec.json"

if not os.path.isdir("./settings"):
  os.makedirs("./settings")

setting_json_default = """
  {
    "targetpath": ""
  }
  """
setting_json = json.loads(setting_json_default)

if os.path.isfile(setting_json_file):
  with open(setting_json_file, "r", encoding="utf-8") as f:
    setting_json = json.load(f)

if not os.path.isdir(str(setting_json["targetpath"])):
  setting_json["targetpath"] = ""

# 入力フレーム
frame1 = teg.Frame('設定',
  [
    [
      teg.Text('検査対象ディレクトリ')
    ],
    [
      teg.InputText(key='-TARGETPATH-', size=(100, 1), default_text=str(setting_json["targetpath"])),
      teg.FolderBrowse(target_key='-TARGETPATH-')
    ],
    [
      teg.Submit(button_text='実行', key='button_execute')
    ]
  ]
)

# 出力フレーム
frame2 = teg.Frame('ログ出力',
  [
    [
      teg.Output(key='-OUTPUT-', size=(100, 20), autoscroll=True, disabled=True),
    ],
  ]
)

# レイアウト
layout = [
  [
    frame1
  ],
  [
    frame2
  ],
]

# Window生成
window = teg.Window('File Exists Checker', layout)

# GUI表示実行部分
while window.is_alive():
  # ウインドウ表示
  event, values = window.read()

  # クローズボタン
  if event is None:
    print('exit')
    break

  # ボタンが押された場合
  if event == 'button_execute':
    targetpath = str(values['-TARGETPATH-'])
    output = window['-OUTPUT-']

    setting_json["targetpath"] = targetpath
    with open(setting_json_file, "w", encoding="utf-8") as f:
      json.dump(setting_json, f, indent=2)

    str_finished = fec.check(targetpath, window, output)

    teg.popup_info(str_finished, "File Exists Checker")

window.close()
