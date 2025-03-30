import shutil,os,sys;
from pathlib import Path;
from colorama import Fore, Back, Style;
from scripts.lib import Console as c;
class ParseVideo:
  content=Path("./content/").glob('**/*.mp4')
  def __init__(self):
    c.header("Start Video Parse");
    for path in self.content:
      print(f"{Style.BRIGHT}{Back.WHITE}{Fore.BLACK}Got video:{Style.RESET_ALL} {Fore.CYAN}{str(path)}{Style.RESET_ALL}");
