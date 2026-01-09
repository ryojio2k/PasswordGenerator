import os
import sys
import datetime
import c_logger

def check(targetpath, window=None, output=None):
  """ディレクトリ下にあるファイルのリストを出力する

  Args:
      targetpath (string): 検索対象となる親ディレクトリのパス
      window (TkEasyGUI.window, optional): TkEasyGUIのWindowオブジェクト. Defaults to None.
      output (TkEasyGUI.window.Output, optional): TkEasyGUIのOutputオブジェクト. Defaults to None.

  Returns:
      string: 終了告知ダイアログに表示する文字列
  """

  # 出力ファイル名
  str_dt = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
  log_file_path = f"./log/log_gui_fec_{str_dt}.txt"
  logger = c_logger.logger()
  logger.start(log_file_path, window, output)

  logger.print(f"targetpath:{targetpath}")
  logger.print("-----")
    
  # フォルダ存在確認
  if not os.path.exists(targetpath):
    logger.print(f"targetpath {targetpath} is not Exists.")
    sys.exit()

  # 捜索
  count = 0
  for root, dirs, files in os.walk(targetpath):
    for file in files:
      logger.print(os.path.join(root, file))
      count += 1

  logger.print("-----")
  logger.print(f"file counts:{count}")
  str_done = "Done."
  logger.print(str_done)
  logger.end()
  return str_done


if __name__ == "__main__":
  if (len(sys.argv)) == 2:
    check(sys.argv[1])

  else:
    print("python3 fec.py [targetpath]")
    sys.exit()