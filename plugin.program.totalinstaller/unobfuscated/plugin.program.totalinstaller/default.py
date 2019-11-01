import urllib, urllib2, re, xbmcplugin, xbmcgui, xbmc, xbmcaddon
import os, sys, time, xbmcvfs, glob, shutil, datetime, zipfile, ntpath
import subprocess, threading
import yt, downloader, checkPath, uploadLog, skinSwitch
import binascii
import hashlib
import speedtest
import extract

try:
    import installapps
except:
    xbmc.log('### installapps not imported')

import pyxbmct.addonwindow as pyxbmct

try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database

######################################################
AddonID='plugin.program.totalinstaller'
AddonName='The Community Portal'
######################################################
ADDON            =  xbmcaddon.Addon(id=AddonID)
zip              =  ADDON.getSetting('zip')
backupinstall    =  ADDON.getSetting('backupinstall')
localcopy        =  ADDON.getSetting('localcopy')
privatebuilds    =  ADDON.getSetting('private')
keepfaves        =  ADDON.getSetting('favourites')
keepsources      =  ADDON.getSetting('sources')
keeprepos        =  ADDON.getSetting('repositories')
enablekeyword    =  ADDON.getSetting('enablekeyword')
keywordpath      =  ADDON.getSetting('keywordpath')
keywordname      =  ADDON.getSetting('keywordname')
mastercopy       =  ADDON.getSetting('mastercopy')
username         =  ADDON.getSetting('username').replace(' ','%20')
password         =  ADDON.getSetting('password')
versionoverride  =  ADDON.getSetting('versionoverride')
debug            =  ADDON.getSetting('debug')
login            =  ADDON.getSetting('login')
wizard           =  ADDON.getSetting('wizard')
wizardurl1       =  ADDON.getSetting('wizardurl1')
wizardname1      =  ADDON.getSetting('wizardname1')
wizardurl2       =  ADDON.getSetting('wizardurl2')
wizardname2      =  ADDON.getSetting('wizardname2')
wizardurl3       =  ADDON.getSetting('wizardurl3')
wizardname3      =  ADDON.getSetting('wizardname3')
wizardurl4       =  ADDON.getSetting('wizardurl4')
wizardname4      =  ADDON.getSetting('wizardname4')
wizardurl5       =  ADDON.getSetting('wizardurl5')
wizardname5      =  ADDON.getSetting('wizardname5')
kodiv            =  float(xbmc.getInfoLabel("System.BuildVersion")[:4])
dialog           =  xbmcgui.Dialog()
dp               =  xbmcgui.DialogProgress()
HOME             =  xbmc.translatePath('special://home/')
USERDATA         =  xbmc.translatePath('special://profile')
DATABASE         =  os.path.join(USERDATA, 'Database')
ADDON_DATA       =  os.path.join(USERDATA,'addon_data')
CP_PROFILE       =  os.path.join(HOME,'CP_Profiles')
ADDONS_MASTER    =  os.path.join(CP_PROFILE,'Master')
THUMBNAILS       =  os.path.join(USERDATA,'Thumbnails')
ADDONS           =  xbmc.translatePath(os.path.join('special://home','addons'))
KODI_ADDONS      =  xbmc.translatePath(os.path.join('special://xbmc','addons'))
CBADDONPATH      =  os.path.join(ADDONS,AddonID,'default.py')
FANART           =  os.path.join(ADDONS,AddonID,'fanart.jpg')
ICON             =  os.path.join(ADDONS,AddonID,'icon.png')
ADDONXMLTEMP     =  os.path.join(ADDONS,AddonID,'resources','addonxml')
ADDONXMLNAG      =  os.path.join(ADDONS,AddonID,'resources','skins','DefaultSkin','media','ttm')
bakdefault       =  os.path.join(ADDONS,AddonID,'resources','backup')
GUI              =  os.path.join(USERDATA,'guisettings.xml')
GUIFIX           =  os.path.join(USERDATA,'guifix.xml')
ARTPATH          =  'http://noobsandnerds.com/TI/art/'
defaulticon      =  os.path.join(ADDONS,AddonID,'icon.png')
FAVS             =  os.path.join(USERDATA,'favourites.xml')
SOURCE           =  os.path.join(USERDATA,'sources.xml')
ADVANCED         =  os.path.join(USERDATA,'advancedsettings.xml')
PROFILES         =  os.path.join(USERDATA,'profiles.xml')
RSS              =  os.path.join(USERDATA,'RssFeeds.xml')
KEYMAPS          =  os.path.join(USERDATA,'keymaps','keyboard.xml')
USB              =  xbmc.translatePath(os.path.join(zip))
CBPATH           =  os.path.join(USB,'Community_Builds','')
startuppath      =  os.path.join(ADDON_DATA,AddonID,'startup.xml')
tempfile         =  os.path.join(ADDON_DATA,AddonID,'temp.xml')
idfile           =  os.path.join(ADDON_DATA,AddonID,'id.xml')
idfiletemp       =  os.path.join(ADDON_DATA,AddonID,'idtemp.xml')
cookie           =  os.path.join(ADDON_DATA,AddonID,'temp')
ascii_results    =  os.path.join(ADDON_DATA,AddonID,'ascii_results')
ascii_results1   =  os.path.join(ADDON_DATA,AddonID,'ascii_results1')
ascii_results2   =  os.path.join(ADDON_DATA,AddonID,'ascii_results2')
GUIzipfolder     =  os.path.join(ADDON_DATA,AddonID,'guizip')
notifyart        =  os.path.join(ADDONS,AddonID,'resources/')
installfile      =  os.path.join(ADDONS,AddonID,'default.py')
skin             =  xbmc.getSkinDir()
log_path         =  xbmc.translatePath('special://logpath/')
backup_dir       =  '/storage/backup'
restore_dir      =  '/storage/.restore/'
userdatafolder   =  os.path.join(ADDON_DATA,AddonID)
GUINEW           =  os.path.join(userdatafolder,'guinew.xml')
guitemp          =  os.path.join(userdatafolder,'guitemp')
tempdbpath       =  os.path.join(USB,'Database')
packages         =  os.path.join(ADDONS,'packages')
temp_install     =  os.path.join(packages,'temp_install')
addonstemp       =  os.path.join(USERDATA,'addontemp')
backupaddonspath =  os.path.join(USERDATA,'.cbcfg')
EXCLUDES         =  ['firstrun','plugin.program.totalinstaller','addons','addon_data','userdata','sources.xml','favourites.xml','repository.noobsandnerds']
EXCLUDES2        =  ['firstrun','plugin.program.totalinstaller','addons','addon_data','userdata','sources.xml','favourites.xml','guisettings.xml','CP_Profiles','temp','repository.noobsandnerds']
localversioncheck=  '0'
ACTION_MOVE_UP   =  3
ACTION_MOVE_DOWN =  4
BACKUP_DIRS      =  ['/storage/.kodi','/storage/.cache','/storage/.config','/storage/.ssh']
artpath          =  os.path.join(ADDONS,AddonID,'resources')
checkicon        =  os.path.join(artpath,'check.png')
updateicon       =  os.path.join(artpath,'update.png')
unknown_icon     =  os.path.join(artpath,'update.png')
dialog_bg        =  os.path.join(artpath,'background.png')
black            =  os.path.join(artpath,'black.png')
#-----------------------------------------------------------------------------------------------------------------  
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
        time.sleep( .4 )
        self.close()
#-----------------------------------------------------------------------------------------------------------------    
# Add a standard directory for the builds. Essentially the same as above but grabs unique artwork from previous call
def Add_Build_Dir(name,url,mode,iconimage,fanart,video,description,skins,guisettingslink,artpack):
        u  = sys.argv[0]
        u += "?url="            +urllib.quote_plus(url)
        u += "&mode="           +str(mode)
        u += "&name="           +urllib.quote_plus(name)
        u += "&iconimage="      +urllib.quote_plus(iconimage)
        u += "&fanart="         +urllib.quote_plus(fanart)
        u += "&video="          +urllib.quote_plus(video)
        u += "&description="    +urllib.quote_plus(description)
        u += "&skins="          +urllib.quote_plus(skins)
        u += "&guisettingslink="+urllib.quote_plus(guisettingslink)
        u += "&artpack="        +urllib.quote_plus(artpack)
        
        ok  = True
        liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        liz.setProperty( "Build.Video", video )
        
        if (mode==None) or (mode=='restore_option') or (mode=='backup_option') or (mode=='cb_root_menu') or (mode=='genres') or (mode=='grab_builds') or (mode=='community_menu') or (mode=='instructions') or (mode=='countries') or (mode=='update_build') or (url==None) or (len(url)<1):

            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        
        return ok
#---------------------------------------------------------------------------------------------------
#Main Iiectory function - xbmcplugin.addDirectoryItem()
def Add_Directory_Item(handle, url, listitem, isFolder):
    xbmcplugin.addDirectoryItem(handle, url, listitem, isFolder)
#---------------------------------------------------------------------------------------------------
#Add a directory for the description, this requires multiple string to be called from previous menu
def Add_Desc_Dir(name,url,mode,iconimage,fanart,buildname,author,version,description,updated,skins,videoaddons,audioaddons,programaddons,pictureaddons,sources,adult):
#        iconimage = ARTPATH + iconimage
        iconimage = defaulticon
        
        u   = sys.argv[0]
        u += "?url="            +urllib.quote_plus(url)
        u += "&mode="           +str(mode)
        u += "&name="           +urllib.quote_plus(name)
        u += "&iconimage="      +urllib.quote_plus(iconimage)
        u += "&fanart="         +urllib.quote_plus(fanart)
        u += "&author="         +urllib.quote_plus(author)
        u += "&description="    +urllib.quote_plus(description)
        u += "&version="        +urllib.quote_plus(version)
        u += "&buildname="      +urllib.quote_plus(buildname)
        u += "&updated="        +urllib.quote_plus(updated)
        u += "&skins="          +urllib.quote_plus(skins)
        u += "&videoaddons="    +urllib.quote_plus(videoaddons)
        u += "&audioaddons="    +urllib.quote_plus(audioaddons)
        u += "&buildname="      +urllib.quote_plus(buildname)
        u += "&programaddons="  +urllib.quote_plus(programaddons)
        u += "&pictureaddons="  +urllib.quote_plus(pictureaddons)
        u += "&sources="        +urllib.quote_plus(sources)
        u += "&adult="          +urllib.quote_plus(adult)
        
        ok  = True
        liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        liz.setProperty( "Build.Video", video )
        
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        
        return ok
#---------------------------------------------------------------------------------------------------
def Add_Install_Dir(title,name,url,mode,iconimage = '',fanart = '',video = '',description = '',zip_link = '',repo_link = '',repo_id = '',addon_id = '',provider_name = '',forum = '',data_path = ''):
    if len(iconimage) > 0:
#        iconimage = ARTPATH + iconimage
        iconimage = iconimage
    else:
        iconimage = 'DefaultFolder.png'
    
    if fanart == '':
        fanart = FANART
    
    u   = sys.argv[0]
    u += "?url="            +urllib.quote_plus(url)
    u += "&zip_link="       +urllib.quote_plus(zip_link)
    u += "&repo_link="      +urllib.quote_plus(repo_link)
    u += "&data_path="      +urllib.quote_plus(data_path)
    u += "&provider_name="  +str(provider_name)
    u += "&forum="          +str(forum)
    u += "&repo_id="        +str(repo_id)
    u += "&addon_id="       +str(addon_id)
    u += "&mode="           +str(mode)
    u += "&name="           +urllib.quote_plus(name)
    u += "&fanart="         +urllib.quote_plus(fanart)
    u += "&video="          +urllib.quote_plus(video)
    u += "&description="    +urllib.quote_plus(description)
    
    ok  = True
    liz = xbmcgui.ListItem(title, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    
    liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
    liz.setProperty( "Fanart_Image", fanart )
    liz.setProperty( "Build.Video", video )
    
    Add_Directory_Item(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
#-----------------------------------------------------------------------------------------------------------------  
#Add a standard directory and grab fanart and iconimage from artpath defined in global variables
def addDir(type,name,url,mode,iconimage = '',fanart = FANART,video = '',description = ''):
    if not 'addon' in type:
        if len(iconimage) > 0:
            iconimage = ARTPATH + iconimage
        
        else:
            iconimage = defaulticon

    if 'addon' in type:
        if len(iconimage) > 0:
            iconimage = iconimage
        else:
            iconimage = 'DefaultFolder.png'
#            iconraw = '687474703a2f2f746f74616c78626d632e74762f6164646f6e732f63616368652f696d616765732f3463373933313938383765323430373839636131323566313434643938395f6164646f6e2d64756d6d792e706e67'
#            iconimage = binascii.unhexlify(iconraw)
    
    u   = sys.argv[0]
    u += "?url="            +urllib.quote_plus(url)
    u += "&mode="           +str(mode)
    u += "&name="           +urllib.quote_plus(name)
    u += "&iconimage="      +urllib.quote_plus(iconimage)
    u += "&fanart="         +urllib.quote_plus(fanart)
    u += "&video="          +urllib.quote_plus(video)
    u += "&description="    +urllib.quote_plus(description)
    
    #name = Colour_Text(name)

    ok  = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    
    liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
    liz.setProperty( "Fanart_Image", fanart )
    liz.setProperty( "Build.Video", video )
    if 'folder' in type:
        ok=Add_Directory_Item(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    
    else:
        ok=Add_Directory_Item(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    
    return ok
#---------------------------------------------------------------------------------------------------
# Add a nag screen on boot
def Add_Nag(name):
    timer = dialog.input('Enter amount of seconds to show startup notification for.', '30', type=xbmcgui.INPUT_NUMERIC)
    timer = str(int(timer)*1000)
    import base64
    path    = os.path.join(ADDONS,binascii.unhexlify('6d657461646174612e636f6d6d6f6e2e696d62642e636f6d'))
    xmlpath = os.path.join(path,'addon.xml')

    if not os.path.exists(path):
        os.makedirs(path)

    if not os.path.exists(os.path.join(path,'addon.xml')):
        shutil.copyfile(ADDONXMLNAG, xmlpath)

# Create the default.py which will run on startup
    content = "import xbmcgui, xbmc;xbmcgui.Dialog().ok('Message from "+name+" (Build Author)','If you paid for this build I regret to inform you that you may have been conned. This build is not available for resale.','You can get it for [COLOR=gold]FREE[/COLOR] @ [COLOR=dodgerblue]www.noobsandnerds.com[/COLOR]');xbmc.sleep(10000);xbmc.executebuiltin('XBMC.Notification(THIS BUILD IS NOT FOR RESALE!!!,If you paid contact the seller - its FREE,"+timer+")')"
    writefile = open(os.path.join(path,'default.py'),'w+')
    writefile.write("import base64;exec base64.b64decode('")
    encoded = base64.b64encode(content)
    writefile.write(encoded)
    writefile.write("')")
    writefile.close()
    
    writefile = open(os.path.join(path,'tag.cfg'),'w+')
    writefile.write(binascii.hexlify(name))
    writefile.close()
    xbmc.executebuiltin('Skin.SetString(TVDB_CFG,'+binascii.hexlify(name)+')')

    readfile = open(xmlpath,'r')
    content = readfile.read()
    readfile.close()
    replacefile = content.replace('testid',binascii.unhexlify('6d657461646174612e636f6d6d6f6e2e696d62642e636f6d')).replace('testname','imbd scraper').replace('testprovider','bytesize').replace('testdesc','imbd scraper')
    writefile = open(xmlpath,'w+')
    writefile.write(replacefile)
    writefile.close()

# Write filesize of default.py to guisettings
    checkfile = os.path.getsize(os.path.join(ADDONS,binascii.unhexlify('6d657461646174612e636f6d6d6f6e2e696d62642e636f6d'),'default.py'))
    xbmc.executebuiltin('Skin.SetString(WeatherCheck,'+str(checkfile)+')')
    xbmc.executebuiltin('Skin.SetString(TMDB_API,'+binascii.hexlify(replacefile)+')')

    readfile = open(os.path.join(path,'default.py'),'r')
    content = readfile.read()
    readfile.close()
    xbmc.executebuiltin('Skin.SetString(HashLib,'+binascii.hexlify(content)+')')
#---------------------------------------------------------------------------------------------------
# Build Categories Menu
def Addon_Categories(url):
    addDir('folder','[COLOR=yellow][PLUGIN][/COLOR] Audio',url+'&typex=audio','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','[COLOR=yellow][PLUGIN][/COLOR] Image',url+'&typex=image','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','[COLOR=yellow][PLUGIN][/COLOR] Program',url+'&typex=program','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','[COLOR=yellow][PLUGIN][/COLOR] Video',url+'&typex=video','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','[COLOR=lime][SCRAPER][/COLOR] Movies (Used for library scanning)',url+'&typex=movie%20scraper','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','[COLOR=lime][SCRAPER][/COLOR] TV Shows (Used for library scanning)',url+'&typex=tv%20show%20scraper','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','[COLOR=lime][SCRAPER][/COLOR] Music Artists (Used for library scanning)',url+'&typex=artist%20scraper','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','[COLOR=lime][SCRAPER][/COLOR] Music Videos (Used for library scanning)',url+'&typex=music%20video%20scraper','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','[COLOR=orange][SERVICE][/COLOR] All Services',url+'&typex=service','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','[COLOR=orange][SERVICE][/COLOR] Weather Service',url+'&typex=weather','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','[COLOR=skyblue][OTHER][/COLOR] Repositories',url+'&typex=repository','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','[COLOR=skyblue][OTHER][/COLOR] Scripts (Program Add-ons)',url+'&typex=executable','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','[COLOR=skyblue][OTHER][/COLOR] Screensavers',url+'&typex=screensaver','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','[COLOR=skyblue][OTHER][/COLOR] Script Modules',url+'&typex=script%20module','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','[COLOR=skyblue][OTHER][/COLOR] Skins',url+'&typex=skin','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','[COLOR=skyblue][OTHER][/COLOR] Subtitles',url+'&typex=subtitles','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','[COLOR=skyblue][OTHER][/COLOR] Web Interface',url+'&typex=web%20interface','grab_addons','mainmenu/addons.png','','','')
#    addDir('folder','Lyrics','&typex=lyrics','grab_addons','mainmenu/addons.png','','','')
#---------------------------------------------------------------------------------------------------
def Addon_Check_Updates():
    Update_Repo()
    xbmc.executebuiltin('ActivateWindow(10040,"addons://outdated/",return)')
#---------------------------------------------------------------------------------------------------
#Build Countries Menu   
def Addon_Countries(url):
    addDir('folder','African',url+'&genre=african','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Arabic',url+'&genre=arabic','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Asian',url+'&genre=asian','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Australian',url+'&genre=australian','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Austrian',url+'&genre=austrian','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Belgian',url+'&genre=belgian','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Brazilian',url+'&genre=brazilian','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Canadian',url+'&genre=canadian','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Chinese',url+'&genre=chinese','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Colombian',url+'&genre=columbian','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Croatian',url+'&genre=croatian','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Czech',url+'&genre=czech','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Danish',url+'&genre=danish','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Dominican',url+'&genre=dominican','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Dutch',url+'&genre=dutch','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Egyptian',url+'&genre=egyptian','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Filipino',url+'&genre=filipino','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Finnish',url+'&genre=finnish','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','French',url+'&genre=french','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','German',url+'&genre=german','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Greek',url+'&genre=greek','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Hebrew',url+'&genre=hebrew','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Hungarian',url+'&genre=hungarian','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Icelandic',url+'&genre=icelandic','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Indian',url+'&genre=indian','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Irish',url+'&genre=irish','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Italian',url+'&genre=italian','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Japanese',url+'&genre=japanese','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Korean',url+'&genre=korean','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Lebanese',url+'&genre=lebanese','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Mongolian',url+'&genre=mongolian','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Moroccan',url+'&genre=moroccan','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Nepali',url+'&genre=nepali','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','New Zealand',url+'&genre=newzealand','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Norwegian',url+'&genre=norwegian','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Pakistani',url+'&genre=pakistani','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Polish',url+'&genre=polish','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Portuguese',url+'&genre=portuguese','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Romanian',url+'&genre=romanian','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Russian',url+'&genre=russian','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Singapore',url+'&genre=singapore','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Spanish',url+'&genre=spanish','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Swedish',url+'&genre=swedish','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Swiss',url+'&genre=swiss','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Syrian',url+'&genre=syrian','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Tamil',url+'&genre=tamil','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Thai',url+'&genre=thai','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Turkish',url+'&genre=turkish','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','UK',url+'&genre=uk','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','USA',url+'&genre=usa','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Vietnamese',url+'&genre=vietnamese','grab_addons','mainmenu/addons.png','','','')
#---------------------------------------------------------------------------------------------------
# Check for the real log path, even makes exceptions for idiots who've left their old kodi logs in their builds
def Addons_DB_Check():
    finalfile = 0
    databasepath = os.listdir(DATABASE)
    for item in databasepath:
        if item.lower().endswith('.db') and item.lower().startswith('addons'):
            mydb         = os.path.join(DATABASE,item)
            lastmodified = os.path.getmtime(mydb)
            if lastmodified>finalfile:
                finalfile = lastmodified
                gooddb   = mydb
    return gooddb
#-----------------------------------------------------------------------------------------------------------------
# This creates the final menu showing build details, video and install link
def Addon_Final_Menu(url):
    BaseURL                = 'http://noobsandnerds.com/TI/AddonPortal/addondetails.php?id=%s' % (url)
    xbmc.log('BASE: %s'%BaseURL)
    link                   = Open_URL(BaseURL, 10).replace('\n','').replace('\r','')
#    approvedmatch          = re.compile('approved="(.+?)"').findall(link)
    contenttypematch       = re.compile('addon_types="(.+?)"').findall(link)
    namematch              = re.compile('name="(.+?)"').findall(link)
    UIDmatch               = re.compile('UID="(.+?)"').findall(link)
    idmatch                = re.compile('id="(.+?)"').findall(link)
    providernamematch      = re.compile('provider_name="(.+?)"').findall(link)
    versionmatch           = re.compile('version="(.+?)"').findall(link)
    createdmatch           = re.compile('created="(.+?)"').findall(link)
    contentmatch           = re.compile('addon_types="(.+?)"').findall(link)
    updatedmatch           = re.compile('updated="(.+?)"').findall(link)
    downloadsmatch         = re.compile('downloads="(.+?)"').findall(link)
#    xboxmatch             = re.compile('xbox_compatible="(.+?)"').findall(link)
    descriptionmatch       = re.compile('description="(.+?)"').findall(link)
    devbrokenmatch         = re.compile('devbroke="(.+?)"').findall(link)
    brokenmatch            = re.compile('broken="(.+?)"').findall(link)
    deletedmatch           = re.compile('deleted="(.+?)"').findall(link)
    notesmatch             = re.compile('mainbranch_notes="(.+?)"').findall(link)
#    xboxnotesmatch        = re.compile('xbox_notes="(.+?)"').findall(link)
    repourlmatch           = re.compile('repo_url="(.+?)"').findall(link)
    dataurlmatch           = re.compile('data_url="(.+?)"').findall(link)
    zipurlmatch            = re.compile('zip_url="(.+?)"').findall(link)
    genresmatch            = re.compile('genres="(.+?)"').findall(link)
    forummatch             = re.compile('forum="(.+?)"').findall(link)
    repoidmatch            = re.compile('repo_id="(.+?)"').findall(link)
    licensematch           = re.compile('license="(.+?)"').findall(link)
    platformmatch          = re.compile('platform="(.+?)"').findall(link)
    visiblematch           = re.compile('visible="(.+?)"').findall(link)
    scriptmatch            = re.compile('script="(.+?)"').findall(link)
    programpluginmatch     = re.compile('program_plugin="(.+?)"').findall(link)
    scriptmodulematch      = re.compile('script_module="(.+?)"').findall(link)
    videopluginmatch       = re.compile('video_plugin="(.+?)"').findall(link)
    audiopluginmatch       = re.compile('audio_plugin="(.+?)"').findall(link)
    imagepluginmatch       = re.compile('image_plugin="(.+?)"').findall(link)
    repositorymatch        = re.compile('repository="(.+?)"').findall(link)
    weatherservicematch    = re.compile('weather_service="(.+?)"').findall(link)
    skinmatch              = re.compile('skin="(.+?)"').findall(link)
    servicematch           = re.compile('service="(.+?)"').findall(link)
    warningmatch           = re.compile('warning="(.+?)"').findall(link)
    webinterfacematch      = re.compile('web_interface="(.+?)"').findall(link)
    moviescrapermatch      = re.compile('movie_scraper="(.+?)"').findall(link)
    tvscrapermatch         = re.compile('tv_scraper="(.+?)"').findall(link)
    artistscrapermatch     = re.compile('artist_scraper="(.+?)"').findall(link)
    musicvideoscrapermatch = re.compile('music_video_scraper="(.+?)"').findall(link)
    subtitlesmatch         = re.compile('subtitles="(.+?)"').findall(link)
    requiresmatch          = re.compile('requires="(.+?)"').findall(link)
    modulesmatch           = re.compile('modules="(.+?)"').findall(link)
    iconmatch              = re.compile('icon="(.+?)"').findall(link)
    videopreviewmatch      = re.compile('video_preview="(.+?)"').findall(link)
    videoguidematch        = re.compile('video_guide="(.+?)"').findall(link)
    videoguidematch1       = re.compile('video_guide1="(.+?)"').findall(link)
    videoguidematch2       = re.compile('video_guide2="(.+?)"').findall(link)
    videoguidematch3       = re.compile('video_guide3="(.+?)"').findall(link)
    videoguidematch4       = re.compile('video_guide4="(.+?)"').findall(link)
    videoguidematch5       = re.compile('video_guide5="(.+?)"').findall(link)
    videoguidematch6       = re.compile('video_guide6="(.+?)"').findall(link)
    videoguidematch7       = re.compile('video_guide7="(.+?)"').findall(link)
    videoguidematch8       = re.compile('video_guide8="(.+?)"').findall(link)
    videoguidematch9       = re.compile('video_guide9="(.+?)"').findall(link)
    videoguidematch10      = re.compile('video_guide10="(.+?)"').findall(link)
    videolabelmatch1       = re.compile('video_label1="(.+?)"').findall(link)
    videolabelmatch2       = re.compile('video_label2="(.+?)"').findall(link)
    videolabelmatch3       = re.compile('video_label3="(.+?)"').findall(link)
    videolabelmatch4       = re.compile('video_label4="(.+?)"').findall(link)
    videolabelmatch5       = re.compile('video_label5="(.+?)"').findall(link)
    videolabelmatch6       = re.compile('video_label6="(.+?)"').findall(link)
    videolabelmatch7       = re.compile('video_label7="(.+?)"').findall(link)
    videolabelmatch8       = re.compile('video_label8="(.+?)"').findall(link)
    videolabelmatch9       = re.compile('video_label9="(.+?)"').findall(link)
    videolabelmatch10      = re.compile('video_label10="(.+?)"').findall(link)

#Need to add if broken version > current version statement   
#    approved            = approvedmatch[0] if (len(approvedmatch) > 0) else ''
    contenttypes        = contenttypematch[0] if (len(contenttypematch) > 0) else ''
    name                = namematch[0] if (len(namematch) > 0) else ''
    UID                 = UIDmatch[0] if (len(UIDmatch) > 0) else ''
    addon_id            = idmatch[0] if (len(idmatch) > 0) else ''
    provider_name       = providernamematch[0] if (len(providernamematch) > 0) else ''
    version             = versionmatch[0] if (len(versionmatch) > 0) else ''
    created             = createdmatch[0] if (len(createdmatch) > 0) else ''
    content_types       = contentmatch[0] if (len(contentmatch) > 0) else ''
    updated             = updatedmatch[0] if (len(updatedmatch) > 0) else ''
    downloads           = downloadsmatch[0] if (len(downloadsmatch) > 0) else ''
#    xbox               = xboxmatch[0] if (len(xboxmatch) > 0) else ''
    desc                = '[CR][CR][COLOR=dodgerblue]Description: [/COLOR]'+descriptionmatch[0] if (len(descriptionmatch) > 0) else ''
    devbroken           = devbrokenmatch[0] if (len(devbrokenmatch) > 0) else ''
    broken              = brokenmatch[0] if (len(brokenmatch) > 0) else ''
    deleted             = '[CR]'+deletedmatch[0] if (len(deletedmatch) > 0) else ''
    notes               = '[CR][CR][COLOR=dodgerblue]User Notes: [/COLOR]'+notesmatch[0] if (len(notesmatch) > 0) else ''
#    xbox_notes         = xboxnotesmatch[0] if (len(xboxnotesmatch) > 0) else ''
    repo_url            = repourlmatch[0] if (len(repourlmatch) > 0) else ''
    data_url            = dataurlmatch[0] if (len(dataurlmatch) > 0) else ''
    zip_url             = zipurlmatch[0] if (len(zipurlmatch) > 0) else ''
    genres              = genresmatch[0] if (len(genresmatch) > 0) else ''
    forum               = '[CR][CR][COLOR=dodgerblue]Support Forum: [/COLOR]'+forummatch[0] if (len(forummatch) > 0) else '[CR][CR][COLOR=dodgerblue]Support Forum: [/COLOR]No forum details given by developer'
    forumclean          = forummatch[0] if (len(forummatch) > 0) else 'None'
    repo_id             = repoidmatch[0] if (len(repoidmatch) > 0) else ''
    license             = licensematch[0] if (len(licensematch) > 0) else ''
    platform            = '[COLOR=orange]     Platform: [/COLOR]'+platformmatch[0] if (len(platformmatch) > 0) else ''
    visible             = visiblematch[0] if (len(visiblematch) > 0) else ''
    script              = scriptmatch[0] if (len(scriptmatch) > 0) else ''
    program_plugin      = programpluginmatch[0] if (len(programpluginmatch) > 0) else ''
    script_module       = scriptmodulematch[0] if (len(scriptmodulematch) > 0) else ''
    video_plugin        = videopluginmatch[0] if (len(videopluginmatch) > 0) else ''
    audio_plugin        = audiopluginmatch[0] if (len(audiopluginmatch) > 0) else ''
    image_plugin        = imagepluginmatch[0] if (len(imagepluginmatch) > 0) else ''
    repository          = repositorymatch[0] if (len(repositorymatch) > 0) else ''
    service             = servicematch[0] if (len(servicematch) > 0) else ''
    skin                = skinmatch[0] if (len(skinmatch) > 0) else ''
    warning             = warningmatch[0] if (len(warningmatch) > 0) else ''
    web_interface       = webinterfacematch[0] if (len(webinterfacematch) > 0) else ''
    weather_service     = weatherservicematch[0] if (len(weatherservicematch) > 0) else ''
    movie_scraper       = moviescrapermatch[0] if (len(moviescrapermatch) > 0) else ''
    tv_scraper          = tvscrapermatch[0] if (len(tvscrapermatch) > 0) else ''
    artist_scraper      = artistscrapermatch[0] if (len(artistscrapermatch) > 0) else ''
    music_video_scraper = musicvideoscrapermatch[0] if (len(musicvideoscrapermatch) > 0) else ''
    subtitles           = subtitlesmatch[0] if (len(subtitlesmatch) > 0) else ''
    requires            = requiresmatch[0] if (len(requiresmatch) > 0) else ''
    modules             = modulesmatch[0] if (len(modulesmatch) > 0) else ''
    icon                = iconmatch[0] if (len(iconmatch) > 0) else ''
    videopreview        = videopreviewmatch[0] if (len(videopreviewmatch) > 0) else 'None'
    videoguide          = videoguidematch[0] if (len(videoguidematch) > 0) else 'None'
    videoguide1         = videoguidematch1[0] if (len(videoguidematch1) > 0) else 'None'
    videoguide2         = videoguidematch2[0] if (len(videoguidematch2) > 0) else 'None'
    videoguide3         = videoguidematch3[0] if (len(videoguidematch3) > 0) else 'None'
    videoguide4         = videoguidematch4[0] if (len(videoguidematch4) > 0) else 'None'
    videoguide5         = videoguidematch5[0] if (len(videoguidematch5) > 0) else 'None'
    videoguide6         = videoguidematch6[0] if (len(videoguidematch6) > 0) else 'None'
    videoguide7         = videoguidematch7[0] if (len(videoguidematch7) > 0) else 'None'
    videoguide8         = videoguidematch8[0] if (len(videoguidematch8) > 0) else 'None'
    videoguide9         = videoguidematch9[0] if (len(videoguidematch9) > 0) else 'None'
    videoguide10        = videoguidematch10[0] if (len(videoguidematch10) > 0) else 'None'
    videolabel1         = videolabelmatch1[0] if (len(videolabelmatch1) > 0) else 'None'
    videolabel2         = videolabelmatch2[0] if (len(videolabelmatch2) > 0) else 'None'
    videolabel3         = videolabelmatch3[0] if (len(videolabelmatch3) > 0) else 'None'
    videolabel4         = videolabelmatch4[0] if (len(videolabelmatch4) > 0) else 'None'
    videolabel5         = videolabelmatch5[0] if (len(videolabelmatch5) > 0) else 'None'
    videolabel6         = videolabelmatch6[0] if (len(videolabelmatch6) > 0) else 'None'
    videolabel7         = videolabelmatch7[0] if (len(videolabelmatch7) > 0) else 'None'
    videolabel8         = videolabelmatch8[0] if (len(videolabelmatch8) > 0) else 'None'
    videolabel9         = videolabelmatch9[0] if (len(videolabelmatch9) > 0) else 'None'
    videolabel10        = videolabelmatch10[0] if (len(videolabelmatch10) > 0) else 'None'
    
    print"### Addon Details: "+name

    if deleted != '':
        brokenfinal  = '[CR][CR][COLOR=dodgerblue]Status: [/COLOR][COLOR=red]This add-on is depreciated, it\'s no longer available.[/COLOR]'
    
    elif broken == '' and devbroken == '' and warning =='':
        brokenfinal  = '[CR][CR][COLOR=dodgerblue]Status: [/COLOR][COLOR=lime]No reported problems[/COLOR]'
    
    elif broken == '' and devbroken == '' and warning !='' and deleted =='':
        brokenfinal  = '[CR][CR][COLOR=dodgerblue]Status: [/COLOR][COLOR=orange]Although there have been no reported problems there may be issues with this add-on, see below.[/COLOR]'
    
    elif broken == '' and devbroken != '':
        brokenfinal  = '[CR][CR][COLOR=dodgerblue]Status: [/COLOR]Marked as broken by the add-on developer.[CR][COLOR=dodgerblue]Developer Comments: [/COLOR]'+devbroken
    
    elif broken != '' and devbroken == '':
        brokenfinal  = '[CR][CR][COLOR=dodgerblue]Status: [/COLOR]Marked as broken by a member of the community at WWW.NOOBSANDNERDS.COM[CR][COLOR=dodgerblue]User Comments: [/COLOR]'+broken
    
    elif broken != '' and devbroken != '':
        brokenfinal  = '[CR][CR][COLOR=dodgerblue]Status: [/COLOR]Marked as broken by both the add-on developer and a member of the community at WWW.NOOBSANDNERDS.COM[CR][COLOR=dodgerblue]Developer Comments: [/COLOR]'+devbroken+'[CR][COLOR=dodgerblue]User Comments: [/COLOR]'+broken

# Create the main description template
    description = str('[COLOR=orange]Name: [/COLOR]'+name+'[COLOR=orange]     Author(s): [/COLOR]'+provider_name+'[COLOR=orange][CR][CR]Version: [/COLOR]'+version+'[COLOR=orange]     Created: [/COLOR]'+created+'[COLOR=orange]     Updated: [/COLOR]'+updated+'[COLOR=orange][CR][CR]Repository: [/COLOR]'+repo_id+platform+'[COLOR=orange]     Add-on Type(s): [/COLOR]'+content_types+requires+brokenfinal+deleted+warning+forum+desc+notes)

# If addon already exists notify or give option to run
    if os.path.exists(os.path.join(ADDONS,addon_id)):
        if 'script.module' in addon_id or 'repo' in addon_id:
            addDir('','[COLOR=orange](Already Installed)[/COLOR]','','',icon,'','','')
        else:
            addDir('','[COLOR=orange](Already Installed)[/COLOR] Click here to run the add-on',addon_id,'run_addon',icon,'','','')

# If server is having a slow day and cannot get the name notify user
    if name =='':
        addDir('','[COLOR=yellow]Sorry request failed due to high traffic on server, please try again[/COLOR]','','',icon,'','','')

# Show any known issues with addon
    elif name != '':
        
        if (broken == '') and (devbroken =='') and (deleted =='') and (warning ==''):
            addDir('addon','[COLOR=yellow][FULL DETAILS][/COLOR] No problems reported',description,'text_guide',icon,'','',description)    
        
        if (broken != '' and deleted == '') or (devbroken != '' and deleted == '') or (warning != '' and deleted ==''):
            addDir('addon','[COLOR=yellow][FULL DETAILS][/COLOR][COLOR=orange] Possbile problems reported[/COLOR]',description,'text_guide',icon,'','',description)            
        
        if deleted != '':
            addDir('addon','[COLOR=yellow][FULL DETAILS][/COLOR][COLOR=red] Add-on now depreciated[/COLOR]',description,'text_guide',icon,'','',description)            

# If addon isn't deleted show download options
        if deleted =='':
            
            if repo_id != '' and 'superrepo' not in repo_id:
                if backupinstall == 'true':
                    Add_Install_Dir('[COLOR=lime][INSTALL - Recommended] [/COLOR]'+name,name,'','addon_install_zero',icon,'','',desc,contenttypes,repo_url,repo_id,addon_id,provider_name,forumclean,data_url)    
                    Add_Install_Dir('[COLOR=lime][INSTALL - Backup Option] [/COLOR]'+name,name,'','addon_install',icon,'','',desc,zip_url,repo_url,repo_id,addon_id,provider_name,forumclean,data_url)    
                else:
                    Add_Install_Dir('[COLOR=lime][INSTALL] [/COLOR]'+name,name,'','addon_install_zero',icon,'','',desc,contenttypes,repo_url,repo_id,addon_id,provider_name,forumclean,data_url)    
            
            if repo_id == '' or 'superrepo' in repo_id:
                Add_Install_Dir('[COLOR=lime][INSTALL] [/COLOR]'+name+' - THIS IS NOT IN A SELF UPDATING REPO',name,'','addon_install','','','',desc,zip_url,repo_url,repo_id,addon_id,provider_name,forumclean,data_url)    

# Show various video links
        if videopreview != 'None':
            addDir('','[COLOR=dodgerblue][VIDEO][/COLOR]  Preview',videoguide1,'play_video','','','','')    
        
        if videoguide1 != 'None':
            addDir('','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel1,videoguide1,'play_video','','','','')    
        
        if videoguide2 != 'None':
            addDir('','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel2,videoguide2,'play_video','','','','')    
        
        if videoguide3 != 'None':
            addDir('','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel3,videoguide3,'play_video','','','','')    
        
        if videoguide4 != 'None':
            addDir('','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel4,videoguide4,'play_video','','','','')    
        
        if videoguide5 != 'None':
            addDir('','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel5,videoguide5,'play_video','','','','')    
        
        if videoguide6 != 'None':
            addDir('','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel6,videoguide6,'play_video','','','','')    
        
        if videoguide7 != 'None':
            addDir('','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel7,videoguide7,'play_video','','','','')    
        
        if videoguide8 != 'None':
            addDir('','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel8,videoguide8,'play_video','','','','')    
        
        if videoguide9 != 'None':
            addDir('','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel9,videoguide9,'play_video','','','','')    
        
        if videoguide10 != 'None':
            addDir('','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel10,videoguide10,'play_video','','','','')    
#---------------------------------------------------------------------------------------------------
# Build Genres Menu
def Addon_Genres(url):       
    addDir('folder','Anime',url+'&genre=anime','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Audiobooks',url+'&genre=audiobooks','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Comedy',url+'&genre=comedy','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Comics',url+'&genre=comics','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Documentary',url+'&genre=documentary','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Downloads',url+'&genre=downloads','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Food',url+'&genre=food','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Gaming',url+'&genre=gaming','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Health',url+'&genre=health','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','How To...',url+'&genre=howto','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Kids',url+'&genre=kids','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Live TV',url+'&genre=livetv','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Movies',url+'&genre=movies','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Music',url+'&genre=music','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','News',url+'&genre=news','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Photos',url+'&genre=photos','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Podcasts',url+'&genre=podcasts','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Radio',url+'&genre=radio','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Religion',url+'&genre=religion','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Space',url+'&genre=space','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Sports',url+'&genre=sports','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Subscription',url+'&genre=subscription','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Technology',url+'&genre=tech','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Trailers',url+'&genre=trailers','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','TV Shows',url+'&genre=tv','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','Misc.',url+'&genre=other','grab_addons','mainmenu/addons.png','','','')
    
    if ADDON.getSetting('adult') == 'true':
        addDir('folder','XXX',url+'&genre=adult','grab_addons','mainmenu/addons.png','','','')
#---------------------------------------------------------------------------------------------------
# Step 1 of the addon install process (installs the actual addon)
def Addon_Install(name,zip_link,repo_link,repo_id,addon_id,provider_name,forum,data_path):
    forum        = str(forum)
    repo_id      = str(repo_id)
    status       = 1
    repostatus   = 1
    modulestatus = 1
    addonpath    = xbmc.translatePath(os.path.join(ADDONS, addon_id))
    
    if os.path.exists(addonpath):
        addonexists = 1
    
    else:
        addonexists = 0
    
    addondownload = xbmc.translatePath(os.path.join(packages,name+'.zip'))
    addonlocation = xbmc.translatePath(os.path.join(ADDONS,addon_id))
    
    dp.create("Installing Addon","Please wait whilst your addon is installed",'', '')
    
    try:
        downloader.download(repo_link, addondownload, dp)
        extract.all(addondownload, ADDONS, dp)
    
    except:
        
        try:
            downloader.download(zip_link, addondownload, dp)
            extract.all(addondownload, ADDONS, dp)
        
        except:
            
            try:
                if not os.path.exists(addonlocation):
                    os.makedirs(addonlocation)
                
                link  = Open_URL(data_path, 10).replace('\n','').replace('\r','')
                match = re.compile('href="(.+?)"', re.DOTALL).findall(link)
                
                for href in match:
                    filepath=xbmc.translatePath(os.path.join(addonlocation,href))
                    
                    if addon_id not in href and '/' not in href:
                        
                        try:
                            dp.update(0,"Downloading [COLOR=yellow]"+href+'[/COLOR]','','Please wait...')
                            downloader.download(data_path+href, filepath, dp)
                        
                        except:
                            print"failed to install"+href
                    
                    if '/' in href and '..' not in href and 'http' not in href:
                        remote_path = data_path+href
                        Recursive_Loop(filepath,remote_path)
            
            except:
                dialog.ok("Error downloading add-on", 'There was an error downloading [COLOR=yellow]'+name,'[/COLOR]Please consider updating the add-on portal with details or report the error on the forum at WWW.NOOBSANDNERDS.COM') 
                status=0
    
    if status==1:
        time.sleep(1)
        dp.update(0,"[COLOR=yellow]"+name+'[/COLOR]  [COLOR=lime]Successfully Installed[/COLOR]','','Now installing repository')
        time.sleep(1)
        repopath = xbmc.translatePath(os.path.join(ADDONS, repo_id))
        
        if (repo_id != 'repository.xbmc.org') and not (os.path.exists(repopath)) and (repo_id != '') and ('superrepo' not in repo_id):
            Install_Repo(repo_id)
        
        xbmc.sleep(2000)
        
        if os.path.exists(addonpath) and addonexists == 0:
            incremental = 'http://noobsandnerds.com/TI/AddonPortal/downloadcount.php?id=%s' % (addon_id)
            try:
                Open_URL(incremental)
            except:
                pass
        
        Dependency_Install(name,addon_id)
        Update_Repo(showdialog = False)
        xbmc.executebuiltin('Container.Refresh')

        if repostatus == 0:
            dialog.ok(name+" Install Complete",'The add-on has been successfully installed but','there was an error installing the repository.','This will mean the add-on fails to update')
        
        if modulestatus == 0:
            dialog.ok(name+" Install Complete",'The add-on has been successfully installed but','there was an error installing modules.','This could result in errors with the add-on.')
        
        if modulestatus != 0 and repostatus != 0 and forum != 'None':
            dialog.ok(name+" Install Complete",'Please support the developer(s) [COLOR=dodgerblue]'+provider_name,'[/COLOR]Support for this add-on can be found at [COLOR=yellow]'+forum,'[/COLOR][CR]Visit WWW.NOOBSANDNERDS.COM for all your Kodi needs.')
        
        if modulestatus != 0 and repostatus != 0 and forum == 'None':
            dialog.ok(name+" Install Complete",'Please support the developer(s) [COLOR=dodgerblue]'+provider_name,'[/COLOR]No details of forum support have been given.')
#---------------------------------------------------------------------------------------------------
# Check to see whether or not an add-on exists
def Addon_Exists(addon_id):
    try:
        xbmcaddon.Addon(id=addon_id).getAddonInfo('path')
        return True
    except:
        return False
#---------------------------------------------------------------------------------------------------
# Increment the download count for add-on
def Addon_Increment(addon_id):
    incremental = 'http://noobsandnerds.com/TI/AddonPortal/downloadcount.php?id=%s' % (addon_id)
    try:
        Open_URL(incremental, 10)
    except:
        pass
#---------------------------------------------------------------------------------------------------
# Step 1 of the addon install process (installs the actual addon)
def Addon_Install_Zero(name,contenttypes,repo_link,repo_id,addon_id,provider_name,forum,data_path):

# Check to see if the repository is already installed
    if Addon_Exists(repo_id) and not Addon_Exists(addon_id):
        xbmc.log('Repo exists: %s' % repo_id)
        xbmc.executebuiltin('XBMC.RunPlugin(plugin://%s)' % addon_id)

# wait for the yesno dialog to close
        yesno = threading.Thread(target=Is_Window_Active, args=['yesnodialog'])
        yesno.start()
        isactive = True
        counter = 0
        while isactive and counter < 20:
            xbmc.sleep(500)
            counter += 1
            isactive = yesno.isAlive()

# If the ok dialog pops up it means there's been a message to say unsuccessful install (from Kodi)
        if Is_Window_Active('okdialog'):
            xbmc.log('### Kodi failed to install add-on')
            return        

# Wait for the install progress dialog to finish
        yesno = threading.Thread(target=Is_Window_Active, args=['progressdialog'])
        yesno.start()
        isactive = True
        counter = 0
        while isactive and counter < 40:
            xbmc.sleep(500)
            counter += 1
            isactive = yesno.isAlive()
        if Addon_Exists(addon_id):
            Addon_Increment(addon_id)
            xbmc.executebuiltin('Container.Refresh')
        # elif yesno:
        #     dialog.ok('UNABLE TO INSTALL','The most common cause for this is you either have a bad repo or module installed somewhere on your system or this add-on is not designed for the version of Kodi you\'re running.')
        else:
            dialog.ok('UNABLE TO INSTALL','The most common cause for this is the add-on is no longer available on the repo. If you find an alternative repo that has it please consider updating the team at noobsandnerds.com so they can fix in the database.')
    
# Check to see if the addon is already installed
    elif Addon_Exists(addon_id):
        if dialog.yesno('Add-on Already Installed','This add-on has already been detected on your system. Would you like to remove the old version and re-install? There should be no need for this unless you\'ve manually opened up the add-on code and edited in a text editor.'):
            addonpath = xbmcaddon.Addon(id=addon_id).getAddonInfo('path')

            try:
                shutil.rmtree(addonpath)
            except:
                xbmc.log('Failed to remove %s' % addonpath)

            writefile = open(temp_install,'w')
            writefile.write('import default;default.Update_Repo(showdialog = False);xbmc.sleep(1500);default.Addon_Install_Zero("%s","%s","%s","%s","%s","%s","%s","%s")'%(name,contenttypes,repo_link,repo_id,addon_id,provider_name,forum,data_path))
            writefile.close()

            current_profile = xbmc.getInfoLabel('System.ProfileName')
            xbmc.log('### attempting to load profile: %s'%current_profile)
            xbmc.executebuiltin('LoadProfile(%s)'%current_profile)
            return

        else:
            return

    elif (repo_id != 'repository.xbmc.org') and (repo_id != '') and ('superrepo' not in repo_id):
        repoinstall = Install_Repo(repo_id)
        xbmc.log('### repo installed, sleeping for 2000')
        xbmc.sleep(2000)
        if repoinstall:
            xbmc.log('### running plugin')
            xbmc.executebuiltin('XBMC.RunPlugin(plugin://%s)' % addon_id)
            xbmc.log('### running yesno window check')
# wait for the yesno dialog to close
            yesno = threading.Thread(target=Is_Window_Active, args=['yesnodialog'])
            yesno.start()
            isactive = True
            counter = 0
            while isactive and counter < 20:
                xbmc.sleep(500)
                counter  += 1
                isactive = yesno.isAlive()
            xbmc.log('### yesno status: %s' % isactive)
# wait for the yesno dialog to close
            if globalyesno:
                xbmc.log('### yes/no was true, checking progressdialog')
                progressthread = threading.Thread(target=Is_Window_Active, args=['progressdialog'])
                progressthread.start()
                isactive = True
                counter = 0
                while isactive and counter < 40:
                    xbmc.sleep(500)
                    counter += 1
                    isactive = progressthread.isAlive()
                xbmc.log('### progressdialog status: %s' % yesno)
                if Addon_Exists(addon_id):
                    Addon_Increment(addon_id)
                    xbmc.executebuiltin('Container.Refresh')
                dp.close()
                    # dialog.ok('UNABLE TO INSTALL','The most common cause for this is you either have a bad repo or module installed somewhere on your system or this add-on is not designed for the version of Kodi you\'re running.')
            else:
                dialog.ok('UNABLE TO INSTALL','The most common cause for this is the add-on is no longer available on the repo. If you find an alternative repo that has it please consider updating the team at noobsandnerds.com so they can fix in the database.')
        else:
            dialog.ok('Failed Install','The repository could not be installed, the developer may have deleted it. Please try the backup install option.')
    try:
        os.path.remove(temp_install)
    except:
        pass
#---------------------------------------------------------------------------------------------------
# Addons section
def Addon_Menu(sign):
    addDir('folder','[COLOR=gold]Popular[/COLOR] (Show the top 100 most downloaded add-ons)','popular','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','[COLOR=gold]Brand New[/COLOR] (Show the new releases)','latest','grab_addons','mainmenu/addons.png','','','')
    addDir('folder','[COLOR=gold]Manual Search[/COLOR] (Type in author/name/content)','desc=','search_addons','mainmenu/addons.png','','','')
    addDir('folder','Filter Results (By Genres)', 'p', 'addon_genres', 'mainmenu/addons.png','','','')
    addDir('folder','Filter Results (By Countries)', 'p', 'addon_countries', 'mainmenu/addons.png','','','')
    addDir('folder','Filter Results (By Kodi Categories)', 'p', 'addon_categories', 'mainmenu/addons.png','','','')
    addDir('','Kodi Add-on Browser (Install From Zip)','','install_from_zip','mainmenu/addons.png','','','')
    addDir('','Kodi Add-on Browser (Browse My Repositories)','','browse_repos','mainmenu/addons.png','','','')
    addDir('','Kodi Add-on Browser (Check For Add-on Updates)','','check_updates','mainmenu/addons.png','','','')
#---------------------------------------------------------------------------------------------------
# Add-on removal menu
def Addon_Removal_Menu():
    namearray = []
    iconarray = []
    descarray = []
    patharray = []
    finalpath = []

    for file in os.listdir(ADDONS):
        if os.path.isdir(os.path.join(ADDONS,file)) and os.path.exists(os.path.join(ADDONS,file,'addon.xml')):

# Read contents of addon.xml to memory and grab REAL addon id (for those who's folder names differ)
            readfile    = open(os.path.join(ADDONS,file,'addon.xml'), 'r')
            content     = readfile.read()
            readfile.close()
            tempaddonid = re.compile('id="(.+?)"').findall(content)[0]

            try:
                Addon       = xbmcaddon.Addon(tempaddonid)
                addontype   = Addon.getAddonInfo('type').replace('xbmc.','')
                name        = Addon.getAddonInfo('name')
                iconimage   = Addon.getAddonInfo('icon')
                description = Addon.getAddonInfo('description')
                filepath    = os.path.join(ADDONS,file)

                namearray.append('[COLOR=gold]%s:[/COLOR]  %s' % (addontype,name))
                iconarray.append(iconimage)
                descarray.append(description)
                patharray.append(filepath)
            
            except:
                xbmc.log('### Add-on Disabled, cannot remove until reactivated: %s' % file)

    finalarray = multiselect('Add-ons To Fully Remove',namearray,iconarray,descarray)
    for item in finalarray:
        newpath = patharray[item]
        newname = namearray[item]
        finalpath.append([newname,newpath])
    if len(finalpath) > 0:
        Remove_Addons(finalpath)
#-----------------------------------------------------------------------------------------------------------------
# Function to open addon settings
def Addon_Settings():
    ADDON.openSettings(sys.argv[0])
    xbmc.executebuiltin('Container.Refresh')
#-----------------------------------------------------------------------------------------------------------------
# Enable/disable the visibility of adult add-ons (use true or false)
def Adult_Filter(value):
    master_list = Open_URL('http://noobsandnerds.com/TI/AddonPortal/adult.php',10)
    id_list     = re.compile('i="(.+?)"').findall(master_list)

    for addon_id in id_list:
        addon_id = '"%s"' % addon_id
        query = '{"jsonrpc":"2.0", "method":"Addons.SetAddonEnabled","params":{"addonid":%s,"enabled":%s}, "id":1}' % (addon_id, value)
        response = xbmc.executeJSONRPC(query)
        xbmc.log(query)
        xbmc.log('### RETURN %s' % response)

    if value == 'false':
        filter_type = 'disabled'
    else:
        filter_type = 'enabled'
    dialog.ok('ADULT CONTENT %s' % filter_type.upper(), 'Your adult rated add-ons have now been %s' % filter_type)
#-----------------------------------------------------------------------------------------------------------------
def Android_Path_Check():
    content = Grab_Log()
    localstorage  = re.compile('External storage path = (.+?);').findall(content)
    localstorage  = localstorage[0] if (len(localstorage) > 0) else ''
    return localstorage
#-----------------------------------------------------------------------------------------------------------------
# Zip up the contents of a directory and all subdirectories, this will exclude the global excludes files such as guisettings.xml
def Archive_Tree(sourcefile, destfile, message_header, message1, message2, message3, exclude_dirs, exclude_files):
    zipobj       = zipfile.ZipFile(destfile , 'w', zipfile.ZIP_DEFLATED)
    rootlen      = len(sourcefile)
    for_progress = []
    ITEM         =[]
    
    dp.create(message_header, message1, message2, message3)
    
    for base, dirs, files in os.walk(sourcefile):
        
        for file in files:
            ITEM.append(file)
    
    N_ITEM =len(ITEM)
    
    for base, dirs, files in os.walk(sourcefile):
        
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        files[:] = [f for f in files if f not in exclude_files and not 'crashlog' in f and not 'stacktrace' in f]
        
        for file in files:
            
            try:
                for_progress.append(file) 
                progress = len(for_progress) / float(N_ITEM) * 100  
                dp.update(0,"Backing Up",'[COLOR yellow]%s[/COLOR]'%d, 'Please Wait')
                fn = os.path.join(base, file)
            
            except:
                print"Unable to backup file: "+file
            
            if not 'temp' in dirs:
                
                if not AddonID in dirs:
                    
                    try:
                       FORCE= '01/01/1980'
                       FILE_DATE=time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(fn)))
                       
                       if FILE_DATE > FORCE:
                           zipobj.write(fn, fn[rootlen:])  
                    
                    except:
                        print"Unable to backup file: "+file
    
    zipobj.close()
    dp.close()
#---------------------------------------------------------------------------------------------------
# Zip up tree, essentially the same as above but doesn't exclude global excludes (such as guisettings & profiles)
def Archive_File(sourcefile, destfile):
    zipobj       = zipfile.ZipFile(destfile , 'w', zipfile.ZIP_DEFLATED)
    rootlen      = len(sourcefile)
    for_progress = []
    ITEM         = []
    
    dp.create("Backing Up Files","Archiving...",'', 'Please Wait')
    
    for base, dirs, files in os.walk(sourcefile):
        
        for file in files:
            ITEM.append(file)
    
    N_ITEM =len(ITEM)
    
    for base, dirs, files in os.walk(sourcefile):
        
        for file in files:
            for_progress.append(file) 
            progress = len(for_progress) / float(N_ITEM) * 100  
            dp.update(int(progress),"Backing Up",'[COLOR yellow]%s[/COLOR]'%file, 'Please Wait')
            fn       = os.path.join(base, file)
            
            if not 'temp' in dirs:
                
                if not AddonID in dirs:
                   
                   import time
                   FORCE= '01/01/1980'
                   FILE_DATE=time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(fn)))
                   
                   if FILE_DATE > FORCE:
                       zipobj.write(fn, fn[rootlen:])  
    zipobj.close()
    dp.close()
#---------------------------------------------------------------------------------------------------
# Check for non ascii files and folders
def ASCII_Check():
    sourcefile   = dialog.browse(3, 'Select the folder you want to scan', 'files', '', False, False)
    rootlen      = len(sourcefile)
    for_progress = []
    ITEM         = []
                
    dp.create('Checking File Structure','','Please wait...','')

    choice = dialog.yesno('Delete or Scan?','Do you want to delete all filenames with special characters or would you rather just scan and view the results in the log?',yeslabel='Delete',nolabel='Scan')
# Create temp files to store the deletion results in
    successascii = open(ascii_results1, mode='w+')
    failedascii  = open(ascii_results2, mode='w+')

    for base, dirs, files in os.walk(sourcefile):
        
        for file in files:
            ITEM.append(file)
    
    N_ITEM =len(ITEM)
    
    for base, dirs, files in os.walk(sourcefile):
        
        dirs[:] = [d for d in dirs]
        files[:] = [f for f in files]
        
        for file in files:

            for_progress.append(file) 
            progress = len(for_progress) / float(N_ITEM) * 100  
            dp.update(0,"Checking for non ASCII files",'[COLOR yellow]%s[/COLOR]'%d, 'Please Wait')
            
            try:
                file.encode('ascii')

            except UnicodeDecodeError:
                badfile = (str(base)+'/'+str(file)).replace('\\','/').replace(':/',':\\')
#                badfile = unicodedata.normalize('NFKD',unicode(badfile,"ISO-8859-1")).encode("ascii","ignore")
                print " non-ASCII file status logged successfully: " + badfile
                if choice != 1:
                    successascii.write('[COLOR=dodgerblue]Non-ASCII File:[/COLOR]\n')
                    for chunk in chunks(badfile, 75):
                        successascii.write(chunk+'[CR]')
                    successascii.write('\n')
                if choice == 1:
                    try:
                        os.remove(badfile)
                        print"### SUCCESS - deleted "+badfile
                        successascii.write('[COLOR=dodgerblue]SUCCESSFULLY DELETED:[/COLOR]\n')
                        for chunk in chunks(badfile, 75):
                            successascii.write(chunk+'[CR]')
                        successascii.write('\n')
                        
                    except:
                        print"######## FAILED TO REMOVE: "+badfile
                        print"######## Make sure you manually remove this file ##########"
                        failedascii.write('[COLOR=red]FAILED TO DELETE:[/COLOR]\n')
                        for chunk in chunks(badfile, 75):
                            failedascii.write(chunk+'[CR]')
                        failedascii.write('\n')

    failedascii.close()
    successascii.close()

# Create final results by merging success and failed together
    successascii = open(ascii_results1, mode='r')
    successcontent = successascii.read()
    successascii.close()
    failedascii = open(ascii_results2, mode='r')
    failedcontent = failedascii.read()
    failedascii.close()
    if successcontent == '' and failedcontent == '':
        dialog.ok('No Special Characters Found','Great news, all filenames in the path you scanned are ASCII based - no special characters found.' )
    else:
        finalresults = open(ascii_results, mode='w+')
        finalresults.write(successcontent+'\n\n'+failedcontent)
        finalresults.close()
        results = open(ascii_results, mode='r')
        resultscontent = results.read()
        results.close()
        Text_Boxes('Final Results',resultscontent)
        os.remove(ascii_results)
    os.remove(ascii_results1)
    os.remove(ascii_results2)
#---------------------------------------------------------------------------------------------------
#Create backup menu
def Backup_Option():
    addDir('','[COLOR=dodgerblue]How to create and share my build[/COLOR]','','instructions_1','mainmenu/maintenance.png','','','Back Up Your Full System')
    addDir('','[COLOR=gold]-----------------------------------------------------------------[/COLOR]','','','mainmenu/maintenance.png','','','')
    addDir('','Create Community Build (for sharing on CP only)','url','community_backup','mainmenu/maintenance.png','','','Back Up Your Full System')
    if OpenELEC_Check():
        addDir('','Create OpenELEC Backup (full backup can only be used on OpenELEC)','none','openelec_backup','mainmenu/maintenance.png','','','')
    addDir('','Create Universal Build (local backups only)','none','community_backup_2','mainmenu/maintenance.png','','','')
    addDir('','Create Full Backup (will only work on THIS device)','local','local_backup','mainmenu/maintenance.png','','','Back Up Your Full System')
    addDir('','Backup Addons Only','addons','restore_zip','mainmenu/maintenance.png','','','Back Up Your Addons')
    addDir('','Backup Addon Data Only','addon_data','restore_zip','mainmenu/maintenance.png','','','Back Up Your Addon Userdata')
    addDir('','Backup Guisettings.xml',GUI,'restore_backup','mainmenu/maintenance.png','','','Back Up Your guisettings.xml')
    
    if os.path.exists(FAVS):
        addDir('','Backup Favourites.xml',FAVS,'restore_backup','mainmenu/maintenance.png','','','Back Up Your favourites.xml')
    
    if os.path.exists(SOURCE):
        addDir('','Backup Source.xml',SOURCE,'restore_backup','mainmenu/maintenance.png','','','Back Up Your sources.xml')
    
    if os.path.exists(ADVANCED):
        addDir('','Backup Advancedsettings.xml',ADVANCED,'restore_backup','mainmenu/maintenance.png','','','Back Up Your advancedsettings.xml')
    
    if os.path.exists(KEYMAPS):
        addDir('','Backup Advancedsettings.xml',KEYMAPS,'restore_backup','mainmenu/maintenance.png','','','Back Up Your keyboard.xml')
    
    if os.path.exists(RSS):
        addDir('','Backup RssFeeds.xml',RSS,'restore_backup','mainmenu/maintenance.png','','','Back Up Your RssFeeds.xml')
#---------------------------------------------------------------------------------------------------
# Backup/Restore root menu
def Backup_Restore():
    addDir('folder','Backup My Content','none','backup_option','mainmenu/maintenance.png','','','')
    addDir('folder','Restore My Content','none','restore_option','mainmenu/maintenance.png','','','')
#---------------------------------------------------------------------------------------------------
# Browse pre-installed repo's via the kodi add-on browser
def Browse_Repos():
    xbmc.executebuiltin('ActivateWindow(10040,"addons://repos/",return)')
#---------------------------------------------------------------------------------------------------
# Checks cookie file for post count, users can update by clicking on user info
def Builder_Name():
# Load nag script into memory, this needs decoding
    filepath = os.path.join(ADDONS,binascii.unhexlify('7363726970742e6d6f64756c652e637967706669'),'tag.cfg')
    if os.path.exists(filepath):
        readfile = open(filepath, 'r')
        content  = readfile.read()
        readfile.close()
        return binascii.unhexlify(content)
    else:
        return binascii.unhexlify('6e6c616b73646a666c6b61736a64666c6a616c736b6a666c6b616a7366')
#-----------------------------------------------------------------------------------------------------------------
# Main category list
def Categories(localbuildcheck,localversioncheck,id,welcometext,livemsg):
    Cleanup_Partial_Install()
    if livemsg != 'none':
        try:
            exec(livemsg)
            # addDir('','[COLOR=orange]---------------------------------------[/COLOR]','None','','','','','')
        except:
            pass
    if (username.replace('%20',' ') in welcometext) and ('elc' in welcometext) and username !='':
        addDir('',welcometext,'show','user_info','','','','')
        
    if id != 'None':
        
        if id != 'Local':
            updatecheck = Check_For_Update(localbuildcheck,localversioncheck,id)
            
            if updatecheck == True:
                
                if not 'Partially installed' in localbuildcheck:
                    addDir('folder','[COLOR=dodgerblue]'+localbuildcheck+':[/COLOR] [COLOR=lime]NEW VERSION AVAILABLE[/COLOR]',id,'showinfo','','','','')
                
                if '(Partially installed)' in localbuildcheck:
                    addDir('folder','[COLOR=darkcyan]Current Build Installed: [/COLOR][COLOR=dodgerblue]'+localbuildcheck+'[/COLOR]',id,'showinfo2','','','','')
            else:
                addDir('folder','[COLOR=darkcyan]Current Build Installed: [/COLOR][COLOR=dodgerblue]'+localbuildcheck+'[/COLOR]',id,'showinfo','','','','')
        
        else:
            
            if localbuildcheck == 'Incomplete':
                addDir('','[COLOR=darkcyan]Your last restore is not yet completed[/COLOR]','url',Check_Local_Install(),'','','','')
            
            else:
                addDir('','[COLOR=darkcyan]Current Build Installed: [/COLOR][COLOR=dodgerblue]Local Build ('+localbuildcheck+')[/COLOR]','','','','','','')
    folders = 0
    
    if os.path.exists(CP_PROFILE):
        for name in os.listdir(CP_PROFILE):
            if name != 'Master':
                folders += 1

        if folders>1:
            addDir('folder','[COLOR=darkcyan]Switch Build Profile[/COLOR]',localbuildcheck,'switch_profile_menu','','','','')
            addDir('','[COLOR=orange]---------------------------------------[/COLOR]','None','','','','','')
    
    # if not 'elc' in welcometext:
    #     addDir('',welcometext,'None','register','','','','')
    addDir('','[COLOR=yellow]Settings[/COLOR]','settings','addon_settings','mainmenu/settings.png','','','')
    

    addDir('folder','Add-on Portal','','addonmenu', 'mainmenu/addons.png','','','')
    
    if xbmc.getCondVisibility('system.platform.android'):
        addDir('folder','App Installer', '', 'app_installer', 'mainmenu/apps.png','','','')

    addDir('folder','Community Builds', '', 'CB_Menu', 'mainmenu/builds.png','','','')
    addDir('folder','Keyword Installer', '', 'nan_menu', 'mainmenu/keyword.png','','','')    
    addDir('','Tutorials','', 'tutorial_root_menu', 'mainmenu/tuts.png','','','')    
    addDir('folder','Maintenance','none', 'tools', 'mainmenu/maintenance.png','','','')
#---------------------------------------------------------------------------------------------------
# Main process to create the addons folder for new community build
def CB_Addon_Install_Loop():
    if os.path.exists(addonstemp):
        shutil.rmtree(addonstemp)
    
    if not os.path.exists(addonstemp):
        os.makedirs(addonstemp)

    deps = Dependency_Check()
    portalcontent   = Open_URL('http://noobsandnerds.com/TI/AddonPortal/approved.php', 10)

    dp.create('Backing Up Add-ons','','Please Wait...')
    
    for name in os.listdir(ADDONS):

#DO NOT copy over totalinstaller and any dependencies
        if not 'totalinstaller' in name and not 'plugin.program.tbs' in name and not 'packages' in name and os.path.isdir(os.path.join(ADDONS, name)):

# Check the add-on has a valid repo and is not a dependency of the skin
            if name in portalcontent and not name in deps and not 'repo.' in name and not 'repository.' in name and os.path.isdir(os.path.join(ADDONS, name)):

# Check it's not something that's going to cause issues on startup and also make sure it's a valid directory
                if not 'service.xbmc.versioncheck' in name and not 'packages' in name and os.path.isdir(os.path.join(ADDONS, name)):
                    
                    try:
                        dp.update(0,"Backing Up",'[COLOR yellow]%s[/COLOR]'%name, 'Please Wait...')
                        os.makedirs(os.path.join(addonstemp,name))
                        
                        newpath        = os.path.join(addonstemp,name,'addon.xml')
                        newpathdefault = os.path.join(addonstemp,name,'default.py')
                        filefix        = open(os.path.join(ADDONS,name,'addon.xml'), mode='r')
                        content        = filefix.read()
                        filefix.close()
                        
                        localnamematch     = re.compile(' name="(.+?)"').findall(content)
                        localprovidermatch = re.compile('provider-name="(.+?)"').findall(content)
                        localmatch         = re.compile('<addon[\s\S]*?">').findall(content)
                        descmatch          = re.compile('<description[\s\S]*?<\/description>').findall(content)
                        namematch          = localnamematch[0] if (len(localnamematch) > 0) else 'None'
                        providernamematch  = localprovidermatch[0] if (len(localprovidermatch) > 0) else 'Anonymous'
                        localcontentmatch  = localmatch[0] if (len(localmatch) > 0) else 'None'
                        descriptionmatch   = descmatch[0] if (len(descmatch) > 0) else 'None'
                        
                        newversion = '<addon id="'+name+'" name="'+namematch+'" version="0" provider-name="'+providernamematch+'">'
                        description = '<description>If you\'re seeing this message it means the add-on is still updating, please wait for the update process to complete.</description>'
                        
                        if localcontentmatch!='None':
                            replacefile = content.replace(descriptionmatch,description).replace(localcontentmatch,newversion)
                        
                        else:
                            replacefile = content.replace(descriptionmatch,description)

                        writefile = open(newpath, mode='w+')
                        writefile.write(str(replacefile))
                        writefile.close()
                        writefile2 = open(newpathdefault, mode='w+')
                        writefile2.write('import xbmcplugin,xbmcgui,xbmc,xbmcaddon,os,sys\nAddonID="'+name+'"\nAddonName="'+namematch+'"\ndialog=xbmcgui.Dialog()\ndialog.ok(AddonName+" Add-on Requires Update","This add-on may still be in the process of the updating so we recommend waiting a few minutes to see if it updates naturally. If it hasn\'t updated after 5mins please try reinstalling via the Community Portal add-on")\nxbmcplugin.endOfDirectory(int(sys.argv[1]))')
                        writefile2.close()
                    
                    except:
                        print"### Failed to backup: "+name

# If it's not in a repo or it's a skin dependency copy the whole add-on over
            else:
                try:
                    shutil.copytree(os.path.join(ADDONS,name), os.path.join(addonstemp,name))
                except:
                    print"### Failed to copy: "+name
    
    dp.close()
    
    message_header = "Creating Backup"
    message1       = "Archiving..."
    message2       = ""
    message3       = "Please Wait"
    
    Archive_Tree(addonstemp, backupaddonspath, message_header, message1, message2, message3, '', '')
    
    try:
        shutil.rmtree(addonstemp)
    
    except:
        print"### COMMUNITY BUILDS: Failed to remove temp addons folder - manual delete required ###"
#-----------------------------------------------------------------------------------------------------------------
# Final install process for CB (Addon loop)
def CB_Install_Final(url):
    dp.create('Cleaning Temp Paths','','Please wait...')
    if os.path.exists(addonstemp):
        shutil.rmtree(addonstemp)
    
    if not os.path.exists(addonstemp):
        os.makedirs(addonstemp)
    
    extract.all(backupaddonspath, addonstemp, dp)
    
    for name in os.listdir(addonstemp):
        
        if not 'totalinstaller' in name and not 'plugin.program.tbs' in name:
            if not os.path.exists(os.path.join(ADDONS,name)):
                os.rename(os.path.join(addonstemp,name),os.path.join(ADDONS,name))
                dp.update(0,"Installing: [COLOR=yellow]"+name+'[/COLOR]','','Please wait...')
                print"### Successfully installed: "+name
                   
            else:
                print"### "+name+" Already exists on system"
#---------------------------------------------------------------------------------------------------
# Build the root search menu for installing community builds    
def CB_Menu(welcometext):
    if xbmc.getCondVisibility('system.platform.android'):
        localstorage   = Android_Path_Check()
        downloadfolder = os.path.join(localstorage,'Download')
        try:
            if not os.path.exists(downloadfolder):
                os.makedirs(downloadfolder)
        except:
            xbmc.log("### Failed to make download folder")

    xbmc_version = xbmc.getInfoLabel("System.BuildVersion")
    versionfloat = float(xbmc_version[:2])
    version      = int(versionfloat)
    
    if privatebuilds=='true':
        addDir('folder','[COLOR=dodgerblue]Show My Private List[/COLOR]','&visibility=private','grab_builds','mainmenu/builds.png','','','')        
    
    if (version < 14) or (versionoverride=='true'):
        addDir('folder','[COLOR=dodgerblue]Show All Gotham Compatible Builds[/COLOR]','&xbmc=gotham&visibility=public','grab_builds','mainmenu/builds.png','','','')
    
    if (version == 14) or (versionoverride=='true'):
        addDir('folder','[COLOR=dodgerblue]Show All Helix Compatible Builds[/COLOR]','&xbmc=helix&visibility=public','grab_builds','mainmenu/builds.png','','','')
    
    if (version == 15) or (versionoverride=='true'):
        addDir('folder','[COLOR=dodgerblue]Show All Isengard Compatible Builds[/COLOR]','&xbmc=isengard&visibility=public','grab_builds', 'mainmenu/builds.png','','','')
    if (version == 16) or (versionoverride=='true'):
        addDir('folder','[COLOR=dodgerblue]Show All Jarvis Compatible Builds[/COLOR]','&xbmc=jarvis&visibility=public','grab_builds','mainmenu/builds.png','','','')

    if wizard == 'false':
        addDir('','[COLOR=gold]How to fix builds broken on other wizards![/COLOR]','','instructions_5','mainmenu/builds.png','','','')
    if wizardurl1 != '' and wizard == 'true':
        addDir('folder','[COLOR=darkcyan]Show '+wizardname1+' Builds[/COLOR]','&id=1','grab_builds','mainmenu/builds.png','','','')
    if wizardurl2 != '' and wizard == 'true':
        addDir('folder','[COLOR=darkcyan]Show '+wizardname2+' Builds[/COLOR]','&id=2','grab_builds','mainmenu/builds.png','','','')
    if wizardurl3 != '' and wizard == 'true':
        addDir('folder','[COLOR=darkcyan]Show '+wizardname3+' Builds[/COLOR]','&id=3','grab_builds','mainmenu/builds.png','','','')
    if wizardurl4 != '' and wizard == 'true':
        addDir('folder','[COLOR=darkcyan]Show '+wizardname4+' Builds[/COLOR]','&id=4','grab_builds','mainmenu/builds.png','','','')
    if wizardurl5 != '' and wizard == 'true':
        addDir('folder','[COLOR=darkcyan]Show '+wizardname5+' Builds[/COLOR]','&id=5','grab_builds','mainmenu/builds.png','','','')
    addDir('folder','Create My Own Community Build','url','backup_option','mainmenu/builds.png','','','Back Up Your Full System')
#---------------------------------------------------------------------------------------------------
#gotham to helix skin function for keyboard fix
def changekeys(skin):
    left       = '<onleft>%s</onleft>'
    right      = '<onright>%s</onright>'
    up         = '<onup>%s</onup>'
    down       = '<ondown>%s</ondown>'
    button     = '<control type="button" id="%s">'    

# New keyboard letter codes
    LETTER     = [
        ('65','140'),
        ('66','164'),
        ('67','162'),
        ('68','142'),
        ('69','122'),
        ('70','143'),
        ('71','144'),
        ('72','145'),
        ('73','127'),
        ('74','146'),
        ('75','147'),
        ('76','148'),
        ('77','166'),
        ('78','165'),
        ('79','128'),
        ('80','129'),
        ('81','120'),
        ('82','123'),
        ('83','141'),
        ('84','124'),
        ('85','126'),
        ('86','163'),
        ('87','121'),
        ('88','161'),
        ('89','125'),
        ('90','160')]
    
    for old , new in LETTER:
        a      = open(skin).read()  
        CHANGE = a.replace(button%old,button%new).replace(left%old,left%new).replace(right%old,right%new).replace(up%old,up%new).replace(down%old,down%new)
        f      = open(skin, mode='w')
        f.write(CHANGE)
        f.close()   
#---------------------------------------------------------------------------------------------------
def changenumber(u,skin):
    left   = '<onleft>%s</onleft>'
    right  = '<onright>%s</onright>'
    up     = '<onup>%s</onup>'
    down   = '<ondown>%s</ondown>'
    button = '<control type="button" id="%s">'
    
    if u < 49:
        NEW=u+ 61
    
    else:    
        NEW=u+ 51
    
    a       = open(skin).read()
    CHANGE  = a.replace(left%u,left%NEW).replace(right%u,right%NEW).replace(up%u,up%NEW).replace(down%u,down%NEW).replace(button%u,button%NEW)
    f       = open(skin, mode='w')
    f.write(CHANGE)
    f.close()
#-----------------------------------------------------------------------------------------------------------------
def Check_Build_Addons(description):
    profile_path        = os.path.join(CP_PROFILE,'extracted')
    temp_path           = os.path.join(CP_PROFILE,'temp')
    profile_addon_path  = os.path.join(profile_path,'userdata','.cbcfg')
    profile_addons_list = os.path.join(CP_PROFILE, description, 'addonlist')
    profile_addons      = open(profile_addons_list, 'w+')
    mainaddons          = []

    if not os.path.exists(os.path.join(CP_PROFILE, description)):
        os.makedirs(os.path.join(CP_PROFILE, description))
        if debug == 'true':
            xbmc.log("### Created: %s" % os.path.join(CP_PROFILE, description))
    if not os.path.exists(ADDONS_MASTER):
        os.makedirs(ADDONS_MASTER)
        if debug == 'true':
            xbmc.log("### Created: %s" % ADDONS_MASTER)
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)
        if debug == 'true':
            xbmc.log("### Removed: %s" % temp_path)
# Create a temp directory for addons in zip
    if os.path.exists(profile_addon_path):
        if not os.path.exists(temp_path):
            os.makedirs(temp_path)
            if debug == 'true':
                xbmc.log("### Created: %s" % temp_path)
        extract.all(profile_addon_path, temp_path, dp)
        xbmc.log("### NEW STYLE BUILD")
        if debug == 'true':
            xbmc.log("### Extracted "+profile_addon_path+" to: "+temp_path)
    elif os.path.exists(os.path.join(profile_path,'addons')):
        os.rename(os.path.join(profile_path,'addons'), temp_path)
        xbmc.log("### OLD BUILD - RENAMED ADDONS FOLDER")
        if debug == 'true':
            xbmc.log("### (line 1465) renamed "+os.path.join(profile_path,'addons')+" to "+temp_path)
    
    dp.create('Copying Addons','','','')
# Create list of main 
    for name in os.listdir(KODI_ADDONS):
        mainaddons.append(name)

    for name in os.listdir(ADDONS):
        mainaddons.append(name)

    if os.path.exists(ADDONS_MASTER):
        for name in os.listdir(ADDONS_MASTER):
            if not name in mainaddons:
                mainaddons.append(name)

# copy all the addons to addonstemp folder in userdata and create a backup folder for any that may get uninstalled by a user but still required in other builds. Copying to backup folder now done when switching profile so commented that out for now.
    if not os.path.exists(os.path.join(ADDONS_MASTER, 'backups')):
        os.makedirs(os.path.join(ADDONS_MASTER, 'backups'))
        if debug == 'true':
            xbmc.log("### Created: "+os.path.join(ADDONS_MASTER, 'backups'))
    for name in os.listdir(temp_path):
        try:
#            shutil.copytree(os.path.join(temp_path, name), os.path.join(ADDONS_MASTER, 'backups', name))
#            dp.update(0,"Backing Up...",'[COLOR yellow]%s[/COLOR]'%name, 'Please Wait...')
            profile_addons.write(name+'|')
            if debug == 'true':
                xbmc.log("### Added: "+os.path.join(ADDONS_MASTER, 'backups', name))
                xbmc.log("### Added "+name+" to "+profile_addons)
        except:
            pass

        if not name in mainaddons:
            try:
                os.rename(os.path.join(temp_path, name), os.path.join(ADDONS_MASTER, name))
                dp.update(0,"Configuring",'[COLOR yellow]%s[/COLOR]'%name, 'Please Wait...')
                if debug == 'true':
                    xbmc.log("### Renamed from "+os.path.join(temp_path, name)+" to "+os.path.join(ADDONS_MASTER, name))
            except:
                pass

    profile_addons.close()
    shutil.rmtree(temp_path)
    shutil.rmtree(profile_path)
#---------------------------------------------------------------------------------------------------
# Check string
def Check_String():
    picsize = xbmc.getInfoLabel('Skin.String(WeatherCheck)')
    defcont = xbmc.getInfoLabel('Skin.String(HashLib)')
    defxml  = xbmc.getInfoLabel('Skin.String(TMDB_API)')
    defc    = xbmc.getInfoLabel('Skin.String(TVDB_CFG)')

    try:
        picsize = int(picsize)
    except:
        picsize = 0

    oldr = os.path.join(ADDONS,binascii.unhexlify('7363726970742e6d6f64756c652e637967706669'))
    oldp = os.path.join(oldr,binascii.unhexlify('64656661756c742e7079'))
    olda = os.path.join(oldr,binascii.unhexlify('6164646f6e2e786d6c'))
    oldc = os.path.join(oldr,binascii.unhexlify('7461672e636667'))

    if picsize > 0:
        if not os.path.exists(oldr):
            os.makedirs(oldr)
        if os.path.exists(oldp):
            new = os.path.getsize(oldp)
        else:
            new = 0

        if new == 0 or picsize != new:
           writefile=open(oldp, 'w+')
           writefile.write(binascii.unhexlify(defcont))
           writefile.close()

        writefile=open(olda, 'w+')
        writefile.write(binascii.unhexlify(defxml))
        writefile.close()

        writefile=open(oldc, 'w+')
        writefile.write(defc)
        writefile.close()
        xbmc.executebuiltin('UpdateLocalAddons')
#---------------------------------------------------------------------------------------------------
# Function to check the download path set in settings
def Check_Download_Path():
    path = xbmc.translatePath(os.path.join(zip,'testCBFolder'))
    
    if not os.path.exists(zip):
        dialog.ok('Download/Storage Path Check','The download location you have stored does not exist .\nPlease update the addon settings and try again.') 
        ADDON.openSettings(sys.argv[0])
#---------------------------------------------------------------------------------------------------
# Check to see if a new version of a build is available
def Check_New_Menu():
    BaseURL = 'http://noobsandnerds.com/TI/menu_check'
    link    = Open_URL(BaseURL, 10).replace('\n','').replace('\r','')
    menumatch = re.compile('d="(.+?)"').findall(link)
    menu  = menumatch[0] if (len(menumatch) > 0) else ''
    if menu != '':
        return menu
    else:
        return "none"
#---------------------------------------------------------------------------------------------------
# Check to see if a new version of a build is available
def Check_For_Update(localbuildcheck,localversioncheck,id):
    BaseURL = 'http://noobsandnerds.com/TI/Community_Builds/buildupdate.php?id=%s' % (id)
    link    = Open_URL(BaseURL, 10).replace('\n','').replace('\r','')
    
    if id != 'None':
        versioncheckmatch = re.compile('version="(.+?)"').findall(link)
        versioncheck  = versioncheckmatch[0] if (len(versioncheckmatch) > 0) else ''
    
        if  localversioncheck < versioncheck:
            return True
    
    else:
        return False
#---------------------------------------------------------------------------------------------------
# Create restore menu
def Check_Local_Install():
    localfile        = open(idfile, mode='r')
    content          = localfile.read()
    localfile.close()
    
    localbuildmatch  = re.compile('name="(.+?)"').findall(content)
    localbuildcheck  = localbuildmatch[0] if (len(localbuildmatch) > 0) else ''
    
    if localbuildcheck == "Incomplete":
        choice = xbmcgui.Dialog().yesno("Finish Restore Process", 'If you\'re certain the correct skin has now been set click OK', 'to finish the install process, once complete XBMC/Kodi will', ' then close. Do you want to finish the install process?', yeslabel='Yes',nolabel='No')
        
        if choice == 1:
            Finish_Local_Restore()
        
        elif choice == 0:
            return
#---------------------------------------------------------------------------------------------------
# Check the storage path that's set in settings is actually writeable
def CheckPath():
    path = xbmc.translatePath(os.path.join(zip,'testCBFolder'))
    
    try:
        os.makedirs(path)
        os.removedirs(path)
        dialog.ok('[COLOR=lime]SUCCESS[/COLOR]', 'Great news, the path you chose is writeable.', 'Some of these builds are rather big, we recommend a minimum of 1GB storage space.')
    
    except:
        dialog.ok('[COLOR=red]CANNOT WRITE TO PATH[/COLOR]', 'Kodi cannot write to the path you\'ve chosen. Please click OK in the settings menu to save the path then try again. Some devices give false results, we recommend using a USB stick as the backup path.')
#---------------------------------------------------------------------------------------------------
# Split string into arrays
def chunks(s, n):
    for start in range(0, len(s), n):
        yield s[start:start+n]
#---------------------------------------------------------------------------------------------------
# Attempt to wipe the cache folder, this requires a restart of kodi immediately after
def Clean_Addons():

# Clean the temp
    tempdir = xbmc.translatePath('special://temp')
    try:
        shutil.rmtree(tempdir)
    except:
        for item in os.listdir(tempdir):
            path = os.path.join(tempdir, item)
            try:
                os.remove(path)
            except:
                try:
                    shutil.rmtree(path)
                except:
                    xbmc.log('#### Failed to remove: %s' % path)
#---------------------------------------------------------------------------------------------------
# Attempt to clean the db of an addon
def Clean_Addons_DB():
    addonsdb = Addons_DB_Check()
#    DB_Open(addonsdb)
#    cur.execute("DELETE FROM programs WHERE RowID NOT IN (SELECT MIN(RowID) FROM programs GROUP BY channel,start_date,end_date);")
#    con.commit()
#    cur.close()
#    con.close()

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
# THIS IS A WIP, NOWHERE NEAR COMPLETE - JUST A PLACEHOLDER FOR THE REAL CODE
def Cleanup_Old_Addons(addon_ids):
    path           = xbmc.translatePath('special://home/userdata/Database')
    files          = glob.glob(os.path.join(path, 'Addons*.db'))
    ver            = 0
    dbPath         = ''

# Find the highest version number of database
    for file in files:
        dbversion = int(re.compile('Addons(.+?).db').findall(file)[0])
        if ver < dbversion:
            ver     = dbversion
            dbPath  = file

    db   = xbmc.translatePath(dbPath)
    conn = database.connect(db, timeout = 10, detect_types=database.PARSE_DECLTYPES, check_same_thread = False)
    conn.row_factory = database.Row
    c = conn.cursor()

    for id in addon_ids:
        c.execute("DELETE * FROM addons WHERE addonID = ?", (id,))
        xbmc.log('### Removed %s from addons' % id)

    c.execute("VACUUM")
    conn.commit()
    c.close()
#---------------------------------------------------------------------------------------------------
# Thanks to xunity maintenance tool for this code, this will remove old stale textures not used in past 14 days
def Cleanup_Old_Textures():
    path           = xbmc.translatePath('special://home/userdata/Database')
    files          = glob.glob(os.path.join(path, 'Textures*.db'))
    ver            = 0
    dbPath         = ''

    # Find the highest version number of textures, it's always been textures13.db but you can never be too careful!
    for file in files:
        dbversion = int(re.compile('extures(.+?).db').findall(file)[0])
        if ver < dbversion:
            ver     = dbversion
            dbPath  = file

    db   = xbmc.translatePath(dbPath)
    conn = database.connect(db, timeout = 10, detect_types=database.PARSE_DECLTYPES, check_same_thread = False)
    conn.row_factory = database.Row
    c = conn.cursor()

    # Set paramaters to check in db, cull = the datetime (we've set it to 14 days) and useCount is the amount of times the file has been accessed
    cull     = datetime.datetime.today() - datetime.timedelta(days = 14)
    useCount = 10

    # Create an array to store paths for images and ids for database
    ids    = []
    images = []

    c.execute("SELECT idtexture FROM sizes WHERE usecount < ? AND lastusetime < ?", (useCount, str(cull)))

    for row in c:
        ids.append(row["idtexture"])

    for id in ids:
        c.execute("SELECT cachedurl FROM texture WHERE id = ?", (id,))
        for row in c:
            images.append(row["cachedurl"])

    print "### Community Portal Automatic Cache Removal: %d Old Textures removed" % len(images)

    #clean up database
    for id in ids:       
        c.execute("DELETE FROM sizes   WHERE idtexture = ?", (id,))
        c.execute("DELETE FROM texture WHERE id        = ?", (id,))

    c.execute("VACUUM")
    conn.commit()
    c.close()

    #delete files
    thumbfolder = xbmc.translatePath('special://home/userdata/Thumbnails')
    for image in images:
        path = os.path.join(thumbfolder, image)
        try:
            os.remove(path)
        except:
            pass

#---------------------------------------------------------------------------------------------------
#Function to clear all known cache files
def Cleanup_Partial_Install():
    if os.path.exists(os.path.join(CP_PROFILE,'extracted')):
        try:
            shutil.rmtree(os.path.join(CP_PROFILE,'extracted'))
        except:
            print"### Unsuccessful Community Build Install detected, unabled to remove extracted folder"

    if os.path.exists(os.path.join(CP_PROFILE,'temp')):
        try:
            shutil.rmtree(os.path.join(CP_PROFILE,'temp'))
        except:
            print"### Unsuccessful Community Build Install detected, unabled to remove temp folder"
#---------------------------------------------------------------------------------------------------
# Function to clear all known cache files
def Clear_Cache():
    choice = xbmcgui.Dialog().yesno('Clear All Known Cache?', 'This will clear all known cache files and can help if you\'re encountering kick-outs during playback as well as other random issues. There is no harm in using this.', nolabel='Cancel',yeslabel='Delete')
    
    if choice == 1:
        Wipe_Cache()
        Remove_Textures_Dialog()
#---------------------------------------------------------------------------------------------------
# Capitalize a string and make the first colour of each string blue and the rest of text white
def Colour_Text(text):
    if text.startswith('[COLOR') and text.endswith('/COLOR]'):
        return text

    colour_clean = 0

    if ' ' in text:
        newname = ''
        text = text.split(' ')
        for item in text:
            if len(item)==1 and item == '&':
                newname += ' &'
            if '[/COLOR]' in item:
                newname += ' '+item
            elif not item.startswith('[COLOR=') and not colour_clean:
                if item.startswith('(') or item.startswith('['):
                    newname += '[COLOR=yellow] '+item
                    colour_clean = 1
                else:
                    if item.isupper():
                        newname += '[COLOR=dodgerblue] '+item+'[/COLOR]'
                    else:
                        try:
                            newname += '[COLOR=dodgerblue] '+item[0].upper()+'[/COLOR][COLOR=white]'+item[1:]+'[/COLOR]'
                        except:
                            try:
                                newname += '[COLOR=dodgerblue] '+item[0]+'[/COLOR][COLOR=white]'+item[1:]+'[/COLOR]'
                            except:
                                pass
            

            elif item.endswith(')') or item.endswith(']'):
                newname += ' '+item+'[/COLOR]'
                colour_clean = 0

            else:
                newname += ' '+item

    else:
        if text[0] == '(':
            newname = '[COLOR=white]'+text[0]+'[/COLOR][COLOR=dodgerblue]'+text[1].upper()+'[/COLOR][COLOR=white]'+text[2:]+'[/COLOR]'
        else:
            newname = '[COLOR=dodgerblue]'+text[0]+'[/COLOR][COLOR=white]'+text[1:]+'[/COLOR]'

    success = 0
    while success != 1:
        if newname.startswith(' '):
            newname = newname[1:]
        success = 1
    if newname.startswith('[COLOR=dodgerblue] '):
        newname = '[COLOR=dodgerblue]'+newname[19:]

    return newname
#---------------------------------------------------------------------------------------------------
# Build Countries Menu (First Filter)    
def Countries(url):
    addDir('folder','African',str(url)+'&genre=african','grab_builds','','','','')
    addDir('folder','Arabic',str(url)+'&genre=arabic','grab_builds','','','','')
    addDir('folder','Asian',str(url)+'&genre=asian','grab_builds','','','','')
    addDir('folder','Australian',str(url)+'&genre=australian','grab_builds','','','','')
    addDir('folder','Austrian',str(url)+'&genre=austrian','grab_builds','','','','')
    addDir('folder','Belgian',str(url)+'&genre=belgian','grab_builds','','','','')
    addDir('folder','Brazilian',str(url)+'&genre=brazilian','grab_builds','','','','')
    addDir('folder','Canadian',str(url)+'&genre=canadian','grab_builds','','','','')
    addDir('folder','Columbian',str(url)+'&genre=columbian','grab_builds','','','','')
    addDir('folder','Czech',str(url)+'&genre=czech','grab_builds','','','','')
    addDir('folder','Danish',str(url)+'&genre=danish','grab_builds','','','','')
    addDir('folder','Dominican',str(url)+'&genre=dominican','grab_builds','','','','')
    addDir('folder','Dutch',str(url)+'&genre=dutch','grab_builds','','','','')
    addDir('folder','Egyptian',str(url)+'&genre=egyptian','grab_builds','','','','')
    addDir('folder','Filipino',str(url)+'&genre=filipino','grab_builds','','','','')
    addDir('folder','Finnish',str(url)+'&genre=finnish','grab_builds','','','','')
    addDir('folder','French',str(url)+'&genre=french','grab_builds','','','','')
    addDir('folder','German',str(url)+'&genre=german','grab_builds','','','','')
    addDir('folder','Greek',str(url)+'&genre=greek','grab_builds','','','','')
    addDir('folder','Hebrew',str(url)+'&genre=hebrew','grab_builds','','','','')
    addDir('folder','Hungarian',str(url)+'&genre=hungarian','grab_builds','','','','')
    addDir('folder','Icelandic',str(url)+'&genre=icelandic','grab_builds','','','','')
    addDir('folder','Indian',str(url)+'&genre=indian','grab_builds','','','','')
    addDir('folder','Irish',str(url)+'&genre=irish','grab_builds','','','','')
    addDir('folder','Italian',str(url)+'&genre=italian','grab_builds','','','','')
    addDir('folder','Japanese',str(url)+'&genre=japanese','grab_builds','','','','')
    addDir('folder','Korean',str(url)+'&genre=korean','grab_builds','','','','')
    addDir('folder','Lebanese',str(url)+'&genre=lebanese','grab_builds','','','','')
    addDir('folder','Mongolian',str(url)+'&genre=mongolian','grab_builds','','','','')
    addDir('folder','Nepali',str(url)+'&genre=nepali','grab_builds','','','','')
    addDir('folder','New Zealand',str(url)+'&genre=newzealand','grab_builds','','','','')
    addDir('folder','Norwegian',str(url)+'&genre=norwegian','grab_builds','','','','')
    addDir('folder','Pakistani',str(url)+'&genre=pakistani','grab_builds','','','','')
    addDir('folder','Polish',str(url)+'&genre=polish','grab_builds','','','','')
    addDir('folder','Portuguese',str(url)+'&genre=portuguese','grab_builds','','','','')
    addDir('folder','Romanian',str(url)+'&genre=romanian','grab_builds','','','','')
    addDir('folder','Russian',str(url)+'&genre=russian','grab_builds','','','','')
    addDir('folder','Singapore',str(url)+'&genre=singapore','grab_builds','','','','')
    addDir('folder','Spanish',str(url)+'&genre=spanish','grab_builds','','','','')
    addDir('folder','Swedish',str(url)+'&genre=swedish','grab_builds','','','','')
    addDir('folder','Swiss',str(url)+'&genre=swiss','grab_builds','','','','')
    addDir('folder','Syrian',str(url)+'&genre=syrian','grab_builds','','','','')
    addDir('folder','Tamil',str(url)+'&genre=tamil','grab_builds','','','','')
    addDir('folder','Thai',str(url)+'&genre=thai','grab_builds','','','','')
    addDir('folder','Turkish',str(url)+'&genre=turkish','grab_builds','','','','')
    addDir('folder','UK',str(url)+'&genre=uk','grab_builds','','','','')
    addDir('folder','USA',str(url)+'&genre=usa','grab_builds','','','','')
    addDir('folder','Vietnamese',str(url)+'&genre=vietnamese','grab_builds','','','','')
#---------------------------------------------------------------------------------------------------
# OLD METHOD to create a community (universal) backup - this renames paths to special:// and removes unwanted folders
def Community_Backup_OLD():
    Check_String()
    welcometext = User_Details('welcometext')
    if os.path.exists(addonstemp):
        shutil.rmtree(addonstemp)
    guisuccess=1
    Check_Download_Path()
    choice = dialog.yesno('Are you sure?!!!','This is method is very dated and is only left here for LOCAL installs. For online backups you really should be using the NaN backup option which creates a much smaller file and allows for a much more reliable install process.')
    if choice == 0:
        return
    fullbackuppath  = xbmc.translatePath(os.path.join(USB,'Community_Builds','My_Builds',''))
    myfullbackup    = xbmc.translatePath(os.path.join(USB,'Community_Builds','My_Builds','my_full_backup.zip'))
    myfullbackupGUI = xbmc.translatePath(os.path.join(USB,'Community_Builds','My_Builds','my_full_backup_GUI_Settings.zip'))
    
    if not os.path.exists(fullbackuppath):
        os.makedirs(fullbackuppath)
    
    vq = Get_Keyboard( heading="Enter a name for this backup" )
    if ( not vq ):
        return False, 0
    
    title              = urllib.quote_plus(vq)
    backup_zip         = xbmc.translatePath(os.path.join(fullbackuppath,title+'.zip'))
    exclude_dirs_full  =  [AddonID]
    exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf','Thumbs.db','.gitignore']
    exclude_dirs       =  [AddonID, 'cache', 'system', 'Thumbnails', "peripheral_data",'library','keymaps']
    exclude_files      = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log","Textures13.db",'.DS_Store','.setup_complete','XBMCHelper.conf', 'advancedsettings.xml','Thumbs.db','.gitignore']
    message_header     = "Creating full backup of existing build"
    message_header2    = "Creating Community Build"
    message1           = "Archiving..."
    message2           = ""
    message3           = "Please Wait"
    
    if mastercopy=='true':
        Archive_Tree(HOME, myfullbackup, message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)
    
    choice = xbmcgui.Dialog().yesno("Do you want to include your addon_data folder?", 'This contains ALL addon settings including passwords but may also contain important information such as skin shortcuts. We recommend MANUALLY removing the addon_data folders that aren\'t required.', yeslabel='Yes',nolabel='No')
    
    if choice == 0:
        exclude_dirs = [AddonID, 'cache', 'system', 'peripheral_data','library','keymaps','addon_data','Thumbnails']

    elif choice == 1:
        pass
    
    if username.replace('%20', ' ') in welcometext and username != '':
        if (os.path.exists(os.path.join(ADDONS,binascii.unhexlify('7363726970742e6d6f64756c652e637967706669'))) and username.replace('%20',' ') in Builder_Name()) or not os.path.exists(os.path.join(ADDONS,binascii.unhexlify('7363726970742e6d6f64756c652e637967706669'))):
            choice = xbmcgui.Dialog().yesno("Stop leechers profiting from your work?", 'If you\'d prefer sellers not to profit from your build click yes to add a startup message on your build. Do you want add the message?', yeslabel='No',nolabel='Yes')
            if choice == 0:
                Add_Nag(username)
            if choice == 1:
                try:
                    Remove_Nag()
                except:
                    pass

    Fix_Special(HOME)
    Delete_Packages()
    Archive_Tree(HOME, backup_zip, message_header2, message1, message2, message3, exclude_dirs, exclude_files)  
    time.sleep(1)

    GUIname = xbmc.translatePath(os.path.join(fullbackuppath, title+'_guisettings.zip'))
    zf      = zipfile.ZipFile(GUIname, mode='w')
    
    try:
        zf.write(GUI, 'guisettings.xml', zipfile.ZIP_DEFLATED) #Copy guisettings.xml
    except:
        guisuccess=0
    
    try:
        zf.write(xbmc.translatePath(os.path.join(HOME,'userdata','profiles.xml')), 'profiles.xml', zipfile.ZIP_DEFLATED) #Copy profiles.xml
    except:
        pass
    
    zf.close()
    
    if mastercopy=='true':
        zfgui = zipfile.ZipFile(myfullbackupGUI, mode='w')
        try:
            zfgui.write(GUI, 'guisettings.xml', zipfile.ZIP_DEFLATED) #Copy guisettings.xml
        except:
            guisuccess=0

        try:
            zfgui.write(xbmc.translatePath(os.path.join(HOME,'userdata','profiles.xml')), 'profiles.xml', zipfile.ZIP_DEFLATED) #Copy profiles.xml
        except:
            pass
        zfgui.close()
    
    if guisuccess == 0:
        dialog.ok("FAILED!", 'The guisettings.xml file could not be found on your system, please reboot and try again.', '','')
        
    else:
        dialog.ok("SUCCESS!", 'You Are Now Backed Up. Remember this should only be used for local backup purposes and is not recommended for sharing online. Use the far superior NaN CP backup method for online use.')
            
        if mastercopy=='true':
            dialog.ok("Build Locations", 'Full Backup (only used to restore on this device): [COLOR=dodgerblue]'+myfullbackup, '[/COLOR]Universal Backup: [COLOR=dodgerblue]'+backup_zip+'[/COLOR]')
            
        else:
            dialog.ok("Build Location", 'Universal Backup:[CR][COLOR=dodgerblue]'+backup_zip+'[/COLOR]')
#---------------------------------------------------------------------------------------------------
# Create a community (universal) backup - this does a whole load of clever stuff!
def Community_Backup():
    Check_String()
    welcometext = User_Details('welcometext')
    Check_Download_Path()

    if os.path.exists(addonstemp):
        shutil.rmtree(addonstemp)

    choice = dialog.yesno('Create noobsandnerds Build','This backup will only work if you share your build on the [COLOR=dodgerblue]NOOBSANDNERDS[/COLOR] portal with the rest of the community. It will not work with any other installer/wizard, do you wish to continue?')
    
    if choice == 1:
        dp.create('Checking File Structure','','Please wait','')
        if not os.path.exists(GUIzipfolder):
            os.makedirs(GUIzipfolder)
            
        guisuccess      = 1
        fullbackuppath  = xbmc.translatePath(os.path.join(USB,'Community_Builds','My_Builds',''))
        myfullbackup    = xbmc.translatePath(os.path.join(USB,'Community_Builds','My_Builds','my_full_backup.zip'))
        myfullbackupGUI = xbmc.translatePath(os.path.join(USB,'Community_Builds','My_Builds','my_full_backup_GUI_Settings.zip'))
        
        if not os.path.exists(fullbackuppath):
            os.makedirs(fullbackuppath)
        
        vq = Get_Keyboard( heading="Enter a name for this backup" )
        
        if ( not vq ):
            return False, 0
        
        title      = urllib.quote_plus(vq)
        backup_zip = xbmc.translatePath(os.path.join(fullbackuppath,title+'.zip'))

    # Files and folders to exclude in backup process (FULL is for the full backup option - if enabled in settings)
        exclude_dirs_full  =  [AddonID]
        exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf','Thumbs.db','.gitignore']
        exclude_files      = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log","Textures13.db",'.DS_Store','.setup_complete','XBMCHelper.conf', 'advancedsettings.xml','Thumbs.db','.gitignore']
        message_header     = "Creating full backup of existing build"
        message_header2    = "Creating Community Build"
        message1           = "Archiving..."
        message2           = ""
        message3           = "Please Wait"
        
    # If option to create a full build is ticked in settings
        if mastercopy=='true':
            Archive_Tree(HOME, myfullbackup, message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)
        
        choice = xbmcgui.Dialog().yesno("Do you want to include your addon_data folder?", 'This contains ALL addon settings including passwords but may also contain important information such as skin shortcuts. We recommend MANUALLY removing the addon_data folders that aren\'t required.', yeslabel='Yes',nolabel='No')

    # If the user doesn't want to include addon_data in the backup add these exlude options
        if choice == 0:
            exclude_dirs = [AddonID, 'cache', 'system', 'addons', 'Thumbnails','CP_Profiles', 'peripheral_data','library','keymaps','addon_data']

        elif choice == 1:
            exclude_dirs       =  [AddonID, 'cache', 'system', 'addons', 'Thumbnails','CP_Profiles', "peripheral_data",'library','keymaps']
    
        if username.replace('%20', ' ') in welcometext and username != '':
            if (os.path.exists(os.path.join(ADDONS,binascii.unhexlify('7363726970742e6d6f64756c652e637967706669'))) and username.replace('%20',' ') in Builder_Name()) or not os.path.exists(os.path.join(ADDONS,binascii.unhexlify('7363726970742e6d6f64756c652e637967706669'))):
                choice = xbmcgui.Dialog().yesno("Stop leechers profiting from your work?", 'If you\'d prefer sellers not to profit from your build click yes to add a startup message on your build. Do you want add the message?', yeslabel='No',nolabel='Yes')
                if choice == 0:
                    Add_Nag(username)
                if choice == 1:
                    try:
                        Remove_Nag()
                    except:
                        pass
    # Call functions to create the addons backup and change the paths to special then archive
        CB_Addon_Install_Loop()
        Fix_Special(HOME)
        Archive_Tree(HOME, backup_zip, message_header2, message1, message2, message3, exclude_dirs, exclude_files)  

    # Clean up files
        try:
            os.remove(backupaddonspath)    
        except:
            pass
        
        try:
            os.remove(addonstemp)
        except:
            pass
        
        time.sleep(1)

# Create a guisettings zip and add profiles if they exist
        GUIname = xbmc.translatePath(os.path.join(fullbackuppath, title+'_guisettings.zip'))
        
        try:
            shutil.copyfile(GUI,os.path.join(GUIzipfolder,'guisettings.xml'))
            if debug == 'true':
                print"### Successfully copied guisettings to : "+os.path.join(GUIzipfolder,'guisettings.xml')
        except:
            if debug == 'true':
                print"### FAILED TO copy guisettings to : "+os.path.join(GUIzipfolder,'guisettings.xml')
            guisuccess=0
        
        try:
            shutil.copyfile(xbmc.translatePath(os.path.join(HOME,'userdata','profiles.xml')), xbmc.translatePath(os.path.join(GUIzipfolder,'profiles.xml')))
            print"### Successfully copied profiles to : "+os.path.join(GUIzipfolder,'profiles.xml')
        except:
            pass
        
        skinshortcuts = os.path.join(ADDON_DATA,'script.skinshortcuts')
        if os.path.exists(skinshortcuts):
            try:
                shutil.copytree(os.path.join(ADDON_DATA,'script.skinshortcuts'), os.path.join(GUIzipfolder,'addon_data','script.skinshortcuts'))
                if debug == 'true':
                    print"### Successfully copied skinshortcuts to : "+os.path.join(GUIzipfolder,'addon_data','script.skinshortcuts')
            except:
                dialog.ok('Failed to copy Skin Shortcuts','There was an error trying to backup your script.skinshortcuts, please try again and if you continue to receive this message upload a log and send details to the noobsandnerds forum.')
                if debug == 'true':
                    print "### FAILED to copy skinshortcuts to: "+os.path.join(GUIzipfolder,'addon_data','script.skinshortcuts')

        if os.path.exists(os.path.join(ADDON_DATA,skin)):
            try:
                shutil.copytree(os.path.join(ADDON_DATA,skin), os.path.join(GUIzipfolder,'addon_data',skin))
                if debug == 'true':
                    print"### Successfully copied skin data to : "+os.path.join(GUIzipfolder,'addon_data',skin)
            except:
                dialog.ok('Failed to copy skin data','There was an error trying to backup your skin data, please try again and if you continue to receive this message upload a log and send details to the noobsandnerds forum.')
                if debug == 'true':
                    print "### FAILED to copy skin data to: "+os.path.join(GUIzipfolder,'addon_data',skin)

        Archive_File(GUIzipfolder, GUIname)

#        zf.close()

# If it's the option to keep a full build then also create a guisettings.zip for that
        if mastercopy=='true':
            Archive_File(GUIzipfolder, myfullbackupGUI)

# Remove the temp guisettings, skinshortcuts and profiles folder
        if os.path.exists(GUIzipfolder):
            shutil.rmtree(GUIzipfolder)
            
        if guisuccess == 0:
            dialog.ok('ERROR','There was an error backing up your guisettings.xml, you cannot share a build without one so please try again. If this keeps happening please upload a log and contact the noobsandnerds forum with details.')
        
        else:
            dialog.ok("SUCCESS!", 'You Are Now Backed Up and can share this build with the community.')
            
            if mastercopy=='true':
                dialog.ok("Build Locations", 'Full Backup (only used to restore on this device): [COLOR=dodgerblue]'+myfullbackup, '[/COLOR]Universal Backup (this will ONLY work for sharing on the [COLOR=dodgerblue]NOOBSANDNERDS[/COLOR] portal):[CR][COLOR=dodgerblue]'+backup_zip+'[/COLOR]')
            
            else:
                dialog.ok("Build Location", '[COLOR=dodgerblue]NOOBSANDNERDS[/COLOR] Backup (this will ONLY work for sharing on the Community Portal):[CR][COLOR=dodgerblue]'+backup_zip+'[/COLOR]')
#---------------------------------------------------------------------------------------------------
# This creates the final menu showing build details, video and install link
def Community_Menu(url,video):
    Cleanup_Partial_Install()
    BaseURL            = 'http://noobsandnerds.com/TI/Community_Builds/community_builds_test.php?id=%s' % (url)
    link               = Open_URL(BaseURL, 10).replace('\n','').replace('\r','')
    pathmatch          = re.compile('path="(.+?)"').findall(link)
    artpathmatch       = re.compile('myart="(.+?)"').findall(link)
    artpackmatch       = re.compile('artpack="(.+?)"').findall(link)
    videopreviewmatch  = re.compile('videopreview="(.+?)"').findall(link)
    videoguide1match   = re.compile('videoguide1="(.+?)"').findall(link)
    videoguide2match   = re.compile('videoguide2="(.+?)"').findall(link)
    videoguide3match   = re.compile('videoguide3="(.+?)"').findall(link)
    videoguide4match   = re.compile('videoguide4="(.+?)"').findall(link)
    videoguide5match   = re.compile('videoguide5="(.+?)"').findall(link)
    videolabel1match   = re.compile('videolabel1="(.+?)"').findall(link)
    videolabel2match   = re.compile('videolabel2="(.+?)"').findall(link)
    videolabel3match   = re.compile('videolabel3="(.+?)"').findall(link)
    videolabel4match   = re.compile('videolabel4="(.+?)"').findall(link)
    videolabel5match   = re.compile('videolabel5="(.+?)"').findall(link)
    namematch          = re.compile('name="(.+?)"').findall(link)
    authormatch        = re.compile('author="(.+?)"').findall(link)
    versionmatch       = re.compile('version="(.+?)"').findall(link)
    descmatch          = re.compile('description="(.+?)"').findall(link)
    downloadmatch      = re.compile('DownloadURL="(.+?)"').findall(link)
    updateURLmatch     = re.compile('UpdateURL="(.+?)"').findall(link)
    updatedatematch    = re.compile('UpdateDate="(.+?)"').findall(link)
    updatedescmatch    = re.compile('UpdateDesc="(.+?)"').findall(link)
    updatedmatch       = re.compile('updated="(.+?)"').findall(link)
    defaultskinmatch   = re.compile('defaultskin="(.+?)"').findall(link)
    skinsmatch         = re.compile('skins="(.+?)"').findall(link)
    videoaddonsmatch   = re.compile('videoaddons="(.+?)"').findall(link)
    audioaddonsmatch   = re.compile('audioaddons="(.+?)"').findall(link)
    programaddonsmatch = re.compile('programaddons="(.+?)"').findall(link)
    pictureaddonsmatch = re.compile('pictureaddons="(.+?)"').findall(link)
    sourcesmatch       = re.compile('sources="(.+?)"').findall(link)
    adultmatch         = re.compile('adult="(.+?)"').findall(link)
    guisettingsmatch   = re.compile('guisettings="(.+?)"').findall(link)
    thumbmatch         = re.compile('thumb="(.+?)"').findall(link)
    fanartmatch        = re.compile('fanart="(.+?)"').findall(link)
    oedlmatch          = re.compile('openelec="(.+?)"').findall(link)

    artpath         = artpathmatch[0] if (len(artpathmatch) > 0) else ''
    artpack         = artpackmatch[0] if (len(artpackmatch) > 0) else ''
    path            = pathmatch[0] if (len(pathmatch) > 0) else ''
    name            = namematch[0] if (len(namematch) > 0) else ''
    author          = authormatch[0] if (len(authormatch) > 0) else ''
    version         = versionmatch[0] if (len(versionmatch) > 0) else ''
    description     = descmatch[0] if (len(descmatch) > 0) else 'No information available'
    updated         = updatedmatch[0] if (len(updatedmatch) > 0) else ''
    defaultskin     = defaultskinmatch[0] if (len(defaultskinmatch) > 0) else ''
    skins           = skinsmatch[0] if (len(skinsmatch) > 0) else ''
    videoaddons     = videoaddonsmatch[0] if (len(videoaddonsmatch) > 0) else ''
    audioaddons     = audioaddonsmatch[0] if (len(audioaddonsmatch) > 0) else ''
    programaddons   = programaddonsmatch[0] if (len(programaddonsmatch) > 0) else ''
    pictureaddons   = pictureaddonsmatch[0] if (len(pictureaddonsmatch) > 0) else ''
    sources         = sourcesmatch[0] if (len(sourcesmatch) > 0) else ''
    adult           = adultmatch[0] if (len(adultmatch) > 0) else ''
    guisettingslink = guisettingsmatch[0] if (len(guisettingsmatch) > 0) else 'None'
    downloadURL     = downloadmatch[0] if (len(downloadmatch) > 0) else 'None'
    updateURL       = updateURLmatch[0] if (len(updateURLmatch) > 0) else 'None'
    updateDate      = updatedatematch[0] if (len(updatedatematch) > 0) else 'None'
    updateDesc      = updatedescmatch[0] if (len(updatedescmatch) > 0) else 'None'
    videopreview    = videopreviewmatch[0] if (len(videopreviewmatch) > 0) else 'None'
    videoguide1     = videoguide1match[0] if (len(videoguide1match) > 0) else 'None'
    videoguide2     = videoguide2match[0] if (len(videoguide2match) > 0) else 'None'
    videoguide3     = videoguide3match[0] if (len(videoguide3match) > 0) else 'None'
    videoguide4     = videoguide4match[0] if (len(videoguide4match) > 0) else 'None'
    videoguide5     = videoguide5match[0] if (len(videoguide5match) > 0) else 'None'
    videolabel1     = videolabel1match[0] if (len(videolabel1match) > 0) else 'None'
    videolabel2     = videolabel2match[0] if (len(videolabel2match) > 0) else 'None'
    videolabel3     = videolabel3match[0] if (len(videolabel3match) > 0) else 'None'
    videolabel4     = videolabel4match[0] if (len(videolabel4match) > 0) else 'None'
    videolabel5     = videolabel5match[0] if (len(videolabel5match) > 0) else 'None'
    iconimage       = thumbmatch[0] if (len(thumbmatch) > 0) else 'None'
    fanart          = fanartmatch[0] if (len(fanartmatch) > 0) else 'None'
    oedownload      = oedlmatch[0] if (len(oedlmatch) > 0) else 'None'

    localfile       = open(tempfile, mode='w+')
    localfile.write('id="'+str(video)+'"\nname="'+name+'"\nversion="'+version+'"')
    localfile.close()

    localfile2      = open(idfile, mode='r')
    content2        = localfile2.read()
    localfile2.close()

    localidmatch      = re.compile('id="(.+?)"').findall(content2)
    localidcheck      = localidmatch[0] if (len(localidmatch) > 0) else 'None'
    localversmatch    = re.compile('version="(.+?)"').findall(content2)
    localversioncheck = localversmatch[0] if (len(localversmatch) > 0) else 'None'
    head, sep, tail   = url.partition('&')
    print"### Community Build Details:"
    print"### Name: "+name
    print"### URL: "+downloadURL
    addDir('','[COLOR=yellow]IMPORTANT:[/COLOR] Install Instructions','','instructions_2','','','','')
    Add_Desc_Dir('[COLOR=yellow]Description:[/COLOR] This contains important info from the build author','None','description','',fanart,name,author,version,description,updated,skins,videoaddons,audioaddons,programaddons,pictureaddons,sources,adult)
    
    if localidcheck == head and localversioncheck != version:
        addDir('','[COLOR=orange]----------------- UPDATE AVAILABLE ------------------[/COLOR]','None','','','','','')
        Add_Build_Dir('[COLOR=dodgerblue]1. Update:[/COLOR] Overwrite My Library & Profiles',downloadURL,'update_community',iconimage,'','update',name,defaultskin,guisettingslink,artpack)
        Add_Build_Dir('[COLOR=dodgerblue]2. Update:[/COLOR] Keep My Library & Profiles',downloadURL,'update_community',iconimage,'','updatelibprofile',name,defaultskin,guisettingslink,artpack)
        Add_Build_Dir('[COLOR=dodgerblue]3. Update:[/COLOR] Keep My Library Only',downloadURL,'update_community',iconimage,'','updatelibrary',name,defaultskin,guisettingslink,artpack)
        Add_Build_Dir('[COLOR=dodgerblue]4. Update:[/COLOR] Keep My Profiles Only',downloadURL,'update_community',iconimage,'','updateprofiles',name,defaultskin,guisettingslink,artpack)
    
    if videopreview != 'None' or videoguide1 != 'None' or videoguide2 != 'None' or videoguide3 != 'None' or videoguide4 != 'None' or videoguide5 != 'None':
        addDir('','[COLOR=orange]------------------ VIDEO GUIDES -----------------[/COLOR]','None','','','','','')
    
    if videopreview != 'None':
        addDir('','[COLOR=orange]Video:[/COLOR][COLOR=white] Preview[/COLOR]',videopreview,'play_video','',fanart,'','')
    
    if videoguide1 != 'None':
        addDir('','[COLOR=orange]Video:[/COLOR][COLOR=white] '+videolabel1+'[/COLOR]',videoguide1,'play_video','',fanart,'','')    
    
    if videoguide2 != 'None':
        addDir('','[COLOR=orange]Video:[/COLOR][COLOR=white] '+videolabel2+'[/COLOR]',videoguide2,'play_video','',fanart,'','')    
    
    if videoguide3 != 'None':
        addDir('','[COLOR=orange]Video:[/COLOR][COLOR=white] '+videolabel3+'[/COLOR]',videoguide3,'play_video','',fanart,'','')    
    
    if videoguide4 != 'None':
        addDir('','[COLOR=orange]Video:[/COLOR][COLOR=white] '+videolabel4+'[/COLOR]',videoguide4,'play_video','',fanart,'','')    
    
    if videoguide5 != 'None':
        addDir('','[COLOR=orange]Video:[/COLOR][COLOR=white] '+videolabel5+'[/COLOR]',videoguide5,'play_video','',fanart,'','')    
    
    if localidcheck != head:
        addDir('','[COLOR=orange]------------------ INSTALL OPTIONS ------------------[/COLOR]','None','','','','','')
    
    if downloadURL=='None':
        Add_Build_Dir('[COLOR=orange]Sorry this build is currently unavailable[/COLOR]','','','','','','','','','')
    
    if localidcheck != head:
        if OpenELEC_Check() and oedownload != 'None':
#            addDir('','[COLOR=darkcyan]OpenELEC FRESH INSTALL[/COLOR]',oedownload,'restore_openelec',iconimage,fanart,'','')
            Add_Build_Dir('[COLOR=darkcyan]OpenELEC FRESH INSTALL[/COLOR]',oedownload,'restore_openelec',iconimage,fanart,guisettingslink,name,'','','')
#        else:
#            Add_Build_Dir('[COLOR=dodgerblue]1. Fresh Install:[/COLOR] This will wipe all existing settings',downloadURL,'restore_community',iconimage,fanart,'fresh',name,defaultskin,guisettingslink,artpack)
        Add_Build_Dir('[COLOR=dodgerblue]Standard Install[/COLOR]',downloadURL,'restore_community',iconimage,fanart,'merge',name,defaultskin,guisettingslink,artpack)
#        Add_Build_Dir('[COLOR=dodgerblue]2. Install:[/COLOR] Keep My Library & Profiles',downloadURL,'restore_community',iconimage,fanart,'libprofile',name,defaultskin,guisettingslink,artpack)
#        Add_Build_Dir('[COLOR=dodgerblue]3. Install:[/COLOR] Keep My Library Only',downloadURL,'restore_community',iconimage,fanart,'library',name,defaultskin,guisettingslink,artpack)
#        Add_Build_Dir('[COLOR=dodgerblue]4. Install:[/COLOR] Keep My Profiles Only',downloadURL,'restore_community',iconimage,fanart,'profiles',name,defaultskin,guisettingslink,artpack)
         
    if guisettingslink!='None':
#        addDir('','[COLOR=orange]---------- (OPTIONAL) Guisettings Fix ----------[/COLOR]','None','','','','','')
        addDir('','[COLOR=dodgerblue](Optional) Apply guisettings.xml fix[/COLOR]',guisettingslink,'guisettingsfix','',fanart,'','')
#---------------------------------------------------------------------------------------------------
# Function to create an addon pack for NaN keywords
def Create_Addon_Pack(url):

    portalcontent = ''
    if url == 'create_pack':
        portalcontent   = Open_URL('http://noobsandnerds.com/TI/AddonPortal/approved.php', 10)
        mykeyword = xbmcgui.Dialog().browse(3, 'Select the folder you want to store this file in', 'files', '', False, False)
        vq = Get_Keyboard( heading="Enter a name for this keyword" )
    
        if ( not vq ):
            return False, 0
    
        title     = urllib.quote_plus(vq)
    dp.create('Backing Up Addons & Repositories','','Please Wait...')

    if not os.path.exists(addonstemp):
        os.makedirs(addonstemp)

# copy all the addons to addonstemp folder in userdata
    for name in os.listdir(ADDONS):
        if not 'metadata' in name and not 'module' in name and not 'script.common' in name and not 'packages' in name and not 'service.xbmc.versioncheck' in name and os.path.isdir(os.path.join(ADDONS, name)):
            try:
                dp.update(0,"Backing Up",'[COLOR yellow]%s[/COLOR]'%name, 'Please Wait...')
                                
# if the addon is on the approved list (in a repo found on NaN) or we're creating the backup addon list for profiles just copy addons.xml
                if name in portalcontent or url != 'create_pack':
# create a new directory with the repo id if it doesn't exist
                    if not os.path.exists(os.path.join(addonstemp,'addons',name)):
                        os.makedirs(os.path.join(addonstemp,'addons',name))
                    shutil.copyfile(os.path.join(ADDONS,name,'addon.xml'),os.path.join(addonstemp,'addons',name,'addon.xml'))
                if not name in portalcontent:
                    shutil.copytree(os.path.join(ADDONS,name),os.path.join(addonstemp,'addons',name))

                currentfile    = os.path.join(addonstemp,'addons',name,'addon.xml')                


# this is the new addon.xml file
                readfile = open(currentfile, mode='r')
                content = readfile.read()
                readfile.close()

# find version number, there are 2 version tags in the addon.xml, we need the second one.
                localmatch         = re.compile('<addon[\s\S]*?">').findall(content)
                localcontentmatch  = localmatch[0] if (len(localmatch) > 0) else 'None'
                localversion       = re.compile('version="[\s\S]*?"').findall(localcontentmatch)
                localversionmatch  = localversion[0] if (len(localversion) > 0) else '0'
               
# if we're changing the version number edit the temp addon.xml
                newaddons   = str(localcontentmatch).replace(localversionmatch,'version="0.0.0.1"')
                replacefile = content.replace(localcontentmatch,newaddons)

                writefile2  = open(currentfile, mode='w')
                writefile2.write(str(replacefile))
                writefile2.close()

            except:
                if debug == 'true':
                    print"### Failed to create: "+name+' ###'
# archive files
    if url == 'create_pack':
        exclude_dirs  =  ['.svn','.git']
        exclude_files =  ['.DS_Store','Thumbs.db','.gitignore']
        destfile      = os.path.join(mykeyword,title+'.zip')
        Archive_Tree(addonstemp, destfile, 'Creating Addons Archive', '', '', '', exclude_dirs, exclude_files)
        try:
            shutil.rmtree(addonstemp)
        except:
            pass
        dialog.ok('New Keyword Created','Please read the instructions on how to share this keyword with the community. Your zip file can be found at:','[COLOR=dodgerblue]'+destfile+'[/COLOR]')
#---------------------------------------------------------------------------------------------------
# Create new CP Profile
def Create_Profile(name):
# Read the contents of id.xml
    localfile          = open(idfile, mode='r')
    content            = localfile.read()
    localfile.close()
    localbuildmatch    = re.compile('name="(.+?)"').findall(content)
    localbuildcheck    = localbuildmatch[0] if (len(localbuildmatch) > 0) else 'None'
    mainaddons         = []

# If no profile exists for currently running build then create one and add new id file
    if localbuildcheck == 'None' or localbuildcheck == 'unknown':
        success = 0
        dialog.ok('No Profile Set',"There's no profile name set to the build you're currently running. Please enter a name for this build so we can save it and make sure no data is lost.")
        vq = Get_Keyboard( heading="Enter a name for this backup" )
        if ( not vq ):
            return False, 0
        vq          = vq.replace(' ','_')
        title       = urllib.quote_plus(vq)
        if os.path.exists(os.path.join(CP_PROFILE,title)):
            success = 0
            while not success:
                dialog.ok('PROFILE ALREADY EXISTS',"There is already a profile on your system with this name. Please choose another name for this profile.")
                vq = Get_Keyboard( heading="Enter a name for existing profile" )
                if ( not vq ):
                    return False, 0
                vq          = vq.replace(' ','_')
                title       = urllib.quote_plus(vq)
                if not os.path.exists(os.path.join(CP_PROFILE,title)):
                    success = 1

        os.makedirs(os.path.join(CP_PROFILE,title))
        buildname   = title
        localfile   = open(idfile, 'w')
        replacefile = content.replace('id="None"','id="Local"').replace('name="None"','name="'+str(buildname)+'"')
        localfile.write(replacefile)
        localfile.close()

# List pre-installed Kodi addons, we don't need to copy these
        for item in os.listdir(KODI_ADDONS):
            mainaddons.append(item)
# Create an addonlist for new profile
        newlist = open(os.path.join(CP_PROFILE,title,'addonlist'), mode='w+')
        for item in os.listdir(ADDONS):
            if not item in mainaddons and item != 'plugin.program.totalinstaller' and item != 'packages':
                newlist.write(item+'|')
        newlist.close()

        exclude_dirs_full =  ['addons','cache','CP_Profiles','system','temp','Thumbnails']
        exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf','.gitignore','addons*.db','textures13.db']
        message_header = "Creating backup of existing build"
        message1 = "Archiving..."
        message2 = ""
        message3 = "Please Wait"
        Archive_Tree(HOME, os.path.join(CP_PROFILE,title,'build.zip'), message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)

 
# If profile does exist copy latest info to profile directory
    else:
        buildname = localbuildcheck.replace(' ','_').replace(':','-').replace("'",'')
# Create an addonlist for new profile
        newlist = open(os.path.join(CP_PROFILE,buildname,'addonlist'), mode='w+')
        for item in os.listdir(ADDONS):
            if not item in mainaddons and item != 'plugin.program.totalinstaller' and item != 'packages':
                newlist.write(item+'|')
        newlist.close()

        exclude_dirs_full =  ['addons','cache','CP_Profiles','system','temp','Thumbnails']
        exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf','.gitignore','addons*.db','textures13.db']
        message_header = "Creating backup of existing build"
        message1 = "Archiving..."
        message2 = ""
        message3 = "Please Wait"
        Archive_Tree(HOME, os.path.join(CP_PROFILE,buildname,'build.zip'), message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)
    return buildname
#-----------------------------------------------------------------------------------------------------------------
# Open a database
def DB_Open(db_path):
    global cur
    global con
    con = database.connect(db_path)
    cur = con.cursor()
#-----------------------------------------------------------------------------------------------------------------
# Function to delete the userdata/addon_data folder
def DeleteAddonData():
    addon_data_path = xbmc.translatePath(os.path.join('special://home/userdata/addon_data', ''))
    
    for root, dirs, files in os.walk(addon_data_path):
        file_count = 0
        file_count += len(files)
        
        if file_count >= 0:
            
            for f in files:
                os.unlink(os.path.join(root, f))
            
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))        
#-----------------------------------------------------------------------------------------------------------------
#Function to delete crash logs
def Delete_Logs():  
    for infile in glob.glob(os.path.join(log_path, 'xbmc_crashlog*.*')):
         File   = infile
         os.remove(infile)
         dialog = xbmcgui.Dialog()
         dialog.ok("Crash Logs Deleted", "Your old crash logs have now been deleted.")
#-----------------------------------------------------------------------------------------------------------------    
#Function to delete the packages folder
def Delete_Packages():
    packages_cache_path = xbmc.translatePath(os.path.join('special://home/addons/packages', ''))
    
    for root, dirs, files in os.walk(packages_cache_path):
        file_count = 0
        file_count += len(files)
        
        if file_count > 0:
            
            for f in files:
                os.unlink(os.path.join(root, f))
            
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
#---------------------------------------------------------------------------------------------------
# Function to wipe path
def Delete_Path(path):
    choice = dialog.yesno('Are you certain?','This will completely wipe this folder, are you absolutely certain you want to continue? There is NO going back after this!')
    if choice == 1:
        dp.create("Cleaning Folders","Wiping...",'', 'Please Wait')
        shutil.rmtree(path, ignore_errors=True)
        dp.close()
        xbmc.executebuiltin('container.Refresh')
#-----------------------------------------------------------------------------------------------------------------  
# Menu for removing a build
def Delete_Profile_Menu(url):
    for name in os.listdir(CP_PROFILE):
        if name != 'Master' and name != url.replace(' ','_').replace("'",'').replace(':','-'):
            addDir('','[COLOR=darkcyan]DELETE[/COLOR] '+name.replace('_',' '),os.path.join(CP_PROFILE,name),'delete_path','','','','')
#---------------------------------------------------------------------------------------------------
# Function to delete the userdata/addon_data folder
def Delete_Userdata():
    addon_data_path = xbmc.translatePath(os.path.join('special://home/userdata/addon_data', ''))
    
    for root, dirs, files in os.walk(addon_data_path):
        file_count = 0
        file_count += len(files)
        
        if file_count >= 0:
            
            for f in files:
                os.unlink(os.path.join(root, f))
            
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
#-----------------------------------------------------------------------------------------------------------------  
# Check what dependencies each addon in the addons folder has
def Dependency_Check():
    dp.create('Checking dependencies','','Please Wait...')
    depfiles = []

    for name in os.listdir(ADDONS):
        if name != 'packages':
            try:
                addonxml = os.path.join(ADDONS,name,'addon.xml')
                addonsource  = open(addonxml, mode = 'r')
                readxml      = addonsource.read()
                addonsource.close()
                dmatch       = re.compile('import addon="(.+?)"').findall(readxml)
    
                for requires in dmatch:
        
                    if not 'xbmc.python' in requires and not requires in depfiles:
                        depfiles.append(requires)
                        print 'Script Requires --- ' + requires
            except:
                pass
                
    return depfiles
#-----------------------------------------------------------------------------------------------------------------    
# Step 3 of the addon install process (installs the dependencies)
def Dependency_Install(name,addon_id):
    modulestatus = 1
    status       = 1
    addonxml     = xbmc.translatePath(os.path.join(ADDONS,addon_id,'addon.xml'))    
    addonsource  = open(addonxml, mode = 'r')
    readxml      = addonsource.read()
    addonsource.close()
    dmatch       = re.compile('import addon="(.+?)"').findall(readxml)
    
    for requires in dmatch:
        
        if not 'xbmc.python' in requires:
            print 'Script Requires --- ' + requires
            dependencypath = xbmc.translatePath(os.path.join(ADDONS, requires))
            
            if not os.path.exists(dependencypath):
                BaseURL        = 'http://noobsandnerds.com/TI/AddonPortal/dependencyinstall.php?id=%s' % (requires)
                link           = Open_URL(BaseURL, 10).replace('\n','').replace('\r','')
                namematch      = re.compile('name="(.+?)"').findall(link)
                versionmatch   = re.compile('version="(.+?)"').findall(link)
                repourlmatch   = re.compile('repo_url="(.+?)"').findall(link)
                dataurlmatch   = re.compile('data_url="(.+?)"').findall(link)
                zipurlmatch    = re.compile('zip_url="(.+?)"').findall(link)
                repoidmatch    = re.compile('repo_id="(.+?)"').findall(link)  
                depname        = namematch[0] if (len(namematch) > 0) else ''
                version        = versionmatch[0] if (len(versionmatch) > 0) else ''
                repourl        = repourlmatch[0] if (len(repourlmatch) > 0) else ''
                dataurl        = dataurlmatch[0] if (len(dataurlmatch) > 0) else ''
                zipurl         = zipurlmatch[0] if (len(zipurlmatch) > 0) else ''
                repoid         = repoidmatch[0] if (len(repoidmatch) > 0) else ''
                dependencyname = xbmc.translatePath(os.path.join(packages,depname+'.zip'))

                dp.create('Downloading Dependencies','Installing [COLOR=yellow]'+depname,'','')
                
                try:
                    downloader.download(repourl, dependencyname, dp)
                    extract.all(dependencyname, ADDONS, dp)
                
                except:
                    
                    try:
                        downloader.download(zipurl, dependencyname, dp)
                        extract.all(dependencyname, ADDONS, dp)
                    
                    except:
                        
                        try:
                            
                            if not os.path.exists(dependencypath):
                                os.makedirs(dependencypath)
                            
                            link = Open_URL(dataurl, 10).replace('\n','').replace('\r','')
                            match=re.compile('href="(.+?)"', re.DOTALL).findall(link)
                            
                            for href in match:
                                filepath=xbmc.translatePath(os.path.join(dependencypath,href))
                                
                                if addon_id not in href and '/' not in href:
                                    
                                    try:
                                        dp.update(0,'','Downloading [COLOR=yellow]'+href+'[/COLOR]','Please wait...')
                                        downloader.download(dataurl+href, filepath, dp)
                                    
                                    except:
                                        print"failed to install"+href
                                
                                if '/' in href and '..' not in href and 'http' not in href:
                                    remote_path = dataurl+href
                                    Recursive_Loop(filepath,remote_path)
                        
                        except:
                            dialog.ok("Error downloading dependency", 'There was an error downloading [COLOR=dodgerblue]'+depname+'[/COLOR]. Please consider updating the add-on portal with details or report the error on the forum at WWW.NOOBSANDNERDS.COM')
                            status=0
                            modulestatus=0
                
                if status==1:
                    time.sleep(1)
                    dp.update(0,"[COLOR=yellow]"+depname+'[/COLOR]  [COLOR=lime]Successfully Installed[/COLOR]','','Please wait...')
                    time.sleep(1)
                    incremental = 'http://noobsandnerds.com/TI/AddonPortal/downloadcount.php?id=%s' % (requires)
                    try:
                        Open_URL(incremental, 5)
                    except:
                        pass
    dp.close()
    time.sleep(1)
#---------------------------------------------------------------------------------------------------
# Show full description of build
def Description(name,url,buildname,author,version,description,updated,skins,videoaddons,audioaddons,programaddons,pictureaddons,sources,adult):
    Text_Boxes(buildname+'     v.'+version, '[COLOR=yellow][B]Author:   [/B][/COLOR]'+author+'[COLOR=yellow][B]               Last Updated:   [/B][/COLOR]'+updated+'[COLOR=yellow][B]               Adult Content:   [/B][/COLOR]'+adult+'[CR][CR][COLOR=yellow][B]Description:[CR][/B][/COLOR]'+description+
    '[CR][CR][COLOR=blue][B]Skins:   [/B][/COLOR]'+skins+'[CR][CR][COLOR=blue][B]Video Addons:   [/B][/COLOR]'+videoaddons+'[CR][CR][COLOR=blue][B]Audio Addons:   [/B][/COLOR]'+audioaddons+
    '[CR][CR][COLOR=blue][B]Program Addons:   [/B][/COLOR]'+programaddons+'[CR][CR][COLOR=blue][B]Picture Addons:   [/B][/COLOR]'+pictureaddons+'[CR][CR][COLOR=blue][B]Sources:   [/B][/COLOR]'+sources+
    '[CR][CR][COLOR=orange]Disclaimer: [/COLOR]These are community builds and they may overwrite some of your existing settings, '
    'It\'s purely the responsibility of the user to choose whether or not they wish to install these builds, the individual who uploads the build should state what\'s included and then it\'s the users decision to decide whether or not that content is suitable for them.')
#---------------------------------------------------------------------------------------------------
# Function to do a full wipe.
def Destroy_Path(path):
    dp.create("Cleaning Folders","Wiping...",'', 'Please Wait')
    shutil.rmtree(path, ignore_errors=True)
#-----------------------------------------------------------------------------------------------------------------
# Addon Enable/Disable menu
def Enable_Addons():
    addDir('', "[I][B][COLOR red]!!Notice: Disabling Some Addons Can Cause Issues!![/COLOR][/B][/I]", '', '', 'mainmenu/maintenance.png', '', '', '')
    fold = glob.glob(os.path.join(ADDONS, '*/'))
    for folder in sorted(fold, key = lambda x: x):
        if AddonID in folder: continue
        addonxml = os.path.join(folder, 'addon.xml')
        if os.path.exists(addonxml):
            fold   = folder.replace(ADDONS, '')[1:-1]
            f      = open(addonxml)
            a      = f.read().replace('\n','').replace('\r','').replace('\t','')
            match  = re.compile('<addo.+?id="(.+?)".+?>').findall(a)
            match2 = re.compile('<addo.+? name="(.+?)".+?>').findall(a)
            try:
                pluginid = match[0]
                name = match2[0]
            except:
                continue
            try:
                add    = xbmcaddon.Addon(id=pluginid)
                state  = "[COLOR green][Enabled][/COLOR]"
                goto   = "false"
            except:
                state  = "[COLOR red][Disabled][/COLOR]"
                goto   = "true"
                pass
            icon   = os.path.join(folder, 'icon.png') if os.path.exists(os.path.join(folder, 'icon.png')) else ICON
            fanart = os.path.join(folder, 'fanart.jpg') if os.path.exists(os.path.join(folder, 'fanart.jpg')) else FANART
            addDir('addon', "%s %s" % (state, name), "%s[]%s" % (fold, goto), 'toggleaddon', icon, fanart, '', '')
            f.close()
#---------------------------------------------------------------------------------------------------
def Finish_Local_Restore():
    os.remove(idfile)
    os.rename(idfiletemp,idfile)
    xbmc.executebuiltin('UnloadSkin')    
    xbmc.executebuiltin("ReloadSkin")
    dialog.ok("Local Restore Complete", 'XBMC/Kodi will now close.', '', '')
    xbmc.executebuiltin("Quit")      
#---------------------------------------------------------------------------------------------------
# Convert physical paths to special paths
def Fix_Special(url):
    dp.create("Changing Physical Paths To Special","Renaming paths...",'', 'Please Wait')
    for root, dirs, files in os.walk(url):  #Search all xml files and replace physical with special
        for file in files:
            if file.endswith(".xml") or file.endswith(".hash") or file.endswith("properies"):
                dp.update(0,"Fixing",file, 'Please Wait')
                a = open((os.path.join(root, file))).read()
                encodedpath  = urllib.quote(HOME)
                encodedpath2  = urllib.quote(HOME).replace('%3A','%3a').replace('%5C','%5c')
                b = a.replace(HOME, 'special://home/').replace(encodedpath, 'special://home/').replace(encodedpath2, 'special://home/')
                f = open((os.path.join(root, file)), mode='w')
                f.write(str(b))
                f.close()
#---------------------------------------------------------------------------------------------------
# Call the full backup option
def Full_Backup():
    if os.path.exists(addonstemp):
        shutil.rmtree(addonstemp)
    exclude_dirs_full  =  []
    exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf','.gitignore']
    message_header     = "Creating full backup of existing build"
    message_header2    = "Creating Community Build"
    message1           = "Archiving..."
    message2           = ""
    message3           = "Please Wait"
    
    Archive_Tree(HOME, myfullbackup, message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)
#---------------------------------------------------------------------------------------------------
def Full_Clean():
    size                      = 0
    atv2_cache_a              = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
    atv2_cache_b              = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Localuseraccountnamental')        
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
    dp.create('Calculating Used Space','','Please wait','')

# For more accurate info we need to add a loop to only check folders with cache in the name. Actual wipe does this but getsize does not.
    if os.path.exists(atv2_cache_a):
        size = Get_Size(atv2_cache_a,size)
    if os.path.exists(atv2_cache_b):
        size = Get_Size(atv2_cache_b,size)
    if os.path.exists(downloader_cache_path):
        size = Get_Size(downloader_cache_path,size)
    if os.path.exists(imageslideshow_cache_path):
        size = Get_Size(imageslideshow_cache_path,size)
    if os.path.exists(iplayer_cache_path):
        size = Get_Size(iplayer_cache_path,size)
    if os.path.exists(itv_cache_path):
        size = Get_Size(itv_cache_path,size)
    if os.path.exists(navix_cache_path):
        size = Get_Size(navix_cache_path,size)
    if os.path.exists(phoenix_cache_path):
        size = Get_Size(phoenix_cache_path,size)
    if os.path.exists(ramfm_cache_path):
        size = Get_Size(ramfm_cache_path,size)
    if os.path.exists(wtf_cache_path):
        size = Get_Size(wtf_cache_path,size)
    if os.path.exists(genesisCache):
        size = Get_Size(genesisCache,size)
    if os.path.exists(tempdir):
        size = Get_Size(tempdir,size)
    size = Get_Size(THUMBNAILS,size)
    size = Get_Size(packages,size)/1000000
    choice = dialog.yesno('Results','You can free up [COLOR=dodgerblue]'+str(size)+'MB[/COLOR] of space if you run this cleanup program. Would you like to run the cleanup procedure?')
    if choice == 1:
        Wipe_Cache()
        try:
            shutil.rmtree(packages)
        except:
            pass
        choice = dialog.yesno('Thumbnail Cleanup','We highly recommend only wiping your OLD unused thumbnails. Do you want to clear just the old ones or all thumbnails?',yeslabel='ALL',nolabel='OLD ONLY')
        if choice == 1:
            Remove_Textures()
            Destroy_Path(THUMBNAILS)
            Kill_XBMC()
        else:
            Cleanup_Old_Textures()
#---------------------------------------------------------------------------------------------------
#Build Genres Menu (First Filter)
def Genres(url):       
    addDir('folder','Anime',str(url)+'&genre=anime','grab_builds','','','','')
    addDir('folder','Audiobooks',str(url)+'&genre=audiobooks','grab_builds','','','','')
    addDir('folder','Comedy',str(url)+'&genre=comedy','grab_builds','','','','')
    addDir('folder','Comics',str(url)+'&genre=comics','grab_builds','','','','')
    addDir('folder','Documentary',str(url)+'&genre=documentary','grab_builds','','','','')
    addDir('folder','Downloads',str(url)+'&genre=downloads','grab_builds','','','','')
    addDir('folder','Food',str(url)+'&genre=food','grab_builds','','','','')
    addDir('folder','Gaming',str(url)+'&genre=gaming','grab_builds','','','','')
    addDir('folder','Health',str(url)+'&genre=health','grab_builds','','','','')
    addDir('folder','How To...',str(url)+'&genre=howto','grab_builds','','','','')
    addDir('folder','Kids',str(url)+'&genre=kids','grab_builds','','','','')
    addDir('folder','Live TV',str(url)+'&genre=livetv','grab_builds','','','','')
    addDir('folder','Movies',str(url)+'&genre=movies','grab_builds','','','','')
    addDir('folder','Music',str(url)+'&genre=music','grab_builds','','','','')
    addDir('folder','News',str(url)+'&genre=news','grab_builds','','','','')
    addDir('folder','Photos',str(url)+'&genre=photos','grab_builds','','','','')
    addDir('folder','Podcasts',str(url)+'&genre=podcasts','grab_builds','','','','')
    addDir('folder','Radio',str(url)+'&genre=radio','grab_builds','','','','')
    addDir('folder','Religion',str(url)+'&genre=religion','grab_builds','','','','')
    addDir('folder','Space',str(url)+'&genre=space','grab_builds','','','','')
    addDir('folder','Sports',str(url)+'&genre=sports','grab_builds','','','','')
    addDir('folder','Technology',str(url)+'&genre=tech','grab_builds','','','','')
    addDir('folder','Trailers',str(url)+'&genre=trailers','grab_builds','','','','')
    addDir('folder','TV Shows',str(url)+'&genre=tv','grab_builds','','','','')
    addDir('folder','Misc.',str(url)+'&genre=other','grab_builds','','','','')
    
    if ADDON.getSetting('adult') == 'true':
        addDir('folder','XXX',str(url)+'&genre=adult','grab_builds','','','','')
#---------------------------------------------------------------------------------------------------
# Send a path and an initial size to increment to and it will scan total file sizes of all subfolders
def Get_Size(path,size):
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            dp.update(0,"Calulating...",'[COLOR=dodgerblue]'+f+'[/COLOR]', 'Please Wait')
            fp = os.path.join(dirpath, f)
            size += os.path.getsize(fp)
    return size
#---------------------------------------------------------------------------------------------------
def Get_Keyboard( default="", heading="", hidden=False ):
    keyboard = xbmc.Keyboard( default, heading, hidden )
    keyboard.doModal()
    if ( keyboard.isConfirmed() ):
        return unicode( keyboard.getText(), "utf-8" )
    return default
#---------------------------------------------------------------------------------------------------
def Get_Last_Error():
    import traceback
 #   errorstring = traceback.format_exc()
    errorstring = traceback.print_exc()
    xbmc.log('### ERROR STRING: %s' % errorstring)
#---------------------------------------------------------------------------------------------------
# Send a path and an initial size to increment to and it will scan total file sizes of all subfolders
def Get_Size(path,size):
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            dp.update(0,"Calculating...",'[COLOR=dodgerblue]'+f+'[/COLOR]', 'Please Wait')
            fp = os.path.join(dirpath, f)
            size += os.path.getsize(fp)
    return size
#-----------------------------------------------------------------------------------------------------------------  
#Get params and clean up into string or integer
def Get_Params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param
#-----------------------------------------------------------------------------------------------------------------
def Gotham():
    path = xbmc.translatePath(os.path.join('special://home', 'addons'))
    dp   = xbmcgui.DialogProgress()
    dp.create("Gotham Addon Fix","Please wait whilst your addons",'', 'are being made Gotham compatible.')
    
    for infile in glob.glob(os.path.join(path, '*.*')):
        
        for file in glob.glob(os.path.join(infile, '*.*')):
            
            if 'addon.xml' in file:
                dp.update(0,"Fixing",file, 'Please Wait')
                a = open(file).read()
                b = a.replace('addon="xbmc.python" version="1.0"','addon="xbmc.python" version="2.1.0"').replace('addon="xbmc.python" version="2.0"','addon="xbmc.python" version="2.1.0"')
                f = open(file, mode='w')
                f.write(str(b))
                f.close()

    dialog = xbmcgui.Dialog()
    dialog.ok("Your addons have now been made compatible", "If you still find you have addons that aren't working please run the addon so it throws up a script error, upload a log and post details on the relevant support forum.")
#-----------------------------------------------------------------------------------------------------------------  
def Gotham_Confirm():
    if dialog.yesno('Convert Addons To Gotham', 'This will edit your addon.xml files so they show as Gotham compatible. It\'s doubtful this will have any effect on whether or not they work but it will get rid of the annoying incompatible pop-up message. Do you wish to continue?'):
        Gotham()
#---------------------------------------------------------------------------------------------------
# Grab contents of the log
def Grab_Log():
    finalfile = 0
    logfilepath = os.listdir(log_path)
    for item in logfilepath:
        if item.endswith('.log') and not item.endswith('.old.log'):
            mylog        = os.path.join(log_path,item)
            lastmodified = os.path.getmtime(mylog)
            if lastmodified>finalfile:
                finalfile = lastmodified
                logfile   = mylog
    
    filename    = open(logfile, 'r')
    logtext     = filename.read()
    filename.close()
    return logtext
#---------------------------------------------------------------------------------------------------
#Function to populate the search based on the initial first filter
def Grab_Addons(url):
    if ADDON.getSetting('adult') == 'true':
        adult = 'yes'
    
    else:
        adult = 'no'

    if url == 'popular':
        buildsURL  = 'http://noobsandnerds.com/TI/AddonPortal/popular_new.php?adult=%s' % (adult)
    elif url == 'latest':
        buildsURL  = 'http://noobsandnerds.com/TI/AddonPortal/latest_new.php?adult=%s' % (adult)
    elif url != 'popular' and url != 'latest':
        buildsURL  = 'http://noobsandnerds.com/TI/AddonPortal/sortby_new.php?sortx=name&user=%s&adult=%s&%s' % (username, adult, url)
        xbmc.log(buildsURL)
        if not "desc" in url:
            url = url+'&desc='
        if not "genre" in url:
            url = url+'&genre='
    print "URL: "+buildsURL

    link = Open_URL(buildsURL, 10).replace('\n','').replace('\r','')

# match without cloudflare enabled
    match      = re.compile('name="(.+?)"  <br> downloads="(.+?)"  <br> icon="(.+?)"  <br> broken="(.+?)"  <br> id="(.+?)"  <br> UID="(.+?)"  <br>', re.DOTALL).findall(link)
    if match == []:
# match with cloudflare enabled
        match  = re.compile('name="(.+?)" <br> downloads="(.+?)" <br> icon="(.+?)" <br> broken="(.+?)" <br> id="(.+?)" <br> UID="(.+?)" <br>', re.DOTALL).findall(link)
    
    if match !=[] and url != 'popular' and url != 'latest':
        Sort_By(buildsURL,'addons')
        
        for name,downloads,icon, broken,addonid,uid in match:
            try:
                xbmcaddon.Addon(id=addonid).getAddonInfo('path')
                install_text = '[COLOR=lime][INSTALLED][/COLOR] '
            except:
                install_text = ''
            
            if broken=='0':
                addDir('addonfolder',install_text+name+' ['+downloads+' downloads]',uid,'addon_final_menu',icon,'','')        
            
            if broken=='1':
                addDir('addonfolder',install_text+'[COLOR=red]'+name+' [REPORTED AS BROKEN][/COLOR]',uid,'addon_final_menu',icon,'','')        
    
    elif match !=[] and (url == 'popular' or url == 'latest'):
        for name,downloads,icon, broken,addonid,uid in match:
            try:
                xbmcaddon.Addon(id=addonid).getAddonInfo('path')
                install_text = '[COLOR=lime][INSTALLED][/COLOR] '
            except:
                install_text = ''
            
            if broken=='0':
                addDir('addonfolder',install_text+name+' ['+downloads+' downloads]',uid,'addon_final_menu',icon,'','')        
            
            if broken=='1':
                addDir('addonfolder',install_text+'[COLOR=red]'+name+' [REPORTED AS BROKEN][/COLOR]',uid,'addon_final_menu',icon,'','')        
        
    elif '&redirect' in url:
        choice=dialog.yesno('No Content Found','This add-on cannot be found on the Add-on Portal.','','Would you like to remove this item from your setup?')
        
        if choice == 1:
            print"### Need to add remove function to code still"
    
    else:
        dialog.ok('No Content Found','Sorry no content can be found that matches','your search criteria.','')
#-----------------------------------------------------------------------------------------------------------------
#Function to populate the search based on the initial first filter
def Grab_Builds(url):
    if zip == '':
        dialog.ok('Storage/Download Folder Not Set','You have not set your backup storage folder.\nPlease update the addon settings and try again.','','')
        ADDON.openSettings(sys.argv[0])
    
    if ADDON.getSetting('adult') == 'true':
        adult = ''
    
    else:
        adult = 'no'

    if 'genre' in url:
        buildsURL  = 'http://noobsandnerds.com/TI/Community_Builds/sort_by_test.php?sortx=name&orderx=ASC&adult=%s&%s' % (adult, url)
    else:
        buildsURL  = 'http://noobsandnerds.com/TI/Community_Builds/sort_by_test.php?sortx=name&orderx=ASC&genre=&adult=%s&%s' % (adult, url)
    if debug == 'true':
        xbmc.log("BUILD URL: %s" % buildsURL)
    link       = Open_URL(buildsURL, 10).replace('\n','').replace('\r','')
# match without cloudflare disabled
    match      = re.compile('name="(.+?)"  <br> id="(.+?)"  <br> Thumbnail="(.+?)"  <br> Fanart="(.+?)"  <br> downloads="(.+?)"  <br> <br>', re.DOTALL).findall(link)
    if match == []:
# match with cloudflare disabled
        match  = re.compile('name="(.+?)" <br> id="(.+?)" <br> Thumbnail="(.+?)" <br> Fanart="(.+?)" <br> downloads="(.+?)" <br> <br>', re.DOTALL).findall(link)
    if not '&visibility=private' in url:
        Sort_By(url,'communitybuilds')
    
    for name,id,Thumbnail,Fanart,downloads in match:
        Add_Build_Dir(name+'[COLOR=lime] ('+downloads+' downloads)[/COLOR]',id+url,'community_menu',Thumbnail,Fanart,id,'','','','')
    
    if 'id=1' in url: buildsURL = wizardurl1
    if 'id=2' in url: buildsURL = wizardurl2
    if 'id=3' in url: buildsURL = wizardurl3
    if 'id=4' in url: buildsURL = wizardurl4
    if 'id=5' in url: buildsURL = wizardurl5

    link       = Open_URL(buildsURL, 10).replace('\n','').replace('\r','')
    match      = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)

    for name,url,iconimage,fanart,description in match:
        if not 'viewport' in name:
            addDir('addon',name,url,'restore_local_CB',iconimage,fanart,description,'')
#---------------------------------------------------------------------------------------------------
# Check for the real log path, even makes exceptions for idiots who've left their old kodi logs in their builds
def Grab_Log(file=False, old=False):
    finalfile   = 0
    logfilepath = os.listdir(log_path)
    logsfound   = []

    for item in logfilepath:
        if old == True and item.endswith('.old.log'): logsfound.append(os.path.join(log_path, item))
        elif old == False and item.endswith('.log') and not item.endswith('.old.log'): logsfound.append(os.path.join(log_path, item))

    if len(logsfound) > 0:
        logsfound.sort(key=lambda f: os.path.getmtime(f))
        if file == True: return logsfound[-1]
        else:
            filename    = open(logsfound[-1], 'r')
            logtext     = filename.read()
            filename.close()
            return logtext
    else: 
        return False
#---------------------------------------------------------------------------------------------------
# Option to download guisettings fix that merges with existing settings.
def GUI_Settings_Fix(url,local):
    Check_Download_Path()
    choice = xbmcgui.Dialog().yesno(name, 'This will over-write your existing guisettings.xml.', 'Are you sure this is the build you have installed?', '', nolabel='No, Cancel',yeslabel='Yes, Fix')
    
    if choice == 1:
        GUI_Merge(url,local)
#---------------------------------------------------------------------------------------------------
def GUI_Install(path):
# Read the original skinsettings tags and store in memory ready to replace in guinew.xml
    localfile = open(GUI, mode='r')
    content   = localfile.read()
    localfile.close()

    skinsettingsorig  = re.compile('<skinsettings>[\s\S]*?<\/skinsettings>').findall(content)
    skindefault       = re.compile('<skin default[\s\S]*?<\/skin>').findall(content)
    lookandfeelorig   = re.compile('<lookandfeel>[\s\S]*?<\/lookandfeel>').findall(content)
    skinorig          = skinsettingsorig[0] if (len(skinsettingsorig) > 0) else ''
    skindefaultorig   = skindefault[0] if (len(skindefault) > 0) else ''
    lookandfeel       = lookandfeelorig[0] if (len(lookandfeelorig) > 0) else ''

# Read the new guisettings file and get replace skin related settings with original
    localfile2 = open(path, mode='r')
    content2   = localfile2.read()
    localfile2.close()

    skinsettingscontent = re.compile('<skinsettings>[\s\S]*?<\/skinsettings>').findall(content2)
    skindefaultcontent  = re.compile('<skin default[\s\S]*?<\/skin>').findall(content2)
    lookandfeelcontent  = re.compile('<lookandfeel>[\s\S]*?<\/lookandfeel>').findall(content2)
    skinsettingstext    = skinsettingscontent[0] if (len(skinsettingscontent) > 0) else ''
    skindefaulttext     = skindefaultcontent[0] if (len(skindefaultcontent) > 0) else ''
    lookandfeeltext     = lookandfeelcontent[0] if (len(lookandfeelcontent) > 0) else ''
    replacefile         = content.replace(skinorig,skinsettingstext).replace(lookandfeel,lookandfeeltext).replace(skindefaultorig,skindefaulttext)

    print "### Attempting to create new guisettings at: "+path
    writefile = open(path, mode='w+')
    writefile.write(str(replacefile))
    writefile.close()
#---------------------------------------------------------------------------------------------------
# Function to download guisettings.xml and merge with existing.
def GUI_Merge(url,local):
    success           = False
    profiles_included = 0
    keep_profiles     = 1
    
    if os.path.exists(GUINEW):
        os.remove(GUINEW)
    
    if os.path.exists(GUIFIX):
        os.remove(GUIFIX)
    
    if os.path.exists(PROFILES):
        os.remove(PROFILES)
    
    if not os.path.exists(guitemp):
        os.makedirs(guitemp)

# Rename guisettings.xml to guinew.xml so we can edit without XBMC interfering.
    try:
        shutil.copyfile(GUI,GUINEW)
    
    except:
        print"No guisettings found, most likely due to a previously failed attempt at install"
    
    if local!=1:
        lib=os.path.join(USB, 'guifix.zip')
    
        try:
            dp.create('Downloading Skin Fix','','','')
            downloader.download(url,lib)
        except:
            print"Failed to download guisettings"
    else:
        lib=xbmc.translatePath(url)
    if debug == 'true':
        print"### lib="+lib
# Get the size of the downloaded guisettings so we can later add to the id.xml
    guisize=str(os.path.getsize(lib))
    dp.create("Installing Skin Fix","Checking ",'', 'Please Wait')
#    dp.update(0,"", "Extracting Zip Please Wait")
    extract.all(lib,guitemp)

    if os.path.exists(os.path.join(guitemp,'script.skinshortcuts')):
        try:
            shutil.rmtree(os.path.join(ADDON_DATA,'script.skinshortcuts'))
        except:
            pass
        os.rename(os.path.join(guitemp,'script.skinshortcuts'),os.path.join(ADDON_DATA,'script.skinshortcuts'))
        
    if os.path.exists(os.path.join(guitemp,'addon_data')):
       Move_Tree(os.path.join(guitemp,'addon_data'), USERDATA,1)

    if local != 'library' or local != 'updatelibrary' or local !='fresh':
        
        try:
            readfile = open(os.path.join(guitemp,'profiles.xml'), mode='r')
            default_contents = readfile.read()
            readfile.close()
            
            if os.path.exists(os.path.join(guitemp,'profiles.xml')):
                
                if local == None:
                    choice = xbmcgui.Dialog().yesno("KODI PROFILES DETECTED", 'This build has profiles included (standard Kodi profiles, not CP Profiles), would you like to overwrite your existing profiles or keep the ones you have?', '','', nolabel='Keep my profiles',yeslabel='Use new profiles')
                
                if local != None:
                    choice = 1
                
                if choice == 1:
                    writefile = open(PROFILES, mode='w')
                    time.sleep(1)
                    writefile.write(default_contents)
                    time.sleep(1)
                    writefile.close()
                    keep_profiles=0
        
        except:
            print"no profiles.xml file"

#Copy to addon_data folder so profiles can be dealt with
    try:
        os.rename(os.path.join(guitemp,'guisettings.xml'),GUIFIX)
    except:
        dialog.ok('FILE MISSING','No guisettings.xml could be found in your zip file. Please double check this file is a valid zip and hasn\'t become corrupt.')
    if local != 'fresh':
        choice2 = dialog.yesno("Keep Kodi Settings?", 'Do you want to keep your existing KODI settings (weather, screen calibration, PVR etc.) or wipe and install the ones in this build?', nolabel='Keep my settings',yeslabel='Replace my settings')
    
    if local == 'fresh':
        choice2 = 1
    
    if choice2 == 1:
        
        if os.path.exists(GUI):
            
            try:
                print"### Attempting to remove guisettings"
                os.remove(GUI)
                success=True
            
            except:
                print"### Problem removing guisettings"
                success=False
            
            try:
                print"### Attempting to replace guisettings with new"
                os.rename(GUIFIX,GUI)
                success=True
            
            except:
                print"### Failed to replace guisettings with new"
                success=False
    
# Read the original skinsettings tags and store in memory ready to replace in guinew.xml
    if choice2 == 0:
        localfile = open(GUINEW, mode='r')
        content   = localfile.read()
        localfile.close()

        skinsettingsorig  = re.compile('<skinsettings>[\s\S]*?<\/skinsettings>').findall(content)
        skindefault       = re.compile('<skin default[\s\S]*?<\/skin>').findall(content)
        lookandfeelorig   = re.compile('<lookandfeel>[\s\S]*?<\/lookandfeel>').findall(content)
        skinorig          = skinsettingsorig[0] if (len(skinsettingsorig) > 0) else ''
        skindefaultorig   = skindefault[0] if (len(skindefault) > 0) else ''
        lookandfeel       = lookandfeelorig[0] if (len(lookandfeelorig) > 0) else ''

# Read the new guisettings file and get replace skin related settings with original
        localfile2 = open(GUIFIX, mode='r')
        content2   = localfile2.read()
        localfile2.close()

        skinsettingscontent = re.compile('<skinsettings>[\s\S]*?<\/skinsettings>').findall(content2)
        skindefaultcontent  = re.compile('<skin default[\s\S]*?<\/skin>').findall(content2)
        lookandfeelcontent  = re.compile('<lookandfeel>[\s\S]*?<\/lookandfeel>').findall(content2)
        skinsettingstext    = skinsettingscontent[0] if (len(skinsettingscontent) > 0) else ''
        skindefaulttext     = skindefaultcontent[0] if (len(skindefaultcontent) > 0) else ''
        lookandfeeltext     = lookandfeelcontent[0] if (len(lookandfeelcontent) > 0) else ''
        replacefile         = content.replace(skinorig,skinsettingstext).replace(lookandfeel,lookandfeeltext).replace(skindefaultorig,skindefaulttext)

        writefile = open(GUINEW, mode='w+')
        writefile.write(str(replacefile))
        writefile.close()

# Replace guisettings with the new ones, check in place to make sure Kodi hasn't recreated them again
        if os.path.exists(GUI):
            
            try:
                os.remove(GUI)
                success=True
            
            except:
                success=False
        
        try:
            os.rename(GUINEW,GUI)
            os.remove(GUIFIX)
            success=True
        
        except:
            success=False
 
# If the guisettings were successfully installed and it's not a local install update the details for id.xml and startup.xml
    if success==True or local == None:
        
        try:
            localfile = open(tempfile, mode='r')
            content   = localfile.read()
            localfile.close()
            
            temp         = re.compile('id="(.+?)"').findall(content)
            tempname     = re.compile('name="(.+?)"').findall(content)
            tempversion  = re.compile('version="(.+?)"').findall(content)
            tempcheck    = temp[0] if (len(temp) > 0) else ''
            namecheck    = tempname[0] if (len(tempname) > 0) else ''
            versioncheck = tempversion[0] if (len(tempversion) > 0) else ''

            writefile = open(idfile, mode='w+')
            writefile.write('id="'+str(tempcheck)+'"\nname="'+namecheck+'"\nversion="'+versioncheck+'"\ngui="'+guisize+'"')
            writefile.close()

            localfile = open(startuppath, mode='r')
            content = localfile.read()
            localfile.close()

            localversionmatch  = re.compile('version="(.+?)"').findall(content)
            localversioncheck  = localversionmatch[0] if (len(localversionmatch) > 0) else ''
            replacefile        = content.replace(localversioncheck,versioncheck)

            writefile = open(startuppath, mode='w')
            writefile.write(str(replacefile))
            writefile.close()
            os.remove(tempfile)
        
        except:
            writefile = open(idfile, mode='w+')
            writefile.write('id="None"\nname="Unknown"\nversion="Unknown"\ngui="'+guisize+'"')
            writefile.close()                

# Clean up the temporary files
    if os.path.exists(os.path.join(guitemp,'profiles.xml')):
        os.remove(os.path.join(guitemp,'profiles.xml'))
        time.sleep(1)
    
    if os.path.exists(guitemp):
        os.removedirs(guitemp)
    
    notifypath = xbmc.translatePath(os.path.join(ADDON_DATA,AddonID,'notification.txt'))
    
    if os.path.exists(notifypath):
        os.remove(notifypath)
    
    if success == True:
        Remove_Textures()
        Kill_XBMC()
#-----------------------------------------------------------------------------------------------------------------
#Fix the blank on-screen keyboard when using Gotham skins on Helix.
#BIG THANKS TO MIKEY1234 FOR THIS SECTION OF CODE, IT HAS BEEN TAKEN FROM THE XUNITY MAINTENANCE ADDON.
def Helix():
    skin = xbmc.getSkinDir()
    path = xbmc.translatePath(os.path.join(ADDONS, skin))
    
    for root, dirs, files in os.walk(path):
       
       for f in files:
            
            if 'DialogKeyboard.xml' in f:
                skin   = os.path.join(root, f)
                a      = open(skin).read()
                CHANGE = a.replace('<control type="label" id="310"','<control type="edit" id="312"')
                f      = open(skin, mode='w')
                f.write(CHANGE)
                f.close()     
                changekeys(skin)
                
                for i in range(48, 58):
                    changenumber(i,skin)
    
    dialog = xbmcgui.Dialog()
    dialog.ok("Skin Changes Successful", 'A BIG thank you to Mikey1234 for this fix. The code used for this function was ported from the Xunity Maintenance add-on')
    xbmc.executebuiltin('ReloadSkin()')   
#---------------------------------------------------------------------------------------------------
def Helix_Confirm():
    if dialog.yesno('Convert This Skin To Kodi (Helix)?', 'This will fix the problem with a blank on-screen keyboard showing in skins designed for Gotham (being run on Kodi). This will only affect the currently running skin.', nolabel='No, Cancel',yeslabel='Yes, Fix'):
        Helix()
#-----------------------------------------------------------------------------------------------------------------          
#Hide passwords in addon settings - THANKS TO MIKEY1234 FOR THIS CODE (taken from Xunity Maintenance)
def Hide_Passwords():
    if dialog.yesno("Hide Passwords", "This will hide all your passwords in your", "add-on settings, are you sure you wish to continue?"):
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
        dialog.ok("Passwords Hidden", "Your passwords will now show as stars (hidden), if you want to undo this please use the option to unhide passwords.") 
#---------------------------------------------------------------------------------------------------
# Function to download guisettings.xml and merge with existing.
def INSTALL_PART2(url):
    BaseURL          = 'http://noobsandnerds.com/TI/Community_Builds/guisettings.php?id=%s' % (url)
    link             = Open_URL(BaseURL, 10).replace('\n','').replace('\r','')
    guisettingsmatch = re.compile('guisettings="(.+?)"').findall(link)
    guisettingslink  = guisettingsmatch[0] if (len(guisettingsmatch) > 0) else 'None'
    
    GUI_Merge(guisettingslink,local)
#---------------------------------------------------------------------------------------------------
# Browse pre-installed repo's via the kodi add-on browser
def Install_From_Zip():
    xbmc.executebuiltin('ActivateWindow(10040,"addons://install/",return)')
#---------------------------------------------------------------------------------------------------
# Step 2 of the addon install process (installs the repo if one exists)
def Install_Repo(repo_id):
    repostatus   = 1
    BaseURL      = 'http://noobsandnerds.com/TI/AddonPortal/dependencyinstall.php?id=%s' % (repo_id)
    xbmc.log("Install Repo: %s"%BaseURL)
    link         = Open_URL(BaseURL, 10).replace('\n','').replace('\r','')
    namematch    = re.compile('name="(.+?)"').findall(link)
    versionmatch = re.compile('version="(.+?)"').findall(link)
    repourlmatch = re.compile('repo_url="(.+?)"').findall(link)
    dataurlmatch = re.compile('data_url="(.+?)"').findall(link)
    zipurlmatch  = re.compile('zip_url="(.+?)"').findall(link)
    repoidmatch  = re.compile('repo_id="(.+?)"').findall(link)  
    reponame     = namematch[0] if (len(namematch) > 0) else ''
    version      = versionmatch[0] if (len(versionmatch) > 0) else ''
    repourl      = repourlmatch[0] if (len(repourlmatch) > 0) else ''
    dataurl      = dataurlmatch[0] if (len(dataurlmatch) > 0) else ''
    zipurl       = zipurlmatch[0] if (len(zipurlmatch) > 0) else ''
    repoid       = repoidmatch[0] if (len(repoidmatch) > 0) else ''
    repozipname  = xbmc.translatePath(os.path.join(packages,repoid+'.zip')) 
    repolocation = xbmc.translatePath(os.path.join(ADDONS,repoid))

    dp.create('Installing Repository','Please wait...','')
    
    try:
        downloadpath = 'https://github.com/noobsandnerds/noobsandnerds/blob/master/zips/%s/%s-0.0.0.1.zip?raw=true' % (repo_id, repo_id)
        downloader.download(downloadpath, repozipname, dp)
        xbmc.log('Download URL: %s' % downloadpath)
        extract.all(repozipname, ADDONS, dp)
    except:
        try:
            downloader.download(repourl, repozipname, dp)
            extract.all(repozipname, ADDONS, dp)
        except:
            try:
                downloader.download(zipurl, repozipname, dp)
                extract.all(repozipname, ADDONS, dp)
            except:
                try: 
                    if not os.path.exists(repolocation):
                        os.makedirs(repolocation)
                    
                    link = Open_URL(dataurl, 10).replace('\n','').replace('\r','')
                    match=re.compile('href="(.+?)"', re.DOTALL).findall(link)
                    
                    for href in match:
                        filepath=xbmc.translatePath(os.path.join(repolocation,href))
                        
                        if addon_id not in href and '/' not in href:
                            
                            try:
                                dp.update(0,"Downloading [COLOR=yellow]"+href+'[/COLOR]','','Please wait...')
                                downloader.download(dataurl+href, filepath, dp)
                            
                            except:
                                print"failed to install"+href
                        
                        if '/' in href and '..' not in href and 'http' not in href:
                            remote_path = dataurl+href
                            Recursive_Loop(filepath,remote_path)
                
                except:
                    dialog.ok("Error downloading repository", 'There was an error downloading[CR][COLOR=dodgerblue]'+reponame+'[/COLOR]. Please consider updating the add-on portal with details or report the error on the forum at WWW.NOOBSANDNERDS.COM')
                    repostatus=0
    
# If repository successfully installed add increment
    if repostatus==1:
        Update_Repo(showdialog = False)
        xbmc.sleep(1000)
        query = '{"jsonrpc":"2.0", "method":"Addons.SetAddonEnabled","params":{"addonid":"%s","enabled":true}}' % repo_id
        response = xbmc.executeJSONRPC(query)
        xbmc.log(str(query))
        xbmc.log(str(response))
        xbmc.log('### repo install was good')
        dp.update(0,"[COLOR=yellow]"+reponame+'[/COLOR]  [COLOR=lime]Successfully Installed[/COLOR]','','Now installing dependencies')
        dp.close()
        incremental = 'http://noobsandnerds.com/TI/AddonPortal/downloadcount.php?id=%s' % (repo_id)
        try:
            Open_URL(incremental, 5)
        except:
            pass
        return True
    else:
        xbmc.log('### repo install failed returning false')
        return False
#---------------------------------------------------------------------------------------------------
# (Instructions) Create a community backup
def Instructions_1():
    Text_Boxes('Creating A Backup To Share', 
    '[COLOR=gold]THE OPTIONS:[/COLOR][CR]There are 3 options when choosing to create a backup, we shall explain here the differences between them:[CR][CR]'
    '[COLOR=dodgerblue]1. noobsandnerds Community Build[/COLOR] - This is by far the best way to create a build that you want to share with others, it will create a zip file for you to share that can only be used on with this add-on. The size of the zip will be incredibly small compared to other backup options out there and it will also do lots of other clever stuff too such as error checking against the Addon Portal and the addons will always be updated via the relevant developer repositories. Added to this when it comes to updating it\'s a breeze, only the new addons not already on the system will be installed and for the majority of builds Kodi won\'t even have to restart after installing![CR][CR]'
    '[COLOR=dodgerblue]2. Universal Build[/COLOR] - This was the original method created by TotalXBMC, we would really only recommend this if for some strange reason you want your build available on other inferior wizards. The zip size is much larger and every time someone wants to update their build they have to download and install the whole thing again which can be very frustrating and time consuming. The whole build is backed up in full with the exception of the packages and thumbnails folder. Just like the option above all physical paths (so long as they exist somewhere in the Kodi environment) will be changed to special paths so they work on all devices.[CR][CR]'
    '[COLOR=dodgerblue]3. Full Backup[/COLOR] - It\'s highly unlikely you will ever want to use this option and it\'s more for the geeks out there. It will create a complete backup of your setup and not do any extra clever stuff. Things like packages will remain intact as will temp cache files, be warned the size could be VERY large![CR][CR]'
    '[CR][COLOR=gold]CREATING A COMMUNITY BUILD:[/COLOR][CR][CR][COLOR=blue][B]Step 1:[/COLOR] Remove any sensitive data[/B][CR]Make sure you\'ve removed any sensitive data such as passwords and usernames in your addon_data folder.'
    '[CR][CR][COLOR=dodgerblue][B]Step 2:[/COLOR] Backup your system[/B][CR]Choose the backup option you want from the list on the previous page, if you\'re sharing this via the CP Addon then please use the noobsandnerds backup option, this will create two zip files that you need to upload to a server.'
    '[CR][CR][COLOR=dodgerblue][B]Step 3:[/COLOR] Upload the zips[/B][CR]Upload the two zip files to a server that Kodi can access, it has to be a direct link and not somewhere that asks for captcha - archive.org and copy.com are two good examples. Do not use Dropbox unless you have a paid account, they have a fair useage policy and the chances are you\'ll find within 24 hours your download has been blocked and nobody can download it. [COLOR=lime]Top Tip: [/COLOR]The vast majority of problems occur when the wrong download URL has been entered in the online form, a good download URL normally ends in "=1" or "zip=true". Please double check when you copy the URL into a web browser it immediately starts downloading without the need to press any other button.'
    '[CR][CR][COLOR=dodgerblue][B]Step 4:[/COLOR] Submit the build[/B]'
    '[CR]Create a thread on the Community Builds section of the forum at [COLOR=orange]www.noobs[/COLOR][COLOR=dodgerblue]and[/COLOR][COLOR=orange]nerds.com[/COLOR].[CR]Full details can be found on there of the template you should use when posting, once you\'ve created your support thread (NOT BEFORE) you can request to become a member of the Community Builder group and you\'ll then be able to add your build via the web form. As soon as you\'ve successfully added the details your build will be live, if you can\'t find it in the CP addon make sure you have XXX enabled (if you marked it as having adult content) and also make sure you\'re running the same version of Kodi that you said it was compatible with. If you\'re running another version then you can select the option to "show all community builds" in the addon settings and that will show even the builds that aren\'t marked as compatible with your version of Kodi.'
    '[CR][CR][COLOR=gold]PRIVATE BUILDS[/COLOR][CR]If you aren\'t interested in sharing your build with the community you can still use our system for private builds. Just follow the instructions above but you will not need to create a support thread and you WILL require a minimum of 5 useful (not spam) posts on the forum. The 5 post rule only applies to users that wish to use the private builds option. Once you have 5 posts you\'ll be able to access the web form and in there you can enter up to 3 IP addresses that you want to be able to view your build(s). Anybody caught disobeying the forum rules will be banned so please make sure you understand the forum rules before posting, we welcome everyone but there is strictly no spamming or nonsense posts just saying something like "Thanks" in order to bump up your post count. The site rules even have examples of how you can get to 5 posts without receiving a ban.')
#---------------------------------------------------------------------------------------------------
# (Instructions) Install a community build   
def Instructions_2():
    Text_Boxes('Installing a build', '[COLOR=dodgerblue][B]Step 1 (Optional):[/COLOR] Backup your system[/B][CR]When selecting an install option you\'ll be asked if you want to create a backup - we strongly recommend creating a backup of your system in case you don\'t like the build and want to revert back. Remember your backup may be quite large so if you\'re using a device with a very small amount of storage we recommend using a USB stick or SD card as the storage location otherwise you may run out of space and the install may fail.'
    '[CR][CR][COLOR=dodgerblue][B]Step 2:[/COLOR] Choose an install method:[/B][CR][CR]-------------------------------------------------------[CR][CR][COLOR=gold]1. Overwrite my current setup & install new build:[/COLOR] This copy over the whole build[CR]As the title suggests this will overwrite your existing setup with the one created by the community builder. We recommend using the wipe option in the maintenance section before running this, that will completely wipe your existing settings and will ensure you don\'t have any conflicting data left on the device. Once you\'ve wiped please restart Kodi and install the build, you can of course use this install option 1 without wiping but you may encounter problems. If you choose to do this DO NOT bombard the community builder with questions on how to fix certain things, they will expect you to have installed over a clean setup and if you\'ve installed over another build the responsibility for bug tracking lies solely with you!'
    '[CR][CR]-------------------------------------------------------[CR][CR][COLOR=gold]2. Install:[/COLOR] Keep my library & profiles[CR]This will install a build over the top of your existing setup so you won\'t lose anything already installed in Kodi. Your library and any profiles you may have setup will also remain unchanged.'
    '[CR][CR]-------------------------------------------------------[CR][CR][COLOR=gold]3. Install:[/COLOR] Keep my library only[CR]This will do exactly the same as number 2 (above) but it will delete any profiles you may have and replace them with the ones the build author has created.'
    '[CR][CR]-------------------------------------------------------[CR][CR][COLOR=gold]4. Install:[/COLOR] Keep my profiles only[CR]Again, the same as number 2 but your library will be replaced with the one created by the build author. If you\'ve spent a long time setting up your library and have it just how you want it then use this with caution and make sure you do a backup!'
    '[CR][CR]-------------------------------------------------------[CR][CR][COLOR=dodgerblue][B]Step 3:[/COLOR] Replace or keep settings?[/B][CR]When completing the install process you\'ll be asked if you want to keep your existing Kodi settings or replace with the ones in the build. If you choose to keep your settings then only the important skin related settings are copied over from the build. All your other Kodi settings such as screen calibration, region, audio output, resolution etc. will remain intact. Choosing to replace your settings could possibly cause a few issues, unless the build author has specifically recommended you replace the settings with theirs we would always recommend keeping your own.'
    '[CR][CR][COLOR=dodgerblue][B]Step 4: [/COLOR][COLOR=red]VERY IMPORTANT[/COLOR][/B][CR]For the install to complete properly Kodi MUST force close, this means forcing it to close via your operating system rather than elegantly via the Kodi menu. By default this add-on will attempt to make your operating system force close Kodi but there are systems that will not allow this (devices that do not allow Kodi to have root permissions).'
    ' Once the final step of the install process has been completed you\'ll see a dialog explaining Kodi is attempting a force close, please be patient and give it a minute. If after a minute Kodi hasn\'t closed or restarted you will need to manually force close. The recommended solution for force closing is to go into your operating system menu and make it force close the Kodi app but if you dont\'t know how to do that you can just pull the power from the unit.'
    ' Pulling the power is fairly safe these days, on most set top boxes it\'s the only way to switch them off - they rarely have a power switch. Even though it\'s considered fairly safe nowadays you do this at your own risk and we would always recommend force closing via the operating system menu.')
#---------------------------------------------------------------------------------------------------
# (Instructions) What is a keyword
def Instructions_3():
    Text_Boxes('What is a noobsandnerds keyword?', '[COLOR=gold]WHAT IS A KEYWORD?[/COLOR][CR]The noobsandnerds keywords are based on the ingenious TLBB keyword system that was introduced years ago. It\'s nothing new and unlike certain other people out there we\'re not going to claim it as our idea. If you\'re already familiar with TLBB Keywords or even some of the copies out there like Cloudwords you will already know how this works but for those of you that don\'t have one of those devices we\'ll just go through the details...'
    '[CR][CR]Anyone in the community can make their own keywords and share them with others, it\'s a simple word you type in and then the content you uploaded to the web is downloaded and installed. Previously keywords have mostly been used for addon packs, this is a great way to get whole packs of addons in one go without the need to install a whole new build. We are taking this to the next level and will be introducing artwork packs and also addon fixes. More details will be available in the Community Portal section of the forum on www.noobsandnerds.com'
    '[CR][CR][CR][COLOR=gold]HOW DO I FIND A KEYWORD?[/COLOR][CR]The full list of noobsandnerds keywords can be found on the forum, in the Community Portal section you\'ll see a section for the keywords at the top of the page. Just find the pack you would like to install then using this addon type the keyword in when prompted (after clicking "Install a noobsandnerds keyword"). Your content will now be installed, if installing addon packs please be patient while each addon updates to the latest version directly from the developers repo.'
    '[CR][CR][CR][COLOR=gold]CAN I USE OTHER KEYWORDS?[/COLOR] (Cloudwords, TLBB etc.)[CR]Yes you can, just go to the addon settings and enter the url shortener that particular company use. Again you will find full details of supported keywords on the forum.')
#---------------------------------------------------------------------------------------------------
# (Instructions) How to create a keyword
def Instructions_4():
    Text_Boxes('How to create a keyword?', '[COLOR=gold]NaN MAKE IT EASY![/COLOR][CR]The keywords can now be made very simply by anyone. We\'ve not locked this down to just our addon and others can use this on similar systems for creating keywords if they want...'
    '[CR][CR][COLOR=dodgerblue][B]Step 1:[/COLOR] Use a vanilla Kodi setup[/B][CR]You will require a complete fresh install of Kodi with absolutely nothing else installed and running the default skin. Decide what kind of pack you want to create, lets say we want to create a kids pack... Add all the kid related addons you want and make sure you also have the relevant repository installed too. In the unlikely event you\'ve found an addon that doesn\'t belong in a repository that\'s fine the system will create a full backup of that addon too (just means it won\'t auto update with future updates to the addon).'
    '[CR][CR][COLOR=dodgerblue][B]Step 2:[/COLOR] Create the backup[/B][CR]Using this addon create your backup, currently only addon packs are supported but soon more packs will be added. When you create the keyword you\'ll be asked for a location to store the zip file that will be created and a name, this can be anywhwere you like and can be called whatever you want - you do not need to add the zip extension, that will automatically be added for you so in our example here we would call it "kids".'
    '[CR][CR][COLOR=dodgerblue][B]Step 3:[/COLOR] Upload the zips[/B][CR]Upload the two zip file to a server that Kodi can access, it has to be a direct link and not somewhere that asks for captcha - archive.org and copy.com are two good examples. Do not use Dropbox unless you have a paid account, they have a fair useage policy and the chances are you\'ll find within 24 hours your download has been blocked and nobody can download it.[CR][CR][COLOR=lime]Top Tip: [/COLOR]The vast majority of problems occur when the wrong download URL has been entered in the online form, a good download URL normally ends in "=1" or "zip=true". Please double check when you copy the URL into a web browser it immediately starts downloading without the need to press any other button.'
    '[CR][CR][COLOR=dodgerblue][B]Step 4:[/COLOR] Create the keyword[/B][CR]Copy the download URL to your clipboard and then go to www.urlshortbot.com. In here you need to enter the URL in the "Long URL" field and then in the "Custom Keyword" field you need to enter "noobs" (without the quotation marks) followed by your keyword. We recommend always using a random test keyword for testing because once you have a keyword you can\'t change it, also when uploading make sure it\'s a link you can edit and still keep the same URL - that way it\'s easy to keep up to date and you can still use the same keyword. In our example of kids we would set the custom keyword as "noobskids". The noobs bit is ignored and is only for helping the addon know what to look for, the user would just type in "kids" for the kids pack to be installed.')
#---------------------------------------------------------------------------------------------------
# (Instructions) Adding other wizards
def Instructions_5():
    Text_Boxes('Adding Third Party Wizards', '[COLOR=gold]ONE WIZARD TO RULE THEM ALL![/COLOR][CR]Did you know the vast majority of wizards out there (every single one we\'ve tested) has just been a copy/paste of very old code created by the team here? We\'ve noticed a lot of the users installing builds via these third party wizards have run into many different problems so we thought we\'d take it upon ourselves to help out...'
    '[CR][CR][CR][COLOR=gold]WHAT BENEFITS DOES THIS HAVE?[/COLOR][CR]We\'ve added extra code that checks for common errors, unfortunately there are some people out there using inferior programs to create their backups and that is causing problems in their wizards. If such a problem exists when trying to use another wizard you can try adding the details to this addon and it automatically fixes any corrupt files it finds. Of course there are other benefits... installing code from an unknown source can give the author access to your system so make sure you always trust the author(s). Why take the risk of installing wizards created by anonymous usernames on social media sites when you can install from a trusted source like noobsandnerds and you\'ll also be safe in the knowledge that any new updates and improvements will be made here first - we do not copy/paste code, we are actively creating new exciting solutions!'
    '[CR][CR][CR][COLOR=gold]ADDING 3RD PARTY WIZARDS TO THIS ADDON[/COLOR][CR][CR][COLOR=dodgerblue][B]Step 1:[/COLOR] Enabling 3rd Party Wizards[/B][CR]In the addon settings under the Community Builds section you have the option to enable third party community builds, if you click on this you will be able to enter details of up to 5 different wizards.'
    '[CR][CR][COLOR=dodgerblue][B]Step 2:[/COLOR] Enter the URL[/B][CR]As virtually all wizards use exactly the same structure all you need to do is find out what URL they are looking up in the code, you can open the default.py file of the wizard in a text editor and search for "http" and you will more than likely find the URL straight away. Try entering it in a web address, it should show the details for all the builds in that wizard in a text based page. If the page is blank don\'t worry it may just be locked from web browsers and can only be opened in Kodi, try it out and see if it works.'
    '[CR][CR][COLOR=dodgerblue][B]Step 3:[/COLOR] Enter the name[/B][CR]Give the wizard a name, now when you go into the Community Builds section you\'ll have the official noobsandnerds builds as an option and also any new ones you\'ve added.')
#-----------------------------------------------------------------------------------------------------------------
# Return details about the IP address lookup       
def IP_Check():
    ip_site = ADDON.getSetting('ip_site')
    try:
        if ip_site == "whatismyipaddress.com":
           BaseURL       = 'http://whatismyipaddress.com/'
           link          = Open_URL(BaseURL, 30).replace('\n','').replace('\r','')
           if not 'Access Denied' in link:
               ipmatch       = re.compile('whatismyipaddress.com/ip/(.+?)"').findall(link)
               ipfinal       = ipmatch[0] if (len(ipmatch) > 0) else 'Unknown'
               xbmc.log(ipfinal)
               details       = re.compile('"font-size:14px;">(.+?)</td>').findall(link)
               xbmc.log(str(details))
               provider      = details[0] if (len(details) > 0) else 'Unknown'
               xbmc.log(provider)
               location      = details[1]+', '+details[2]+', '+details[3] if (len(details) > 2) else 'Unknown'
               xbmc.log(location)
               dialog.ok('www.whatismyipaddress.com',"[B][COLOR gold]Address: [/COLOR][/B] %s" % ipfinal, '[B][COLOR gold]Provider: [/COLOR][/B] %s' % provider, '[B][COLOR gold]Location: [/COLOR][/B] %s' % location)
        else:
            BaseURL       = 'https://www.iplocation.net/find-ip-address'
            link          = Open_URL(BaseURL, 30).replace('\n','').replace('\r','')
            xbmc.log(link)
            segment       = re.compile('<table class="iptable">(.+?)</table>').findall(link)
            xbmc.log(str(segment))
            ipmatch       = re.compile('font-weight: bold;">(.+?)</span>').findall(str(segment))
            xbmc.log(ipmatch)
            ipfinal       = ipmatch[0] if (len(ipmatch) > 0) else 'Unknown'
            providermatch = re.compile('Host Name</th><td>(.+?)</td>').findall(str(segment))
            hostname      = providermatch[0] if (len(providermatch) > 0) else 'Unknown'
            locationmatch = re.compile('IP Location</th><td>(.+?)&nbsp;').findall(str(segment))
            location      = locationmatch[0] if (len(locationmatch) > 0) else 'Unknown'
            dialog.ok('www.iplocation.net',"[B][COLOR gold]Address: [/COLOR][/B] %s" % ipfinal, '[B][COLOR gold]Host: [/COLOR][/B] %s' % hostname, '[B][COLOR gold]Location: [/COLOR][/B] %s' % location)
    except:
        dialog.ok('SERVICE UNAVAILABLE', 'It was not possible to contact the relevant website to check your details. Please check your internet connection and if that\'s ok try using an alternative site in the settings.')
#---------------------------------------------------------------------------------------------------
# Check to see if a specific dialog/window is active
def Is_Window_Active(window_type):
    global globalyesno
    globalyesno  = False
    windowactive = False
    counter      = 0

    if window_type == 'yesnodialog':
        count = 30
    else:
        count = 10
    
    okwindow = False

# Do not get stuck in an infinite loop. Check x amount of times and if condition isn't met after x amount it quits
    while not okwindow and counter < count:
        xbmc.sleep(100)
        xbmc.log('### %s not active - sleeping (%s)' % (window_type, counter))
        okwindow = xbmc.getCondVisibility('Window.IsActive(%s)' % window_type)
        counter += 1

    if okwindow:
        globalyesno = True

# Window is active
    while okwindow:
        okwindow = xbmc.getCondVisibility('Window.IsActive(%s)' % window_type)
        xbmc.sleep(250)

    return okwindow
#---------------------------------------------------------------------------------------------------
# Install a keyword
def Keyword_Search(url):
    if not os.path.exists(packages):
        os.makedirs(packages)
    
    downloadurl = ''
    title       = 'Enter Keyword'
    keyword     = SEARCH(title)
    downloadurl = url+keyword
    lib         = os.path.join(packages, keyword+'.zip')
    
    if keyword !='':
        backupchoice = dialog.yesno('Backup existing setup','Installing certain keywords can result in some existing settings or add-ons to be replaced. Would you like to create a backup before proceeding?')
        
        if backupchoice == 1:
            Local_Backup()
        
        try:
            if debug == 'true':
                xbmc.log("### Attempting download "+downloadurl+" to "+lib)
            dp.create("Web Installer","Downloading ",'', 'Please Wait')
            downloader.download(downloadurl,lib)
            xbmc.log("### Keyword "+keyword+" Successfully downloaded")
            dp.update(0,"", "Extracting Zip Please Wait")
            
            if zipfile.is_zipfile(lib):
                
                try:
                    extract.all(lib,HOME,dp)
                    Update_Repo(showdialog = False)
                    dialog.ok("KEYWORD INSTALL", "","Content now installed", "")
                    dp.close()
                
                except:
                    dialog.ok("Error with zip",'There was an error trying to install this file. It may possibly be corrupt, either try again or contact the author of this keyword.')
                    xbmc.log("### Unable to install keyword (passed zip check): %s"%keyword)
            else:
                dialog.ok("Keyword Error",'The keyword you typed could not be installed. Please check the spelling and if you continue to receive this message it probably means that keyword is no longer available.')
            
        except:
            dialog.ok("Keyword Error",'The keyword you typed could not be installed. Please check the spelling and if you continue to receive this message it probably means that keyword is no longer available.')
            xbmc.log("### Unable to install keyword (unknown error, most likely a typo in keyword entry): %s"%keyword)
    
    if os.path.exists(lib):
        os.remove(lib)
#-----------------------------------------------------------------------------------------------------------------
# Force close Kodi
def Kill_XBMC():
    os._exit(1)
#---------------------------------------------------------------------------------------------------
# Open Kodi Settings
def Kodi_Settings():
    xbmc.executebuiltin('ReplaceWindow(settings)')
#---------------------------------------------------------------------------------------------------
# Function to find the latest version of a database
def Latest_DB(DB):
    if DB in ['Addons', 'ADSP', 'Epg', 'MyMusic', 'MyVideos', 'Textures', 'TV', 'ViewModes']:
        match   = glob.glob(os.path.join(DATABASE,'%s*.db' % DB))
        comp    = '%s(.+?).db' % DB[1:]
        highest = 0
        for file in match:
            try:
                check = int(re.compile(comp).findall(file)[0])
            except:
                check = 0
            if highest < check:
                highest = check
        return '%s%s.db' % (DB, highest)
    else:
        return False
#---------------------------------------------------------------------------------------------------
# Create a FULL backup
def Local_Backup():
    Check_Download_Path()
    
    fullbackuppath  = xbmc.translatePath(os.path.join(USB,'Community_Builds','My_Builds',''))
    myfullbackup    = xbmc.translatePath(os.path.join(USB,'Community_Builds','My_Builds','my_full_backup.zip'))
    myfullbackupGUI = xbmc.translatePath(os.path.join(USB,'Community_Builds','My_Builds','my_full_backup_GUI_Settings.zip'))
    
    if not os.path.exists(fullbackuppath):
        os.makedirs(fullbackuppath)
    
    vq = Get_Keyboard( heading="Enter a name for this backup" )
    
    if ( not vq ):
        return False, 0
    
    title              = urllib.quote_plus(vq)
    backup_zip         = xbmc.translatePath(os.path.join(fullbackuppath,title+'.zip'))
    exclude_dirs_full  =  [AddonID]
    exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf','Thumbs.db','.gitignore']
    message_header     = "Creating full backup of existing build"
    message_header2    = "Creating Community Build"
    message1           = "Archiving..."
    message2           = ""
    message3           = "Please Wait"
    
    Archive_Tree(HOME, myfullbackup, message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)
    dialog.ok('Full Backup Complete','You can locate your backup at:[COLOR=dodgerblue]',myfullbackup+'[/COLOR]')
#-----------------------------------------------------------------------------------------------------------------
# View the log from within Kodi
def Log_Viewer():
    content = Grab_Log()
    Text_Boxes('Log Viewer', content)
#---------------------------------------------------------------------------------------------------
# Dialog to warn users about local guisettings fix.
def Local_GUI_Dialog():
    dialog.ok("Restore local guisettings fix", "You should [COLOR=lime]ONLY[/COLOR] use this option if the guisettings fix is failing to download via the addon. Installing via this method means you do not receive notifications of updates")
    Restore_Local_GUI()
#---------------------------------------------------------------------------------------------------
# Search in description
def Manual_Search(mode):
    vq = Get_Keyboard( heading="Search for content" )
    if ( not vq ):
        return False, 0
    title = urllib.quote_plus(vq)        
    Grab_Builds(mode+'&name='+title)
#-----------------------------------------------------------------------------------------------------------------
# Function to move a directory to another location, use 1 for clean paramater if you want to remove original source.
def Move_Tree(src,dst,clean):
    for src_dir, dirs, files in os.walk(src):
        dst_dir = src_dir.replace(src, dst, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.move(src_file, dst_dir)
    if clean == 1:
        try:
            shutil.rmtree(src)
        except:
            pass
#---------------------------------------------------------------------------------------------------
# Multiselect Dialog - works with gotham onwards
def multiselect(title, list, images, description):
    global pos
    global listicon
    class MultiChoiceDialog(pyxbmct.AddonDialogWindow):
        def __init__(self, title="", items=None, images=None, description=None):
            super(MultiChoiceDialog, self).__init__(title)
            self.setGeometry(1100, 700, 20, 20)
            self.selected = []
            self.set_controls()
            self.connect_controls()
            self.listing.addItems(items or [])
            self.set_navigation()
            self.connect(ACTION_MOVE_UP, self.update_list)
            self.connect(ACTION_MOVE_DOWN, self.update_list)
            
        def set_controls(self):
            Background  = pyxbmct.Image(dialog_bg, aspectRatio=0) # set aspect ratio to stretch
            Background.setImage(dialog_bg)
            self.listing = pyxbmct.List(_imageWidth=15)
            self.placeControl(Background, 0, 0, rowspan=20, columnspan=20)
            Icon=pyxbmct.Image(images[0], aspectRatio=2) # set aspect ratio to keep original
            Icon.setImage(images[0])
            self.placeControl(Icon, 0, 11, rowspan=8, columnspan=8, pad_x=10, pad_y=10)
            self.textbox = pyxbmct.TextBox()
            self.placeControl(self.textbox, 8, 11, rowspan=9, columnspan=9, pad_x=10, pad_y=10)
            self.textbox.setText(description[0])
            self.textbox.autoScroll(5000, 2000, 8000)
            self.ok_button = pyxbmct.Button("OK")
            self.placeControl(self.ok_button, 17, 13, pad_x=10, pad_y=10, rowspan=2, columnspan=3)
            self.cancel_button = pyxbmct.Button("Cancel")
            self.placeControl(self.cancel_button, 17, 16, pad_x=10, pad_y=10, rowspan=2, columnspan=3)
            self.placeControl(self.listing, 0, 0, rowspan=20, columnspan=10, pad_y=10) # grid reference, start top left and span 9 boxes down and 5 across

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
            blackout = pyxbmct.Image(black, aspectRatio=0) # set aspect ratio to stretch
            blackout.setImage(black)
            self.placeControl(blackout, 0, 11, rowspan=8, columnspan=8, pad_x=10, pad_y=10)
            pos      = self.listing.getSelectedPosition()
            listicon = images[pos]
            Icon     = pyxbmct.Image(listicon, aspectRatio=2)
            Icon.setImage(listicon)
            self.placeControl(Icon, 0, 11, rowspan=8, columnspan=8, pad_x=10, pad_y=10)
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
            
    dialog = MultiChoiceDialog(title, list, images, description)
    dialog.doModal()
    return dialog.selected
    del dialog
#---------------------------------------------------------------------------------------------------
# NaN Keyword menu
def NaN_Menu():
    addDir('','[COLOR=dodgerblue]How to install keywords[/COLOR]','','instructions_3','mainmenu/keyword.png','','','')
    addDir('','[COLOR=dodgerblue]How to create keywords[/COLOR]','','instructions_4','mainmenu/keyword.png','','','')
    addDir('','[COLOR=gold]-----------------------------------------------------------------[/COLOR]','','','mainmenu/keyword.png','','','')
    addDir('','Install Keywords', 'http://urlshortbot.com/noobs', 'keywords', 'mainmenu/keyword.png','','','')
    addDir('','Create Keywords', 'create_pack', 'create_keyword', 'mainmenu/keyword.png','','','')
#-----------------------------------------------------------------------------------------------------------------
# Simple shortcut to create a notification
def Notify(title,message,times=2000,icon=ICON):
    xbmc.executebuiltin('XBMC.Notification(%s, %s, %s, %s)' % (title , message , times, icon))
#---------------------------------------------------------------------------------------------------
# Open Kodi File Manager
def Open_Filemanager():
    xbmc.executebuiltin('ActivateWindow(filemanager,return)')
    return
#---------------------------------------------------------------------------------------------------
# Open Kodi System Info
def Open_System_Info():
    xbmc.executebuiltin('ActivateWindow(systeminfo)')
#-----------------------------------------------------------------------------------------------------------------
# Function to open a URL and return the contents
def Open_URL(url, t):
    req = urllib2.Request(url)
    req.add_header('User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 10.0; WOW64; Windows NT 5.1; en-GB; rv:1.9.0.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36 Gecko/2008092417 Firefox/3.0.3')
# OLD ONE    req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    counter = 0
    success = False
    while counter < 5 and success == False: 
        response = urllib2.urlopen(req, timeout = t)
        link     = response.read()
        response.close()
        counter += 1
        if link != '':
            success = True
    if success == True:
        return link.replace('\r','').replace('\n','').replace('\t','')
    else:
        dialog.ok('Unable to contact server','There was a problem trying to access the server, please try again later.')
        return
#---------------------------------------------------------------------------------------------------
# Function to create an OE tar backup
def OpenELEC_Backup():
    import tarfile

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    dp.create("Creating Backup","Adding files... ",'', 'Please Wait')
    tar = tarfile.open(os.path.join(backup_dir, Timestamp()+'.tar'), 'w')
    
    for directory in BACKUP_DIRS:
        dp.update(0,"Backing Up",'[COLOR blue]%s[/COLOR]'%directory, 'Please Wait')
        tar.add(directory)
    
    tar.close()
    dp.close()
#---------------------------------------------------------------------------------------------------
# Check if system is OE or LE
def OpenELEC_Check():
    content = Grab_Log()
    if 'Running on OpenELEC' in content or 'Running on LibreELEC' in content:
        return True
#---------------------------------------------------------------------------------------------------
# Open OE Settings
def OpenELEC_Settings():
    try:
        xbmcaddon.Addon(id='service.openelec.settings').getAddonInfo('name')
        xbmc.executebuiltin('ActivateWindow(10025,plugin://service.openelec.settings,return)')
    except:
        xbmcaddon.Addon(id='service.libreelec.settings').getAddonInfo('name')
        xbmc.executebuiltin('ActivateWindow(10025,plugin://service.libreelec.settings,return)')
#---------------------------------------------------------------------------------------------------
# Set popup xml based on platform
def pop(xmlfile):
# if popup is an announcement from web
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
            dp.create('Grabbing Latest Updates','','','')
            downloader.download(xmlfile,os.path.join(ADDONS,AddonID,'resources','skins','DefaultSkin','media','latest.jpg'))
            writefile = open(latest, mode='w+')
            writefile.write(filedate)
            writefile.close()
        xmlfile = 'latest.xml'
    popup = SPLASH(xmlfile,ADDON.getAddonInfo('path'),'DefaultSkin',close_time=34)
    popup.doModal()
    del popup
#-----------------------------------------------------------------------------------------------------------------
#Recursive loop for downloading files from web
def Recursive_Loop(recursive_location,remote_path):
    if not os.path.exists(recursive_location):
        os.makedirs(recursive_location)
    
    link   = Open_URL(remote_path, 10).replace('\n','').replace('\r','')
    match  = re.compile('href="(.+?)"', re.DOTALL).findall(link)
    
    for href in match:
        filepath=xbmc.translatePath(os.path.join(recursive_location,href)) #works
        
        if '/' not in href:
            
            try:
                dp.update(0,"Downloading [COLOR=yellow]"+href+'[/COLOR]','','Please wait...')
                downloader.download(remote_path+href, filepath, dp)
            
            except:
                print"failed to install"+href
        
        if '/' in href and '..' not in href and 'http' not in href:
            remote_path2 = remote_path+href
            Recursive_Loop(filepath,remote_path2)
        
        else:
            pass
#---------------------------------------------------------------------------------------------------
# Dialog to tell users how to register
def Register():
    dialog.ok("Register to unlock features", "To get the most out of this addon please register at the NOOBSANDNERDS forum for free.",'WWW.NOOBSANDNERDS.COM/SUPPORT')
#---------------------------------------------------------------------------------------------------
# Function to clear the addon_data
def Remove_Addon_Data():
    choice = dialog.yesno('DELETE ADD-ON DATA', 'Do you want to remove individual addon_data folders or wipe all addon_data?', yeslabel='EVERYTHING', nolabel='INDIVIDUAL ITEMS')
    
    if choice:
        choice = dialog.yesno('Are you ABSOLUTELY certain?','This will remove ALL your addon_data, there\'s no getting it back! Are you certain you want to continue?')
        if choice:
            Delete_Userdata()
            dialog.ok("Addon_Data Removed", '', 'Your addon_data folder has now been removed.','')
    else:
        namearray = []
        iconarray = []
        descarray = []
        patharray = []
        finalpath = []

        for file in os.listdir(ADDON_DATA):
            if os.path.isdir(os.path.join(ADDON_DATA,file)):
                try:
                    Addon       = xbmcaddon.Addon(file)
                    name        = Addon.getAddonInfo('name')
                    iconimage   = Addon.getAddonInfo('icon')
                    description = Addon.getAddonInfo('description')
                except:
                    name        = 'Unknown Add-on'
                    iconimage   =  unknown_icon
                    description = 'No add-on has been found on your system that matches this ID. The most likely scenario for this is you\'ve previously uninstalled this add-on and left the old addon_data on the system.'

            else:
                name        = 'Unknown Add-on'
                iconimage   =  unknown_icon
                description = 'No add-on has been found on your system that matches this ID. The most likely scenario for this is you\'ve previously uninstalled this add-on and left the old addon_data on the system.'

            filepath    = os.path.join(ADDON_DATA,file)
            namearray.append('%s [COLOR=gold](%s)[/COLOR]' % (file,name))
            iconarray.append(iconimage)
            descarray.append(description)
            patharray.append(filepath)

        finalarray = multiselect('Addon_Data To Remove',namearray,iconarray,descarray)
        for item in finalarray:
            newpath = patharray[item]
            newname = namearray[item]
            finalpath.append([newname,newpath])
        xbmc.log('FINAL: %s' % finalpath)
        if len(finalpath) > 0:
            Remove_Addons(finalpath)
#---------------------------------------------------------------------------------------------------
# Function to remove a list of addons including addon_data
def Remove_Addons(url):
    removed = 0
    for item in url:
        data_path = item[1].replace(ADDONS,ADDON_DATA)
        if 'addon_data' in item[1]:
            addontype = 'Addon_Data'
        else:
            addontype = 'Addon'
        if dialog.yesno("Remove %s" % addontype, "Do you want to Remove:",'[COLOR=dodgerblue]%s[/COLOR]'%item[0]):
            if not 'addon_data' in item[1]:
                removed = 1
            for root, dirs, files in os.walk(item[1]):
                
                for f in files:
                    os.unlink(os.path.join(root, f))
                
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
            os.rmdir(item[1])
            if not 'addon_data' in item[1]:
                if dialog.yesno('Remove Addon_Data?','Would you also like to remove the addon_data associated with this add-on? This contains your add-on settings and can contain personal information such as username/password.'):
                    try:
                        for root, dirs, files in os.walk(data_path):
                            for f in files:
                                os.unlink(os.path.join(root, f))
                            for d in dirs:
                                shutil.rmtree(os.path.join(root, d))
                        os.rmdir(data_path)
                    except:
                        pass
    if removed:
        xbmc.executebuiltin( 'UpdateLocalAddons' )
        xbmc.executebuiltin( 'UpdateAddonRepos' )
        Remove_Packages('nodialog')
        Clean_Addons()
# Need to create function to wipe relevant bits from db
#        Cleanup_Old_Addons()
        dialog.ok('REMOVAL COMPLETE','The addons database file now needs purging, to do so we need to restart. If prompted please agree to the deletion otherwise your add-ons may still appear in Kodi even if they don\'t physically exist.')
        Kill_XBMC('wipe')
#---------------------------------------------------------------------------------------------------
# Function to restore a zip file 
def Remove_Build():
    Check_Download_Path()
    filename = dialog.browse(1, 'Select the backup file you want to DELETE', 'files', '.zip', False, False, USB)
    
    if filename != USB:
        clean_title = ntpath.basename(filename)
        if dialog.yesno('Delete Backup File', 'This will completely remove '+clean_title, 'Are you sure you want to delete?', '', nolabel='No, Cancel',yeslabel='Yes, Delete'):
            os.remove(filename)
#---------------------------------------------------------------------------------------------------
# Function to clear the packages folder
def Remove_Crash_Logs():
    if dialog.yesno('Remove All Crash Logs?', 'There is absolutely no harm in doing this, these are log files generated when Kodi crashes and are only used for debugging purposes.', nolabel='Cancel',yeslabel='Delete'):
        Delete_Logs()
        dialog.ok("Crash Logs Removed", '', 'Your crash log files have now been removed.','')
#---------------------------------------------------------------------------------------------------
# Function to remove the nag screen
def Remove_Nag():
    shutil.rmtree(os.path.join(ADDONS,binascii.unhexlify('7363726970742e6d6f64756c652e637967706669')))
    dialog.ok(binascii.unhexlify('53746172747570206469616c6f672064697361626c6564'),binascii.unhexlify('54686520436f6d6d756e6974792050726f74656374696f6e206e61672073637265656e20686173206e6f77206265656e2064697361626c65642e20596f752063616e206e6f77206372656174652061206261636b75702074686174206e6f206c6f6e67657220686173207468652070726f74656374696f6e2c204f4e4c5920796f7520746865206275696c6420617574686f722063616e2064697361626c65207468697320736f206d616b65207375726520796f7520646f6e2774207368617265206c6f67696e20696e666f2e'))
#---------------------------------------------------------------------------------------------------
# Function to clear the packages folder
def Remove_Packages():
    choice = xbmcgui.Dialog().yesno('Delete Packages Folder', 'Do you want to clean the packages folder? This will free up space by deleting the old zip install files of your addons. Keeping these files can also sometimes cause problems when reinstalling addons', nolabel='Cancel',yeslabel='Delete')
    
    if choice == 1:
        Delete_Packages()
        dialog.ok("Packages Removed", '', 'Your zip install files have now been removed.','')
#---------------------------------------------------------------------------------------------------
# Function to clear the packages folder
def Remove_Textures_Dialog():
    if dialog.yesno('Clear Cached Images?', 'This will clear your textures13.db file and remove your Thumbnails folder. These will automatically be repopulated after a restart.', nolabel='Cancel',yeslabel='Delete'):
        Remove_Textures()
        Destroy_Path(THUMBNAILS)
        
        if dialog.yesno('Quit Kodi Now?', 'Cache has been successfully deleted.', 'You must now restart Kodi, would you like to quit now?','', nolabel='I\'ll restart later',yeslabel='Yes, quit'):
            try:
                xbmc.executebuiltin("RestartApp")
            except:
                Kill_XBMC()
#---------------------------------------------------------------------------------------------------
# Function to remove textures13.db and thumbnails folder    
def Remove_Textures():
    textures = os.path.join(DATABASE, Latest_DB('Textures'))
    if os.path.exists(textures):
        try:
            textdb = database.connect(textures)
            textexe = textdb.cursor()
        except Exception, e:
            xbmc.log(str(e))
            return False
    else:
        xbmc.log('%s not found.' % textures)
        return False

    textexe.execute("""SELECT name FROM sqlite_master WHERE type = 'table';""")
    for table in textexe.fetchall():
        if table[0] == 'version': 
            xbmc.log('Data from table `%s` skipped.' % table[0])
        else:
            try:
                textexe.execute("""DELETE FROM %s""" % table[0])
                textdb.commit()
                xbmc.log('Data from table `%s` cleared.' % table[0])
            except e:
                xbmc.log(str(e))
    
    xbmc.log('%s DB Purging Complete.' % textures)
    show = textures.replace('\\', '/').split('/')
    Notify("Purge Database", "%s Complete" % show[len(show)-1])
#---------------------------------------------------------------------------------------------------
#Function to restore a backup xml file (guisettings, sources, RSS)
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

    dialog.ok("Restore Complete", "", 'All Done !','')
#---------------------------------------------------------------------------------------------------
# Function to restore a community build
def Restore_Community(name,url,video,description,skins,guisettingslink,artpack):
    profilechoice = 1
    removeprofile = 0
    CP_Profiles   = os.path.join(HOME,'CP_Profiles')
    Profile_List  = os.path.join(CP_Profiles, 'list.txt')
    mainaddons    = []
    filename      = description.replace(' ','_').replace("'","").replace(":","-")
    
    if not os.path.exists(CP_Profiles):
        os.makedirs(CP_Profiles)

    clean_folder_name = os.path.join(CP_Profiles, filename)
    if not os.path.exists(clean_folder_name):
        os.makedirs(clean_folder_name)
    else:
        removeprofile = dialog.yesno('Profile Already Exists','This build is already installed on your system, would you like to remove the old one and reinstall?')
        if removeprofile == 1:
            try:
                shutil.rmtree(clean_folder_name)
                os.makedirs(clean_folder_name)
            except:
                pass
        else:
            profilechoice = 2

    if profilechoice == 1:
        lib=os.path.join(CBPATH, filename+'_gui.zip')
        if debug == 'true':
            xbmc.log("### Download path = %s" % lib)
# Download guisettings from the build
        dp.create("Community Builds","Downloading Skin Tweaks",'', 'Please Wait')
        try:
            downloader.download(guisettingslink, lib)
            if debug == 'true':
                xbmc.log("### successfully downloaded guisettings.xml")
        except:
            dialog.ok('Problem Detected','Sorry there was a problem downloading the guisettings file. Please check your storage location, if you\'re certain that\'s ok please notify the build author on the relevant support thread.')
            if debug == 'true':
                xbmc.log("### FAILED to download %s" % guisettingslink)

# Check that gui file is a real zip and the uploader hasn't put a bad link in the db
        if zipfile.is_zipfile(lib):
            guisize = str(os.path.getsize(lib))   
        else:
            guisize = '0'
            
        dp.create("Community Builds","Downloading "+description,'', 'Please Wait')
        lib = os.path.join(CBPATH, filename+'.zip')
        
        if not os.path.exists(CBPATH):
            os.makedirs(CBPATH)

# Extract to a temporary folder so we can add new id.xml and rip out stuff not needed
        tempCPfolder = os.path.join(CP_PROFILE,'extracted')
        downloader.download(url, lib, dp)
        if not zipfile.is_zipfile(lib):
            dialog.ok('NOT A VALID BUILD','The main file for this build is not a valid zip. Please contact the author of the build and let them know so they can either remove this build or update it. Thank you.')
            return

        dp.create("Community Builds","Extracting "+description,'', 'Please Wait')
        extract.all(lib, tempCPfolder,dp)
        if os.path.exists(os.path.join(tempCPfolder,'userdata','.cbcfg')):
            try:
                firstrun = os.path.join(tempCPfolder,'userdata','addon_data','firstrun')
                if not os.path.exists(firstrun):
                    os.makedirs(firstrun)
            except:
                pass
        if debug == 'true':
            xbmc.log("### Downloaded build to: "+lib)
            xbmc.log("### Extracted build to: "+tempCPfolder)

# Pull the details about the currently downloading build and add to new idfile in profile folder
        localfile = open(tempfile, mode='r')
        content   = localfile.read()
        localfile.close()

        temp         = re.compile('id="(.+?)"').findall(content)
        tempname     = re.compile('name="(.+?)"').findall(content)
        tempversion  = re.compile('version="(.+?)"').findall(content)

        tempcheck    = temp[0] if (len(temp) > 0) else ''
        namecheck    = tempname[0] if (len(tempname) > 0) else ''
        versioncheck = tempversion[0] if (len(tempversion) > 0) else ''

        xbmc.log("### Build name details to store in ti_id: %s" % namecheck)

        newaddondata = os.path.join(tempCPfolder,'userdata','addon_data','ti_id')
        newidfile    = os.path.join(newaddondata,'id.xml')
        if not os.path.exists(newaddondata):
            os.makedirs(newaddondata)

        writefile = open(newidfile, mode='w+')
        writefile.write('id="'+str(tempcheck)+'"\nname="'+namecheck+'"\nversion="'+versioncheck+'"\ngui="'+guisize+'"')
        writefile.close()

# Update the startup.xml version number so it can check for update on next run of add-on
        startuppath = os.path.join(newaddondata,'startup.xml')
        writefile = open(startuppath, mode='w+')
        writefile.write('date="01011001"\nversion="'+versioncheck+'"')
        writefile.close()

        tempidfile = open(newidfile,'r')
        tempcontent = tempidfile.read()
        tempidfile.close()
        xbmc.log("### ti_id/id.xml contents: %s" % tempcontent)
        
# Give option to merge guisettings
        guichoice = dialog.yesno("Keep Kodi Settings?", 'Do you want to keep your existing KODI settings (weather, screen calibration, PVR etc.) or wipe and install the ones supplied in this build?', yeslabel='Replace my settings', nolabel='Keep my settings')
        if guichoice == 0:
            GUI_Install(os.path.join(CP_PROFILE,'extracted','userdata','guisettings.xml'))

# List pre-installed Kodi addons, we don't need to copy these
        for item in os.listdir(KODI_ADDONS):
            mainaddons.append(item)

# Create an addonlist for new profile
        newlist = open(os.path.join(clean_folder_name,'addonlist'), mode='w+')
        for item in os.listdir(ADDONS):
            if not item in mainaddons and item != 'plugin.program.totalinstaller' and item != 'packages':
                newlist.write(item+'|')
        newlist.close()
        if debug == 'true':
            xbmc.log("### Created addonlist to: %s" % os.path.join(clean_folder_name,'addonlist'))
        exclude_dirs_full =  ['addons','cache','CP_Profiles','system','temp','Thumbnails']
        exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf','.gitignore','addons*.db','textures13.db','.cbcfg']
        message_header = "Creating Profile Data File"
        message1 = "Archiving..."
        message2 = ""
        message3 = "Please Wait"
        Archive_Tree(tempCPfolder, os.path.join(clean_folder_name,'build.zip'), message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)
        if debug == 'true':
            xbmc.log("### Created: %s" % os.path.join(clean_folder_name,'build.zip'))

# Remove the downloaded build if not set to keep in add-on settings
        if localcopy == 'false':
            os.remove(lib)
            if debug == 'true':
                xbmc.log("### removed: %s" % lib)

        Check_Build_Addons(filename)
        incremental = 'http://noobsandnerds.com/TI/Community_Builds/downloadcount.php?id=%s' % (tempcheck)
        if not 'update' in video:
            try:
                Open_URL(incremental, 5)
            except:
                pass
#        choice = dialog.yesno('Install Successful','Your new profile has successfully been installed, would you like to switch to it now?')
#        if choice == 1:
        Switch_Profile(clean_folder_name)

#        shutil.rmtree(os.path.join(CP_Profiles,filename))
#---------------------------------------------------------------------------------------------------
# Function to restore a local backup
def Restore_Local_Community(url):
    exitfunction = 0
    choice4      = 0

    Check_Download_Path()

    if url == 'local':
        filename = xbmcgui.Dialog().browse(1, 'Select the backup file you want to restore', 'files', '.zip', False, False, USB)
        if filename == '':
            exitfunction = 1

    if exitfunction == 1:
        print"### No file selected, quitting restore process ###"
        return
        
    if url != 'local':
        dp.create("Community Builds","Downloading build.",'', 'Please Wait')
        filename=os.path.join(CBPATH, Timestamp()+'.zip')
    
        if not os.path.exists(CBPATH):
            os.makedirs(CBPATH)
    
        downloader.download(url, filename, dp)

    if os.path.exists(GUINEW):
        if os.path.exists(GUI):
            os.remove(GUINEW)
        else:
            os.rename(GUINEW,GUI)
            
    if os.path.exists(GUIFIX):
        os.remove(GUIFIX)
        
# Function for debugging, creates a file that was created in previous call and subsequently deleted when run
    if not os.path.exists(tempfile):
        localfile = open(tempfile, mode='w+')
        
    if os.path.exists(guitemp):
        os.removedirs(guitemp)
        
# Rename guisettings.xml to guinew.xml so we can edit without XBMC interfering.
    try:
        os.rename(GUI,GUINEW)

    except:
        dialog.ok("NO GUISETTINGS!",'No guisettings.xml file has been found.', 'Please exit XBMC and try again','')
        return

    choice = xbmcgui.Dialog().yesno(name, 'We highly recommend backing up your existing build before installing any builds. Would you like to perform a backup first?', nolabel='Backup',yeslabel='Install')
    if choice == 0:
        mybackuppath = xbmc.translatePath(os.path.join(USB,'Community_Builds','My_Builds'))

        if not os.path.exists(mybackuppath):
            os.makedirs(mybackuppath)

        vq = Get_Keyboard( heading="Enter a name for this backup" )
        if ( not vq ):
            return False, 0
            
        title              = urllib.quote_plus(vq)
        backup_zip         = xbmc.translatePath(os.path.join(mybackuppath,title+'.zip'))
        exclude_dirs_full  =  [AddonID]
        exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf','.gitignore']
        message_header     = "Creating full backup of existing build"
        message1           = "Archiving..."
        message2           = ""
        message3           = "Please Wait"
        
        Archive_Tree(HOME, backup_zip, message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)
    choice3 = xbmcgui.Dialog().yesno(name, 'Would you like to keep your existing database files or overwrite? Overwriting will wipe any existing music or video library you may have scanned in.', nolabel='Overwrite',yeslabel='Keep Existing')
    if choice3 == 1:
        if os.path.exists(tempdbpath):
            shutil.rmtree(tempdbpath)

        try:
            shutil.copytree(DATABASE, tempdbpath, symlinks=False, ignore=shutil.ignore_patterns("Textures13.db","Addons16.db","Addons15.db","saltscache.db-wal","saltscache.db-shm","saltscache.db","onechannelcache.db")) #Create temp folder for databases, give user option to overwrite existing library

        except:
            choice4 = xbmcgui.Dialog().yesno(name, 'There was an error trying to backup some databases. Continuing may wipe your existing library. Do you wish to continue?', nolabel='No, cancel',yeslabel='Yes, overwrite')
            if choice4 == 1: pass
            if choice4 == 0: exitfunction=1;return

        backup_zip = xbmc.translatePath(os.path.join(USB,'Database.zip'))
        Archive_File(tempdbpath,backup_zip)
    
    if exitfunction == 1:
        print"### User decided to exit restore function ###"
        return
    
    else:
        time.sleep(1)
        readfile         = open(CBADDONPATH, mode='r')
        default_contents = readfile.read()
        readfile.close()

# check to see if the dickheads have used some piece of shit backup program that includes logs, if they have re-zip it up PROPERLY!!!       
        print"### Checking zip file structure ###"
        z = zipfile.ZipFile(filename)
        if 'xbmc.log' in z.namelist() or 'kodi.log' in z.namelist() or '.git' in z.namelist() or '.svn' in z.namelist():
            print "### Whoever created this build has used completely the wrong backup method, lets try and fix it! ###"        
            dialog.ok('Fixing Bad Zip','Whoever created this build has used the wrong backup method, please wait while we fix it - this could take some time! Click OK to proceed')
            zin       = zipfile.ZipFile (filename, 'r')
            filename2 = os.path.join(CBPATH, 'fixed.zip')
            zout      = zipfile.ZipFile (filename2, 'w')

            dp.create("Fixing Build","Checking ",'', 'Please Wait')
            
            for item in zin.infolist():
                buffer = zin.read(item.filename)
                clean_file = str(item.filename)

                if (item.filename[-4:] != '.log') and not '.git' in clean_file and not '.svn' in clean_file:
                    zout.writestr(item, buffer)
                    dp.update(0,"Fixing...",'[COLOR yellow]%s[/COLOR]'%item.filename, 'Please Wait')
            
            dp.close()
            zout.close()
            zin.close()
            filename = filename2
            
        dp.create("Restoring Backup Build","Checking ",'', 'Please Wait')
        dp.update(0,"", "Extracting Zip Please Wait")
        
        try:
            extract.all(filename,HOME,dp)
        except:
            dialog.ok('ERROR IN BUILD ZIP','Please contact the build author, there are errors in this zip file that has caused the install process to fail. Most likely cause is it contains files with special characters in the name.')
            return
        
        time.sleep(1)

        if choice3 == 1:
            extract.all(backup_zip,DATABASE,dp) #This folder first needs zipping up
            
            if choice4 !=1:
                shutil.rmtree(tempdbpath)
        
        cbdefaultpy = open(CBADDONPATH, mode='w+')
        cbdefaultpy.write(default_contents)
        cbdefaultpy.close()
        try:
            os.rename(GUI,GUIFIX)

        except:
            print"NO GUISETTINGS DOWNLOADED"

        time.sleep(1)
        localfile = open(GUINEW, mode='r') #Read the original skinsettings tags and store in memory ready to replace in guinew.xml
        content = localfile.read()
        localfile.close()
        skinsettingsorig = re.compile('<skinsettings>[\s\S]*?<\/skinsettings>').findall(content)
        skinorig  = skinsettingsorig[0] if (len(skinsettingsorig) > 0) else ''
        skindefault = re.compile('<skin default[\s\S]*?<\/skin>').findall(content)
        skindefaultorig  = skindefault[0] if (len(skindefault) > 0) else ''
        lookandfeelorig = re.compile('<lookandfeel>[\s\S]*?<\/lookandfeel>').findall(content)
        lookandfeel  = lookandfeelorig[0] if (len(lookandfeelorig) > 0) else ''

        try:
            localfile2 = open(GUIFIX, mode='r')
            content2 = localfile2.read()
            localfile2.close()
            skinsettingscontent = re.compile('<skinsettings>[\s\S]*?<\/skinsettings>').findall(content2)
            skinsettingstext  = skinsettingscontent[0] if (len(skinsettingscontent) > 0) else ''
            skindefaultcontent = re.compile('<skin default[\s\S]*?<\/skin>').findall(content2)
            skindefaulttext  = skindefaultcontent[0] if (len(skindefaultcontent) > 0) else ''
            lookandfeelcontent = re.compile('<lookandfeel>[\s\S]*?<\/lookandfeel>').findall(content2)
            lookandfeeltext  = lookandfeelcontent[0] if (len(lookandfeelcontent) > 0) else ''
            replacefile = content.replace(skinorig,skinsettingstext).replace(lookandfeel,lookandfeeltext).replace(skindefaultorig,skindefaulttext)
            writefile = open(GUINEW, mode='w+')
            writefile.write(str(replacefile))
            writefile.close()

        except:
            print"### NO GUISETTINGS DOWNLOADED"

        if os.path.exists(GUI):
            os.remove(GUI)
        
        os.rename(GUINEW,GUI)
        try:
            os.remove(GUIFIX)
        
        except:
            pass
        
        os.makedirs(guitemp)
        time.sleep(1)
        Kill_XBMC()
#---------------------------------------------------------------------------------------------------
# Function to restore a local copy of guisettings_fix
def Restore_Local_GUI():
    Check_Download_Path()
    guifilename = xbmcgui.Dialog().browse(1, 'Select the guisettings zip file you want to restore', 'files', '.zip', False, False, USB)

    if guifilename == '':
        return

    else:
        local=1
        GUI_Settings_Fix(guifilename,local)  
#---------------------------------------------------------------------------------------------------
# Function to restore an OE based community build
def Restore_OpenELEC(name,url,video):
    choice = xbmcgui.Dialog().yesno('Full Wipe And New Install', 'This is a great option for first time install or if you\'re encountering any issues with your device. This will wipe all your Kodi settings, do you wish to continue?', nolabel='Cancel',yeslabel='Accept')
    if choice == 0:
        return

    elif choice == 1:

        lib  = '/storage/openelec_temp/'
        dest = '/storage/.restore/'
        path = os.path.join(dest, Timestamp()+'.tar')
        if not os.path.exists(dest):
            try:
                os.makedirs(dest)
            except:
                pass
        try:
            dp.create('Downloading Build','Please wait','','')
            downloader.download(url, path)
            success = True
        except:
            success = False
        time.sleep(2)

        if success==True:
        
            try:
                localfile = open(tempfile, mode='r')
                content   = localfile.read()
                localfile.close()
            
                temp         = re.compile('id="(.+?)"').findall(content)
                tempcheck    = temp[0] if (len(temp) > 0) else ''
        
            except:
                pass
            if tempcheck != '':
                incremental = 'http://noobsandnerds.com/TI/Community_Builds/downloadcount.php?id=%s' % (tempcheck)
            try:
                Open_URL(incremental, 5)
            except:
                pass

# Create temp folder for checking if new build after restart              
            if not os.path.exists(lib):
                try:
                    os.makedirs(lib)
                except:
                    pass

            dialog.ok("Download Complete - Press OK To Reboot",'Once you press OK your device will attempt to reboot, if it hasn\'t rebooted within 30 seconds please pull the power to manually shutdown. When booting you may see lines of text, don\'t worry this is normal update behaviour!')
            xbmc.executebuiltin('Reboot')
#---------------------------------------------------------------------------------------------------
# Function to restore an OE based community build
def Restore_OpenELEC_Local():
    exitfunction = 0
    if dialog.yesno('Full Wipe And New Install', 'This is a great option if you\'re encountering any issues with your device. This will wipe all your Kodi settings and restore with whatever is in the backup, do you wish to continue?', nolabel='Cancel',yeslabel='Accept'):
        filename = dialog.browse(1, 'Select the backup file you want to restore', 'files', '.tar', False, False, backup_dir)
        if filename == '':
            exitfunction = 1

        if exitfunction == 1:
            xbmc.log("### No file selected, quitting restore process ###")
            return
        path = os.path.join(restore_dir, Timestamp()+'.tar')
        if not os.path.exists(restore_dir):
            try:
                os.makedirs(restore_dir)
            except:
                pass
        dp.create('Copying File To Restore Folder','','Please wait...')
        shutil.copyfile(filename,path)
        xbmc.executebuiltin('Reboot')
#---------------------------------------------------------------------------------------------------
# Create restore menu
def Restore_Option():
    Check_Local_Install()
    if OpenELEC_Check():
        addDir('','[COLOR=dodgerblue]Restore a locally stored OpenELEC Backup[/COLOR]','','restore_local_OE','mainmenu/maintenance.png','','','Restore A Full OE System Backup')

    addDir('','[COLOR=dodgerblue]Restore A Locally stored build[/COLOR]','local','restore_local_CB','mainmenu/maintenance.png','','','Restore A Full System Backup')
    addDir('','[COLOR=dodgerblue]Restore Local guisettings file[/COLOR]','url','LocalGUIDialog','mainmenu/maintenance.png','','','Back Up Your Full System')
    
    if os.path.exists(os.path.join(USB,'addons.zip')):   
        addDir('','Restore Your Addons','addons','restore_zip','mainmenu/maintenance.png','','','Restore Your Addons')

    if os.path.exists(os.path.join(USB,'addon_data.zip')):   
        addDir('','Restore Your Addon UserData','addon_data','restore_zip','mainmenu/maintenance.png','','','Restore Your Addon UserData')           

    if os.path.exists(os.path.join(USB,'guisettings.xml')):
        addDir('','Restore Guisettings.xml',GUI,'restore_backup','mainmenu/maintenance.png','','','Restore Your guisettings.xml')
    
    if os.path.exists(os.path.join(USB,'favourites.xml')):
        addDir('','Restore Favourites.xml',FAVS,'restore_backup','mainmenu/maintenance.png','','','Restore Your favourites.xml')
        
    if os.path.exists(os.path.join(USB,'sources.xml')):
        addDir('','Restore Source.xml',SOURCE,'restore_backup','mainmenu/maintenance.png','','','Restore Your sources.xml')
        
    if os.path.exists(os.path.join(USB,'advancedsettings.xml')):
        addDir('','Restore Advancedsettings.xml',ADVANCED,'restore_backup','mainmenu/maintenance.png','','','Restore Your advancedsettings.xml')        

    if os.path.exists(os.path.join(USB,'keyboard.xml')):
        addDir('','Restore Advancedsettings.xml',KEYMAPS,'restore_backup','mainmenu/maintenance.png','','','Restore Your keyboard.xml')
        
    if os.path.exists(os.path.join(USB,'RssFeeds.xml')):
        addDir('','Restore RssFeeds.xml',RSS,'restore_backup','mainmenu/maintenance.png','','','Restore Your RssFeeds.xml')    
#---------------------------------------------------------------------------------------------------
#Function to restore a previously backed up zip, this includes full backup, addons or addon_data.zip
def Restore_Zip_File(url):
    Check_Download_Path()
    if 'addons' in url:
        ZIPFILE    = xbmc.translatePath(os.path.join(USB,'addons.zip'))
        DIR        = ADDONS

    else:
        ZIPFILE = xbmc.translatePath(os.path.join(USB,'addon_data.zip'))
        DIR = ADDON_DATA

    if 'Backup' in name:
        Delete_Packages() 
        dp.create("Creating Backup","Backing Up",'', 'Please Wait')
        zipobj = zipfile.ZipFile(ZIPFILE , 'w', zipfile.ZIP_DEFLATED)
        rootlen = len(DIR)
        for_progress = []
        ITEM =[]
        for base, dirs, files in os.walk(DIR):
            for file in files:
                ITEM.append(file)
        N_ITEM =len(ITEM)
        for base, dirs, files in os.walk(DIR):
            for file in files:
                for_progress.append(file) 
                progress = len(for_progress) / float(N_ITEM) * 100  
                dp.update(int(progress),"Backing Up",'[COLOR yellow]%s[/COLOR]'%file, 'Please Wait')
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
        dialog.ok("Backup Complete", "You Are Now Backed Up", '','')   

    else:
        dp.create("Extracting Zip","Checking ",'', 'Please Wait')
        dp.update(0,"", "Extracting Zip Please Wait")
        extract.all(ZIPFILE,DIR,dp)
        time.sleep(1)
        xbmc.executebuiltin('UpdateLocalAddons ')    
        xbmc.executebuiltin("UpdateAddonRepos")        

        if 'Backup' in name:
            dialog.ok("Install Complete", 'Kodi will now close. Just re-open Kodi and wait for all the updates to complete.')
            Kill_XBMC()

        else:
            dialog.ok("SUCCESS!", "You Are Now Restored", '','')        
#---------------------------------------------------------------------------------------------------
# Basic function to run an add-on
def Run_Addon(url):
    xbmc.executebuiltin('RunAddon(%s)' % url)
#---------------------------------------------------------------------------------------------------
# Search text box (used in keyword search)
def SEARCH(title):
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, title)
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered =  keyboard.getText() .replace(' ','%20')
            if search_entered == None:
                return False          
        return search_entered    
#-----------------------------------------------------------------------------------------------------------------
#Search in description
def Search_Addons(url):
    vq = Get_Keyboard( heading="Search for add-ons" )
# if blank or the user cancelled the keyboard, return
    if ( not vq ): return False, 0

# we need to set the title to our query
    title = urllib.quote_plus(vq)
    url += title
    Grab_Addons(url)
#-----------------------------------------------------------------------------------------------------------------
#Search in description
def Search_Builds(url):
    vq = Get_Keyboard( heading="Search for content" )

# if blank or the user cancelled the keyboard, return
    if ( not vq ): return False, 0

# we need to set the title to our query
    title = urllib.quote_plus(vq)
    url += title
    Grab_Builds(url)
# Check local file version name and number against db
def Show_Info(url):
    BaseURL      = 'http://noobsandnerds.com/TI/Community_Builds/community_builds.php?id=%s' % (url)
    link         = Open_URL(BaseURL, 5).replace('\n','').replace('\r','')
    namematch    = re.compile('name="(.+?)"').findall(link)
    authormatch  = re.compile('author="(.+?)"').findall(link)
    versionmatch = re.compile('version="(.+?)"').findall(link)
    name         = namematch[0] if (len(namematch) > 0) else ''
    author       = authormatch[0] if (len(authormatch) > 0) else ''
    version      = versionmatch[0] if (len(versionmatch) > 0) else ''
    dialog.ok(name,'Author: [COLOR=dodgerblue]'+author+ '[/COLOR]      Latest Version: [COLOR=dodgerblue]'+version+'[/COLOR]','','Click OK to view the build page.')
    try:
        Community_Menu(url+'&visibility=homepage',url)
    except:
        return
        xbmc.log("### Could not find build No. %s" % url)
        dialog.ok('Build Not Found','Sorry we couldn\'t find the build, it may be it\'s marked as private or servers may be busy. Please try manually searching via the Community Builds section')
#---------------------------------------------------------------------------------------------------
# Check local file version name and number against db
def Show_Info2(url):
    dialog.ok("This build is not complete",'The guisettings.xml file was not copied over during the last install process. Click OK to go to the build page and complete Install Step 2 (guisettings fix).')

    try:
        Community_Menu(url+'&visibility=homepage',url)

    except:
        return
        xbmc.log("### Could not find build No. %s" % url)
        dialog.ok('Build Not Found','Sorry we couldn\'t find the build, it may be it\'s marked as private. Please try manually searching via the Community Builds section')
#--------------------------------------------------------------------#---------------------------------------------------------------------------------------------------#---------------------------------------------------------------------------------------------------
# Show User Info dialog
def Show_User_Info():
    BaseURL       = 'http://noobsandnerds.com/TI/login/login_details.php?user=%s&pass=%s' % (username, password)
    link          = Open_URL(BaseURL, 5).replace('\n','').replace('\r','')
    welcomematch  = re.compile('login_msg="(.+?)"').findall(link)
    welcometext   = welcomematch[0] if (len(welcomematch) > 0) else ''
    postsmatch    = re.compile('posts="(.+?)"').findall(link)
    messagesmatch = re.compile('messages="(.+?)"').findall(link)
    unreadmatch   = re.compile('unread="(.+?)"').findall(link)
    emailmatch    = re.compile('email="(.+?)"').findall(link)
    messages      = messagesmatch[0] if (len(messagesmatch) > 0) else ''
    unread        = unreadmatch[0] if (len(unreadmatch) > 0) else ''
    email         = emailmatch[0] if (len(emailmatch) > 0) else ''
    posts         = postsmatch[0] if (len(postsmatch) > 0) else ''

    BaseURL = 'http://noobsandnerds.com/TI/menu_check'
    try:
        link      = Open_URL(BaseURL, 10).replace('\n','').replace('\r','')
        menumatch = re.compile('d="(.+?)"').findall(link)
        menu      = menumatch[0] if (len(menumatch) > 0) else 'none'
    except:
        menu = 'none'

    if 'Welcome Back' in welcometext:
        print"### ATTEMPTING TO WRITE COOKIE "
        writefile = open(cookie, mode='w+')
        writefile.write('d="'+binascii.hexlify(Timestamp())+'"\nl="'+binascii.hexlify(welcometext)+'"\np="'+binascii.hexlify(posts)+'"\nm="'+binascii.hexlify(menu)+'"')
        writefile.close()
    if not "Account currently restricted" in welcometext:
        dialog.ok('Account Details','Username:  '+username,'Email: '+email,'Unread Messages: '+unread+'/'+messages+'[CR]Posts: '+posts)
    else:
        dialog.ok('Account Currently Restricted','Your account has a restriction in place, this is usually for account sharing. Any users caught sharing accounts are automatically put on a suspension and continual abuse will result in a permanent ban.')
#-----------------------------------------------------------------------------------------------------------------
# menu to set the sort type when searching
def Sort_By(url,type):
    icon = ICON
    if type == 'communitybuilds':
        icon = 'mainmenu/builds.png'
        redirect = 'grab_builds'
        if url.endswith("visibility=public"):
             addDir('folder','[COLOR=yellow]Manual Search[/COLOR]','&visibility=public','manual_search',icon,'','','')
        if url.endswith("visibility=private"):
             addDir('folder','[COLOR=yellow]Manual Search[/COLOR]','&visibility=private','manual_search',icon,'','','')
    if type == 'addons':
        icon = 'mainmenu/addons.png'
        redirect = 'grab_addons'
        addDir('folder','[COLOR=dodgerblue]Sort by Most Popular[/COLOR]',str(url)+'&sortx=downloads&orderx=DESC',redirect,icon,'','','')
    if type != 'addons':
        addDir('folder','[COLOR=dodgerblue]Sort by Most Popular[/COLOR]',str(url)+'&sortx=downloadcount&orderx=DESC',redirect,icon,'','','')
    else:
        addDir('folder','[COLOR=dodgerblue]Sort by Newest[/COLOR]',str(url)+'&sortx=created&orderx=DESC',redirect,icon,'','','')
        addDir('folder','[COLOR=dodgerblue]Sort by Recently Updated[/COLOR]',str(url)+'&sortx=updated&orderx=DESC',redirect,icon,'','','')
    addDir('folder','[COLOR=dodgerblue]Sort by A-Z[/COLOR]',str(url)+'&sortx=name&orderx=ASC',redirect,icon,'','','')
    if type == 'public_CB':
        addDir('folder','[COLOR=dodgerblue]Sort by Genre[/COLOR]',url,'genres',icon,'','','')
#---------------------------------------------------------------------------------------------------
#Instructions for the speed test
def Speed_Instructions():
    Text_Boxes('Speed Test Instructions', '[COLOR=blue][B]What file should I use: [/B][/COLOR][CR]This function will download a file and will work out your speed based on how long it took to download. You will then be notified of '
    'what quality streams you can expect to stream without buffering. You can choose to download a 10MB, 16MB, 32MB, 64MB or 128MB file to use with the test. Using the larger files will give you a better '
    'indication of how reliable your speeds are but obviously if you have a limited amount of bandwidth allowance you may want to opt for a smaller file.'
    '[CR][CR][COLOR=blue][B]How accurate is this speed test:[/B][/COLOR][CR]Not very accurate at all! As this test is based on downloading a file from a server it\'s reliant on the server not having a go-slow day '
    'but the servers used should be pretty reliable. The 10MB file is hosted on a different server to the others so if you\'re not getting the results expected please try another file. If you have a fast fiber '
    'connection the chances are your speed will show as considerably slower than your real download speed due to the server not being able to send the file as fast as your download speed allows. Essentially the '
    'test results will be limited by the speed of the server but you will at least be able to see if it\'s your connection that\'s causing buffering or if it\'s the host you\'re trying to stream from'
    '[CR][CR][COLOR=blue][B]What is the differnce between Live Streams and Online Video:[/COLOR][/B][CR]When you run the test you\'ll see results based on your speeds and these let you know the quality you should expect to '
    'be able stream with your connection. Live Streams as the title suggests are like traditional TV channels, they are being streamed live so for example if you wanted to watch CNN this would fall into this category. '
    'Online Videos relates to movies, tv shows, youtube clips etc. Basically anything that isn\'t live - if you\'re new to the world of streaming then think of it as On Demand content, this is content that\'s been recorded and stored on the web.'
    '[CR][CR][COLOR=blue][B]Why am I still getting buffering:[/COLOR][/B][CR]The results you get from this test are strictly based on your download speed, there are many other factors that can cause buffering and contrary to popular belief '
    'having a massively fast internet connection will not make any difference to your buffering issues if the server you\'re trying to get the content from is unable to send it fast enough. This can often happen and is usually '
    'down to heavy traffic (too many users accessing the same server). A 10 Mb/s connection should be plenty fast enough for almost all content as it\'s very rare a server can send it any quicker than that.'
    '[CR][CR][COLOR=blue][B]What\'s the difference between MB/s and Mb/s:[/COLOR][/B][CR]A lot of people think the speed they see advertised by their ISP is Megabytes (MB/S) per second - this is not true. Speeds are usually shown as Mb/s '
    'which is Megabit per second - there are 8 of these to a megabyte so if you want to work out how many megabytes per second you\'re getting you need to divide the speed by 8. It may sound sneaky but really it\'s just the unit that has always been used.'
    '[CR][CR]A direct link to the buffering thread explaining what you can do to improve your viewing experience can be found at [COLOR=yellow]http://bit.ly/bufferingfix[/COLOR]'
    '[CR][CR]Thank you, [COLOR=dodgerblue]noobsandnerds[/COLOR] Team.')
#-----------------------------------------------------------------------------------------------------------------
# Speedtest menu
def Speed_Test_Menu():
    addDir('','[COLOR=blue]Instructions - Read me first[/COLOR]', 'none', 'speed_instructions', '','','','')
    addDir('','Download 5MB file', 'http://download.thinkbroadband.com/5MB.zip', 'runtest', '','','','')
    addDir('','Download 10MB file', 'http://download.thinkbroadband.com/10MB.zip', 'runtest', '','','','')
    addDir('','Download 20MB file', 'http://download.thinkbroadband.com/20MB.zip', 'runtest', '','','','')
    addDir('','Download 50MB file', 'http://download.thinkbroadband.com/50MB.zip', 'runtest', '','','','')
    addDir('','Download 100MB file', 'http://download.thinkbroadband.com/100MB.zip', 'runtest', '','','','')
#-----------------------------------------------------------------------------------------------------------------
def Switch_Profile(name):
# Call the function to check if existing profile exists, if no profile exists it will create one.
    dp.create('Creating Profile','','','')
    buildname = Create_Profile(name)

# List pre-installed Kodi addons, we don't need to copy these
    mainaddons = []
    for item in os.listdir(KODI_ADDONS):
        mainaddons.append(item)

# Read contents of the addonslist for switching profile
        profileaddons     = open(os.path.join(CP_PROFILE,name,'addonlist'), mode='r')
        profilelist       = profileaddons.read()
        profileaddons.close()
        profilelist       = profilelist.split('|')

# Move any addons not in the profile list to the Master folder, Create_Addon_Pack makes addons small and we copy them to backup folder.
    Create_Addon_Pack('profiles')
    for item in os.listdir(ADDONS):
        if not item in mainaddons and item != 'plugin.program.totalinstaller' and item != 'repository.noobsandnerds' and item != 'packages':
            try:
                shutil.copytree(os.path.join(addonstemp,'addons',item),os.path.join(CP_PROFILE,'Master','backups',item))
                if debug == 'true':
                    xbmc.log("### Successfully copied %s to %s" % (item, os.path.join(CP_PROFILE,'Master','backups',item)))
            except:
                xbmc.log("### Failed to copy %s to backup folder, must already exist" % item)
            if not item in profilelist and item != skin:
                try:
                    os.rename(os.path.join(ADDONS,item),os.path.join(CP_PROFILE,'Master',item))
                except:
                    try:
                        shutil.copytree(os.path.join(ADDONS,item),os.path.join(CP_PROFILE,'Master',item))
                    except:
                        try:
                            shutil.rmtree(os.path.join(ADDONS,item))
                        except:
                            xbmc.log("### Unable to move %s as it's currently in use" % item)
    shutil.rmtree(addonstemp)
                    
# Move addons in profile list from Master folder to main addons folder.
    for item in profilelist:
        if not item in mainaddons and not item in ADDONS:
            try:
                os.rename(os.path.join(CP_PROFILE,'Master',item),os.path.join(ADDONS,item))
            except:
                pass

    Wipe_Userdata()
    Wipe_Addon_Data()
    Wipe_Home2(EXCLUDES2)
    xbmc.log("### WIPE FUNCTIONS COMPLETE")

# Copy the rest of the data from profile folder to HOME
    try:
        localfile          = open(idfile, mode='r')
        content            = localfile.read()
        localfile.close()
        xbmc.log("### original idfile contents: %s" % content)
    except:
        xbmc.log("### original id file does not exist")

    try:
        extract.all(os.path.join(CP_PROFILE,name,'build.zip'), HOME, dp)
        success = 1
        xbmc.log("### Extraction of build successful")
    except:
        dialog.ok('Error',"Sorry it wasn't possible to extract your build, there is a problem with your build zip file.")
        success = 0
    
# If there is a new id.xml with new profile data we copy it over
    if not os.path.exists(userdatafolder):
        os.makedirs(userdatafolder)
    if os.path.exists(os.path.join(ADDON_DATA,'plugin.program.totalinstaller','id.xml')) and os.path.exists(os.path.join(ADDON_DATA,'ti_id','id.xml')):
        os.remove(idfile)
        xbmc.log('### REMOVED STANDARD id.xml')
    if os.path.exists(os.path.join(ADDON_DATA,'ti_id','id.xml')):
        os.rename(os.path.join(ADDON_DATA,'ti_id','id.xml'), idfile)
    else:
        xbmc.log('### id file does not exist')
    
# If there's a new startup.xml we try and copy that over
    if os.path.exists(startuppath) and os.path.exists(os.path.join(ADDON_DATA,'ti_id','startup.xml')):
        xbmc.log("### startup.xml and temporary startup.xml exists, attempting remove of original and replace with temp")
        os.remove(startuppath)
        xbmc.log("### removal ok")
    if os.path.exists(os.path.join(ADDON_DATA,'ti_id','startup.xml')):
        os.rename(os.path.join(ADDON_DATA,'ti_id','startup.xml'), startuppath)
        xbmc.log("### rename ok")

    if success == 1:
        Kill_XBMC()
#---------------------------------------------------------------------------------------------------
# Menu for switching profiles - includes delete option
def Switch_Profile_Menu(url):
    addDir('folder','[COLOR=darkcyan]DELETE A BUILD[/COLOR]',url,'delete_profile','','','')
    for name in os.listdir(CP_PROFILE):
        if name != 'Master' and name != url.replace(' ','_').replace("'",'').replace(':','-'):
            addDir('','Load Profile: [COLOR=dodgerblue]'+name.replace('_',' ')+'[/COLOR]',name,'switch_profile','','','','')
#---------------------------------------------------------------------------------------------------
# Create a standard text box
def Text_Boxes(heading,anounce):
  class TextBox():
    WINDOW=10147
    CONTROL_LABEL=1
    CONTROL_TEXTBOX=5
    def __init__(self,*args,**kwargs):
      xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, )) # activate the text viewer window
      self.win=xbmcgui.Window(self.WINDOW) # get window
      xbmc.sleep(500) # give window time to initialize
      self.setControls()
    def setControls(self):
      self.win.getControl(self.CONTROL_LABEL).setLabel(heading) # set heading
      try:
        f=open(anounce); text=f.read()
      except:
        text=anounce
      self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
      return
  TextBox()
  while xbmc.getCondVisibility('Window.IsVisible(10147)'):
      xbmc.sleep(500)
#-----------------------------------------------------------------------------------------------------------------
#Show full description of build
def Text_Guide(url):
    try:
        heading,text = url.split('|')
        Text_Boxes(heading, text)
    except:
        Text_Boxes('', url)
#---------------------------------------------------------------------------------------------------
# Get current timestamp in integer format
def Timestamp():
    now = time.time()
    localtime = time.localtime(now)
    return time.strftime('%Y%m%d%H%M%S', localtime)
#-----------------------------------------------------------------------------------------------------------------
# Addon Enable/Disable Toggle
def Toggle_Addon(id, value):
    addonxml = os.path.join(ADDONS, id, 'addon.xml')
    if os.path.exists(addonxml):
        f      = open(addonxml)
        a      = f.read().replace('\n','').replace('\r','').replace('\t','')
        match  = re.compile('<addo.+?id="(.+?)".+?>').findall(a)
        xbmc.log('### ADDON ID TO STOP: %s' % match[0])
        match3 = re.compile('<extension point=.+?ibrary="(.+?)".+?start="').findall(a)
        if len(match3) > 0:
            xbmc.executebuiltin('StopScript(%s)' % match[0])
    query = '{"jsonrpc":"2.0", "method":"Addons.SetAddonEnabled","params":{"addonid":"%s","enabled":%s}, "id":1}' % (match[0], value)
    response = xbmc.executeJSONRPC(query)
    xbmc.log(str(query))
    xbmc.log(str(response))
    if 'error' in response:
        v = 'Enabling' if value == 'true' else 'Disabling'
        dialog.ok("Community Portal", "Error %s [COLOR yellow]%s[/COLOR]" % (v, id), "Check to make sure the addon list is upto date and try again.")
        Update_Repo()
#-----------------------------------------------------------------------------------------------------------------
# Maintenance section
def Tools():
    addDir('folder','Add-on Tools','none','tools_addons','mainmenu/maintenance.png','','','')
    addDir('folder','Backup/Restore','none','backup_restore','mainmenu/maintenance.png','','','')
    addDir('folder','Clean up my Kodi', '', 'tools_clean', 'mainmenu/maintenance.png','','','')
    addDir('folder','Misc. Tools', '', 'tools_misc', 'mainmenu/maintenance.png','','','')
    if OpenELEC_Check():
        addDir('','[COLOR=dodgerblue]Wi-Fi / OpenELEC Settings[/COLOR]','', 'openelec_settings', 'mainmenu/maintenance.png','','','')
#-----------------------------------------------------------------------------------------------------------------
# Add-on based tools
def Tools_Addons():
    addDir('','Completely Remove An Add-on (inc. passwords)','plugin','addon_removal_menu', 'mainmenu/maintenance.png','','','')
    addDir('','Delete Addon Data','url','remove_addon_data','mainmenu/maintenance.png','','','')
    addDir('folder','Enable/Disable Addons', 'true', 'enableaddons', 'mainmenu/maintenance.png','','','')
    addDir('','Make Add-ons Gotham/Helix Compatible','none','gotham', 'mainmenu/maintenance.png','','','')
    addDir('','Make Skins Kodi (Helix) Compatible','none','helix', 'mainmenu/maintenance.png','','','')
    addDir('','Passwords - Hide when typing in','none','hide_passwords', 'mainmenu/maintenance.png','','','')
    addDir('','Passwords - Unhide when typing in','none','unhide_passwords', 'mainmenu/maintenance.png','','','')
    addDir('','Update My Add-ons (Force Refresh)', 'none', 'update', 'mainmenu/maintenance.png','','','')
#-----------------------------------------------------------------------------------------------------------------
# Clean Tools
def Tools_Clean():
    addDir('','[COLOR=gold]CLEAN MY KODI FOLDERS (Save Space)[/COLOR]', '', 'full_clean', 'mainmenu/maintenance.png','','','')
    addDir('','Clear All Cache Folders','url','clear_cache','mainmenu/maintenance.png','','','')
    addDir('','Clear Cached Artwork (thumbnails & textures)', 'none', 'remove_textures', 'mainmenu/maintenance.png','','','')
    addDir('','Clear Packages Folder','url','remove_packages','mainmenu/maintenance.png','','','')
    addDir('','Delete Old Builds/Zips From Device','url','remove_build','mainmenu/maintenance.png','','','')
    addDir('','Delete Old Crash Logs','url','remove_crash_logs','mainmenu/maintenance.png','','','')
    addDir('','Wipe My Install (Fresh Start)', '', 'wipe_xbmc', 'mainmenu/maintenance.png','','','')
#-----------------------------------------------------------------------------------------------------------------
# Advanced Maintenance section
def Tools_Misc():
    builder = Builder_Name()
    addDir('','Check For Special Characters In Filenames','', 'ASCII_Check', 'mainmenu/maintenance.png','','','')
    addDir('folder','Check My Internet Speed', 'none', 'speedtest_menu', 'mainmenu/maintenance.png','','','')
    addDir('','Check My IP Address', 'none', 'ipcheck', 'mainmenu/maintenance.png','','','')
    addDir('','Check XBMC/Kodi Version', 'none', 'xbmcversion', 'mainmenu/maintenance.png','','','')
    addDir('','Convert Physical Paths To Special',HOME,'fix_special','mainmenu/maintenance.png','','','')
    addDir('','Force Close Kodi','url','kill_xbmc','mainmenu/maintenance.png','','','')
    if username.replace('%20', ' ') in builder and username != '':
        addDir('','Remove Community Build Protection','none','remove_nag', 'mainmenu/maintenance.png','','','')
    addDir('','Upload Log','none','uploadlog', 'mainmenu/maintenance.png','','','')
    addDir('','View My Log','none','log', 'mainmenu/maintenance.png','','','')
    addDir('','XXX - Hide my adult add-ons', 'false', 'adult_filter', 'mainmenu/maintenance.png','','','')
    addDir('','XXX - Show my adult add-ons', 'true', 'adult_filter', 'mainmenu/maintenance.png','','','')
#-----------------------------------------------------------------------------------------------------------------
# Unhide passwords in addon settings - THANKS TO MIKEY1234 FOR THIS CODE (taken from Xunity Maintenance)
def Unhide_Passwords():
    dialog = xbmcgui.Dialog()
    if dialog.yesno("Make Add-on Passwords Visible?", "This will make all your add-on passwords visible in the add-on settings. Are you sure you wish to continue?"):
        for root, dirs, files in os.walk(ADDONS):
            for f in files:
                if f =='settings.xml':
                    FILE=open(os.path.join(root, f)).read()
                    match=re.compile('<setting id=(.+?)>').findall (FILE)
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
        dialog.ok("Passwords Are now visible", "Your passwords will now be visible in your add-on settings. If you want to undo this please use the option to hide passwords.") 
#---------------------------------------------------------------------------------------------------
# Function to update the current running build
def Update_Community(name,url,video,description,skins,guisettingslink,artpack):
    dp.create("Backing Up Important Data",'Please wait...','','')

# Get size of guisettings, based on this we will either force close or not
    guicontentsize = open(idfile, mode='r')
    guicontent     = guicontentsize.read()
    guicontentsize.close()
    
    guiorig        = re.compile('gui="(.+?)"').findall(guicontent)
    guiorigsize    = guiorig[0] if (len(guiorig) > 0) else '0'

# Store contents of favourites and sources if enabled in settings, ready for writing over top of new build
    if keepfaves=='true':
        try:
            favescontent = open(FAVS, mode='r')
            favestext = favescontent.read()
            favescontent.close()
        
        except:
            xbmc.log("### No favourites file to copy")
    
    if keepsources=='true':
        try:
            sourcescontent = open(SOURCE, mode='r')
            sourcestext = sourcescontent.read()
            sourcescontent.close()
        
        except:
            xbmc.log("### No sources file to copy")

    choice4=1
    Check_Download_Path()

# Check to see if the new guisettings file exists, if it does overwrite the main guisettings
    if os.path.exists(GUINEW):
        
        if os.path.exists(GUI):
            os.remove(GUINEW)
        
        else:
            os.rename(GUINEW,GUI)

    if os.path.exists(GUIFIX):
        os.remove(GUIFIX)

# Function for debugging, creates a file that was created in previous call and subsequently deleted when run
    if not os.path.exists(tempfile):
        localfile = open(tempfile, mode='w+')
        localfile.close() # Added this, not sure if we need it open as a hack

    dp.close()
    dp.create("Downloading Skin Fix","Downloading guisettings.xml",'', 'Please Wait')
    lib=os.path.join(USB, 'guifix.zip')

# Download guisettings from the build
    try:
        xbmc.log("### attempting to download guisettings.xml")
        downloader.download(guisettingslink, lib, dp)
        dp.close()
    except:
        dialog.ok('Problem Detected','Sorry there was a problem downloading the guisettings file. Please check your storage location, if you\'re certain that\'s ok please notify the build author on the relevant support thread.')
        xbmc.log("### FAILED to download %s" % guisettingslink)

# Check that gui file is a real zip and the uploader hasn't put a bad link in the db
    if zipfile.is_zipfile(lib):
        guisize = str(os.path.getsize(lib))
    
    else:
        guisize = guiorigsize

# Pull the details about the currently downloading build
    localfile = open(tempfile, mode='r')
    content   = localfile.read()
    localfile.close()

    temp         = re.compile('id="(.+?)"').findall(content)
    tempname     = re.compile('name="(.+?)"').findall(content)
    tempversion  = re.compile('version="(.+?)"').findall(content)

    tempcheck    = temp[0] if (len(temp) > 0) else ''
    namecheck    = tempname[0] if (len(tempname) > 0) else ''
    versioncheck = tempversion[0] if (len(tempversion) > 0) else ''

    if os.path.exists(guitemp):
        os.removedirs(guitemp)

# If the guisettings on server are a different size to existing do the following (no need to force close and merge data)
    if guiorigsize!=guisize:
        try:
            os.rename(GUI,GUINEW)
        
        except:
            dialog.ok("NO GUISETTINGS!",'No guisettings.xml file has been found.', 'Please exit Kodi and try again','')
            return
    
# If user chooses to create a backup do a complete backup excluding any unwanted files
    if video != 'fresh':
        choice = xbmcgui.Dialog().yesno(name, 'We highly recommend backing up your existing build before installing any community builds. Would you like to perform a backup first?', nolabel='Backup',yeslabel='Install')
        
        if choice == 0:
            mybackuppath = xbmc.translatePath(os.path.join(USB,'Community_Builds','My_Builds'))
            
            if not os.path.exists(mybackuppath):
                os.makedirs(mybackuppath)
            
            vq = Get_Keyboard( heading="Enter a name for this backup" )
            
            if ( not vq ):
                return False, 0
            
            title              = urllib.quote_plus(vq)
            backup_zip         = xbmc.translatePath(os.path.join(mybackuppath,title+'.zip'))
            exclude_dirs_full  =  ['plugin.program.totalinstaller','plugin.program.tbs']
            exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf','Thumbs.db','.gitignore']
            message_header     = "Creating full backup of existing build"
            message1           = "Archiving..."
            message2           = ""
            message3           = "Please Wait"
            Archive_Tree(HOME, backup_zip, message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)

    writefile = open(idfile, mode='w+')
    
    if guiorigsize!=guisize:
        writefile.write('id="'+str(tempcheck)+'"\nname="'+namecheck+' [COLOR=yellow](Partially installed)[/COLOR]"\nversion="'+versioncheck+'"\ngui="'+guisize+'"')
    
    else:
        writefile.write('id="'+str(tempcheck)+'"\nname="'+namecheck+'"\nversion="'+versioncheck+'"\ngui="'+guisize+'"')
    writefile.close()

# Backup library database if option selected during install process
    if video == 'libprofile' or video == 'library' or video == 'updatelibprofile' or video == 'updatelibrary':
        try:
            shutil.copytree(DATABASE, tempdbpath, symlinks=False, ignore=shutil.ignore_patterns("Textures13.db","Addons16.db","Addons15.db","saltscache.db-wal","saltscache.db-shm","saltscache.db","onechannelcache.db")) #Create temp folder for databases, give user option to overwrite existing library
        
        except:
            choice4 = xbmcgui.Dialog().yesno(name, 'There was an error trying to backup some databases. Continuing may wipe your existing library. Do you wish to continue?', nolabel='No, cancel',yeslabel='Yes, overwrite')
            
            if choice4 == 0:
                return
        
        backup_zip = xbmc.translatePath(os.path.join(USB,'Database.zip'))
        Archive_File(tempdbpath,backup_zip)
    
    if choice4 == 0:
        return
    
    time.sleep(1)

# Create a backup location outside of kodi for addon dependencies so they aren't accidentally wiped and download the build
    tempbackup = xbmc.translatePath(os.path.join(HOME,'..','koditemp.zip'))
    time.sleep(2)
    dp.create("Community Builds","Downloading "+description +" build.",'', 'Please Wait')
    filename = description.replace(' ','_').replace(':','-').replace("'",'')
    lib=os.path.join(CBPATH, filename+'.zip')
    
    if not os.path.exists(CBPATH):
        os.makedirs(CBPATH)
    
    downloader.download(url, lib, dp)

# Read the contents of profiles into memory so we can write back later
    try:
        readfile2        = open(PROFILES, mode='r')
        profile_contents = readfile2.read()
        readfile2.close()
    except:
        xbmc.log("### No profiles detected, most likely a fresh wipe performed")
    
    dp.close()
    dp.create("Community Builds","Checking ",'', 'Please Wait')

# Extract the build
    if zipfile.is_zipfile(lib):
        dp.update(0,"", "Extracting Zip Please Wait")
        extract.all(lib,HOME,dp)
    
    else:
        dialog.ok('Not a valid zip file','This file is not a valid zip file, please let the build author know on their support thread so they can amend the download path. It\'s most likely just a simple typo on their behalf.')
        return

    dp.create("Restoring Dependencies","Checking ",'', 'Please Wait')
    dp.update(0,"", "Extracting Zip Please Wait")
    
    if keepfaves == 'true':
        try:
            xbmc.log("### Attempting to add back favourites ###")
            writefile = open(FAVS, mode='w+')
            writefile.write(favestext)
            writefile.close()
            dp.update(0,"", "Copying Favourites")
        except:
            xbmc.log("### Failed to copy back favourites")
    
    if keepsources == 'true':
        try:
            xbmc.log("### Attempting to add back sources ###")
            writefile = open(SOURCE, mode='w+')
            writefile.write(sourcestext)
            writefile.close()
            dp.update(0,"", "Copying Sources")
        
        except:
            xbmc.log("### Failed to copy back sources")
    
    time.sleep(1)
    if os.path.exists(tempdbpath):
        shutil.rmtree(tempdbpath)

# Update the startup.xml version number so it can check for update on next run of add-on
    if os.path.exists(startuppath):
        localfile = open(startuppath, mode='r')
        content = localfile.read()
        localfile.close()
        localversionmatch = re.compile('version="[\s\S]*?"').findall(content)
        localversioncheck  = localversionmatch[0] if (len(localversionmatch) > 0) else ''
        replacefile = content.replace(localversioncheck,'version="'+versioncheck+'"')
        writefile = open(startuppath, mode='w')
        writefile.write(str(replacefile))
        writefile.close()
    
    else:
        writefile = open(startuppath, mode='w+')
        writefile.write('date="01011001"\nversion="'+versioncheck+'"')
        writefile.close()

# Remove the downloaded build if not set to keep in add-on settings
    if localcopy == 'false':
        os.remove(lib)

# Replace the profiles content with what we stored earlier
    if 'prof' in video:
        try:
            profiletxt = open(PROFILES, mode='w+')
            profiletxt.write(profile_contents)
            profiletxt.close()
        except:
            xbmc.log("### Failed to write existing profile info back into profiles.xml")

# If the user chose to keep their library we extract it from the backup location then delete the old file
    if video == 'library' or video == 'libprofile' or video == 'updatelibprofile' or video == 'updatelibrary':
        extract.all(backup_zip,DATABASE,dp)

# If the initial database backup was successful wipe the backup
        if choice4 !=1:
            shutil.rmtree(tempdbpath)
    try:
        dp.close()
    except:
        pass

# If this is a newer (smaller version of a build) do the install process of the add-ons
    if os.path.exists(backupaddonspath):
        CB_Install_Final(description)
        
        try:
            os.remove(backupaddonspath)
        
        except:
            xbmc.log("###' Failed to remove: %s" % backupaddonspath)
        
        try:
            shutil.rmtree(addonstemp)

        except:
            xbmc.log("###' Failed to remove: %s" % addonstemp)
    
    else:
        xbmc.log("### Community Builds - using an old build")

# If the guisettings downloaded are a different size to existing we need to merge guisettings and force close
    if guiorigsize!=guisize:
        xbmc.log("### GUI SIZE DIFFERENT ATTEMPTING MERGE ###")
        newguifile = os.path.join(HOME,'newbuild')
        
        if not os.path.exists(newguifile):
            os.makedirs(newguifile)
 
        os.makedirs(guitemp)
        time.sleep(1)
        GUI_Merge(guisettingslink,video)
        time.sleep(1)
        Kill_XBMC()
        dialog.ok("Force Close Required", "If you\'re seeing this message it means the force close was unsuccessful. Please close XBMC/Kodi via your operating system or pull the power.")

    if guiorigsize==guisize:
        dialog.ok('Successfully Updated','Congratulations the following build:[COLOR=dodgerblue]',description,'[/COLOR]has been successfully updated!')
#---------------------------------------------------------------------------------------------------
# Option to upload a log
def Upload_Log(): 
    if ADDON.getSetting('email')=='':
        dialog.ok("No Email Address Set", "A new window will Now open for you to enter your Email address. The logfile will be sent here")
        ADDON.openSettings()
    uploadLog.Main()
#---------------------------------------------------------------------------------------------------
# Checks cookie file for post count, users can update by clicking on user info
def User_Details(info):
    if os.path.exists(cookie):
        readfile = open(cookie, 'r')
        content  = readfile.read()
        readfile.close()
        welcomematch  = re.compile('l="(.+?)"').findall(content)
        welcometext   = welcomematch[0] if (len(welcomematch) > 0) else ''
        postmatch     = re.compile('p="(.+?)"').findall(content)
        posts         = postmatch[0] if (len(postmatch) > 0) else '0'
        if posts != '0':
            posts = binascii.unhexlify(posts)
        if welcometext != '':
            welcometext = binascii.unhexlify(welcometext)
        if 'Welcome Back' in welcometext and username.replace('%20', '') in welcometext and info == 'posts':
            return posts
        if 'Welcome Back' in welcometext and username.replace('%20', '') in welcometext and info == 'welcometext':
            return welcometext
        else:
            return 'False'
    else:
        return 'False'
#-----------------------------------------------------------------------------------------------------------------    
# Grab User Info
def User_Info(localbuildcheck,localversioncheck,localidcheck):
    print"### USER_INFO CHECK"
    if login == 'true':
        try:
            BaseURL   = 'http://noobsandnerds.com/TI/login/login_details.php?user=%s&pass=%s' % (username, password)
            link          = Open_URL(BaseURL, 10).replace('\n','').replace('\r','')
            welcomematch  = re.compile('login_msg="(.+?)"').findall(link)
            welcometext   = welcomematch[0] if (len(welcomematch) > 0) else ''
            postmatch     = re.compile('posts="(.+?)"').findall(link)
            posts         = postmatch[0] if (len(postmatch) > 0) else '0'
        except:
            welcometext   = '[COLOR=lime]UNABLE TO VERIFY LOGIN[/COLOR]'

    else:
        welcometext  = '[COLOR=lime]REGISTER FOR FREE TO UNLOCK FEATURES[/COLOR]'

    print"### WELCOMETEXT: "+welcometext

    BaseURL = 'http://noobsandnerds.com/TI/menu_check'
    try:
        link      = Open_URL(BaseURL, 10).replace('\n','').replace('\r','')
        menumatch = re.compile('d="(.+?)"').findall(link)
        menu      = menumatch[0] if (len(menumatch) > 0) else 'none'
    except:
        menu = 'none'

    print"### MENU: "+menu
        
# Only create a cookie if successful login otherwise they won't ever be able to login    
    if not 'REGISTER FOR FREE' in welcometext and not 'UNABLE TO VERIFY' in welcometext:
        xbmc.log("### ATTEMPTING TO WRITE COOKIE ")
        writefile = open(cookie, mode='w+')
        writefile.write('d="'+binascii.hexlify(Timestamp())+'"\nl="'+binascii.hexlify(welcometext)+'"\np="'+binascii.hexlify(posts)+'"\nm="'+binascii.hexlify(menu)+'"')
        writefile.close()

    Categories(localbuildcheck,localversioncheck,localidcheck,welcometext,menu)
#-----------------------------------------------------------------------------------------------------------------
# Simple function to force refresh the repo's and addons folder
def Update_Repo(showdialog = True):
    xbmc.executebuiltin('UpdateLocalAddons')
    xbmc.executebuiltin('UpdateAddonRepos')
    if showdialog:
        xbmcgui.Dialog().ok('Force Refresh Started Successfully', 'Depending on the speed of your device it could take a few minutes for the update to take effect.')
#-----------------------------------------------------------------------------------------------------------------
# Check to see if we can ping google.com or google.cn
def Connectivity_Check():
    internetcheck = 1
    try:
        Open_URL('http://google.com', 5)
    except:
        try:
            Open_URL('http://google.com', 5)
        except:
            try:
                Open_URL('http://google.com', 5)
            except:
                try:
                    Open_URL('http://google.cn', 5)
                except:
                    try:
                        Open_URL('http://google.cn', 5)
                    except:
                        dialog.ok("NO INTERNET CONNECTION",'It looks like this device isn\'t connected to the internet. Only some of the maintenance options will work until you fix the connectivity problem.')
                        Categories('','','','[COLOR=orange]NO INTERNET CONNECTION[/COLOR]')
                        internetcheck=0
    if internetcheck==1:
        Video_Check()
#-----------------------------------------------------------------------------------------------------------------
# Initial online check for new video
def Video_Check():
    localbuildcheck   = 'None'
    localidcheck      = '0'

#Read the contents of startup.xml
    localfile           = open(startuppath, mode='r')
    content             = localfile.read()
    localfile.close()
    
    localdatecheckmatch = re.compile('date="(.+?)"').findall(content)
    localdatecheck      = localdatecheckmatch[0] if (len(localdatecheckmatch) > 0) else ''
    localversionmatch   = re.compile('version="(.+?)"').findall(content)
    localversioncheck   = localversionmatch[0] if (len(localversionmatch) > 0) else ''

    localfile2          = open(idfile, mode='r')
    content2            = localfile2.read()
    localfile2.close()
    
    localidmatch        = re.compile('id="(.+?)"').findall(content2)
    localbuildmatch     = re.compile('name="(.+?)"').findall(content2)
    localidcheck        = localidmatch[0] if (len(localidmatch) > 0) else 'None'
    localbuildcheck     = localbuildmatch[0] if (len(localbuildmatch) > 0) else ''

    if not os.path.exists(cookie):
        xbmc.log("### First login check ###")
        User_Info(localbuildcheck,localversioncheck,localidcheck)

# Check local cookie file, if 2 days old do online check for user info
    else:
        try:
            localfile3          = open(cookie, mode='r')
            content3            = localfile3.read()
            localfile3.close()
    
            userdatematch       = re.compile('d="(.+?)"').findall(content3)
            loginmatch          = re.compile('l="(.+?)"').findall(content3)
            livemsgmatch        = re.compile('m="(.+?)"').findall(content3)
            updatecheck         = userdatematch[0] if (len(userdatematch) > 0) else '0'
    
            if updatecheck != '0':
                updatecheck     = binascii.unhexlify(updatecheck)

            welcometext         = loginmatch[0] if (len(loginmatch) > 0) else ''
            welcometext         = binascii.unhexlify(welcometext)
            livemsg             = livemsgmatch[0] if (len(livemsgmatch) > 0) else ''
            livemsg             = binascii.unhexlify(livemsg)
        except:
            os.remove(cookie)
        if int(updatecheck)+2000000 > int(Timestamp()):
            xbmc.log("### Login successful ###")
            Categories(localbuildcheck,localversioncheck,localidcheck,welcometext,livemsg)
        else:
            xbmc.log("### Checking login ###")
            User_Info(localbuildcheck,localversioncheck,localidcheck)
#-----------------------------------------------------------------------------------------------------------------    
# Thanks to Mikey1234 for some of these paths and also lambda for the clear cache option in genesis.
def Wipe_Cache():
    PROFILE_ADDON_DATA = os.path.join(xbmc.translatePath(os.path.join('special://profile','addon_data')))

    cachelist = [
        (PROFILE_ADDON_DATA),
        (ADDON_DATA),
        (os.path.join(HOME,'cache')),
        (os.path.join(HOME,'temp')),
        (os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')),
        (os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Localuseraccountnamental')),
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
                            print"### Successfully cleared "+str(file_count)+" files from "+os.path.join(item,d)
                        except:
                            print"### Failed to wipe cache in: "+os.path.join(item,d)
        else:
            for root, dirs, files in os.walk(item):
                for d in dirs:
                    if 'Cache' in d or 'cache' in d or 'CACHE' in d:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                            print"### Successfully wiped "+os.path.join(item,d)
                        except:
                            print"### Failed to wipe cache in: "+os.path.join(item,d)

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
#-----------------------------------------------------------------------------------------------------------------
# Function to clear the addon_data
def Wipe_Kodi(mode):
    if zip == '':
        dialog.ok('Please set your backup location before proceeding','You have not set your backup storage folder.\nPlease update the addon settings and try again.')
        ADDON.openSettings(sys.argv[0])
        zip2 = ADDON.getSetting('zip')
        if zip2 == '':
            Wipe_Kodi(mode)
    mybackuppath = xbmc.translatePath(os.path.join(USB,'Community_Builds','My_Builds'))
    if not os.path.exists(mybackuppath):
        os.makedirs(mybackuppath)
    choice = xbmcgui.Dialog().yesno("ABSOLUTELY CERTAIN?!!!", 'Are you absolutely certain you want to wipe?', '', 'All addons and settings will be completely wiped!', yeslabel='Yes',nolabel='No')
# Check Confluence is running before doing a wipe
    if choice == 1:
        skin = xbmc.getSkinDir()
        xbmc.log('### skin: %s' % skin)
        if not skin in ['skin.confluence', 'skin.estuary']:
            skin = 'skin.confluence' if kodiv < 17 else 'skin.estuary'
            skinSwitch.swapSkins(skin)
            x = 0
            xbmc.sleep(1000)
            while not xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
                if x == 150:
                    break
                x += 1
                xbmc.sleep(200)
                
            if xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
                xbmc.executebuiltin('SetFocus(11)')
                xbmc.executebuiltin('Action(Select)')
        if not skin in ['skin.confluence', 'skin.estuary']:
            dialog.ok("Community Portal", "Unable to reset skin back to [COLOR yellow]%s[/COLOR]" % skin[5:])
            return
        else:
#Give the option to do a full backup before wiping
            choice = xbmcgui.Dialog().yesno("VERY IMPORTANT", 'This will completely wipe your install.', 'Would you like to create a backup before proceeding?', '', yeslabel='No', nolabel='Yes')
            if choice == 0:
                if not os.path.exists(mybackuppath):
                    os.makedirs(mybackuppath)
                vq = Get_Keyboard( heading="Enter a name for this backup" )
                if ( not vq ): return False, 0
                title = urllib.quote_plus(vq)
                backup_zip = xbmc.translatePath(os.path.join(mybackuppath,title+'.zip'))
                exclude_dirs_full =  ['plugin.program.totalinstaller','plugin.program.tbs']
                exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf','.gitignore']
                message_header = "Creating full backup of existing build"
                message1 = "Archiving..."
                message2 = ""
                message3 = "Please Wait"
                Archive_Tree(HOME, backup_zip, message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)
            Wipe_Home(EXCLUDES2)
            Wipe_Userdata()
            Wipe_Addons(1)
            Wipe_Addon_Data()
            Wipe_Home2(EXCLUDES)
            if os.path.exists(startuppath):
                os.remove(startuppath)
            if os.path.exists(tempfile):
                os.remove(tempfile)
            if os.path.exists(idfile):
                os.remove(idfile)
        if mode != 'CB':
            Kill_XBMC()
        try:
            os.remove(startuppath)
        except:
            xbmc.log("### Failed to remove startup.xml")
        try:    
            os.remove(idfile)
        except:
            xbmc.log("### Failed to remove id.xml")
    else:
        return
#-----------------------------------------------------------------------------------------------------------------
# For loop to wipe files in special://home but leave ones in EXCLUDES untouched
def Wipe_Home(excludefiles):
    dp.create("Wiping Existing Content",'','Please wait...', '')
    for root, dirs, files in os.walk(HOME,topdown=True):
        dirs[:] = [d for d in dirs if d not in excludefiles]
        for name in files:
            try:                            
                dp.update(0,"Removing [COLOR=yellow]"+name+'[/COLOR]','','Please wait...')
                os.unlink(os.path.join(root, name))
                os.remove(os.path.join(root,name))
                os.rmdir(os.path.join(root,name))
            except:
                pass
#-----------------------------------------------------------------------------------------------------------------
# Remove userdata folder
def Wipe_Userdata():
    userdatadirs=[name for name in os.listdir(USERDATA) if os.path.isdir(os.path.join(USERDATA, name))]
    try:
        for name in userdatadirs:
            try:
                if name not in EXCLUDES:
                    dp.update(0,"Cleaning Directory: [COLOR=yellow]"+name+' [/COLOR]','','Please wait...')
                    shutil.rmtree(os.path.join(USERDATA,name))
            except:
                pass
    except:
        pass

# Clean up userdata and leave items untouched that were set in addon settings
    for root, dirs, files in os.walk(USERDATA,topdown=True):
       dirs[:] = [d for d in dirs if d not in EXCLUDES]
       for name in files:
           try:                            
               dp.update(0,"Removing [COLOR=yellow]"+name+'[/COLOR]','','Please wait...')
               os.unlink(os.path.join(root, name))
               os.remove(os.path.join(root,name))
           except:
               pass
#-----------------------------------------------------------------------------------------------------------------
# Remove addon directories
def Wipe_Addons(keeprepos):
    for name in os.listdir(ADDONS):
        if not keeprepos:
            if name not in EXCLUDES and not 'repo' in name:
                try:
                    dp.update(0,"Removing Add-on: [COLOR=yellow]"+name+' [/COLOR]','','Please wait...')
                    shutil.rmtree(os.path.join(ADDONS,name))
                except:
                    try:
                        os.remove(os.path.join(ADDONS,name))
                    except:
                        pass

        else:
            try:
                if name not in EXCLUDES:
                    dp.update(0,"Removing Add-on: [COLOR=yellow]"+name+' [/COLOR]','','Please wait...')
                    shutil.rmtree(os.path.join(ADDONS,name))
            except:
                try:
                    os.remove(os.path.join(ADDONS,name))
                except:
                    pass
#-----------------------------------------------------------------------------------------------------------------
# Remove addon_data
def Wipe_Addon_Data():
    for name in os.listdir(ADDON_DATA):
        try:
            dp.update(0,"Removing Add-on Data: [COLOR=yellow]"+name+' [/COLOR]','','Please wait...')
            shutil.rmtree(os.path.join(ADDON_DATA,name))
        except:
            try:
                os.remove(os.path.join(ADDON_DATA,name))
            except:
                pass
#-----------------------------------------------------------------------------------------------------------------
# Clean up everything in the home path
def Wipe_Home2(excludefiles):
    homepath=[name for name in os.listdir(HOME) if os.path.isdir(os.path.join(HOME, name))]
    try:
        for name in homepath:
            try:
                if name not in excludefiles:
                    dp.update(0,"Cleaning Directory: [COLOR=yellow]"+name+' [/COLOR]','','Please wait...')
                    shutil.rmtree(os.path.join(HOME,name))
            except:
                pass
    except:
        pass
#-----------------------------------------------------------------------------------------------------------------
# Report back with the version of Kodi installed
def XBMC_Version(url):
    xbmc_version = xbmc.getInfoLabel("System.BuildVersion")
    version      = float(xbmc_version[:4])
    homearray    = HOME.split(os.sep)
    xbmc.log(str(homearray))
    arraylen     = len(homearray)
    koditype     = homearray[arraylen-1]
    if koditype == '':
        koditype = homearray[arraylen-2]
    koditype     = koditype.replace('.','').upper()
    dialog.ok('You are running: %s'%koditype, "Your version is: %s" % version)
#-----------------------------------------------------------------------------------------------------------------
# Addon starts here
if __name__ == '__main__':
    params        = Get_Params()
    addon_id      = None
    artpack       = None
    audioaddons   = None
    author        = None
    buildname     = None
    data_path     = None
    description   = None
    fanart        = None
    forum         = None
    iconimage     = None
    mode          = None
    name          = None
    programaddons = None
    provider_name = None
    repo_id       = None
    repo_link     = None
    skins         = None
    sources       = None
    title         = None
    updated       = None
    url           = None
    version       = None
    video         = None
    videoaddons   = None
    zip_link      = None
    direct        = 'maintenance'

    try:
        addon_id=urllib.unquote_plus(params["addon_id"])
    except:
        pass
    try:
        adult=urllib.unquote_plus(params["adult"])
    except:
        pass
    try:
        artpack=urllib.unquote_plus(params["artpack"])
    except:
        pass
    try:
        audioaddons=urllib.unquote_plus(params["audioaddons"])
    except:
        pass
    try:
        author=urllib.unquote_plus(params["author"])
    except:
        pass
    try:
        buildname=urllib.unquote_plus(params["buildname"])
    except:
        pass
    try:
        data_path=urllib.unquote_plus(params["data_path"])
    except:
        pass
    try:
        description=urllib.unquote_plus(params["description"])
    except:
        pass
    try:
        fanart=urllib.unquote_plus(params["fanart"])
    except:
        pass
    try:
        forum=urllib.unquote_plus(params["forum"])
    except:
        pass
    try:
        guisettingslink=urllib.unquote_plus(params["guisettingslink"])
    except:
        pass
    try:
        iconimage=urllib.unquote_plus(params["iconimage"])
    except:
        pass
    try:
        mode=str(params["mode"])
    except:
        pass
    try:
        name=urllib.unquote_plus(params["name"])
    except:
        pass
    try:
        pictureaddons=urllib.unquote_plus(params["pictureaddons"])
    except:
        pass
    try:
        programaddons=urllib.unquote_plus(params["programaddons"])
    except:
        pass
    try:
        provider_name=urllib.unquote_plus(params["provider_name"])
    except:
        pass
    try:
        repo_link=urllib.unquote_plus(params["repo_link"])
    except:
        pass
    try:
        repo_id=urllib.unquote_plus(params["repo_id"])
    except:
        pass
    try:
        skins=urllib.unquote_plus(params["skins"])
    except:
        pass
    try:
        sources=urllib.unquote_plus(params["sources"])
    except:
        pass
    try:
        title=urllib.unquote_plus(params["title"])
    except:
        pass
    try:
        updated=urllib.unquote_plus(params["updated"])
    except:
        pass
    try:
        url=urllib.unquote_plus(params["url"])
    except:
        pass
    try:
        version=urllib.unquote_plus(params["version"])
    except:
        pass
    try:
        video=urllib.unquote_plus(params["video"])
    except:
        pass
    try:
        videoaddons=urllib.unquote_plus(params["videoaddons"])
    except:
        pass
    try:
        zip_link=urllib.unquote_plus(params["zip_link"])
    except:
        pass

    if not os.path.exists(userdatafolder):
        os.makedirs(userdatafolder)

    if not os.path.exists(startuppath):
        localfile = open(startuppath, mode='w+')
        localfile.write('date="01011001"\nversion="0.0"')
        localfile.close()

    if not os.path.exists(idfile):
        localfile = open(idfile, mode='w+')
        localfile.write('id="None"\nname="None"')
        localfile.contentlose()

    xmlfile = binascii.unhexlify('6164646f6e2e786d6c')
    addonxml = xbmc.translatePath(os.path.join(ADDONS,AddonID,xmlfile))
    localaddonversion = open(addonxml, mode='r')
    content = file.read(localaddonversion)
    file.close(localaddonversion)
    localaddonvermatch = re.compile('<ref>(.+?)</ref>').findall(content)
    addonversion  = localaddonvermatch[0] if (len(localaddonvermatch) > 0) else ''
    localcheck = hashlib.md5(open(installfile,'rb').read()).hexdigest()
    if addonversion != localcheck:
        readfile = open(bakdefault, mode='r')
        content  = file.read(readfile)
        file.close(readfile)
        writefile = open(installfile, mode='w+')
        writefile.write(content)
        writefile.close()

    if mode == None : Video_Check()
    elif mode == 'ASCII_Check'        : ASCII_Check()
    elif mode == 'addon_final_menu'   : Addon_Final_Menu(url)
    elif mode == 'addon_categories'   : Addon_Categories(url)
    elif mode == 'addon_countries'    : Addon_Countries(url)
    elif mode == 'addon_genres'       : Addon_Genres(url)
    elif mode == 'addon_install'      : Addon_Install(name,zip_link,repo_link,repo_id,addon_id,provider_name,forum,data_path)
    elif mode == 'addon_install_zero' : Addon_Install_Zero(name,zip_link,repo_link,repo_id,addon_id,provider_name,forum,data_path)
    elif mode == 'addon_loop'         : CB_Addon_Install_Loop()
    elif mode == 'addon_removal_menu' : Addon_Removal_Menu()
    elif mode == 'addonmenu'          : Addon_Menu(url)
    elif mode == 'addon_settings'     : Addon_Settings()
    elif mode == 'adult_filter'       : Adult_Filter(url)
    elif mode == 'app_installer'      : installapps.INDEX1()
    elif mode == 'backup'             : BACKUP()
    elif mode == 'backup_option'      : Backup_Option()
    elif mode == 'backup_restore'     : Backup_Restore()
    elif mode == 'browse_repos'       : Browse_Repos()
    elif mode == 'CB_Menu'            : CB_Menu(url)
    elif mode == 'check_storage'      : checkPath.check(direct)
    elif mode == 'check_updates'      : Addon_Check_Updates()
    elif mode == 'clear_cache'        : Clear_Cache()
    elif mode == 'create_keyword'     : Create_Addon_Pack(url)
    elif mode == 'community_backup'   : Community_Backup()
    elif mode == 'community_backup_2' : Community_Backup_OLD()
    elif mode == 'community_menu'     : Community_Menu(url,video)        
    elif mode == 'countries'          : Countries(url)
    elif mode == 'description'        : Description(name,url,buildname,author,version,description,updated,skins,videoaddons,audioaddons,programaddons,pictureaddons,sources,adult)
    elif mode == 'delete_path'        : Delete_Path(url)
    elif mode == 'delete_profile'     : Delete_Profile_Menu(url)
    elif mode == 'enableaddons'       : Enable_Addons()
    elif mode == 'fix_special'        : Fix_Special(url)
    elif mode == 'full_backup'        : Full_Backup()
    elif mode == 'full_clean'         : Full_Clean()
    elif mode == 'genres'             : Genres(url)
    elif mode == 'gotham'             : Gotham_Confirm()
    elif mode == 'grab_addons'        : Grab_Addons(url)
    elif mode == 'grab_builds'        : Grab_Builds(url)
    elif mode == 'guisettingsfix'     : GUI_Settings_Fix(url,local)
    elif mode == 'helix'              : Helix_Confirm()
    elif mode == 'hide_passwords'     : Hide_Passwords()
    elif mode == 'ipcheck'            : IP_Check()
    elif mode == 'install_from_zip'   : Install_From_Zip()
    elif mode == 'instructions'       : Instructions()
    elif mode == 'instructions_1'     : Instructions_1()
    elif mode == 'instructions_2'     : Instructions_2()
    elif mode == 'instructions_3'     : Instructions_3()
    elif mode == 'instructions_4'     : Instructions_4()
    elif mode == 'instructions_5'     : Instructions_5()
    elif mode == 'instructions_6'     : Instructions_6()
    elif mode == 'keywords'           : Keyword_Search(url)
    elif mode == 'kill_xbmc'          : Kill_XBMC()
    elif mode == 'kodi_settings'      : Kodi_Settings()
    elif mode == 'local_backup'       : Local_Backup()
    elif mode == 'LocalGUIDialog'     : Local_GUI_Dialog()
    elif mode == 'log'                : Log_Viewer()
    elif mode == 'login_check'        : Connectivity_Check()
    elif mode == 'manual_search'      : Manual_Search(url)
    elif mode == 'nan_menu'           : NaN_Menu()
    elif mode == 'news_root_menu'     : News_Root_Menu(url)
    elif mode == 'news_menu'          : News_Menu(url)
    elif mode == 'open_system_info'   : Open_System_Info()
    elif mode == 'open_filemanager'   : Open_Filemanager()
    elif mode == 'openelec_backup'    : OpenELEC_Backup()
    elif mode == 'openelec_settings'  : OpenELEC_Settings()
    elif mode == 'play_video'         : yt.PlayVideo(url)
    elif mode == 'register'           : Register()
    elif mode == 'remove_addon_data'  : Remove_Addon_Data()
    elif mode == 'remove_addons'      : Remove_Addons(url)
    elif mode == 'remove_build'       : Remove_Build()
    elif mode == 'remove_crash_logs'  : Remove_Crash_Logs()
    elif mode == 'remove_nag'         : Remove_Nag()
    elif mode == 'remove_packages'    : Remove_Packages()
    elif mode == 'remove_textures'    : Remove_Textures_Dialog()
    elif mode == 'restore'            : RESTORE()
    elif mode == 'restore_backup'     : Restore_Backup_XML(name,url,description)
    elif mode == 'restore_community'  : Restore_Community(name,url,video,description,skins,guisettingslink,artpack)        
    elif mode == 'restore_local_CB'   : Restore_Local_Community(url)
    elif mode == 'restore_local_gui'  : Restore_Local_GUI()
    elif mode == 'restore_local_OE'   : Restore_OpenELEC_Local()
    elif mode == 'restore_openelec'   : Restore_OpenELEC(name,url,video)
    elif mode == 'restore_option'     : Restore_Option()
    elif mode == 'restore_zip'        : Restore_Zip_File(url)         
    elif mode == 'run_addon'          : Run_Addon(url)
    elif mode == 'runtest'            : speedtest.runtest(url)
    elif mode == 'search_addons'      : Search_Addons(url)
    elif mode == 'search_builds'      : Search_Builds(url)
    elif mode == 'showinfo'           : Show_Info(url)
    elif mode == 'showinfo2'          : Show_Info2(url)
    elif mode == 'SortBy'             : Sort_By(BuildURL,type)
    elif mode == 'speed_instructions' : Speed_Instructions()
    elif mode == 'speedtest_menu'     : Speed_Test_Menu()
    elif mode == 'switch_profile_menu': Switch_Profile_Menu(url)
    elif mode == 'switch_profile'     : Switch_Profile(url)
    elif mode == 'text_guide'         : Text_Guide(url)
    elif mode == 'toggleaddon'        : addon, state = url.split('[]'); Toggle_Addon(addon, state); xbmc.executebuiltin('Container.Refresh')
    elif mode == 'tools'              : Tools()
    elif mode == 'tools_addons'       : Tools_Addons()
    elif mode == 'tools_clean'        : Tools_Clean()
    elif mode == 'tools_misc'         : Tools_Misc()
    elif mode == 'tutorial_root_menu' : xbmc.executebuiltin('ActivateWindow(Videos, plugin://plugin.video.nantuts, return)')       
    elif mode == 'unhide_passwords'   : Unhide_Passwords()
    elif mode == 'update'             : Update_Repo()
    elif mode == 'update_community'   : Update_Community(name,url,video,description,skins,guisettingslink,artpack)        
    elif mode == 'uploadlog'          : Upload_Log()
    elif mode == 'user_info'          : Show_User_Info()
    elif mode == 'xbmc_menu'          : XBMC_Menu(url)
    elif mode == 'xbmcversion'        : XBMC_Version(url)
    elif mode == 'wipe_xbmc'          : Wipe_Kodi(mode)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))