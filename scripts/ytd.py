import xlsxwriter,os,time,sys,json,shutil;
from pathlib import Path;
from pytubefix import YouTube;
from pytubefix.cli import on_progress;
from selenium import webdriver;
from selenium.webdriver.chrome.service import Service;
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup;
from colorama import Fore, Back, Style;
from scripts.lib import Console as c;
class ytd:
  SAVE_PATH="./content/";
  row=0;
  shortsurls=[];
  # dexe=Path(f"{os.getcwd()}\\resources\\chromedriver.exe");
  def __init__(self,urls):
    self.urls=urls;
    self.main();
  
  def setupDriver(self):
    options=Options();
    options.add_argument('--disable-gpu');
    options.add_argument('--disable-dev-shm-usage');
    options.add_argument('--no-sandbox');
    options.add_argument('--disable-web-security');
    options.add_argument('--allow-running-insecure-content');
    options.add_argument('--disable-webrtc');
    service=Service(executable_path="./resources/chromedriver.exe"); 
    try:
      return webdriver.Chrome(service=service, options=options);
    except Exception as e:
      print(f"Error setting up ChromeDriver: {str(e)}");
      return None;

  def getVideos(self):
    for url in self.urls: 
      times=0;
      self.driver.get('{}/shorts?view=0&sort=p&flow=grid'.format(url)) 
      while times<1:
        time.sleep(1);
        self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);");
        times+=1;
      content=self.driver.page_source.encode('utf-8').strip();
      soup=BeautifulSoup(content,"lxml");
      # print(soup);
    shortsurlhtags=soup.findAll(
      'a',class_='shortsLockupViewModelHostEndpoint reel-item-endpoint');
    
    for i in shortsurlhtags: 
      self.shortsurls.append(f"https://youtube.com/{str(i['href']).replace('shorts','video')}");
    return self.shortsurls;

  def downloadVideo(self,link):
    try: 
      yt=YouTube(link,on_progress_callback=on_progress);
      ys=yt.streams.get_highest_resolution()
      try:
        ys.download(output_path=self.SAVE_PATH);
        print('Video downloaded successfully!');
      except Exception as e: 
        print(f"Failed to download video: {str(e)}")
    except Exception as e:print(f"Download Failed: {str(e)}");

  def main(self):
    try:
      if not('--skip-get-videos' in sys.argv or '-s1' in sys.argv):
        self.driver=self.setupDriver();
        if self.driver:
          #?get videos
          self.getVideos();
          # print(self.shortsurls,len(self.shortsurls));
          c.header("Got Videos");
          for v in self.shortsurls:print(f" {Fore.CYAN} {v} {Style.RESET_ALL}");
          print(f"total length: {len(self.shortsurls)}");
          with open("videolist.json","w") as final:
            json.dump(self.shortsurls,final,indent=2);
          self.driver.quit();
      else:
        self.shortsurls=json.loads(open("videolist.json","r").read());

      if not('--skip-download-videos' in sys.argv or '-s2' in sys.argv):
        #?download videos
        if os.path.isdir("./content/"):
          if not('--skip-content-folder-reset' in sys.argv or '-s2-noreset' in sys.argv):
            try:shutil.rmtree("./content/");
            except Exception as e:print(f"Ran into error when reseting content folder: {str(e)}");
            os.mkdir("content");
        else:os.mkdir("content");
        c.header("Starting Video Download");
        i=0;
        for url in self.shortsurls:
          if '--download-limit' in sys.argv and int(sys.argv[sys.argv.index('--download-limit')+1]):
            if i>=int(sys.argv[sys.argv.index('--download-limit')+1]):break;
          self.downloadVideo(url);
          i+=1;

    except Exception as e:
      print(f"Error during execution: {str(e)}");
    finally:
      pass;



