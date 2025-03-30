from scripts.ytd import ytd;
from scripts.parseVideo import ParseVideo;
import os,sys,shutil;
from dotenv import load_dotenv;
from openai import OpenAI;
from colorama import init as clrinit, Fore, Back, Style
from scripts.lib import Console as c;

class AutoReactor:
  def __init__(self):
    # os.system('color');
    clrinit();
    load_dotenv();
    self.client=OpenAI(api_key=os.getenv("api_key"));

    ytd();
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