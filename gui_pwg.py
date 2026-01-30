import os
import json
import TkEasyGUI as teg # type: ignore
import pwg

charactor_type_keys = ["-CHARACTOR_TYPE_ALPHABETS-", "-CHARACTOR_TYPE_ALPHABETS_SIGNS-", "-CHARACTOR_TYPE_ALPHABETS_NUMBERS-", "-CHARACTOR_TYPE_ALPHABETS_NUMBERS_SIGNS-"]

# 使用する文字の種類をkeyからintに変換する
def get_charactor_type_int(values):
  for i in range(len(charactor_type_keys)):
    if values[charactor_type_keys[i]]:
      return i
  return 0

# 使用する文字の種類の選択状況を返却する
def get_charactor_type_key(values):
  for i in range(len(charactor_type_keys)):
    if values[charactor_type_keys[i]]:
      return charactor_type_keys[i]
  return charactor_type_keys[0]

# Outputの更新
def update_output(input_data: str | list[str]):
  # 文字列の場合は配列化する
  lines: list[str] = [input_data] if isinstance(input_data, str) else input_data
  output.update(disabled=False)
  output.update('')
  for line in lines:
    output.print(line)
  output.update(disabled=True)

# Outputウインドウのリサイズ
def set_output_size(window, x, y):
  w = x+1
  h = y+1
  window["-OUTPUT-"].widget.configure(width=w, height=h)

# ファイルの保存
def save_as_textfile(input_data: str | list[str]):
  lines: list[str] = [input_data] if isinstance(input_data, str) else input_data
  file_path = teg.popup_get_file(
    message="保存先を選択してください",
    save_as=True,
    file_types=(("Text Files", "*.txt"), ("All Files", "*.*")),
    default_extension=".txt"
  )
  
  if file_path:
    try:
      with open(file_path, "w", encoding="utf-8") as f:
        for line in lines:
          print(line, file=f)
      teg.popup(f"保存しました\n{file_path}")
    except Exception as e:
      teg.popup(f"エラー\n{e}")

# UI初期化
def feedback_ui(window, setting_json):
  window["-DIGIT-"].update(setting_json["digit"])
  window["-NUM-"].update(setting_json["num"])
  window["-SIGNS-"].update(setting_json["signs"])
  window["-FIRST_CHARACTOR_ALPHABETS-"].update(setting_json["first_charactor_alphabets"])
  last_selected_charactor_types = setting_json["charactor_type"]
  window[last_selected_charactor_types].select()
  update_output('')
  set_output_size(window, setting_json["digit"], setting_json["num"])

# 設定ファイル
setting_json_file = "./settings/settings_gui_pwg.json"

if not os.path.isdir("./settings"):
  os.makedirs("./settings")

setting_json_default = """
  {
    "digit": 8,
    "num": 10,
    "charactor_type": "-CHARACTOR_TYPE_ALPHABETS-",
    "signs": "/*-+.,!#$%&()~|_",
    "first_charactor_alphabets": "False"
  }
  """
setting_json = json.loads(setting_json_default)

if os.path.isfile(setting_json_file):
  with open(setting_json_file, "r", encoding="utf-8") as f:
    setting_json = json.load(f)

last_selected_charactor_types = setting_json["charactor_type"]

# 入力フレーム
frame1 = teg.Frame('設定',
  [
    [
      teg.Text('桁数'),
      teg.InputText(key='-DIGIT-', size=(2, 1), default_text=int(setting_json["digit"])),
    ],
    [
      teg.Text('生成するパスワードの数'),
      teg.InputText(key='-NUM-', size=(2, 1), default_text=int(setting_json["num"])),
    ],
    [
      teg.Text('使用する記号'),
      teg.InputText(key='-SIGNS-', size=(20, 1), default_text=str(setting_json["signs"]))
    ],
    [ teg.Checkbox("先頭を必ず英字とする", key="-FIRST_CHARACTOR_ALPHABETS-", enable_events=False, default=bool(setting_json["first_charactor_alphabets"]) ) ]
  ]
)

frame2 = teg.Frame('使用する文字の種類',
  [
    [ teg.Radio("英字のみ", group_id="charactor_type", key="-CHARACTOR_TYPE_ALPHABETS-", enable_events=False, default=(last_selected_charactor_types == "-CHARACTOR_TYPE_ALPHABETS-") ) ],
    [ teg.Radio("英字+記号", group_id="charactor_type", key="-CHARACTOR_TYPE_ALPHABETS_SIGNS-", enable_events=False, default=(last_selected_charactor_types == "-CHARACTOR_TYPE_ALPHABETS_SIGNS-" ) ) ],
    [ teg.Radio("英字+数字", group_id="charactor_type", key="-CHARACTOR_TYPE_ALPHABETS_NUMBERS-", enable_events=False, default=(last_selected_charactor_types == "-CHARACTOR_TYPE_ALPHABETS_NUMBERS-" ) ) ],
    [ teg.Radio("英字+数字+記号", group_id="charactor_type", key="-CHARACTOR_TYPE_ALPHABETS_NUMBERS_SIGNS-", enable_events=False, default=(last_selected_charactor_types == "-CHARACTOR_TYPE_ALPHABETS_NUMBERS_SIGNS-" ) ) ]
  ]
)

frame_submit = teg.Frame('',
  [
    [
      teg.Submit(button_text='実行', key='button_execute')
    ],
  ]
)

frame_save = teg.Frame('',
  [
    [
      teg.Submit(button_text='保存', key='button_save')
    ]
  ]
)

frame_initialize = teg.Frame('',
  [
    [
      teg.Submit(button_text='初期設定に戻す', key='button_initialize')
    ],
  ]
)

# 出力フレーム
frame_log = teg.Frame('ログ出力',
  [
    [
      teg.Output(key='-OUTPUT-', size=(setting_json["digit"]+1, setting_json["num"]+1), autoscroll=True, disabled=True),
    ],
  ]
)

# レイアウト
layout = [
  [ frame1, frame2 ],
  [ frame_submit, frame_save, frame_initialize ],
  [ frame_log ]
]

# Window生成
window = teg.Window('Password Generator', layout)

passwords: list[str] = []

# GUI表示実行部分
while window.is_alive():
  # ウインドウ表示
  event, values = window.read()

  # クローズボタン
  if event is None:
    print('exit')
    break

  # 実行ボタン押下時
  if event == 'button_execute':
    # 各入力値を変数に格納
    digit = int(values['-DIGIT-'])
    num = int(values["-NUM-"])
    signs = values["-SIGNS-"]
    first_charactor_alphabets = bool(values["-FIRST_CHARACTOR_ALPHABETS-"])
    charactor_type = get_charactor_type_int(values)
    output = window['-OUTPUT-']
    set_output_size(window, digit, num)

    # 設定jsonに反映
    setting_json["digit"] = digit
    setting_json["num"] = num
    setting_json["signs"] = signs
    setting_json["first_charactor_alphabets"] = first_charactor_alphabets
    setting_json["charactor_type"] = get_charactor_type_key(values)

    # setting.json更新
    with open(setting_json_file, "w", encoding="utf-8") as f:
      json.dump(setting_json, f, indent=2)

    # パスワード列生成
    passwords = pwg.pwg(digit,num,charactor_type,signs,first_charactor_alphabets)
    # 出力
    update_output(passwords)
  
  # 保存ボタン押下時
  if event == 'button_save':
    if len(passwords) <= 0:
      teg.popup('パスワードを生成してください')
    else:
      save_as_textfile(passwords)

  # 初期状態に戻すボタン押下時
  if event == 'button_initialize':
    passwords = []
    # デフォルト設定を読み込む
    setting_json = json.loads(setting_json_default)
    # 表示反映
    feedback_ui(window, setting_json)

window.close()
