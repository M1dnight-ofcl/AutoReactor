import shutil,os,sys,json,wave;
from pathlib import Path;
from colorama import Fore, Back, Style;
from scripts.lib import Console as c;
import moviepy as mp;
from vosk import Model, KaldiRecognizer, SetLogLevel;
# import speech_recognition as sr
class ParseVideo:
  content=Path("./content/").glob('**/*.mp4')
  def __init__(self):
    c.header("Start Video Parse");
    for path in self.content:
      #?print (literally does nothing else)
      nstr=f'{str(path).replace(".mp4","")[:os.get_terminal_size().columns-30]}';
      if not nstr==str(path).replace(".mp4",""):nstr=f"{nstr}...mp4";
      else:nstr=f"{nstr}.mp4"
      print(f"{Style.BRIGHT}{Back.WHITE}{Fore.BLACK}Got video:{Style.RESET_ALL} {Fore.CYAN}{nstr}{Style.RESET_ALL}");
      self.parseVideo(path);

  def parseVideo(self,path): 
    video=mp.VideoFileClip(path);
    if os.path.isdir("./extracted/"):
      if not('--skip-extracted-audio-folder-reset' in sys.argv or '-s3-noreset' in sys.argv):
        try:shutil.rmtree("./extracted/");
        except Exception as e:print(f"Ran into error when reseting extracted audio folder: {str(e)}");
        os.mkdir("extracted");
    else:os.mkdir("extracted");
    video.audio.write_audiofile(f"extracted/{Path(path).stem}.wav",ffmpeg_params=["-ac", "1"]);
    model=Model(lang="en-us");
    with wave.open(f"extracted/{Path(path).stem}.wav","rb") as wf:
      if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print("Audio file must be WAV format mono PCM.")
        sys.exit(1)
      rec=KaldiRecognizer(model,wf.getframerate());
      rec.SetMaxAlternatives(10);
      rec.SetWords(True);
      results=[];
      while True:
        data=wf.readframes(4000);
        if len(data)==0:break;
        if rec.AcceptWaveform(data):
          results.append(rec.Result())
      results.append(rec.FinalResult())
      with open(f"extracted/{Path(path).stem}.json","w") as f:
        print(results);
        json.dump(results,f,indent=2);#barely works goddammit
        # json.dump(json.loads(rec.FinalResult()),f,indent=2);

