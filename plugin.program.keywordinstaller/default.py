import urllib, urllib2, re, xbmcplugin, xbmcgui, xbmc, xbmcaddon
import os, sys, shutil, zipfile
import downloader, extract

######################################################
AddonID='plugin.program.keywordinstaller'
AddonName='Keyword Installer'
######################################################
ADDON            =  xbmcaddon.Addon(id=AddonID)
enablekeyword    =  ADDON.getSetting('enablekeyword')
keywordpath      =  ADDON.getSetting('keywordpath')
keywordname      =  ADDON.getSetting('keywordname')
dialog           =  xbmcgui.Dialog()
dp               =  xbmcgui.DialogProgress()
HOME             =  xbmc.translatePath('special://home/')
USERDATA         =  xbmc.translatePath(os.path.join('special://home/userdata',''))
ADDON_DATA       =  xbmc.translatePath(os.path.join(USERDATA,'addon_data'))
ADDONS           =  xbmc.translatePath(os.path.join('special://home','addons',''))
FANART           =  os.path.join(ADDONS,AddonID,'Fanart.jpg')
packages         =  os.path.join(ADDONS,'packages')
#-----------------------------------------------------------------------------------------------------------------    
#Add a standard directory and grab fanart and iconimage from artpath defined in global variables
def addDir(type,name,url,mode,iconimage = '',fanart = '',video = '',description = ''):
    iconimage = 'DefaultFolder.png'
    
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
    
    if (type=='folder'):
        ok=Add_Directory_Item(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    
    else:
        ok=Add_Directory_Item(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    
    return ok
#---------------------------------------------------------------------------------------------------
#Main Iiectory function - xbmcplugin.addDirectoryItem()
def Add_Directory_Item(handle, url, listitem, isFolder):
    xbmcplugin.addDirectoryItem(handle, url, listitem, isFolder)
#---------------------------------------------------------------------------------------------------
# Zip up the contents of a directory and all subdirectories, this will exclude the global excludes files such as guisettings.xml
def Archive_Tree(sourcefile, destfile, message_header, message1, message2, message3, exclude_dirs, exclude_files):
    zipobj       = zipfile.ZipFile(destfile , 'w', zipfile.ZIP_DEFLATED)
    rootlen      = len(sourcefile)
    for_progress = []
    ITEM         = []
    
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
# Function to create an addon pack for NaN keywords
def Create_Addon_Pack():
    mykeyword = xbmcgui.Dialog().browse(3, 'Select the folder you want to store this file in', 'files', '', False, False)
    vq = Get_Keyboard( heading="Enter a name for this keyword" )
    
    if ( not vq ):
        return False, 0
    
    title     = urllib.quote_plus(vq)
    dp.create('Backing Up Addons & Repositories','','Please Wait...')

    if not os.path.exists(addonstemp):
        os.makedirs(addonstemp)

    portalcontent   = Open_URL('http://noobsandnerds.com/TI/AddonPortal/approved.php')

# copy all the addons to addonstemp folder in userdata
    for name in os.listdir(ADDONS):
        if not 'metadata' in name and not 'module' in name and not 'script.common' in name and not 'packages' in name and not 'service.xbmc.versioncheck' in name and os.path.isdir(os.path.join(ADDONS, name)):
            try:
                dp.update(0,"Backing Up",'[COLOR yellow]%s[/COLOR]'%name, 'Please Wait...')
                                
# if the addon is on the approved list (in a repo found on NaN) just copy addons.xml
                if name in portalcontent:
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
                print"### Failed to create: "+name+' ###'
# archive files
    exclude_dirs  =  ['.svn','.git']
    exclude_files =  ['.DS_Store','Thumbs.db','.gitignore']
    destfile      = os.path.join(mykeyword,title+'.zip')
    Archive_Tree(addonstemp, destfile, 'Creating Keyword', '', '', '', exclude_dirs, exclude_files)
    try:
        shutil.rmtree(addonstemp)
    except:
        pass
    dialog.ok('New Keyword Created','Please read the instructions on how to share this keyword with the community. Your zip file can be found at:','[COLOR=dodgerblue]'+destfile+'[/COLOR]')
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
#Installs special art for premium.
def Install_Art(path):
    background_art = xbmc.translatePath(os.path.join(USERDATA,'background_art',''))
    
    if os.path.exists(background_art):
        shutil.rmtree(background_art)
    
    time.sleep(1)
    
    if not os.path.exists(background_art):
        os.makedirs(background_art)
    
    try:
        dp.create("Installing Artwork","Downloading artwork pack",'', 'Please Wait')
        artpack=os.path.join(USB, 'artpack.zip')
        downloader.download(path, artpack, dp)
        time.sleep(1)
        dp.create("Installing Artwork","Checking ",'', 'Please Wait')
        dp.update(0,"", "Extracting Zip Please Wait")
        extract.all(artpack,background_art,dp)
    
    except:
        pass
#---------------------------------------------------------------------------------------------------
# Install a keyword
def Keyword_Search(url):
    if not os.path.exists(packages):
        os.makedirs(packages)
    
    downloadurl = ''
    title       = 'Enter Keyword'
    keyword     = Search(title)
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
#(Instructions) How to create a keyword
def Instructions():
    Text_Boxes('How to create a keyword?', '[COLOR=gold]NaN MAKE IT EASY![/COLOR][CR]The keywords can now be made very simply by anyone. We\'ve not locked this down to just our addon and others can use this on similar systems for creating keywords if they want...'
    '[CR][CR][COLOR=dodgerblue][B]Step 1:[/COLOR] Use a vanilla Kodi setup[/B][CR]You will require a complete fresh install of Kodi with absolutely nothing else installed and running the default skin. Decide what kind of pack you want to create, lets say we want to create a kids pack... Add all the kid related addons you want and make sure you also have the relevant repository installed too. In the unlikely event you\'ve found an addon that doesn\'t belong in a repository that\'s fine the system will create a full backup of that addon too (just means it won\'t auto update with future updates to the addon).'
    '[CR][CR][COLOR=dodgerblue][B]Step 2:[/COLOR] Create the backup[/B][CR]Using this addon create your backup, currently only addon packs are supported but soon more packs will be added. When you create the keyword you\'ll be asked for a location to store the zip file that will be created and a name, this can be anywhwere you like and can be called whatever you want - you do not need to add the zip extension, that will automatically be added for you so in our example here we would call it "kids".'
    '[CR][CR][COLOR=dodgerblue][B]Step 3:[/COLOR] Upload the zips[/B][CR]Upload the two zip file to a server that Kodi can access, it has to be a direct link and not somewhere that asks for captcha - archive.org and copy.com are two good examples. Do not use Dropbox unless you have a paid account, they have a fair useage policy and the chances are you\'ll find within 24 hours your download has been blocked and nobody can download it.[CR][CR][COLOR=lime]Top Tip: [/COLOR]The vast majority of problems occur when the wrong download URL has been entered in the online form, a good download URL normally ends in "=1" or "zip=true". Please double check when you copy the URL into a web browser it immediately starts downloading without the need to press any other button.'
    '[CR][CR][COLOR=dodgerblue][B]Step 4:[/COLOR] Create the keyword[/B][CR]Copy the download URL to your clipboard and then go to www.urlshortbot.com. In here you need to enter the URL in the "Long URL" field and then in the "Custom Keyword" field you need to enter "noobs" (without the quotation marks) followed by your keyword. We recommend always using a random test keyword for testing because once you have a keyword you can\'t change it, also when uploading make sure it\'s a link you can edit and still keep the same URL - that way it\'s easy to keep up to date and you can still use the same keyword. In our example of kids we would set the custom keyword as "noobskids". The noobs bit is ignored and is only for helping the addon know what to look for, the user would just type in "kids" for the kids pack to be installed.')
#---------------------------------------------------------------------------------------------------
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
    exclude_dirs_full  =  [AddonID]
    exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf','Thumbs.db','.gitignore']
    message_header     = "Creating full backup of existing build"
    message_header2    = "Creating Community Build"
    message1           = "Archiving..."
    message2           = ""
    message3           = "Please Wait"
    
    Archive_Tree(HOME, myfullbackup, message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)
    dialog.ok('Full Backup Complete','You can locate your backup at:[COLOR=dodgerblue]',myfullbackup+'[/COLOR]')
#---------------------------------------------------------------------------------------------------
##Function to create a text box
def Open_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 10.0; WOW64; Windows NT 5.1; en-GB; rv:1.9.0.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36 Gecko/2008092417 Firefox/3.0.3')
# OLD ONE    req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link     = response.read()
    response.close()
    return link.replace('\r','').replace('\n','').replace('\t','')
#---------------------------------------------------------------------------------------------------
# Search text box (used in keyword search)
def Search(title):
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, title)
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered =  keyboard.getText() .replace(' ','%20')
            if search_entered == None:
                return False          
        return search_entered    
# Create a standard text box
#-----------------------------------------------------------------------------------------------------------------
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


addDir('','INSTALL Standard [COLOR=orange]noobs[/COLOR][COLOR=dodgerblue]and[/COLOR][COLOR=orange]nerds[/COLOR] Keyword', 'http://urlshortbot.com/noobs', 'keywords', '','','','')
addDir('','INSTALL [COLOR=orange]noobs[/COLOR][COLOR=dodgerblue]and[/COLOR][COLOR=orange]nerds[/COLOR] Artwork Pack', 'http://urlshortbot.com/noobsart', 'keywords', '','','','')
addDir('','CREATE [COLOR=orange]noobs[/COLOR][COLOR=dodgerblue]and[/COLOR][COLOR=orange]nerds[/COLOR] Add-on Pack', '', 'create_keyword', '','','','')
addDir('','CREATE [COLOR=orange]noobs[/COLOR][COLOR=dodgerblue]and[/COLOR][COLOR=orange]nerds[/COLOR] Artwork Pack', '', 'create_artpack', '','','','')
addDir('','[COLOR=darkcyan][INSTRUCTIONS][/COLOR] Creating a keyword','','instructions','','','','')

if mode   == 'instructions' : Instructions()
elif mode == 'keywords'     : Keyword_Search(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))