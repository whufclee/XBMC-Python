import urllib, urllib2, re, xbmcplugin, xbmcgui, xbmc, xbmcaddon
import os, sys, time, xbmcvfs, glob, shutil, datetime, zipfile, ntpath
import subprocess, threading
import yt, downloader, checkPath
import binascii
import hashlib
import extract

######################################################
AddonID='plugin.program.communitybuilds'
AddonName='Community Builds'
######################################################
ADDON            =  xbmcaddon.Addon(id=AddonID)
zip              =  ADDON.getSetting('zip')
privatebuilds    =  ADDON.getSetting('private')
openelec         =  ADDON.getSetting('openelec')
keepfaves        =  ADDON.getSetting('favourites')
keepsources      =  ADDON.getSetting('sources')
username         =  ADDON.getSetting('username').replace(' ','%20')
password         =  ADDON.getSetting('password')
debug            =  ADDON.getSetting('debug')
login            =  ADDON.getSetting('login')
versionoverride  =  ADDON.getSetting('versionoverride')
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
dialog           =  xbmcgui.Dialog()
dp               =  xbmcgui.DialogProgress()
HOME             =  xbmc.translatePath('special://home/')
USERDATA         =  xbmc.translatePath(os.path.join('special://home/userdata',''))
ADDON_DATA       =  os.path.join(USERDATA,'addon_data')
CP_PROFILE       =  os.path.join(HOME,'CP_Profiles')
ADDONS_MASTER    =  os.path.join(CP_PROFILE,'Master')
DATABASE         =  os.path.join(USERDATA,'Database')
THUMBNAILS       =  os.path.join(USERDATA,'Thumbnails')
ADDONS           =  xbmc.translatePath(os.path.join('special://home','addons'))
KODI_ADDONS      =  xbmc.translatePath(os.path.join('special://xbmc','addons'))
CBADDONPATH      =  os.path.join(ADDONS,AddonID,'default.py')
FANART           =  os.path.join(ADDONS,AddonID,'fanart.jpg')
ADDONXMLTEMP     =  os.path.join(ADDONS,AddonID,'resources','addonxml')
bakdefault       =  os.path.join(ADDONS,AddonID,'resources','backup')
GUI              =  os.path.join(USERDATA,'guisettings.xml')
GUIFIX           =  os.path.join(USERDATA,'guifix.xml')
ARTPATH          =  'http://www.noobsandnerds.com/TI/artwork/'
defaulticon      =  os.path.join(ADDONS,AddonID,'icon_menu.png')
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
scriptfolder     =  os.path.join(ADDON_DATA,AddonID,'scripts')
tempdbpath       =  os.path.join(USB,'Database')
packages         =  os.path.join(ADDONS,'packages')
addonstemp       =  os.path.join(USERDATA,'addontemp')
backupaddonspath =  os.path.join(USERDATA,'.cbcfg')
EXCLUDES         =  ['firstrun','plugin.program.tbs','plugin.program.totalinstaller','plugin.program.communitybuilds','script.module.addon.common','addons','addon_data','userdata','sources.xml','favourites.xml']
EXCLUDES2        =  ['firstrun','plugin.program.tbs','plugin.program.totalinstaller','plugin.program.communitybuilds','script.module.addon.common','addons','addon_data','userdata','sources.xml','favourites.xml','guisettings.xml','CP_Profiles','temp']

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
                        if debug == 'true':
                            print 'Script Requires --- ' + requires
            except:
                pass
                
    return depfiles
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
def o0oO(type,name,url,mode,iconimage = '',fanart = '',video = '',description = ''):
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
def Addon_Check_Updates():
    Update_Repo()
    xbmc.executebuiltin('ActivateWindow(10040,"addons://outdated/",return)')
#-----------------------------------------------------------------------------------------------------------------
#Function to open addon settings
def Addon_Settings():
    ADDON.openSettings(sys.argv[0])
    xbmc.executebuiltin('Container.Refresh')
#-----------------------------------------------------------------------------------------------------------------
def Android_Path_Check():
    xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
    version=float(xbmc_version[:4])
    if version < 14:
        log_path_new = os.path.join(log_path,'xbmc.log')
    else:
        log_path_new = os.path.join(log_path,'kodi.log')
        
    try:
        localfile = open(log_path_new, mode='r')
        content   = localfile.read()
        localfile.close()
    except:
        try:
            localfile = open(os.path.join(HOME,'temp','kodi.log'), mode='r')
            content   = localfile.read()
            localfile.close()
        except:
            try:
                localfile = open(os.path.join(HOME,'temp','xbmc.log'), mode='r')
                content   = localfile.read()
                localfile.close()
            except:
                pass                

    localstoragematch  = re.compile('External storage path = (.+?);').findall(content)
    localstorage       = localstoragematch[0] if (len(localstoragematch) > 0) else ''
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
#Main category list
def Categories(localbuildcheck,localversioncheck,id,welcometext,livemsg):
    Cleanup_Partial_Install()
    if livemsg != 'none':
        try:
            exec menuitem
            o0oO('','[COLOR=orange]---------------------------------------[/COLOR]','None','','','','','')
        except:
            pass
    if (username.replace('%20',' ') in welcometext) and ('elc' in welcometext):
        o0oO('',welcometext,'show','user_info','','','','')
        
        if id != 'None':
            
            if id != 'Local':
                updatecheck = Check_For_Update(localbuildcheck,localversioncheck,id)
                
                if updatecheck == True:
                    
                    if not 'Partially installed' in localbuildcheck:
                        o0oO('folder','[COLOR=dodgerblue]'+localbuildcheck+':[/COLOR] [COLOR=lime]NEW VERSION AVAILABLE[/COLOR]',id,'showinfo','','','','')
                    
                    if '(Partially installed)' in localbuildcheck:
                        o0oO('folder','[COLOR=darkcyan]Current Build Installed: [/COLOR][COLOR=dodgerblue]'+localbuildcheck+'[/COLOR]',id,'showinfo2','','','','')
                else:
                    o0oO('folder','[COLOR=darkcyan]Current Build Installed: [/COLOR][COLOR=dodgerblue]'+localbuildcheck+'[/COLOR]',id,'showinfo','','','','')
            
            else:
                
                if localbuildcheck == 'Incomplete':
                    o0oO('','[COLOR=darkcyan]Your last restore is not yet completed[/COLOR]','url',Check_Local_Install(),'','','','')
                
                else:
                    o0oO('','[COLOR=darkcyan]Current Build Installed: [/COLOR][COLOR=dodgerblue]Local Build ('+localbuildcheck+')[/COLOR]','','','','','','')
        folders = 0
        
        if os.path.exists(CP_PROFILE):
            for name in os.listdir(CP_PROFILE):
                if name != 'Master':
                    folders += 1

            if folders>1:
                o0oO('folder','[COLOR=darkcyan]Switch Build Profile[/COLOR]',localbuildcheck,'switch_profile_menu','','','','')

        o0oO('','[COLOR=orange]---------------------------------------[/COLOR]','None','','','','','')

    if login =='true' and not 'elc' in welcometext:
        o0oO('',welcometext,'None','addon_settings','','','','')   
    
    if not 'elc' in welcometext and not "UNABLE" in welcometext:
        o0oO('',welcometext,'None','register','','','','')
    o0oO('','[COLOR=yellow]Settings[/COLOR]','settings','addon_settings','','','','')
    
    o0oO('folder','Install A Community Build',welcometext,'community', '','','','')
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
        if not 'totalinstaller' in name and not 'plugin.program.communitybuilds' in name and not 'plugin.program.tbs' in name and not 'packages' in name and os.path.isdir(os.path.join(ADDONS, name)):

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
        
        if not 'totalinstaller' in name and not 'plugin.program.tbs' in name and not 'plugin.program.communitybuilds' in name:
            if not os.path.exists(os.path.join(ADDONS,name)):
                os.rename(os.path.join(addonstemp,name),os.path.join(ADDONS,name))
                dp.update(0,"Installing: [COLOR=yellow]"+name+'[/COLOR]','','Please wait...')
                print"### Successfully installed: "+name
                   
            else:
                print"### "+name+" Already exists on system"
#---------------------------------------------------------------------------------------------------
# Disclaimer popup prior to opening the main CB menu. Means user has to click to proceed and also fixes issue with popup keep opening during backup
def CB_Root_Menu(welcometext):
    pop('disclaimer.xml')
    o0oO('folder','I have read and understand the disclaimer.',welcometext,'CB_Menu','','','','')        
#-----------------------------------------------------------------------------------------------------------------
#Build the root search menu for installing community builds    
def CB_Menu(welcometext):
    if xbmc.getCondVisibility('system.platform.android'):
        localstorage   = Android_Path_Check()
        downloadfolder = os.path.join(localstorage,'Download')
        try:
            if not os.path.exists(downloadfolder):
                os.makedirs(downloadfolder)
        except:
            print"### Failed to make download folder"
    
        if not os.path.exists('/data/data/com.rechild.advancedtaskkiller'):
            choice = dialog.yesno('Advanced Task Killer Required','To be able to us features such as the backup/restore and community builds you need the Advanced Task Killer app installed. Would you like to download it now?')
            if choice == 1:
                dp.create('Downloading APK file','','','')
                try:
                    downloader.download('https://archive.org/download/com.rechild.advancedtaskkiller/com.rechild.advancedtaskkiller.apk',os.path.join(downloadfolder,'AdvancedTaskKiller.apk'))
                    dialog.ok('Download Complete',"The apk file has now been downloaded, you'll find this in your downloads folder. Just install this exactly the same as you would any other apk file - click on it and then click through the setup screen. The file is called AdvancedTaskKiller.apk")
                except:
                    try:
                        downloader.download('https://archive.org/download/com.rechild.advancedtaskkiller/com.rechild.advancedtaskkiller.apk',os.path.join('storage','emulated','legacy','Download','AdvancedTaskKiller.apk'))
                        dialog.ok('Download Complete',"The AdvancedTaskKiller.apk file has now been downloaded, you'll find this in your downloads folder. You'll need a File Manager app to install this file, we recommend installing ES File Explorer - just do a search for this on your box/stick.")
                    except:
                        dialog.ok('Download Failed','It wasn\'t possible to download the Advanced Task Killer, without it you will almost certainly run into problems so make sure you get it installed otherwise you\'ll need to manually force close and switching profiles may fail.')
                        
 
    xbmc_version = xbmc.getInfoLabel("System.BuildVersion")
    versionfloat = float(xbmc_version[:2])
    version      = int(versionfloat)
    print"#### Welcome: "+welcometext
    
    if ((username.replace('%20',' ') in welcometext) and ('elc' in welcometext)):
        if privatebuilds=='true':
            o0oO('folder','[COLOR=dodgerblue]Show My Private List[/COLOR]','&visibility=private','grab_builds','','','','')        
     
        if (version < 14) and (versionoverride=='false'):
            o0oO('folder','[COLOR=dodgerblue]Show All Gotham Compatible Builds[/COLOR]','&xbmc=gotham&visibility=public','grab_builds','','','','')
        
        if (version == 14) and (versionoverride=='false'):
            o0oO('folder','[COLOR=dodgerblue]Show All Helix Compatible Builds[/COLOR]','&xbmc=helix&visibility=public','grab_builds','','','','')
        
        if (version == 15) and (versionoverride=='false'):
            o0oO('folder','[COLOR=dodgerblue]Show All Isengard Compatible Builds[/COLOR]','&xbmc=isengard&visibility=public','grab_builds','','','','')
        if (version == 16) and (versionoverride=='false'):
            o0oO('folder','[COLOR=dodgerblue]Show All Jarvis Compatible Builds[/COLOR]','&xbmc=jarvis&visibility=public','grab_builds','','','','')
        if versionoverride=='true':
            o0oO('folder','[COLOR=dodgerblue]Show All Builds[/COLOR]','&xbmc=all&visibility=public','grab_builds','','','','')
        if wizard == 'false':
            o0oO('','[COLOR=gold]How to fix builds broken on other wizards![/COLOR]','','instructions_5','','','','')
        if wizardurl1 != '' and wizard == 'true':
            o0oO('folder','[COLOR=darkcyan]Show '+wizardname1+' Builds[/COLOR]','&id=1','grab_builds','','','','')
        if wizardurl2 != '' and wizard == 'true':
            o0oO('folder','[COLOR=darkcyan]Show '+wizardname2+' Builds[/COLOR]','&id=2','grab_builds','','','','')
        if wizardurl3 != '' and wizard == 'true':
            o0oO('folder','[COLOR=darkcyan]Show '+wizardname3+' Builds[/COLOR]','&id=3','grab_builds','','','','')
        if wizardurl4 != '' and wizard == 'true':
            o0oO('folder','[COLOR=darkcyan]Show '+wizardname4+' Builds[/COLOR]','&id=4','grab_builds','','','','')
        if wizardurl5 != '' and wizard == 'true':
            o0oO('folder','[COLOR=darkcyan]Show '+wizardname5+' Builds[/COLOR]','&id=5','grab_builds','','','','')

    else:
        o0oO('folder','[COLOR=dodgerblue]Show All Builds[/COLOR]','&j=1&xbmc=all&visibility=public','grab_builds','','','','')
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
            print"### Created: "+os.path.join(CP_PROFILE, description)
    if not os.path.exists(ADDONS_MASTER):
        os.makedirs(ADDONS_MASTER)
        if debug == 'true':
            print"### Created: "+ADDONS_MASTER
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)
        if debug == 'true':
            print"### Removed: "+temp_path
# Create a temp directory for addons in zip
    if os.path.exists(profile_addon_path):
        if not os.path.exists(temp_path):
            os.makedirs(temp_path)
            if debug == 'true':
                print"### Created: "+temp_path
        extract.all(profile_addon_path, temp_path, dp)
        print"### NEW STYLE BUILD"
        if debug == 'true':
            print"### Extracted "+profile_addon_path+" to: "+temp_path
    elif os.path.exists(os.path.join(profile_path,'addons')):
        os.rename(os.path.join(profile_path,'addons'), temp_path)
        print"### OLD BUILD - RENAMED ADDONS FOLDER"
        if debug == 'true':
            print"### renamed "+os.path.join(profile_path,'addons')+" to "+temp_path
    
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
            print"### Created: "+os.path.join(ADDONS_MASTER, 'backups')
    for name in os.listdir(temp_path):
        try:
#            shutil.copytree(os.path.join(temp_path, name), os.path.join(ADDONS_MASTER, 'backups', name))
#            dp.update(0,"Backing Up...",'[COLOR yellow]%s[/COLOR]'%name, 'Please Wait...')
            profile_addons.write(name+'|')
            if debug == 'true':
                print"### Added: "+os.path.join(ADDONS_MASTER, 'backups', name)
                print"### Added "+name+" to "+profile_addons
        except:
            pass

        if not name in mainaddons:
            try:
                os.rename(os.path.join(temp_path, name), os.path.join(ADDONS_MASTER, name))
                dp.update(0,"Configuring",'[COLOR yellow]%s[/COLOR]'%name, 'Please Wait...')
                if debug == 'true':
                    print"### Renamed from "+os.path.join(temp_path, name)+" to "+os.path.join(ADDONS_MASTER, name)
            except:
                pass

    profile_addons.close()
    shutil.rmtree(temp_path)
    shutil.rmtree(profile_path)
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
    link    = Open_URL(BaseURL, 10).replace('\n','').replace('\r','')
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
    link    = Open_URL(BaseURL, 10).replace('\n','').replace('\r','')
    
    if id != 'None':
        versioncheckmatch = re.compile('version="(.+?)"').findall(link)
        versioncheck  = versioncheckmatch[0] if (len(versioncheckmatch) > 0) else ''
    
        if  localversioncheck < versioncheck:
            return True
    
    else:
        return False
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
# Split string into arrays
def chunks(s, n):
    for start in range(0, len(s), n):
        yield s[start:start+n]
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
def Cleanup_Old_Textures():
# Thanks to xunity maintenance tool for this code, this will remove old stale textures not used in past 14 days
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
#Function to clear all known cache files
def Clear_Cache():
    choice = xbmcgui.Dialog().yesno('Clear All Known Cache?', 'This will clear all known cache files and can help if you\'re encountering kick-outs during playback as well as other random issues. There is no harm in using this.', nolabel='Cancel',yeslabel='Delete')
    
    if choice == 1:
        Wipe_Cache()
        Remove_Textures_Dialog()
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
# This creates the final menu showing build details, video and install link
def Community_Menu(url,video):
    Cleanup_Partial_Install()
    BaseURL            = 'http://noobsandnerds.com/TI/Community_Builds/community_builds_premium.php?id=%s' % (url)
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
    o0oO('','[COLOR=yellow]IMPORTANT:[/COLOR] Install Instructions','','instructions_2','','','','')
    Add_Desc_Dir('[COLOR=yellow]Description:[/COLOR] This contains important info from the build author','None','description','',fanart,name,author,version,description,updated,skins,videoaddons,audioaddons,programaddons,pictureaddons,sources,adult)
    
    if localidcheck == head and localversioncheck != version:
        o0oO('','[COLOR=orange]----------------- UPDATE AVAILABLE ------------------[/COLOR]','None','','','','','')
        Add_Build_Dir('[COLOR=dodgerblue]1. Update:[/COLOR] Overwrite My Library & Profiles',downloadURL,'update_community',iconimage,'','update',name,defaultskin,guisettingslink,artpack)
        Add_Build_Dir('[COLOR=dodgerblue]2. Update:[/COLOR] Keep My Library & Profiles',downloadURL,'update_community',iconimage,'','updatelibprofile',name,defaultskin,guisettingslink,artpack)
        Add_Build_Dir('[COLOR=dodgerblue]3. Update:[/COLOR] Keep My Library Only',downloadURL,'update_community',iconimage,'','updatelibrary',name,defaultskin,guisettingslink,artpack)
        Add_Build_Dir('[COLOR=dodgerblue]4. Update:[/COLOR] Keep My Profiles Only',downloadURL,'update_community',iconimage,'','updateprofiles',name,defaultskin,guisettingslink,artpack)
    
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
        if OpenELEC_Check() and oedownload != 'None':
            Add_Build_Dir('[COLOR=darkcyan]OpenELEC FRESH INSTALL[/COLOR]',oedownload,'restore_openelec',iconimage,fanart,guisettingslink,name,'','','')
        Add_Build_Dir('[COLOR=dodgerblue]Standard Install[/COLOR]',downloadURL,'restore_community',iconimage,fanart,'merge',name,defaultskin,guisettingslink,artpack)
         
    if guisettingslink!='None':
        o0oO('','[COLOR=dodgerblue](Optional) Apply guisettings.xml fix[/COLOR]',guisettingslink,'guisettingsfix','',fanart,'','')
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
    if localbuildcheck == 'None' or 'unknown':
        dialog.ok('No Profile Set',"There's no profile name set to the build you're currently running. Please enter a name for this build so we can save it and make sure no data is lost.")
        vq = Get_Keyboard( heading="Enter a name for this backup" )
        if ( not vq ):
            return False, 0
        vq          = vq.replace(' ','_')
        title       = urllib.quote_plus(vq)
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
            if not item in mainaddons and item != 'plugin.program.totalinstaller' and item != 'plugin.program.communitybuilds' and item != 'script.module.addon.common' and item != 'packages':
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
            if not item in mainaddons and item != 'plugin.program.totalinstaller' and item != 'plugin.program.communitybuilds' and item != 'script.module.addon.common' and item != 'packages':
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
#---------------------------------------------------------------------------------------------------
#Function to delete the userdata/addon_data folder
def DeleteAddonData():
    print '############################################################       DELETING USERDATA             ###############################################################'
    addon_data_path = xbmc.translatePath(os.path.join('special://home/userdata/addon_data', ''))
    
    for root, dirs, files in os.walk(addon_data_path):
        file_count = 0
        file_count += len(files)
        
        if file_count >= 0:
            
            for f in files:
                os.unlink(os.path.join(root, f))
            
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))        
#---------------------------------------------------------------------------------------------------
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
    print '############################################################       DELETING PACKAGES             ###############################################################'
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
        dp.create("[COLOR=orange]noobs[/COLOR][COLOR=dodgerblue]and[/COLOR][COLOR=orange]nerds[/COLOR]","Wiping...",'', 'Please Wait')
        shutil.rmtree(path, ignore_errors=True)
        dp.close()
        xbmc.executebuiltin('container.Refresh')
#-----------------------------------------------------------------------------------------------------------------  
# Function to delete the userdata/addon_data folder
def Delete_Userdata():
    print '############################################################       DELETING USERDATA             ###############################################################'
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
                            dialog.ok("Error downloading dependency", 'There was an error downloading [COLOR=dodgerblue]'+depname+'[/COLOR]. Please consider updating the add-on portal with details or report the error on the forum at [COLOR=orange]noobs[/COLOR][COLOR=dodgerblue]and[/COLOR][COLOR=orange]nerds[/COLOR]')
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
#Convert physical paths to special paths
def Fix_Special(url):
    dp.create("Changing Physical Paths To Special","Renaming paths...",'', 'Please Wait')
    
    for root, dirs, files in os.walk(url):  #Search all xml files and replace physical with special
        
        for file in files:
            
            if file.endswith(".xml") or file.endswith(".hash") or file.endswith("properies"):
                 dp.update(0,"Fixing",file, 'Please Wait')
                 a = open((os.path.join(root, file))).read()
                 encodedpath  = HOME.replace(':','%3a').replace('\\','%5c')
                 extraslashes = HOME.replace('\\','\\\\')
                 b = a.replace(HOME, 'special://home/').replace(encodedpath, 'special://home/').replace(extraslashes, 'special://home/')
                 f = open((os.path.join(root, file)), mode='w')
                 f.write(str(b))
                 f.close()
#---------------------------------------------------------------------------------------------------
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
        link       = Open_URL(buildsURL, 10).replace('\n','').replace('\r','')
# match without cloudflare disabled
        match      = re.compile('name="(.+?)"  <br> id="(.+?)"  <br> Thumbnail="(.+?)"  <br> Fanart="(.+?)"  <br> downloads="(.+?)"  <br> <br>', re.DOTALL).findall(link)
        if match == []:
# match with cloudflare disabled
            match  = re.compile('name="(.+?)" <br> id="(.+?)" <br> Thumbnail="(.+?)" <br> Fanart="(.+?)" <br> downloads="(.+?)" <br> <br>', re.DOTALL).findall(link)
        if not 'j=1' in url:
            Sort_By(url,'communitybuilds')
    
        for name,id,Thumbnail,Fanart,downloads in match:
            Add_Build_Dir(name+'[COLOR=lime] ('+downloads+' downloads)[/COLOR]',id+url,'community_menu',Thumbnail,Fanart,id,'','','','')
    
    if not 'j=1' in url:
        if 'id=1' in url: buildsURL = wizardurl1
        if 'id=2' in url: buildsURL = wizardurl2
        if 'id=3' in url: buildsURL = wizardurl3
        if 'id=4' in url: buildsURL = wizardurl4
        if 'id=5' in url: buildsURL = wizardurl5

    link       = Open_URL(buildsURL, 10).replace('\n','').replace('\r','')
    match      = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)

    for name,url,iconimage,fanart,description in match:
        if not 'viewport' in name:
            o0oO('addon',name,url,'restore_local_CB',iconimage,fanart,description,'')
#---------------------------------------------------------------------------------------------------
#Option to download guisettings fix that merges with existing settings.
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
       shutil.move(os.path.join(guitemp,'addon_data'), USERDATA)

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
#---------------------------------------------------------------------------------------------------
#Function to download guisettings.xml and merge with existing.
def INSTALL_PART2(url):
    BaseURL          = 'http://noobsandnerds.com/TI/Community_Builds/guisettings.php?id=%s' % (url)
    link             = Open_URL(BaseURL, 10).replace('\n','').replace('\r','')
    guisettingsmatch = re.compile('guisettings="(.+?)"').findall(link)
    guisettingslink  = guisettingsmatch[0] if (len(guisettingsmatch) > 0) else 'None'
    
    GUI_Merge(guisettingslink,local)
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
#(Instructions) Adding other wizards
def Instructions_5():
    Text_Boxes('Adding Third Party Wizards', '[COLOR=gold]ONE WIZARD TO RULE THEM ALL![/COLOR][CR]Did you know the vast majority of wizards out there (every single one we\'ve tested) has just been a copy/paste of very old code created by the team here? We\'ve noticed a lot of the users installing builds via these third party wizards have run into many different problems so we thought we\'d take it upon ourselves to help out...'
    '[CR][CR][CR][COLOR=gold]WHAT BENEFITS DOES THIS HAVE?[/COLOR][CR]We\'ve added extra code that checks for common errors, unfortunately there are some people out there using inferior programs to create their backups and that is causing problems in their wizards. If such a problem exists when trying to use another wizard you can try adding the details to this addon and it automatically fixes any corrupt files it finds. Of course there are other benefits... installing code from an unknown source can give the author access to your system so make sure you always trust the author(s). Why take the risk of installing wizards created by anonymous usernames on social media sites when you can install from a trusted source like noobsandnerds and you\'ll also be safe in the knowledge that any new updates and improvements will be made here first - we do not copy/paste code, we are actively creating new exciting solutions!'
    '[CR][CR][CR][COLOR=gold]ADDING 3RD PARTY WIZARDS TO THIS ADDON[/COLOR][CR][CR][COLOR=dodgerblue][B]Step 1:[/COLOR] Enabling 3rd Party Wizards[/B][CR]In the addon settings under the Community Builds section you have the option to enable third party community builds, if you click on this you will be able to enter details of up to 5 different wizards.'
    '[CR][CR][COLOR=dodgerblue][B]Step 2:[/COLOR] Enter the URL[/B][CR]As virtually all wizards use exactly the same structure all you need to do is find out what URL they are looking up in the code, you can open the default.py file of the wizard in a text editor and search for "http" and you will more than likely find the URL straight away. Try entering it in a web address, it should show the details for all the builds in that wizard in a text based page. If the page is blank don\'t worry it may just be locked from web browsers and can only be opened in Kodi, try it out and see if it works.'
    '[CR][CR][COLOR=dodgerblue][B]Step 3:[/COLOR] Enter the name[/B][CR]Give the wizard a name, now when you go into the Community Builds section you\'ll have the official noobsandnerds builds as an option and also any new ones you\'ve added.')
#-----------------------------------------------------------------------------------------------------------------
#ANDROID ONLY WORKS WITH ROOT
def Kill_XBMC():
#    dialog.ok('Kodi will now close','The system will now attempt to force close Kodi.','You may encounter a freeze, if that happens give it a minute','and if it doesn\'t close please restart your system.')
    if not os.path.exists(scriptfolder):
        os.makedirs(scriptfolder)
    xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
    version=float(xbmc_version[:4])
    if xbmc.getCondVisibility('system.platform.windows'):
        if version < 14:
            try:
                writefile = open(os.path.join(scriptfolder,'win_xbmc.bat'), 'w+')
                writefile.write('@ECHO off\nTASKKILL /im XBMC.exe /f\ntskill XBMC.exe\nXBMC.exe')
                writefile.close()
                os.system(os.path.join(scriptfolder,'win_xbmc.bat'))
            except:
                print"### Failed to run win_xbmc.bat"
        else:
            try:
                writefile = open(os.path.join(scriptfolder,'win_kodi.bat'), 'w+')
                writefile.write('@ECHO off\nTASKKILL /im Kodi.exe /f\ntskill Kodi.exe\nKodi.exe')
                writefile.close()
                os.system(os.path.join(scriptfolder,'win_kodi.bat'))
            except:
                print"### Failed to run win_kodi.bat"
    elif xbmc.getCondVisibility('system.platform.osx'):
        if version < 14:
            try:
                writefile = open(os.path.join(scriptfolder,'osx_xbmc.sh'), 'w+')
                writefile.write('killall -9 XBMC\nXBMC')
                writefile.close()
            except:
                pass
            try:
                os.system('chmod 755 '+os.path.join(scriptfolder,'osx_xbmc.sh'))
            except:
                pass
            try:
                os.system(os.path.join(scriptfolder,'osx_xbmc.sh'))
            except:
                print"### Failed to run osx_xbmc.sh"
        else:
            try:
                writefile = open(os.path.join(scriptfolder,'osx_kodi.sh'), 'w+')
                writefile.write('killall -9 Kodi\nKodi')
                writefile.close()
            except:
                pass
            try:
                os.system('chmod 755 '+os.path.join(scriptfolder,'osx_kodi.sh'))
            except:
                pass
            try:
                os.system(os.path.join(scriptfolder,'osx_kodi.sh'))
            except:
                print"### Failed to run osx_kodi.sh"
#    else:
    elif xbmc.getCondVisibility('system.platform.android'):
        if os.path.exists('/data/data/com.rechild.advancedtaskkiller'):
            dialog.ok('Attempting to force close','On the following screen please press the big button at the top which says "KILL selected apps". Kodi will restart, please be patient while your system updates the necessary files and your skin will automatically switch once fully updated.')
            try:
                xbmc.executebuiltin('StartAndroidActivity(com.rechild.advancedtaskkiller)')
            except:
                print"### Failed to run Advanced Task Killer. Make sure you have it installed, you can download from https://archive.org/download/com.rechild.advancedtaskkiller/com.rechild.advancedtaskkiller.apk"
        else:
            dialog.ok('Advanced Task Killer Not Found',"The Advanced Task Killer app cannot be found on this system. Please make sure you actually installed it after downloading. We can't do everything for you - on Android you do have to physically click on the download to install an app.")
        try:
            os.system('adb shell am force-stop org.xbmc.kodi')
        except:
            pass
        try:
            os.system('adb shell am force-stop org.kodi')
        except:
            pass
        try:
            os.system('adb shell am force-stop org.xbmc.xbmc')
        except:
            pass
        try:
            os.system('adb shell am force-stop org.xbmc')
        except:
            pass
        try:
            os.system('adb shell kill org.xbmc.kodi')
        except:
            pass
        try:
            os.system('adb shell kill org.kodi')
        except:
            pass
        try:
            os.system('adb shell kill org.xbmc.xbmc')
        except:
            pass
        try:
            os.system('adb shell kill org.xbmc')
        except:
            pass
        try:
            os.system('Process.killProcess(android.os.Process.org.xbmc,kodi());')
        except:
            pass
        try:
            os.system('Process.killProcess(android.os.Process.org.kodi());')
        except:
            pass
        try:
            os.system('Process.killProcess(android.os.Process.org.xbmc.xbmc());')
        except:
            pass
        try:
            os.system('Process.killProcess(android.os.Process.org.xbmc());')
        except:
            pass
    elif xbmc.getCondVisibility('system.platform.linux'):
        if version < 14:
            try:
                writefile = open(os.path.join(scriptfolder,'linux_xbmc'), 'w+')
                writefile.write('killall XBMC\nkillall -9 xbmc.bin\nXBMC')
                writefile.close()
            except:
                pass
            try:
                os.system('chmod a+x '+os.path.join(scriptfolder,'linux_xbmc'))
            except:
                pass
            try:
                os.system(os.path.join(scriptfolder,'linux_xbmc'))
            except:
                print "### Failed to run: linux_xbmc"
        else:
            try:
                writefile = open(os.path.join(scriptfolder,'linux_kodi'), 'w+')
                writefile.write('killall Kodi\nkillall -9 kodi.bin\nkodi')
                writefile.close()
            except:
                pass
            try:
                os.system('chmod a+x '+os.path.join(scriptfolder,'linux_kodi'))
            except:
                pass
            try:
                os.system(os.path.join(scriptfolder,'linux_kodi'))
            except:
                print "### Failed to run: linux_kodi"
    else: #ATV and OSMC
        try:
            os.system('killall AppleTV')
        except:
            pass
        try:
            os.system('sudo initctl stop kodi')
        except:
            pass
        try:
            os.system('sudo initctl stop xbmc')
        except:
            pass
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
##Function to create a text box
def Open_URL(url, t):
    req = urllib2.Request(url)
    req.add_header('User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 10.0; WOW64; Windows NT 5.1; en-GB; rv:1.9.0.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36 Gecko/2008092417 Firefox/3.0.3')
# OLD ONE    req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req, timeout = t)
    link     = response.read()
    response.close()
    return link.replace('\r','').replace('\n','').replace('\t','')
#---------------------------------------------------------------------------------------------------
# Check if system is OE
def OpenELEC_Check():
    xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
    version=float(xbmc_version[:4])
    if version < 14:
        log_path_new = os.path.join(log_path,'xbmc.log')
    else:
        log_path_new = os.path.join(log_path,'kodi.log')
        
    try:
        localfile = open(log_path_new, mode='r')
        content   = localfile.read()
        localfile.close()
    except:
        try:
            localfile = open(os.path.join(HOME,'temp','kodi.log'), mode='r')
            content   = localfile.read()
            localfile.close()
        except:
            try:
                localfile = open(os.path.join(HOME,'temp','xbmc.log'), mode='r')
                content   = localfile.read()
                localfile.close()
            except:
                pass                
            
    if 'OpenELEC' in content:
        return True
#---------------------------------------------------------------------------------------------------
#Set popup xml based on platform
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
#Dialog to tell users how to register
def Register():
    dialog.ok("Register to unlock features", "To get the most out of this addon please register at the [COLOR=orange]noobs[/COLOR][COLOR=dodgerblue]and[/COLOR][COLOR=orange]nerds[/COLOR] forum for free.",'www.noobsandnerds.com')
#---------------------------------------------------------------------------------------------------
#Function to remove textures13.db and thumbnails folder
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
#Function to restore a community build
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
            print "### Download path = "+lib
# Download guisettings from the build
        dp.create("Community Builds","Downloading Skin Tweaks",'', 'Please Wait')
        try:
            downloader.download(guisettingslink, lib)
            if debug == 'true':
                print"### successfully downloaded guisettings.xml"
        except:
            dialog.ok('Problem Detected','Sorry there was a problem downloading the guisettings file. Please check your storage location, if you\'re certain that\'s ok please notify the build author on the relevant support thread.')
            if debug == 'true':
                print"### FAILED to download "+guisettingslink

# Check that gui file is a real zip and the uploader hasn't put a bad link in the db
        if zipfile.is_zipfile(lib):
            guisize = str(os.path.getsize(lib))   
        else:
            guisize = '0'
            
        dp.create("Community Builds","Downloading "+description,'', 'Please Wait')
        lib=os.path.join(CBPATH, filename+'.zip')
        
        if not os.path.exists(CBPATH):
            os.makedirs(CBPATH)

# Extract to a temporary folder so we can add new id.xml and rip out stuff not needed
        tempCPfolder = os.path.join(CP_PROFILE,'extracted')
        downloader.download(url, lib, dp)
        dp.create("Community Builds","Extracting "+description,'', 'Please Wait')
        extract.all(lib, tempCPfolder,dp)
        if os.path.exists(os.path.join(tempCPfolder,'userdata','.cbcfg')):
            try:
                os.makedirs(os.path.join(ADDON_DATA,AddonID,'updating'))
            except:
                pass
        if debug == 'true':
            print"### Downloaded build to: "+lib
            print"### Extracted build to: "+tempCPfolder
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

        print"### Build name details to store in ti_id: "+namecheck

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
        print"### ti_id/id.xml contents: "+tempcontent
        
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
            if not item in mainaddons and item != 'plugin.program.totalinstaller' and item != 'plugin.program.communitybuilds' and item != 'script.module.addon.common' and item != 'packages':
                newlist.write(item+'|')
        newlist.close()
        if debug == 'true':
            print"### Created addonlist to: "+os.path.join(clean_folder_name,'addonlist')
        exclude_dirs_full =  ['addons','cache','CP_Profiles','system','temp','Thumbnails']
        exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf','.gitignore','addons*.db','textures13.db','.cbcfg']
        message_header = "Creating Profile Data File"
        message1 = "Archiving..."
        message2 = ""
        message3 = "Please Wait"
        Archive_Tree(tempCPfolder, os.path.join(clean_folder_name,'build.zip'), message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)
        if debug == 'true':
            print"### Created: "+os.path.join(clean_folder_name,'build.zip')
# Remove the downloaded build if not set to keep in add-on settings
        if localcopy == 'false':
            os.remove(lib)
            if debug == 'true':
                print"### removed: "+lib
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
#Function to restore an OE based community build
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
#Search in description
def Search_Builds(url):
    vq = Get_Keyboard( heading="Search for content" )

# if blank or the user cancelled the keyboard, return
    if ( not vq ): return False, 0

# we need to set the title to our query
    title = urllib.quote_plus(vq)
    url += title
    Grab_Builds(url)
#---------------------------------------------------------------------------------------------------
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
        print"### Could not find build No. "+url
        dialog.ok('Build Not Found','Sorry we couldn\'t find the build, it may be it\'s marked as private or servers may be busy. Please try manually searching via the Community Builds section')
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
    link          = Open_URL(BaseURL, 5).replace('\n','').replace('\r','')
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
        o0oO('folder','[COLOR=dodgerblue]Sort by Newest[/COLOR]',str(url)+'&sortx=created&orderx=DESC',redirect,'','','','')
#        o0oO('folder','[COLOR=dodgerblue]Sort by Recently Updated[/COLOR]',str(url)+'&sortx=updated&orderx=DESC',redirect,'','','','')
        o0oO('folder','[COLOR=dodgerblue]Sort by A-Z[/COLOR]',str(url)+'&sortx=name&orderx=ASC',redirect,'','','','')
        o0oO('folder','[COLOR=dodgerblue]Sort by Z-A[/COLOR]',str(url)+'&sortx=name&orderx=DESC',redirect,'','','','')
    if type == 'public_CB':
        o0oO('folder','[COLOR=dodgerblue]Sort by Genre[/COLOR]',url,'genres','','','','')
        o0oO('folder','[COLOR=dodgerblue]Sort by Country/Language[/COLOR]',url,'countries','','','','')
#---------------------------------------------------------------------------------------------------
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
        if not item in mainaddons and item != 'plugin.program.totalinstaller' and item != 'plugin.program.communitybuilds' and item != 'script.module.addon.common' and item != 'repository.noobsandnerds' and item != 'packages':
            try:
                shutil.copytree(os.path.join(addonstemp,'addons',item),os.path.join(CP_PROFILE,'Master','backups',item))
                if debug == 'true':
                    print"### Successfully copied "+item+" to "+os.path.join(CP_PROFILE,'Master','backups',item)
            except:
                print"### Failed to copy "+item+" to backup folder, must already exist"
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
                            print"### Unable to move "+item+" as it's currently in use"
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
    print"### WIPE FUNCTIONS COMPLETE"
# Copy the rest of the data from profile folder to HOME
    try:
        localfile          = open(idfile, mode='r')
        content            = localfile.read()
        localfile.close()
        print"### original idfile contents: "+content
    except:
        print"### original id file does not exist"

    try:
        extract.all(os.path.join(CP_PROFILE,name,'build.zip'), HOME, dp)
        success = 1
        print"### Extraction of build successful"
    except:
        dialog.ok('Error',"Sorry it wasn't possible to extract your build, there is a problem with your build zip file.")
        success = 0
    if os.path.exists(os.path.join(ADDON_DATA,'plugin.program.totalinstaller','id.xml')) and os.path.exists(os.path.join(ADDON_DATA,'ti_id','id.xml')):
        print"### id.xml and temporary id.xml exists, attempting remove of original and replace with temp"
        os.remove(os.path.join(ADDON_DATA,'plugin.program.totalinstaller','id.xml'))
        print"### removal ok"
        os.rename(os.path.join(ADDON_DATA,'ti_id','id.xml'), os.path.join(ADDON_DATA,'plugin.program.totalinstaller','id.xml'))
        print"### rename ok"
    if os.path.exists(os.path.join(ADDON_DATA,'plugin.program.totalinstaller','startup.xml')) and os.path.exists(os.path.join(ADDON_DATA,'ti_id','startup.xml')):
        print"### startup.xml and temporary startup.xml exists, attempting remove of original and replace with temp"
        os.remove(os.path.join(ADDON_DATA,'plugin.program.totalinstaller','startup.xml'))
        print"### removal ok"
        os.rename(os.path.join(ADDON_DATA,'ti_id','startup.xml'), os.path.join(ADDON_DATA,'plugin.program.totalinstaller','startup.xml'))
        print"### rename ok"
# Read the contents of id.xml
    localfile          = open(idfile, mode='r')
    content            = localfile.read()
    localfile.close()

    print"### new idfile contents: "+content

    if success == 1:
        Kill_XBMC()
#---------------------------------------------------------------------------------------------------
# Menu for switching profiles - includes delete option
def Switch_Profile_Menu(url):
    o0oO('folder','[COLOR=darkcyan]DELETE A BUILD[/COLOR]',url,'delete_profile','','','')
    for name in os.listdir(CP_PROFILE):
        if name != 'Master' and name != url.replace(' ','_').replace("'",'').replace(':','-'):
            o0oO('','Load Profile: [COLOR=dodgerblue]'+name.replace('_',' ')+'[/COLOR]',name,'switch_profile','','','','')
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
            print"### No favourites file to copy"
    
    if keepsources=='true':
        try:
            sourcescontent = open(SOURCE, mode='r')
            sourcestext = sourcescontent.read()
            sourcescontent.close()
        
        except:
            print"### No sources file to copy"

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

#Download guisettings from the build
    try:
        print"### attempting to download guisettings.xml"
        downloader.download(guisettingslink, lib, dp)
        dp.close()
    except:
        dialog.ok('Problem Detected','Sorry there was a problem downloading the guisettings file. Please check your storage location, if you\'re certain that\'s ok please notify the build author on the relevant support thread.')
        print"### FAILED to download "+guisettingslink
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
            exclude_dirs_full  =  ['plugin.program.totalinstaller','plugin.program.communitybuilds','plugin.program.tbs']
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
        print"### No profiles detected, most likely a fresh wipe performed"
    
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
            print"### Attempting to add back favourites ###"
            writefile = open(FAVS, mode='w+')
            writefile.write(favestext)
            writefile.close()
            dp.update(0,"", "Copying Favourites")
        except:
            print"### Failed to copy back favourites"
    
    if keepsources == 'true':
        try:
            print"### Attempting to add back sources ###"
            writefile = open(SOURCE, mode='w+')
            writefile.write(sourcestext)
            writefile.close()
            dp.update(0,"", "Copying Sources")
        
        except:
            print"### Failed to copy back sources"
    
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
            print"### Failed to write existing profile info back into profiles.xml"

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
            print"###' Failed to remove: "+backupaddonspath
        
        try:
            shutil.rmtree(addonstemp)

        except:
            print"###' Failed to remove: "+addonstemp
    
    else:
        print"### Community Builds - using an old build"

# If the guisettings downloaded are a different size to existing we need to merge guisettings and force close
    if guiorigsize!=guisize:
        print"### GUI SIZE DIFFERENT ATTEMPTING MERGE ###"
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
#Grab User Info
def User_Info(localbuildcheck,localversioncheck,localidcheck):
    print"### USER_INFO CHECK"
    if login == 'true':
        try:
            BaseURL   = 'http://noobsandnerds.com/TI/login/login_details.php?user=%s&pass=%s' % (username, password)
            link          = Open_URL(BaseURL, 10).replace('\n','').replace('\r','')
            welcomematch  = re.compile('login_msg="(.+?)"').findall(link)
            welcometext   = welcomematch[0] if (len(welcomematch) > 0) else ''
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
        print"### ATTEMPTING TO WRITE COOKIE "
        writefile = open(cookie, mode='w+')
        writefile.write('d="'+binascii.hexlify(Timestamp())+'"\nl="'+binascii.hexlify(welcometext)+'"\nm="'+binascii.hexlify(menu)+'"')
        writefile.close()

    Categories(localbuildcheck,localversioncheck,localidcheck,welcometext,menu)
#-----------------------------------------------------------------------------------------------------------------
# Simple function to force refresh the repo's and addons folder
def Update_Repo():
    xbmc.executebuiltin( 'UpdateLocalAddons' )
    xbmc.executebuiltin( 'UpdateAddonRepos' )    
    xbmcgui.Dialog().ok('Force Refresh Started Successfully', 'Depending on the speed of your device it could take a few minutes for the update to take effect.')
    return
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
#Initial credentials check
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
        print"### First login check ###"
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
            print"### Login successful ###"
            Categories(localbuildcheck,localversioncheck,localidcheck,welcometext,livemsg)
        else:
            print"### Checking login ###"
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
                exclude_dirs_full =  ['plugin.program.totalinstaller','plugin.program.communitybuilds','plugin.program.tbs']
                exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf','.gitignore']
                message_header = "Creating full backup of existing build"
                message1 = "Archiving..."
                message2 = ""
                message3 = "Please Wait"
                Archive_Tree(HOME, backup_zip, message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)
            Wipe_Home(EXCLUDES)
            Wipe_Userdata()
            Wipe_Addons()
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
            print"### Failed to remove startup.xml"
        try:    
            os.remove(idfile)
        except:
            print"### Failed to remove id.xml"
    else:
        return
#-----------------------------------------------------------------------------------------------------------------
#For loop to wipe files in special://home but leave ones in EXCLUDES untouched
def Wipe_Home(excludefiles):
    dp.create("Wiping Existing Content",'','Please wait...', '')
    for root, dirs, files in os.walk(HOME,topdown=True):
        dirs[:] = [d for d in dirs if d not in EXCLUDES]
        for name in files:
            try:                            
                dp.update(0,"Removing [COLOR=yellow]"+name+'[/COLOR]','','Please wait...')
                os.unlink(os.path.join(root, name))
                os.remove(os.path.join(root,name))
                os.rmdir(os.path.join(root,name))
            except:
                print"Failed to remove file: "+name
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
                print "Failed to remove: "+name
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
               print"Failed to remove file: "+name
#-----------------------------------------------------------------------------------------------------------------
# Remove addon directories
def Wipe_Addons():
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
            except:
                print "Failed to remove: "+name
    except:
        pass
#-----------------------------------------------------------------------------------------------------------------
# Remove addon_data
def Wipe_Addon_Data():
    addondatadirs=[name for name in os.listdir(ADDON_DATA) if os.path.isdir(os.path.join(ADDON_DATA, name))]
    try:
        for name in addondatadirs:
            try:
                if name not in EXCLUDES:
                    dp.update(0,"Removing Add-on Data: [COLOR=yellow]"+name+' [/COLOR]','','Please wait...')
                    shutil.rmtree(os.path.join(ADDON_DATA,name))
            except:
                print "Failed to remove: "+name
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
                print "Failed to remove: "+name
    except:
        pass
#-----------------------------------------------------------------------------------------------------------------
#Report back with the version of Kodi installed
def XBMC_Version(url):
    xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
    version=float(xbmc_version[:4])
    if version < 14:
        kodiorxbmc = 'You are running XBMC'
    else:
        kodiorxbmc = 'You are running Kodi'
    dialog=xbmcgui.Dialog()
    dialog.ok(kodiorxbmc, "Your version is: %s" % version)
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
    email=urllib.unquote_plus(params["email"])
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
    link=urllib.unquote_plus(params["link"])
except:
    pass
try:
    local=urllib.unquote_plus(params["local"])
except:
    pass
try:
    messages=urllib.unquote_plus(params["messages"])
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
    posts=urllib.unquote_plus(params["posts"])
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
    unread=urllib.unquote_plus(params["unread"])
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
    welcometext=urllib.unquote_plus(params["welcometext"])
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
    localfile.close()

xmlfile = binascii.unhexlify('6164646f6e2e786d6c')
addonxml = xbmc.translatePath(os.path.join(ADDONS,AddonID,xmlfile))
localaddonversion = open(addonxml, mode='r')
content = file.read(localaddonversion)
file.close(localaddonversion)
localaddonvermatch = re.compile('<ref>(.+?)</ref>').findall(content)
addonversion  = localaddonvermatch[0] if (len(localaddonvermatch) > 0) else ''
localcheck = hashlib.md5(open(installfile,'rb').read()).hexdigest()
#if addonversion != localcheck:
 #readfile = open(bakdefault, mode='r')
 #content  = file.read(readfile)
 #file.close(readfile)
 #writefile = open(installfile, mode='w+')
 #writefile.write(content)
 #writefile.close()

print"### SKIN: "+skin

if mode == None : Video_Check()
elif mode == 'addon_loop'         : CB_Addon_Install_Loop()
elif mode == 'addon_settings'     : Addon_Settings()
elif mode == 'cb_test_loop'       : CB_Addon_Install_Loop()
elif mode == 'CB_Menu'            : CB_Menu(url)
elif mode == 'check_storage'      : checkPath.check(direct)
elif mode == 'check_updates'      : Addon_Check_Updates()
elif mode == 'clear_cache'        : Clear_Cache()
elif mode == 'community'          : CB_Root_Menu(url)
elif mode == 'community_menu'     : Community_Menu(url,video)        
elif mode == 'description'        : Description(name,url,buildname,author,version,description,updated,skins,videoaddons,audioaddons,programaddons,pictureaddons,sources,adult)
elif mode == 'delete_path'        : Delete_Path(url)
elif mode == 'delete_profile'     : Delete_Profile_Menu(url)
elif mode == 'fix_special'        : Fix_Special(url)
elif mode == 'full_clean'         : Full_Clean()
elif mode == 'grab_builds'        : Grab_Builds(url)
elif mode == 'grab_builds_premium': Grab_Builds_Premium(url)
elif mode == 'guisettingsfix'     : GUI_Settings_Fix(url,local)
elif mode == 'instructions'       : Instructions()
elif mode == 'instructions_1'     : Instructions_1()
elif mode == 'instructions_2'     : Instructions_2()
elif mode == 'instructions_3'     : Instructions_3()
elif mode == 'instructions_4'     : Instructions_4()
elif mode == 'instructions_5'     : Instructions_5()
elif mode == 'instructions_6'     : Instructions_6()
elif mode == 'kill_xbmc'          : Kill_XBMC()
elif mode == 'login_check'        : Connectivity_Check()
elif mode == 'manual_search'      : Manual_Search(url)
elif mode == 'manual_search_builds': Manual_Search_Builds()
elif mode == 'play_video'         : yt.PlayVideo(url)
elif mode == 'pop'                : pop(url)
elif mode == 'register'           : Register()
elif mode == 'remove_addon_data'  : Remove_Addon_Data()
elif mode == 'remove_addons'      : Remove_Addons(url)
elif mode == 'remove_build'       : Remove_Build()
elif mode == 'remove_crash_logs'  : Remove_Crash_Logs()
elif mode == 'remove_packages'    : Remove_Packages()
elif mode == 'remove_textures'    : Remove_Textures_Dialog()
elif mode == 'restore_community'  : Restore_Community(name,url,video,description,skins,guisettingslink,artpack)        
elif mode == 'restore_openelec'   : Restore_OpenELEC(name,url,video)
elif mode == 'run_addon'          : Run_Addon(url)
elif mode == 'search_builds'      : Search_Builds(url)
elif mode == 'showinfo'           : Show_Info(url)
elif mode == 'showinfo2'          : Show_Info2(url)
elif mode == 'SortBy'             : Sort_By(BuildURL,type)
elif mode == 'switch_profile_menu': Switch_Profile_Menu(url)
elif mode == 'switch_profile'     : Switch_Profile(url)
elif mode == 'text_guide'         : Text_Guide(url)
elif mode == 'update'             : Update_Repo()
elif mode == 'update_community'   : Update_Community(name,url,video,description,skins,guisettingslink,artpack)        
elif mode == 'user_info'          : Show_User_Info()
elif mode == 'xbmcversion'        : XBMC_Version(url)
elif mode == 'wipe_xbmc'          : Wipe_Kodi(mode)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
