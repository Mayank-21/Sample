'''
Created on Jan 9, 2018

@author: admin
'''
#!/usr/bin/env python
# encoding: utf-8

from bs4 import BeautifulSoup
import urllib2
import os
import re 
import sys
import time
from Createfolder import log
from HTMLParser import HTMLParser
h = HTMLParser()
#from Get_Request import GET_header


def Get_ReplaceData(value):

	h = HTMLParser()
	value = re.sub("(\<.*?\>)", "", value.strip())
	value = re.sub('[ \t]+', ' ', value.strip())
	value = value.replace("&#39;", "'")
	value = value.replace("&#39", "'")
	value = value.replace("&#034;", '"')
	value = value.replace("&amp;", "&")
	value = value.replace("&quot;", "\"")
	value = value.replace("&gt;", ">")
	value = value.replace("&lt;", "<")
	value = value.replace('&nbsp;&nbsp;', '')
	value = value.replace('&nbsp;', '')
	value = value.replace("&#39;", "'")
	value = value.replace('&amp;', '&')
	value = value.replace('&#160;', '')
	value = value.replace('\n', '')
	value = value.replace('\r', '')
	value = value.replace('\xc2', '')
	value = value.replace("\xa0", "")
	value = value.replace("\xc3", "")
	value = value.replace("\x82", "")


	if value == "'":
		value = ''
	if value == ".":
		value = ''
	if value == '\\':
		value = ''
	if value == "`":
		value = ''


	value = h.unescape(value)

	# print value

	return value
def Replace_Junk(strhtml):
    strhtml = strhtml.replace("&nbsp;", "")
    strhtml = strhtml.replace("&amp;", "&")
    strhtml = strhtml.replace("&amp;", "&")
    strhtml = strhtml.replace("&#39;", "'") #&#039;
    strhtml = strhtml.replace("&#039;", "'")
    strhtml = strhtml.replace("&quot;", '"')
    strhtml = strhtml.replace("&gt;", '>')
    # strhtml = strhtml.replace('&gt;', '>')
    return strhtml
def Strip_Tag(value):
    value_temp = ''
    h = HTMLParser()
    value = re.sub("(\<.*?\>)", "", value)
    value = re.sub('[ \t]+', ' ', value)
    value = value.replace(',,', ',')
    if ', ' in value:
        value = value.replace(', ', ',')
    if ',' in value:
        value = value.replace(',', ', ')
    k = 0
    while k < 5:
        k = k + 1
        replace_char = ['\n', '\r', ',,','  ']
        replay_char = ['', '', ',',' ']
        length_replace = len(replace_char)
        for i in range(0, length_replace):
            while replace_char[i] in value:
                value = value.replace(replace_char[i], replay_char[i])

        slice_char = [' ', ',', ';', ':']
        length_slice = len(slice_char)
        for i in range(0, length_slice):
            while value.startswith(slice_char[i]):
                value = value[1:]
            while value.endswith(slice_char[i]):
                value = value[:-1]

    try:
        value = value.strip()
        if value != '':
            value_temp = h.unescape(value)
        if value_temp != '':
            value = value_temp
    except Exception as e:
        log(str(e))
    # if value == '.' or value == '\\' or value == '* *' or value == '- -' or value == '*':
    #     value = ''
    return value

    value = re.sub("(\<.*?\>)", "", value)
    value = re.sub('[ \t]+', ' ', value)
    value = value.replace('\n', "")
    value = value.replace('\r', "")
    while value.startswith(" "):
        value = value[1:]
    while value.endswith(" "):
        value = value[:-1]
    value = value.strip()

    return value
def GET_tag(strhtml,starttag,endtag):
    if starttag in str(strhtml):
        value = strhtml.split(starttag, 1)[1]
        value = value.split(endtag, 1)[0]        
    while value.startswith(" "): 
        value = value[1:]
    while value.startswith(" "): 
        value = value[:-1]
            
    return value

def GET_data(strhtml,starttag,endtag):
    if starttag in str(strhtml):
        value = strhtml.split(starttag, 1)[1]
        value = value.split(endtag, 1)[0]
        value=value.replace('"',"")
        value=value.replace("<td width=17% nowrap=nowrap>","")
        value=value.replace("</td>","")
        value=value.replace("\r","")
        value=value.replace("\t","")
        value=value.replace("<span class=color-1>","")
        value=value.replace('<td>',"")
        value=value.replace('&nbsp;',"")
        value=value.replace('\n',"")
    while value.startswith(" "): 
        value = value[1:]
    while value.startswith(" "): 
        value = value[:-1]
            
    return value
def GET_ReData1(strhtml,starttag,endtag,endtag1):
    if starttag in str(strhtml):
        value = strhtml.split(starttag, 1)[1]
        value = value.split(endtag, 1)[0]
        value = value.split(endtag1, 1)[1]
        value=value.replace('"',"") 
        value=value.replace('\n',"")       
        #print value
        while value.startswith(" "): 
            value = value[1:]
        while value.startswith(" "): 
            value = value[:-1] 
    return value
def Get_ReData2(strhtml,starttag,endtag):
    if starttag in str(strhtml):
        value = strhtml.split(starttag, 1)[1]
        value = value.split(endtag)[1]
        value = re.sub("(\<.*?\>)", "",value)
        value = value.strip()
        value=value.replace('"',"")
        value = re.sub('[ \t]+' , ' ', value)
        value=value.replace('\n',"")
        while value.startswith(" "): 
            value = value[1:]
        while value.startswith(" "): 
            value = value[:-1]      
    return value   
def Get_ReData(strhtml,starttag,endtag):
    if starttag in str(strhtml):
        value = strhtml.split(starttag, 1)[1]
        value = value.split(endtag, 1)[0]
        value = re.sub("(\<.*?\>)", "",value)
        value = re.sub('[ \t]+' , ' ', value) 
        value=value.replace('\n',"") 
        while value.startswith(" "): 
            value = value[1:]
        while value.startswith(" "): 
            value = value[:-1]
    return value

def Get_ReplaceData(strhtml,starttag,endtag,replace_value,replay_value):
    
    if starttag =="":
        ReplaceOnly = True
    else:
        ReplaceOnly = False    
    
    if ReplaceOnly == False:
        if starttag in str(strhtml):
            length = len(replace_value)
            value = strhtml.split(starttag, 1)[1]
            if endtag!="":
                value = value.split(endtag, 1)[0]                        
            value = value.strip()
            value=value.replace('\n',"")
            value=value.replace('&amp;',"&")
            
            ##print value
            value=value.replace("style=\"border-width:0px;\">","")
            value=value.replace("|",",")
            for i in range(0,length):
                value = value.replace(replace_value[i],replay_value[i])                   
            value = re.sub("(\<.*?\>)", "", value.strip())
            value = re.sub('[ \t]+' , ' ',  value.strip())
            value=value.replace(". . |","")               
            value=value.replace("&lt; Prev 1 2 Next &gt;","")
            value = value.replace('&nbsp;&nbsp;','')
            value = value.replace('&nbsp;','')
            value = value.replace('View Details','')
            #===================================================================
            # if value[0] in '|' :
            #     value=value[1:]                   
            #===================================================================
            value_ext = "\n".join([ll.rstrip() for ll in value.splitlines() if ll.strip()])
            value = value.replace('"','')
            if "if (typeof (onCompletedListLoaded) != " in str(value_ext):
                value_ext = value_ext.split("if (typeof (onCompletedListLoaded) != ", 1)[0]
            value_ext = value_ext.replace('"','')
            value_ext=re.sub(' +',' ',value_ext.strip())
            value_ext = "\n".join([ll.rstrip() for ll in value_ext.splitlines() if ll.strip()])
            value_ext = value_ext.strip()
            value_ext = value_ext.replace("\n","") 
            value_ext = re.sub("(\<.*?\>)", "",value_ext) 
            k=0
            while k<5:
                k = k +1
                replace_char = [" |","| ","||"," ,",", ",",,",'&nbsp;',': ',' :','Date,Type,Description,Status',',|','::',':|',',--,',' ;','; ',',;,',';|',';;',';;'] 
                replay_char  = ["|","|","|",",",",",",",'',':',':','','|',':','|','--',';',';',';','|',';',';'] 
                length_replace = len(replace_char) 
                for i in range(0,length_replace):
                    while replace_char[i] in value_ext:
                        value_ext = value_ext.replace(replace_char[i],replay_char[i]) 
                
                slice_char=[' ',',',';','|',':']   
                length_slice = len(slice_char)
                for i in range(0,length_slice):
                    while value_ext.startswith(slice_char[i]): 
                        value_ext = value_ext[1:]
                    while value_ext.endswith(slice_char[i]): 
                        value_ext = value_ext[:-1]
                        
                replace_char = [" |","| ","||"," ,",", ",",,",'&nbsp;',': ',' :','Date,Type,Description,Status',',|','::',':|',',--,',' ;','; ',',;,',';|',';;',';;'] 
                replay_char  = ["|","|","|",",",",",",",'',':',':','','|',':','|','--',';',';',';','|',';',';']  
                length_replace = len(replace_char) 
                for i in range(0,length_replace):
                    while replace_char[i] in value_ext:
                        value_ext = value_ext.replace(replace_char[i],replay_char[i])    
                                           
    if ReplaceOnly == True:
        try:
            
            length = len(replace_value)
            value = str(strhtml)
            value = value.replace('&nbsp;','') 
            value=value.replace('&amp;',"&") 
            value = value.strip()
            ##print value
            value=value.replace("style=\"border-width:0px;\">","")
            value=value.replace("|",",")
            for i in range(0,length):
                value = value.replace(replace_value[i],replay_value[i])                   
            value = re.sub("(\<.*?\>)", "", value.strip())
            value = re.sub('[ \t]+' , ' ',  value.strip())
            value=value.replace(". . |","")               
            value=value.replace("&lt; Prev 1 2 Next &gt;","")
            value = value.replace('&nbsp;&nbsp;','')
            value = value.replace('&nbsp;','')
            value = value.replace('View Details','')
            #===================================================================
            # if value[0] in '|' :
            #     value=value[1:]                   
            #===================================================================
            value_ext = "\n".join([ll.rstrip() for ll in value.splitlines() if ll.strip()])
            value = value.replace('"','')
            if "if (typeof (onCompletedListLoaded) != " in str(value_ext):
                value_ext = value_ext.split("if (typeof (onCompletedListLoaded) != ", 1)[0]
            value_ext = value_ext.replace('"','')
            value_ext=re.sub(' +',' ',value_ext.strip())
            value_ext = "\n".join([ll.rstrip() for ll in value_ext.splitlines() if ll.strip()])
            value_ext = value_ext.strip()
            value_ext = value_ext.replace("\n","") 
            value_ext = re.sub("(\<.*?\>)", "",value_ext) 
            k=0
            while k<5:
                k = k +1
                replace_char = [" |","| ","||"," ,",", ",",,",'&nbsp;',': ',' :','Date,Type,Description,Status',',|','::',':|',',--,',' ;','; ',',;,',';|',';;',';;'] 
                replay_char  = ["|","|","|",",",",",",",'',':',':','','|',':','|','--',';',';',';','|',';',';']  
                length_replace = len(replace_char) 
                for i in range(0,length_replace):
                    while replace_char[i] in value_ext:
                        value_ext = value_ext.replace(replace_char[i],replay_char[i]) 
                
                slice_char=[' ',',',';','|',':']   
                length_slice = len(slice_char)
                for i in range(0,length_slice):
                    while value_ext.startswith(slice_char[i]): 
                        value_ext = value_ext[1:]
                    while value_ext.endswith(slice_char[i]): 
                        value_ext = value_ext[:-1]
                        
                replace_char = [" |","| ","||"," ,",", ",",,",'&nbsp;',': ',' :','Date,Type,Description,Status',',|','::',':|',',--,',' ;','; ',',;,',';|',';;',';;'] 
                replay_char  = ["|","|","|",",",",",",",'',':',':','','|',':','|','--',';',';',';','|',';',';'] 
                length_replace = len(replace_char) 
                for i in range(0,length_replace):
                    while replace_char[i] in value_ext:
                        value_ext = value_ext.replace(replace_char[i],replay_char[i])    
                                
        except Exception as e:
            log("Not found")
            
    value_ext = re.sub("(\<.*?\>)", "",value_ext)    
    return value_ext
def Get_ReplaceData_old(strhtml,starttag,endtag,replace_value,replay_value):
    if starttag in str(strhtml):
        value = strhtml.split(starttag, 1)[1]
        value = value.split(endtag, 1)[0]
        value = value.strip()
        value=value.replace("style=\"border-width:0px;\">","")
        value=value.replace("^",",")
        value = value.replace(replace_value[0],replay_value[0])
        value = value.replace(replace_value[1],replay_value[1])
        value = value.replace(replace_value[2],replay_value[2])
        value = re.sub("(\<.*?\>)", "", value.strip())
        value = re.sub('[ \t]+' , ' ',  value.strip())
        value=value.replace("&#39;","'")
        value=value.replace("&#39","'")
        value=value.replace("&amp;", "&")
        value=value.replace("&quot;", "\"")
        value=value.replace("&lt; Prev 1 2 Next &gt;","")
        value=value.replace("&gt;","")
        value=value.replace("&lt;","")
        value = value.replace('&nbsp;&nbsp;','')
        value = value.replace('View Details','')
        if value[0] in '^' :
            value=value[1:]
       
        #=======================================================================
        # if value[int(len(value)-1)] in '^' :
        #     value=value[1:]
        #=======================================================================
       
        value_ext = "\n".join([ll.rstrip() for ll in value.splitlines() if ll.strip()])
        value = value.replace('"','')
        if "if (typeof (onCompletedListLoaded) != " in str(value_ext):
            value_ext = value_ext.split("if (typeof (onCompletedListLoaded) != ", 1)[0]
        value_ext = value_ext.replace('"','')
        value_ext=re.sub(' +',' ',value_ext.strip())
        value_ext = "\n".join([ll.rstrip() for ll in value_ext.splitlines() if ll.strip()])
        value_ext = value_ext.strip()
        value_ext = value_ext.replace("\n","")        
        while " ^" in value_ext:
            value_ext = value_ext.replace(" ^","^") 
        while "^ " in value_ext:
            value_ext = value_ext.replace("^ ","^")
        while "^^" in value_ext:
            value_ext = value_ext.replace("^^","^")    
        while value_ext.startswith(" "): 
            value_ext = value_ext[1:]
        while value_ext.endswith(" "): 
            value_ext = value_ext[:-1]
        while value_ext.startswith("^"): 
            value_ext = value_ext[1:]
        while value_ext.endswith("^"): 
            value_ext = value_ext[:-1] 
        value_ext = value_ext.replace("&amp;","&") 
        value_ext = value_ext.replace('&nbsp;','')           
        value_ext = value_ext.replace("^^","^")
        while value_ext.endswith("^"): 
            value_ext = value_ext[:-1] 
        value_ext = value_ext.rstrip()
        value_ext = value_ext.lstrip()
        
    return value_ext
def ViewState(webContent_main):

    try:
        if "id=\"__VIEWSTATE\" value=\"" in str(webContent_main):
            ViewState = webContent_main.split("id=\"__VIEWSTATE\" value=\"", 1)[1]
            ViewState = ViewState.split("\"", 1)[0]
            ViewState = re.sub("(\<.*?\>)", "",ViewState)
            ViewState = ViewState.replace("/","%2F")
            ViewState = ViewState.replace("=","%3D")
            ViewState = ViewState.replace("+","%2B")
        elif "name=\"__VIEWSTATE\" type=\"hidden\" value=\"" in str(webContent_main):
            ViewState = webContent_main.split("name=\"__VIEWSTATE\" type=\"hidden\" value=\"", 1)[1]
            ViewState = ViewState.split("\"/>", 1)[0]
            ViewState = re.sub("(\<.*?\>)", "",ViewState)
            ViewState = ViewState.replace("/","%2F")
            ViewState = ViewState.replace("=","%3D")
            ViewState = ViewState.replace("+","%2B") 
        elif "VIEWSTATE0" in str(webContent_main):
            ViewState = webContent_main.split("VIEWSTATE0", 1)[1]
            #print ViewState
            ViewState = ViewState.split("0__EVENTVALIDATION", 1)[0]
            ViewState = re.sub("(\<.*?\>)", "",ViewState)
            #print ViewState
            ViewState = ViewState.replace("/","%2F")
            ViewState = ViewState.replace("=","%3D")
            ViewState = ViewState.replace("+","%2B")
        elif "__VIEWSTATE|" in str(webContent_main):
            ViewState = webContent_main.split("__VIEWSTATE|", 1)[1]
            #print ViewState
            ViewState = ViewState.split("|", 1)[0]
            ViewState = re.sub("(\<.*?\>)", "",ViewState)
            #print ViewState
            ViewState = ViewState.replace("/","%2F")
            ViewState = ViewState.replace("=","%3D")
            ViewState = ViewState.replace("+","%2B")        
    except: 
        log("ViewState Not found")
        
    try : 
        if 'id="CSRF_TOKEN" value="' in str(webContent_main):
           CSRF_TOKEN = webContent_main.split('id="CSRF_TOKEN" value="', 1)[1]
           CSRF_TOKEN =CSRF_TOKEN.split("\"", 1)[0]
           CSRF_TOKEN = re.sub("(\<.*?\>)", "",CSRF_TOKEN)
           CSRF_TOKEN =CSRF_TOKEN.replace("/","%2F")
           CSRF_TOKEN =CSRF_TOKEN.replace("=","%3D")
           CSRF_TOKEN =CSRF_TOKEN.replace("+","%2B")
        elif "name=\"__CSRF_TOKEN\" type=\"hidden\" value=\"" in str(webContent_main):
           CSRF_TOKEN = webContent_main.split("name=\"__CSRF_TOKEN\" type=\"hidden\" value=\"", 1)[1]
           CSRF_TOKEN =CSRF_TOKEN.split("/>", 1)[0]
           CSRF_TOKEN = re.sub("(\<.*?\>)", "",CSRF_TOKEN)
           CSRF_TOKEN =CSRF_TOKEN.replace("\"","")
           CSRF_TOKEN =CSRF_TOKEN.replace("/","%2F")
           CSRF_TOKEN =CSRF_TOKEN.replace("=","%3D")
           CSRF_TOKEN =CSRF_TOKEN.replace("+","%2B")  
        elif "CSRF_TOKEN|" in str(webContent_main):
           CSRF_TOKEN = webContent_main.split("CSRF_TOKEN|", 1)[1]
           CSRF_TOKEN =CSRF_TOKEN.split("|", 1)[0]
           CSRF_TOKEN = re.sub("(\<.*?\>)", "",CSRF_TOKEN)
           CSRF_TOKEN =CSRF_TOKEN.replace("\"","")
           CSRF_TOKEN =CSRF_TOKEN.replace("/","%2F")
           CSRF_TOKEN =CSRF_TOKEN.replace("=","%3D")
           CSRF_TOKEN =CSRF_TOKEN.replace("+","%2B")               
    except:
        log("CSRF_TOKEN Found") 
          
    try : 
        if "id=\"__VIEWSTATEGENERATOR\" value=\"" in str(webContent_main):
            VIEWSTATEGENERATOR = webContent_main.split("id=\"__VIEWSTATEGENERATOR\" value=\"", 1)[1]
            VIEWSTATEGENERATOR = VIEWSTATEGENERATOR.split("\"", 1)[0]
            VIEWSTATEGENERATOR = re.sub("(\<.*?\>)", "",VIEWSTATEGENERATOR)
            VIEWSTATEGENERATOR = VIEWSTATEGENERATOR.replace("/","%2F")
            VIEWSTATEGENERATOR = VIEWSTATEGENERATOR.replace("=","%3D")
            VIEWSTATEGENERATOR = VIEWSTATEGENERATOR.replace("+","%2B")
        elif "name=\"__VIEWSTATEGENERATOR\" type=\"hidden\" value=\"" in str(webContent_main):
            VIEWSTATEGENERATOR = webContent_main.split("name=\"__VIEWSTATEGENERATOR\" type=\"hidden\" value=\"", 1)[1]
            VIEWSTATEGENERATOR = VIEWSTATEGENERATOR.split("/>", 1)[0]
            VIEWSTATEGENERATOR = re.sub("(\<.*?\>)", "",VIEWSTATEGENERATOR)
            VIEWSTATEGENERATOR = VIEWSTATEGENERATOR.replace("\"","")
            VIEWSTATEGENERATOR = VIEWSTATEGENERATOR.replace("/","%2F")
            VIEWSTATEGENERATOR = VIEWSTATEGENERATOR.replace("=","%3D")
            VIEWSTATEGENERATOR = VIEWSTATEGENERATOR.replace("+","%2B")   
        elif "__VIEWSTATEGENERATOR|" in str(webContent_main):
            VIEWSTATEGENERATOR = webContent_main.split("__VIEWSTATEGENERATOR|", 1)[1]
            VIEWSTATEGENERATOR = VIEWSTATEGENERATOR.split("|", 1)[0]
            VIEWSTATEGENERATOR = re.sub("(\<.*?\>)", "",VIEWSTATEGENERATOR)
            VIEWSTATEGENERATOR = VIEWSTATEGENERATOR.replace("\"","")
            VIEWSTATEGENERATOR = VIEWSTATEGENERATOR.replace("/","%2F")
            VIEWSTATEGENERATOR = VIEWSTATEGENERATOR.replace("=","%3D")
            VIEWSTATEGENERATOR = VIEWSTATEGENERATOR.replace("+","%2B")               
    except:
        log("VIEWSTATEGENERATORNot Found")
    try : 
        if "id=\"__EVENTVALIDATION\" value=\"" in str(webContent_main):
            EVENTVALIDATION = webContent_main.split("id=\"__EVENTVALIDATION\" value=\"", 1)[1]
            EVENTVALIDATION = EVENTVALIDATION.split("\" />", 1)[0]
            #print EVENTVALIDATION
            EVENTVALIDATION = re.sub("(\<.*?\>)", "",EVENTVALIDATION)
            EVENTVALIDATION = EVENTVALIDATION.replace("/","%2F")
            EVENTVALIDATION = EVENTVALIDATION.replace("=","%3D")
            EVENTVALIDATION = EVENTVALIDATION.replace("+","%2B") 
        elif "name=\"__EVENTVALIDATION\" type=\"hidden\" value=\"" in str(webContent_main):
            EVENTVALIDATION = webContent_main.split("name=\"__EVENTVALIDATION\" type=\"hidden\" value=\"", 1)[1]
            EVENTVALIDATION = EVENTVALIDATION.split("/>", 1)[0]
            #print EVENTVALIDATION
            EVENTVALIDATION = re.sub("(\<.*?\>)", "",EVENTVALIDATION)
            EVENTVALIDATION = EVENTVALIDATION.replace("/","%2F")
            EVENTVALIDATION = EVENTVALIDATION.replace("=","%3D")
            EVENTVALIDATION = EVENTVALIDATION.replace("+","%2B")
            EVENTVALIDATION = EVENTVALIDATION.replace("\"","")
        elif "0__EVENTVALIDATION0" in str(webContent_main):
            EVENTVALIDATION = webContent_main.split("0__EVENTVALIDATION0", 1)[1]
            EVENTVALIDATION = EVENTVALIDATION.split("0<jssrc>", 1)[0]
            #print EVENTVALIDATION
            EVENTVALIDATION = re.sub("(\<.*?\>)", "",EVENTVALIDATION)
            EVENTVALIDATION = EVENTVALIDATION.replace("/","%2F")
            EVENTVALIDATION = EVENTVALIDATION.replace("=","%3D")
            EVENTVALIDATION = EVENTVALIDATION.replace("+","%2B")
            EVENTVALIDATION = EVENTVALIDATION.replace("\"","")                  
    except:
        log("ACA_CS_FIELD Found")     
    EVENTTARGET=""     
    try:
        if 'class="SelectedPageButton font11px">' in str(webContent_main):
            EVENTTARGET = webContent_main.split('class="SelectedPageButton font11px">', 1)[1]
            EVENTTARGET = EVENTTARGET.split("javascript:__doPostBack", 1)[1] 
            EVENTTARGET = EVENTTARGET.split("\"", 1)[0] 
            EVENTTARGET = re.sub("(\<.*?\>)", "",EVENTTARGET)
            EVENTTARGET = EVENTTARGET.replace("&#39;", "")
            EVENTTARGET = EVENTTARGET.replace("$", "%24")
            EVENTTARGET = EVENTTARGET.replace("(", "")
            EVENTTARGET = EVENTTARGET.replace(")", "")
            EVENTTARGET = EVENTTARGET.replace("'", "")
            EVENTTARGET = EVENTTARGET.replace(",", "")                                                                              
    except Exception as e:
        EVENTTARGET=''
        log(str(e))
        
    return [ViewState,VIEWSTATEGENERATOR,EVENTVALIDATION]
    #return [ViewState]
def ViewState2(webContent_main):

    try:
        if "id=\"__VIEWSTATE\" value=\"" in str(webContent_main):
            ViewState = webContent_main.split("id=\"__VIEWSTATE\" value=\"", 1)[1]
            ViewState = ViewState.split("\"", 1)[0]
            ViewState = re.sub("(\<.*?\>)", "",ViewState)
            ViewState = ViewState.replace("/","%2F")
            ViewState = ViewState.replace("=","%3D")
            ViewState = ViewState.replace("+","%2B")
        elif "name=\"__VIEWSTATE\" type=\"hidden\" value=\"" in str(webContent_main):
            ViewState = webContent_main.split("name=\"__VIEWSTATE\" type=\"hidden\" value=\"", 1)[1]
            ViewState = ViewState.split("\"/>", 1)[0]
            ViewState = re.sub("(\<.*?\>)", "",ViewState)
            ViewState = ViewState.replace("/","%2F")
            ViewState = ViewState.replace("=","%3D")
            ViewState = ViewState.replace("+","%2B") 
        elif "VIEWSTATE<&>0" in str(webContent_main):
            ViewState = webContent_main.split("VIEWSTATE<&>0", 1)[1]
            #print ViewState
            ViewState = ViewState.split("<&>0", 1)[0]
            ViewState = re.sub("(\<.*?\>)", "",ViewState)
            #print ViewState
            ViewState = ViewState.replace("/","%2F")
            ViewState = ViewState.replace("=","%3D")
            ViewState = ViewState.replace("+","%2B")
        elif "VIEWSTATE0" in str(webContent_main):
            ViewState = webContent_main.split("VIEWSTATE0", 1)[1]
            #print ViewState
            ViewState = ViewState.split("0<jssrc>", 1)[0]
            ViewState = re.sub("(\<.*?\>)", "",ViewState)
            #print ViewState
            ViewState = ViewState.replace("/","%2F")
            ViewState = ViewState.replace("=","%3D")
            ViewState = ViewState.replace("+","%2B")
        elif "__VIEWSTATE|" in str(webContent_main):
            ViewState = webContent_main.split("__VIEWSTATE|", 1)[1]
            #print ViewState
            ViewState = ViewState.split("|", 1)[0]
            ViewState = re.sub("(\<.*?\>)", "",ViewState)
            #print ViewState
            ViewState = ViewState.replace("/","%2F")
            ViewState = ViewState.replace("=","%3D")
            ViewState = ViewState.replace("+","%2B")    
            
            
    except:
        
        log("ViewState Not found")
        
    try : 
        if "id=\"__EVENTVALIDATION\" value=\"" in str(webContent_main):
            EVENTVALIDATION = webContent_main.split("id=\"__EVENTVALIDATION\" value=\"", 1)[1]
            EVENTVALIDATION = EVENTVALIDATION.split("\" />", 1)[0]
            #print EVENTVALIDATION
            EVENTVALIDATION = re.sub("(\<.*?\>)", "",EVENTVALIDATION)
            EVENTVALIDATION = EVENTVALIDATION.replace("/","%2F")
            EVENTVALIDATION = EVENTVALIDATION.replace("=","%3D")
            EVENTVALIDATION = EVENTVALIDATION.replace("+","%2B") 
        elif "name=\"__EVENTVALIDATION\" type=\"hidden\" value=\"" in str(webContent_main):
            EVENTVALIDATION = webContent_main.split("name=\"__EVENTVALIDATION\" type=\"hidden\" value=\"", 1)[1]
            EVENTVALIDATION = EVENTVALIDATION.split("/>", 1)[0]
            #print EVENTVALIDATION
            EVENTVALIDATION = re.sub("(\<.*?\>)", "",EVENTVALIDATION)
            EVENTVALIDATION = EVENTVALIDATION.replace("/","%2F")
            EVENTVALIDATION = EVENTVALIDATION.replace("=","%3D")
            EVENTVALIDATION = EVENTVALIDATION.replace("+","%2B")
            EVENTVALIDATION = EVENTVALIDATION.replace("\"","")
        elif "0__EVENTVALIDATION0" in str(webContent_main):
            EVENTVALIDATION = webContent_main.split("0__EVENTVALIDATION0", 1)[1]
            EVENTVALIDATION = EVENTVALIDATION.split("0<jssrc>", 1)[0]
            #print EVENTVALIDATION
            EVENTVALIDATION = re.sub("(\<.*?\>)", "",EVENTVALIDATION)
            EVENTVALIDATION = EVENTVALIDATION.replace("/","%2F")
            EVENTVALIDATION = EVENTVALIDATION.replace("=","%3D")
            EVENTVALIDATION = EVENTVALIDATION.replace("+","%2B")
            EVENTVALIDATION = EVENTVALIDATION.replace("\"","")                  
    except:
        log("ACA_CS_FIELD Found")     
   
    return [ViewState]
def GET_Cookie(Response_Headers2):
    from Extract_Data import GET_data
    try:
        global ASPXANONYMOUS
        global LASTEST_REQUEST_TIME
        global ASP_NET_SessionId
        global ACA_USER_PREFERRED_CULTURE
        global ACA_COOKIE_SUPPORT_ACCESSSIBILITY
        global ACA_CSRF_TOKEN
       
        
        try:
            if "ASPXANONYMOUS=" in Response_Headers2:
                ASPXANONYMOUS=GET_data(Response_Headers2,"ASPXANONYMOUS=",";")
                ##print ASPXANONYMOUS
        except Exception as e:
            ASPXANONYMOUS=""                
        try:
            if "LASTEST_REQUEST_TIME=" in Response_Headers2:
                LASTEST_REQUEST_TIME=GET_data(Response_Headers2,"LASTEST_REQUEST_TIME=",";")
                ##print LASTEST_REQUEST_TIME 
        except Exception as e: 
            LASTEST_REQUEST_TIME=""  
        try:
            if "ASP.NET_SessionId=" in Response_Headers2:
                ASP_NET_SessionId=GET_data(Response_Headers2,"ASP.NET_SessionId=",";")
                ##print ASP_NET_SessionId
        except Exception as e:
            ASP_NET_SessionId=""     
        try:
            if "ACA_USER_PREFERRED_CULTURE=" in Response_Headers2:
                ACA_USER_PREFERRED_CULTURE=GET_data(Response_Headers2,"ACA_USER_PREFERRED_CULTURE=",";")
                ##print ACA_USER_PREFERRED_CULTURE 
        except Exception as e:
            ACA_USER_PREFERRED_CULTURE=""        
        try:
            if "ACA_COOKIE_SUPPORT_ACCESSSIBILITY=" in Response_Headers2:
                ACA_COOKIE_SUPPORT_ACCESSSIBILITY=GET_data(Response_Headers2,"ACA_COOKIE_SUPPORT_ACCESSSIBILITY=",";")
                ##print ASPXANONYMOUS
        except Exception as e:
            ACA_COOKIE_SUPPORT_ACCESSSIBILITY=""   
        try:
            if "ACA_CSRF_TOKEN=" in Response_Headers2:
                ACA_CSRF_TOKEN=GET_data(Response_Headers2,"ACA_CSRF_TOKEN=",";")
                ##print ACA_CS_KEY
        except Exception as e:
            ACA_CSRF_TOKEN=""     
             
               
        #Cookie=' LASTEST_REQUEST_TIME='+LASTEST_REQUEST_TIME+'; .ASPXANONYMOUS='+ASPXANONYMOUS+'; ASP.NET_SessionId='+ASP_NET_SessionId+'; ACA_USER_PREFERRED_CULTURE='+ACA_USER_PREFERRED_CULTURE+'; ACA_COOKIE_SUPPORT_ACCESSSIBILITY='+ACA_COOKIE_SUPPORT_ACCESSSIBILITY+'; ACA_CSRF_TOKEN='+ACA_CSRF_TOKEN
        #return Cookie
        
        return [LASTEST_REQUEST_TIME,ASPXANONYMOUS,ASP_NET_SessionId,ACA_USER_PREFERRED_CULTURE,ACA_COOKIE_SUPPORT_ACCESSSIBILITY,ACA_CSRF_TOKEN]
        
    except Exception as e:
        log(str(e))
        
            