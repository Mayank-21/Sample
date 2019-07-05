import time
import datetime
import os
tstamp = time.strftime('%d_%m_%Y')
Current_Project_Path = os.path.dirname(os.path.abspath(__file__))
index1 = Current_Project_Path.rfind("\\")
#InternalDirectory = Current_Project_Path[0:index1]
#InternalDirectory = Current_Project_Path

def FolderCreate(Current_Project_Path):
    
    HTML_Path_Link = Current_Project_Path +'\\Htmls\\' + '\\HTML_Link\\'
    HTML_Path_DataField = Current_Project_Path +'\\Htmls\\' + '\\HTML_DataField\\'
    if not os.path.exists(HTML_Path_Link):
        os.makedirs(HTML_Path_Link)
    if not os.path.exists(HTML_Path_DataField):
        os.makedirs(HTML_Path_DataField)

