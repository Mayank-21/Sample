'''
Created on Nov 9, 2018

@author: admin
'''
from bs4 import BeautifulSoup
import urllib2
import os
import re 
import sys
import time
#from CreateFolder import FolderCreate

def Replace_ExtraChar(MainString):
    MainString = MainString.replace("&nbsp;", "")
    MainString = MainString.replace("&amp;", "&")
    MainString = MainString.replace("&amp", "&")
    MainString = MainString.replace("&#39;", "'")
    MainString = MainString.replace("&quot;", '"')
    MainString = MainString.replace("&gt;", '>')
    return MainString


def Scrape_BetweenString(MainString,StartString,EndString):
    if StartString in str(MainString):
        OutputString = MainString.split(StartString, 1)[1]
        OutputString = OutputString.split(EndString, 1)[0]
        OutputString = re.sub("(\<.*?\>)", "",OutputString)
        OutputString = re.sub('[ \t]+' , ' ', OutputString)
        OutputString=OutputString.replace('\n',"")
        while OutputString.startswith(" "):
            OutputString = OutputString[1:]
        while OutputString.startswith(" "):
            OutputString = OutputString[:-1]
    return OutputString
