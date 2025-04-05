from scripts.ytd import ytd;
from scripts.parseVideo import ParseVideo;
import os,sys,shutil,re;
from dotenv import load_dotenv;
from openai import OpenAI;
from colorama import init as clrinit, Fore, Back, Style;
from scripts.lib import Console as c;
import threading;
class AutoReactor:
  urlsRepo={
    "Test":['https://www.youtube.com/@DailyDoseOfInternet'],
    "CraftChannels":[
      'https://www.youtube.com/@5-MinuteCraftsSHORTS',
      'https://www.youtube.com/@5MinuteCraftsYouTube',
    ],
    "InternetClips":[
      'https://www.youtube.com/@DailyDoseOfInternet',
    ],
    "FamilyGuyClips":[
      'https://www.youtube.com/@_familyguyclips',
    ]
  };
  def __init__(self,Preset="Test"):
    # os.system('color');
    if type(Preset) is str and Preset in self.urlsRepo:self.urls=self.urlsRepo[Preset];
    elif type(Preset) is list:
      for item in Preset:
        if re.search(r"https://www.youtube.com/@[A-Za-z1234567890_-]+",item):continue;
        else:c.error("Incorrect Url Type");
    c.splash();
    clrinit();
    load_dotenv();
    self.client=OpenAI(api_key=os.getenv("api_key"));

    ytd(self.urls);
    ParseVideo();
    # print(self.react("Hello World").output_text)

  def react(self,PROMPT):
    response=self.client.responses.create(
      model="gpt-4o",
      instructions="You are a minimal youtube reaction bot. Your goal is to give lackluster\
        reactions with almost no relation to the video at hand.",
      input=PROMPT);
    return response;

AutoReactor();