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
from CreateFolder import FolderCreate

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


def Scrape_BetweenStringWithReplace(Input):

    Input = Input.replace('\r', '')
    Input = Input.replace('\n', '')
    Input = re.sub("(\<.*?\>)", "", Input.strip())
    Input = re.sub('[ \t]+', ' ', Input.strip())
    replace_input = [" |", "| ", "||", " ,", ", ", ",,", '&nbsp;', ': ', ' :', ',|', '::', ':|', ',--,', ' ;', '; ', ',;,', ';|']
    replace_output = ["|", "|", "|", ",", ",", ",", '', ':', ':', '--', ';', ';', ';', '|']
    length_replace = len(replace_input)
    for i in range(0, length_replace):
        while replace_input[i] in Input:
            Input = Input.replace(replace_input[i], replace_output[i])
    check_char = [' ', ',', ';', '|', ':']
    for i in range(0, len(check_char)):
        while Input.startswith(check_char[i]):
            Input = Input[1:]
        while Input.endswith(check_char[i]):
            Input = Input[:-1]

    return Input
