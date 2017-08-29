# -*- coding: utf-8 -*-

# plugin.program.tbs
# Total Revolution Maintenance (c) by whufclee (info@totalrevolution.tv)

# Total Revolution Maintenance is licensed under a
# Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.

# You should have received a copy of the license along with this
# work. If not, see http://creativecommons.org/licenses/by-nc-nd/4.0.

import binascii
import koding
import os
import pyxbmct
import re
import sys
import time
import urllib
import urllib2
import urlparse
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import shutil
import zipfile

try: from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database

from koding import *

try:
    AddonID = xbmcaddon.Addon().getAddonInfo('id')
except:
    AddonID = Caller()
#---------------------------------------------------------------------------------------------------
ADDON            =  xbmcaddon.Addon(id=AddonID)
ADDON_PATH       =  ADDON.getAddonInfo('path')
USB              =  Addon_Setting(setting='zip')
thirdparty       =  Addon_Setting(setting='thirdparty')
userid           =  Addon_Setting(setting='userid')
debug            =  Addon_Setting(setting='debug')
HOME             =  xbmc.translatePath('special://home/')
USERDATA         =  xbmc.translatePath('special://profile/')
ADDON_DATA       =  os.path.join(USERDATA,  'addon_data')
TBSDATA          =  os.path.join(ADDON_DATA,AddonID)
PLAYLISTS        =  os.path.join(USERDATA,  'playlists')
MEDIA            =  os.path.join(HOME,      'media')
DATABASE         =  os.path.join(USERDATA,  'Database')
THUMBNAILS       =  os.path.join(USERDATA,  'Thumbnails')
ADDONS           =  os.path.join(HOME,      'addons')
PACKAGES         =  os.path.join(ADDONS,    'packages')
BRANDART         =  os.path.join(MEDIA,     'branding','Splash.png')
KEYMAPS          =  os.path.join(USERDATA,  'keymaps','keyboard.xml')
KEYWORD_FILE     =  os.path.join(HOME,      'userdata','addon_data','script.openwindow','keyword')
FAVS             =  os.path.join(USERDATA,  'favourites.xml')
GUI              =  os.path.join(USERDATA,  'guisettings.xml')
SOURCE           =  os.path.join(USERDATA,  'sources.xml')
ADVANCED         =  os.path.join(USERDATA,  'advancedsettings.xml')
RSS              =  os.path.join(USERDATA,  'RssFeeds.xml')
PROGRESS_TEMP    =  os.path.join(TBSDATA,   'progresstemp')
SLEEPER          =  os.path.join(ADDON_PATH,'resources','tmr')
KEYWORD_CREATE   =  os.path.join(TBSDATA,   'keyword_create.txt')
MY_HOME_MENUS    =  os.path.join(TBSDATA,   'my_home_menus')
MAIN_MENUS       =  os.path.join(TBSDATA,   'main_menu_names')
REDIRECTS        =  os.path.join(TBSDATA,   'redirects')
SF_ROOT          =  os.path.join(ADDON_DATA,'plugin.program.super.favourites', 'Super Favourites')
NON_REGISTERED   =  os.path.join(ADDON_DATA,'script.openwindow','unregistered')
XBMC_VERSION     =  xbmc.getInfoLabel("System.BuildVersion")[:2]
CONFIG           =  '/storage/.config/'
STORAGE          =  '/storage/'
BASE2            =  '687474703a2f2f6e6f6f6273616e646e657264732e636f6d2f'
BASE             =  Addon_Setting(addon_id='script.openwindow',setting='base')
dialog           =  xbmcgui.Dialog()
dp               =  xbmcgui.DialogProgress()
skin             =  xbmc.getSkinDir()
artpath          =  os.path.join(ADDON_PATH,'resources')
checkicon        =  os.path.join(artpath,'check.png')
unknown_icon     =  os.path.join(artpath,'update.png')
dialog_bg        =  os.path.join(artpath,'background.png')
black            =  os.path.join(artpath,'black.png')
db_social        =  xbmc.translatePath('special://profile/addon_data/plugin.program.tbs/database.db')
usercheck_file   =  os.path.join(ADDON_DATA,AddonID,'usercheck')
adult_store      =  xbmc.translatePath("special://profile/addon_data/script.module.python.koding.aio/adult_store")
pos              =  0
listicon         =  ''
my_dialog        = True
progress         = False

ACTION_NAV_BACK  =  92
ACTION_MOVE_UP   =  3
ACTION_MOVE_DOWN =  4

try:
    adult_list = Addon_Genre(custom_url='http://totalrevolution.xyz/addons/addon_list.txt').items()
except:
    try:
        adult_list = Addon_Genre().items()
    except:
        adult_list = []

adult_addons = []
for item in adult_list:
    adult_addons.append(item[1])

if os.path.exists(BRANDART):
    FANART = BRANDART
else:
    FANART = os.path.join(ADDONS,AddonID,'fanart.jpg')

if thirdparty == 'true':
    social_shares = 1
else:
    social_shares = 0
#---------------------------------------------------------------------------------------------------
# Popup class - thanks to whoever codes the help popup in TVAddons Maintenance for this section. Unfortunately there doesn't appear to be any author details in that code so unable to credit by name.
class SPLASH(xbmcgui.WindowXMLDialog):
    
    def __init__(self,*args,**kwargs):
        self.shut=kwargs['close_time']
        xbmc.executebuiltin("Skin.Reset(AnimeWindowXMLDialogClose)")
        xbmc.executebuiltin("Skin.SetBool(AnimeWindowXMLDialogClose)")
    
    def onFocus(self,controlID):
        pass
    
    def onClick(self,controlID): 
        if controlID==12:
            xbmc.Player().stop()
            self._close_dialog()
    
    def onAction(self,action):
        if action in [5,6,7,9,10,92,117] or action.getButtonCode() in [275,257,261]:
            xbmc.Player().stop()
            self._close_dialog()
    
    def _close_dialog(self):
        xbmc.executebuiltin("Skin.Reset(AnimeWindowXMLDialogClose)")
        xbmc.sleep(400)
        self.close()
#---------------------------------------------------------------------------------------------------
# Add-on removal menu
@route(mode='addon_removal_menu', args=['removal_types'])
def Addon_Removal_Menu(removal_types='all'):
    skiparray = ['repository.xbmc.org','repository.spartacus','plugin.program.tbs','script.openwindow','plugin.program.super.favourites','plugin.video.metalliq','script.qlickplay','script.trtv','plugin.video.addons.ini.creator']
    namearray = []
    iconarray = []
    descarray = []
    patharray = []
    finalpath = []
    Adult_Toggle(adult_list=adult_addons,disable=False)
    Refresh('addons')
    my_addons = []

    currently_installed = Get_Contents(ADDONS,['packages','temp'])
    dolog(repr(currently_installed))
    if removal_types == 'all' or 'video' in removal_types:
        my_addons = Installed_Addons(content='video', properties='name,path,description,thumbnail')
    if removal_types == 'all' or 'audio' in removal_types:
        my_addons += Installed_Addons(content='audio', properties='name,path,description,thumbnail')
    if removal_types == 'all' or 'image' in removal_types:
        my_addons += Installed_Addons(content='image', properties='name,path,description,thumbnail')
    if removal_types == 'all' or 'program' in removal_types:
        my_addons += Installed_Addons(content='executable', properties='name,path,description,thumbnail')
    if removal_types == 'all' or 'repo' in removal_types:
        my_addons += Installed_Addons(types='xbmc.addon.repository', properties='name,path,description,thumbnail')
    for item in my_addons:
        if not item["addonid"] in skiparray and item["path"] in currently_installed:
            namearray.append(item["name"])
            iconarray.append(item["thumbnail"])
            descarray.append(item["description"])
            patharray.append(item["path"])

    finalarray = multiselect(String(30312),namearray,iconarray,descarray)
    for item in finalarray:
        newpath = patharray[item]
        newname = namearray[item]
        finalpath.append([newname,newpath])
    if len(finalpath) > 0:
        Remove_Addons(finalpath)
#---------------------------------------------------------------------------------------------------
# Function to browse the userdata/addon_data folder
@route(mode='addon_browser', args=['browser_type','header','skiparray','addons'])
def Addon_Browser(browser_type='list',header='',skiparray=[],addons=[]):
    if browser_type == 'keyword':
        skiparray = ['plugin.program.tbs','script.openwindow',skin]
    if header == '':
        header = String(30043)

    namearray = []
    iconarray = []
    descarray = []
    finallist = []
    idarray   = []
    my_addons = []
    temp_list = []

    my_addons_full = [
        Installed_Addons(content='video', properties='name,description,thumbnail'),
        Installed_Addons(content='audio', properties='name,description,thumbnail'),
        Installed_Addons(content='image', properties='name,description,thumbnail'),
        Installed_Addons(content='executable', properties='name,path,description,thumbnail'),
        Installed_Addons(types='xbmc.gui.skin', properties='name,path,description,thumbnail')]

    for mylist in my_addons_full:
        for item in mylist:
            if not item['addonid'] in temp_list:
                my_addons.append(item)
            temp_list.append(item["addonid"])

    for item in my_addons:
        if ( not item["addonid"].encode('utf-8') in skiparray and (len(addons)==0) or ( item["addonid"].encode('utf-8') in addons) ):
            namearray.append(item["name"])
            iconarray.append(item["thumbnail"])
            descarray.append(item["description"])
            idarray.append(item["addonid"].encode('utf-8'))

    finalarray = multiselect( String(30043),namearray,iconarray,descarray )
    for item in finalarray:
        if browser_type == 'list':
            finallist.append( [namearray[item].encode('utf-8'), idarray[item]] )
        elif browser_type == 'keyword':
            finallist.append( idarray[item] )

    return finallist
#---------------------------------------------------------------------------------------------------
# Browse the add-on data folders and return a list
def Addon_Data_Browser(header='',skiparray=[]):
    if header == '':
        header = String(30400)

    namearray = []
    iconarray = []
    descarray = []
    finallist = []
    idarray   = []
    my_addons = []

    addon_data = Get_Contets(path=ADDON_DATA,folders=True)
    for item in addon_data:
        try:
            name        = Addon_Info(addon_id=item,id='name')
            thumbnail   = Addon_Info(addon_id=item,id='icon')
            description = Addon_Info(addon_id=item,id='description')
            namearray.append(name)
            iconarray.append(thumbnail)
            descarray.append(description)
            idarray.append(item)
        except:
            pass

    finalarray = multiselect(String(30043),namearray,iconarray,descarray)
    for item in finalarray:
        finallist.append(idarray[item])

    return finallist
#---------------------------------------------------------------------------------------------------
# Enable/disable the visibility of adult add-ons (use true or false)
@route(mode='adult_filter', args=['value','loadtype'])
def Adult_Filter(value, loadtype = ''):
    success = 0
    if value == 'true':
        try:
            password = Addon_Setting(setting='xxxpass')
            if password != '':
                password = encryptme('d',password)
            else:
                password = converthex(Text_File(xbmc.translatePath('special://home/userdata/addon_data/plugin.program.tbs/x'),'r'))
        except:
            password = ''

# If the password in the local file is blank we set it to the default of 69
        if password == '' or password == 'not set':
            password = '69'
        userpw   = Keyboard(String(30002)).replace('%20',' ')
        if userpw != password:
            value = 'false'
            OK_Dialog(String(30000),String(30001))
            xbmc.executebuiltin('HOME')
        else:
            success = 1
    dolog('ADULT ADDONS: %s'%adult_addons)
    if value == 'false':
        filter_type = 'disabled'
        Adult_Toggle(adult_list=adult_addons,disable=True)
    else:
        filter_type = 'enabled'
        Sleep_If_Function_Active(function=Adult_Toggle, args=[adult_addons,False])
    if loadtype != 'menu' and loadtype != 'startup':
        OK_Dialog(String(30003) % filter_type.upper(), String(30004) % filter_type)
    return success
#---------------------------------------------------------------------------------------------------
# Check for storage location on android
def Android_Path_Check():
    content = Grab_Log()
    localstorage  = re.compile('External storage path = (.+?);').findall(content)
    localstorage  = localstorage[0] if (len(localstorage) > 0) else 'Unknown'
    return localstorage
#---------------------------------------------------------------------------------------------------
# Check for non ascii files and folders
@route(mode='ASCII_Check')
def ASCII_Checker():
    failed_array = []
    sourcefile   = dialog.browse(3, String(30005), 'files', '', False, False)
    dp.create(String(30006),'',String(30007),'')
    asciifiles = ASCII_Check(sourcefile,dp)
    if len(asciifiles) > 0:
        mytext = String(30008)
        for item in asciifiles:
            mytext += item+'\n'
        Text_Box(String(30009),mytext)
        Sleep_If_Window_Active()
        if YesNo_Dialog(String(30010),String(30011)):
            if YesNo_Dialog(String(30012),String(30013)):
                for item in asciifiles:
                    if os.path.exists(item):
                        try:
                            os.remove(item)
                        except:
                            try:
                                shutil.rmtree(item)
                            except:
                                failed_array.append(item)
        if len(failed_array) > 0:
            mytext = String(30014)
            for item in asciifiles:
                mytext += item+'\n'
            Text_Box(String(30015),mytext)
            Sleep_If_Window_Active()
        else:
            OK_Dialog(String(30016),String(30017))
    else:
        OK_Dialog(String(30018),String(30019),String(30020))
#---------------------------------------------------------------------------------------------------
# Create backup menu
@route(mode='backup_option')
def Backup_Option():
    Add_Dir(String(30021),'addons','restore_zip',False,'','','Back Up Your Addons')
    Add_Dir(String(30022),'addon_data','restore_zip',False,'','','Back Up Your Addon Userdata')
    Add_Dir(String(30023),GUI,'restore_backup',False,'','','Back Up Your guisettings.xml')
    
    if os.path.exists(FAVS):
        Add_Dir(String(30024),FAVS,'restore_backup',False,'Backup.png','','Back Up Your favourites.xml')
    
    if os.path.exists(SOURCE):
        Add_Dir(String(30025),SOURCE,'restore_backup',False,'Backup.png','','Back Up Your sources.xml')
    
    if os.path.exists(ADVANCED):
        Add_Dir(String(30026),ADVANCED,'restore_backup',False,'Backup.png','','Back Up Your advancedsettings.xml')
    
    if os.path.exists(KEYMAPS):
        Add_Dir(String(30027),KEYMAPS,'restore_backup',False,'Backup.png','','Back Up Your keyboard.xml')
    
    if os.path.exists(RSS):
        Add_Dir(String(30028),RSS,'restore_backup',False,'Backup.png','','Back Up Your RssFeeds.xml')
#---------------------------------------------------------------------------------------------------
# Backup/Restore root menu
@route(mode='backup_restore')
def Backup_Restore():
    Add_Dir(String(30029),'none','backup_option',True,'Backup.png','','')
    Add_Dir(String(30030),'none','restore_option',True,'Restore.png','','')
#---------------------------------------------------------------------------------------------------
@route(mode='browse_qp')
def Browse_QP():
    options = [String(30549),String(13280,'system'),String(559,'system'),String(19029,'system')]
    choice  = Select_Dialog(String(1024,'system')+' YouTube',options)
    if choice >=0:
        if choice == 0:
            xbmc.executebuiltin('RunScript(script.qlickplay,info=list,type=playlist,id=PLrEnWoR732-BHrPp_Pm8_VleD68f9s14-)')
        if choice == 1:
            xbmc.executebuiltin('RunScript(script.qlickplay,info=list,type=video,sort=date)')
        if choice == 2:
            xbmc.executebuiltin('RunScript(script.qlickplay,info=list,type=playlist,sort=viewCount)')
        if choice == 3:
            xbmc.executebuiltin('RunScript(script.qlickplay,info=list,type=channel,sort=viewCount)')
#---------------------------------------------------------------------------------------------------
# Browse pre-installed repo's via the kodi add-on browser
@route(mode='browse_repos')
def Browse_Repos():
    xbmc.executebuiltin('ActivateWindow(10040,"addons://repos/",return)')
#---------------------------------------------------------------------------------------------------
def Build_Info():
    Build = ''
    if os.path.exists('/etc/release'):
        Build    = Text_File('/etc/release','r')

    if Build == '':
        logtext = Grab_Log()
        Buildmatch  = re.compile('Running on (.+?)\n').findall(logtext)
        Build       = Buildmatch[0] if (len(Buildmatch) > 0) else ''
    return Build.replace(' ','%20')
#---------------------------------------------------------------------------------------------------
# Main category list
@route(mode='start')
def Categories():
    if debug == 'true':
        Add_Dir('Koding','', "tutorials", True,'','','')
    Add_Dir(String(30032),'', 'my_details', False,'','','')
    Add_Dir(String(30033),'','install_content',True,'Search_Addons.png','','')
    Add_Dir(String(30034),'','startup_wizard',False,'Startup_Wizard.png','','')
    Add_Dir(String(30035),'none', 'tools',True,'Additional_Tools.png','','')
    # Add_Dir('Video Check','none', 'get_video',False,'Additional_Tools.png','','')
    # Add_Dir('folder','Android Apps','', 'android_apps', 'Additional_Tools.png','','','')
#---------------------------------------------------------------------------------------------------
# Main category list
def Change_Email():
    username  = encryptme( 'e',Addon_Setting('username') )
    email     = encryptme( 'e',Addon_Setting('email') )
    urlparams = encryptme( 'e',URL_Params() )
    password  = Update_Password(return_pass=True)

    if email != '' and username != '' and password != '':
        Run_Code( url='boxer/User_Change_Email.php',payload={"x":urlparams,"n":username,"e":email,"p":password,"a":"2"})
#---------------------------------------------------------------------------------------------------
@route(mode='change_id')
def Change_ID():
    if os.path.exists( os.path.join(TBSDATA,'admin') ):
        newid = Keyboard(String(30036))
        if newid != '':
            ADDON.setSetting('userid', encryptme('e',newid))
        else:
            Check_License()
        Refresh('container')
#---------------------------------------------------------------------------------------------------
def Change_XXX_Password():
    password = Addon_Setting('password')
    if password != '':
        OK_Dialog(String(30404),String(30406))
        user_pass = Keyboard(String(30407))
        if md5_check(user_pass,True) == password:
            OK_Dialog(String(30408),String(30409))
            new_pass = Keyboard(String(30408))
            Addon_Setting(setting='xxxpass',value=encryptme('e',new_pass))
        else:
            OK_Dialog(String(30000),String(30001))
    else:
        OK_Dialog(String(30404),String(30405))
#---------------------------------------------------------------------------------------------------
# Function to check the download path set in settings
def Check_Download_Path():
    path = os.path.join(USB,'testCBFolder')
    if not os.path.exists(USB):
        OK_Dialog(String(30037),String(30038)) 
        Open_Settings()
#---------------------------------------------------------------------------------------------------
def Check_File_Date(url, datefile, localdate, dst):
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        conn = urllib2.urlopen(req)
        last_modified = conn.info().getdate('last-modified')
        last_modified = time.strftime('%Y%m%d%H%M%S', last_modified)
        if int(last_modified) > int(localdate):
            urllib.urlretrieve(url,dst)
            if dst==epgdst:
                Extract(dst,ADDON_DATA)         
            else:
                Extract(dst,STORAGE)
            Text_File(last_modified,'w')
        try:
            if os.path.exists(dst):
                os.remove(dst)
        except:
            pass
    except:
        dolog("Failed with update: %s" % str(url))
        dolog( Last_Error() )
    Remove_Files()
#---------------------------------------------------------------------------------------------------
# Update registration status
def Check_License(r_mode='3'):
    try:
        Run_Code( url='boxer/Check_License.php', payload={'x':encryptme('e',URL_Params()),'v':XBMC_VERSION,'r':r_mode} )
    except:
        dolog( Last_Error() )
#---------------------------------------------------------------------------------------------------
# Check to see if any local shares require updating on server
@route(mode='check_shares', args=['url'])
def Check_My_Shares(url = ''):
    message = 0
    results = koding.Get_All_From_Table("shares")
    for item in results:
        path        = item["path"]
        oldmd5      = item["stamp"]
        cleanpath   = urllib.unquote(path).upper()
        try:
            dolog('CLEAN PATH: %s'%cleanpath)
            section,share = cleanpath.split('/')
        except:
            section = False
        dolog('Path: %s'%path)
        dolog('md5: %s'%oldmd5)
        local_path = os.path.join(SF_ROOT, 'HOME_'+urllib.unquote(path), 'favourites.xml')
        if os.path.exists(local_path):
            dolog('LOCAL PATH: %s'%local_path)
            localcheck = md5_check(local_path)
            dolog('new: %s'%localcheck)
            if oldmd5 != localcheck:
                message     = 1
                if YesNo_Dialog(String(30247), String(30248) % cleanpath):
                    success = Update_Share(os.path.join(SF_ROOT, 'HOME_'+path))
                    if success:
                        DB_Query(db_path=db_social, query='UPDATE shares SET stamp=? WHERE `path`=?', values=[localcheck,path])
        elif section:
            dolog('String1: %s'%String(30351))
            dolog('String2: %s'%String(30352))
            if YesNo_Dialog(String(30351),String(30352)%cleanpath):
                Sleep_If_Function_Active( Run_Code, ['boxer/Remove_Share.php', {"x":encryptme('e',URL_Params()),"y":encryptme('e',section),"z":encryptme('e',share)}] )
    if url == 'manual' and message == 0:
        OK_Dialog(String(30249), String(30249))
#---------------------------------------------------------------------------------------------------
def Check_Updates(url, datefile, dst):
    if os.path.exists(datefile):
        localdate = Text_File(datefile,'r')
    else:
        localdate = 0
    Check_File_Date(url, datefile, int(localdate), dst)
#---------------------------------------------------------------------------------------------------
# Function to clean HTML into plain text. Not perfect but it's better than raw html code!
def Clean_HTML(data):        
    data = data.replace('</p><p>','[CR][CR]').replace('&ndash;','-').replace('&mdash;','-').replace("\n", " ").replace("\r", " ").replace("&rsquo;", "'").replace("&rdquo;", '"').replace("</a>", " ").replace("&hellip;", '...').replace("&lsquo;", "'").replace("&ldquo;", '"')
    data = " ".join(data.split())   
    p    = re.compile(r'< script[^<>]*?>.*?< / script >')
    data = p.sub('', data)
    p    = re.compile(r'< style[^<>]*?>.*?< / style >')
    data = p.sub('', data)
    p    = re.compile(r'')
    data = p.sub('', data)
    p    = re.compile(r'<[^<]*?>')
    data = p.sub('', data)
    data = data.replace('&nbsp;',' ')
    return data
#---------------------------------------------------------------------------------------------------
# Function to clear all known cache files
@route(mode='clear_cache')
def Clear_Cache():
    choice = YesNo_Dialog(String(30039), String(30040), no=String(30041),yes=String(30042))
    if choice == 1:
        Wipe_Cache()
        Remove_Textures_Dialog()
#---------------------------------------------------------------------------------------------------
@route(mode='clear_commands')
def Clear_Commands():
    urlparams = encryptme('e',URL_Params())
    Run_Code( url='boxer/Clear_Commands.php',payload={"x":urlparams} )
#---------------------------------------------------------------------------------------------------
# Function to clear online cookie for user_info page
def Clear_User_Cookie():
    urlparams = encryptme('e',URL_Params())
    Run_Code( url='boxer/User_Info.php',payload={"x":urlparams,"r":"2"} )
#---------------------------------------------------------------------------------------------------
# Function to disassociate device from username
def Clear_User_Data(silent=False):
    Default_Setting(setting='email',reset=True)
    Default_Setting(setting='username',reset=True)
    Default_Setting(setting='userid',reset=True)
    Default_Setting(setting='password',reset=True)
    urlparams = encryptme('e',URL_Params())
    Run_Code( url='boxer/User_Info.php',payload={"x":urlparams,"r":"1"} )
#---------------------------------------------------------------------------------------------------
# Function to delete the userdata/addon_data folder
def CPU_Check():
    logtext     = Grab_Log()
    CPUmatch    = re.compile('Host CPU: (.+?) available').findall(logtext)
    CPU         = CPUmatch[0] if (len(CPUmatch) > 0) else ''
    return CPU.replace(' ','%20')
#---------------------------------------------------------------------------------------------------
# Create a list of addons
def Create_Keyword():
    addon_settings = []
    redirect_list  = []
    settings_list  = []
    addon_list     = [skin]
    content_list   = ['special://profile/guisettings.xml','special://profile/favourites.xml','special://profile/sources.xml','special://profile/addon_data/plugin.video.addons.ini.creator/.storage/folders']
    data_list      = []
    email          = encryptme( 'e',Addon_Setting('email') )
    username       = Addon_Setting('username')
    password       = Addon_Setting('password')
    keyword_backup = os.path.join(TBSDATA,'keyword_backup.txt')

# Add the redirects to the extras
    for item in os.listdir(REDIRECTS):
        if item.startswith('HOME_'):
            redirect_list.append(item)
    content_list  += ['special://profile/addon_data/plugin.program.tbs/redirects/' + s for s in redirect_list]
    dolog('DOING ADULT TOGGLE')
# Enable adult addons
    Sleep_If_Function_Active(function=Adult_Toggle, args=[adult_addons,False])

# Do a full backup or selection of addons/data to include
    if YesNo_Dialog(String(30189),String(30395),String(30396),String(30397)):
        my_addons = Keyword_Full_Backup()
    else:
        OK_Dialog(String(30398),String(30399))
        addons = Addon_Browser(browser_type='keyword')
        my_addons = 'my_addons=%s'%addons

# Backup all addon_data or select
        if YesNo_Dialog(String(30400),String(30401),String(30402),String(30397)):
            addon_settings = Create_Keyword_Addon_Data()
        else:

# Check to see if any valid addon_data exists for chosen addons
            for item in addons:
                if os.path.exists( os.path.join(ADDON_DATA,item,'settings.xml') ):
                    data_list.append(item)

# If addon_data exists bring up the select box to choose which data to include
            if len(data_list) > 0:
                settings_choice = Addon_Browser(addons=data_list)
                for item in settings_choice:
                    addon_list.append(item[1])
            else:
                OK_Dialog( String(30146),String(30500) )

            addon_settings  = Create_Keyword_Addon_Data(addons=addon_list)

# If we have some settings we add to an array
        if len(addon_settings) > 0:
            for item in addon_settings:
                if item[0] in addons or item[0]=='plugin.program.tbs' or item[0]==skin:
                    settings_list.append([item[0],item[1]])
        my_addons += '\nmy_settings=%s'%settings_list
        my_addons += '\nskin_shortcuts=%s'%Create_Skin_Shortcut_Data()

        extras     = File_Contents(content_list)
        my_addons += '\nmy_extras=%s'%extras

    Adult_Toggle(adult_list=adult_addons,disable=True)
    success   = False
    lock_user = False
# Optionally lock to username
    if YesNo_Dialog( String(30524),String(30525)%username ):
        lock_user = True
    
# Optionally add a password
    if YesNo_Dialog( String(30522),String(30523) ):
        mypass = ''
        while mypass == '':
            mypass      = Update_Password(header=String(30002),text=String(30375),retry_header=String(30371),retry_msg=String(30372),return_pass=True)
        mypass      = md5_check(src=mypass,string=True)
        start_code  =  "pass_md5='%s'\n"%mypass
        start_code  += "mypass=md5_check(Keyboard(String(30373)),True)\n"
        start_code  += "if pass_md5!=mypass:\n"
        start_code  += "    OK_Dialog(String(30000),String(30001))\n"
        start_code  += "    sys.exit()\n"
        my_addons   = start_code+my_addons

# Upload the keyword
    OK_Dialog('[COLOR=gold]%s[/COLOR]'%String(30189),String(30526))
    while not success:
        keyword_name = Keyboard(String(30517))
        if lock_user:
            keyword_name = username+'~split~'+keyword_name

        url          = BASE+'boxer/Create_Keyword.php'
        params       = {"x":encryptme('e',URL_Params()),"b":encryptme('e',my_addons),"n":encryptme('e',username),"p":password,"c":encryptme('e',keyword_name),"e":email}
        response     = Open_URL(url=url,payload=params,post_type='post')
        try:
            exec( encryptme('d',response) )
        except:
            OK_Dialog(String(30131),String(30132))
#---------------------------------------------------------------------------------------------------
# Return paths of selected addon_data folders
def Create_Keyword_Addon_Data(addons=[skin]):
    tbs_raw = Text_File(os.path.join(TBSDATA,'settings.xml'),'r')
    tbs_data = '<settings>'
    for line in tbs_raw.splitlines():
        if 'HOME_' in line:
            tbs_data += '\n'+line
    tbs_data += '\n</settings>'
    settings_array = [ ['plugin.program.tbs',tbs_data] ]
    exclude = ['plugin.program.tbs','script.openwindow']
    folders = Get_Contents(path=ADDON_DATA,exclude_list=exclude)
    for item in folders:
        addon_name = os.path.basename(item)
        if addon_name in addons:
            item = os.path.join(item,'settings.xml')
            if os.path.exists(item):
                contents = Text_File(item,'r')
                settings_array.append([addon_name,contents])
    return settings_array
#---------------------------------------------------------------------------------------------------
# Return paths of selected addon_data folders
def Create_Skin_Shortcut_Data():
    settings_array = []
    exclude        = ['plugin.program.tbs','script.openwindow']
    shortcuts_path = os.path.join(ADDON_DATA,'script.skinshortcuts')
    folders        = Get_Contents(path=shortcuts_path,folders=False,full_path=True)

    for item in folders:
        if item.endswith('DATA.xml'):
            shortcut = End_Path(item)
            contents = Text_File(item,'r')
            settings_array.append([shortcut,contents])
    return settings_array
#---------------------------------------------------------------------------------------------------
# Fully remove an account from the server
def Delete_Account():
    email          = Addon_Setting('email')
    username       = Addon_Setting('username')
    password       = Addon_Setting('password')
    if YesNo_Dialog( '[COLOR=gold]%s[/COLOR]'%String(30530),String(30531) ):
        if YesNo_Dialog( '[COLOR=gold]%s[/COLOR]'%String(30532),String(30533)%(username,email),yes=String(30042),no=String(30041) ):
            url        = BASE+'boxer/Delete_Account.php'
            params     = {"x":encryptme('e',URL_Params()),"n":encryptme('e',username),"p":password,"e":encryptme('e',email)}
            response   = Open_URL(url=url,payload=params,post_type='post')
            try:
                exec( encryptme('d',response) )
            except:
                OK_Dialog(String(30131),String(30132))
#---------------------------------------------------------------------------------------------------
# Delete a keyword from server
def Delete_Keyword():
    email        = encryptme( 'e',Addon_Setting('email') )
    username     = encryptme( 'e',Addon_Setting('username') )
    password     = Addon_Setting('password')
    keyword_name = ''

# List all previously created keywords
    url   = BASE+'boxer/Delete_Keywords.php'
    params    = {"x":encryptme('e',URL_Params()),"n":username,"p":password,"e":email}
    response  = Open_URL(url=url,payload=params,post_type='post')
    try:
        exec( encryptme('d',response) )
    except:
        dolog(Last_Error())
        OK_Dialog(String(30131),String(30132))   

# Remove the relevant keyword from server
    if keyword_name != '':
        url            = BASE+'boxer/Delete_Keyword.php'
        params         = {"x":encryptme('e',URL_Params()),"n":username,"p":password,"c":encryptme('e',keyword_name),"e":email}
        response       = Open_URL(url=url,payload=params,post_type='post')
        try:
            exec( encryptme('d',response) )
        except:
            dolog(Last_Error())
            OK_Dialog(String(30131),String(30132))
#---------------------------------------------------------------------------------------------------
# Function to delete the userdata/addon_data folder
def Delete_Userdata():
    tbs_data    = os.path.join(ADDON_DATA,'plugin.program.tbs')
    ow_data     = os.path.join(ADDON_DATA,'script.openwindow')
    ignore_list = [tbs_data, ow_data]
    Delete_Folders(filepath=ADDON_DATA, ignore=ignore_list)
    zipcheck = xbmc.translatePath(os.path.join(ADDON_DATA,'plugin.program.tbs','zipcheck'))
    if os.path.exists(zipcheck):
        os.remove(zipcheck)
#---------------------------------------------------------------------------------------------------
# Disable the master mode
@route(mode='disable_master')
def Disable_Master():
    ADDON.setSetting('master','false')
    xbmc.executebuiltin('Container.Refresh')
#---------------------------------------------------------------------------------------------------
# Function to pull commands and update
def DLE(command,repo_link,repo_id):
    check1='DLE'
    downloadpath = os.path.join(PACKAGES,'updates.zip')
    if not os.path.exists(PACKAGES):
        os.makedirs(PACKAGES)
    
    if command=='delete':
        shutil.rmtree(xbmc.translatePath(repo_link))
        Refresh(['addons','repos'])
    
    if command=='addons' or command=='ADDON_DATA' or command=='media' or command=='config' or command=='playlists' or command == 'custom':
#        dp.create('Installing Content','','')
        if not os.path.exists(os.path.join(ADDONS,repo_id)) or repo_id == '':
            try:
                Download(repo_link, downloadpath)
            except:
                pass       
        if command=="addons":
            try:
                Extract(downloadpath, ADDONS)
                Refresh(['addons','repos'])
            except:
                pass

        if command=='ADDON_DATA':
            try:
                Extract(downloadpath, ADDON_DATA)
            except:
                dolog("### FAILED TO EXTRACT TO "+ADDON_DATA)
        
        if command=='media':
            try:
                Extract(downloadpath, MEDIA)
            except:
                pass
        
        if command=='config':
            try:
                Extract(downloadpath, CONFIG)
            except:
                pass

        if command=='playlists':
            try:
                Extract(downloadpath, PLAYLISTS)
            except:
                pass

        if command=='custom':
            try:
                Extract(downloadpath, repo_id)
            except:
                dolog("### Failed to extract update "+repo_link)
            
    if os.path.exists(downloadpath):
        try:
            os.remove(downloadpath)
        except:
            pass
#---------------------------------------------------------------------------------------------------
# Enables/disables the social sharing
@route(mode='enable_all_addons')
def Enable_All_Addons():
    if YesNo_Dialog(String(30547),String(30548)):
        Toggle_Addons(new_only=False)
#---------------------------------------------------------------------------------------------------
# Enables/disables the social sharing
@route(mode='enable_shares', args=['share_mode'])
def Enable_Shares(share_mode):
    choice = 1
    if share_mode == 'true':
        if not YesNo_Dialog( String(30049), String(30050) ):
            choice = 0
    if choice:
        ADDON.setSetting('thirdparty', share_mode)
        xbmc.executebuiltin('Container.Refresh')
#---------------------------------------------------------------------------------------------------
def encryptme(mode, message):
    if mode == 'e':
        import random
        count = 0
        finaltext = ''
        while count < 4:
            count += 1
            randomnum = random.randrange(1, 10)
            hexoffset = hex(randomnum)[2:]
            if len(hexoffset)==1:
                hexoffset = '0'+hexoffset
            finaltext = finaltext+hexoffset
        randomchar = random.randrange(1,4)
        if randomchar == 1: finaltext = finaltext+'0A'
        if randomchar == 2: finaltext = finaltext+'04'
        if randomchar == 3: finaltext = finaltext+'06'
        if randomchar == 4: finaltext = finaltext+'08'
        key1    = finaltext[-2:]
        key2    = int(key1,16)
        hexkey  = finaltext[-key2:-(key2-2)]
        key     = -int(hexkey,16)

# enctrypt/decrypt the message
        translated = ''
        finalstring = ''
        for symbol in message:
            num = ord(symbol)
            num2 = int(num) + key
            hexchar = hex(num2)[2:]
            if len(hexchar)==1:
                hexchar = '0'+hexchar
            finalstring = str(finalstring)+str(hexchar)
        return finalstring+finaltext
    else:
        key1    = message[-2:]
        key2    = int(key1,16)
        hexkey  = message[-key2:-(key2-2)]
        key     = int(hexkey,16)
        message = message [:-10]
        messagearray = [message[i:i+2] for i in range(0, len(message), 2)]
        numbers = [ int(x,16)+key for x in messagearray ]
        finalarray = [ str(unichr(x)) for x in numbers ]
        finaltext = ''.join(finalarray)
        return finaltext.encode('utf-8')
#---------------------------------------------------------------------------------------------------
# Function to execute a command
@route(mode='exec_xbmc', args=['command'])
def Exec_XBMC(command):
    xbmc.executebuiltin(command)
    xbmc.executebuiltin('Container.Refresh')
#---------------------------------------------------------------------------------------------------
# Reads contents from a list of special paths and returns in form of a list
def File_Contents(paths=['special://profile/guisettings.xml']):
    settings_array = []
    for item in paths:
        xml_raw = Text_File(xbmc.translatePath(item),'r')
        xml_data = ''
        if xml_raw:
            for line in xml_raw.splitlines():
                xml_data += '\n'+line.rstrip()
            # if xml_data.startswith('\n'):
            #     xml_data = xml_data[1:]
        settings_array.append( [item,xml_data] )
    return settings_array
#---------------------------------------------------------------------------------------------------
# Firmware update
def Firmware_Update(url):
    dl_path = '/tmp/cache/update.zip'
    os.system('mkdir -p /tmp/cache\nmount -t ext4 /dev/cache /tmp/cache\nrm -f /tmp/cache/*.zip')
    dp.create(String(30051),String(30048))
    Download(url,dl_path,dp)
    os.system('mkdir -p /tmp/cache/recovery')
    os.system('echo -e "--update_package=/cache/update.zip\n--wipe_cache" > /tmp/cache/recovery/command || exit 1\numount /tmp/cache\nreboot recovery')
#---------------------------------------------------------------------------------------------------
# Remove the downloaded zip info and re-do social update
@route(mode='force_update')
def Force_Update():
    dolog('FORCE UPDATE')
    if YesNo_Dialog('[COLOR=gold]%s[/COLOR]'%String(30501),String(30544)):
        zip_path = os.path.join(TBSDATA,'zipcheck')
        dolog('zip_path: %s'%zip_path)
        if os.path.exists(zip_path):
            os.remove(zip_path)
        Get_Updates()
#---------------------------------------------------------------------------------------------------
# Clean up all known cache files
def Friend_Options(my_array=[]):
    username  = encryptme("e",Addon_Setting("username"))
    email     = encryptme("e",Addon_Setting("email"))
    password  = Addon_Setting("password")
    urlparams = encryptme("e",URL_Params())
    if my_array[1] == 'pending':
        if my_array[2]=='sent':
            choice = YesNo_Dialog( String(30474),String(30476) )
            if choice:
                dolog(BASE+"boxer/User_Revoke_Request.php?x=%s&n=%s&e=%s&p=%s&f=%s&i=%s"%( urlparams,username,email,password,encryptme('e',my_array[0]),encryptme('e',str(my_array[3]))))
                Sleep_If_Function_Active( Run_Code, ["boxer/User_Revoke_Request.php", {"x":urlparams,"n":username,"e":email,"p":password,"f":encryptme('e',my_array[0]),"i":encryptme('e',str(my_array[3]))}] )
            else:
                My_Friends()
        else:
            Sleep_If_Function_Active( Run_Code, ["boxer/User_Accept_Request.php", {"x":urlparams,"n":username,"e":email,"p":password,"f":encryptme('e',my_array[0]),"i":encryptme('e',str(my_array[3]))}] )
    elif my_array[1] == 'friend':
        my_options = [String(30495),'[COLOR=red]%s[/COLOR] %s'%( String(30468),username )]
        choice = Select_Dialog('[COLOR=cyan]%s[/COLOR]'%username,my_options)
        if choice == 0:
            Send_To_Friend(username)
        elif choice == 1:
            OK_Dialog('COMING SOON','Our development team are currently working on this section.')
        else:
            My_Profile()
#---------------------------------------------------------------------------------------------------
# Clean up all known cache files
@route(mode='full_clean')
def Full_Clean():
    size                      = 0
    atv2_cache_a              = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
    atv2_cache_b              = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')        
    downloader_cache_path     = os.path.join(xbmc.translatePath('special://profile/addon_data/script.module.simple.downloader'), '')
    imageslideshow_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/script.image.music.slideshow/cache'), '')
    iplayer_cache_path        = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.iplayer/iplayer_http_cache'), '')
    itv_cache_path            = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.itv/Images'), '')
    navix_cache_path          = os.path.join(xbmc.translatePath('special://profile/addon_data/script.navi-x/cache'), '')
    phoenix_cache_path        = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.phstreams/Cache'), '')
    ramfm_cache_path          = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.audio.ramfm/cache'), '')
    wtf_cache_path            = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.whatthefurk/cache'), '')
    genesisCache              = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.genesis'), 'cache.db')
    tempdir                   = os.path.join(HOME,'temp')
    dp.create(String(30052),'',String(30048),'')

# For more accurate info we need to add a loop to only check folders with cache in the name. Actual wipe does this but getsize does not.
    if os.path.exists(atv2_cache_a):
        size += Folder_Size(atv2_cache_a,'b')
    if os.path.exists(atv2_cache_b):
        size += Folder_Size(atv2_cache_b,'b')
    if os.path.exists(downloader_cache_path):
        size += Folder_Size(downloader_cache_path,'b')
    if os.path.exists(imageslideshow_cache_path):
        size += Folder_Size(imageslideshow_cache_path,'b')
    if os.path.exists(iplayer_cache_path):
        size += Folder_Size(iplayer_cache_path,'b')
    if os.path.exists(itv_cache_path):
        size += Folder_Size(itv_cache_path,'b')
    if os.path.exists(navix_cache_path):
        size += Folder_Size(navix_cache_path,'b')
    if os.path.exists(phoenix_cache_path):
        size += Folder_Size(phoenix_cache_path,'b')
    if os.path.exists(ramfm_cache_path):
        size += Folder_Size(ramfm_cache_path,'b')
    if os.path.exists(wtf_cache_path):
        size += Folder_Size(wtf_cache_path,'b')
    if os.path.exists(genesisCache):
        size += Folder_Size(genesisCache,'b')
    if os.path.exists(tempdir):
        size += Folder_Size(tempdir,'b')
    size += Folder_Size(THUMBNAILS,'b')
    size += Folder_Size(PACKAGES,'b')
    size = "%.2f" % (float(size / 1024) / 1024)
    choice = YesNo_Dialog(String(30053),String(30054)%size)
    if choice == 1:
        Wipe_Cache()
        try:
            shutil.rmtree(PACKAGES)
        except:
            pass
        choice = YesNo_Dialog(String(30055),String(30056),yes=String(30057),no=String(30058))
        if choice == 1:
            Remove_Textures()
            Delete_Folders(THUMBNAILS)
            Force_Close()
        else:
            Cleanup_Textures()
#---------------------------------------------------------------------------------------------------
# Return mac address, not currently checked on Mac OS
def Get_Mac(protocol):
    cont    = 0
    counter = 0
    mac     = ''
    while mac == '' and counter < 5: 
        if sys.platform == 'win32': 
            mac = ''
            for line in os.popen("ipconfig /all"):
                if protocol == 'wifi':
                    if line.startswith('Wireless LAN adapter Wi'):
                        cont = 1
                    if line.lstrip().startswith('Physical Address') and cont == 1:
                        mac = line.split(':')[1].strip().replace('-',':').replace(' ','')
                        if len(mac) == 17:
                            break
                        else:
                            mac = ''
                            counter += 1

                else:
                    if line.lstrip().startswith('Physical Address'): 
                        mac = line.split(':')[1].strip().replace('-',':').replace(' ','')
                        if len(mac) == 17:
                            break
                        else:
                            mac = ''
                            counter += 1

        elif sys.platform == 'darwin': 
            mac = ''
            if protocol == 'wifi':
                for line in os.popen("ifconfig en0 | grep ether"):
                    if line.lstrip().startswith('ether'):
                        mac = line.split('ether')[1].strip().replace('-',':').replace(' ','')
                        dolog('(count: %s) (len: %s) wifi: %s' % (counter, len(mac), mac))
                        if len(mac) == 17:
                            break
                        else:
                            mac = ''
                            counter += 1

            else:
                for line in os.popen("ifconfig en1 | grep ether"):
                    if line.lstrip().startswith('ether'):
                        mac = line.split('ether')[1].strip().replace('-',':').replace(' ','')
                        dolog('(count: %s) (len: %s) ethernet: %s' % (counter, len(mac), mac))
                        if len(mac) == 17:
                            break
                        else:
                            mac = ''
                            counter += 1

        elif xbmc.getCondVisibility('System.Platform.Android'):
            mac = ''
            if os.path.exists('/sys/class/net/wlan0/address') and protocol == 'wifi':
                readfile = open('/sys/class/net/wlan0/address', mode='r')
            if os.path.exists('/sys/class/net/eth0/address') and protocol != 'wifi':
                readfile = open('/sys/class/net/eth0/address', mode='r')
            mac = readfile.read()
            readfile.close()
            try:
                mac = mac.replace(' ','')
                mac = mac[:17]
            except:
                mac = ''
                counter += 1

        else:
            if protocol == 'wifi':
                for line in os.popen("/sbin/ifconfig"): 
                    if line.find('wlan0') > -1: 
                        mac = line.split()[4]
                        if len(mac) == 17:
                            break
                        else:
                            mac = ''
                            counter += 1

            else:
               for line in os.popen("/sbin/ifconfig"): 
                    if line.find('eth0') > -1: 
                        mac = line.split()[4] 
                        if len(mac) == 17:
                            break
                        else:
                            mac = ''
                            counter += 1
    if mac == '':
        dolog('Unknown mac')
        mac = 'Unknown'

    return str(mac)
#---------------------------------------------------------------------------------------------------
# Run the social update command and optionally show a busy working symbol until finished
@route(mode='get_updates', args=['url'])
def Get_Updates(url=True):
    if url:
        Show_Busy(True)
    Sleep_If_Function_Active( Grab_Updates, [BASE+'boxer/comm_live.php?multi&z=c&x=','ignoreplayer'], kill_time=600)
    # if url:
    #     Show_Busy(False)
#---------------------------------------------------------------------------------------------------
# Grab current playing video details
@route(mode='get_video')
def Get_Video():
    OK_Dialog( String(30498),String(30499) )
    isplaying = xbmc.Player().isPlaying()
    counter_array = [10,20,30,40,50,60]
    counter = 60
    while not isplaying and counter != 0:
        xbmc.sleep(1000)
        counter += -1
        if counter in counter_array:
            Notify(String(30496),String(30497)%counter,'4000','Video.png')
        isplaying = xbmc.Player().isPlaying()
    if isplaying:
        currentvid = xbmc.Player().getPlayingFile()
        vid_title   = ''
        title_count = 0
        while vid_title == '' and title_count < 10:
            vid_title  = xbmc.getInfoLabel('Player.Title')
            xbmc.sleep(100)
            title_count += 1

        xbmc.log('CURRENT VID: %s'%currentvid,2)
        xbmc.log('CURRENT TITLE: %s'%vid_title,2)
        xbmc.Player().stop()
        Notify('PLEASE WAIT','Checking Link','10000','Video.png')
        Show_Busy(True)
        xbmc.Player().play(currentvid)
        xbmc.sleep(11000)
        isplaying = xbmc.Player().isPlaying()
        if isplaying:
            if Check_Playback():
                xbmc.Player().stop()
                xbmc.sleep(1000)
                active_plugin  = System(command='addonid')
                plugin_path    = System(command='currentpath')
                if not os.path.exists(currentvid):
                    OK_Dialog('SUCCESS','Playback was successful:\n%s'%vid_title)
                else:
                    OK_Dialog('INVALID VIDEO','You can only share online streams. If you want to share a local file you may want to consider uploading via a file sharing add-on such as GDrive.')
                    return False
                dolog('STREAM: '+currentvid)
                dolog('PLUGIN PATH: '+plugin_path)
                dolog('PLUGIN: '+active_plugin)
            else:
                OK_Dialog('FAILED','Playback was unsuccessful')
        else:
            OK_Dialog('FAILED','Playback was unsuccessful')
        Show_Busy(False)

    else:
        OK_Dialog('FAILED','Playback was unsuccessful')
#---------------------------------------------------------------------------------------------------
# Run social update command to check for any updates
@route(mode='grab_updates', args=['url','runtype'])
def Grab_Updates(url, runtype = ''):
    dolog('GRAB_UPDATES - URL: %s'%url)
    dolog('GRAB_UPDATES - RUNTYPE: %s'%runtype)
    if runtype != 'ignoreplayer':
        isplaying = xbmc.Player().isPlaying()
        while isplaying:
            xbmc.sleep(1000)
            isplaying = xbmc.Player().isPlaying()

    urlparams   = URL_Params()
    mysuccess   = 0
    failed      = 0
    counter     = 0
    changetimer = 0
    multi       = 0
    previous    = ''

    if urlparams != 'Unknown':
        dolog('### CHECKING MAIN MENU DEFAULTS')
        Main_Menu_Defaults()
        if url == BASE+'boxer/comm_live.php?multi&z=c&x=':
            multi = 1
            url=url.replace('multi&','')
        if url == BASE+'boxer/comm_live.php?update&z=c&x=':
            Notify(String(30059),String(30007),'1000',os.path.join(ADDONS,'script.openwindow','resources','images','update_software.png'))
            url=url.replace('update&','')
        url,params = url.split('?')
        dolog('### MAIN MENU DEFAULTS RUN MOVING ON')
        while mysuccess != 1 and failed != 1:

            # try:
            dolog("### URL: "+url+'?'+encryptme('e',urlparams))
            link = Open_URL(url=url,post_type='post',payload={"x":encryptme('e',urlparams),"z":"c"})
            if link != '' and not 'sleep' in link:
                link = encryptme('d',link).replace('\n',';').replace('|_|',' ').replace('|!|','\n').replace('http://venztech.com/repo_jpegs/',BASE+'repo_jpegs/')
            try:
                dolog("### Return: "+link)
            except:
                pass

            if link == '':
                dolog("### Blank page returned")
                counter += 1
                if counter == 3:
                    failed = 1

# Check that no body tag exists, if it does then we know TLBB is offline
            if not '<body' in link and link != '':
                linematch  = re.compile('com(.+?)="').findall(link)
                commline   = linematch[0] if (len(linematch) > 0) else ''
                commatch   = re.compile('="(.+?)endcom"').findall(link)
                command    = commatch[0] if (len(commatch) > 0) else 'End'
            
                SF_match   = re.compile('<favourite[\s\S]*?</favourite>').findall(command)
                SF_command = SF_match[0] if (len(SF_match) > 0) else 'None'

# Create array of commands so we can check if the install video needs to be played
                previous += command
                dolog("### command: "+command)
                dolog("### SF_command: "+SF_command)

                Open_URL( post_type='post',url=BASE+'boxer/comm_live.php',payload={"x":encryptme('e',urlparams),"y":commline} )
                dolog("### COMMAND *CLEANED: "+command.replace('|#|',';'))
                dolog("### LINK *ORIG: "+link)
                if SF_command!='None':
                    Text_File(PROGRESS_TEMP, 'w', SF_command)

                elif command!='End' and not 'sleep' in link:
                    if ';' in command:
                        dolog(command)
                        newcommands = command.split(';')
                        for item in newcommands:
                            if 'branding/install.mp4' in item:
                                item = ''

                            if 'extract.all' in item:
                                try:
                                    item = item.replace('extract.all','Extract')
                                    exec item
                                    if os.path.exists(os.path.join(PACKAGES,'updates.zip')):
                                        os.remove(os.path.join(PACKAGES,'updates.zip'))
                                except:
                                    dolog(Last_Error())
                            else:
                                try:
                                    if 'Dialog().ok(' in item:
                                        xbmc.sleep(1000)
                                        while xbmc.Player().isPlaying():
                                            xbmc.sleep(500)
                                    exec item.replace('|#|',';') # Change to semicolon for user agent otherwise it splits into a new command
                                    dolog("### RUNNING ITEM: "+item.replace('|#|',';'))
                                except:
                                    dolog("### Failed with item: "+item.replace('|#|',';'))
                                    dolog(Last_Error())
                    else:
                        try:
                            if 'Dialog().ok(' in command:
                                if not multi:
                                    xbmc.sleep(1000)
                                    dolog("### OK_Dialog in this command, checking if xbmc is playing....")
                                    while xbmc.Player().isPlaying():
                                        xbmc.sleep(500)
                                else: command = ''

                            if 'extract.all' in command:
                                try:
                                    command = command.replace('extract.all','Extract')
                                    exec command
                                    if os.path.exists(os.path.join(PACKAGES,'updates.zip')):
                                        os.remove(os.path.join(PACKAGES,'updates.zip'))
                                except:
                                    dolog("### Failed with command: "+command.replace('|#|',';'))
                                    dolog(Last_Error())

                            if 'branding/install.mp4' in command:
                                command = ''

                            else:
                                exec command.replace('|#|',';') # Change to semicolon for user agent otherwise it splits into a new command
                                dolog("### RUNNING COMMAND: "+item.replace('|#|',';'))
                        except:
                            dolog("### Failed with command: "+command.replace('|#|',';'))
                    previous = ''
                    if os.path.exists(PROGRESS_TEMP):
                        os.remove(PROGRESS_TEMP)
                    
                elif command=='End':
                    if 'sleep' in link:
                        content=Text_File(SLEEPER, 'r')
                        if content != "sleep=STOPALL":
                            sleep = str(link[6:])
                        else:
                            sleep = "23:59:59"
                            dolog("### SLEEP MODE - SERVER MAINTENANCE")
                        if str(sleep) != str(content):
                            Text_File(SLEEPER, 'w',sleep)
                            dolog("### Changed timer to "+sleep)
                            changetimer = 1
                        else:
                            dolog("### Timer same, no changes required")
                    if sleep != '23:59:59':
                        Refresh(['addons','repos'])
                        mysuccess = 1
            # except:
            #     dolog("### Failed with update command: "+Last_Error())
            #     failed = 1

        if changetimer == 1:
            dolog('### TBS GRAB UPDATES - TIMER CHANGED, STOPPING/RUNNING SERVICE')
            xbmc.executebuiltin('StopScript(special://home/addons/plugin.program.tbs/service.py)')
            xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.tbs/service.py)')

    dolog('### TBS GRAB UPDATES - RUNNING FUNCTIONS')
    if os.path.exists( xbmc.translatePath('special://home/addons/script.openwindow/functions.py') ):
        xbmc.executebuiltin('RunScript(special://home/addons/script.openwindow/functions.py,%s)'%runtype)
    elif os.path.exists( xbmc.translatePath('special://xbmc/addons/script.openwindow/functions.py') ):
        xbmc.executebuiltin('RunScript(special://xbmc/addons/script.openwindow/functions.py,%s)'%runtype)
    Sync_Settings()
    Remove_Files()
    dolog('### TBS_RUNNING: %s'%xbmcgui.Window(10000).getProperty('TBS_Running'))
    if runtype != 'silent':
        counter = 2
        updates_running = 'true'
        while updates_running == 'true':
            xbmc.sleep(2000)
            updates_running = xbmcgui.Window(10000).getProperty('TBS_Running')
            dolog('### TBS_RUNNING: %ss'%counter)
            counter += 2
        Notify(String(30330),String(30331),'1000',os.path.join(ADDONS,'plugin.program.tbs','resources','tick.png'))
#---------------------------------------------------------------------------------------------------
# Hide passwords in addon settings
@route(mode='hide_passwords')
def Hide_Passwords():
    if YesNo_Dialog(String(30094), String(30095)):
        for root, dirs, files in os.walk(ADDONS):
            for f in files:
                if f =='settings.xml':
                    FILE=open(os.path.join(root, f)).read()
                    match=re.compile('<setting id=(.+?)>').findall (FILE)
                    for LINE in match:
                        if 'pass' in LINE:
                            if not 'option="hidden"' in LINE:
                                try:
                                    CHANGEME=LINE.replace('/',' option="hidden"/') 
                                    f = open(os.path.join(root, f), mode='w')
                                    f.write(str(FILE).replace(LINE,CHANGEME))
                                    f.close()
                                except:
                                    pass
        OK_Dialog(String(30096), String(30097)) 
#---------------------------------------------------------------------------------------------------
# Loop through a list of add-ons and install them
def Install_Addons(url):
    failed_array = []
    repo_list    = {}
    xbmc_gui     = Requirements('xbmc.gui')
    xbmc_python  = Requirements('xbmc.python')
    gui_min      = encryptme('e',xbmc_gui['min'])
    gui_max      = encryptme('e',xbmc_gui['max'])
    python_min   = encryptme('e',xbmc_python['min'])
    python_max   = encryptme('e',xbmc_python['max'])

    try:
        mycode       = Open_URL(url=binascii.unhexlify(BASE2)+'boxer/addoninstall.php',post_type='post',payload={"a":url,"v":encryptme('e',XBMC_VERSION),'guimin':gui_min,'guimax':gui_max,'pymin':python_min,'pymax':python_max,'ignore':'false'})
        my_download  = ''
        url_clean    = encryptme('d',url)
        exec(mycode)
    except:
        mycode       = Open_URL(url=BASE+'boxer/masterscripts/addoninstall.php',post_type='post',payload={"a":url,"v":encryptme('e',XBMC_VERSION),'guimin':gui_min,'guimax':gui_max,'pymin':python_min,'pymax':python_max,'ignore':'false'})
        my_download  = ''
        url_clean    = encryptme('d',url)
        exec(mycode)

    if len(repo_list) > 0 and not ',' in url_clean:
        my_download = download_array[url_clean]
    if len(my_download) > 0 or ',' in url_clean:
        Show_Busy()
        for key in repo_list:

# If the addon does not already exist on system or is in adult_store then try to install
            if not (xbmc.getCondVisibility('System.HasAddon(%s)'%key)) and (not os.path.exists(os.path.join(adult_store,key))):
                dolog('INSTALLING ADDON: %s'%key)
                temp_zip = os.path.join(PACKAGES,key+'.zip')
                official_repo = repo_list[key]
                downloads     = download_array[key]
                try:
                    Sleep_If_Function_Active(function=Download,args=[downloads[official_repo],temp_zip],show_busy=False,kill_time=180)
                    repoexists = True
                except:
                    dolog('Failed to download from official repo')
                    repoexists = False
                if os.path.exists(temp_zip) and zipfile.is_zipfile(temp_zip) and repoexists:
                    dolog('%s Download Complete: %s'%(key,downloads[official_repo]))

# If download from official repo failed we try alternative sources (highest versions first)
                else:
                    success  = False
                    backup   = downloads.items()
                    new_list = []
                    for item in backup:
                        new_list.append(item[1])
                    while not success and len(new_list) != 0:
                        highest_repo = Highest_Version(new_list,'-','.zip')
                        if highest_repo != '':
                            try:
                                Sleep_If_Function_Active(function=Download,args=[highest_repo,temp_zip],show_busy=False,kill_time=180)
                            except:
                                dolog('Failed to download from: %s'%highest_repo)
                            if os.path.exists(temp_zip) and zipfile.is_zipfile(temp_zip):
                                dolog('%s Download Complete: %s'%(key,highest_repo))
                                success = True
                            else:
                                new_list.remove(highest_repo)
                    if not success and len(new_list) == 0:
                        failed_array.append(key)
                if os.path.exists(temp_zip) and zipfile.is_zipfile(temp_zip):
                    Sleep_If_Function_Active(function=Extract,args=[temp_zip,ADDONS],show_busy=False,kill_time=180)
        
        dolog('### ENABLING ADDONS')
        # Sleep_If_Function_Active(function=Toggle_Addons,show_busy=False)
        Toggle_Addons()
        Show_Busy(False)
        # Adult_Toggle(adult_list=adult_addons,disable=True)
    else:
        OK_Dialog(String(30513),String(30514)%encryptme('d',url))
    if len(failed_array) == 0:
        return 'success'
    else:
        return failed_array
#---------------------------------------------------------------------------------------------------
# Menu to install content via the TR add-on
@route(mode='install_content')
def Install_Content():
    if Addon_Setting('master') == 'true':
        Add_Dir(String(30098),'','disable_master',False,'','','')
    if Addon_Setting('userid') != '':
        Add_Dir(String(30099) % encryptme('d',userid),'','change_id',False,'','','')
    Add_Dir(String(30100),'', 'get_updates',False,'','','')
    Add_Dir(String(30101),'','keywords',False,'Keywords.png','','')
    Add_Dir(String(30102),'','install_from_zip',False,'','','')
    Add_Dir(String(30103),'','browse_repos',False,'','','')
#---------------------------------------------------------------------------------------------------
# Browse pre-installed repo's via the kodi add-on browser
@route(mode='install_from_zip')
def Install_From_Zip():
    xbmc.executebuiltin('ActivateWindow(10040,"addons://install/",return)')
#---------------------------------------------------------------------------------------------------
# Install a keyword
@route(mode='keywords')
def Install_Keyword():
    email       = encryptme( 'e',Addon_Setting('email') )
    username    = Addon_Setting('username')
    password    = Addon_Setting('password')
    choice      = False
    
    if username == '':
        Register_Device()
        return
    else:
        choice = YesNo_Dialog('[COLOR=gold]%s[/COLOR]'%String(30101),String(30535))

# List all previously created keywords
    if choice:
        url   = BASE+'boxer/My_Keywords.php'
        params    = {"x":encryptme('e',URL_Params()),"n":encryptme('e',username),"p":password,"e":email}
        response  = Open_URL(url=url,payload=params,post_type='post')
        try:
            exec( encryptme('d',response) )
        except:
            dolog(Last_Error())
            OK_Dialog(String(30131),String(30132))   

# Allow custom keyword to be entered
    else:
        keyword_name   = Keyboard('[COLOR=gold]%s[/COLOR]'%String(30517))
    
    username = encryptme('e',username)
    if keyword_name != '':
        url            = BASE+'boxer/Install_Keyword_new.php'
        params         = {"x":encryptme('e',URL_Params()),"n":username,"p":password,"c":encryptme('e',keyword_name),"e":email}
        response       = Open_URL(url=url,payload=params,post_type='post')
        try:
            exec( encryptme('d',response) )
        except:
            dolog(Last_Error())
            OK_Dialog(String(30131),String(30132))
#---------------------------------------------------------------------------------------------------
# Show final results for installing (if multiple shares of same name order by popularity)
def Install_Repos(to_install):
    email       = encryptme( 'e',Addon_Setting('email') )
    username    = encryptme( 'e',Addon_Setting('username') )
    password    = Addon_Setting('password')
    addon_list  = ''

# Check addons 
    for item in to_install:
        addon_installed = xbmc.getCondVisibility('System.HasAddon(%s)'%item)
        adult_exists    = os.path.exists( os.path.join(adult_store,item) )
        path_exists     = os.path.exists( os.path.join(ADDONS,item) )
        if not addon_installed and not path_exists and not adult_exists:
            addon_list += item+','
    if addon_list != '':
        url       = BASE+'boxer/Install_Repos.php'
        params    = {"x":encryptme('e',URL_Params()),"n":username,"p":password,"c":encryptme('e',addon_list),"e":email}
        response  = Open_URL(url=url,payload=params,post_type='post')
        try:
            exec( encryptme('d',response) )
        except:
            dolog(Last_Error())
            OK_Dialog(String(30131),String(30132))
#---------------------------------------------------------------------------------------------------
# Show final results for installing (if multiple shares of same name order by popularity)
def Install_Shares(function, menutype, menu, choices, contentarray = '', imagearray = '', descarray = ''):
        shares_contentarray = []
        shares_imagearray   = []
        shares_descarray    = []
        shares_contenturl   = []
        urlparams           = URL_Params()

# HAD TO REVERT BACK TO OLD OPEN_URL2 METHOD FOR THIS FUNCTION, SOMETHING CURRENTLY OFF WITH PYTHON KODING REQUESTS METHOD

#    try:
        for item in choices:
            xbmc.log('CHOICE: %s' % item)
            if debug == 'true':
                xbmc.log(BASE+'boxer/cat_search_live.php?x=%s' % (encryptme('e','%s&%s&1&%s&%s' % (urlparams, function, social_shares, contentarray[item]))))
            sharelist_URL  = BASE+'boxer/cat_search_live.php?x=%s' % (encryptme('e','%s&%s&1&%s&%s' % (urlparams, function, social_shares, contentarray[item])))
            content_list   = Open_URL2(sharelist_URL)
            clean_link     = encryptme('d',content_list)
            if debug == 'true':
                xbmc.log('#### %s' % clean_link)

# Grab all the shares which match the master sub-category
            match = re.compile('n="(.+?)"t="(.+?)"d="(.+?)"l="(.+?)"', re.DOTALL).findall(clean_link)
            for name, thumb, desc, link in match:
                shares_contentarray.append(name)
                shares_imagearray.append(thumb)
                shares_descarray.append(desc)
                shares_contenturl.append(link)

# If we have more than one item in the list we present them so the user can select which one they want installed
            if len(shares_contentarray) > 1:
                choice = dialog.select('Select share for [COLOR=dodgerblue]%s[/COLOR]' % contentarray[item].replace('ADD ',''), shares_contentarray)
                install_share = shares_contenturl[choice]

            else:
                install_share = shares_contenturl[0]

# Remove any matching menu items previously installed from different boxes
            if len(shares_contentarray)>0:
                for item in shares_contentarray:
                    xbmc.log('### Removing any old instances of %s' % item)
                    if item.startswith('Add'):
                        item         = 'Remove'+item[3:]
                    change_text  = re.compile(' to the (.+?)Menu').findall(item)[0]
                    if change_text.endswith(' '):
                        change_text = change_text[:-1]
                    item         = item.replace(' to the %s' % change_text, '%'+' from the %s' % change_text)
                    if 'by box' in item:
                        change_text2 = re.compile('by box (.+?)from').findall(item)[0]
                        xbmc.log('by box: %s' % change_text2)
                        item         = item.replace(change_text2, '%')
                    Remove_Menu('from_the_%s_menu' % change_text.lower().replace(' ', '_'), item)
#            content_list   = Open_URL2(sharelist_URL)

                Open_URL2(install_share)

# Clean the arrays so they don't show old data
            del shares_contentarray[:]
            del shares_imagearray[:]
            del shares_descarray[:]
            del shares_contenturl[:]
            del match[:]
        xbmc.executebuiltin('ActivateWindow(HOME)')
        Get_Updates()
#---------------------------------------------------------------------------------------------------
# Function to grab the main sub-categories 
@route(mode='install_venz_menu', args=['url'])
def Install_Venz_Menu(url):
    menutype    = ''
    menu        = ''
    if '||' in url:
        url,menutype,menu = url.split('||')
    menu = menu.replace('_',' ').lower()

    urlparams  = URL_Params()
    if urlparams != 'Unknown':
        try:

# Inititalise the arrays for sending to multi-select window
            contentarray = []
            imagearray   = []
            descarray    = []
            contenturl   = []

# Add an item to one of the main menu categories or add a sub-menu item
            if menutype == 'add_main' or menutype == 'add_sub' or url.startswith('manualsearch'):
                categoryURL  = BASE+'boxer/cat_search_live.php'
                dolog(categoryURL)
                link_orig  = Open_URL(url=categoryURL,post_type='post',payload={"x":encryptme('e','%s&%s&0&%s' % (urlparams, url, social_shares))})
                link       = encryptme('d',link_orig)
                dolog('#### '+encryptme('d',link_orig))
            
                match  = re.compile('n="(.+?)"t="(.+?)"d="(.+?)"', re.DOTALL).findall(link)
                for name, thumb, desc in match:
                    contentarray.append(name)
                    imagearray.append(thumb)
                    descarray.append(desc)

                if len(contentarray)>0:
                    choices = multiselect(String(30078), contentarray, imagearray, descarray)
                    xbmc.executebuiltin('ActivateWindow(HOME)')
                    dolog('Choices: %s' % choices)
                    if len(choices) > 0:
                        Install_Shares(url, menutype, menu, choices, contentarray, imagearray, descarray)
                else:
                    if thirdparty == 'true':
                        OK_Dialog(String(30079),String(30080))
                    else:
                        OK_Dialog(String(30079),String(30081))


# If this is a remove item
            else:
                Remove_Menu(url)
        except:
            Notify(String(30082),String(30083),'1000',os.path.join(ADDONS,'plugin.program.tbs','resources','cross.png'))
    else:
        OK_Dialog(String(30084), String(30085))    
#---------------------------------------------------------------------------------------------------
# Return details about the IP address lookup       
@route(mode='ip_check')
def IP_Check():
    ip_site = Addon_Setting('ip_site')
    try:
        if ip_site == "whatismyipaddress.com":
           BaseURL       = 'http://whatismyipaddress.com/'
           link          = Open_URL(BaseURL).replace('\n','').replace('\r','')
           if not 'Access Denied' in link:
               ipmatch = Find_In_Text(content=link,start='http://whatismyipaddress.com/ip/',end='"')
               ipfinal = ipmatch[0] if (len(ipmatch) > 0) else 'Unknown'
               details = Find_In_Text(content=link,start='style="font-size:14px;">',end='</td>')
               isp     = details[0]
               details.pop(0)
               location = ",".join(details)
               dolog('ISP: %s'%isp)
               dolog('location: %s'%location)
               OK_Dialog('www.whatismyipaddress.com',String(30386)%ipfinal+'\n'+String(30387)%isp+'\n'+String(30388)%location)
        else:
            BaseURL       = 'https://www.iplocation.net/find-ip-address'
            link          = Open_URL(BaseURL).replace('\n','').replace('\r','')
            segment       = Find_In_Text(content=link,start='<table class="iptable">',end='<\/table>')
            segment       = segment[0] if (len(segment) > 0) else 'Unknown'
            ipmatch       = Find_In_Text(content=segment,start='font-weight: bold;">',end='<\/span>')
            ipfinal       = ipmatch[0] if (len(ipmatch) > 0) else 'Unknown'
            providermatch = Find_In_Text(content=segment,start='Host Name<\/th><td>',end='<\/td>')
            isp           = providermatch[0] if (len(providermatch) > 0) else 'Unknown'
            locationmatch = Find_In_Text(content=segment,start='IP Location<\/th><td>',end='&nbsp;')
            location      = locationmatch[0] if (len(locationmatch) > 0) else 'Unknown'
            OK_Dialog('www.iplocation.net',String(30386)%ipfinal+'\n'+String(30387)%isp+'\n'+String(30388)%location)
    except:
        OK_Dialog(String(30104), String(30105))
#---------------------------------------------------------------------------------------------------
# Return details of a full keyword backup (addons,addon_data,faves,sources,guisettings)
@route(mode='kw_full')
def Keyword_Full_Backup():
    id_array       = []
    my_addons      = []
    skiparray      = ['plugin.program.super.favourites','plugin.program.tbs','script.openwindow','script.trtv','script.qlickplay','plugin.video.metalliq']
    content_list   = ['special://profile/guisettings.xml','special://profile/favourites.xml','special://profile/sources.xml','special://profile/addon_data/plugin.video.addons.ini.creator/.storage/folders']
    redirect_list  = Get_Contents(path=REDIRECTS,folders=False,full_path=False)
    content_list  += ['special://profile/addon_data/plugin.program.tbs/redirects/' + s for s in redirect_list]

    my_addons =  Installed_Addons(content='video')
    my_addons += Installed_Addons(content='audio')
    my_addons += Installed_Addons(content='image')
    my_addons += Installed_Addons(content='executable')

    for item in my_addons:
        item = item["addonid"].encode('utf-8')
        if not item in skiparray and not item in id_array:
            id_array.append(item)

    my_addons      = 'my_addons=%s\n'%id_array
    my_addons     += '\nmy_settings=%s'%Create_Keyword_Addon_Data()
    my_addons     += '\nskin_shortcuts=%s'%Create_Skin_Shortcut_Data()
    extras         = File_Contents(content_list)
    my_addons     += '\nmy_extras=%s'%extras
    return my_addons
#---------------------------------------------------------------------------------------------------
# Show the various keyword options (create, install & delete)
def Keyword_Options():
    choice = Select_Dialog('[COLOR=gold]%s[/COLOR]'%String(30552),['[COLOR=dodgerblue]%s[/COLOR]'%String(30189),'[COLOR=lime]%s[/COLOR]'%String(30101),'[COLOR=red]%s[/COLOR]'%String(30550)])
    if choice >= 0:
        if choice == 0:
            Create_Keyword()
        if choice == 1:
            Install_Keyword()
        if choice == 2:
            Delete_Keyword()
    else:
        My_Details()
#---------------------------------------------------------------------------------------------------
# Run the force close command
@route(mode='kill_xbmc')
def Kill_XBMC():
    Force_Close()
#---------------------------------------------------------------------------------------------------
# View the log from within Kodi
@route(mode='log')
def Log_Viewer():
    logpath = xbmc.translatePath('special://logpath')
    valid_logfile = Get_Contents(path=logpath,folders=False,filter='.log')
    if len(valid_logfile) >= 1:
        if YesNo_Dialog(String(30118),String(30119),yes=String(30120),no=String(30121)):
            Upload_Log()
        else:
            viewer = [String(30122),String(30123),String(30124),String(30125),String(30126)]
            choice = Select_Dialog(String(30127),viewer)
            if choice == -1: return
            elif choice == 0: content=Grab_Log(formatting='errors')
            elif choice == 1: content=Grab_Log(formatting='warnings_errors')
            elif choice == 2: content=Grab_Log()
            elif choice == 3: content=Grab_Log(sort_order='original')
            elif choice == 4: content=Grab_Log(log_type='old')
            Text_Box(String(30118), content)
            Sleep_If_Window_Active()
    else:
        OK_Dialog(String(30327),String(30328))
#---------------------------------------------------------------------------------------------------
# Set the default main menu items
@route(mode='main_menu_defaults')
def Main_Menu_Defaults():
    urlparams = URL_Params()
    Run_Code(url='boxer/main_menus.php', payload={"x":encryptme('e', urlparams)} )
#---------------------------------------------------------------------------------------------------
# Function to enable/disable the main menu items - added due to glitch on server
@route(mode='main_menu_install', args=['url'])
def Main_Menu_Install(url):
    menu_list = (['Custom6HomeItem.Disable','comedy'],['Custom3HomeItem.Disable','cooking'],['Custom4HomeItem.Disable','fitness'],
    ['Custom5HomeItem.Disable','gaming'],['FavoritesHomeItem.Disable','kids'],['LiveTVHomeItem.Disable','livetv'],
    ['MovieHomeItem.Disable','movies'],['MusicHomeItem.Disable','music'],['ProgramsHomeItem.Disable','news'],
    ['VideosHomeItem.Disable','sports'],['Custom2HomeItem.Disable','technology'],['WeatherHomeItem.Disable','travel'],
    ['TVShowHomeItem.Disable','tvshows'],['PicturesHomeItem.Disable','world'],['ShutdownHomeItem.Disable','youtube'],
    ['MusicVideoHomeItem.Disable','xxx'])

    menu_options = []

    if os.path.exists(MAIN_MENUS):
        main_menu_list = encryptme('d',Text_File(MAIN_MENUS,'r'))
        main_list = eval(main_menu_list)
        dolog(main_menu_list)
        for item in menu_list:
            try:
                exec( '%s = "%s"' % (item[1],main_list[item[1]]) )
                menu_options.append(item[1])
            except:
                dolog(Last_Error())
    else:
        urlparams       = URL_Params()
        menu_options    = Open_URL( post_type='post', url=BASE+'boxer/my_details_live.php', payload={"x":encryptme('e', urlparams),"m":"1"} )
        menu_options    = encryptme('d', menu_options)
        comedy          = String(30061)
        cooking         = String(30077)
        fitness         = String(30062)
        gaming          = String(30063)
        kids            = String(30064)
        livetv          = String(30065)
        movies          = String(30066)
        music           = String(30067)
        news            = String(30068)
        sports          = String(30069)
        system          = String(30550)
        technology      = String(30070)
        travel          = String(30071)
        tvshows         = String(30072)
        world           = String(30073)
        youtube         = String(30074)

    if url == 'add':
        listcount = Sleep_If_Function_Active(function=Main_Menu_Visibility,args=[menu_list,menu_options,True])
        if xbmc.getCondVisibility('Skin.String(Custom6HomeItem.Disable)') and 'comedy' in menu_options:
            Add_Dir('%s %s'%(String(30060),comedy),'Skin.SetString(Custom6HomeItem.Disable,)','set_home_menu',False,'special://home/media/branding/backgrounds/HOME_COMEDY/HOME_COMEDY_001.jpg','','')
        if xbmc.getCondVisibility('Skin.String(Custom3HomeItem.Disable)') and 'cooking' in menu_options:
            Add_Dir('%s %s'%(String(30060),cooking),'Skin.SetString(Custom3HomeItem.Disable,)','set_home_menu',False,'special://home/media/branding/backgrounds/HOME_COOKING/HOME_COOKING_001.jpg','','')
        if xbmc.getCondVisibility('Skin.String(Custom4HomeItem.Disable)') and 'fitness' in menu_options:
            Add_Dir('%s %s'%(String(30060),fitness),'Skin.SetString(Custom4HomeItem.Disable,)','set_home_menu',False,'special://home/media/branding/backgrounds/HOME_FITNESS/HOME_FITNESS_001.jpg','','')
        if xbmc.getCondVisibility('Skin.String(Custom5HomeItem.Disable)') and 'gaming' in menu_options:
            Add_Dir('%s %s'%(String(30060),gaming),'Skin.SetString(Custom5HomeItem.Disable,)','set_home_menu',False,'special://home/media/branding/backgrounds/HOME_GAMING/HOME_GAMING_001.jpg','','')
        if xbmc.getCondVisibility('Skin.String(FavoritesHomeItem.Disable)') and 'kids' in menu_options:
            Add_Dir('%s %s'%(String(30060),kids),'Skin.SetString(FavoritesHomeItem.Disable,)','set_home_menu',False,'special://home/media/branding/backgrounds/HOME_KIDS/HOME_KIDS_001.jpg','','')
        if xbmc.getCondVisibility('Skin.String(LiveTVHomeItem.Disable)') and 'livetv' in menu_options:
            Add_Dir('%s %s'%(String(30060),livetv),'Skin.SetString(LiveTVHomeItem.Disable,)','set_home_menu',False,'special://home/media/branding/backgrounds/HOME_LIVE_TV/HOME_LIVE_TV_001.jpg','','')
        if xbmc.getCondVisibility('Skin.String(MovieHomeItem.Disable)') and 'movies' in menu_options:
            Add_Dir('%s %s'%(String(30060),movies),'Skin.SetString(MovieHomeItem.Disable,)','set_home_menu',False,'special://home/media/branding/backgrounds/HOME_MOVIES/HOME_MOVIES_001.jpg','','')
        if xbmc.getCondVisibility('Skin.String(MusicHomeItem.Disable)') and 'music' in menu_options:
            Add_Dir('%s %s'%(String(30060),music),'Skin.SetString(MusicHomeItem.Disable,)','set_home_menu',False,'special://home/media/branding/backgrounds/HOME_MUSIC/HOME_MUSIC_001.jpg','','')
        if xbmc.getCondVisibility('Skin.String(ProgramsHomeItem.Disable)') and 'news' in menu_options:
            Add_Dir('%s %s'%(String(30060),news),'Skin.SetString(ProgramsHomeItem.Disable,)','set_home_menu',False,'special://home/media/branding/backgrounds/HOME_NEWS/HOME_NEWS_001.jpg','','')
        if xbmc.getCondVisibility('Skin.String(VideosHomeItem.Disable)') and 'sports' in menu_options:
            Add_Dir('%s %s'%(String(30060),sports),'Skin.SetString(VideosHomeItem.Disable,)','set_home_menu',False,'special://home/media/branding/backgrounds/HOME_SPORTS/HOME_SPORTS_001.jpg','','')
        if xbmc.getCondVisibility('Skin.String(Custom2HomeItem.Disable)') and 'technology' in menu_options:
            Add_Dir('%s %s'%(String(30060),technology),'Skin.SetString(Custom2HomeItem.Disable,)','set_home_menu',False,'special://home/media/branding/backgrounds/HOME_TECHNOLOGY/HOME_TECHNOLOGY_001.jpg','','')
        if xbmc.getCondVisibility('Skin.String(WeatherHomeItem.Disable)') and 'travel' in menu_options:
            Add_Dir('%s %s'%(String(30060),travel),'Skin.SetString(WeatherHomeItem.Disable,)','set_home_menu',False,'special://home/media/branding/backgrounds/HOME_TRAVEL/HOME_TRAVEL_001.jpg','','')
        if xbmc.getCondVisibility('Skin.String(TVShowHomeItem.Disable)') and 'tvshows' in menu_options:
            Add_Dir('%s %s'%(String(30060),tvshows),'Skin.SetString(TVShowHomeItem.Disable,)','set_home_menu',False,'special://home/media/branding/backgrounds/HOME_TV_SHOWS/HOME_TV_SHOWS_001.jpg','','')
        if xbmc.getCondVisibility('Skin.String(PicturesHomeItem.Disable)') and 'world' in menu_options:
            Add_Dir('%s %s'%(String(30060),world),'Skin.SetString(PicturesHomeItem.Disable,)','set_home_menu',False,'special://home/media/branding/backgrounds/HOME_WORLD/HOME_WORLD_001.jpg','','')
        if xbmc.getCondVisibility('Skin.String(ShutdownHomeItem.Disable)') and 'youtube' in menu_options:
            Add_Dir('%s %s'%(String(30060),youtube),'Skin.SetString(ShutdownHomeItem.Disable,)','set_home_menu',False,'special://home/media/branding/backgrounds/HOME_YOUTUBE/HOME_YOUTUBE_001.jpg','','')
        if xbmc.getCondVisibility('Skin.String(MusicVideoHomeItem.Disable)') and 'xxx' in menu_options:
            Add_Dir('%s %s'%(String(30060),xxx),'Skin.SetString(MusicVideoHomeItem.Disable,)','set_home_menu',False,'special://home/media/branding/backgrounds/HOME_XXX/HOME_XXX_001.jpg','','')
        if listcount > 0:
            OK_Dialog(String(30079),String(30310))
            xbmc.executebuiltin('ActivateWindow(home)')

    if url == 'remove':
        listcount = Sleep_If_Function_Active(function=Main_Menu_Visibility,args=[menu_list,'',False])
        if not xbmc.getCondVisibility('Skin.String(Custom6HomeItem.Disable)') and 'comedy' in menu_options:
            Add_Dir('%s %s'%(String(30076),comedy),'Skin.SetString(Custom6HomeItem.Disable,True)','set_home_menu',False,'special://home/media/branding/backgrounds/HOME_COMEDY/HOME_COMEDY_001.jpg','','')
        if not xbmc.getCondVisibility('Skin.String(Custom3HomeItem.Disable)') and 'cooking' in menu_options:
            Add_Dir('%s %s'%(String(30076),cooking),'Skin.SetString(Custom3HomeItem.Disable,True)','set_home_menu',False,'special://home/media/branding/backgrounds/HOME_COOKING/HOME_COOKING_001.jpg','','')
        if not xbmc.getCondVisibility('Skin.String(Custom4HomeItem.Disable)') and 'fitness' in menu_options:
            Add_Dir('%s %s'%(String(30076),fitness),'Skin.SetString(Custom4HomeItem.Disable,True)','set_home_menu',False,'special://home/media/branding/backgrounds/HOME_FITNESS/HOME_FITNESS_001.jpg','','')
        if not xbmc.getCondVisibility('Skin.String(Custom5HomeItem.Disable)') and 'gaming' in menu_options:
            Add_Dir('%s %s'%(String(30076),gaming),'Skin.SetString(Custom5HomeItem.Disable,True)','set_home_menu',False,'special://home/media/branding/backgrounds/HOME_GAMING/HOME_GAMING_001.jpg','','')
        if not xbmc.getCondVisibility('Skin.String(FavoritesHomeItem.Disable)') and 'kids' in menu_options:
            Add_Dir('%s %s'%(String(30076),kids),'Skin.SetString(FavoritesHomeItem.Disable,True)','set_home_menu',False,'special://home/media/branding/backgrounds/HOME_KIDS/HOME_KIDS_001.jpg','','')
        if not xbmc.getCondVisibility('Skin.String(LiveTVHomeItem.Disable)') and 'livetv' in menu_options:
            Add_Dir('%s %s'%(String(30076),livetv),'Skin.SetString(LiveTVHomeItem.Disable,True)','set_home_menu',False,'special://home/media/branding/backgrounds/HOME_LIVE_TV/HOME_LIVE_TV_001.jpg','','')
        if not xbmc.getCondVisibility('Skin.String(MovieHomeItem.Disable)') and 'movies' in menu_options:
            Add_Dir('%s %s'%(String(30076),movies),'Skin.SetString(MovieHomeItem.Disable,True)','set_home_menu',False,'special://home/media/branding/backgrounds/HOME_MOVIES/HOME_MOVIES_001.jpg','','')
        if not xbmc.getCondVisibility('Skin.String(MusicHomeItem.Disable)') and 'music' in menu_options:
            Add_Dir('%s %s'%(String(30076),music),'Skin.SetString(MusicHomeItem.Disable,True)','set_home_menu',False,'special://home/media/branding/backgrounds/HOME_MUSIC/HOME_MUSIC_001.jpg','','')
        if not xbmc.getCondVisibility('Skin.String(ProgramsHomeItem.Disable)') and 'news' in menu_options:
            Add_Dir('%s %s'%(String(30076),news),'Skin.SetString(ProgramsHomeItem.Disable,True)','set_home_menu',False,'special://home/media/branding/backgrounds/HOME_NEWS/HOME_NEWS_001.jpg','','')
        if not xbmc.getCondVisibility('Skin.String(VideosHomeItem.Disable)') and 'sports' in menu_options:
            Add_Dir('%s %s'%(String(30076),sports),'Skin.SetString(VideosHomeItem.Disable,True)','set_home_menu',False,'special://home/media/branding/backgrounds/HOME_SPORTS/HOME_SPORTS_001.jpg','','')
        if not xbmc.getCondVisibility('Skin.String(Custom2HomeItem.Disable)') and 'technology' in menu_options:
            Add_Dir('%s %s'%(String(30076),technology),'Skin.SetString(Custom2HomeItem.Disable,True)','set_home_menu',False,'special://home/media/branding/backgrounds/HOME_TECHNOLOGY/HOME_TECHNOLOGY_001.jpg','','')
        if not xbmc.getCondVisibility('Skin.String(WeatherHomeItem.Disable)') and 'travel' in menu_options:
            Add_Dir('%s %s'%(String(30076),travel),'Skin.SetString(WeatherHomeItem.Disable,True)','set_home_menu',False,'special://home/media/branding/backgrounds/HOME_TRAVEL/HOME_TRAVEL_001.jpg','','')
        if not xbmc.getCondVisibility('Skin.String(TVShowHomeItem.Disable)') and 'tvshows' in menu_options:
            Add_Dir('%s %s'%(String(30076),tvshows),'Skin.SetString(TVShowHomeItem.Disable,True)','set_home_menu',False,'special://home/media/branding/backgrounds/HOME_TV_SHOWS/HOME_TV_SHOWS_001.jpg','','')
        if not xbmc.getCondVisibility('Skin.String(PicturesHomeItem.Disable)') and 'world' in menu_options:
            Add_Dir('%s %s'%(String(30076),world),'Skin.SetString(PicturesHomeItem.Disable,True)','set_home_menu',False,'special://home/media/branding/backgrounds/HOME_WORLD/HOME_WORLD_001.jpg','','')
        if not xbmc.getCondVisibility('Skin.String(ShutdownHomeItem.Disable)') and 'youtube' in menu_options:
            Add_Dir('%s %s'%(String(30076),youtube),'Skin.SetString(ShutdownHomeItem.Disable,True)','set_home_menu',False,'special://home/media/branding/backgrounds/HOME_YOUTUBE/HOME_YOUTUBE_001.jpg','','')
        if not xbmc.getCondVisibility('Skin.String(MusicVideoHomeItem.Disable)') and 'xxx' in menu_options:
            Add_Dir('%s %s'%(String(30076),xxx),'Skin.SetString(MusicVideoHomeItem.Disable,True)','set_home_menu',False,'special://home/media/branding/backgrounds/HOME_XXX/HOME_XXX_001.jpg','','')
        if listcount > 0:
            OK_Dialog(String(30079),String(30311))
            xbmc.executebuiltin('ActivateWindow(home)')
#---------------------------------------------------------------------------------------------------
def Main_Menu_Visibility(menu_list='',menu_options='',enabled=True):
    listcount = 0
    if enabled:
        for item in menu_list:
            if item[1] in menu_options and xbmc.getCondVisibility('Skin.String(%s)'%item[0]):
                listcount += 1
    else:
        for item in menu_list:
            if not xbmc.getCondVisibility('Skin.String(%s)'%item[0]):
                listcount += 1
    return listcount
#---------------------------------------------------------------------------------------------------
# Function to move a directory to another location, use 1 for clean paramater if you want to remove original source.
def Move_Tree(src,dst,clean):
    dolog('SOURCE TO MOVE: %s'%src)
    for src_dir, dirs, files in os.walk(src):
        dst_dir = src_dir.replace(src, dst, 1)
        if not os.path.exists(dst_dir):
            dolog('Creating path: %s'% dst_dir)
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.move(src_file, dst_dir)
            dolog('moved: %s to %s'% (src_file, dst_dir))
    if clean:
        try:
            shutil.rmtree(src)
            dolog('Successfully removed %s'% src)
        except:
            dolog('Failed to remove %s'% src)
#---------------------------------------------------------------------------------------------------
# Multiselect Dialog - try the built-in multiselect or fallback to pre-jarvis workaround
def multidialog(title, mylist, images, description):
    try:
        ret = dialog.multiselect(title, mylist)
    except:
        ret = multiselect(title, mylist, images, description)
    return ret if not ret == None else []
#---------------------------------------------------------------------------------------------------
# Multiselect Dialog for older Kodi versions (pre Jarvis)
def multiselect(title, mylist, images, description):
    global pos
    global listicon
    class MultiChoiceDialog(pyxbmct.AddonDialogWindow):
        def __init__(self, title="", items=None, images=None, description=None):
            super(MultiChoiceDialog, self).__init__(title)
            self.setGeometry(1100, 700, 9, 9)
            self.selected = []
            self.set_controls()
            self.connect_controls()
            self.listing.addItems(items or [])
            self.set_navigation()
            self.connect(ACTION_NAV_BACK, self.close)
            self.connect(ACTION_MOVE_UP, self.update_list)
            self.connect(ACTION_MOVE_DOWN, self.update_list)
            
        def set_controls(self):
            Background  = pyxbmct.Image(dialog_bg, aspectRatio=0) # set aspect ratio to stretch
            Background.setImage(dialog_bg)
            self.listing = pyxbmct.List(_imageWidth=15)
            self.placeControl(Background, 0, 0, rowspan=20, columnspan=20)
            self.placeControl(self.listing, 0, 0, rowspan=9, columnspan=5, pad_y=10) # grid reference, start top left and span 9 boxes down and 5 across
            Icon=pyxbmct.Image(images[0], aspectRatio=2) # set aspect ratio to keep original
            Icon.setImage(images[0])
            self.placeControl(Icon, 0, 5, rowspan=3, columnspan=3, pad_x=10, pad_y=10)
            self.textbox = pyxbmct.TextBox()
            self.placeControl(self.textbox, 4, 5, rowspan=3, columnspan=3, pad_x=10, pad_y=10)
            self.textbox.setText(description[0])
            self.ok_button = pyxbmct.Button("OK")
            self.placeControl(self.ok_button, 7, 5, pad_x=10, pad_y=10)
            self.cancel_button = pyxbmct.Button("Cancel")
            self.placeControl(self.cancel_button, 7, 6, pad_x=10, pad_y=10)

        def connect_controls(self):
            self.connect(self.listing, self.check_uncheck)
            self.connect(self.ok_button, self.ok)
            self.connect(self.cancel_button, self.close)

        def set_navigation(self):
            self.listing.controlLeft(self.ok_button)
            self.listing.controlRight(self.ok_button)
            self.ok_button.setNavigation(self.listing, self.listing, self.cancel_button, self.cancel_button)
            self.cancel_button.setNavigation(self.listing, self.listing, self.ok_button, self.ok_button)
            if self.listing.size():
                self.setFocus(self.listing)
            else:
                self.setFocus(self.cancel_button)
            
        def update_list(self):
            pos      = self.listing.getSelectedPosition()
            listicon = images[pos]
            Icon=pyxbmct.Image(listicon, aspectRatio=2)
            Icon.setImage(listicon)
            self.placeControl(Icon, 0, 5, rowspan=3, columnspan=3, pad_x=10, pad_y=10)
            self.textbox.setText(description[pos])

        def check_uncheck(self):
            list_item = self.listing.getSelectedItem()
            if list_item.getLabel2() == "checked":
                list_item.setIconImage("")
                list_item.setLabel2("unchecked")
            else:
                list_item.setIconImage(checkicon)
                list_item.setLabel2("checked")

        def ok(self):
            self.selected = [index for index in xrange(self.listing.size())
                            if self.listing.getListItem(index).getLabel2() == "checked"]
            super(MultiChoiceDialog, self).close()

        def close(self):
            self.selected = []
            super(MultiChoiceDialog, self).close()
            
    dialog = MultiChoiceDialog(title, mylist, images, description)
    dialog.doModal()
    return dialog.selected
    del dialog
#---------------------------------------------------------------------------------------------------
# Bring up a dialog select of user profile details
@route(mode='my_details')
def My_Details():
    try:
        userid = encryptme('d',Addon_Setting(setting='userid'))
    except:
        try:
            Sleep_If_Function_Active(Check_License)
            userid = encryptme('d',Addon_Setting(setting='userid'))
        except:
            Addon_Setting(setting='userid',value='')
            userid = ''

    username = Addon_Setting('username')

    if os.path.exists(usercheck_file):
        username = encryptme('d',Text_File(usercheck_file,'r'))
    if userid != '':
        if username != '':
            username = String(30350)%username
            my_array = [String(30100),username,String(30354),String(30552)]
        else:
            username = String(30348)
            my_array = [String(30100),username,String(30354)]

        choice = Select_Dialog(String(30349)%userid,my_array)
        if choice >= 0:
            if choice == 0:
                Get_Updates()
                # Grab_Updates(BASE+'boxer/comm_live.php?z=c&x=')
            if choice == 1 and username == String(30348):
                Run_Code(url="boxer/User_Registration.php")
            elif choice == 1:
                My_Profile()
            if choice == 2:
                Social_Shares()
            if choice == 3:
                Keyword_Options()
    else:
        OK_Dialog(String(30380),String(30381))
        xbmc.executebuiltin('RunAddon(script.openwindow)')
#---------------------------------------------------------------------------------------------------
# List all the users shared menus
def My_Friends():
    results     = Get_All_From_Table('friends')
    my_array    = [String(30451)]
    final_array = []
    for item in results:
        username = item["username"]
        status   = item["status"]
        sender   = item["sender"]
        friendid = item["id"]
        if status == 'friends':
            my_array.append('[COLOR=dodgerblue]%s[/COLOR]'%username)
        elif status == 'pending':
            my_array.append('[COLOR=grey]%s[/COLOR] [PENDING]'%username)
        if status != 'blocked':
            final_array.append([username,status,sender,friendid])

    choice = Select_Dialog(String(30377),my_array)
    if choice == 0:
        Run_Code(url='boxer/User_Friend_Request.php')
    elif choice == 1:
        Friend_Options(final_array[choice-1])
    else:
        My_Profile()
#---------------------------------------------------------------------------------------------------
# List messages
def My_Messages(show_dialog=True):
    if show_dialog:
        Update_Messages(show_dialog=False)
    my_array     = []
    full_array   = []
    message_list = Get_All_From_Table('inbox')
    for item in message_list:
        status    = item["read"]
        orig_msg  = item["message"]
        message   = encryptme("d",orig_msg)
        command   = item["command"]
        timestamp = item["timestamp"]
        sender    = item["sender"]
        if str(status) != '1':
            title     = '[COLOR=dodgerblue][%s][/COLOR][COLOR=gold] '%sender
        else:
            title     = '[COLOR=dodgerblue][%s][/COLOR] '%sender
        header    = Find_In_Text(content=message,start='~header~',end='~msg~',show_errors=False)[0]
        if header.startswith('String('):
            header = eval(header)
        title    += header
        if str(status) != '1':
            title += '[/COLOR]'
        main_msg  = eval( Find_In_Text(content=message,start='~msg~',end='~type~',show_errors=False)[0] )
        main_msg  = Find_In_Text(content=message,start='~msg~',end='~type~',show_errors=False)[0]
        msg_type  = Find_In_Text(content=message,start='~type~',end='~',show_errors=False)[0]
        if main_msg.startswith('String('):
            main_msg = eval(main_msg)
        full_array.append({"title":header,"timestamp":timestamp,"sender":sender,"message":main_msg,"type":msg_type,"command":command})
        my_array.append(title)

    choice = Select_Dialog('[COLOR=cyan]%s[/COLOR]'%String(30376),my_array)
    if choice >= 0:
        DB_Query(db_path=db_social,query='UPDATE inbox SET `read`="1" WHERE `command`="%s" AND `message`="%s" AND `sender`="%s"'%(command,orig_msg,sender) )
        Open_Message(full_array[choice])
    else:
        My_Profile()
#---------------------------------------------------------------------------------------------------
# Bring up a dialog select of user profile details
def My_Profile():
    userid     = Addon_Setting('userid')
    username   = Addon_Setting('username')

# LIST WITH UPDATE ACCOUNT PASSWORD - NOT YET READY
    # my_array = [String(30376),String(30377),String(30389),String(30404),String(30407),String(30379),String(30385),'[COLOR=red]%s[/COLOR]'%String(30382)]

# LIST WITH MY FRIENDS - NOT YET RELEASE READY, NEED TO CHECK STATUS SYNC
    # my_array = [String(30376),String(30377),String(30389),String(30404),String(30379),String(30385),'[COLOR=red]%s[/COLOR]'%String(30382)]


    my_array = [String(30376),String(30389),String(30404),String(30379),String(30385),'[COLOR=orange]%s[/COLOR]'%String(30382),'[COLOR=red]%s[/COLOR]'%String(30530)]
    choice = Select_Dialog('[COLOR=cyan]%s[/COLOR]'%username,my_array)
    if choice >= 0:
        if choice == 0:
            My_Messages()

# MY FRIENDS - NOT YET RELEASE READY
        # if choice == 1 and username != String(30348):
        #     My_Friends()
        if choice == 1:
            Show_Log()
        if choice == 2:
            if username != '':
                Change_XXX_Password()
            else:
                OK_Dialog(String(30380),String(30405))
        # if choice == 4:
        #     User_Check('reset')
        if choice == 3:
            Run_Code(url='boxer/User_Email.php')
        if choice == 4:
            Clear_User_Cookie()
        if choice == 5:
            Clear_User_Data()
        if choice == 6:
            Delete_Account()
    else:
        My_Details()
#---------------------------------------------------------------------------------------------------
# List all the users shared menus
def My_Shares():
    results   = Get_All_From_Table('shares')
    my_array  = []
    for item in results:
        my_array.append( urllib.unquote(item["path"]) )

    choice = Select_Dialog(String(30355),my_array)
    if choice >= 0:
        Share_Options(my_array[choice])
    else:
        Social_Shares()
#---------------------------------------------------------------------------------------------------
@route(mode='network_settings')
def Network():
    Network_Settings()
#---------------------------------------------------------------------------------------------------
# Open Kodi File Manager
@route(mode='open_sf')
def Open_SF():    
    menu_array = [String(30061), String(30077), String(30062), String(30063),\
    String(30064), String(30065), String(30066), String(30067), String(30068),\
    String(30069), String(30070), String(30071), String(30072), String(30073),\
    String(30074), String(30075)]

    final_list = ['HOME_COMEDY','HOME_COOKING','HOME_FITNESS','HOME_GAMING',\
    'HOME_KIDS','HOME_LIVE_TV','HOME_MOVIES','HOME_MUSIC','HOME_NEWS','HOME_SPORTS',\
    'HOME_TECHNOLOGY','HOME_TRAVEL','HOME_TV_SHOWS','HOME_WORLD','HOME_YOUTUBE','HOME_XXX']

    choice = Select_Dialog(String(30128),menu_array)
    if choice >= 0:
        category    = final_list[choice]
        SF_Path     = os.path.join(SF_ROOT,category)
        My_Folders  = Get_Contents(path=SF_Path,full_path=False)
        final_array = []
        for item in My_Folders:
            item = item.replace(os.sep,'')
            xml_path = os.path.join(SF_Path,item,'favourites.xml')
            if os.path.exists(xml_path):
                final_array.append(item)
        dolog(repr(final_array))
        if len(final_array) == 0:
            OK_Dialog(String(30079),String(30080))
            Open_SF()
        else:
            choice = Select_Dialog(String(30359)%menu_array[choice],final_array)
            if choice >= 0:
                share    = final_array[choice]
                my_array = [String(30360),String(30361)]
                share_choice = Select_Dialog(String(30359)%final_array[choice],my_array)
                if share_choice >= 0:
                    if share_choice == 0:
                        Upload_Share( fullpath=xml_path.replace('favourites.xml',''), item=share )
                    if share_choice == 1:
                        xbmc.executebuiltin( 'ActivateWindow(programs,"plugin://plugin.program.super.favourites/?folder=%s/%s",return)' % (category,share) )
                else:
                    Social_Shares()
            else:
                Social_Shares()
    else:
        Social_Shares()
#---------------------------------------------------------------------------------------------------
# Function to install venz pack
def Open_Link(url):
    response = Open_URL(post_type='post',url=url)
    dolog("### "+response)
    if "record" in response:
        Get_Updates()
        xbmc.executebuiltin('Container.Refresh')
    else:
        OK_Dialog(String(30131),String(30132))
#---------------------------------------------------------------------------------------------------
# Open the relevant message type
def Open_Message(contents={}):
    username    = encryptme("e",Addon_Setting("username"))
    email       = encryptme("e",Addon_Setting("email"))
    password    = Addon_Setting("password")
    urlparams   = encryptme("e",URL_Params())
    title       = contents["title"]
    timestamp   = contents["timestamp"]
    sender      = contents["sender"]
    message     = contents["message"]
    msg_type    = contents["type"]
    command     = contents["command"]

    if msg_type == 'fr':
        choice = YesNo_Dialog(title,message)
        if choice == 1:
            exec( encryptme('d',command) )
        elif choice == 0:
            if email != "" and username != "" and password != "":
                choice2 = YesNo_Dialog(String(30466),String(30467),String(30468),String(30469))
                if choice2 == 1:
                    Run_Code(url="boxer/User_Reject_Request.php",payload={"x":urlparams,"n":username,"e":email,"p":password,"f":encryptme('e',sender)} )
                elif choice2 == 0:
                    Run_Code(url="boxer/User_Ignore_Request.php",payload={"x":urlparams,"n":username,"e":email,"p":password,"f":encryptme('e',sender)} )
#-----------------------------------------------------------------------------------------------------------------
## Function to open a URL, try 3 times then respond with blank
def Open_URL2(url):
    if debug == 'true':
        xbmc.log(url)
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req, timeout = 10)
    if response != '':
        link     = response.read()
        response.close()
        return link.replace('\r','').replace('\n','').replace('\t','')
    else:
        return response
#---------------------------------------------------------------------------------------------------
# Check if system is OE or LE
def OpenELEC_Check():
    try:
        content = Grab_Log()
        if 'Running on OpenELEC' in content or 'Running on LibreELEC' in content:
            return True
        else:
            return False
    except:
        return False
#---------------------------------------------------------------------------------------------------
def OpenELEC_Settings():
    if xbmc.getCondVisibility("System.HasAddon(service.openelec.settings)") or xbmc.getCondVisibility("System.HasAddon(service.libreelec.settings)"):
        if xbmc.getCondVisibility("System.HasAddon(service.openelec.settings)"): 
            xbmc.executebuiltin('RunAddon(service.openelec.settings)')
        elif xbmc.getCondVisibility("System.HasAddon(service.libreelec.settings)"): 
            xbmc.executebuiltin('RunAddon(service.libreelec.settings)')
        xbmc.sleep(1500)
        xbmc.executebuiltin('Control.SetFocus(1000,2)')
        xbmc.sleep(500)
        xbmc.executebuiltin('Control.SetFocus(1200,0)')
#---------------------------------------------------------------------------------------------------
# Scrape Google PlayStore
def Play_Store_Scrape(i):
    name        = i
    fanart      = Fanart_Path
    iconimage   = "androidapp://sources/apps/%s.png" % i
    category    = 'Unknown'
    genre       = 'Unknown'
    video       = 'none'
    PEGI        = 'N/A'
    author      = 'N/A'
    description = 'N/A'

    base_url = "https://play.google.com/store/apps/details?id=" +i
    link = Open_URL(url=base_url)
    if link != False:
        link = link.replace('\n','').replace('\r','')
        raw_content = re.compile(r'<div class="id-app-title[\s\S]*?id-cluster-container details-section recommendation').findall(link)
        link = raw_content[0]

# App Name
        regexTitle = r'<div class="id-app-title".tabindex=".">(.+?)</div>'
        match = re.search(regexTitle, link)
        if match != None:
            name = urllib.unquote(match.group(1))
        else:
            name = i
 
# Category
        regexCategory = r'/store/apps/category/(.+?).">'
        match = re.compile(regexCategory).findall(link)
        category = urllib.unquote(match[0]) if len(match) > 0 else 'Unknown'

# Fanart
        regexBackdrop = r'data-expand-to="full-screenshot-[0-9]{1,2}" src="(//\w+?.\w+?.\S+?=h900)"'
        match = re.compile(regexBackdrop).findall(link)
        if len(match) > 0:
            fanart = "https:" +match[len(match) - 1]

# Genre
        regexGenre = r'<span itemprop="genre">(.+?)</span>'
        match = re.search(regexGenre, link)
        if match != None:
            genre = urllib.unquote(match.group(1))

# Apk Description
        regexDescription = r'itemprop="description"> <div jsname=".+?">(.+?)<div class="show-more-end"'
        match = re.compile(regexDescription).findall(link)
        if len(match) !=0:
            description = match[0].replace('<b>','[B]').replace('</b>','[/B]').replace('<i>','[I]').replace('</i>','[/I]').replace('<p>','[CR]').replace('</p>','').replace('&ndash;','-').replace('&mdash;','-').replace("&rsquo;", "'").replace("&rdquo;", '"').replace("</a>", " ").replace("&hellip;", '...').replace("&lsquo;", "'").replace("&ldquo;", '"').replace("&amp;",'&').replace('&#39;',"'").replace('<br>','[CR]').replace('<div>','').replace('</div>','')
            description = description.strip().rstrip()

# Preview Video
        regexVideo = r'data-video-url="https://www.youtube.com/embed/(\S.+?)\?ps=play.+?"'
        match = re.search(regexVideo, link)
        video = match.group(1) if match != None else 'none'

# Age Restriction
        regexAge = r'<div class=".+?ontent-rating-title">(.+?)</div>'
        match = re.search(regexAge, link)
        PEGI = match.group(1) if match != None else 'N/A'
        PEGI = PEGI.replace('</span> ','')

# Author
        regexMaker = r'<span itemprop="name">(.+?)</span>'
        match = re.search(regexMaker, link)
        author = match.group(1) if match != None else 'N/A'

    final_list = [i, name, iconimage, fanart, category, genre, video, PEGI, author, description]
    return final_list
#---------------------------------------------------------------------------------------------------
# Set popup xml based on platform
def pop(xmlfile):
# if popup is an advert from the web
    if 'http' in xmlfile:
        contents = 'none'
        filedate = xmlfile[-10:]
        filedate = filedate[:-4]
        latest = os.path.join(ADDON_DATA,AddonID,'latest')

        if os.path.exists(latest):
            readfile = open(latest, mode='r')
            contents = readfile.read()
            readfile.close()

        if contents == filedate:
            filedate = contents
                
        else:
            Download(xmlfile,os.path.join(ADDONS,AddonID,'resources','skins','DefaultSkin','media','latest.jpg'))
            writefile = open(latest, mode='w+')
            writefile.write(filedate)
            writefile.close()
        xmlfile = 'latest.xml'
    popup = SPLASH(xmlfile,ADDON.getAddonInfo('path'),'DefaultSkin',close_time=34)
    popup.doModal()
    del popup
#---------------------------------------------------------------------------------------------------
# Called by openwindow for registration
@route(mode='register_device')
def Register_Device():
    Run_Code(url="boxer/User_Registration.php")
#---------------------------------------------------------------------------------------------------
# Function to clear the addon_data
@route(mode='remove_addon_data')
def Remove_Addon_Data():
# Offer to remove everything, we don't want this as it will cause a fresh install

    # choice = YesNo_Dialog(String(30133), String(30134), yeslabel=String(30135), nolabel=String(30136))
    
    # if choice:
    #     choice = YesNo_Dialog(String(30137),String(30138))
    #     if choice:
    #         Delete_Userdata()
    #         OK_Dialog(String(30139), '', String(30140),'')
    # else:
    skiparray = ['.DS_Store','plugin.program.tbs','script.openwindow','script.trtv','plugin.program.super.favourites']
    namearray = []
    iconarray = []
    descarray = []
    patharray = []
    finalpath = []

    for file in os.listdir(ADDON_DATA):
        addon_id    = None
        if os.path.isdir(os.path.join(ADDON_DATA,file)):
            try:
                addon_id    = Get_Addon_ID(file)
                Addon       = xbmcaddon.Addon(addon_id)
                name        = Addon.getAddonInfo('name')
                iconimage   = Addon.getAddonInfo('icon')
                description = Addon.getAddonInfo('description')
            except:
                name        = String(30142)
                iconimage   = unknown_icon
                description = String(30141)

        else:
            name        = 'Unknown Add-on'
            iconimage   =  unknown_icon
            description = 'No add-on has been found on your system that matches this ID. The most likely scenario for this is you\'ve previously uninstalled this add-on and left the old addon_data on the system.'

        if not addon_id in skiparray and addon_id != None:
            filepath = os.path.join(ADDON_DATA,file)
            namearray.append(file)
            iconarray.append(iconimage)
            descarray.append('[COLOR=gold]%s[/COLOR][CR][CR]%s'% (name, description))
            patharray.append(filepath)

    finalarray = multiselect(String(30143),namearray,iconarray,descarray)
    for item in finalarray:
        newpath = patharray[item]
        newname = namearray[item]
        finalpath.append([newname,newpath])
    if len(finalpath) > 0:
        Remove_Addons(finalpath)
#---------------------------------------------------------------------------------------------------
# Function to remove a list of addons including addon_data
@route(mode='remove_addons', args=['url'])
def Remove_Addons(url):
    for item in url:
        data_path = item[1].replace(ADDONS,ADDON_DATA)
        if 'addon_data' in item[1]:
            addontype = String(30146)
            dialog_text = String(30144)
        else:
            addontype = String(30147)
            dialog_text = String(30145)
        if YesNo_Dialog(String(30148) % addontype, String(30149)% dialog_text+'[COLOR=dodgerblue]%s[/COLOR]'% item[0]):
            addon_id = Get_Addon_ID(item[1])
            Set_Setting(setting_type='addon_enable',setting=addon_id, value='false')
            Delete_Folders(item[1])
            if not 'addon_data' in item[1]:
                if YesNo_Dialog(String(30133),String(30150)):
                    try:
                        Delete_Folders(item[1])
                    except:
                        pass
#---------------------------------------------------------------------------------------------------
# Function to clear the packages folder
@route(mode='remove_crash_logs')
def Remove_Crash_Logs():
    if YesNo_Dialog(String(30153),String(30154),no=String(30041),yes=String(30042)):
        Delete_Crashlogs()
        OK_Dialog(String(30155),String(30156))
#-----------------------------------------------------------------------------
# Remove a path, whether folder or file it will be deleted
def Remove_Files():
    remlist = os.path.join(TBSDATA,'remlist')
    dolog('### Attempting to Remove Files')
    if os.path.exists(remlist):
        readfile = open(remlist,'r')
        content  = readfile.read().splitlines()
        readfile.close()
        for item in content:
            rempath = xbmc.translatePath('special://home')+item
            if os.path.exists(rempath):
                try:
                    os.remove(rempath)
                    dolog('### Successfully removed file: %s' % rempath)
                except:
                    try:
                        shutil.rmtree(rempath)
                        dolog('### Successfully removed folder: %s' % rempath)
                    except:
                        dolog("### Failed to remove: %s" %rempath)
#---------------------------------------------------------------------------------------------------
# Remove an item from the system
def Remove_Menu(function, menutype = ''):
    contentarray = []
    imagearray   = []
    descarray    = []
    contenturl   = []
    urlparams = URL_Params()
    dolog('### OPENING URL TO GRAB DETAILS OF WHAT TO REMOVE:')
    dolog(BASE+'boxer/cat_search_live.php?x=%s' % (encryptme('e','%s&%s&0&%s&%s' % (urlparams, function, social_shares, menutype))))
    content_list   = Open_URL(post_type='post',url=BASE+'boxer/cat_search_live.php',payload={"x":encryptme('e','%s&%s&0&%s&%s' % (urlparams, function, social_shares, menutype))})
    clean_link     = encryptme('d',content_list)
    dolog('#### RETURN: %s' % clean_link)
# Grab all the shares which match the master sub-category
    match = re.compile('n="(.+?)"t="(.+?)"d="(.+?)"l="(.+?)"', re.DOTALL).findall(clean_link)
    for name, thumb, desc, link in match:
        contentarray.append(name)
        imagearray.append(thumb)
        descarray.append(desc)
        contenturl.append(link)

# Return the results and update
    if len(contentarray) > 0:
        if menutype == '':
            choices = multiselect(String(30088),contentarray,imagearray,descarray)
            if len(choices) > 0:
                Notify(String(30086),String(30087),'5000',os.path.join(ADDONS,'plugin.program.tbs','resources','update.png'))
                xbmc.executebuiltin('ActivateWindow(HOME)')
                for item in choices:
                    Open_URL(post_type='post',url=contenturl[item])
        else:
            for item in contenturl:
                dolog('### URL TO REMOVE: %s' % item)
                Open_URL(post_type='post',url=item)

        Get_Updates()
    elif menutype == '':
        OK_Dialog(String(30089),String(30090))
#---------------------------------------------------------------------------------------------------
# Function to clear the packages folder
@route(mode='remove_packages', args=['url'])
def Remove_Packages(url=''):
    if YesNo_Dialog(String(30157), String(30158), no=String(30041),yes=String(30042)):
        Delete_Folders(PACKAGES)
    if url == '':
        OK_Dialog(String(30155), '', String(30159))
#---------------------------------------------------------------------------------------------------
# Function to clear the packages folder
@route(mode='remove_textures_dialog')
def Remove_Textures_Dialog():
    if YesNo_Dialog(String(30160),String(30161)):
        Remove_Textures()
        Delete_Folders(THUMBNAILS)
    
        if YesNo_Dialog(String(30162), String(30163), no=String(30164),yes=String(30165)):
            System('quit')
#---------------------------------------------------------------------------------------------------
# Function to remove textures13.db
@route(mode='remove_textures')
def Remove_Textures():
    textures   =  xbmc.translatePath('special://home/userdata/Database/Textures13.db')
    try:
        dbcon = database.connect(textures)
        dbcur = dbcon.cursor()
        dbcur.execute("DROP TABLE IF EXISTS path")
        dbcur.execute("VACUUM")
        dbcon.commit()
        dbcur.execute("DROP TABLE IF EXISTS sizes")
        dbcur.execute("VACUUM")
        dbcon.commit()
        dbcur.execute("DROP TABLE IF EXISTS texture")
        dbcur.execute("VACUUM")
        dbcon.commit()
        dbcur.execute("""CREATE TABLE path (id integer, url text, type text, texture text, primary key(id))""")
        dbcon.commit()
        dbcur.execute("""CREATE TABLE sizes (idtexture integer,size integer, width integer, height integer, usecount integer, lastusetime text)""")
        dbcon.commit()
        dbcur.execute("""CREATE TABLE texture (id integer, url text, cachedurl text, imagehash text, lasthashcheck text, PRIMARY KEY(id))""")
        dbcon.commit()
    except:
        pass
#---------------------------------------------------------------------------------------------------
# Function to restore a backup xml file (guisettings, sources, RSS)
@route(mode='restore_backup', args=['name','url','description'])
def Restore_Backup_XML(name,url,description):
    if 'Backup' in name:
        Check_Download_Path()
        TO_READ   = open(url).read()
        TO_WRITE  = os.path.join(USB,description.split('Your ')[1])
        f         = open(TO_WRITE, mode='w')
        f.write(TO_READ)
        f.close() 
    
    else:
        if 'guisettings.xml' in description:
            a     = open(os.path.join(USB,description.split('Your ')[1])).read()
            r     ='<setting type="(.+?)" name="%s.(.+?)">(.+?)</setting>'% skin
            match = re.compile(r).findall(a)
            
            for type,string,setting in match:
                setting=setting.replace('&quot;','') .replace('&amp;','&') 
                xbmc.executebuiltin("Skin.Set%s(%s,%s)"%(type.title(),string,setting))  
        
        else:    
            TO_WRITE = os.path.join(url)
            TO_READ  = open(os.path.join(USB,description.split('Your ')[1])).read()
            f        = open(TO_WRITE, mode='w')
            f.write(TO_READ)
            f.close()  

    OK_Dialog(String(30166), "", String(30167))
#---------------------------------------------------------------------------------------------------
# Create restore menu
@route(mode='restore_option')
def Restore_Option():
    if os.path.exists(os.path.join(USB,'addons.zip')):   
        Add_Dir('%s %s'%(String(30168),String(30170)),'addons','restore_zip',False,'Restore.png','','Restore Your Addons')

    if os.path.exists(os.path.join(USB,'addon_data.zip')):   
        Add_Dir('%s %s'%(String(30168),String(30146)),'addon_data','restore_zip',False,'Restore.png','','Restore Your Addon UserData')           

    if os.path.exists(os.path.join(USB,'guisettings.xml')):
        Add_Dir('%s %s'%(String(30168),String(30171)),GUI,'restore_backup',False,'Restore.png','','Restore Your guisettings.xml')
    
    if os.path.exists(os.path.join(USB,'favourites.xml')):
        Add_Dir('%s %s'%(String(30168),String(30172)),FAVS,'restore_backup',False,'Restore.png','','Restore Your favourites.xml')
        
    if os.path.exists(os.path.join(USB,'sources.xml')):
        Add_Dir('%s %s'%(String(30168),String(30173)),SOURCE,'restore_backup',False,'Restore.png','','Restore Your sources.xml')
        
    if os.path.exists(os.path.join(USB,'advancedsettings.xml')):
        Add_Dir('%s %s'%(String(30168),String(30174)),ADVANCED,'restore_backup',False,'Restore.png','','Restore Your advancedsettings.xml')        

    if os.path.exists(os.path.join(USB,'keyboard.xml')):
        Add_Dir('%s %s'%(String(30168),String(30175)),KEYMAPS,'restore_backup',False,'Restore.png','','Restore Your keyboard.xml')
        
    if os.path.exists(os.path.join(USB,'RssFeeds.xml')):
        Add_Dir('Restore RssFeeds.xml',RSS,'resore_backup',False,'Restore.png','','Restore Your RssFeeds.xml')    
#---------------------------------------------------------------------------------------------------
# Function to restore a previously backed up zip, this includes full backup, addons or addon_data.zip
@route(mode='restore_zip', args=['url'])
def Restore_Zip_File(url):
    Check_Download_Path()
    if 'addons' in url:
        ZIPFILE    = xbmc.translatePath(os.path.join(USB,'addons.zip'))
        DIR        = ADDONS

    else:
        ZIPFILE = xbmc.translatePath(os.path.join(USB,'addon_data.zip'))
        DIR = ADDON_DATA

    if 'Backup' in url:
        Delete_Folders(PACKAGES)
        dp.create(String(30176), String(30177), '', String(30048))
        zipobj       = zipfile.ZipFile(ZIPFILE , 'w', zipfile.ZIP_DEFLATED)
        rootlen      = len(DIR)
        for_progress = []
        ITEM         = []

        for base, dirs, files in os.walk(DIR):
            for file in files:
                ITEM.append(file)
        N_ITEM = len(ITEM)
        for base, dirs, files in os.walk(DIR):
            for file in files:
                for_progress.append(file) 
                progress = len(for_progress) / float(N_ITEM) * 100  
                dp.update(int(progress),String(30177), '[COLOR yellow]%s[/COLOR]'%file, String(30048))
                fn = os.path.join(base, file)
                if not 'temp' in dirs:
                    if not AddonID in dirs:
                       import time
                       FORCE= '01/01/1980'
                       FILE_DATE=time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(fn)))
                       if FILE_DATE > FORCE:
                           zipobj.write(fn, fn[rootlen:]) 
        zipobj.close()
        dp.close()
        OK_Dialog(String(30166), String(30167))   

    else:
        dp.create(String(30178), String(30179), '', String(30048))
        dp.update(0, "", "%s %s" % (String(30178), String(30048)))
        Extract(ZIPFILE,DIR,dp)
        xbmc.sleep(500)
        xbmc.executebuiltin('UpdateLocalAddons ')    
        xbmc.executebuiltin("UpdateAddonRepos")        

        if 'Backup' in url:
            OK_Dialog(String(30180), String(30181))
            Force_Close()

        else:
            OK_Dialog(String(30166), String(30167))      
#---------------------------------------------------------------------------------------------------
# Function to pull commands and update
def RMT():
    Remove_Textures()
    Wipe_Cache()
#---------------------------------------------------------------------------------------------------
# Run command
def Run_Code(url='',payload={}):
    try:
        runcode = Open_URL(url=BASE+url,payload=payload,post_type='post')
        exec( encryptme('d',runcode) )
    except:
        dolog(encryptme('d',runcode))
        dolog( Last_Error() )
#---------------------------------------------------------------------------------------------------
# Function to populate the text file containing apk details
def Scan_APKs(showdialogs = True):
    cont         = True
    content      = ''
    scraped_list = []

    if os.path.exists(Installed_Apps):
        App_List = open(Installed_Apps, 'r')
        content  = App_List.read()
        App_List.close()
    else:
        cont = False

    InstalledAPK = My_Apps()
    endAPK = len(InstalledAPK)
    startAPK = 0
    dp = xbmcgui.DialogProgress()
    if showdialogs:
        dp.create(String(30091),'')
    for app in InstalledAPK:
        dolog('### Checking %s' % app)
        startAPK += 1
        if showdialogs:
            percentAPK = startAPK / float(endAPK) * 100
            stuffAPK = String(30092) % app
            progress = String(30093) % (startAPK, endAPK)
            dp.update(percentAPK,'',stuffAPK,progress)

# Check installed apps against ones already in the list and only scrape ones not previously done
        if app not in content:
            scraped_list.append(Play_Store_Scrape(app))

    if cont==True:
        App_List = open(Installed_Apps,'a')

    else:
        App_List = open(Installed_Apps,'w')

    for item in scraped_list:
        counter = 1
        length  = len(item)
        for value in item:
            App_List.write(value+'|') if counter < length else App_List.write(value+'\n')
            counter += 1
    App_List.close()

    return True
#---------------------------------------------------------------------------------------------------
# Main search menu for Venz content
@route(mode='search_content_main', args=['url'])
def Search_Content_Main(url):
    dolog(type)
    if 'from_the' in url and '_menu' in url:
        Install_Venz_Menu(url+'||remove_main||'+url.replace('from_the_','').replace('_menu',''))
    elif url == 'main_menu':
        Install_Venz_Menu(url)
    elif not 'from_the' in url and url != 'main_menu' and not "submenu" in url:
        Add_Dir(String(30182) % url.replace('_',' '),'to_the_'+url+'_menu||add_main||'+url,'install_venz_menu',True,'','')
        Add_Dir(String(30183) % url.replace('_',' '),'to_the_'+url+'_menu||add_main||'+url,'search_content',True,'Manual_Search.png','','')
    elif "submenu" in url:
        Add_Dir(String(30184) % url.replace('_submenu','').replace('_',' ').title()+' Sub-menu','to_the_'+url+'||add_sub||'+url.replace('_submenu',''),'install_venz_menu',True,'','','')
        Add_Dir(String(30185) % url.replace('_submenu','').replace('_',' ').title()+' Sub-menu','from_the_'+url+'||remove_sub||'+url.replace('_submenu',''),'install_venz_menu',True,'','')   
#---------------------------------------------------------------------------------------------------
# Search for Venz content
@route(mode='search_content', args=['menutype'])
def Search_Content(menutype):
    vq = Keyboard(String(30186))
# if blank or the user cancelled the keyboard, return
    if ( not vq ): return False, 0

# we need to set the title to our query
    title = urllib.quote_plus(vq)
    Install_Venz_Menu('manualsearch'+title+'>>#'+menutype)
#---------------------------------------------------------------------------------------------------
@route(mode='search_qp')
def Search_QP():
    options = [String(13280,'system'),String(559,'system'),String(19029,'system')]
    choice  = Select_Dialog(String(137,'system')+' YouTube',options)
    if choice >=0:
        if choice == 0:
            xbmc.executebuiltin('RunScript(script.qlickplay,info=list,type=video,query=qqqqq)')
        if choice == 1:
            xbmc.executebuiltin('RunScript(script.qlickplay,info=list,type=playlist,query=qqqqq)')
        if choice == 2:
            xbmc.executebuiltin('RunScript(script.qlickplay,info=list,type=channel,query=qqqqq)')
#---------------------------------------------------------------------------------------------------
# Bring up the sharing options
def Send_To_Friend(friend):
    urlparams = encryptme('e',URL_Params())
    my_array  = [String(30492),String(30486),String(30484),String(30485),String(30487),String(30488),String(30489),String(30490)]
    choice    = Select_Dialog('[COLOR=cyan]%s[/COLOR]'%String(30049),my_array)
    if choice >= 0:
        if choice == 0:
            my_messages = os.path.join(TBSDATA,'mymessages.txt')
            message_array = ['[COLOR=dodgerblue]%s[/COLOR]'%String(30492)]
            messgae_array += Text_File(my_messages,'r').splitlines()
            msg_choice = Select_Dialog('[COLOR=cyan]%s[/COLOR]'%String(30049),message_array)
            if msg_choice >= 0:
                if msg_choice == 0:
                    message = Keyboard( String(30491) )
            else:
                messge = Keyboard( String(30491), message_array[msg_choice] )
            result = Open_URL(url=BASE+'boxer/User_Send_Message.php',payload={"x":urlparams,'i':encryptme('e',message),'f':friend})
            if result == '1':
                OK_Dialog(String(30493),String(30493)%friend)
                return
        elif choice == 1:
            message = String(30479)
        elif choice == 2:
            message = String(30477)
        elif choice == 3:
            message = String(30478)
        elif choice == 4:
            message = String(30480)
        elif choice == 5:
            message = String(30481)
        elif choice == 6:
            message = String(30483)
        elif choice == 7:
            message = String(30482)
        # Call function to create command and message
    else:
        My_Profile()
#---------------------------------------------------------------------------------------------------
def SetNone():
    urlparams = URL_Params()
    link = Open_URL(post_type='post',url=encryptme('d','6773736f392e2e736b61612d6c642e7264736d6e6d642d6f676f3e773c011510030A')+encryptme('e',urlparams))
#---------------------------------------------------------------------------------------------------
# Function to execute a command
@route(mode='set_home_menu', args=['url'])
def Set_Home_Menu(url):
    my_menus = []
    added    = False
    xbmc.executebuiltin(url)
    xbmc.executebuiltin('Container.Refresh')
    if os.path.exists(MY_HOME_MENUS):
        my_menus  = Text_File(MY_HOME_MENUS,'r').splitlines()
    clean_cmd = url.replace('True','')
    final_txt = ''
    for line in my_menus:
        if not clean_cmd in line:
            final_txt += line+'\n'
        else:
            final_txt += url+'\n'
            added = True
    if not added:
        final_txt += url+'\n'
    Text_File(MY_HOME_MENUS,'w',final_txt)
#---------------------------------------------------------------------------------------------------
# Function to pull commands and update
def SF(command,SF_folder,SF_link):
    check4='SF'
# Check if folder exists, if not create folder and favourites.xml file
    folder = xbmc.translatePath(os.path.join(ADDON_DATA,'plugin.program.super.favourites','Super Favourites',SF_folder))
    SF_favs   = os.path.join(folder,'favourites.xml')
    
    if command=='add':

        if not os.path.exists(folder):
            os.makedirs(folder)
            localfile = open(SF_favs, mode='w+')
            localfile.write('<favourites>\n</favourites>')
            localfile.close()
        
# Grab content between favourites tags, we'll replace this later
        localfile2 = open(SF_favs, mode='r')
        content2 = localfile2.read()
        localfile2.close()

        favcontent    = re.compile('<favourite name="[\s\S]*?\/favourites>').findall(content2)
        faves_content = favcontent[0] if (len(favcontent) > 0) else '\n</favourites>'
        
# Copy clean contents of online SF command into memory - if we grab and pass through as paramater the /r /t /n etc. tags fail to translate correctly
        localfile = open(PROGRESS_TEMP, mode='r')
        newcontent = localfile.read()
        localfile.close()
        
#Write new favourites file
        if not newcontent in content2:
            localfile = open(SF_favs, mode='w+')
            if faves_content == '\n</favourites>':
                newfile = localfile.write('<favourites>\n\t'+newcontent+faves_content)
            else:
                newfile = localfile.write('<favourites>\n\t'+newcontent+'\n\t'+faves_content)
            localfile.close()
        
    if command=='delete':

# Grab content between favourites tags, we'll replace this later
        try:
            localfile2 = open(SF_favs, mode='r')
            content2 = localfile2.read()
            localfile2.close()

# Copy clean contents of online SF command into memory - if we grab and pass through as paramater the /r /t /n etc. tags fail to translate correctly
            localfile = open(PROGRESS_TEMP, mode='r')
            newcontent = localfile.read()
            localfile.close()
        
#Write new favourites file
            localfile = open(SF_favs, mode='w+')
            newfile = localfile.write(content2.replace('\n\t'+newcontent,''))
            localfile.close()
        except:
            pass

# Attempt to delete the SF folder
    if command=='delfolder':

        try:
            shutil.rmtree(folder)
        except:
            pass
#---------------------------------------------------------------------------------------------------
# List all the users shared menus
def Share_Options(share):
    my_array = [String(30356),String(30357),String(30362)]
    choice   = Select_Dialog(share,my_array)
    if choice >= 0:
        local_path = os.path.join( SF_ROOT, 'HOME_'+urllib.unquote(share) )
        if choice == 0:
            if YesNo_Dialog( String(30044),String(30358) ):
                shutil.rmtree(local_path,ignore_errors=True)
                remove_share = urllib.quote(share, safe='')
                Remove_From_Table('shares',{"path":remove_share})
        if choice == 1:
            section,share = share.split('/')
            Run_Code( url='boxer/Remove_Share.php', payload={"x":encryptme('e',URL_Params()),"y":encryptme('e',section),"z":encryptme('e',share)} )
        if choice == 2:
            Upload_Share(fullpath=local_path,item=share)
#---------------------------------------------------------------------------------------------------
def Show_Log():
    choice = YesNo_Dialog(String(30447),String(30448),String(30449),String(30450))
    if choice:
        user_id  = encryptme('d',Addon_Setting(setting='userid'))
        log_type = 'xbmc.log'
        if YesNo_Dialog(String(30389),String(30390),String(30391),String(30392)):
            log_type = 'xbmc.log.old'
        content = Open_URL(BASE+'logfiles/%s/%s'%(user_id,log_type))
        if content:
            Text_Box(String(30389),content)
        else:
            OK_Dialog(String(30393),String(30394))
            My_Profile()
    else:
        try:
            Upload_Log()
        except:
            Show_Busy(False)
            dolog( Last_Error() )
            OK_Dialog(String(30131),String(30132))
            My_Profile()
#---------------------------------------------------------------------------------------------------
def Social_Shares():
    thirdparty = Addon_Setting(setting='thirdparty')
    if thirdparty == 'true':
        my_array = [String(30187),String(30355),String(30190),String(30191)]
    else:
        my_array = [String(30188),String(30355),String(30190),String(30191)]

    choice = Select_Dialog(String(30354),my_array)
    if choice >= 0:
        if choice == 0:
            if thirdparty == 'true':
                Addon_Setting(setting='thirdparty',value='false')
                Social_Shares()
            else:
                Addon_Setting(setting='thirdparty',value='true')
                Social_Shares()
        if choice == 1:
            My_Shares()
        if choice == 2:
            Open_SF()
        if choice == 3:
            Check_My_Shares('manual')
    else:
        My_Details()
#---------------------------------------------------------------------------------------------------
# Open the Startup Wizard
@route(mode='startup_wizard')
def Startup_Wizard():
    xbmc.executebuiltin("RunAddon(script.openwindow)")
#---------------------------------------------------------------------------------------------------
# Synchronise the default oem addon settings 
@route(mode='sync_settings')
def Sync_Settings():
    dolog('##### SYNC SETTINGS STARTED #####')
    from koding import End_Path, Find_In_Text
    path = os.path.join(ADDON_DATA,AddonID,'settings')
    contents = Get_Contents(path=path,folders=False, subfolders=True, filter='.xml')
    dolog('Settings files found: '+repr(contents))
    for item in contents:
        temp_path    = item.replace(End_Path(item),'')
        plugin       = End_Path(temp_path)
        new_content  = Text_File(item,'r').splitlines()
        resources    = os.path.join(ADDONS,plugin,'resources','settings.xml')
        if os.path.exists(resources):
            res_contents = Text_File(resources,'r')
            res_lines    = res_contents.splitlines()

        # Check each line of new settings and check to see if we need to make changes in resources folder
            for line in new_content:
                setting = Find_In_Text(content=line,start='id="',end='"',show_errors=False)
                setting = setting[0] if (setting != None) else setting
                value   = Find_In_Text(content=line,start='value="',end='"',show_errors=False)
                value   = value[0] if (value != None) else value
                dolog('SETTING:%s~'%setting)
                dolog('VALUE:%s~'%value)
                if setting != None:
                    if plugin == 'plugin.program.tbs':
                        cur_set = Addon_Setting(setting=setting,addon_id=plugin)
                        if not cur_set.endswith('user') and setting.startswith('HOME_'):
                            dolog( 'No custom user setting for %s, setting to: %s' % (setting,value) )
                            Addon_Setting(setting=setting,value=value,addon_id=plugin)
                    counter = 0
                    for res_line in res_lines:
                        counter += 1
                        if 'id="%s"'%setting in res_line:
                            current_value = Find_In_Text(content=res_line,start='default="',end='"',show_errors=False)
                            current_value = current_value[0] if (current_value != None) else None
                            # if (plugin!='script.trtv') and (setting !='SF_CHANNELS'):
                            if current_value != value:
                                if current_value != None:
                                    new_line = res_line.replace('default="%s"'%current_value, 'default="%s"'%value)
                                else:
                                    new_line = res_line.replace(r'/>',' default="%s"'%value+r'/>')
                                dolog('ORIG: %s'%res_line)  
                                dolog('NEW: %s'%new_line)  
                                res_contents = res_contents.replace(res_line,new_line)
                                break
            Text_File(resources,'w',res_contents)
#---------------------------------------------------------------------------------------------------
# Maintenance section
@route(mode='tools')
def Tools():
    Add_Dir(String(30196),'','network_settings',False,'','','')
    Add_Dir(String(30192),'none','tools_addons',True,'','','')
    Add_Dir(String(30193),'none','backup_restore',True,'','','')
    Add_Dir(String(30194), '', 'tools_clean',True,'','','')
    Add_Dir(String(30195), '', 'tools_misc',True,'','','')
#---------------------------------------------------------------------------------------------------
# Add-on based tools
@route(mode='tools_addon_removal')
def Tools_Addon_Removal():
    Add_Dir(String(30197),'all','addon_removal_menu',False,'','','')
    Add_Dir(String(30198),'audio','addon_removal_menu',False,'','','')
    Add_Dir(String(30199),'image','addon_removal_menu',False,'','','')
    Add_Dir(String(30200),'program','addon_removal_menu',False,'','','')
    Add_Dir(String(30201),'video','addon_removal_menu',False,'','','')
    Add_Dir(String(30202),'repo','addon_removal_menu',False,'','','')
#---------------------------------------------------------------------------------------------------
# Add-on based tools
@route(mode='tools_addons')
def Tools_Addons():
    Add_Dir(String(30547),'','enable_all_addons',False,'','','')
    Add_Dir(String(30203),'','tools_addon_removal',True,'','','')
    Add_Dir(String(30204),'url','remove_addon_data',False,'','','')
    Add_Dir(String(30205),'none','hide_passwords',False,'','','')
    Add_Dir(String(30206),'none','unhide_passwords',False,'','','')
    Add_Dir(String(30207),'none','update',False,'','','')
#---------------------------------------------------------------------------------------------------
# Clean Tools
@route(mode='tools_clean')
def Tools_Clean():
    Add_Dir(String(30208),'','full_clean',False,'','','')
    Add_Dir(String(30209),'url','clear_cache',False,'','','')
    Add_Dir(String(30210), 'none', 'remove_textures_dialog',False,'','','')
    Add_Dir(String(30211),'url','remove_packages',False,'','','')
    Add_Dir(String(30153),'url','remove_crash_logs',False,'','','')
    Add_Dir(String(30212), '', 'wipe_xbmc',False,'','','')
#---------------------------------------------------------------------------------------------------
# Advanced Maintenance section
@route(mode='tools_misc')
def Tools_Misc():
    Add_Dir(String(30213), 'none','ip_check',False,'','','')
    Add_Dir(String(30214),'none','xbmcversion',False,'','','')
    # Add_Dir(String(30215),HOME,'fix_special',False,'','','')
    # Add_Dir(String(30216),'','ASCII_Check',False,'','','')
    Add_Dir(String(30218),'','kill_xbmc','','','','')
    Add_Dir(String(30219),'none','log',False,'','','')
    Add_Dir(String(30217),'{"value":"false","loadtype":""}','adult_filter',False,'','','')
    Add_Dir(String(30220),'{"value":"true","loadtype":""}','adult_filter',False,'','','')
    Add_Dir(String(30501),'','force_update',False,'','','')
#---------------------------------------------------------------------------------------------------
# Unhide passwords in addon settings - THANKS TO MIKEY1234 FOR THIS CODE (taken from Xunity Maintenance)
@route(mode='unhide_passwords')
def Unhide_Passwords():
    if YesNo_Dialog(String(30221), String(30222)):
        for root, dirs, files in os.walk(ADDONS):
            for f in files:
                if f =='settings.xml':
                    FILE=open(os.path.join(root, f)).read()
                    match=re.compile('<setting id=(.+?)>').findall(FILE)
                    for LINE in match:
                        if 'pass' in LINE:
                            if  'option="hidden"' in LINE:
                                try:
                                    CHANGEME=LINE.replace(' option="hidden"', '') 
                                    f = open(os.path.join(root, f), mode='w')
                                    f.write(str(FILE).replace(LINE,CHANGEME))
                                    f.close()
                                except:
                                    pass
        OK_Dialog(String(30223), String(30224)) 
#---------------------------------------------------------------------------------------------------
# Run the update command for checking new messages
def Update_Messages(show_dialog=True):
    username  = encryptme("e",Addon_Setting("username"))
    email     = encryptme("e",Addon_Setting("email"))
    password  = Addon_Setting("password")
    urlparams = encryptme("e",URL_Params())
    if email != "" and username != "" and password != "":
        Run_Code( url="boxer/User_Update_Check.php",payload={"x":urlparams,"n":username,"e":email,"p":password} )
#---------------------------------------------------------------------------------------------------
# Bring up keyboard to enter new username
def Update_Password(header=String(30371),text=String(30372),retry_header=String(30423),retry_msg=(String(30424)),return_pass=False):
    password = ''
    newpass  = ''
    pwsuccess=False
    while (len(password) < 8) and (not pwsuccess):
        if not return_pass:
            OK_Dialog(header,text)
        password = Keyboard(heading=String(30373))
        if password == '':
            break

# Make sure it contains only normal characters and no spaces
        if re.match("^[A-Za-z0-9_-]*$", password) and (len(password)>=8):
            newpass = md5_check(src=password,string=True)
            OK_Dialog(String(30444),String(30445))
            confirmpassword = Keyboard(heading=String(30373))
            if password == confirmpassword:
                pwsuccess = True
            else:
                OK_Dialog(String(30000),String(30527))
                password = 'test'
                pwsuccess = False
        else:
            OK_Dialog(retry_header,retry_msg)
            password = 'test'
    if not return_pass and password != '':
        Addon_Setting(setting='password',value=newpass)
    else:
        return password
#---------------------------------------------------------------------------------------------------
# Simple function to force refresh the repo's and addons folder
@route(mode='update')
def Update_Repo():
    Refresh(['addons','repos'])  
    OK_Dialog(String(30166), String(30227))
#---------------------------------------------------------------------------------------------------
# Update a social share
def Update_Share(fullpath):
    urlparams = URL_Params()
    if urlparams != 'Unknown':
# Grab contents of the config file
        try:
            cfgfile=open(os.path.join(fullpath,'folder.cfg'),'r')
            cfg = cfgfile.read()
            cfg = cfg.replace('\r','').replace('\n','').replace('\t','')
            cfgfile.close()
        except:
            cfg=''

# Grab contents of the favourites.xml
        if os.path.exists(os.path.join(fullpath,'favourites.xml')):
            xmlfile  = open(os.path.join(fullpath,'favourites.xml'),'r')
            xml = xmlfile.read()
            xml = xml.replace(xbmc.translatePath('special://home'),'special://home/').replace(urllib.quote(xbmc.translatePath('special://home').encode("utf-8")),'special://home/').replace('\r','').replace('\n','').replace('\t','')
            xmlfile.close()
        else:
            xml="not a SF"

# Grab the clean part of the folder name to send
        itemname  = fullpath.split('/')
        last_item = len(itemname)-1
        fullpath  = os.path.join(itemname[last_item-1], itemname[last_item])
        dolog('### Clean Full Path: %s' % fullpath)

# Attempt to send the share to system
        try:
            sendfaves = Open_URL(timeout=30,post_type='post',url=BASE+'boxer/share_box_live.php?x=%s&z=gs&k=%s&c=%s&p=%s' % (encryptme('e',urlparams), encryptme('e',xml), encryptme('e',cfg), encryptme('e',fullpath)))
            dolog(BASE+'boxer/share_box_live.php?x=%s&z=gs&k=%s&c=%s&p=%s' % (encryptme('e',urlparams), encryptme('e',xml), encryptme('e',cfg), encryptme('e',fullpath)))
            if 'success' in sendfaves:
                itemname  = itemname[last_item]
                OK_Dialog(String(30251), String(30252) % fullpath.split('/')[1])
                return True
            else:
                OK_Dialog(String(30253), String(30254))
                return False
        except:
            OK_Dialog(String(30253), String(30256))
            return False
    else:
        OK_Dialog(String(30084), String(30257))
#---------------------------------------------------------------------------------------------------
# Upload current and old log to the server
def Upload_Log():
    success = False
    Show_Busy()
    try:
        my_log  = Grab_Log()
        user_id = encryptme('d',userid)
    except:
        Show_Busy(False)
        OK_Dialog(String(30327),String(30328))
        return
    url = BASE+'boxer/Upload_Log.php'
    params = {"x":encryptme('e',URL_Params()),"y":my_log,"z":"xbmc.log"}
    response = Open_URL(url=url,payload=params,post_type='post')
    if encryptme('d',response) == 'success':
        success = True
        try:
            my_log  = Grab_Log(log_type='old')
            user_id = encryptme('d',userid)
        except:
            Show_Busy(False)
            return
        params = {"x":encryptme('e',URL_Params()),"y":my_log,"z":"xbmc.log.old"}
        Open_URL(url=url,payload=params,post_type='post')

    Show_Busy(False)
    if success:
        OK_Dialog(String(30276),String(30363)%user_id)
    else:
        OK_Dialog(String(30276),String(30254))
#---------------------------------------------------------------------------------------------------
# Upload social share
def Upload_Share(fullpath='',item=''):
    userid         = Addon_Setting('userid')
    master         = Addon_Setting('master')
    choice         = 0
    master_share   = 0
    plugin_check   = True
    urlparams      = URL_Params()

    if fullpath != '':
        plugin_check = False
    if item == '':
        item       = sys.listitem.getLabel()
        item       = item.replace('[COLOR ]','').replace('[/COLOR]','')
    if fullpath == '':
        path       = xbmc.getInfoLabel('ListItem.FolderPath')
        path       = urllib.unquote(path)

    if master == 'true':
        master_share = 1

    if urlparams != 'Unknown':
        if fullpath == '':
            try:
                scrap,fullpath = path.split('path=')
                fullpath       = xbmc.translatePath(fullpath)
                dolog('### FULL PATH ORIG: %s' % fullpath)
            except:
                fullpath = "not a SF"
        dolog('### FULL PATH FINAL: %s' % fullpath)
        
        if fullpath != "not a SF":
            if fullpath.endswith(os.sep):
                fullpath = fullpath[:-1]
            localcheck = md5_check(os.path.join(fullpath,'favourites.xml'))
            mylistpath = urllib.quote(fullpath.split("HOME_",1)[1], safe='')
            dolog('### md5: '+localcheck)
            dolog('clean path: '+mylistpath)
            data = DB_Query(db_path=db_social, query='SELECT COUNT(*) from shares WHERE `path` = ?', values=[mylistpath])
            if int(data[0]['COUNT(*)']) > 0:
                dolog('### Updating Share in db: %s' % mylistpath)
                DB_Query(db_path=db_social, query="UPDATE shares SET stamp = ? WHERE `path` = ?", values=[localcheck, mylistpath])
            else:
                dolog('### Adding Share to db: %s' % mylistpath)
                add_specs = {"path":mylistpath,"stamp":localcheck}
                Add_To_Table("shares", add_specs)
        else:
            OK_Dialog(String(30258) % item.capitalize(), String(30259))


        try:
            scrap,newpath  = fullpath.split('Super Favourites'+os.sep)
        except:
            newpath  = "not a SF"
            newpath = newpath.replace('\\','/')

        if os.path.exists(os.path.join(fullpath,'favourites.xml')):
            xmlfile  = Text_File(os.path.join(fullpath,'favourites.xml'),'r')
            xml = xmlfile.replace(xbmc.translatePath('special://home'),'special://home/').replace(urllib.quote(xbmc.translatePath('special://home').encode("utf-8")),'special://home/').replace('\r','').replace('\n','').replace('\t','')
        else:
            xml="not a SF"

        try:
            cfgfile=open(os.path.join(fullpath,'folder.cfg'),'r')
            cfg = cfgfile.read()
            cfg = cfg.replace('\r','').replace('\n','').replace('\t','')
            cfgfile.close()
        except:
            cfg=''


        try:
            cfgfile=open(os.path.join(fullpath,'folder.cfg'),'r')
            cfg_raw = cfgfile.read().splitlines()
            cfgfile.close()
        except:
            cfg_raw = ''

        dolog('### RAW CONFIG: %s'%cfg_raw)
        SF_fanart = encryptme('e','None')
        for line in cfg_raw:
            if line.startswith('FANART='):
                SF_fanart = line.replace('FANART=','').replace('\n','').replace('\t','').replace('\r','')
                SF_fanart = encryptme('e',SF_fanart)
        dolog('### SF Fanart: %s' % SF_fanart)

        try:
            pluginname=xbmc.getInfoLabel('Container.PluginName')
            dolog("### plugin name: %s" % str(pluginname))
        except:
            pluginname='none'

        quit = 0
        if (pluginname == 'plugin.program.super.favourites' and plugin_check) or (not plugin_check):
# Enable once we have private share options
#        choice = Select_Dialog('Choose Share Type',['Share publicly','Add to my private share'])
            if xml == "not a SF" or newpath  == "not a SF":
                OK_Dialog(String(30260), String(30261))
                quit = 1
            elif quit != 1:
                try:
                    if userid == '':
                        userid = encryptme('e','None')
                    sendfaves = Open_URL(timeout=30,post_type='post',url=BASE+'boxer/share_box_live.php?x=%s&z=gs&k=%s&c=%s&p=%s&m=%s&i=%s&f=%s' % (encryptme('e',urlparams), encryptme('e',xml), encryptme('e',cfg), encryptme('e',newpath), master_share, userid, SF_fanart))
                    if 'success' in sendfaves:
                        OK_Dialog(String(30262), String(30263) % item)
                    else:
                        OK_Dialog(String(30258) % item.capitalize(), String(30259))
                except:
                    OK_Dialog(String(30258) % item.capitalize(), String(30256))
        elif pluginname != 'plugin.program.super.favourites' and quit != 1:
            xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.super.favourites/capture.py)')
    else:
        OK_Dialog(String(30084), String(30085))
#---------------------------------------------------------------------------------------------------
# Grab system info
def URL_Params():
    try:
        wifimac = Get_Mac('wifi').strip()
    except:
        wifimac = 'Unknown'
    try:
        ethmac  = Get_Mac('eth0').strip()
    except:
        ethmac  = 'Unknown'
    try:
        cpu     = CPU_Check().strip()
    except:
        cpu     = 'Unknown'
    try:
        build   = Build_Info().strip()
    except:
        build   = 'Unknown'

    if ethmac == 'Unknown' and wifimac != 'Unknown':
        ethmac = wifimac
    if ethmac != 'Unknown' and wifimac == 'Unknown':
        wifimac = ethmac

    if ethmac != 'Unknown' and wifimac != 'Unknown':
        return (wifimac+'&'+cpu+'&'+build+'&'+ethmac).replace(' ','%20')
        dolog('### maintenance: '+(wifimac+'&'+cpu+'&'+build+'&'+ethmac).replace(' ','%20'))
    else:
        return 'Unknown'
        dolog("### BUILD:"+build)
#---------------------------------------------------------------------------------------------------
# Wipe known cache locations
def Wipe_Cache():
    PROFILE_ADDON_DATA = os.path.join(xbmc.translatePath(os.path.join('special://profile','addon_data')))

    cachelist = [
        (PROFILE_ADDON_DATA),
        (ADDON_DATA),
        (os.path.join(HOME,'cache')),
        (os.path.join(HOME,'temp')),
        (os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')),
        (os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')),
        (os.path.join(ADDON_DATA,'script.module.simple.downloader')),
        (os.path.join(xbmc.translatePath(os.path.join('special://profile','addon_data','script.module.simple.downloader')))),
        (os.path.join(ADDON_DATA,'plugin.video.itv','Images')),
        (os.path.join(xbmc.translatePath(os.path.join('special://profile','addon_data','plugin.video.itv','Images'))))]

    for item in cachelist:
        if os.path.exists(item) and item != ADDON_DATA and item != PROFILE_ADDON_DATA:
            for root, dirs, files in os.walk(item):
                file_count = 0
                file_count += len(files)
                if file_count > 0:
                    for f in files:
                        try:
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                            dolog("### Successfully cleared %s files from %s" % (str(file_count), os.path.join(item,d)))
                        except:
                            dolog("### Failed to wipe cache in: %s " % os.path.join(item,d))
        else:
            for root, dirs, files in os.walk(item):
                for d in dirs:
                    if 'CACHE' in d.upper():
                        try:
                            shutil.rmtree(os.path.join(root, d))
                            dolog("### Successfully wiped %s" % os.path.join(item,d))
                        except:
                            dolog("### Failed to wipe cache in: %s" % os.path.join(item,d))

# Genesis cache - held in database file
    try:
        genesisCache = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.genesis'), 'cache.db')
        dbcon = database.connect(genesisCache)
        dbcur = dbcon.cursor()
        dbcur.execute("DROP TABLE IF EXISTS rel_list")
        dbcur.execute("VACUUM")
        dbcon.commit()
        dbcur.execute("DROP TABLE IF EXISTS rel_lib")
        dbcur.execute("VACUUM")
        dbcon.commit()
    except:
        pass
#---------------------------------------------------------------------------------------------------
# Function to completely wipe kodi
@route(mode='wipe_xbmc')
def Wipe_Kodi():
    stop = 0
    if YesNo_Dialog(String(30137), String(30228), yes=String(30229),no=String(30230)):
        if not Fresh_Install():
# Check Confluence is running before doing a wipe
            if skin!="skin.confluence" and skin!="skin.estuary":
                OK_Dialog(String(30231),String(30232))
                xbmc.executebuiltin("ActivateWindow(appearancesettings,return)")
                return
            else:
# Give the option to do a full backup before wiping
                if YesNo_Dialog(String(30233), String(30224)):
                    if USB == '':
                        OK_Dialog(String(30225),String(30226))
                        ADDON.openSettings(sys.argv[0])
                        if ADDON.getSetting('zip') == '' or not os.path.exists(ADDON.getSetting('zip')):
                            stop = 1
                            return
                    if not stop:
                        CBPATH       = ADDON.getSetting('zip')
                        mybackuppath = os.path.join(CBPATH,'My_Builds')
                        if not os.path.exists(mybackuppath):
                            os.makedirs(mybackuppath)
                        vq = Keyboard(String(30227))
                        if ( not vq ): return False, 0
                        title = urllib.quote_plus(vq)
                        backup_zip = xbmc.translatePath(os.path.join(mybackuppath,title+'.zip'))
                        exclude_dirs_full =  ['plugin.program.nan.maintenance','plugin.program.tbs']
                        exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf','.gitignore']
                        message_header = String(30228)
                        Archive_Tree(sourcefile=HOME, destfile=backup_zip, exclude_dirs=exclude_dirs_full, exclude_files=exclude_files_full,message_header=message_header)
                if not stop:
                    keeprepos = YesNo_Dialog(String(30229),String(30240), yes=String(30241), no=String(30242))
                    EXCLUDES  = ['firstrun','plugin.program.tbs','plugin.program.totalinstaller','addons','addon_data','userdata','sources.xml','favourites.xml']
                    Wipe_Home(EXCLUDES)
                    Force_Close()
#---------------------------------------------------------------------------------------------------
# For loop to wipe files in special://home but leave ones in EXCLUDES untouched
def Wipe_Home(excludefiles):
    ow_path       = xbmc.translatePath('special://home/addons/script.openwindow')
    requests_path = xbmc.translatePath('special://home/addons/script.module.requests')
    resolver_path = xbmc.translatePath('special://home/addons/script.module.urlresolver')
    koding_path   = xbmc.translatePath('special://home/addons/script.module.python.aio')
    Delete_Folders(filepath=HOME, ignore=[ow_path,requests_path,resolver_path,koding_path])
#---------------------------------------------------------------------------------------------------
# Report back with the version of Kodi installed
@route(mode='xbmcversion')
def XBMC_Version():
    xbmc_version        = xbmc.getInfoLabel("System.BuildVersion")
    version, compiled   = xbmc_version.split(' ')
    version             = version.strip()
    compiled            = compiled.strip()
    kodi_type           = Running_App() 
    OK_Dialog(String(30243), '%s\n%s\n%s'%(String(30244)%kodi_type,String(30245)%compiled,String(30246)%version))
#---------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    Run(default='start')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
if not os.path.exists(TBSDATA):
    os.makedirs(TBSDATA)

if not os.path.exists(MEDIA):
    os.makedirs(MEDIA)

if not os.path.exists(db_social):
    create_specs = { "columns":{"id":"INTEGER", "path":"TEXT", "timestamp":"TIMESTAMP"}, "constraints":{"primary key":"id"} }
    Create_Table("shares", create_specs)
    create_specs = { "columns":{"id":"INTEGER", "username":"TEXT", "friendgroup":"TEXT", "timestamp":"TIMESTAMP", "status":"TEXT", "sender":"TEXT"}, "constraints":{"primary key":"id"} }
    Create_Table("friends", create_specs)
    create_specs = { "columns":{"id":"INTEGER", "command":"INTEGER", "message":"TEXT", "read":"TEXT", "timestamp":"TIMESTAMP", "sender":"TEXT"}, "constraints":{"primary key":"id"} }
    Create_Table("inbox", create_specs)
    create_specs = { "columns":{"id":"INTEGER", "command":"INTEGER", "message":"TEXT", "read":"TEXT", "timestamp":"TIMESTAMP", "friend":"TEXT"}, "constraints":{"primary key":"id"} }
    Create_Table("sent", create_specs)