import urllib, urllib2, re, xbmcplugin, xbmcgui, xbmc, xbmcaddon
import os, sys, time, glob, shutil, datetime, zipfile, ntpath
import subprocess, threading
import yt, downloader, checkPath
import binascii
import hashlib
import speedtest
import extract
try:
    from sqlite3 import dbapi2 as database

except:
    from pysqlite2 import dbapi2 as database

from addon.common.addon import Addon
from addon.common.net import Net

__plugin__  = "Community Portal 4Xbox (BETA)"

######################################################
AddonID='plugin.program.totalinstaller4xbox'
AddonName='Community Portal 4Xbox (BETA)'
######################################################
ADDON            =  xbmcaddon.Addon(id=AddonID)
zip              =  ADDON.getSetting('zip')
localcopy        =  ADDON.getSetting('localcopy')
privatebuilds    =  ADDON.getSetting('private')
keepfaves        =  ADDON.getSetting('favourites')
keepsources      =  ADDON.getSetting('sources')
keeprepos        =  ADDON.getSetting('repositories')
mastercopy       =  ADDON.getSetting('mastercopy')
username         =  ADDON.getSetting('username').replace(' ','%20')
password         =  ADDON.getSetting('password')
versionoverride  =  ADDON.getSetting('versionoverride')
login            =  ADDON.getSetting('login')
addonportal      =  ADDON.getSetting('addonportal')
commbuilds       =  ADDON.getSetting('maintenance')
hardware         =  ADDON.getSetting('hardwareportal')
maintenance      =  ADDON.getSetting('maintenance')
newsportal       =  ADDON.getSetting('latestnews')
showall          =  ADDON.getSetting('showall')
tutorials        =  ADDON.getSetting('tutorialportal')
startupvideo     =  ADDON.getSetting('startupvideo')
startupvideopath =  ADDON.getSetting('startupvideopath')
xbmcdir          =  ADDON.getSetting('xbmcdir')
dialog           =  xbmcgui.Dialog()
dp               =  xbmcgui.DialogProgress()
HOME             =  xbmc.translatePath('special://home/')
USERDATA         =  xbmc.translatePath(os.path.join(HOME,'UserData'))
ADDON_DATA       =  xbmc.translatePath(os.path.join(USERDATA,'plugin_data'))
DATABASE         =  xbmc.translatePath(os.path.join(USERDATA,'Database'))
THUMBNAILS       =  xbmc.translatePath(os.path.join(USERDATA,'Thumbnails'))
ADDONS           =  xbmc.translatePath(os.path.join('special://home','plugins'))
CBADDONPATH      =  xbmc.translatePath(os.path.join(ADDONS,'programs',AddonName,'default.py'))
FANART           =  xbmc.translatePath(os.path.join(ADDONS,'programs',AddonName,'fanart.jpg'))
ADDONXMLTEMP     =  xbmc.translatePath(os.path.join(ADDONS,'programs',AddonName,'resources','addonxml'))
GUI              =  xbmc.translatePath(os.path.join(USERDATA,'guisettings.xml'))
GUIFIX           =  xbmc.translatePath(os.path.join(USERDATA,'guifix.xml'))
ARTPATH          =  'http://www.noobsandnerds.com/TI/artwork/'
defaulticon      =  xbmc.translatePath(os.path.join(ADDONS,'programs',AddonName,'icon_menu.png'))
FAVS             =  xbmc.translatePath(os.path.join(USERDATA,'favourites.xml'))
SOURCE           =  xbmc.translatePath(os.path.join(USERDATA,'sources.xml'))
ADVANCED         =  xbmc.translatePath(os.path.join(USERDATA,'advancedsettings.xml'))
PROFILES         =  xbmc.translatePath(os.path.join(USERDATA,'profiles.xml'))
RSS              =  xbmc.translatePath(os.path.join(USERDATA,'RssFeeds.xml'))
KEYMAPS          =  xbmc.translatePath(os.path.join(USERDATA,'keymaps','keyboard.xml'))
USB              =  xbmc.translatePath(os.path.join(zip))
CBPATH           =  xbmc.translatePath(os.path.join(USB,'Community_Builds',''))
startuppath      =  xbmc.translatePath(os.path.join(ADDON_DATA,'programs',AddonName,'startup.xml'))
tempfile         =  xbmc.translatePath(os.path.join(ADDON_DATA,'programs',AddonName,'temp.xml'))
idfile           =  xbmc.translatePath(os.path.join(ADDON_DATA,'programs',AddonName,'id.xml'))
idfiletemp       =  xbmc.translatePath(os.path.join(ADDON_DATA,'programs',AddonName,'idtemp.xml'))
cookie           =  xbmc.translatePath(os.path.join(ADDON_DATA,'programs',AddonName,'temp'))
notifyart        =  xbmc.translatePath(os.path.join(ADDONS,'programs',AddonName,'resources/'))
installfile      =  xbmc.translatePath(os.path.join(ADDONS,'programs',AddonName,'default.py'))
skin             =  xbmc.getSkinDir()
log_path         =  xbmc.translatePath('special://logpath/')
net              =  Net()
userdatafolder   =  xbmc.translatePath(os.path.join(ADDON_DATA,'programs',AddonName))
GUINEW           =  xbmc.translatePath(os.path.join(userdatafolder,'guinew.xml'))
guitemp          =  xbmc.translatePath(os.path.join(userdatafolder,'guitemp',''))
tempdbpath       =  xbmc.translatePath(os.path.join(USB,'Database'))
packages         =  xbmc.translatePath(os.path.join('special://home','plugins','packages'))
EXCLUDES         =  ['plugin.program.cp4xbox','script.module.addon.common','addons','addon_data','plugin_data','script_data','UserData','sources.xml','favourites.xml']
max_Bps          =  0.0
downloaded_bytes =  0.0
localversioncheck=  '0'
BACKUP_DIRS      =  ['/storage/.kodi','/storage/.cache','/storage/.config','/storage/.ssh']

if not os.path.exists(packages):
    os.makedirs(packages)
#-----------------------------------------------------------------------------------------------------------------    
#Popup class - thanks to whoever codes the help popup in TVAddons Maintenance for this section. Unfortunately there doesn't appear to be any author details in that code so unable to credit by name.
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
#Add a standard directory for the builds. Essentially the same as above but grabs unique artwork from previous call
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
    if 'http' in iconimage:
        
        if len(iconimage) > 0:
            iconimage = iconimage
        else:
            iconimage = defaulticon
    else:

        if len(iconimage) > 0:
#           iconimage = ARTPATH + iconimage
            iconimage = defaulticon
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
def o0oO(type,name,url,mode,iconimage = '',fanart = '',video = '',description = ''):
    if 'addon' not in type:

        if len(iconimage) > 0:
            iconimage = ARTPATH + iconimage
        
        else:
            iconimage = defaulticon

    if 'addon' in type:
        
        if len(iconimage) > 0:
            iconimage = iconimage
        else:
            iconimage = defaulticon
    
    if fanart == '':
        fanart = FANART
    
    u   = sys.argv[0]
    u += "?url="            +urllib.quote_plus(url)
    u += "&mode="           +str(mode)
    u += "&name="           +urllib.quote_plus(name)
    u += "&iconimage="      +urllib.quote_plus(iconimage)
    u += "&fanart="         +urllib.quote_plus(fanart)
    u += "&video="          +urllib.quote_plus(video)
    u += "&description="    +urllib.quote_plus(description)
        
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
#Build Categories Menu
def Addon_Categories(url):
    o0oO('folder','[COLOR=darkcyan]Xbox Skins[/COLOR]','','grab_skins','','','','')
    o0oO('folder','[COLOR=yellow][PLUGIN][/COLOR] Audio',url+'&typex=audio','grab_addons','','','','')
    o0oO('folder','[COLOR=yellow][PLUGIN][/COLOR] Image (Picture)',url+'&typex=image','grab_addons','','','','')
    o0oO('folder','[COLOR=yellow][PLUGIN][/COLOR] Program',url+'&typex=program','grab_addons','','','','')
    o0oO('folder','[COLOR=yellow][PLUGIN][/COLOR] Video',url+'&typex=video','grab_addons','','','','')
    o0oO('folder','[COLOR=lime][SCRAPER][/COLOR] Movies (Used for library scanning)',url+'&typex=movie%20scraper','grab_addons','','','','')
    o0oO('folder','[COLOR=lime][SCRAPER][/COLOR] TV Shows (Used for library scanning)',url+'&typex=tv%20show%20scraper','grab_addons','','','','')
    o0oO('folder','[COLOR=lime][SCRAPER][/COLOR] Music Artists (Used for library scanning)',url+'&typex=artist%20scraper','grab_addons','','','','')
    o0oO('folder','[COLOR=lime][SCRAPER][/COLOR] Music Videos (Used for library scanning)',url+'&typex=music%20video%20scraper','grab_addons','','','','')
    o0oO('folder','[COLOR=orange][SERVICE][/COLOR] All Services',url+'&typex=service','grab_addons','','','','')
    o0oO('folder','[COLOR=orange][SERVICE][/COLOR] Weather Service',url+'&typex=weather','grab_addons','','','','')
    o0oO('folder','[COLOR=dodgerblue][OTHER][/COLOR] Repositories',url+'&typex=repository','grab_addons','','','','')
    o0oO('folder','[COLOR=dodgerblue][OTHER][/COLOR] Scripts (Program Add-ons)',url+'&typex=executable','grab_addons','','','','')
    o0oO('folder','[COLOR=dodgerblue][OTHER][/COLOR] Screensavers',url+'&typex=screensaver','grab_addons','','','','')
    o0oO('folder','[COLOR=dodgerblue][OTHER][/COLOR] Script Modules',url+'&typex=script%20module','grab_addons','','','','')
    o0oO('folder','[COLOR=dodgerblue][OTHER][/COLOR] Subtitles',url+'&typex=subtitles','grab_addons','','','','')
    o0oO('folder','[COLOR=dodgerblue][OTHER][/COLOR] Web Interface',url+'&typex=web%20interface','grab_addons','','','','')
#    o0oO('folder','Lyrics','&typex=lyrics','grab_addons','','','','')
#---------------------------------------------------------------------------------------------------
#Build Countries Menu   
def Addon_Countries(url):
    o0oO('folder','African',url+'&genre=african','grab_addons','','','','')
    o0oO('folder','Arabic',url+'&genre=arabic','grab_addons','','','','')
    o0oO('folder','Asian',url+'&genre=asian','grab_addons','','','','')
    o0oO('folder','Australian',url+'&genre=australian','grab_addons','','','','')
    o0oO('folder','Austrian',url+'&genre=austrian','grab_addons','','','','')
    o0oO('folder','Belgian',url+'&genre=belgian','grab_addons','','','','')
    o0oO('folder','Brazilian',url+'&genre=brazilian','grab_addons','','','','')
    o0oO('folder','Canadian',url+'&genre=canadian','grab_addons','','','','')
    o0oO('folder','Chinese',url+'&genre=chinese','grab_addons','','','','')
    o0oO('folder','Colombian',url+'&genre=columbian','grab_addons','','','','')
    o0oO('folder','Croatian',url+'&genre=croatian','grab_addons','','','','')
    o0oO('folder','Czech',url+'&genre=czech','grab_addons','','','','')
    o0oO('folder','Danish',url+'&genre=danish','grab_addons','','','','')
    o0oO('folder','Dominican',url+'&genre=dominican','grab_addons','','','','')
    o0oO('folder','Dutch',url+'&genre=dutch','grab_addons','','','','')
    o0oO('folder','Egyptian',url+'&genre=egyptian','grab_addons','','','','')
    o0oO('folder','Filipino',url+'&genre=filipino','grab_addons','','','','')
    o0oO('folder','Finnish',url+'&genre=finnish','grab_addons','','','','')
    o0oO('folder','French',url+'&genre=french','grab_addons','','','','')
    o0oO('folder','German',url+'&genre=german','grab_addons','','','','')
    o0oO('folder','Greek',url+'&genre=greek','grab_addons','','','','')
    o0oO('folder','Hebrew',url+'&genre=hebrew','grab_addons','','','','')
    o0oO('folder','Hungarian',url+'&genre=hungarian','grab_addons','','','','')
    o0oO('folder','Icelandic',url+'&genre=icelandic','grab_addons','','','','')
    o0oO('folder','Indian',url+'&genre=indian','grab_addons','','','','')
    o0oO('folder','Irish',url+'&genre=irish','grab_addons','','','','')
    o0oO('folder','Italian',url+'&genre=italian','grab_addons','','','','')
    o0oO('folder','Japanese',url+'&genre=japanese','grab_addons','','','','')
    o0oO('folder','Korean',url+'&genre=korean','grab_addons','','','','')
    o0oO('folder','Lebanese',url+'&genre=lebanese','grab_addons','','','','')
    o0oO('folder','Mongolian',url+'&genre=mongolian','grab_addons','','','','')
    o0oO('folder','Moroccan',url+'&genre=moroccan','grab_addons','','','','')
    o0oO('folder','Nepali',url+'&genre=nepali','grab_addons','','','','')
    o0oO('folder','New Zealand',url+'&genre=newzealand','grab_addons','','','','')
    o0oO('folder','Norwegian',url+'&genre=norwegian','grab_addons','','','','')
    o0oO('folder','Pakistani',url+'&genre=pakistani','grab_addons','','','','')
    o0oO('folder','Polish',url+'&genre=polish','grab_addons','','','','')
    o0oO('folder','Portuguese',url+'&genre=portuguese','grab_addons','','','','')
    o0oO('folder','Romanian',url+'&genre=romanian','grab_addons','','','','')
    o0oO('folder','Russian',url+'&genre=russian','grab_addons','','','','')
    o0oO('folder','Singapore',url+'&genre=singapore','grab_addons','','','','')
    o0oO('folder','Spanish',url+'&genre=spanish','grab_addons','','','','')
    o0oO('folder','Swedish',url+'&genre=swedish','grab_addons','','','','')
    o0oO('folder','Swiss',url+'&genre=swiss','grab_addons','','','','')
    o0oO('folder','Syrian',url+'&genre=syrian','grab_addons','','','','')
    o0oO('folder','Tamil',url+'&genre=tamil','grab_addons','','','','')
    o0oO('folder','Thai',url+'&genre=thai','grab_addons','','','','')
    o0oO('folder','Turkish',url+'&genre=turkish','grab_addons','','','','')
    o0oO('folder','UK',url+'&genre=uk','grab_addons','','','','')
    o0oO('folder','USA',url+'&genre=usa','grab_addons','','','','')
    o0oO('folder','Vietnamese',url+'&genre=vietnamese','grab_addons','','','','')
#---------------------------------------------------------------------------------------------------
# This creates the final menu showing build details, video and install link
def Addon_Final_Menu(url):
    BaseURL                = 'http://noobsandnerds.com/TI/AddonPortal/addondetails.php?id=%s' % (url)
    link                   = Open_URL(BaseURL).replace('\n','').replace('\r','')
#    approvedmatch          = re.compile('approved="(.+?)"').findall(link)
    namematch              = re.compile('name="(.+?)"').findall(link)
    UIDmatch               = re.compile('UID="(.+?)"').findall(link)
    idmatch                = re.compile('id="(.+?)"').findall(link)
    providernamematch      = re.compile('provider_name="(.+?)"').findall(link)
    versionmatch           = re.compile('version="(.+?)"').findall(link)
    createdmatch           = re.compile('created="(.+?)"').findall(link)
    contentmatch           = re.compile('addon_types="(.+?)"').findall(link)
    updatedmatch           = re.compile('updated="(.+?)"').findall(link)
    downloadsmatch         = re.compile('downloads="(.+?)"').findall(link)
    xboxmatch              = re.compile('xbox_compatible="(.+?)"').findall(link)
    descriptionmatch       = re.compile('description="(.+?)"').findall(link)
    devbrokenmatch         = re.compile('devbroke="(.+?)"').findall(link)
    brokenmatch            = re.compile('broken="(.+?)"').findall(link)
    deletedmatch           = re.compile('deleted="(.+?)"').findall(link)
    notesmatch             = re.compile('mainbranch_notes="(.+?)"').findall(link)
    xboxnotesmatch         = re.compile('xbox_notes="(.+?)"').findall(link)
    repourlmatch           = re.compile('repo_url="(.+?)"').findall(link)
    dataurlmatch           = re.compile('data_url="(.+?)"').findall(link)
    zipurlmatch            = re.compile('zip_url="(.+?)"').findall(link)
    genresmatch            = re.compile('genres="(.+?)"').findall(link)
    forummatch             = re.compile('forum="(.+?)"').findall(link)
    repoidmatch            = re.compile('repo_id="(.+?)"').findall(link)
    licensematch           = re.compile('license="(.+?)"').findall(link)
    platformmatch          = re.compile('platform="(.+?)"').findall(link)
    visiblematch           = re.compile('visible="(.+?)"').findall(link)
    repositorymatch        = re.compile('repository="(.+?)"').findall(link)
    weatherservicematch    = re.compile('weather_service="(.+?)"').findall(link)
    skinmatch              = re.compile('skin="(.+?)"').findall(link)
    servicematch           = re.compile('service="(.+?)"').findall(link)
    warningmatch           = re.compile('warning="(.+?)"').findall(link)
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
    name                = namematch[0] if (len(namematch) > 0) else ''
    UID                 = UIDmatch[0] if (len(UIDmatch) > 0) else ''
    addon_id            = idmatch[0] if (len(idmatch) > 0) else ''
    provider_name       = providernamematch[0] if (len(providernamematch) > 0) else ''
    version             = versionmatch[0] if (len(versionmatch) > 0) else ''
    created             = createdmatch[0] if (len(createdmatch) > 0) else ''
    content_types       = contentmatch[0] if (len(contentmatch) > 0) else ''
    updated             = updatedmatch[0] if (len(updatedmatch) > 0) else ''
    downloads           = downloadsmatch[0] if (len(downloadsmatch) > 0) else ''
    xbox                = xboxmatch[0] if (len(xboxmatch) > 0) else ''
    desc                = '[CR][CR][COLOR=dodgerblue]Description: [/COLOR]'+descriptionmatch[0] if (len(descriptionmatch) > 0) else ''
    devbroken           = devbrokenmatch[0] if (len(devbrokenmatch) > 0) else ''
    broken              = brokenmatch[0] if (len(brokenmatch) > 0) else ''
    deleted             = '[CR]'+deletedmatch[0] if (len(deletedmatch) > 0) else ''
    notes               = '[CR][CR][COLOR=dodgerblue]User Notes: [/COLOR]'+notesmatch[0] if (len(notesmatch) > 0) else ''
    xbox_notes          = xboxnotesmatch[0] if (len(xboxnotesmatch) > 0) else ''
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
    repository          = repositorymatch[0] if (len(repositorymatch) > 0) else ''
    service             = servicematch[0] if (len(servicematch) > 0) else ''
    skin                = skinmatch[0] if (len(skinmatch) > 0) else ''
    warning             = warningmatch[0] if (len(warningmatch) > 0) else ''
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

# Set the addon location so we can check if it's already installed
    if 'executable' in content_types:
        addonlocation = os.path.join(HOME,'scripts',name)
    
    elif 'skin' in content_types:
        addonlocation = os.path.join(HOME,'skin',name)

    elif 'video' in content_types:
        addonlocation = os.path.join(HOME,'plugins','video',name)
    
    elif 'audio' in content_types:
        addonlocation = os.path.join(HOME,'plugins','music',name)

    elif 'images' in content_types:
        addonlocation = os.path.join(HOME,'plugins','pictures',name)

    elif 'module' in content_types:
        addonlocation = os.path.join(HOME,'scripts','.modules',addon_id)

    elif 'repository' in content_types:
        addonlocation = xbmc.translatePath(os.path.join(USERDATA,'plugin_data','programs','Addons4Xbox Installer','repositories',addon_id))

# Set the addon status (broken, working etc.)
    if deleted != '':
        brokenfinal  = '[CR][CR][COLOR=dodgerblue]Status: [/COLOR][COLOR=red]This add-on is depreciated, it\'s no longer available.[/COLOR]'
    
    elif broken == '' and devbroken == '' and warning =='':
        brokenfinal  = '[CR][CR][COLOR=dodgerblue]Status: [/COLOR][COLOR=lime]No reported problems[/COLOR]'
    
    elif broken == '' and devbroken == '' and warning !='' and deleted =='':
        brokenfinal  = '[CR][CR][COLOR=dodgerblue]Status: [/COLOR][COLOR=orange]Although there have been no reported problems there may be issues with this add-on, see below.[/COLOR]'
    
    elif broken == '' and devbroken != '':
        brokenfinal  = '[CR][CR][COLOR=dodgerblue]Status: [/COLOR]Marked as broken by the add-on developer.[CR][COLOR=dodgerblue]Developer Comments: [/COLOR]'+devbroken
    
    elif broken != '' and devbroken == '':
        brokenfinal  = '[CR][CR][COLOR=dodgerblue]Status: [/COLOR]Marked as broken by a member of the community at [COLOR=orange]www.noobs[/COLOR][COLOR=dodgerblue]and[/COLOR][COLOR=orange]nerds.com[/COLOR][CR][COLOR=dodgerblue]User Comments: [/COLOR]'+broken
    
    elif broken != '' and devbroken != '':
        brokenfinal  = '[CR][CR][COLOR=dodgerblue]Status: [/COLOR]Marked as broken by both the add-on developer and a member of the community at [COLOR=orange]www.noobs[/COLOR][COLOR=dodgerblue]and[/COLOR][COLOR=orange]nerds.com[/COLOR][CR][COLOR=dodgerblue]Developer Comments: [/COLOR]'+devbroken+'[CR][COLOR=dodgerblue]User Comments: [/COLOR]'+broken

# Create the main description template
    description = str('[COLOR=orange]Name: [/COLOR]'+name+'[COLOR=orange]     Author(s): [/COLOR]'+provider_name+'[COLOR=orange][CR][CR]Version: [/COLOR]'+version+'[COLOR=orange]     Created: [/COLOR]'+created+'[COLOR=orange]     Updated: [/COLOR]'+updated+'[COLOR=orange][CR][CR]Repository: [/COLOR]'+repo_id+platform+'[COLOR=orange]     Add-on Type(s): [/COLOR]'+content_types+requires+brokenfinal+deleted+warning+forum+desc+notes)

# If addon already exists notify or give option to run
    if os.path.exists(addonlocation):
#        if 'script.module' in addon_id or 'repo' in addon_id:
        o0oO('addon','[COLOR=orange]Already installed[/COLOR]','','',icon,'','','')

# Needs some adjustments to work on xbox
#        else:
#            o0oO('','[COLOR=orange]Already installed -[/COLOR] Click here to run the add-on',addonlocation,'run_addon',icon,'','','')

# If server is having a slow day and cannot get the name notify user
    if name =='':
        o0oO('','[COLOR=yellow]Sorry request failed due to high traffic on server, please try again[/COLOR]','','',icon,'','','')

# Show any known issues with addon
    elif name != '':
        
        if (broken == '') and (devbroken =='') and (deleted =='') and (warning ==''):
            o0oO('addon','[COLOR=yellow][FULL DETAILS][/COLOR] No problems reported',description,'text_guide',icon,'','',description)    
        
        if (broken != '' and deleted == '') or (devbroken != '' and deleted == '') or (warning != '' and deleted ==''):
            o0oO('addon','[COLOR=yellow][FULL DETAILS][/COLOR][COLOR=orange] Possbile problems reported[/COLOR]',description,'text_guide',icon,'','',description)            
        
        if deleted != '':
            o0oO('addon','[COLOR=yellow][FULL DETAILS][/COLOR][COLOR=red] Add-on now depreciated[/COLOR]',description,'text_guide',icon,'','',description)            

# If addon isn't deleted show download options
        if deleted =='':
            Add_Install_Dir('[COLOR=lime][INSTALL] [/COLOR]'+name,name+'|'+content_types,'','addon_install',icon,'','',desc,zip_url,repo_url,repo_id,addon_id,provider_name,forumclean,data_url)    

# Show various video links
        if videopreview != 'None':
            o0oO('addon','[COLOR=dodgerblue][VIDEO][/COLOR]  Preview',videoguide1,'play_video',icon,'','','')    
        
        if videoguide1 != 'None':
            o0oO('addon','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel1,videoguide1,'play_video',icon,'','','')    
        
        if videoguide2 != 'None':
            o0oO('addon','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel2,videoguide2,'play_video',icon,'','','')    
        
        if videoguide3 != 'None':
            o0oO('addon','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel3,videoguide3,'play_video',icon,'','','')    
        
        if videoguide4 != 'None':
            o0oO('addon','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel4,videoguide4,'play_video',icon,'','','')    
        
        if videoguide5 != 'None':
            o0oO('addon','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel5,videoguide5,'play_video',icon,'','','')    
        
        if videoguide6 != 'None':
            o0oO('addon','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel6,videoguide6,'play_video',icon,'','','')    
        
        if videoguide7 != 'None':
            o0oO('addon','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel7,videoguide7,'play_video',icon,'','','')    
        
        if videoguide8 != 'None':
            o0oO('addon','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel8,videoguide8,'play_video',icon,'','','')    
        
        if videoguide9 != 'None':
            o0oO('addon','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel9,videoguide9,'play_video',icon,'','','')    
        
        if videoguide10 != 'None':
            o0oO('addon','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel10,videoguide10,'play_video',icon,'','','')    
#---------------------------------------------------------------------------------------------------
#Build Genres Menu
def Addon_Genres(url):
    o0oO('folder','Anime',url+'&genre=anime','grab_addons','','','','')
    o0oO('folder','Audiobooks',url+'&genre=audiobooks','grab_addons','','','','')
    o0oO('folder','Comedy',url+'&genre=comedy','grab_addons','','','','')
    o0oO('folder','Comics',url+'&genre=comics','grab_addons','','','','')
    o0oO('folder','Documentary',url+'&genre=documentary','grab_addons','','','','')
    o0oO('folder','Downloads',url+'&genre=downloads','grab_addons','','','','')
    o0oO('folder','Food',url+'&genre=food','grab_addons','','','','')
    o0oO('folder','Gaming',url+'&genre=gaming','grab_addons','','','','')
    o0oO('folder','Health',url+'&genre=health','grab_addons','','','','')
    o0oO('folder','How To...',url+'&genre=howto','grab_addons','','','','')
    o0oO('folder','Kids',url+'&genre=kids','grab_addons','','','','')
    o0oO('folder','Live TV',url+'&genre=livetv','grab_addons','','','','')
    o0oO('folder','Movies',url+'&genre=movies','grab_addons','','','','')
    o0oO('folder','Music',url+'&genre=music','grab_addons','','','','')
    o0oO('folder','News',url+'&genre=news','grab_addons','','','','')
    o0oO('folder','Photos',url+'&genre=photos','grab_addons','','','','')
    o0oO('folder','Podcasts',url+'&genre=podcasts','grab_addons','','','','')
    o0oO('folder','Radio',url+'&genre=radio','grab_addons','','','','')
    o0oO('folder','Religion',url+'&genre=religion','grab_addons','','','','')
    o0oO('folder','Space',url+'&genre=space','grab_addons','','','','')
    o0oO('folder','Sports',url+'&genre=sports','grab_addons','','','','')
    o0oO('folder','Technology',url+'&genre=tech','grab_addons','','','','')
    o0oO('folder','Trailers',url+'&genre=trailers','grab_addons','','','','')
    o0oO('folder','TV Shows',url+'&genre=tv','grab_addons','','','','')
    o0oO('folder','Misc.',url+'&genre=other','grab_addons','','','','')
    
    if ADDON.getSetting('adult') == 'true':
        o0oO('folder','XXX',url+'&genre=adult','grab_addons','','','','')
#---------------------------------------------------------------------------------------------------
#Step 1 of the addon install process (installs the actual addon)
def Addon_Install(name,zip_link,repo_link,repo_id,addon_id,provider_name,forum,data_path):
    name,content = name.split('|')
    name = name.replace("'",'').replace('"','').replace('[/COLOR]','').replace('[(.+?)]','')
    print"### Name: "+name
    print"### Content: "+content
    print"### Addon ID: "+addon_id
    forum        = str(forum)
    repo_id      = str(repo_id)
    status       = 1
    repostatus   = 1
    modulestatus = 1
        
# Set download path (normally packages on mainbranch so we'll emulate that)
    addondownload = os.path.join(HOME,'plugins','packages',addon_id+'.zip')

# Set where the addon should be installed to, on mainbranch it's the addons folder but we still use old structure from XBMC Dharma
    if 'executable' in content:
        addonlocation = os.path.join(HOME,'scripts',name)
        installdir    = os.path.join(HOME,'scripts')
    
    elif 'skin' in content:
        addonlocation = os.path.join(HOME,'skin',name)
        installdir    = os.path.join(HOME,'skin')

    elif 'video' in content:
        addonlocation = os.path.join(HOME,'plugins','video',name)
        installdir    = os.path.join(HOME,'plugins','video')
    
    elif 'audio' in content:
        addonlocation = os.path.join(HOME,'plugins','music',name)
        installdir    = os.path.join(HOME,'plugins','music')

    elif 'images' in content:
        addonlocation = os.path.join(HOME,'plugins','pictures',name)
        installdir    = os.path.join(HOME,'plugins','pictures')

    elif 'module' in content:
        addonlocation = os.path.join(HOME,'scripts','.modules',addon_id)
        installdir    = os.path.join(HOME,'scripts','.modules')

    elif 'repository' in content:
        addonlocation = xbmc.translatePath(os.path.join(USERDATA,'plugin_data','programs','Addons4Xbox Installer','repositories',addon_id))
        installdir    = xbmc.translatePath(os.path.join(USERDATA,'plugin_data','programs','Addons4Xbox Installer','repositories'))

# Check if addon already exists
    contprocess = 1
    if os.path.exists(addonlocation):
        addonexists = 1
        print"### Addon Exists"
        choice = dialog.yesno('Add-on already exists','Do you want to delete the existing addon and reinstall?','There is no recovering this old addon once deleted!')
        if choice == 1:
            shutil.rmtree(addonlocation)
        else:
            contprocess = 0
    else:
        addonexists = 0
        print"### Addon does not exist"

# Try installing from zip - presuming the dev has it in a repo
    if contprocess == 1 or addonexists == 0:
        dp.create("Installing Addon","Please wait while your addon is installed",'', '')
        print"Download Path: "+addondownload
        try:
            print"### repo_link: "+repo_link
            downloader.download(repo_link,addondownload,dp)
            print"### SUCCESSFULLY DOWNLOADED: "+repo_link
            extract.all(addondownload, installdir, dp)
        except:

# Try installing from standalone zip (not in a repo or in a poorly laid out repo)
            try:
                print"### zip_link: "+zip_link
                downloader.download(zip_link, addondownload, dp)
                print"### SUCCESSFULLY DOWNLOADED: "+zip_link
                extract.all(addondownload, installdir, dp)
            except:

# Finally try installing as single files from the web
                try:
                    print"### install dir: "+installdir
                    if not os.path.exists(installdir):
                        os.makedirs(installdir)

                    link  = Open_URL(data_path).replace('\n','').replace('\r','')
                    match = re.compile('href="(.+?)"', re.DOTALL).findall(link)
                    
                    for href in match:
                        filepath=xbmc.translatePath(os.path.join(installdir,href))
                        
                        if addon_id not in href and '/' not in href:
                            
                            try:
                                dp.update(0,"Downloading "+href,'','Please wait...')
                                downloader.download(data_path+href, filepath, dp)
                            except:
                                print"failed to install"+href

                        if '/' in href and '..' not in href and 'http' not in href:
                            remote_path = data_path+href
                            Recursive_Loop(filepath,remote_path)
                
                except:
                    dialog.ok("Error downloading add-on", 'There was an error downloading '+name,'Please consider updating the add-on portal with details or','report the error on the forum at www.noobsandnerds.com') 
                    status=0

# If successfully installed rename the icon.png to default.tbn                  
        if status==1:
            try:
                os.rename(os.path.join(installdir,addon_id,'icon.png'), os.path.join(installdir,addon_id,'default.tbn'))
            except:
                print"### unable to rename icon.png"

# If it's not a module rename the folder from the addon ID to the user friendly name
            if not 'module' in content:
                try:
                    os.rename(os.path.join(installdir,addon_id), addonlocation)
                except: print"### Unable to rename addon ID "+addon_id+" to "+name
            time.sleep(1)
            dp.update(0,name+' Successfully Installed','','Now installing repository')
            time.sleep(1)
            repopath = xbmc.translatePath(os.path.join(USERDATA,'plugin_data','programs','Addons4Xbox Installer','repositories',repo_id))
            
            if (repo_id != 'repository.xbmc.org') and not (os.path.exists(repopath)) and (repo_id != ''):
                Install_Repo(repo_id)
            
            xbmc.sleep(2000)

# if it's a fresh install of an addon add to the increment count            
            if os.path.exists(addonlocation) and addonexists == 0:
                try:
                    incremental = 'http://noobsandnerds.com/TI/AddonPortal/downloadcount.php?id=%s' % (addon_id)
                    Open_URL(incremental)
                except: pass

# Install any dependencies required
            Dependency_Install(name,addon_id,addonlocation)
            
            if repostatus == 0:
                dialog.ok(name+" Install Complete",'The add-on has been successfully installed but','there was an error installing the repository.','')
            
            if modulestatus == 0:
                dialog.ok(name+" Install Complete",'The add-on has been successfully installed but','there was an error installing modules.','This could result in errors with the add-on.')
            
            if modulestatus != 0 and repostatus != 0 and forum != 'None':
                dialog.ok(name+" Install Complete",'Please support the developer(s) '+provider_name,'Support for this add-on can be found at '+forum,'[CR]Visit www.noobsandnerds.com for all your XBMC needs.')
            
            if modulestatus != 0 and repostatus != 0 and forum == 'None':
                dialog.ok(name+" Install Complete",'Please support the developer(s) '+provider_name,'No details of forum support have been given.')
        
        xbmc.executebuiltin('Container.Refresh')         
#---------------------------------------------------------------------------------------------------
#Addons section
def Addon_Menu():
    o0oO('folder','[COLOR=gold][TOP 100][/COLOR] Show the most downloaded add-ons','popular','grab_addons','','','','')
    o0oO('folder','[COLOR=lime][Manual Search][/COLOR] Type in author/name/content','desc=','search_addons','','','','')
    o0oO('folder','[COLOR=dodgerblue][Filter Results][/COLOR] By Xbox Skins','','grab_skins','','','','')
    o0oO('folder','[COLOR=dodgerblue][Filter Results][/COLOR] By Genres', 'p', 'addon_genres', '','','','')
    o0oO('folder','[COLOR=dodgerblue][Filter Results][/COLOR] By Countries', 'p', 'addon_countries', '','','','')
    o0oO('folder','[COLOR=dodgerblue][Filter Results][/COLOR] By XBMC Categories', 'p', 'addon_categories', '','','','')
#---------------------------------------------------------------------------------------------------
#Function to open addon settings
def Addon_Settings():
    ADDON.openSettings()
    xbmc.executebuiltin('Container.Refresh')
#-----------------------------------------------------------------------------------------------------------------
#Zip up tree
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
                
                if not AddonName in dirs:
                    
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
#Zip up tree - think we can get rid of this and edit the two calls to use Archive_Tree instead. Leaving it here for now though.
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
                
                if not AddonName in dirs:
                   
                   import time
                   FORCE= '01/01/1980'
                   FILE_DATE=time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(fn)))
                   
                   if FILE_DATE > FORCE:
                       zipobj.write(fn, fn[rootlen:])  
    zipobj.close()
    dp.close()
#---------------------------------------------------------------------------------------------------
#Create backup menu
def Backup_Option():
    o0oO('','[COLOR=orange][INSTRUCTIONS][/COLOR] How to create and share my build','','instructions_1','','','','Back Up Your Full System')
    o0oO('','[COLOR=dodgerblue]Create My Own Universal Build[/COLOR] (For copying to other devices)','none','community_backup_2','','','','')
    o0oO('','[COLOR=dodgerblue]Create My Own Full Backup[/COLOR] (will only work on THIS device)','local','local_backup','','','','Back Up Your Full System')
    o0oO('','Backup Addons Only','addons','restore_zip','','','','Back Up Your Addons')
    o0oO('','Backup Addon Data Only','addon_data','restore_zip','','','','Back Up Your Addon Userdata')
    o0oO('','Backup Guisettings.xml',GUI,'restore_backup','','','','Back Up Your guisettings.xml')
    
    if os.path.exists(FAVS):
        o0oO('','Backup Favourites.xml',FAVS,'restore_backup','','','','Back Up Your favourites.xml')
    
    if os.path.exists(SOURCE):
        o0oO('','Backup Source.xml',SOURCE,'restore_backup','','','','Back Up Your sources.xml')
    
    if os.path.exists(ADVANCED):
        o0oO('','Backup Advancedsettings.xml',ADVANCED,'restore_backup','','','','Back Up Your advancedsettings.xml')
    
    if os.path.exists(KEYMAPS):
        o0oO('','Backup Advancedsettings.xml',KEYMAPS,'restore_backup','','','','Back Up Your keyboard.xml')
    
    if os.path.exists(RSS):
        o0oO('','Backup RssFeeds.xml',RSS,'restore_backup','','','','Back Up Your RssFeeds.xml')
#---------------------------------------------------------------------------------------------------
#Backup/Restore root menu
def Backup_Restore():
    o0oO('folder','Backup My Content','none','backup_option','','','','')
    o0oO('folder','Restore My Content','none','restore_option','','','','')
#---------------------------------------------------------------------------------------------------
#Main category list
def Categories(localbuildcheck,localversioncheck,id,welcometext):
    menuitem = Check_New_Menu()
    if menuitem != 'none':
        try:
            exec menuitem
            o0oO('','[COLOR=orange]---------------------------------------[/COLOR]','None','','','','','')
        except: pass
    if (username.replace('%20',' ') in welcometext) and ('elc' in welcometext):
        o0oO('',welcometext,'show','user_info','','','','')
        
        if id != 'None':
            
            if id != 'Local':
                updatecheck = Check_For_Update(localbuildcheck,localversioncheck,id)
                
                if updatecheck == True:
                    
                    if not 'Partially installed' in localbuildcheck:
                        o0oO('folder','[COLOR=dodgerblue]'+localbuildcheck+':[/COLOR] [COLOR=lime]NEW VERSION AVAILABLE[/COLOR]',id,'showinfo','','','','')
                    
                    if '(Partially installed)' in localbuildcheck:
                        o0oO('folder','[COLOR=lime]Current Build Installed: [/COLOR][COLOR=dodgerblue]'+localbuildcheck+'[/COLOR]',id,'showinfo2','','','','')
                else:
                    o0oO('folder','[COLOR=lime]Current Build Installed: [/COLOR][COLOR=dodgerblue]'+localbuildcheck+'[/COLOR]',id,'showinfo','','','','')
            
            else:
                
                if localbuildcheck == 'Incomplete':
                    o0oO('','[COLOR=lime]Your last restore is not yet completed[/COLOR]','url',Check_Local_Install(),'','','','')
                
                else:
                    o0oO('','[COLOR=lime]Current Build Installed: [/COLOR][COLOR=dodgerblue]Local Build ('+localbuildcheck+')[/COLOR]','','','','','','')
        o0oO('','[COLOR=orange]---------------------------------------[/COLOR]','None','','','','','')
    
    if username != '' and password !='' and not 'elc' in welcometext:
        o0oO('','[COLOR=lime]Unable to login, please check your details[/COLOR]','None','addon_settings','','','','')   
    
    if not 'elc' in welcometext:
        o0oO('',welcometext,'None','register','','','','')
    o0oO('','[COLOR=yellow]Settings[/COLOR]','settings','addon_settings','','','','')
    
    o0oO('folder','Addon Portal',welcometext,'addonmenu', '','','','')

#    if hardware == 'true':
#        o0oO('folder','Hardware Reviews', 'none', 'hardware_root_menu', '','','','')
    
#    if newsportal == 'true':
#        o0oO('folder','Latest News', 'none', 'news_root_menu', '','','','')
    
    if tutorials == 'true':
        o0oO('folder','Tutorials','', 'tutorial_root_menu', '','','','')
    
    if maintenance == 'true':
        o0oO('folder','Maintenance','none', 'tools', '','','','')
#---------------------------------------------------------------------------------------------------
# Disclaimer popup prior to opening the main CB menu. Means user has to click to proceed and also fixes issue with popup keep opening during backup
def CB_Root_Menu(welcometext):
    pop('disclaimer.xml')
    if trcheck=='true':
        o0oO('folder','I have read and understand the disclaimer.',welcometext,'CB_Menu','','','','')        
    else:
        o0oO('folder','I have read and understand the disclaimer.','welcome','CB_Menu','','','','')        
#-----------------------------------------------------------------------------------------------------------------
#Build the root search menu for installing community builds    
def CB_Menu(welcometext):
    xbmc_version = xbmc.getInfoLabel("System.BuildVersion")
    versionfloat = float(xbmc_version[:2])
    version      = int(versionfloat)
    print"#### Welcome: "+welcometext    
    if not 'elc' in welcometext:
        o0oO('','[COLOR=orange]To access community builds you must be logged in[/COLOR]','settings','addon_settings','','','','Register at [COLOR=orange]noobs[/COLOR][COLOR=dodgerblue]and[/COLOR][COLOR=orange]nerds[/COLOR]')
    
    if privatebuilds=='true':
        o0oO('folder','[COLOR=dodgerblue]Show My Private List[/COLOR]','&visibility=private','grab_builds','','','','')        
    
    if ((username.replace('%20',' ') in welcometext) and ('elc' in welcometext)):
        o0oO('folder','[COLOR=dodgerblue]Show All XBMC4Xbox Builds[/COLOR]','&xbmc=XBMC4Xbox&visibility=public','grab_builds','','','','')
    o0oO('folder','Create My Own Community Build','url','backup_option','','','','Back Up Your Full System')
#---------------------------------------------------------------------------------------------------
#Function to restore a zip file 
def Check_Download_Path():
    path = xbmc.translatePath(os.path.join(zip,'testCBFolder'))
    
    if not os.path.exists(zip):
        dialog.ok('Download/Storage Path Check','The download location you have stored does not exist .\nPlease update the addon settings and try again.') 
        ADDON.openSettings(sys.argv[0])
#---------------------------------------------------------------------------------------------------
#Check to see if a new version of a build is available
def Check_New_Menu():
    BaseURL = 'http://noobsandnerds.com/TI/menu_check'
    link    = Open_URL(BaseURL).replace('\n','').replace('\r','')
    menumatch = re.compile('d="(.+?)"').findall(link)
    menu  = menumatch[0] if (len(menumatch) > 0) else ''
    if menu != '':
        return menu
    else:
        return "none"
#---------------------------------------------------------------------------------------------------
#Check to see if a new version of a build is available
def Check_For_Update(localbuildcheck,localversioncheck,id):
    BaseURL = 'http://noobsandnerds.com/TI/Community_Builds/buildupdate.php?id=%s' % (id)
    link    = Open_URL(BaseURL).replace('\n','').replace('\r','')
    
    if id != 'None':
        versioncheckmatch = re.compile('version="(.+?)"').findall(link)
        versioncheck  = versioncheckmatch[0] if (len(versioncheckmatch) > 0) else ''
    
        if  localversioncheck < versioncheck:
            return True
    
    else:
        return False
#---------------------------------------------------------------------------------------------------
#Create restore menu
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
def CheckPath():
    path = xbmc.translatePath(os.path.join(zip,'testCBFolder'))
    
    try:
        os.makedirs(path)
        os.removedirs(path)
        dialog.ok('[COLOR=lime]SUCCESS[/COLOR]', 'Great news, the path you chose is writeable.', 'Some of these builds are rather big, we recommend a minimum of 1GB storage space.')
    
    except:
        dialog.ok('[COLOR=red]CANNOT WRITE TO PATH[/COLOR]', 'Kodi cannot write to the path you\'ve chosen. Please click OK in the settings menu to save the path then try again. Some devices give false results, we recommend using a USB stick as the backup path.')
#---------------------------------------------------------------------------------------------------
#Function to clean HTML into plain text. Not perfect but it's better than raw html code!
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
#Build Countries Menu (First Filter)    
def Countries(url):
    o0oO('folder','African',str(url)+'&genre=african','grab_builds','','','','')
    o0oO('folder','Arabic',str(url)+'&genre=arabic','grab_builds','','','','')
    o0oO('folder','Asian',str(url)+'&genre=asian','grab_builds','','','','')
    o0oO('folder','Australian',str(url)+'&genre=australian','grab_builds','','','','')
    o0oO('folder','Austrian',str(url)+'&genre=austrian','grab_builds','','','','')
    o0oO('folder','Belgian',str(url)+'&genre=belgian','grab_builds','','','','')
    o0oO('folder','Brazilian',str(url)+'&genre=brazilian','grab_builds','','','','')
    o0oO('folder','Canadian',str(url)+'&genre=canadian','grab_builds','','','','')
    o0oO('folder','Columbian',str(url)+'&genre=columbian','grab_builds','','','','')
    o0oO('folder','Czech',str(url)+'&genre=czech','grab_builds','','','','')
    o0oO('folder','Danish',str(url)+'&genre=danish','grab_builds','','','','')
    o0oO('folder','Dominican',str(url)+'&genre=dominican','grab_builds','','','','')
    o0oO('folder','Dutch',str(url)+'&genre=dutch','grab_builds','','','','')
    o0oO('folder','Egyptian',str(url)+'&genre=egyptian','grab_builds','','','','')
    o0oO('folder','Filipino',str(url)+'&genre=filipino','grab_builds','','','','')
    o0oO('folder','Finnish',str(url)+'&genre=finnish','grab_builds','','','','')
    o0oO('folder','French',str(url)+'&genre=french','grab_builds','','','','')
    o0oO('folder','German',str(url)+'&genre=german','grab_builds','','','','')
    o0oO('folder','Greek',str(url)+'&genre=greek','grab_builds','','','','')
    o0oO('folder','Hebrew',str(url)+'&genre=hebrew','grab_builds','','','','')
    o0oO('folder','Hungarian',str(url)+'&genre=hungarian','grab_builds','','','','')
    o0oO('folder','Icelandic',str(url)+'&genre=icelandic','grab_builds','','','','')
    o0oO('folder','Indian',str(url)+'&genre=indian','grab_builds','','','','')
    o0oO('folder','Irish',str(url)+'&genre=irish','grab_builds','','','','')
    o0oO('folder','Italian',str(url)+'&genre=italian','grab_builds','','','','')
    o0oO('folder','Japanese',str(url)+'&genre=japanese','grab_builds','','','','')
    o0oO('folder','Korean',str(url)+'&genre=korean','grab_builds','','','','')
    o0oO('folder','Lebanese',str(url)+'&genre=lebanese','grab_builds','','','','')
    o0oO('folder','Mongolian',str(url)+'&genre=mongolian','grab_builds','','','','')
    o0oO('folder','Nepali',str(url)+'&genre=nepali','grab_builds','','','','')
    o0oO('folder','New Zealand',str(url)+'&genre=newzealand','grab_builds','','','','')
    o0oO('folder','Norwegian',str(url)+'&genre=norwegian','grab_builds','','','','')
    o0oO('folder','Pakistani',str(url)+'&genre=pakistani','grab_builds','','','','')
    o0oO('folder','Polish',str(url)+'&genre=polish','grab_builds','','','','')
    o0oO('folder','Portuguese',str(url)+'&genre=portuguese','grab_builds','','','','')
    o0oO('folder','Romanian',str(url)+'&genre=romanian','grab_builds','','','','')
    o0oO('folder','Russian',str(url)+'&genre=russian','grab_builds','','','','')
    o0oO('folder','Singapore',str(url)+'&genre=singapore','grab_builds','','','','')
    o0oO('folder','Spanish',str(url)+'&genre=spanish','grab_builds','','','','')
    o0oO('folder','Swedish',str(url)+'&genre=swedish','grab_builds','','','','')
    o0oO('folder','Swiss',str(url)+'&genre=swiss','grab_builds','','','','')
    o0oO('folder','Syrian',str(url)+'&genre=syrian','grab_builds','','','','')
    o0oO('folder','Tamil',str(url)+'&genre=tamil','grab_builds','','','','')
    o0oO('folder','Thai',str(url)+'&genre=thai','grab_builds','','','','')
    o0oO('folder','Turkish',str(url)+'&genre=turkish','grab_builds','','','','')
    o0oO('folder','UK',str(url)+'&genre=uk','grab_builds','','','','')
    o0oO('folder','USA',str(url)+'&genre=usa','grab_builds','','','','')
    o0oO('folder','Vietnamese',str(url)+'&genre=vietnamese','grab_builds','','','','')
#---------------------------------------------------------------------------------------------------
# OLD METHOD to create a community (universal) backup - this renames paths to special:// and removes unwanted folders
def Community_Backup_OLD():
    Check_Download_Path()
    fullbackuppath  = xbmc.translatePath(os.path.join(USB,'Community_Builds','My_Builds',''))
    myfullbackup    = xbmc.translatePath(os.path.join(USB,'Community_Builds','My_Builds','my_full_backup.zip'))
    
    if not os.path.exists(fullbackuppath):
        os.makedirs(fullbackuppath)
    
    vq = Get_Keyboard( heading="Enter a name for this backup" )
    if ( not vq ):
        return False, 0
    
    title              = urllib.quote_plus(vq)
    backup_zip         = xbmc.translatePath(os.path.join(fullbackuppath,title+'.zip'))
    exclude_dirs       = ['Thumbnails']
    exclude_files      = ["xbmc.log","xbmc.old.log","Textures13.db",'.DS_Store','.setup_complete','XBMCHelper.conf', 'advancedsettings.xml','Thumbs.db','.gitignore']
    message_header     = "Creating full backup of existing build"
    message_header2    = "Creating Community Build"
    message1           = "Archiving..."
    message2           = ""
    message3           = "Please Wait"
    
    Fix_Special(HOME)
    Archive_Tree(HOME, backup_zip, message_header2, message1, message2, message3, exclude_dirs, exclude_files)  
    time.sleep(1)
   
    dialog.ok("Build Location", 'Universal Backup:[CR][COLOR=dodgerblue]'+backup_zip+'[/COLOR]')
#---------------------------------------------------------------------------------------------------
# This creates the final menu showing build details, video and install link
def Community_Menu(url,video):
    BaseURL            = 'http://noobsandnerds.com/TI/Community_Builds/community_builds_premium.php?id=%s' % (url)
    link               = Open_URL(BaseURL).replace('\n','').replace('\r','')
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
    o0oO('','[COLOR=yellow]IMPORTANT:[/COLOR] Install Instructions','','instructions_2','','','','')
    Add_Desc_Dir('[COLOR=yellow]Description:[/COLOR] This contains important info from the build author','None','description','',fanart,name,author,version,description,updated,skins,videoaddons,audioaddons,programaddons,pictureaddons,sources,adult)
    
    if localidcheck == head and localversioncheck != version:
        o0oO('','[COLOR=orange]----------------- UPDATE AVAILABLE ------------------[/COLOR]','None','','','','','')
        Add_Build_Dir('[COLOR=dodgerblue]1. Update:[/COLOR] Overwrite My Current Setup & Install New Build',downloadURL,'restore_community',iconimage,'','update',name,defaultskin,guisettingslink,artpack)
        Add_Build_Dir('[COLOR=dodgerblue]2. Update:[/COLOR] Keep My Library & Profiles',downloadURL,'restore_community',iconimage,'','updatelibprofile',name,defaultskin,guisettingslink,artpack)
        Add_Build_Dir('[COLOR=dodgerblue]3. Update:[/COLOR] Keep My Library Only',downloadURL,'restore_community',iconimage,'','updatelibrary',name,defaultskin,guisettingslink,artpack)
        Add_Build_Dir('[COLOR=dodgerblue]4. Update:[/COLOR] Keep My Profiles Only',downloadURL,'restore_community',iconimage,'','updateprofiles',name,defaultskin,guisettingslink,artpack)
    
    if videopreview != 'None' or videoguide1 != 'None' or videoguide2 != 'None' or videoguide3 != 'None' or videoguide4 != 'None' or videoguide5 != 'None':
        o0oO('','[COLOR=orange]------------------ VIDEO GUIDES -----------------[/COLOR]','None','','','','','')
    
    if videopreview != 'None':
        o0oO('','[COLOR=orange]Video:[/COLOR][COLOR=white] Preview[/COLOR]',videopreview,'play_video','',fanart,'','')
    
    if videoguide1 != 'None':
        o0oO('','[COLOR=orange]Video:[/COLOR][COLOR=white] '+videolabel1+'[/COLOR]',videoguide1,'play_video','',fanart,'','')    
    
    if videoguide2 != 'None':
        o0oO('','[COLOR=orange]Video:[/COLOR][COLOR=white] '+videolabel2+'[/COLOR]',videoguide2,'play_video','',fanart,'','')    
    
    if videoguide3 != 'None':
        o0oO('','[COLOR=orange]Video:[/COLOR][COLOR=white] '+videolabel3+'[/COLOR]',videoguide3,'play_video','',fanart,'','')    
    
    if videoguide4 != 'None':
        o0oO('','[COLOR=orange]Video:[/COLOR][COLOR=white] '+videolabel4+'[/COLOR]',videoguide4,'play_video','',fanart,'','')    
    
    if videoguide5 != 'None':
        o0oO('','[COLOR=orange]Video:[/COLOR][COLOR=white] '+videolabel5+'[/COLOR]',videoguide5,'play_video','',fanart,'','')    
    
    if localidcheck != head:
        o0oO('','[COLOR=orange]------------------ INSTALL OPTIONS ------------------[/COLOR]','None','','','','','')
    
    if downloadURL=='None':
        Add_Build_Dir('[COLOR=orange]Sorry this build is currently unavailable[/COLOR]','','','','','','','','','')
    
    if localidcheck != head:
        Add_Build_Dir('[COLOR=dodgerblue]1. Install:[/COLOR] Overwrite My Current Setup & Install New Build',downloadURL,'restore_community',iconimage,fanart,'merge',name,defaultskin,guisettingslink,artpack)
        Add_Build_Dir('[COLOR=dodgerblue]2. Install:[/COLOR] Keep My Library & Profiles',downloadURL,'restore_community',iconimage,fanart,'libprofile',name,defaultskin,guisettingslink,artpack)
        Add_Build_Dir('[COLOR=dodgerblue]3. Install:[/COLOR] Keep My Library Only',downloadURL,'restore_community',iconimage,fanart,'library',name,defaultskin,guisettingslink,artpack)
        Add_Build_Dir('[COLOR=dodgerblue]4. Install:[/COLOR] Keep My Profiles Only',downloadURL,'restore_community',iconimage,fanart,'profiles',name,defaultskin,guisettingslink,artpack)
         
    if guisettingslink!='None':
        o0oO('','[COLOR=orange]---------- (OPTIONAL) Guisettings Fix ----------[/COLOR]','None','','','','','')
        o0oO('','[COLOR=orange]Install Step 2:[/COLOR] Apply guisettings.xml fix',guisettingslink,'guisettingsfix','',fanart,'','')
#---------------------------------------------------------------------------------------------------
#Function to delete the packages folder
def Delete_Packages():
    print '############################################################       DELETING PACKAGES             ###############################################################'
    for root, dirs, files in os.walk(packages):
        file_count = 0
        file_count += len(files)
        
        if file_count > 0:
            
            for f in files:
                os.unlink(os.path.join(root, f))
            
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
#---------------------------------------------------------------------------------------------------
#Step 3 of the addon install process (installs the dependencies)
def Dependency_Install(name,addon_id,addonpath):
    modulestatus = 1
    status       = 1
    addonxml     = os.path.join(addonpath,'addon.xml')   
    addonsource  = open(addonxml, mode = 'r')
    readxml      = addonsource.read()
    addonsource.close()
    dmatch       = re.compile('import addon="(.+?)"').findall(readxml)
    
    for requires in dmatch:
        
        if not 'xbmc.python' in requires and 'beautifulsoup' not in requires and 'xbmcaddon' not in requires:
            print 'Script Requires --- ' + requires

            try:
                BaseURL        = 'http://noobsandnerds.com/TI/AddonPortal/dependencyinstall.php?id=%s' % (requires)
                link           = Open_URL(BaseURL).replace('\n','').replace('\r','')
                namematch      = re.compile('name="(.+?)"').findall(link)
                versionmatch   = re.compile('version="(.+?)"').findall(link)
                repourlmatch   = re.compile('repo_url="(.+?)"').findall(link)
                dataurlmatch   = re.compile('data_url="(.+?)"').findall(link)
                zipurlmatch    = re.compile('zip_url="(.+?)"').findall(link)
                repoidmatch    = re.compile('repo_id="(.+?)"').findall(link)  
                contentmatch   = re.compile('content_types="(.+?)"').findall(link)  
                depname        = namematch[0] if (len(namematch) > 0) else ''
                version        = versionmatch[0] if (len(versionmatch) > 0) else ''
                repourl        = repourlmatch[0] if (len(repourlmatch) > 0) else ''
                dataurl        = dataurlmatch[0] if (len(dataurlmatch) > 0) else ''
                zipurl         = zipurlmatch[0] if (len(zipurlmatch) > 0) else ''
                repoid         = repoidmatch[0] if (len(repoidmatch) > 0) else ''
                content        = contentmatch[0] if (len(contentmatch) > 0) else ''
                dependencyname = xbmc.translatePath(os.path.join(packages,depname+'.zip')) 
            except:
                dialog.ok('Unable to contact server','Sorry, it wasn\'t possible to access the noobsandnerds','server. Please try reinstalling as the modules may not','have been installed correctly')
                return
            
            if 'executable' in content:
                addonlocation = os.path.join(HOME,'scripts',depname)
                installdir    = os.path.join(HOME,'scripts')
            
            elif 'video' in content:
                addonlocation = os.path.join(HOME,'plugins','video',depname)
                installdir    = os.path.join(HOME,'plugins','video')
            
            elif 'audio' in content:
                addonlocation = os.path.join(HOME,'plugins','music',depname)
                installdir    = os.path.join(HOME,'plugins','music')

            elif 'images' in content:
                addonlocation = os.path.join(HOME,'plugins','pictures',depname)
                installdir    = os.path.join(HOME,'plugins','pictures')

            elif 'module' in content:
                addonlocation = os.path.join(HOME,'scripts','.modules',requires)
                installdir    = os.path.join(HOME,'scripts','.modules')

            elif 'repository' in content:
                addonlocation = xbmc.translatePath(os.path.join(USERDATA,'plugin_data','programs','Addons4Xbox Installer','repositories',requires))
                installdir    = xbmc.translatePath(os.path.join(USERDATA,'plugin_data','programs','Addons4Xbox Installer','repositories'))
            
            if not os.path.exists(addonlocation):
                try:
                    downloader.download('https://github.com/noobsandnerds/addons4xbox/blob/master/xbox_modules/'+requires+'.zip?raw=true', dependencyname, dp)
                    extract.all(dependencyname, xbmc.translatePath(os.path.join("special://home", "scripts", ".modules")), dp)
                except:

                    try:
                        downloader.download(repourl, dependencyname, dp)
                        extract.all(dependencyname, installdir, dp)
                        if not 'repository' in content and not 'module' in content:
                            os.rename(addonlocation,os.path.join(installdir,depname))
                    except:
                    
                        try:
                            downloader.download(zipurl, dependencyname, dp)
                            extract.all(dependencyname, installdir, dp)
                            if not 'repository' in content and not 'module'in content:
                                os.rename(addonlocation,os.path.join(installdir,depname))                
                        except:
                        
                            try:
                            
                                if not os.path.exists(addonlocation):
                                    os.makedirs(addonlocation)
                            
                                link = Open_URL(dataurl).replace('\n','').replace('\r','')
                                match=re.compile('href="(.+?)"', re.DOTALL).findall(link)
                            
                                for href in match:
                                    filepath=xbmc.translatePath(os.path.join(addonlocation,href))
                                
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
                                dialog.ok("Error downloading dependency", 'There was an error downloading [COLOR=dodgerblue]'+depname+'[/COLOR]. Please consider updating the add-on portal with details or report the error on the forum at [COLOR=orange]noobs[/COLOR][COLOR=dodgerblue]and[/COLOR][COLOR=orange]nerds[/COLOR]')
                                status=0
                                modulestatus=0
                
                if status==1:
                    time.sleep(1)
                    dp.update(0,"[COLOR=yellow]"+depname+'[/COLOR]  [COLOR=lime]Successfully Installed[/COLOR]','','Please wait...')
                    time.sleep(1)
                    incremental = 'http://noobsandnerds.com/TI/AddonPortal/downloadcount.php?id=%s' % (requires)
                    Open_URL(incremental)
    dp.close()
    time.sleep(1)
#---------------------------------------------------------------------------------------------------
#Show full description of build
def Description(name,url,buildname,author,version,description,updated,skins,videoaddons,audioaddons,programaddons,pictureaddons,sources,adult):
    Text_Boxes(buildname+'     v.'+version, '[COLOR=yellow][B]Author:   [/B][/COLOR]'+author+'[COLOR=yellow][B]               Last Updated:   [/B][/COLOR]'+updated+'[COLOR=yellow][B]               Adult Content:   [/B][/COLOR]'+adult+'[CR][CR][COLOR=yellow][B]Description:[CR][/B][/COLOR]'+description+
    '[CR][CR][COLOR=blue][B]Skins:   [/B][/COLOR]'+skins+'[CR][CR][COLOR=blue][B]Video Addons:   [/B][/COLOR]'+videoaddons+'[CR][CR][COLOR=blue][B]Audio Addons:   [/B][/COLOR]'+audioaddons+
    '[CR][CR][COLOR=blue][B]Program Addons:   [/B][/COLOR]'+programaddons+'[CR][CR][COLOR=blue][B]Picture Addons:   [/B][/COLOR]'+pictureaddons+'[CR][CR][COLOR=blue][B]Sources:   [/B][/COLOR]'+sources+
    '[CR][CR][COLOR=orange]Disclaimer: [/COLOR]These are community builds and they may overwrite some of your existing settings, '
    'It\'s purely the responsibility of the user to choose whether or not they wish to install these builds, the individual who uploads the build should state what\'s included and then it\'s the users decision to decide whether or not that content is suitable for them.')
#---------------------------------------------------------------------------------------------------
#Function to do a full wipe.
def Destroy_Path(path):
    dp.create("[COLOR=orange]noobs[/COLOR][COLOR=dodgerblue]and[/COLOR][COLOR=orange]nerds[/COLOR]","Wiping...",'', 'Please Wait')
    shutil.rmtree(path, ignore_errors=True)
#---------------------------------------------------------------------------------------------------
def Finish_Local_Restore():
    os.remove(idfile)
    os.rename(idfiletemp,idfile)
    xbmc.executebuiltin('UnloadSkin')    
    xbmc.executebuiltin("ReloadSkin")
    dialog.ok("Local Restore Complete", 'XBMC/Kodi will now close.', '', '')
    xbmc.executebuiltin("Quit")      
#---------------------------------------------------------------------------------------------------
#Convert physical paths to special paths
def Fix_Special(url):
    dp.create("Changing Physical Paths To Special","Renaming paths...",'', 'Please Wait')
    
    for root, dirs, files in os.walk(url):  #Search all xml files and replace physical with special
        
        for file in files:
            
            if file.endswith(".xml"):
                 dp.update(0,"Fixing",file, 'Please Wait')
                 a = open((os.path.join(root, file))).read()
                 b = a.replace(HOME, 'special://home/')
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
#Build Genres Menu (First Filter)
def Genres(url):       
    o0oO('folder','Anime',str(url)+'&genre=anime','grab_builds','','','','')
    o0oO('folder','Audiobooks',str(url)+'&genre=audiobooks','grab_builds','','','','')
    o0oO('folder','Comedy',str(url)+'&genre=comedy','grab_builds','','','','')
    o0oO('folder','Comics',str(url)+'&genre=comics','grab_builds','','','','')
    o0oO('folder','Documentary',str(url)+'&genre=documentary','grab_builds','','','','')
    o0oO('folder','Downloads',str(url)+'&genre=downloads','grab_builds','','','','')
    o0oO('folder','Food',str(url)+'&genre=food','grab_builds','','','','')
    o0oO('folder','Gaming',str(url)+'&genre=gaming','grab_builds','','','','')
    o0oO('folder','Health',str(url)+'&genre=health','grab_builds','','','','')
    o0oO('folder','How To...',str(url)+'&genre=howto','grab_builds','','','','')
    o0oO('folder','Kids',str(url)+'&genre=kids','grab_builds','','','','')
    o0oO('folder','Live TV',str(url)+'&genre=livetv','grab_builds','','','','')
    o0oO('folder','Movies',str(url)+'&genre=movies','grab_builds','','','','')
    o0oO('folder','Music',str(url)+'&genre=music','grab_builds','','','','')
    o0oO('folder','News',str(url)+'&genre=news','grab_builds','','','','')
    o0oO('folder','Photos',str(url)+'&genre=photos','grab_builds','','','','')
    o0oO('folder','Podcasts',str(url)+'&genre=podcasts','grab_builds','','','','')
    o0oO('folder','Radio',str(url)+'&genre=radio','grab_builds','','','','')
    o0oO('folder','Religion',str(url)+'&genre=religion','grab_builds','','','','')
    o0oO('folder','Space',str(url)+'&genre=space','grab_builds','','','','')
    o0oO('folder','Sports',str(url)+'&genre=sports','grab_builds','','','','')
    o0oO('folder','Technology',str(url)+'&genre=tech','grab_builds','','','','')
    o0oO('folder','Trailers',str(url)+'&genre=trailers','grab_builds','','','','')
    o0oO('folder','TV Shows',str(url)+'&genre=tv','grab_builds','','','','')
    o0oO('folder','Misc.',str(url)+'&genre=other','grab_builds','','','','')
    
    if ADDON.getSetting('adult') == 'true':
        o0oO('folder','XXX',str(url)+'&genre=adult','grab_builds','','','','')
#---------------------------------------------------------------------------------------------------
def Get_Keyboard( default="", heading="", hidden=False ):
    """ shows a keyboard and returns a value """
    keyboard = xbmc.Keyboard( default, heading, hidden )
    keyboard.doModal()
    if ( keyboard.isConfirmed() ):
        return unicode( keyboard.getText(), "utf-8" )
    return default
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
#Function to populate the search based on the initial first filter
def Grab_Addons(url):
    print"URL: "+url
    
    if ADDON.getSetting('adult') == 'true':
        adult = 'yes'
    
    else:
        adult = 'no'

    if 'popular' in url and showall == 'false':
        buildsURL  = 'http://noobsandnerds.com/TI/AddonPortal/popular_xbox.php?adult=%s&approved=yes' % (adult)
    elif 'popular' in url and showall == 'true':
        buildsURL  = 'http://noobsandnerds.com/TI/AddonPortal/popular_xbox.php?adult=%s&approved=no' % (adult)

# Only show approved addons (should be fully legal in all regions) unless overriden in plugin settings
    elif not 'popular' in url and showall == 'true':
        buildsURL  = 'http://noobsandnerds.com/TI/AddonPortal/sortby_xbox.php?approved=no&sortx=name&user=%s&adult=%s&%s' % (username, adult, url)
    elif not 'popular' in url and showall == 'false':
        buildsURL  = 'http://noobsandnerds.com/TI/AddonPortal/sortby_xbox.php?approved=yes&sortx=name&user=%s&adult=%s&%s' % (username, adult, url)
    link       = Open_URL(buildsURL).replace('\n','').replace('\r','')
# match without cloudflare enabled
    match      = re.compile('name="(.+?)"  <br> downloads="(.+?)"  <br> icon="(.+?)"  <br> broken="(.+?)"  <br> UID="(.+?)"  <br>', re.DOTALL).findall(link)
    if match == []:
# match with cloudflare enabled
        match  = re.compile('name="(.+?)" <br> downloads="(.+?)" <br> icon="(.+?)" <br> broken="(.+?)" <br> UID="(.+?)" <br>', re.DOTALL).findall(link)
    
    if match !=[]:
        if not 'xbox=c' in url:
            o0oO('folder','[COLOR=gold]Show only Add-ons marked as Xbox Compatible[/COLOR]',url+'&xbox=c','grab_addons','','','','')
        if not 'popular' in url and not 'xbox=c' in url:
            Sort_By(buildsURL,'addons')
        
        for name,downloads,icon, broken, uid in match:
            
            if broken=='0':
                o0oO('addonfolder',name+'[COLOR=lime] ['+downloads+' downloads][/COLOR]',uid,'addon_final_menu',icon,'','')        
            
            if broken=='1':
                o0oO('addonfolder','[COLOR=red]'+name+' [REPORTED AS BROKEN][/COLOR]',uid,'addon_final_menu',icon,'','')        
    
    elif '&redirect' in url:
        choice=dialog.yesno('No Content Found','This add-on cannot be found on the Add-on Portal.','','Would you like to remove this item from your setup?')
        
        if choice == 1: print"remove"
    
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

    if not 'id=' in url:
        buildsURL  = 'http://noobsandnerds.com/TI/Community_Builds/sortby.php?sortx=name&orderx=ASC&adult=%s&%s' % (adult, url)
        link       = Open_URL(buildsURL).replace('\n','').replace('\r','')
# match without cloudflare disabled
        match      = re.compile('name="(.+?)"  <br> id="(.+?)"  <br> Thumbnail="(.+?)"  <br> Fanart="(.+?)"  <br> downloads="(.+?)"  <br> <br>', re.DOTALL).findall(link)
        if match == []:
# match with cloudflare disabled
            match  = re.compile('name="(.+?)" <br> id="(.+?)" <br> Thumbnail="(.+?)" <br> Fanart="(.+?)" <br> downloads="(.+?)" <br> <br>', re.DOTALL).findall(link)
        Sort_By(url,'communitybuilds')
    
        for name,id,Thumbnail,Fanart,downloads in match:
            Add_Build_Dir(name+'[COLOR=lime] ('+downloads+' downloads)[/COLOR]',id+url,'community_menu',Thumbnail,Fanart,id,'','','','')
    
    if 'id=1' in url: buildsURL = wizardurl1
    if 'id=2' in url: buildsURL = wizardurl2
    if 'id=3' in url: buildsURL = wizardurl3
    if 'id=4' in url: buildsURL = wizardurl4
    if 'id=5' in url: buildsURL = wizardurl5

    link       = Open_URL(buildsURL).replace('\n','').replace('\r','')
    match      = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)

    for name,url,iconimage,fanart,description in match:
        if not 'viewport' in name:
            o0oO('addon',name,url,'restore_local_CB',iconimage,fanart,description,'')
#-----------------------------------------------------------------------------------------------------------------
#Function to populate the search based on the initial first filter
def Grab_Skins():
    buildsURL  = 'http://noobsandnerds.com/TI/AddonPortal/xbox_skins.php?sortx=name&orderx=ASC'
    link       = Open_URL(buildsURL).replace('\n','').replace('\r','')
# match without cloudflare enabled
    match      = re.compile('name="(.+?)"  <br> downloads="(.+?)"  <br> icon="(.+?)"  <br> broken="(.+?)"  <br> UID="(.+?)"  <br>', re.DOTALL).findall(link)
    if match == []:
# match with cloudflare enabled
        match  = re.compile('name="(.+?)" <br> downloads="(.+?)" <br> icon="(.+?)" <br> broken="(.+?)" <br> UID="(.+?)" <br>', re.DOTALL).findall(link)
    
    if match !=[]:
        for name,downloads,icon, broken, uid in match:
            
            if broken=='0':
                o0oO('addonfolder',name+'[COLOR=lime] ['+downloads+' downloads][/COLOR]',uid,'addon_final_menu',icon,'','')
            
            if broken=='1':
                o0oO('addonfolder','[COLOR=red]'+name+' [REPORTED AS BROKEN][/COLOR]',uid,'addon_final_menu',icon,'','')
    
    else:
        dialog.ok('No Content Found','Sorry no content can be found that matches','your search criteria.','')
#---------------------------------------------------------------------------------------------------
#Function to populate the search based on the initial first filter
def Grab_Hardware(url):
    buildsURL  = 'http://noobsandnerds.com/TI/HardwarePortal/sortby.php?sortx=Added&orderx=DESC&%s' % (url)
    link       = Open_URL(buildsURL).replace('\n','').replace('\r','')
# match without cloudflare enabled
    match      = re.compile('name="(.+?)"  <br> id="(.+?)"  <br> thumb="(.+?)"  <br><br>', re.DOTALL).findall(link)
    if match == []:
# match with cloudflare enabled
        match  = re.compile('name="(.+?)" <br> id="(.+?)" <br> thumb="(.+?)" <br><br>', re.DOTALL).findall(link)
    Sort_By(buildsURL,'hardware')
    
    for name, id, thumb in match:
        o0oO('folder2',name,id,'hardware_final_menu',thumb,'','')
#---------------------------------------------------------------------------------------------------
#Function to populate the news search
def Grab_News(url):
    buildsURL = 'http://noobsandnerds.com/TI/LatestNews/sortby.php?sortx=item_date&orderx=DESC&%s' % (url)
    link      = Open_URL(buildsURL).replace('\n','').replace('\r','')
# match without cloudflare enabled
    match     = re.compile('name="(.+?)"  <br> date="(.+?)"  <br> source="(.+?)"  <br> id="(.+?)"  <br><br>', re.DOTALL).findall(link)
    if match == []:
# match with cloudflare enabled
        match     = re.compile('name="(.+?)" <br> date="(.+?)" <br> source="(.+?)" <br> id="(.+?)" <br><br>', re.DOTALL).findall(link)
    for name, date, source, id in match:
        
        if "OpenELEC" in source:
            o0oO('',name+'  ('+date+')',id,'news_menu','','','')
        
        if "Official" in source:
            o0oO('',name+'  ('+date+')',id,'news_menu','','','')
        
        if "Raspbmc" in source:
            o0oO('',name+'  ('+date+')',id,'news_menu','','','')
        
        if "XBMC4Xbox" in source:
            o0oO('',name+'  ('+date+')',id,'news_menu','','','')
        
        if "noobsandnerds" in source:
            o0oO('',name+'  ('+date+')',id,'news_menu','','','')
#---------------------------------------------------------------------------------------------------
#Function to populate the search based on the initial first filter
def Grab_Tutorials(url):
    buildsURL  = 'http://noobsandnerds.com/TI/TutorialPortal/sortby.php?sortx=Name&orderx=ASC&%s' % (url)
    link       = Open_URL(buildsURL).replace('\n','').replace('\r','')
# match without cloudflare enabled
    match      = re.compile('name="(.+?)"  <br> about="(.+?)"  <br> id="(.+?)"  <br><br>', re.DOTALL).findall(link)
    if match == []:
# match with cloudflare enabled
        match      = re.compile('name="(.+?)" <br> about="(.+?)" <br> id="(.+?)" <br><br>', re.DOTALL).findall(link)
    Sort_By(buildsURL,'tutorials')
    
    for name, about, id in match:
        o0oO('folder',name,id,'tutorial_final_menu','','',about)
#---------------------------------------------------------------------------------------------------
#Option to download guisettings fix that merges with existing settings.
def GUI_Settings_Fix(url,local):
    Check_Download_Path()
    choice = xbmcgui.Dialog().yesno(name, 'This will over-write your existing guisettings.xml.', 'Are you sure this is the build you have installed?', '', nolabel='No, Cancel',yeslabel='Yes, Fix')
    
    if choice == 1:
        GUI_Merge(url,local)
#---------------------------------------------------------------------------------------------------
#Function to download guisettings.xml and merge with existing.
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

#Rename guisettings.xml to guinew.xml so we can edit without XBMC interfering.
    try:
        shutil.copyfile(GUI,GUINEW)
    
    except:
        print"No guisettings found, most likely due to a previously failed attempt at install"
    
    if local!=1:
        lib=os.path.join(USB, 'guifix.zip')
    
    else:
        lib=xbmc.translatePath(url)

# Get the size of the downloaded guisettings so we can later add to the id.xml
    guisize=str(os.path.getsize(lib))
    dp.create("Installing Skin Fix","Checking ",'', 'Please Wait')
    dp.update(0,"", "Extracting Zip Please Wait")
    extract.all(lib,guitemp,dp)
    
    if local != 'library' or local != 'updatelibrary' or local !='fresh':
        
        try:
            readfile = open(guitemp+'profiles.xml', mode='r')
            default_contents = readfile.read()
            readfile.close()
            
            if os.path.exists(guitemp+'profiles.xml'):
                
                if local == None:
                    choice = xbmcgui.Dialog().yesno("PROFILES DETECTED", 'This build has profiles included, would you like to overwrite your existing profiles or keep the ones you have?', '','', nolabel='Keep my profiles',yeslabel='Use new profiles')
                
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
    os.rename(guitemp+'guisettings.xml',GUIFIX)
    
    if local != 'fresh':
        choice2 = dialog.yesno("Do You Want To Keep Your Kodi Settings?", 'Would you like to keep your existing settings or would you rather erase them and install the ones associated with this latest build?', nolabel='Keep my settings',yeslabel='Replace my settings')
    
    if local == 'fresh':
        choice2 = 1
    
    if choice2 == 1:
        
        if os.path.exists(GUI):
            
            try:
                print"Attempting to remove guisettings"
                os.remove(GUI)
                success=True
            
            except:
                print"Problem removing guisettings"
                success=False
            
            try:
                print"Attempting to replace guisettings with new"
                os.rename(GUIFIX,GUI)
                success=True
            
            except:
                print"Failed to replace guisettings with new"
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
    if os.path.exists(guitemp+'profiles.xml'):
        os.remove(guitemp+'profiles.xml')
        time.sleep(1)
    
    if os.path.exists(guitemp):
        os.removedirs(guitemp)
    
    notifypath = xbmc.translatePath(os.path.join(ADDON_DATA,'programs',AddonName,'notification.txt'))
    
    if os.path.exists(notifypath):
        os.remove(notifypath)
    
    if success == True:
        Remove_Textures()
        Kill_XBMC()
#---------------------------------------------------------------------------------------------------
# This creates the final menu showing build details, video and install link
def Hardware_Menu(url):
    BaseURL           = 'http://noobsandnerds.com/TI/HardwarePortal/hardwaredetails.php?id=%s' % (url)
    link              = Open_URL(BaseURL).replace('\n','').replace('\r','')
    namematch         = re.compile('name="(.+?)"').findall(link)
    manufacturermatch = re.compile('manufacturer="(.+?)"').findall(link)
    videoguide1match  = re.compile('video_guide1="(.+?)"').findall(link)
    videoguide2match  = re.compile('video_guide2="(.+?)"').findall(link)
    videoguide3match  = re.compile('video_guide3="(.+?)"').findall(link)
    videoguide4match  = re.compile('video_guide4="(.+?)"').findall(link)
    videoguide5match  = re.compile('video_guide5="(.+?)"').findall(link)
    videolabel1match  = re.compile('video_label1="(.+?)"').findall(link)
    videolabel2match  = re.compile('video_label2="(.+?)"').findall(link)
    videolabel3match  = re.compile('video_label3="(.+?)"').findall(link)
    videolabel4match  = re.compile('video_label4="(.+?)"').findall(link)
    videolabel5match  = re.compile('video_label5="(.+?)"').findall(link)
    shopmatch         = re.compile('shops="(.+?)"').findall(link)
    descmatch         = re.compile('description="(.+?)"').findall(link)
    screenshot1match  = re.compile('screenshot1="(.+?)"').findall(link)
    screenshot2match  = re.compile('screenshot2="(.+?)"').findall(link)
    screenshot3match  = re.compile('screenshot3="(.+?)"').findall(link)
    screenshot4match  = re.compile('screenshot4="(.+?)"').findall(link)
    screenshot5match  = re.compile('screenshot5="(.+?)"').findall(link)
    screenshot6match  = re.compile('screenshot6="(.+?)"').findall(link)
    screenshot7match  = re.compile('screenshot7="(.+?)"').findall(link)
    screenshot8match  = re.compile('screenshot8="(.+?)"').findall(link)
    screenshot9match  = re.compile('screenshot9="(.+?)"').findall(link)
    screenshot10match = re.compile('screenshot10="(.+?)"').findall(link)
    screenshot11match = re.compile('screenshot11="(.+?)"').findall(link)
    screenshot12match = re.compile('screenshot12="(.+?)"').findall(link)
    screenshot13match = re.compile('screenshot13="(.+?)"').findall(link)
    screenshot14match = re.compile('screenshot14="(.+?)"').findall(link)
    addedmatch        = re.compile('added="(.+?)"').findall(link)
    platformmatch     = re.compile('platform="(.+?)"').findall(link)
    chipsetmatch      = re.compile('chipset="(.+?)"').findall(link)
    guidematch        = re.compile('official_guide="(.+?)"').findall(link)
    previewmatch      = re.compile('official_preview="(.+?)"').findall(link)
    thumbmatch        = re.compile('thumbnail="(.+?)"').findall(link)
    stockmatch        = re.compile('stock_rom="(.+?)"').findall(link)
    cpumatch          = re.compile('CPU="(.+?)"').findall(link)
    gpumatch          = re.compile('GPU="(.+?)"').findall(link)
    rammatch          = re.compile('RAM="(.+?)"').findall(link)
    flashmatch        = re.compile('flash="(.+?)"').findall(link)
    wifimatch         = re.compile('wifi="(.+?)"').findall(link)
    bluetoothmatch    = re.compile('bluetooth="(.+?)"').findall(link)
    lanmatch          = re.compile('LAN="(.+?)"').findall(link)
    xbmcmatch         = re.compile('xbmc_version="(.+?)"').findall(link)
    prosmatch         = re.compile('pros="(.+?)"').findall(link)
    consmatch         = re.compile('cons="(.+?)"').findall(link)
    librarymatch      = re.compile('library_scan="(.+?)"').findall(link)
    fourkmatch        = re.compile('4k="(.+?)"').findall(link)
    teneightymatch    = re.compile('1080="(.+?)"').findall(link)
    seventwentymatch  = re.compile('720="(.+?)"').findall(link)
    threedmatch       = re.compile('3D="(.+?)"').findall(link)
    dtsmatch          = re.compile('DTS="(.+?)"').findall(link)
    bootmatch         = re.compile('BootTime="(.+?)"').findall(link)
    copyfilesmatch    = re.compile('CopyFiles="(.+?)"').findall(link)
    copyvideomatch    = re.compile('CopyVideo="(.+?)"').findall(link)
    ethernetmatch     = re.compile('EthernetTest="(.+?)"').findall(link)
    slideshowmatch    = re.compile('Slideshow="(.+?)"').findall(link)
    reviewmatch       = re.compile('total_review="(.+?)"').findall(link)
    whufcleematch     = re.compile('whufclee_review="(.+?)"').findall(link)
    cbmatch           = re.compile('CB_Premium="(.+?)"').findall(link)
   
    name                  = namematch[0] if (len(namematch) > 0) else ''
    manufacturer          = manufacturermatch[0] if (len(manufacturermatch) > 0) else ''
    videoguide1           = videoguide1match[0] if (len(videoguide1match) > 0) else 'None'
    videoguide2           = videoguide2match[0] if (len(videoguide2match) > 0) else 'None'
    videoguide3           = videoguide3match[0] if (len(videoguide3match) > 0) else 'None'
    videoguide4           = videoguide4match[0] if (len(videoguide4match) > 0) else 'None'
    videoguide5           = videoguide5match[0] if (len(videoguide5match) > 0) else 'None'
    videolabel1           = videolabel1match[0] if (len(videolabel1match) > 0) else 'None'
    videolabel2           = videolabel2match[0] if (len(videolabel2match) > 0) else 'None'
    videolabel3           = videolabel3match[0] if (len(videolabel3match) > 0) else 'None'
    videolabel4           = videolabel4match[0] if (len(videolabel4match) > 0) else 'None'
    videolabel5           = videolabel5match[0] if (len(videolabel5match) > 0) else 'None'
    shop                  = shopmatch[0] if (len(shopmatch) > 0) else ''    
    description           = descmatch[0] if (len(descmatch) > 0) else ''
    screenshot1           = screenshot1match[0] if (len(screenshot1match) > 0) else ''
    screenshot2           = screenshot2match[0] if (len(screenshot2match) > 0) else ''
    screenshot3           = screenshot3match[0] if (len(screenshot3match) > 0) else ''
    screenshot4           = screenshot4match[0] if (len(screenshot4match) > 0) else ''
    screenshot5           = screenshot5match[0] if (len(screenshot5match) > 0) else ''
    screenshot6           = screenshot6match[0] if (len(screenshot6match) > 0) else ''
    screenshot7           = screenshot7match[0] if (len(screenshot7match) > 0) else ''
    screenshot8           = screenshot8match[0] if (len(screenshot8match) > 0) else ''
    screenshot9           = screenshot9match[0] if (len(screenshot9match) > 0) else ''
    screenshot10          = screenshot10match[0] if (len(screenshot10match) > 0) else ''
    screenshot11          = screenshot11match[0] if (len(screenshot11match) > 0) else ''
    screenshot12          = screenshot12match[0] if (len(screenshot12match) > 0) else ''
    screenshot13          = screenshot13match[0] if (len(screenshot13match) > 0) else ''
    screenshot14          = screenshot14match[0] if (len(screenshot14match) > 0) else ''
    added                 = addedmatch[0] if (len(addedmatch) > 0) else ''
    platform              = platformmatch[0] if (len(platformmatch) > 0) else ''
    chipset               = chipsetmatch[0] if (len(chipsetmatch) > 0) else ''
    guide                 = guidematch[0] if (len(guidematch) > 0) else 'None'
    preview               = previewmatch[0] if (len(previewmatch) > 0) else 'None'
    thumb                 = thumbmatch[0] if (len(thumbmatch) > 0) else ''
    stock                 = stockmatch[0] if (len(stockmatch) > 0) else ''
    CPU                   = cpumatch[0] if (len(cpumatch) > 0) else ''
    GPU                   = gpumatch[0] if (len(gpumatch) > 0) else ''
    RAM                   = rammatch[0] if (len(rammatch) > 0) else ''
    flash                 = flashmatch[0] if (len(flashmatch) > 0) else ''
    wifi                  = wifimatch[0] if (len(wifimatch) > 0) else ''
    bluetooth             = bluetoothmatch[0] if (len(bluetoothmatch) > 0) else ''
    LAN                   = lanmatch[0] if (len(lanmatch) > 0) else ''
    xbmc_version          = xbmcmatch[0] if (len(xbmcmatch) > 0) else ''
    pros                  = prosmatch[0] if (len(prosmatch) > 0) else ''
    cons                  = consmatch[0] if (len(consmatch) > 0) else ''
    library               = librarymatch[0] if (len(librarymatch) > 0) else ''
    fourk                 = fourkmatch[0] if (len(fourkmatch) > 0) else ''
    teneighty             = teneightymatch[0] if (len(teneightymatch) > 0) else ''
    seventwenty           = seventwentymatch[0] if (len(seventwentymatch) > 0) else ''
    threed                = threedmatch[0] if (len(threedmatch) > 0) else ''
    DTS                   = dtsmatch[0] if (len(dtsmatch) > 0) else ''
    BootTime              = bootmatch[0] if (len(bootmatch) > 0) else ''
    CopyFiles             = copyfilesmatch[0] if (len(copyfilesmatch) > 0) else ''
    CopyVideo             = copyvideomatch[0] if (len(copyvideomatch) > 0) else ''
    EthernetTest          = ethernetmatch[0] if (len(ethernetmatch) > 0) else ''
    Slideshow             = slideshowmatch[0] if (len(slideshowmatch) > 0) else ''
    review                = reviewmatch[0] if (len(reviewmatch) > 0) else ''
    whufcleevid           = whufcleematch[0] if (len(whufcleematch) > 0) else 'None'
    cb                    = cbmatch[0] if (len(cbmatch) > 0) else ''
    official_description  = str('[COLOR=dodgerblue]Added: [/COLOR]'+added+'[CR][COLOR=dodgerblue]Manufacturer: [/COLOR]'+manufacturer+'[CR][COLOR=dodgerblue]Supported Roms: [/COLOR]'+platform+'[CR][COLOR=dodgerblue]Chipset: [/COLOR]'+chipset+'[CR][COLOR=dodgerblue]CPU: [/COLOR]'+CPU+'[CR][COLOR=dodgerblue]GPU: [/COLOR]'+GPU+'[CR][COLOR=dodgerblue]RAM: [/COLOR]'+RAM+'[CR][COLOR=dodgerblue]Flash: [/COLOR]'+flash+'[CR][COLOR=dodgerblue]Wi-Fi: [/COLOR]'+wifi+'[CR][COLOR=dodgerblue]Bluetooth: [/COLOR]'+bluetooth+'[CR][COLOR=dodgerblue]LAN: [/COLOR]'+LAN+'[CR][CR][COLOR=yellow]About: [/COLOR]'+description+'[CR][CR][COLOR=yellow]Summary:[/COLOR][CR][CR][COLOR=dodgerblue]Pros:[/COLOR]    '+pros+'[CR][CR][COLOR=dodgerblue]Cons:[/COLOR]  '+cons+'[CR][CR][COLOR=yellow]Benchmark Results:[/COLOR][CR][CR][COLOR=dodgerblue]Boot Time:[/COLOR][CR]'+BootTime+'[CR][CR][COLOR=dodgerblue]Time taken to scan 1,000 movies (local NFO files):[/COLOR][CR]'+library+'[CR][CR][COLOR=dodgerblue]Copy 4,000 files (660.8MB) locally:[/COLOR][CR]'+CopyFiles+'[CR][CR][COLOR=dodgerblue]Copy a MP4 file (339.4MB) locally:[/COLOR][CR]'+CopyVideo+'[CR][CR][COLOR=dodgerblue]Ethernet Speed - Copy MP4 (339.4MB) from SMB share to device:[/COLOR][CR]'+EthernetTest+'[CR][CR][COLOR=dodgerblue]4k Playback:[/COLOR][CR]'+fourk+'[CR][CR][COLOR=dodgerblue]1080p Playback:[/COLOR][CR]'+teneighty+'[CR][CR][COLOR=dodgerblue]720p Playback:[/COLOR][CR]'+seventwenty+'[CR][CR][COLOR=dodgerblue]Audio Playback:[/COLOR][CR]'+DTS+'[CR][CR][COLOR=dodgerblue]Image Slideshow:[/COLOR][CR]'+Slideshow)
    official_description2 = str('[COLOR=dodgerblue]Added: [/COLOR]'+added+'[CR][COLOR=dodgerblue]Manufacturer: [/COLOR]'+manufacturer+'[CR][COLOR=dodgerblue]Supported Roms: [/COLOR]'+platform+'[CR][COLOR=dodgerblue]Chipset: [/COLOR]'+chipset+'[CR][COLOR=dodgerblue]CPU: [/COLOR]'+CPU+'[CR][COLOR=dodgerblue]GPU: [/COLOR]'+GPU+'[CR][COLOR=dodgerblue]RAM: [/COLOR]'+RAM+'[CR][COLOR=dodgerblue]Flash: [/COLOR]'+flash+'[CR][COLOR=dodgerblue]Wi-Fi: [/COLOR]'+wifi+'[CR][COLOR=dodgerblue]Bluetooth: [/COLOR]'+bluetooth+'[CR][COLOR=dodgerblue]LAN: [/COLOR]'+LAN+'[CR][CR][COLOR=yellow]About: [/COLOR]'+description+'[CR][CR][COLOR=yellow]Summary:[/COLOR][CR][CR][COLOR=dodgerblue]Pros:[/COLOR]    '+pros+'[CR][CR][COLOR=dodgerblue]Cons:[/COLOR]  '+cons+'[CR][CR][COLOR=orange]4k Playback:[/COLOR]  '+fourk+'[CR][CR][COLOR=orange]1080p Playback:[/COLOR]  '+teneighty+'[CR][CR][COLOR=orange]720p Playback:[/COLOR]  '+seventwenty+'[CR][CR][COLOR=orange]DTS Compatibility:[/COLOR]  '+DTS+'[CR][CR][COLOR=orange]Time taken to scan 100 movies:[/COLOR]  '+library)
    
    if description != '' and shop !='':
        o0oO('','[COLOR=yellow][Text Guide][/COLOR]  Official Description',official_description,'text_guide','',FANART,'','')    
    if description != '' and shop =='':
        o0oO('','[COLOR=yellow][Text Guide][/COLOR]  Official Description',official_description2,'text_guide','',FANART,'','')    
    if whufcleevid != 'None':
        o0oO('','[COLOR=lime][VIDEO][/COLOR]   Benchmark Review',whufcleevid,'play_video','',FANART,'','')    
    if preview != 'None':
        o0oO('','[COLOR=lime][VIDEO][/COLOR]   Official Video Preview',preview,'play_video','',FANART,'','')    
    if guide != 'None':
        o0oO('','[COLOR=lime][VIDEO][/COLOR]   Official Video Guide',guide,'play_video','',FANART,'','')    
    if videoguide1 != 'None':
        o0oO('','[COLOR=lime][VIDEO][/COLOR]  '+videolabel1,videoguide1,'play_video','',FANART,'','')
    if videoguide2 != 'None':
        o0oO('','[COLOR=lime][VIDEO][/COLOR]  '+videolabel2,videoguide2,'play_video','',FANART,'','')    
    if videoguide3 != 'None':
        o0oO('','[COLOR=lime][VIDEO][/COLOR]  '+videolabel3,videoguide3,'play_video','',FANART,'','')    
    if videoguide4 != 'None':
        o0oO('','[COLOR=lime][VIDEO][/COLOR]  '+videolabel4,videoguide4,'play_video','',FANART,'','')    
    if videoguide5 != 'None':
        o0oO('','[COLOR=lime][VIDEO][/COLOR]  '+videolabel5,videoguide5,'play_video','',FANART,'','')    
#---------------------------------------------------------------------------------------------------
#Hardware Root menu listings
def Hardware_Root_Menu():
    o0oO('folder','[COLOR=yellow]Manual Search[/COLOR]', 'hardware', 'manual_search', '','','','')
    o0oO('folder','[COLOR=lime]All Devices[/COLOR]', '', 'grab_hardware', '','','','')
    o0oO('folder','[COLOR=orange][Hardware][/COLOR] Game Consoles', 'device=Console', '', '','','','')
    o0oO('folder','[COLOR=orange][Hardware][/COLOR] HTPC', 'device=HTPC', 'grab_hardware', '','','','')
    o0oO('folder','[COLOR=orange][Hardware][/COLOR] Phones', 'device=Phone', 'grab_hardware', '','','','')
    o0oO('folder','[COLOR=orange][Hardware][/COLOR] Set Top Boxes', 'device=STB', 'grab_hardware', '','','','')
    o0oO('folder','[COLOR=orange][Hardware][/COLOR] Tablets', 'device=Tablet', 'grab_hardware', '','','','')
    o0oO('folder','[COLOR=dodgerblue][Accessories][/COLOR] Remotes/Keyboards', 'device=Remote', 'grab_hardware', '','','','')
    o0oO('folder','[COLOR=dodgerblue][Accessories][/COLOR] Gaming Controllers', 'device=Controller', 'grab_hardware', '','','','')
    o0oO('folder','[COLOR=dodgerblue][Accessories][/COLOR] Dongles', 'device=Dongle', 'grab_hardware', '','','','')
#---------------------------------------------------------------------------------------------------
#CPU Root menu listings
def Hardware_Filter_Menu(url):
    o0oO('folder','[COLOR=yellow][CPU][/COLOR] Allwinner Devices', str(url)+'&chip=Allwinner', 'grab_hardware', '','','','')
    o0oO('folder','[COLOR=yellow][CPU][/COLOR] AMLogic Devices', str(url)+'&chip=AMLogic', 'grab_hardware', '','','','')
    o0oO('folder','[COLOR=yellow][CPU][/COLOR] Intel Devices', str(url)+'&chip=Intel', 'grab_hardware', '','','','')
    o0oO('folder','[COLOR=yellow][CPU][/COLOR] Rockchip Devices', str(url)+'&chip=Rockchip', 'grab_hardware', '','','','')
    o0oO('folder','[COLOR=lime][Platform][/COLOR] Android', str(url)+'&platform=Android', 'grab_hardware', '','','','')
    o0oO('folder','[COLOR=lime][Platform][/COLOR] iOS', str(url)+'&platform=iOS', 'grab_hardware', '','','','')
    o0oO('folder','[COLOR=lime][Platform][/COLOR] Linux', str(url)+'&platform=Linux', 'grab_hardware', '','','','')
    o0oO('folder','[COLOR=lime][Platform][/COLOR] OpenELEC', str(url)+'&platform=OpenELEC', 'grab_hardware', '','','','')
    o0oO('folder','[COLOR=lime][Platform][/COLOR] OSX', str(url)+'&platform=OSX', 'grab_hardware', '','','','')
    o0oO('folder','[COLOR=lime][Platform][/COLOR] Pure Linux', str(url)+'&platform=Custom_Linux', 'grab_hardware', '','','','')
    o0oO('folder','[COLOR=lime][Platform][/COLOR] Windows', str(url)+'&platform=Windows', 'grab_hardware', '','','','')
    o0oO('folder','[COLOR=orange][Flash Storage][/COLOR] 4GB', str(url)+'&flash=4GB', 'grab_hardware', '','','','')
    o0oO('folder','[COLOR=orange][Flash Storage][/COLOR] 8GB', str(url)+'&flash=8GB', 'grab_hardware', '','','','')
    o0oO('folder','[COLOR=orange][Flash Storage][/COLOR] 16GB', str(url)+'&flash=16GB', 'grab_hardware', '','','','')
    o0oO('folder','[COLOR=orange][Flash Storage][/COLOR] 32GB', str(url)+'&flash=32GB', 'grab_hardware', '','','','')
    o0oO('folder','[COLOR=orange][Flash Storage][/COLOR] 64GB', str(url)+'&flash=64GB', 'grab_hardware', '','','','')
    o0oO('folder','[COLOR=dodgerblue][RAM][/COLOR] 1GB', str(url)+'&ram=1GB', 'grab_hardware', '','','','')
    o0oO('folder','[COLOR=dodgerblue][RAM][/COLOR] 2GB', str(url)+'&ram=2GB', 'grab_hardware', '','','','')
    o0oO('folder','[COLOR=dodgerblue][RAM][/COLOR] 4GB', str(url)+'&ram=4GB', 'grab_hardware', '','','','')
#-----------------------------------------------------------------------------------------------------------------
# Menu to install content via the CP add-on
def Install_Content(url):
    o0oO('folder','[COLOR=orange]noobs[/COLOR][COLOR=dodgerblue]and[/COLOR][COLOR=orange]nerds[/COLOR] Keywords', '', 'nan_menu', '','','','')

    if addonportal == 'true':
        o0oO('folder','Manage Add-ons','','addonmenu', '','','','')
    
    if commbuilds == 'true':
        o0oO('folder','Community Builds', url, 'community', '','','','')
#---------------------------------------------------------------------------------------------------
#Step 2 of the addon install process (installs the repo if one exists)
def Install_Repo(repo_id):
    repostatus   = 1
    BaseURL      = 'http://noobsandnerds.com/TI/AddonPortal/dependencyinstall.php?id=%s' % (repo_id)
    link         = Open_URL(BaseURL).replace('\n','').replace('\r','')
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
    repopath = xbmc.translatePath(os.path.join(USERDATA,'plugin_data','programs','Addons4Xbox Installer','repositories'))
    repolocation = xbmc.translatePath(os.path.join(repopath,repoid))

    dp.create('Installing Repository','Please wait...','')
    
    try:
        downloader.download(repourl, repozipname, dp)
        extract.all(repozipname, repopath, dp)
    
    except:
        
        try:
            downloader.download(zipurl, repozipname, dp)
            extract.all(repozipname, repopath, dp)
        
        except:
            
            try:
                
                if not os.path.exists(repolocation):
                    os.makedirs(repolocation)
                
                link = Open_URL(dataurl).replace('\n','').replace('\r','')
                match=re.compile('href="(.+?)"', re.DOTALL).findall(link)
                
                for href in match:
                    filepath=xbmc.translatePath(os.path.join(repolocation,href))
                    
                    if addon_id not in href and '/' not in href:
                        
                        try:
                            dp.update(0,"Downloading [COLOR=yellow]"+href+'[/COLOR]','','Please wait...')
                            downloader.download(dataurl+href, filepath, dp)
                        
                        except: print"failed to install"+href
                    
                    if '/' in href and '..' not in href and 'http' not in href:
                        remote_path = dataurl+href
                        Recursive_Loop(filepath,remote_path)
            
            except:
                dialog.ok("Error downloading repository", 'There was an error downloading[CR][COLOR=dodgerblue]'+reponame+'[/COLOR]. Please consider updating the add-on portal with details or report the error on the forum at [COLOR=orange]www.noobs[/COLOR][COLOR=dodgerblue]and[/COLOR][COLOR=orange]nerds.com[/COLOR]')
                repostatus=0
    
# If repository successfully installed add increment
    if repostatus==1:
        time.sleep(1)
        dp.update(0,"[COLOR=yellow]"+reponame+'[/COLOR]  [COLOR=lime]Successfully Installed[/COLOR]','','Now installing dependencies')
        time.sleep(1)
        incremental = 'http://noobsandnerds.com/TI/AddonPortal/downloadcount.php?id=%s' % (repo_id)
        Open_URL(incremental)
#---------------------------------------------------------------------------------------------------
#Create How To (instructions) menu
def Instructions():
    o0oO('','[COLOR=dodgerblue][TEXT GUIDE][/COLOR]  What is Community Builds?','url','instructions_3','','','','')
    o0oO('','[COLOR=dodgerblue][TEXT GUIDE][/COLOR]  Creating a Community Build','url','instructions_1','','','','')
    o0oO('','[COLOR=dodgerblue][TEXT GUIDE][/COLOR]  Installing a Community Build','url','instructions_2','','','','')
    o0oO('','[COLOR=lime][VIDEO GUIDE][/COLOR]  Add Your Own Guides @ [COLOR=orange]www.noobs[/COLOR][COLOR=dodgerblue]and[/COLOR][COLOR=orange]nerds.com[/COLOR]','K0XIxEodUhc','play_video','','','','')
    o0oO('','[COLOR=lime][VIDEO GUIDE][/COLOR]  Community Builds FULL GUIDE',"ewuxVfKZ3Fs",'play_video','','','','')
    o0oO('','[COLOR=lime][VIDEO GUIDE][/COLOR]  IMPORTANT initial settings',"1vXniHsEMEg",'play_video','','','','')
    o0oO('','[COLOR=lime][VIDEO GUIDE][/COLOR]  Install a Community Build',"kLsVOapuM1A",'play_video','','','','')
    o0oO('','[COLOR=lime][VIDEO GUIDE][/COLOR]  Fixing a half installed build (guisettings.xml fix)',"X8QYLziFzQU",'play_video','','','','')
    o0oO('','[COLOR=lime][VIDEO GUIDE][/COLOR]  [COLOR=yellow](OLD METHOD)[/COLOR]Create a Community Build (part 1)',"3rMScZF2h_U",'play_video','','','','')
    o0oO('','[COLOR=lime][VIDEO GUIDE][/COLOR]  [COLOR=yellow](OLD METHOD)[/COLOR]Create a Community Build (part 2)',"C2IPhn0OSSw",'play_video','','','','')
#---------------------------------------------------------------------------------------------------
#(Instructions) Create a community backup
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
#(Instructions) Install a community build   
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
#(Instructions) What is a keyword
def Instructions_3():
    Text_Boxes('What is a noobsandnerds keyword?', '[COLOR=gold]WHAT IS A KEYWORD?[/COLOR][CR]The noobsandnerds keywords are based on the ingenious TLBB keyword system that was introduced years ago. It\'s nothing new and unlike certain other people out there we\'re not going to claim it as our idea. If you\'re already familiar with TLBB Keywords or even some of the copies out there like Cloudwords you will already know how this works but for those of you that don\'t have one of those devices we\'ll just go through the details...'
    '[CR][CR]Anyone in the community can make their own keywords and share them with others, it\'s a simple word you type in and then the content you uploaded to the web is downloaded and installed. Previously keywords have mostly been used for addon packs, this is a great way to get whole packs of addons in one go without the need to install a whole new build. We are taking this to the next level and will be introducing artwork packs and also addon fixes. More details will be available in the Community Portal section of the forum on www.noobsandnerds.com'
    '[CR][CR][CR][COLOR=gold]HOW DO I FIND A KEYWORD?[/COLOR][CR]The full list of noobsandnerds keywords can be found on the forum, in the Community Portal section you\'ll see a section for the keywords at the top of the page. Just find the pack you would like to install then using this addon type the keyword in when prompted (after clicking "Install a noobsandnerds keyword"). Your content will now be installed, if installing addon packs please be patient while each addon updates to the latest version directly from the developers repo.'
    '[CR][CR][CR][COLOR=gold]CAN I USE OTHER KEYWORDS?[/COLOR] (Cloudwords, TLBB etc.)[CR]Yes you can, just go to the addon settings and enter the url shortener that particular company use. Again you will find full details of supported keywords on the forum.')
#---------------------------------------------------------------------------------------------------
#(Instructions) How to create a keyword
def Instructions_4():
    Text_Boxes('How to create a keyword?', '[COLOR=gold]NaN MAKE IT EASY![/COLOR][CR]The keywords can now be made very simply by anyone. We\'ve not locked this down to just our addon and others can use this on similar systems for creating keywords if they want...'
    '[CR][CR][COLOR=dodgerblue][B]Step 1:[/COLOR] Use a vanilla Kodi setup[/B][CR]You will require a complete fresh install of Kodi with absolutely nothing else installed and running the default skin. Decide what kind of pack you want to create, lets say we want to create a kids pack... Add all the kid related addons you want and make sure you also have the relevant repository installed too. In the unlikely event you\'ve found an addon that doesn\'t belong in a repository that\'s fine the system will create a full backup of that addon too (just means it won\'t auto update with future updates to the addon).'
    '[CR][CR][COLOR=dodgerblue][B]Step 2:[/COLOR] Create the backup[/B][CR]Using this addon create your backup, currently only addon packs are supported but soon more packs will be added. When you create the keyword you\'ll be asked for a location to store the zip file that will be created and a name, this can be anywhwere you like and can be called whatever you want - you do not need to add the zip extension, that will automatically be added for you so in our example here we would call it "kids".'
    '[CR][CR][COLOR=dodgerblue][B]Step 3:[/COLOR] Upload the zips[/B][CR]Upload the two zip file to a server that Kodi can access, it has to be a direct link and not somewhere that asks for captcha - archive.org and copy.com are two good examples. Do not use Dropbox unless you have a paid account, they have a fair useage policy and the chances are you\'ll find within 24 hours your download has been blocked and nobody can download it.[CR][CR][COLOR=lime]Top Tip: [/COLOR]The vast majority of problems occur when the wrong download URL has been entered in the online form, a good download URL normally ends in "=1" or "zip=true". Please double check when you copy the URL into a web browser it immediately starts downloading without the need to press any other button.'
    '[CR][CR][COLOR=dodgerblue][B]Step 4:[/COLOR] Create the keyword[/B][CR]Copy the download URL to your clipboard and then go to www.urlshortbot.com. In here you need to enter the URL in the "Long URL" field and then in the "Custom Keyword" field you need to enter "noobs" (without the quotation marks) followed by your keyword. We recommend always using a random test keyword for testing because once you have a keyword you can\'t change it, also when uploading make sure it\'s a link you can edit and still keep the same URL - that way it\'s easy to keep up to date and you can still use the same keyword. In our example of kids we would set the custom keyword as "noobskids". The noobs bit is ignored and is only for helping the addon know what to look for, the user would just type in "kids" for the kids pack to be installed.')
#---------------------------------------------------------------------------------------------------
#(Instructions) Adding other wizards
def Instructions_5():
    Text_Boxes('Adding Third Party Wizards', '[COLOR=gold]ONE WIZARD TO RULE THEM ALL![/COLOR][CR]Did you know the vast majority of wizards out there (every single one we\'ve tested) has just been a copy/paste of very old code created by the team here? We\'ve noticed a lot of the users installing builds via these third party wizards have run into many different problems so we thought we\'d take it upon ourselves to help out...'
    '[CR][CR][CR][COLOR=gold]WHAT BENEFITS DOES THIS HAVE?[/COLOR][CR]We\'ve added extra code that checks for common errors, unfortunately there are some people out there using inferior programs to create their backups and that is causing problems in their wizards. If such a problem exists when trying to use another wizard you can try adding the details to this addon and it automatically fixes any corrupt files it finds. Of course there are other benefits... installing code from an unknown source can give the author access to your system so make sure you always trust the author(s). Why take the risk of installing wizards created by anonymous usernames on social media sites when you can install from a trusted source like noobsandnerds and you\'ll also be safe in the knowledge that any new updates and improvements will be made here first - we do not copy/paste code, we are actively creating new exciting solutions!'
    '[CR][CR][CR][COLOR=gold]ADDING 3RD PARTY WIZARDS TO THIS ADDON[/COLOR][CR][CR][COLOR=dodgerblue][B]Step 1:[/COLOR] Enabling 3rd Party Wizards[/B][CR]In the addon settings under the Community Builds section you have the option to enable third party community builds, if you click on this you will be able to enter details of up to 5 different wizards.'
    '[CR][CR][COLOR=dodgerblue][B]Step 2:[/COLOR] Enter the URL[/B][CR]As virtually all wizards use exactly the same structure all you need to do is find out what URL they are looking up in the code, you can open the default.py file of the wizard in a text editor and search for "http" and you will more than likely find the URL straight away. Try entering it in a web address, it should show the details for all the builds in that wizard in a text based page. If the page is blank don\'t worry it may just be locked from web browsers and can only be opened in Kodi, try it out and see if it works.'
    '[CR][CR][COLOR=dodgerblue][B]Step 3:[/COLOR] Enter the name[/B][CR]Give the wizard a name, now when you go into the Community Builds section you\'ll have the official noobsandnerds builds as an option and also any new ones you\'ve added.')
#-----------------------------------------------------------------------------------------------------------------
#Thanks to metalkettle for his work on the original IP checker addon        
def IP_Check(url='http://www.iplocation.net/',inc=1):
    match=re.compile("<td width='80'>(.+?)</td><td>(.+?)</td><td>(.+?)</td><td>.+?</td><td>(.+?)</td>").findall(net.http_GET(url).content)
    for ip, region, country, isp in match:
        if inc <2: dialog=xbmcgui.Dialog(); dialog.ok('Check My IP',"[B][COLOR gold]Your IP Address is: [/COLOR][/B] %s" % ip, '[B][COLOR gold]Your IP is based in: [/COLOR][/B] %s' % country, '[B][COLOR gold]Your Service Provider is:[/COLOR][/B] %s' % isp)
        inc=inc+1
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
            print"Attempting download "+downloadurl+" to "+lib
            dp.create("Web Installer","Downloading ",'', 'Please Wait')
            downloader.download(downloadurl,lib)
            print"### Keyword "+keyword+" Successfully downloaded"
            dp.update(0,"", "Extracting Zip Please Wait")
            
            if zipfile.is_zipfile(lib):
                
                try:
                    extract.all(lib,HOME,dp)
                    xbmc.executebuiltin('UpdateLocalAddons')
                    xbmc.executebuiltin( 'UpdateAddonRepos' )
                    dialog.ok("[COLOR=orange]noobs[/COLOR][COLOR=dodgerblue]and[/COLOR][COLOR=orange]nerds[/COLOR]", "","Content now installed", "")
                    dp.close()
                
                except:
                    dialog.ok("Error with zip",'There was an error trying to install this file. It may possibly be corrupt, either try again or contact the author of this keyword.')
                    print"### Unable to install keyword (passed zip check): "+keyword
            else:
                dialog.ok("Keyword Error",'The keyword you typed could not be installed. Please check the spelling and if you continue to receive this message it probably means that keyword is no longer available.')
            
        except:
            dialog.ok("Keyword Error",'The keyword you typed could not be installed. Please check the spelling and if you continue to receive this message it probably means that keyword is no longer available.')
            print"### Unable to install keyword (unknown error, most likely a typo in keyword entry): "+keyword
    
    if os.path.exists(lib):
        os.remove(lib)
#-----------------------------------------------------------------------------------------------------------------
#Create a FULL backup
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
    exclude_dirs_full  =  [AddonName]
    exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf','Thumbs.db','.gitignore']
    message_header     = "Creating full backup of existing build"
    message_header2    = "Creating Community Build"
    message1           = "Archiving..."
    message2           = ""
    message3           = "Please Wait"
    
    Archive_Tree(HOME, myfullbackup, message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)
    dialog.ok('Full Backup Complete','You can locate your backup at:[COLOR=dodgerblue]',myfullbackup+'[/COLOR]')
#---------------------------------------------------------------------------------------------------
# View the log from within XBMC4Xbox
def Log_Viewer():
    log = os.path.join(log_path, 'xbmc.log')
    Text_Boxes('XBMC Log', log)
#---------------------------------------------------------------------------------------------------
# Dialog to warn users about local guisettings fix.
def Local_GUI_Dialog():
    dialog.ok("Restore local guisettings fix", "You should [COLOR=lime]ONLY[/COLOR] use this option if the guisettings fix is failing to download via the addon. Installing via this method means you do not receive notifications of updates")
    Restore_Local_GUI()
#---------------------------------------------------------------------------------------------------
#Search in description
def Manual_Search(mode):
    if not mode.endswith("premium") and not mode.endswith("public") and not mode.endswith("private"):
        vq = Get_Keyboard( heading="Search for content" )
        
        if ( not vq ):
            return False, 0
        
        title = urllib.quote_plus(vq)
        
        if mode == 'tutorials':
            Grab_Tutorials('name='+title)
        
        if mode == 'hardware':
            Grab_Hardware('name='+title)
        
        if mode == 'news':
            Grab_News('name='+title)
    
    if mode.endswith("premium") or mode.endswith("public") or mode.endswith("private"):
        o0oO('folder','Search By Name',mode+'&name=','search_builds','','','','')
        o0oO('folder','Search By Uploader',mode+'&author=','search_builds','','','','')
        o0oO('folder','Search By Audio Addons Installed',mode+'&audio=','search_builds','','','','')
        o0oO('folder','Search By Picture Addons Installed',mode+'&pics=','search_builds','','','','')
        o0oO('folder','Search By Program Addons Installed',mode+'&progs=','search_builds','','','','')
        o0oO('folder','Search By Video Addons Installed',mode+'&vids=','search_builds','','','','')
        o0oO('folder','Search By Skins Installed',mode+'&skins=','search_builds','','','','')
#-----------------------------------------------------------------------------------------------------------------
# NaN Keyword menu
def NaN_Menu():
    o0oO('','[COLOR=gold][INSTALL][/COLOR] [COLOR=orange]noobs[/COLOR][COLOR=dodgerblue]and[/COLOR][COLOR=orange]nerds[/COLOR] Keyword', 'http://urlshortbot.com/noobsxbox', 'keywords', '','','','')
    o0oO('','[COLOR=gold][CREATE][/COLOR] [COLOR=orange]noobs[/COLOR][COLOR=dodgerblue]and[/COLOR][COLOR=orange]nerds[/COLOR] Keyword', '', 'create_keyword', '','','','')
    o0oO('','[COLOR=dodgerblue][INSTRUCTIONS][/COLOR] Installing a keyword','','instructions_3','','','','')
    o0oO('','[COLOR=dodgerblue][INSTRUCTIONS][/COLOR] Creating a keyword','','instructions_4','','','','')
#-----------------------------------------------------------------------------------------------------------------
# This creates the final menu showing build details, video and install link
def News_Menu(url):
    BaseURL      = 'http://noobsandnerds.com/TI/LatestNews/LatestNews.php?id=%s' % (url)
    link         = Open_URL(BaseURL).replace('\n','').replace('\r','')
    namematch    = re.compile('name="(.+?)"').findall(link)
    authormatch  = re.compile('author="(.+?)"').findall(link)
    datematch    = re.compile('date="(.+?)"').findall(link)
    contentmatch = re.compile('content="(.+?)###END###"').findall(link)
   
    name        = namematch[0] if (len(namematch) > 0) else ''
    author      = authormatch[0] if (len(authormatch) > 0) else ''
    date        = datematch[0] if (len(datematch) > 0) else ''
    content     = contentmatch[0] if (len(contentmatch) > 0) else ''
    clean_text  = Clean_HTML(content)
    description = str('[COLOR=orange]Source: [/COLOR]'+author+'     [COLOR=orange]Date: [/COLOR]'+date+'[CR][CR][COLOR=lime]Details: [/COLOR][CR]'+clean_text)
    
    Text_Boxes(name,description)
#---------------------------------------------------------------------------------------------------
#News Menu
def News_Root_Menu(url):
    o0oO('folder','[COLOR=yellow]Manual Search[/COLOR]', 'news', 'manual_search', '','','','')
    o0oO('folder','[COLOR=lime][All News][/COLOR] From all sites', str(url)+'', 'grab_news', '','','','')
    o0oO('folder','Official Kodi.tv News', str(url)+'&author=Official%20Kodi', 'grab_news', '','','','')
    o0oO('folder','OpenELEC News', str(url)+'&author=OpenELEC', 'grab_news', '','','','')
    o0oO('folder','Raspbmc News', str(url)+'&author=Raspbmc', 'grab_news', '','','','')
    o0oO('folder','[COLOR=orange]noobs[/COLOR][COLOR=dodgerblue]and[/COLOR][COLOR=orange]nerds[/COLOR] News', str(url)+'&author=noobsandnerds', 'grab_news', '','','','')
    o0oO('folder','XBMC4Xbox News', str(url)+'&author=XBMC4Xbox', 'grab_news', '','','','')
#-----------------------------------------------------------------------------------------------------------------
# All credit goes to DanDar3 for the Notepad plugin, it was hard to track down so I've put it in here so it doesn't get lost and forgotten
def Notepad():
    if ( "action=edit" in sys.argv[ 2 ] ):
    #
    # Check if a file was passed as a parameter...
    #
        params = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split('&'))
        file   = urllib.unquote_plus( params.get( "file", "" ) )
    #
    # Browse for movie file...
    #
        if file == "" :
            browse = xbmcgui.Dialog()
            file   = browse.browse(1, xbmc.getLocalizedString(30200), "files", "")
    #
    # Open in editor window...
    #
        if file != "" :   
            import notepad_edit as plugin
            gui = plugin.GUI( "notepad_edit.xml", os.getcwd(), "default", file=file)
            gui.doModal()
            del gui
            xbmc.executebuiltin("Container.Refresh")
#
# Main menu
#
    else :
        import notepad_main as plugin
        plugin.Main()   
        
class NotepadMain:
    def __init__( self ):
        #
        # Open file...
        #
        listitem = xbmcgui.ListItem( xbmc.getLocalizedString(30001), iconImage="DefaultFolder.png" )
        ok = xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1] ), url = sys.argv[ 0 ] + '?action=edit', listitem=listitem, isFolder=False)

        #
        # Recent files...
        #
        try :
            recent_files = eval( xbmcplugin.getSetting( "recent_files" ) )
        except :
            recent_files = []
        
        for file in recent_files :
            listitem = xbmcgui.ListItem( file, iconImage="DefaultFile.png" )
            xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), 
                                         url = '%s?action=edit&file=%s' % ( sys.argv[ 0 ], urllib.quote_plus( file) ), 
                                         listitem=listitem, 
                                         isFolder=False )

        #
        # Disable sorting...
        #
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

        #
        # End of list...
        #        
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )        
#-----------------------------------------------------------------------------------------------------------------
#Simple shortcut to create a notification
def Notify(title,message,times,icon):
    icon = notifyart+icon
    xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")
#---------------------------------------------------------------------------------------------------
##Function to create a text box
def Open_URL(url):
    req = urllib2.Request(url)
 #   req.add_header('User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 10.0; WOW64; Windows NT 5.1; en-GB; rv:1.9.0.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36 Gecko/2008092417 Firefox/3.0.3')
    req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req,timeout=60)
    link     = response.read()
    response.close()
    return link.replace('\r','').replace('\n','').replace('\t','')
#---------------------------------------------------------------------------------------------------
#Platform tutorial menu
def Platform_Menu(url):
    o0oO('folder','[COLOR=yellow]1. Install:[/COLOR]  Installation tutorials (e.g. flashing a new OS)', str(url)+'&thirdparty=InstallTools', 'grab_tutorials', '','','','')
    o0oO('folder','[COLOR=dodgerblue]Add-on Tools:[/COLOR]  Add-on maintenance and coding tutorials', str(url)+'&thirdparty=AddonTools', 'grab_tutorials', '','','','')
    o0oO('folder','[COLOR=dodgerblue]Audio Tools:[/COLOR]  Audio related tutorials', str(url)+'&thirdparty=AudioTools', 'grab_tutorials', '','','','')
    o0oO('folder','[COLOR=dodgerblue]Gaming Tools:[/COLOR]  Integrate a gaming section into your setup', str(url)+'&thirdparty=GamingTools', 'grab_tutorials', '','','','')
    o0oO('folder','[COLOR=dodgerblue]Image Tools:[/COLOR]  Tutorials to assist with your pictures/photos', str(url)+'&thirdparty=ImageTools', 'grab_tutorials', '','','','')
    o0oO('folder','[COLOR=dodgerblue]Library Tools:[/COLOR]  Music and Video Library Tutorials', str(url)+'&thirdparty=LibraryTools', 'grab_tutorials', '','','','')
    o0oO('folder','[COLOR=dodgerblue]Skinning Tools:[/COLOR]  All your skinning advice', str(url)+'&thirdparty=SkinningTools', 'grab_tutorials', '','','','')
    o0oO('folder','[COLOR=dodgerblue]Video Tools:[/COLOR]  All video related tools', str(url)+'&thirdparty=VideoTools', 'grab_tutorials', '','','','')
#---------------------------------------------------------------------------------------------------
#Set popup xml based on platform
def pop(xmlfile):
# if popup is an advert from the web
    if 'http' in xmlfile:
        contents = 'none'
        filedate = xmlfile[-10:]
        filedate = filedate[:-4]
        latest = os.path.join(ADDON_DATA,'programs',AddonName,'latest')

        if os.path.exists(latest):
            readfile = open(latest, mode='r')
            contents = readfile.read()
            readfile.close()

        if contents == filedate:
            filedate = contents
                
        else:
            downloader.download(xmlfile,os.path.join(ADDONS,'programs',AddonName,'resources','skins','DefaultSkin','media','latest.jpg'))
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
    
    link   = Open_URL(remote_path).replace('\n','').replace('\r','')
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
#Dialog to tell users how to register
def Register():
    dialog.ok("Register to unlock features", 'To get the most out of this addon please register at the','[COLOR=orange]noobs[/COLOR][COLOR=dodgerblue]and[/COLOR][COLOR=orange]nerds[/COLOR] forum for free.','www.noobsandnerds.com')
#---------------------------------------------------------------------------------------------------
#Function to restore a zip file 
def Remove_Build():
    Check_Download_Path()
    filename = xbmcgui.Dialog().browse(1, 'Select the backup file you want to DELETE', 'files', '.zip', False, False, USB)
    
    if filename != USB:
        clean_title = ntpath.basename(filename)
        choice = xbmcgui.Dialog().yesno('Delete Backup File', 'This will completely remove '+clean_title, 'Are you sure you want to delete?', '', nolabel='No, Cancel',yeslabel='Yes, Delete')
        
        if choice == 1:
            os.remove(filename)
#---------------------------------------------------------------------------------------------------
#Function to clear the packages folder
def Remove_Packages():
    choice = xbmcgui.Dialog().yesno('Delete Packages Folder', 'Do you want to clean the packages folder? This will free up space by deleting the old zip install files of your addons. Keeping these files can also sometimes cause problems when reinstalling addons', nolabel='Cancel',yeslabel='Delete')
    
    if choice == 1:
        Delete_Packages()
        dialog.ok("Packages Removed", '', 'Your zip install files have now been removed.','')
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
#Function to restore a community build
def Restore_Community(name,url,video,description,skins,guisettingslink,artpack):
    path = xbmc.translatePath(os.path.join('special://home/plugins','packages'))
    dp.create("[COLOR dodgerblue]Installing Your Build[/COLOR] [COLOR lime]Please Wait[/COLOR]","Downloading ",'', 'Please Wait')
    lib=os.path.join(path, name+'.zip')
    try:
       os.remove(lib)
    except:
       pass
    downloader.download(url, lib, dp)
    title       = 'Enter New Directory Name For This Build'
    newbuild     = SEARCH(title)
    addonfolder = xbmc.translatePath(os.path.join(xbmcdir,newbuild))
    if not os.path.exists(addonfolder):
        os.makedirs(addonfolder)
    xbe = os.path.join(addonfolder,'default.xbe')
    dp.update(0,"", "Extracting Zip Please Wait")
    print '======================================='
    print addonfolder
    print '======================================='
    extract.all(lib,addonfolder,dp)
    dialog = xbmcgui.Dialog()
    choice = dialog.yesno("BUILD INSTALL SUCCESS", 'Congratulations your new build has been installed. Would','you like to test it out now? If you like it and want to','make it your default dash please use XBMC4Xbox Installer')
    if choice == 1:
        xbmc.executebuiltin('RunXBE('+xbe+')')
#---------------------------------------------------------------------------------------------------
#Function to restore a local backup
def Restore_Local_Community(url):
    exitfunction = 0
    print"Restore Location: "+url
#Show disclaimer
#    pop('noobsandnerds.xml')

    Check_Download_Path()

    if url == 'local':
        filename = xbmcgui.Dialog().browse(1, 'Select the backup file you want to restore', 'files', '.zip', False, False, USB)
        if filename == '':
            exitfunction = 1

    if exitfunction == 1:
        print"### No file selected, quitting restore process ###"
        return
    
    elif exitfunction == 0:

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
            
        title       = 'Enter New Directory Name For This Build'
        newbuild    = SEARCH(title)
        dp.create("[COLOR dodgerblue]Installing Your Build[/COLOR] [COLOR lime]Please Wait[/COLOR]","Downloading ",'', 'Please Wait')
        addonfolder = xbmc.translatePath(os.path.join(xbmcdir,newbuild))
        if not os.path.exists(addonfolder):
            os.makedirs(addonfolder)
        xbe = os.path.join(addonfolder,'default.xbe')
        dp.update(0,"", "Extracting Zip Please Wait")
        print '======================================='
        print addonfolder
        print '======================================='
        try:
            extract.all(filename,addonfolder,dp)
            dp.update(0,"", "Extracting Zip Please Wait")
            choice = dialog.yesno("BUILD INSTALL SUCCESS", 'Congratulations your new build has been installed. Would','you like to test it out now? If you like it and want to','make it your default dash please use XBMC4Xbox Installer')
            if choice == 1:
                xbmc.executebuiltin('RunXBE('+xbe+')')
        except:
            dialog.ok('ERROR IN BUILD ZIP','Please contact the build author, there are errors in this zip file that has caused the install process to fail. Most likely cause is it contains files with special characters in the name.')
            return
#---------------------------------------------------------------------------------------------------
#Create restore menu
def Restore_Option():
    Check_Local_Install()
    o0oO('','[COLOR=dodgerblue]Restore A Locally stored build[/COLOR]','local','restore_local_CB','','','','Restore A Full System Backup')
    
    if os.path.exists(os.path.join(USB,'addons.zip')):   
        o0oO('','Restore Your Addons','addons','restore_zip','','','','Restore Your Addons')

    if os.path.exists(os.path.join(USB,'addon_data.zip')):   
        o0oO('','Restore Your Addon UserData','addon_data','restore_zip','','','','Restore Your Addon UserData')           

    if os.path.exists(os.path.join(USB,'guisettings.xml')):
        o0oO('','Restore Guisettings.xml',GUI,'resore_backup','','','','Restore Your guisettings.xml')
    
    if os.path.exists(os.path.join(USB,'favourites.xml')):
        o0oO('','Restore Favourites.xml',FAVS,'resore_backup','','','','Restore Your favourites.xml')
        
    if os.path.exists(os.path.join(USB,'sources.xml')):
        o0oO('','Restore Source.xml',SOURCE,'resore_backup','','','','Restore Your sources.xml')
        
    if os.path.exists(os.path.join(USB,'advancedsettings.xml')):
        o0oO('','Restore Advancedsettings.xml',ADVANCED,'resore_backup','','','','Restore Your advancedsettings.xml')        

    if os.path.exists(os.path.join(USB,'keyboard.xml')):
        o0oO('','Restore Advancedsettings.xml',KEYMAPS,'resore_backup','','','','Restore Your keyboard.xml')
        
    if os.path.exists(os.path.join(USB,'RssFeeds.xml')):
        o0oO('','Restore RssFeeds.xml',RSS,'resore_backup','','','','Restore Your RssFeeds.xml')    
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
                    if not AddonName in dirs:
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

        if 'Backup' in name:
            dialog.ok("Install Complete", 'Your Xbox will now reboot and all changes will','automatically take affect on the restart.')
            xbmc.executebuiltin('reboot')

        else:
            dialog.ok("SUCCESS", "Task completed", '','')        
#---------------------------------------------------------------------------------------------------
# Basic function to run an add-on
def Run_Addon(url):
    xbmc.executebuiltin('RunAddon('+url+')')
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
#---------------------------------------------------------------------------------------------------#---------------------------------------------------------------------------------------------------
# Check local file version name and number against db
def Show_Info(url):
    BaseURL      = 'http://noobsandnerds.com/TI/Community_Builds/community_builds.php?id=%s' % (url)
    link         = Open_URL(BaseURL).replace('\n','').replace('\r','')
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
        print"### Could not find build No. "+url
        dialog.ok('Build Not Found','Sorry we couldn\'t find the build, it may be it\'s marked as private. Please try manually searching via the Community Builds section')
#---------------------------------------------------------------------------------------------------
# Check local file version name and number against db
def Show_Info2(url):
    dialog.ok("This build is not complete",'The guisettings.xml file was not copied over during the last install process. Click OK to go to the build page and complete Install Step 2 (guisettings fix).')

    try:
        Community_Menu(url+'&visibility=homepage',url)

    except:
        return
        print"### Could not find build No. "+url
        dialog.ok('Build Not Found','Sorry we couldn\'t find the build, it may be it\'s marked as private. Please try manually searching via the Community Builds section')
#---------------------------------------------------------------------------------------------------
#Show User Info dialog
def Show_User_Info():
    BaseURL       = 'http://noobsandnerds.com/TI/login/login_details.php?user=%s&pass=%s' % (username, password)
    link          = Open_URL(BaseURL).replace('\n','').replace('\r','')
    postsmatch    = re.compile('posts="(.+?)"').findall(link)
    messagesmatch = re.compile('messages="(.+?)"').findall(link)
    unreadmatch   = re.compile('unread="(.+?)"').findall(link)
    emailmatch    = re.compile('email="(.+?)"').findall(link)
    messages      = messagesmatch[0] if (len(messagesmatch) > 0) else ''
    unread        = unreadmatch[0] if (len(unreadmatch) > 0) else ''
    email         = emailmatch[0] if (len(emailmatch) > 0) else ''
    posts         = postsmatch[0] if (len(postsmatch) > 0) else ''
    dialog.ok('[COLOR=orange]noobs[/COLOR][COLOR=dodgerblue]and[/COLOR][COLOR=orange]nerds[/COLOR]','Username:  '+username,'Email: '+email,'Unread Messages: '+unread+'/'+messages+'[CR]Posts: '+posts)
#-----------------------------------------------------------------------------------------------------------------
# menu to set the sort type when searching
def Sort_By(url,type):
    if type == 'communitybuilds':
        redirect = 'grab_builds'
        if url.endswith("visibility=public"):
             o0oO('folder','[COLOR=yellow]Manual Search[/COLOR]','&visibility=public','manual_search','','','','')
        if url.endswith("visibility=private"):
             o0oO('folder','[COLOR=yellow]Manual Search[/COLOR]','&visibility=private','manual_search','','','','')
    if type == 'tutorials':
        redirect = 'grab_tutorials'
    if type == 'hardware':
        redirect = 'grab_hardware'
    if type == 'addons':
        redirect = 'grab_addons'
        o0oO('folder','[COLOR=dodgerblue]Sort by Most Popular[/COLOR]',str(url)+'&sortx=downloads&orderx=DESC',redirect,'','','','')
    if type == 'hardware':
        o0oO('folder','[COLOR=lime]Filter Results[/COLOR]',url,'hardware_filter_menu','','','','')  
    if type != 'addons':
        o0oO('folder','[COLOR=dodgerblue]Sort by Most Popular[/COLOR]',str(url)+'&sortx=downloadcount&orderx=DESC',redirect,'','','','')
    if type == 'tutorials' or type == 'hardware':
        o0oO('folder','[COLOR=dodgerblue]Sort by Newest[/COLOR]',str(url)+'&sortx=Added&orderx=DESC',redirect,'','','','')
    else:
        o0oO('folder','[COLOR=dodgerblue]Sort by Newest[/COLOR]',str(url)+'&sortx=created&orderx=DESC',redirect,'','','','')
        o0oO('folder','[COLOR=dodgerblue]Sort by Recently Updated[/COLOR]',str(url)+'&sortx=updated&orderx=DESC',redirect,'','','','')
    o0oO('folder','[COLOR=dodgerblue]Sort by A-Z[/COLOR]',str(url)+'&sortx=name&orderx=ASC',redirect,'','','','')
    o0oO('folder','[COLOR=dodgerblue]Sort by Z-A[/COLOR]',str(url)+'&sortx=name&orderx=DESC',redirect,'','','','')
    if type == 'public_CB':
        o0oO('folder','[COLOR=dodgerblue]Sort by Genre[/COLOR]',url,'genres','','','','')
        o0oO('folder','[COLOR=dodgerblue]Sort by Country/Language[/COLOR]',url,'countries','','','','')
#---------------------------------------------------------------------------------------------------
# Create a standard text box
def Text_Boxes(heading,anounce):
  class TextBox():
    WINDOW=10142
    CONTROL_LABEL=1
    CONTROL_TEXTBOX=5
    def __init__(self,*args,**kwargs):
      xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, )) # activate the text viewer window
      self.win=xbmcgui.Window(self.WINDOW) # get window
      xbmc.sleep(500) # give window time to initialize
      self.setControls()
    def setControls(self):
      self.win.getControl(self.CONTROL_LABEL).setLabel(heading) # set heading
      try: f=open(anounce); text=f.read()
      except: text=anounce
      self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
      return
  TextBox()
  while xbmc.getCondVisibility('Window.IsVisible(textviewer)'):
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
#Maintenance section
def Tools():
    o0oO('folder','Backup/Restore A Build','','backup_restore', '','','','')
    o0oO('','Convert Physical Paths To Special',HOME,'fix_special','','','','')
    o0oO('','Upload Log','none','uploadlog', '','','','')
    o0oO('','View My Log','none','log', '','','','')
    o0oO('folder','View/Edit A File','none','notepad', '','','','')
#-----------------------------------------------------------------------------------------------------------------
#Tutorials Addon Menu
def Tutorials_Addon_Menu(url):
    o0oO('folder','[COLOR=yellow]1. Add-on Maintenance[/COLOR]', str(url)+'&type=Maintenance', 'grab_tutorials', '','','','')
    o0oO('folder','Audio Add-ons', str(url)+'&type=Audio', 'grab_tutorials', '','','','')
    o0oO('folder','Picture Add-ons', str(url)+'&type=Pictures', 'grab_tutorials', '','','','')
    o0oO('folder','Program Add-ons', str(url)+'&type=Programs', 'grab_tutorials', '','','','')
    o0oO('folder','Video Add-ons', str(url)+'&type=Video', 'grab_tutorials', '','','','')
#-----------------------------------------------------------------------------------------------------------------
# This creates the final menu showing build details, video and install link
def Tutorial_Menu(url):
    incremental = 'http://noobsandnerds.com/TI/TutorialPortal/downloadcount.php?id=%s' % (url)
    Open_URL(incremental)
    BaseURL           = 'http://noobsandnerds.com/TI/TutorialPortal/tutorialdetails.php?id=%s' % (url)
    link              = Open_URL(BaseURL).replace('\n','').replace('\r','')
    namematch         = re.compile('name="(.+?)"').findall(link)
    authormatch       = re.compile('author="(.+?)"').findall(link)
    videoguide1match  = re.compile('video_guide1="(.+?)"').findall(link)
    videoguide2match  = re.compile('video_guide2="(.+?)"').findall(link)
    videoguide3match  = re.compile('video_guide3="(.+?)"').findall(link)
    videoguide4match  = re.compile('video_guide4="(.+?)"').findall(link)
    videoguide5match  = re.compile('video_guide5="(.+?)"').findall(link)
    videolabel1match  = re.compile('video_label1="(.+?)"').findall(link)
    videolabel2match  = re.compile('video_label2="(.+?)"').findall(link)
    videolabel3match  = re.compile('video_label3="(.+?)"').findall(link)
    videolabel4match  = re.compile('video_label4="(.+?)"').findall(link)
    videolabel5match  = re.compile('video_label5="(.+?)"').findall(link)
    aboutmatch        = re.compile('about="(.+?)"').findall(link)
    step1match        = re.compile('step1="(.+?)"').findall(link)
    step2match        = re.compile('step2="(.+?)"').findall(link)
    step3match        = re.compile('step3="(.+?)"').findall(link)
    step4match        = re.compile('step4="(.+?)"').findall(link)
    step5match        = re.compile('step5="(.+?)"').findall(link)
    step6match        = re.compile('step6="(.+?)"').findall(link)
    step7match        = re.compile('step7="(.+?)"').findall(link)
    step8match        = re.compile('step8="(.+?)"').findall(link)
    step9match        = re.compile('step9="(.+?)"').findall(link)
    step10match       = re.compile('step10="(.+?)"').findall(link)
    step11match       = re.compile('step11="(.+?)"').findall(link)
    step12match       = re.compile('step12="(.+?)"').findall(link)
    step13match       = re.compile('step13="(.+?)"').findall(link)
    step14match       = re.compile('step14="(.+?)"').findall(link)
    step15match       = re.compile('step15="(.+?)"').findall(link)
    screenshot1match  = re.compile('screenshot1="(.+?)"').findall(link)
    screenshot2match  = re.compile('screenshot2="(.+?)"').findall(link)
    screenshot3match  = re.compile('screenshot3="(.+?)"').findall(link)
    screenshot4match  = re.compile('screenshot4="(.+?)"').findall(link)
    screenshot5match  = re.compile('screenshot5="(.+?)"').findall(link)
    screenshot6match  = re.compile('screenshot6="(.+?)"').findall(link)
    screenshot7match  = re.compile('screenshot7="(.+?)"').findall(link)
    screenshot8match  = re.compile('screenshot8="(.+?)"').findall(link)
    screenshot9match  = re.compile('screenshot9="(.+?)"').findall(link)
    screenshot10match = re.compile('screenshot10="(.+?)"').findall(link)
    screenshot11match = re.compile('screenshot11="(.+?)"').findall(link)
    screenshot12match = re.compile('screenshot12="(.+?)"').findall(link)
    screenshot13match = re.compile('screenshot13="(.+?)"').findall(link)
    screenshot14match = re.compile('screenshot14="(.+?)"').findall(link)
    screenshot15match = re.compile('screenshot15="(.+?)"').findall(link)
   
    name         = namematch[0] if (len(namematch) > 0) else ''
    author       = authormatch[0] if (len(authormatch) > 0) else ''
    videoguide1  = videoguide1match[0] if (len(videoguide1match) > 0) else 'None'
    videoguide2  = videoguide2match[0] if (len(videoguide2match) > 0) else 'None'
    videoguide3  = videoguide3match[0] if (len(videoguide3match) > 0) else 'None'
    videoguide4  = videoguide4match[0] if (len(videoguide4match) > 0) else 'None'
    videoguide5  = videoguide5match[0] if (len(videoguide5match) > 0) else 'None'
    videolabel1  = videolabel1match[0] if (len(videolabel1match) > 0) else 'None'
    videolabel2  = videolabel2match[0] if (len(videolabel2match) > 0) else 'None'
    videolabel3  = videolabel3match[0] if (len(videolabel3match) > 0) else 'None'
    videolabel4  = videolabel4match[0] if (len(videolabel4match) > 0) else 'None'
    videolabel5  = videolabel5match[0] if (len(videolabel5match) > 0) else 'None'
    about        = aboutmatch[0] if (len(aboutmatch) > 0) else ''
    step1        = '[CR][CR][COLOR=dodgerblue]Step 1:[/COLOR][CR]'+step1match[0] if (len(step1match) > 0) else ''
    step2        = '[CR][CR][COLOR=dodgerblue]Step 2:[/COLOR][CR]'+step2match[0] if (len(step2match) > 0) else ''
    step3        = '[CR][CR][COLOR=dodgerblue]Step 3:[/COLOR][CR]'+step3match[0] if (len(step3match) > 0) else ''
    step4        = '[CR][CR][COLOR=dodgerblue]Step 4:[/COLOR][CR]'+step4match[0] if (len(step4match) > 0) else ''
    step5        = '[CR][CR][COLOR=dodgerblue]Step 5:[/COLOR][CR]'+step5match[0] if (len(step5match) > 0) else ''
    step6        = '[CR][CR][COLOR=dodgerblue]Step 6:[/COLOR][CR]'+step6match[0] if (len(step6match) > 0) else ''
    step7        = '[CR][CR][COLOR=dodgerblue]Step 7:[/COLOR][CR]'+step7match[0] if (len(step7match) > 0) else ''
    step8        = '[CR][CR][COLOR=dodgerblue]Step 8:[/COLOR][CR]'+step8match[0] if (len(step8match) > 0) else ''
    step9        = '[CR][CR][COLOR=dodgerblue]Step 9:[/COLOR][CR]'+step9match[0] if (len(step9match) > 0) else ''
    step10       = '[CR][CR][COLOR=dodgerblue]Step 10:[/COLOR][CR]'+step10match[0] if (len(step10match) > 0) else ''
    step11       = '[CR][CR][COLOR=dodgerblue]Step 11:[/COLOR][CR]'+step11match[0] if (len(step11match) > 0) else ''
    step12       = '[CR][CR][COLOR=dodgerblue]Step 12:[/COLOR][CR]'+step12match[0] if (len(step12match) > 0) else ''
    step13       = '[CR][CR][COLOR=dodgerblue]Step 13:[/COLOR][CR]'+step13match[0] if (len(step13match) > 0) else ''
    step14       = '[CR][CR][COLOR=dodgerblue]Step 14:[/COLOR][CR]'+step14match[0] if (len(step14match) > 0) else ''
    step15       = '[CR][CR][COLOR=dodgerblue]Step 15:[/COLOR][CR]'+step15match[0] if (len(step15match) > 0) else ''
    screenshot1  = screenshot1match[0] if (len(screenshot1match) > 0) else ''
    screenshot2  = screenshot2match[0] if (len(screenshot2match) > 0) else ''
    screenshot3  = screenshot3match[0] if (len(screenshot3match) > 0) else ''
    screenshot4  = screenshot4match[0] if (len(screenshot4match) > 0) else ''
    screenshot5  = screenshot5match[0] if (len(screenshot5match) > 0) else ''
    screenshot6  = screenshot6match[0] if (len(screenshot6match) > 0) else ''
    screenshot7  = screenshot7match[0] if (len(screenshot7match) > 0) else ''
    screenshot8  = screenshot8match[0] if (len(screenshot8match) > 0) else ''
    screenshot9  = screenshot9match[0] if (len(screenshot9match) > 0) else ''
    screenshot10 = screenshot10match[0] if (len(screenshot10match) > 0) else ''
    screenshot11 = screenshot11match[0] if (len(screenshot11match) > 0) else ''
    screenshot12 = screenshot12match[0] if (len(screenshot12match) > 0) else ''
    screenshot13 = screenshot13match[0] if (len(screenshot13match) > 0) else ''
    screenshot14 = screenshot14match[0] if (len(screenshot14match) > 0) else ''
    screenshot15 = screenshot15match[0] if (len(screenshot15match) > 0) else ''
    description  = str('[COLOR=orange]Author: [/COLOR]'+author+'[CR][CR][COLOR=lime]About: [/COLOR]'+about+step1+step2+step3+step4+step5+step6+step7+step8+step9+step10+step11+step12+step13+step14+step15)

    if step1 != '':
        o0oO('','[COLOR=yellow][Text Guide][/COLOR]  '+name,description,'text_guide','',FANART,about,'')    
    if videoguide1 != 'None':
        o0oO('','[COLOR=lime][VIDEO][/COLOR]  '+videolabel1,videoguide1,'play_video','',FANART,'','')    
    if videoguide2 != 'None':
        o0oO('','[COLOR=lime][VIDEO][/COLOR]  '+videolabel2,videoguide2,'play_video','',FANART,'','')    
    if videoguide3 != 'None':
        o0oO('','[COLOR=lime][VIDEO][/COLOR]  '+videolabel3,videoguide3,'play_video','',FANART,'','')    
    if videoguide4 != 'None':
        o0oO('','[COLOR=lime][VIDEO][/COLOR]  '+videolabel4,videoguide4,'play_video','',FANART,'','')    
    if videoguide5 != 'None':
        o0oO('','[COLOR=lime][VIDEO][/COLOR]  '+videolabel5,videoguide5,'play_video','',FANART,'','')    
#-----------------------------------------------------------------------------------------------------------------
#Tutorials Root menu listings
def Tutorial_Root_Menu():
    if ADDON.getSetting('tutorial_manual_search')=='true':
        o0oO('folder','[COLOR=yellow]Manual Search[/COLOR]', 'tutorials', 'manual_search', '','','','')
    if ADDON.getSetting('tutorial_all')=='true':
        o0oO('folder','[COLOR=lime]All Guides[/COLOR] Everything in one place', '', 'grab_tutorials', '','','','')
    if ADDON.getSetting('tutorial_kodi')=='true':
        o0oO('folder','[COLOR=lime]XBMC / Kodi[/COLOR] Specific', '', 'xbmc_menu', '','','','')
    if ADDON.getSetting('tutorial_xbmc4xbox')=='true':
        o0oO('folder','[COLOR=lime]XBMC4Xbox[/COLOR] Specific', '&platform=XBMC4Xbox', 'xbmc_menu', '','','','')
    if ADDON.getSetting('tutorial_android')=='true':
        o0oO('folder','[COLOR=orange][Platform][/COLOR] Android', '&platform=Android', 'platform_menu', '','','','')
    if ADDON.getSetting('tutorial_atv')=='true':
        o0oO('folder','[COLOR=orange][Platform][/COLOR] Apple TV', '&platform=ATV', 'platform_menu', '','','','')
    if ADDON.getSetting('tutorial_ios')=='true':
        o0oO('folder','[COLOR=orange][Platform][/COLOR] ATV2 & iOS', '&platform=iOS', 'platform_menu', '','','','')
    if ADDON.getSetting('tutorial_linux')=='true':
        o0oO('folder','[COLOR=orange][Platform][/COLOR] Linux', '&platform=Linux', 'platform_menu', '','','','')
    if ADDON.getSetting('tutorial_pure_linux')=='true':
        o0oO('folder','[COLOR=orange][Platform][/COLOR] Pure Linux', '&platform=Custom_Linux', 'platform_menu', '','','','')
    if ADDON.getSetting('tutorial_openelec')=='true':
        o0oO('folder','[COLOR=orange][Platform][/COLOR] OpenELEC', '&platform=OpenELEC', 'platform_menu', '','','','')
    if ADDON.getSetting('tutorial_osmc')=='true':
        o0oO('folder','[COLOR=orange][Platform][/COLOR] OSMC', '&platform=OSMC', 'platform_menu', '','','','')
    if ADDON.getSetting('tutorial_osx')=='true':
        o0oO('folder','[COLOR=orange][Platform][/COLOR] OSX', '&platform=OSX', 'platform_menu', '','','','')
    if ADDON.getSetting('tutorial_raspbmc')=='true':
        o0oO('folder','[COLOR=orange][Platform][/COLOR] Raspbmc', '&platform=Raspbmc', 'platform_menu', '','','','')
    if ADDON.getSetting('tutorial_windows')=='true':
        o0oO('folder','[COLOR=orange][Platform][/COLOR] Windows', '&platform=Windows', 'platform_menu', '','','','')
    if ADDON.getSetting('tutorial_allwinner')=='true':
        o0oO('folder','[COLOR=dodgerblue][Hardware][/COLOR] Allwinner Devices', '&hardware=Allwinner', 'platform_menu', '','','','')
    if ADDON.getSetting('tutorial_aftv')=='true':
        o0oO('folder','[COLOR=dodgerblue][Hardware][/COLOR] Amazon Fire TV', '&hardware=AFTV', 'platform_menu', '','','','')
    if ADDON.getSetting('tutorial_amlogic')=='true':
        o0oO('folder','[COLOR=dodgerblue][Hardware][/COLOR] AMLogic Devices', '&hardware=AMLogic', 'platform_menu', '','','','')
    if ADDON.getSetting('tutorial_boxee')=='true':
        o0oO('folder','[COLOR=dodgerblue][Hardware][/COLOR] Boxee', '&hardware=Boxee', 'platform_menu', '','','','')
    if ADDON.getSetting('tutorial_intel')=='true':
        o0oO('folder','[COLOR=dodgerblue][Hardware][/COLOR] Intel Devices', '&hardware=Intel', 'platform_menu', '','','','')
    if ADDON.getSetting('tutorial_rpi')=='true':
        o0oO('folder','[COLOR=dodgerblue][Hardware][/COLOR] Raspberry Pi', '&hardware=RaspberryPi', 'platform_menu', '','','','')
    if ADDON.getSetting('tutorial_rockchip')=='true':
        o0oO('folder','[COLOR=dodgerblue][Hardware][/COLOR] Rockchip Devices', '&hardware=Rockchip', 'platform_menu', '','','','')
    if ADDON.getSetting('tutorial_xbox')=='true':
        o0oO('folder','[COLOR=dodgerblue][Hardware][/COLOR] Xbox', '&hardware=Xbox', 'platform_menu', '','','','')
#-----------------------------------------------------------------------------------------------------------------
#Option to upload a log
def Upload_Log(): 
    if ADDON.getSetting('email')=='':
        dialog = xbmcgui.Dialog()
        dialog.ok("No Email Address Set", "A new window will Now open for you to enter your Email address. The logfile will be sent here")
        ADDON.openSettings()
    xbmc.executebuiltin('XBMC.RunScript(special://home/plugins/programs/'+AddonName+'/uploadLog.py)')
#---------------------------------------------------------------------------------------------------
#Grab User Info
def User_Info(localbuildcheck,localversioncheck,localidcheck):
    if login == 'true':
        BaseURL   = 'http://noobsandnerds.com/TI/login/login_details.php?user=%s&pass=%s' % (username, password)
    else: BaseURL = 'http://noobsandnerds.com/TI/login/login_details.php?user=%s&pass=%s' % ('','')
    link          = Open_URL(BaseURL).replace('\n','').replace('\r','')
    welcomematch  = re.compile('login_msg="(.+?)"').findall(link)
    welcometext   = welcomematch[0] if (len(welcomematch) > 0) else ''

# Only create a cookie if successful login otherwise they won't ever be able to login    
    if not 'REGISTER FOR FREE' in welcometext:
        writefile = open(cookie, mode='w+')
        writefile.write('d="'+Timestamp()+'"\nlogin_msg="'+welcometext+'"')
        writefile.close()

    Categories(localbuildcheck,localversioncheck,localidcheck,welcometext)
#-----------------------------------------------------------------------------------------------------------------
# Check to see if we can ping google.com or google.cn
def Connectivity_Check():
    internetcheck = 1
    try:
        Open_URL('http://google.com')
    except:
        try:
            Open_URL('http://google.com')
        except:
            try:
                Open_URL('http://google.com')
            except:
                try:
                    Open_URL('http://google.cn')
                except:
                    try:
                        Open_URL('http://google.cn')
                    except:
                        dialog.ok("NO INTERNET CONNECTION",'It looks like this device isn\'t connected to the internet. Only some of the maintenance options will work until you fix the connectivity problem.')
                        Categories('','','','[COLOR=orange]NO INTERNET CONNECTION[/COLOR]')
                        internetcheck=0
    if internetcheck==1:
        Video_Check()
#-----------------------------------------------------------------------------------------------------------------
#Initial online check for new video
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

# Check for a new startup video
    if startupvideo=='true':
        try:
            link           = Open_URL(startupvideopath).replace('\n','').replace('\r','')
            datecheckmatch = re.compile('date="(.+?)"').findall(link)
            videomatch     = re.compile('video="https://www.youtube.com/watch\?v=(.+?)"').findall(link)
            datecheck      = datecheckmatch[0] if (len(datecheckmatch) > 0) else ''
            videocheck     = videomatch[0] if (len(videomatch) > 0) else ''

# If the date of online video is newer than the date in startup edit startup.xml
            if  int(localdatecheck) < int(datecheck):
                replacefile = content.replace(localdatecheck,datecheck)
                writefile = open(startuppath, mode='w')
                writefile.write(str(replacefile))
                writefile.close()
# Play new video
            yt.PlayVideo(videocheck, forcePlayer=True)
            xbmc.sleep(500)
            while xbmc.Player().isPlaying():
                xbmc.sleep(500)
        except: pass
    if not os.path.exists(cookie):
        print"### First login check ###"
        User_Info(localbuildcheck,localversioncheck,localidcheck)

# Check local cookie file, if 2 days old do online check for user info
    else:
        localfile3          = open(cookie, mode='r')
        content3            = localfile3.read()
        localfile3.close()
    
        userdatematch       = re.compile('d="(.+?)"').findall(content3)
        loginmatch          = re.compile('login_msg="(.+?)"').findall(content3)
        updatecheck         = userdatematch[0] if (len(userdatematch) > 0) else '0'
        welcometext         = loginmatch[0] if (len(loginmatch) > 0) else ''
        
        if int(updatecheck)+2000000 > int(Timestamp()):
            print"### Login successful ###"
            Categories(localbuildcheck,localversioncheck,localidcheck,welcometext)
        else:
            print"### Checking login ###"
            User_Info(localbuildcheck,localversioncheck,localidcheck)       
#-----------------------------------------------------------------------------------------------------------------    
#Function to clear the addon_data
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
        if skin!= "skin.confluence":
            dialog.ok('Default Confluence Skin Required','Please switch to the default Confluence skin before performing a wipe.')
            xbmc.executebuiltin("ActivateWindow(appearancesettings,return)")
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
                exclude_dirs_full =  ''
                exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf','.gitignore']
                message_header = "Creating full backup of existing build"
                message1 = "Archiving..."
                message2 = ""
                message3 = "Please Wait"
                Archive_Tree(HOME, backup_zip, message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)

#For loop to wipe files in special://home but leave ones in EXCLUDES untouched
            dp.create("Wiping Existing Content",'','Please wait...', '')
            for root, dirs, files in os.walk(HOME,topdown=True):
                dirs[:] = [d for d in dirs if d not in EXCLUDES]
                for name in files:
                    try:                            
                        dp.update(0,"Removing [COLOR=yellow]"+name+'[/COLOR]','','Please wait...')
                        os.unlink(os.path.join(root, name))
                        os.remove(os.path.join(root,name))
                        os.rmdir(os.path.join(root,name))
                    except: print"Failed to remove file: "+name
# Remove userdata folder
            userdatadirs=[name for name in os.listdir(USERDATA) if os.path.isdir(os.path.join(USERDATA, name))]
            try:
                for name in userdatadirs:
                    try:
                        if name not in EXCLUDES:
                            dp.update(0,"Cleaning Directory: [COLOR=yellow]"+name+' [/COLOR]','','Please wait...')
                            shutil.rmtree(os.path.join(USERDATA,name))
                    except: print "Failed to remove: "+name
            except: pass
# Clean up userdata and leave items untouched that were set in addon settings
            for root, dirs, files in os.walk(USERDATA,topdown=True):
                dirs[:] = [d for d in dirs if d not in EXCLUDES]
                for name in files:
                    try:                            
                        dp.update(0,"Removing [COLOR=yellow]"+name+'[/COLOR]','','Please wait...')
                        os.unlink(os.path.join(root, name))
                        os.remove(os.path.join(root,name))
                    except: print"Failed to remove file: "+name
# Remove addon directories
            addondirs=[name for name in os.listdir(ADDONS) if os.path.isdir(os.path.join(ADDONS, name))]
            try:
                for name in addondirs:
                    try:
                        if keeprepos=='true':
                            if name not in EXCLUDES and not 'repo' in name:
                                dp.update(0,"Removing Add-on: [COLOR=yellow]"+name+' [/COLOR]','','Please wait...')
                                shutil.rmtree(os.path.join(ADDONS,name))
                        else:   
                            if name not in EXCLUDES:
                                dp.update(0,"Removing Add-on: [COLOR=yellow]"+name+' [/COLOR]','','Please wait...')
                                shutil.rmtree(os.path.join(ADDONS,name))
                    except: print "Failed to remove: "+name
            except: pass
# Remove addon_data
            addondatadirs=[name for name in os.listdir(ADDON_DATA) if os.path.isdir(os.path.join(ADDON_DATA, name))]
            try:
                for name in addondatadirs:
                    try:
                        if name not in EXCLUDES:
                            dp.update(0,"Removing Add-on Data: [COLOR=yellow]"+name+' [/COLOR]','','Please wait...')
                            shutil.rmtree(os.path.join(ADDON_DATA,name))
                    except: print "Failed to remove: "+name
            except: pass
# Clean up everything in the home path
            homepath=[name for name in os.listdir(HOME) if os.path.isdir(os.path.join(HOME, name))]
            try:
                for name in homepath:
                    try:
                        if name not in EXCLUDES:
                            dp.update(0,"Cleaning Directory: [COLOR=yellow]"+name+' [/COLOR]','','Please wait...')
                            shutil.rmtree(os.path.join(HOME,name))
                    except: print "Failed to remove: "+name
            except: pass
        if mode != 'CB':
            dialog.ok('Wipe Complete','Kodi will now close.','When you next load up Kodi it should boot into the default Confluence skin and you should have a fresh install.')
            xbmc.executebuiltin('quit')
        try:
            os.remove(startuppath)
        except: print"### Failed to remove startup.xml"
        try:    
            os.remove(idfile)
        except: print"### Failed to remove id.xml"
    else: return
#---------------------------------------------------------------------------------------------------
#XBMC/Kodi/XBMC4Xbox tutorials menu2
def XBMC_Menu(url):
    o0oO('folder','[COLOR=yellow]1. Install[/COLOR]', str(url)+'&tags=Install&XBMC=1', 'grab_tutorials', '','','','')
    o0oO('folder','[COLOR=lime]2. Settings[/COLOR]', str(url)+'&tags=Settings', 'grab_tutorials', '','','','')
    o0oO('folder','[COLOR=orange]3. Add-ons[/COLOR]', str(url), 'tutorial_addon_menu', '','','','')
    o0oO('folder','[COLOR=dodgerblue][XBMC/Kodi][/COLOR]  Audio', str(url)+'&tags=Audio', 'grab_tutorials', '','','','')
    o0oO('folder','[COLOR=dodgerblue][XBMC/Kodi][/COLOR]  Errors', str(url)+'&tags=Errors', 'grab_tutorials', '','','','')
    o0oO('folder','[COLOR=dodgerblue][XBMC/Kodi][/COLOR]  Gaming', str(url)+'&tags=Gaming', 'grab_tutorials', '','','','')
    o0oO('folder','[COLOR=dodgerblue][XBMC/Kodi][/COLOR]  LiveTV', str(url)+'&tags=LiveTV', 'grab_tutorials', '','','','')
    o0oO('folder','[COLOR=dodgerblue][XBMC/Kodi][/COLOR]  Maintenance', str(url)+'&tags=Maintenance', 'grab_tutorials', '','','','')
    o0oO('folder','[COLOR=dodgerblue][XBMC/Kodi][/COLOR]  Pictures', str(url)+'&tags=Pictures', 'grab_tutorials', '','','','')
    o0oO('folder','[COLOR=dodgerblue][XBMC/Kodi][/COLOR]  Profiles', str(url)+'&tags=Profiles', 'grab_tutorials', '','','','')
    o0oO('folder','[COLOR=dodgerblue][XBMC/Kodi][/COLOR]  Skins', str(url)+'&tags=Skins', 'grab_tutorials', '','','','')
    o0oO('folder','[COLOR=dodgerblue][XBMC/Kodi][/COLOR]  Video', str(url)+'&tags=Video', 'grab_tutorials', '','','','')
    o0oO('folder','[COLOR=dodgerblue][XBMC/Kodi][/COLOR]  Weather', str(url)+'&tags=Weather', 'grab_tutorials', '','','','')
#-----------------------------------------------------------------------------------------------------------------
#Addon starts here
params=Get_Params()
addon_id=None
artpack=None
audioaddons=None
author=None
buildname=None
data_path=None
description=None
email=None
fanart=None
forum=None
iconimage=None
link=None
local=None
messages=None
mode=None
name=None
posts=None
programaddons=None
provider_name=None
repo_id=None
repo_link=None
skins=None
sources=None
title=None
updated=None
unread=None
url=None
version=None
video=None
videoaddons=None
welcometext=None
zip_link=None
direct='maintenance'

try:    addon_id=urllib.unquote_plus(params["addon_id"])
except: pass
try:    adult=urllib.unquote_plus(params["adult"])
except: pass
try:    artpack=urllib.unquote_plus(params["artpack"])
except: pass
try:    audioaddons=urllib.unquote_plus(params["audioaddons"])
except: pass
try:    author=urllib.unquote_plus(params["author"])
except: pass
try:    buildname=urllib.unquote_plus(params["buildname"])
except: pass
try:    data_path=urllib.unquote_plus(params["data_path"])
except: pass
try:    description=urllib.unquote_plus(params["description"])
except: pass
try:    email=urllib.unquote_plus(params["email"])
except: pass
try:    fanart=urllib.unquote_plus(params["fanart"])
except: pass
try:    forum=urllib.unquote_plus(params["forum"])
except: pass
try:    guisettingslink=urllib.unquote_plus(params["guisettingslink"])
except: pass
try:    iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try:    link=urllib.unquote_plus(params["link"])
except: pass
try:    local=urllib.unquote_plus(params["local"])
except: pass
try:    messages=urllib.unquote_plus(params["messages"])
except: pass
try:    mode=str(params["mode"])
except: pass
try:    name=urllib.unquote_plus(params["name"])
except: pass
try:    pictureaddons=urllib.unquote_plus(params["pictureaddons"])
except: pass
try:    posts=urllib.unquote_plus(params["posts"])
except: pass
try:    programaddons=urllib.unquote_plus(params["programaddons"])
except: pass
try:    provider_name=urllib.unquote_plus(params["provider_name"])
except: pass
try:    repo_link=urllib.unquote_plus(params["repo_link"])
except: pass
try:    repo_id=urllib.unquote_plus(params["repo_id"])
except: pass
try:    skins=urllib.unquote_plus(params["skins"])
except: pass
try:    sources=urllib.unquote_plus(params["sources"])
except: pass
try:    title=urllib.unquote_plus(params["title"])
except: pass
try:    updated=urllib.unquote_plus(params["updated"])
except: pass
try:    unread=urllib.unquote_plus(params["unread"])
except: pass
try:    url=urllib.unquote_plus(params["url"])
except: pass
try:    version=urllib.unquote_plus(params["version"])
except: pass
try:    video=urllib.unquote_plus(params["video"])
except: pass
try:    videoaddons=urllib.unquote_plus(params["videoaddons"])
except: pass
try:    welcometext=urllib.unquote_plus(params["welcometext"])
except: pass
try:    zip_link=urllib.unquote_plus(params["zip_link"])
except: pass

if not os.path.exists(userdatafolder):
    os.makedirs(userdatafolder)

if not os.path.exists(startuppath):
    localfile = open(startuppath, mode='w+')
    localfile.write('date="01011001"\nversion="0.0"')
    localfile.close()

if not os.path.exists(idfile):
    localfile = open(idfile, mode='w+')
    localfile.write('id="None"\nname="None"')
    localfile.close()

vfsfile = xbmc.translatePath(os.path.join('special://home','scripts','.modules','script.module.xbmcvfs','lib','xbmcvfs.py'))
readfile = open(vfsfile, mode='r')
content = file.read(readfile)
file.close(readfile)
print readfile
if not 'class File' in content:
    choice = dialog.yesno('Original XBMCVFS File Detected','The original xbmcvfs module pre-installed with XBMC4Xbox','has been detected, we find much greater success with Jans','modified version. Would you like to install?')
    if choice == 1:
        downloader.download('https://github.com/noobsandnerds/addons4xbox/blob/master/xbox_modules/script.module.xbmcvfs.zip?raw=true',os.path.join(packages,'xbmcvfs.zip'))
        extract.all(os.path.join(packages,'xbmcvfs.zip'),xbmc.translatePath(os.path.join('special://home','scripts','.modules')))
        
if mode == None : Connectivity_Check()
elif mode == 'addon_final_menu'   : Addon_Final_Menu(url)
elif mode == 'addon_categories'   : Addon_Categories(url)
elif mode == 'addon_countries'    : Addon_Countries(url)
elif mode == 'addon_genres'       : Addon_Genres(url)
elif mode == 'addon_install'      : Addon_Install(name,zip_link,repo_link,repo_id,addon_id,provider_name,forum,data_path)
elif mode == 'addon_install_badzip': Addon_Install_BadZip(name,zip_link,repo_link,repo_id,addon_id,provider_name,forum,data_path)
elif mode == 'addon_install_na'   : Addon_Install_NA(name,zip_link,repo_link,repo_id,addon_id,provider_name,forum,data_path)
elif mode == 'addon_install_zero' : Addon_Install_Zero(name,zip_link,repo_link,repo_id,addon_id,provider_name,forum,data_path)
elif mode == 'addon_loop'         : CB_Addon_Install_Loop()
elif mode == 'addon_removal_menu' : Addon_Removal_Menu()
elif mode == 'addonfixes'         : Addon_Fixes()
elif mode == 'addonmenu'          : Addon_Menu()
elif mode == 'addon_settings'     : Addon_Settings()
elif mode == 'backup'             : BACKUP()
elif mode == 'backup_option'      : Backup_Option()
elif mode == 'backup_restore'     : Backup_Restore()
elif mode == 'browse_repos'       : Browse_Repos()
elif mode == 'cb_test_loop'       : CB_Addon_Install_Loop()
elif mode == 'CB_Menu'            : CB_Menu(url)
elif mode == 'check_storage'      : checkPath.check(direct)
elif mode == 'check_updates'      : Addon_Check_Updates()
elif mode == 'clear_cache'        : Clear_Cache()
elif mode == 'create_keyword'     : Create_Addon_Pack()
elif mode == 'community'          : CB_Root_Menu(url)
elif mode == 'community_backup'   : Community_Backup()
elif mode == 'community_backup_2' : Community_Backup_OLD()
elif mode == 'community_menu'     : Community_Menu(url,video)        
elif mode == 'countries'          : Countries(url)
elif mode == 'description'        : Description(name,url,buildname,author,version,description,updated,skins,videoaddons,audioaddons,programaddons,pictureaddons,sources,adult)
elif mode == 'fix_special'        : Fix_Special(url)
elif mode == 'full_backup'        : Full_Backup()
elif mode == 'genres'             : Genres(url)
elif mode == 'gotham'             : Gotham_Confirm()
elif mode == 'grab_addons'        : Grab_Addons(url)
elif mode == 'grab_builds'        : Grab_Builds(url)
elif mode == 'grab_builds_premium': Grab_Builds_Premium(url)
elif mode == 'grab_hardware'      : Grab_Hardware(url)
elif mode == 'grab_news'          : Grab_News(url)
elif mode == 'grab_skins'         : Grab_Skins()
elif mode == 'grab_tutorials'     : Grab_Tutorials(url)
elif mode == 'guisettingsfix'     : GUI_Settings_Fix(url,local)
elif mode == 'hardware_filter_menu': Hardware_Filter_Menu(url)
elif mode == 'hardware_final_menu': Hardware_Menu(url)        
elif mode == 'hardware_root_menu' : Hardware_Root_Menu()       
elif mode == 'helix'              : Helix_Confirm()
elif mode == 'hide_passwords'     : Hide_Passwords()
elif mode == 'ipcheck'            : IP_Check()
elif mode == 'install_content'    : Install_Content(url)
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
elif mode == 'manual_search'      : Manual_Search(url)
elif mode == 'manual_search_builds': Manual_Search_Builds()
elif mode == 'nan_menu'           : NaN_Menu()
elif mode == 'news_root_menu'     : News_Root_Menu(url)
elif mode == 'news_menu'          : News_Menu(url)
elif mode == 'notify_msg'         : Notify_Check(url)
elif mode == 'notepad'            : Notepad()
elif mode == 'open_system_info'   : Open_System_Info()
elif mode == 'open_filemanager'   : Open_Filemanager()
elif mode == 'play_video'         : yt.PlayVideo(url)
elif mode == 'platform_menu'      : Platform_Menu(url)
elif mode == 'pop'                : pop(url)
elif mode == 'register'           : Register()
elif mode == 'remove_addon_data'  : Remove_Addon_Data()
elif mode == 'remove_addons'      : Remove_Addons(url)
elif mode == 'remove_build'       : Remove_Build()
elif mode == 'remove_crash_logs'  : Remove_Crash_Logs()
elif mode == 'remove_packages'    : Remove_Packages()
elif mode == 'remove_textures'    : Remove_Textures_Dialog()
elif mode == 'restore'            : RESTORE()
elif mode == 'restore_backup'     : Restore_Backup_XML(name,url,description)
elif mode == 'restore_community'  : Restore_Community(name,url,video,description,skins,guisettingslink,artpack)        
elif mode == 'restore_local_CB'   : Restore_Local_Community(url)
elif mode == 'restore_local_gui'  : Restore_Local_GUI()
elif mode == 'restore_option'     : Restore_Option()
elif mode == 'restore_zip'        : Restore_Zip_File(url)         
elif mode == 'run_addon'          : Run_Addon(url)
elif mode == 'runtest'            : speedtest.runtest(url)
elif mode == 'search_addons'      : Search_Addons(url)
elif mode == 'search_builds'      : Search_Builds(url)
elif mode == 'Search_Private'     : Private_Search(url)
elif mode == 'showinfo'           : Show_Info(url)
elif mode == 'showinfo2'          : Show_Info2(url)
elif mode == 'SortBy'             : Sort_By(BuildURL,type)
elif mode == 'speed_instructions' : Speed_Instructions()
elif mode == 'speedtest_menu'     : Speed_Test_Menu()
elif mode == 'text_guide'         : Text_Guide(url)
elif mode == 'tools'              : Tools()
elif mode == 'tutorial_final_menu': Tutorial_Menu(url)        
elif mode == 'tutorial_addon_menu': Tutorials_Addon_Menu(url)        
elif mode == 'tutorial_root_menu' : Tutorial_Root_Menu()        
elif mode == 'unhide_passwords'   : Unhide_Passwords()
elif mode == 'update'             : Update_Repo()
elif mode == 'uploadlog'          : Upload_Log()
elif mode == 'user_info'          : Show_User_Info()
elif mode == 'wipetools'          : Wipe_Tools()
elif mode == 'xbmc_menu'          : XBMC_Menu(url)
elif mode == 'xbmcversion'        : XBMC_Version(url)
elif mode == 'wipe_xbmc'          : Wipe_Kodi(mode)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
