import time
import datetime
import os
tstamp = time.strftime('%d_%m_%Y')
Current_Directory = os.path.dirname(os.path.abspath(__file__))
index1 = Current_Directory.rfind("\\")
HtmlDirectory = Current_Directory[0:index1]

def Create_Folder(HtmlDirectory,tstamp):
    
    HTML_Path_Link = HtmlDirectory +'\\Html\\' + '\\HTML_Link\\'
    HTML_Path_Data = HtmlDirectory +'\\Html\\' + '\\HTML_Data\\'
    HTML_Path_Image = HtmlDirectory  + '\\Images\\'
    HTML_Path = HtmlDirectory +'\\Html\\'   
    HTML_Path_Main = HtmlDirectory +'\\Html\\' + '\\Main\\'
    HTML_Path1 = HtmlDirectory +'\\Html\\'
    HTML_Path2 = HtmlDirectory +'\\Html\\' + '\\CSV\\'
    HTML_Path3 = HtmlDirectory +'\\Html\\' + '\\PermitNumber\\'
    Current_Directory = os.path.dirname(os.path.abspath(__file__))
    Log_Path = HtmlDirectory +'\\Log\\'
    
    
    if not os.path.exists(HTML_Path_Image):
        os.makedirs(HTML_Path_Image)
    # if not os.path.exists(HTML_Path2):
    #     os.makedirs(HTML_Path2)
    if not os.path.exists(HTML_Path_Link):
        os.makedirs(HTML_Path_Link)
    if not os.path.exists(HTML_Path_Data):
        os.makedirs(HTML_Path_Data)
    # if not os.path.exists(HTML_Path3):
    #     os.makedirs(HTML_Path3)
    if not os.path.exists(HTML_Path_Main):
        os.makedirs(HTML_Path_Main)
    # if not os.path.exists(Log_Path):
    #     os.makedirs(Log_Path)
        
def log(message):
    Log_Path = Current_Directory +'\\Log\\'
    currenttime = time.strftime('%Y-%m-%d %H:%M:%S')
    f = open(Log_Path+'\\log.log', "a")    
    f.seek(0, 0)
    f.write(currenttime + ":"+message+"\n")
    f.close()
    #===========================================================================
    # Log_Path = HtmlDirectory +'\\Log\\'
    # f = open(Log_Path+'\\log.log', "a")
    # f.write(message)
    # f.close
    #===========================================================================