import os

class logger:
  """共通ロガークラス

    標準出力、ログファイルの他に、GUI(TkEasyGUI, PySimpleGUI)が存在する場合はそちらにも逐次出力する
  """
  def __init__(self):
      self.filepath = ""
      self.window = None
      self.output_gui = None
      self.log_file = None

  def start(self, _filepath=None, _window=None, _output_gui=None):
    self.filepath = _filepath
    self.window = _window
    self.output_gui = _output_gui
    if self.filepath is not None:
      dirname = os.path.dirname(self.filepath)
      if not os.path.isdir(dirname):
        os.makedirs(dirname)
      self.log_file = open(self.filepath, "w", encoding="utf-8")
    if self.output_gui is not None:
      self.output_gui.update(disabled=False)
      self.output_gui.update("")
      self.output_gui.update(disabled=True)
    if self.window is not None:
      self.window.refresh()

  def print(self, str):
    print(str)
    if self.log_file is not None:
      print(str, file=self.log_file)
    if self.output_gui is not None:
      self.output_gui.update(disabled=False)
      self.output_gui.print(str)
      self.output_gui.update(disabled=True)
    if self.window is not None:
      self.window.refresh()

  def end(self):
    if self.log_file is not None:
      self.log_file.close()
      self.log_file = None