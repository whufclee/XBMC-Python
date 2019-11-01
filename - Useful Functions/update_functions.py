# These imports and variables may or may not be used, I've left them here as some are definitely used in some modules.
import urllib, urllib2, re, xbmcplugin, xbmcgui, xbmc, xbmcaddon, os, sys, time, xbmcvfs, datetime, zipfile, shutil, binascii, hashlib
import downloader
import extract
import yt
import threading

try:
    import json as simplejson 
except:
    import simplejson

ADDONID                    = 'script.openwindow'
ADDON                      = xbmcaddon.Addon(ADDONID)
ADDONS                     = xbmc.translatePath(os.path.join('special://home','addons',''))
ADDONPATH                  = xbmcaddon.Addon('script.openwindow').getAddonInfo("path")
LANGUAGEPATH               = xbmc.translatePath(os.path.join(ADDONPATH,'resources','language'))
ACTION_HOME                = 7
ACTION_PREVIOUS_MENU       = 10
ACTION_SELECT_ITEM         = 7
installfile                = xbmc.translatePath(os.path.join(ADDONS,ADDONID,'default.py'))
dialog                     = xbmcgui.Dialog()
dp                         = xbmcgui.DialogProgress()
skin                       = xbmc.getSkinDir()
currently_downloaded_bytes = 0.0
max_Bps                    = 0.0
restore_dir                = '/storage/.restore/'
path                       = xbmc.translatePath(os.path.join('special://home/addons','packages'))
thumbnails                 = xbmc.translatePath(os.path.join('special://home','userdata','Thumbnails'))
PACKAGES                   = xbmc.translatePath(os.path.join('special://home','addons','packages',''))
HOME                       = xbmc.translatePath('special://home/')
RestoreGUI                 = os.path.join(HOME,'userdata','addon_data','service.openelec.settings','restoregui')
RunWizard                  = os.path.join(HOME,'userdata','addon_data','service.openelec.settings','runwizard')
timepath                   = os.path.join(HOME,'userdata','addon_data','service.openelec.settings','dltime')
addondata                  = os.path.join(HOME,'userdata','addon_data','service.openelec.settings')
SYSTEM                     = xbmc.translatePath('special://xbmc/')
branding_update            = xbmc.translatePath('special://home/media/branding/branding_update.png')
ipaddress                  = xbmc.getIPAddress()
log_path                   = xbmc.translatePath('special://logpath/')
m3u_file                   = xbmc.translatePath(os.path.join(HOME, 'debug.txt'))
addonfolder                = xbmc.translatePath('special://home/addons/script.openwindow/')
xbmc_version               = xbmc.getInfoLabel("System.BuildVersion")
email = ''
download_thread = ''

if not os.path.exists(addonfolder):
    addonfolder = xbmc.translatePath('special://xbmc/addons/script.openwindow/')
	
#----------------------------------------------------------------------------------------------
#############################################################
# Check if system is OpenELEC, returns true or false.       #
#                                                           #
# Example:                                                  #
#         variable = Openelec()                             #
#         if variable:                                      #
#############################################################	
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
#############################################################
# Original Keyword Search/Install from TBS addon            #
# This can be edited, only main difference is the download  #
# will not be using URLShortbot. Will send search paramater #
# to tlbb.me/<some_query> which gets details of build.      #
# Will need to send MAC to compare against db in case it's  #
# marked as a private build. See Activation module.         #
#############################################################	
def Keyword_Search(url):
    if not os.path.exists(packages):
        os.makedirs(packages)
    
    downloadurl = ''
    title       = 'Enter Keyword'
    keyword     = SEARCH(title)
    downloadurl = url+keyword
    lib         = os.path.join(packages, keyword+'.zip')
    
# Function for putting the box in test mode, testmode will make the unit check every 20 seconds for a new update. testoff is default of 30mins.
    if keyword == 'teston' or keyword == 'testoff':
        if keyword == 'teston':
            readfile = open(SETTINGSXML).read()
            replacecontent = readfile.replace('checknews.py,silent=true),00:30:00','checknews.py,silent=true),00:00:20')
            message = 'Test mode now ENABLED. Test mode successfully enabled, update checks will now take place every 20 seconds'
            xbmc.executebuiltin('StopScript(special://home/addons/plugin.program.tbs/service.py)')
            xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.tbs/service.py)')
            writefile      = open(SETTINGSXML, mode='w')
            writefile.write(str(replacecontent))
            writefile.close()
            dialog.ok('SUCCESS',message)
        if keyword == 'testoff':
            Test_Off()
        xbmc.executebuiltin('Container.Refresh')

# if the keyword is a real keyword then offer option to backup existing install		
    if keyword !='' and keyword !='teston' and keyword != 'testoff':
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
                    if 'venztech' in url:
                        extract.all(lib,'/storage',dp)
                    else:
                        extract.all(lib,HOME,dp)
                    xbmc.executebuiltin('UpdateLocalAddons')
                    xbmc.executebuiltin( 'UpdateAddonRepos' )
                    dialog.ok("Web Installer", "","Content now installed", "")
                    dp.close()
                
                except:
                    dialog.ok("Error with zip",'There was an error trying to install this file. It may possibly be corrupt, either try again or contact the author of this keyword.')
                    print"### Unable to install keyword (passed zip check): "+keyword
            
            else:
                try:
                    if os.path.getsize(lib) > 100000 and 'venztech' in url:
                        dp.create("Restoring Backup","Copying Files...",'', 'Please Wait')
                        os.rename(lib,restore_dir+'20150815123607.tar')
                        dp.update(0,"", "Kodi will now reboot")
                        xbmc.executebuiltin('reboot')
                    else: dialog.ok("Keyword error",'The keyword you typed could not be installed.','Please check the spelling and if you continue to receive','this message it probably means that keyword is no longer available.')
                except:
                    dialog.ok("Error with zip",'The file you attempted to download is not in a valid zip format, please double check you typed in the correct word.')
                    print"### UNABLE TO INSTALL BACKUP - IT IS NOT A ZIP"
        
        except:
            dialog.ok("Keyword Error",'The keyword you typed could not be installed. Please check the spelling and if you continue to receive this message it probably means that keyword is no longer available.')
            print"### Unable to install keyword (unknown error, most likely a typo in keyword entry): "+keyword
    
    if os.path.exists(lib):
        os.remove(lib)
		
def Test_Off():
    readfile = open(SETTINGSXML).read()
    replacecontent = readfile.replace('checknews.py,silent=true),00:00:20', 'checknews.py,silent=true),00:30:00')
    message = 'Test mode now DISABLED. Normal update mode resumed, updates will now check every 30 minutes.'
    xbmc.executebuiltin('StopScript(special://home/addons/plugin.program.tbs/service.py)')
    xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.tbs/service.py)')
    xbmc.executebuiltin('Container.Refresh')
    writefile      = open(SETTINGSXML, mode='w')
    writefile.write(str(replacecontent))
    writefile.close()
    dialog.ok('SUCCESS',message)
	
#------------------------------------------------------------------------------------------------------------
#############################################################
# Generic keyboard search box                               #
# Returns the text entered and quits cleanly if esc pressed #
#############################################################
def SEARCH(searchtext):
        print"SEARCH"
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered,searchtext)
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered =  keyboard.getText() .replace(' ','%20')
            if search_entered == None:
                return False          
        return search_entered
		
#------------------------------------------------------------------------------------------------------------
##############################################################
# Set of modules for showing a nice update screen that can't #
# be escaped out of, this also allows for showing a yt video #
# whilst downloading and will extract a zip and force close  #
# once extraction completed.                                 #
##############################################################

# Main script for showing the window
class Image_Screen(xbmcgui.Window):
  def __init__(self,*args,**kwargs):
    global download_thread
    self.header=kwargs['header']
    self.background=kwargs['background']
    self.icon=kwargs['icon']
    self.maintext=kwargs['maintext']

    if not os.path.exists(branding_update):
        self.addControl(xbmcgui.ControlImage(0,0,1280,720, addonfolder+'resources/images/whitebg.jpg'))
    self.addControl(xbmcgui.ControlImage(0,0,1280,720, branding_update))

# Add rotating update icon
    self.updateimage = xbmcgui.ControlImage(200,230,250,250, addonfolder+'resources/images/'+self.icon)
    self.addControl(self.updateimage)   
    self.updateimage.setAnimations([('conditional','effect=rotate start=0 end=360 center=auto time=3000 loop=true condition=true',)])

# Add description text
    if not os.path.exists(branding_update):
        self.strDescription = xbmcgui.ControlTextBox(570, 250, 600, 300, 'font14','0xFF000000')
        self.addControl(self.strDescription)
        self.strDescription.setText(self.maintext)
    
  def onAction(self, action):
    if action == ACTION_PREVIOUS_MENU or action == ACTION_HOME:
      print"ESC and HOME Disabled"
#---------------------------------			
# This has been added as a separate function so we can use threading (conntinue downloading while running more of the script)
def Download_Function(url):
    urllib.urlretrieve(url,lib)
#---------------------------------			
# This calls the actual main update window    
def Update_Screen():
    mydisplay = Image_Screen(
        header='Update In Progress',
        background='register.png',
        icon='update_software.png',
        maintext=ADDON.getLocalizedString(30074),
        )
    mydisplay .doModal()
    del mydisplay
#---------------------------------			
# Main function to actually download/extract and calls the threading commands	
def Download_Extract(url,video):
    global download_thread
    global endtime
    download_thread = threading.Thread(target=Download_Function, args=[url])
    updatescreen_thread = threading.Thread(target=Update_Screen)
    try:
        download_thread.start()
        starttime = datetime.datetime.now()
        print"###Download Started"
    except:
        dialog.ok('Error','Unable to download updates from server. Please try opening a web browser on your PC to make sure your internet is working correctly. Click OK to try again.')
        return
    try:
        yt.PlayVideo(video)
    except:
        pass
    while xbmc.Player().isPlaying():
        xbmc.sleep(500)
    updatescreen_thread.start()
    while download_thread.isAlive():
        xbmc.sleep(500)

# This is used to get our speedtest results, you probably won't need this
    endtime   = datetime.datetime.fromtimestamp(os.path.getmtime(lib))
    timediff  = endtime-starttime
    libsize   = os.path.getsize(lib) / (128*1024.0)
    timediff = str(timediff).replace(':','')
    speed = libsize / float(timediff)
    writefile = open(timepath, mode='w+')
    writefile.write(str(speed))
    writefile.close()

# Deal with the downloaded file, you'll need to extract but pass through a password because it will be pw protected zip
    if os.path.exists(lib) and zipfile.is_zipfile(lib):
        zin = zipfile.ZipFile(lib, 'r')
        zin.extractall(rootfolder)
        try:
            os.remove(lib)
        except:
            print"### Failed to remove temp file"
        Remove_Textures()
        if not os.path.exists(RunWizard):
            os.makedirs(RunWizard)
        print"### Removed textures"
        KILL_KODI()
		
#----------------------------------------------------------------------------------------
##############################################################
# This checks activation status based on contents of URL     #
# which is populated by PHP based on params sent.            #
#                                                            #
# You'll see the encryptme function is called everytime we   #
# make any URL calls, this must always be used.              #
# The enctyptme function I've created can use 'd' to decrypt #
# or 'e' will encrypt. Take a look at the examples below.    #
##############################################################
def Check_Status():
    print"Check_Status"
    url   = ''
    video = ''
    status = Activate()
# If the url contains a ~ we know we need to split it at that point as it contains two variables we need
    if '~' in status:
        url,video = status.split('~')
        url = encryptme('d',url)
        video = encryptme('d',video)
    else:
        try:
            url = encryptme('d',status)
        except:
            pass
# If activation sends back vanilla
    if  url==encryptme('d','595d515c110b0d1804'):
        mode = 'quit'

# If activation sends back registration
    if encryptme('d','5b6767632d2222675f555521605804060d1006') in url:
        if '~' in status and not os.path.exists(xbmc.translatePath(os.path.join(HOME,'media','branding'))):
            try:
                xbmc.executebuiltin("ActivateWindow(busydialog)")
                urllib.urlretrieve(video,lib)
                xbmc.executebuiltin("Dialog.Close(busydialog)")
            except:
                pass
            if os.path.exists(lib) and zipfile.is_zipfile(lib):
                zin = zipfile.ZipFile(lib, 'r')
                zin.extractall(rootfolder)
                zin.close()
                try:
                    os.remove(lib)
                except:
                    pass
        Get_Activation(url)
                
# If download URL in activation
    elif encryptme('d','5e6a6a663025250b1c0a0506') in url:
        Download_Extract(url,video)
        
# If user has no internet on first boot and wants to use Kodi vanilla
    elif status == 'back':
        try:
            shutil.rmtree(addondata)
        except:
            pass
        xbmc.executebuiltin('reboot')
		
#----------------------------------------------------------------------------------------
##############################################################
# Force close Kodi, this ensures guisettings are stored.     #
##############################################################        
def KILL_KODI():
    print"KILL_KODI"
    if xbmc.getCondVisibility('system.platform.windows'):
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im Kodi.exe /f')
        except:
            pass
        try:
            os.system('@ECHO off')
            os.system('tskill Kodi.exe')
        except:
            pass
        try:
            os.system('@ECHO off')
            os.system('tskill XBMC.exe')
        except:
            pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im XBMC.exe /f')
        except:
            pass
    elif xbmc.getCondVisibility('system.platform.osx'):
        try:
            os.system('killall -9 XBMC')
        except:
            pass
        try:
            os.system('killall -9 Kodi')
        except:
            pass
    else:
#    elif xbmc.getCondVisibility('system.platform.linux'):
        try:
            os.system('killall XBMC')
        except:
            pass
        try:
            os.system('killall Kodi')
        except:
            pass
        try:
            os.system('killall -9 xbmc.bin')
        except:
            pass
        try:
            os.system('killall -9 kodi.bin')
        except:
            pass
 #   else: #ATV
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
#    elif xbmc.getCondVisibility('system.platform.android'):
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
        dialog.ok('Attempting to use advanced task killer apk','If you have the advanced task killer apk installed please click the big button at the top which says "KILL selected apps". Click "OK" then "Kill selected apps. Please be patient while your system updates the necessary files and your skin will automatically switch once fully updated.')
        try:
            xbmc.executebuiltin('StartAndroidActivity(com.rechild.advancedtaskkiller)')
        except:
            pass
			
#----------------------------------------------------------------------------------------
##############################################################
# Flush the textures13.db and wipe thumbnails directory      #
# A restart is required after calling this                   #
##############################################################
def Remove_Textures():
    textures  =  xbmc.translatePath('special://home/userdata/Database/Textures13.db')
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
    shutil.rmtree(thumbnails)
	
#----------------------------------------------------------------------------------------
##############################################################
# Get full CPU information, we need to send this when making #
# URL calls to check activation.                             #
#                                                            #
# Example:                                                   #
#         variable = CPU_Check()                             #
#         print variable                                     #
#         "intel based ...."                                 #
##############################################################
def CPU_Check():
    version=str(xbmc_version[:2])
    if version < 14:
        logfile = os.path.join(log_path, 'xbmc.log')
    
    else:
        logfile = os.path.join(log_path, 'kodi.log')

    filename    = open(logfile, 'r')
    logtext     = filename.read()
    filename.close()

    CPUmatch    = re.compile('Host CPU: (.+?) available').findall(logtext)
    CPU         = CPUmatch[0] if (len(CPUmatch) > 0) else ''
    return CPU.replace(' ','%20')
	
#----------------------------------------------------------------------------------------
##############################################################
# Get full Build information, we need to send this when      #
# making URL calls to check activation. This gets FULL build #
# info and not the crappy one Kodi returns.                  #
#                                                            #
# Example:                                                   #
#         variable = Build_Info()                            #
#         print variable                                     #
#         "full build details not just github timestamp"     #
##############################################################
def Build_Info():
    version=str(xbmc_version[:2])
    if version < 14:
        logfile = os.path.join(log_path, 'xbmc.log')
    
    else:
        logfile = os.path.join(log_path, 'kodi.log')

    filename    = open(logfile, 'r')
    logtext     = filename.read()
    filename.close()

    Buildmatch  = re.compile('Running on (.+?)\n').findall(logtext)
    Build       = Buildmatch[0] if (len(Buildmatch) > 0) else ''
    return Build.replace(' ','%20')
	
#----------------------------------------------------------------------------------------
##############################################################
# Get Mac Address, we need to send this when making URL      #
# calls to check activation. You can get wi-fi or ethernet   #
# mac on all systems apart from windows (that only shows     #
# ethernet on Windows).                                      #
#                                                            #
# Example:                                                   #
#         variable = getMacAddress('wifi')                   #
#         print variable                                     #
#         "WiFi Mac"                                         #
#                                                            #
#         variable2 = getMacAddress('eth0')                  #
#         print variable                                     #
#         "Ethernet Mac"                                     #
##############################################################
def getMacAddress(protocol):
    if sys.platform == 'win32': 
        for line in os.popen("ipconfig /all"): 
            if line.lstrip().startswith('Physical Address'): 
                mac = line.split(':')[1].strip().replace('-',':')
                break 

    if xbmc.getCondVisibility('System.Platform.Android'):
        if protcol == 'wifi':
            readfile = open('/sys/class/net/wlan0/address', mode='r')
        else:
            readfile = open('/sys/class/net/eth0/address', mode='r')
        mac = readfile.read()
        mac = mac[:17]
        readfile.close()

    else:
        if protocol == 'wifi':
            for line in os.popen("/sbin/ifconfig"): 
                if line.find('wlan0') > -1: 
                    mac = line.split()[4] 
                    break
        else:
           for line in os.popen("/sbin/ifconfig"): 
                if line.find('eth0') > -1: 
                    mac = line.split()[4] 
                    break
    return str(mac)
	
#----------------------------------------------------------------------------------------
##############################################################
# Show a full screen text box                                #
#                                                            #
# Example:                                                   #
#         Text_Boxes('Test Heading','Body Text Here')        #
##############################################################
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
	  
#----------------------------------------------------------------------------------------
##############################################################
# Check activation, this is the main function for checking   #
# and gives a good working example of how to send the        #
# enctyption with mac, cpu and build info.                   #
##############################################################    
def Activate():
    counter = 0
    success = 0
    try:
        wifimac = getMacAddress('wifi')
    except:
        wifimac = 'Unknown'
    try:
        ethmac  = getMacAddress('eth0')
    except:
        ethmac  = 'Unknown'
    try:
        cpu     = CPU_Check()
    except:
        cpu     = 'Unknown'
    try:
        build   = Build_Info()
    except:
        build   = 'Unknown'
    urlparams = wifimac+'&'+cpu+'&'+build+'&'+ethmac.replace(' ','%20')
    while counter <3 and success == 0:
        try:
            counter += 1
            link = Open_URL(encryptme('d','4a5656521c1111564e4444104f471123464610524a52215a1f0e16141e04')+encryptme('e',urlparams))
            success = 1
        except:
            dialog.ok(ADDON.getLocalizedString(30075),ADDON.getLocalizedString(30076))
    if success == 1:
        return link
    else:
        choice = dialog.yesno(ADDON.getLocalizedString(30075),ADDON.getLocalizedString(30077))
        if choice == 1:
            dialog.ok(ADDON.getLocalizedString(30075),ADDON.getLocalizedString(30078))
            try:
                shutil.rmtree(addondata)
            except:
                pass
            return '595d515c110b0d1804'
        else:
            return 'back'
			
#----------------------------------------------------------------------------------------
##############################################################
# Basic URL call function using urllib2 module               #
##############################################################    
def Open_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 10.0; WOW64; Windows NT 5.1; en-GB; rv:1.9.0.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36 Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link     = response.read()
    response.close()
    return link.replace('\r','').replace('\n','').replace('\t','')
	
#----------------------------------------------------------------------------------------
##############################################################
# This is our clever enctyption method. DO NOT share this    #
# with anybody as it took many days to code up and get the   #
# server working with it. For your eyes only!                #
#                                                            #
# Example:                                                   #
#        print encryptme('d','595d515c110b0d1804')           #
#        ^ will return the decrypted string                  #
#                                                            #
#        print encryptme('e','Hello World')                  #
#        ^ will return the encrypted string of "Hello World" #
##############################################################    
def encryptme(mode, message):
    if mode == 'e':
        import random
        count = 0
        finaltext = ''
        while count < 4:
            count += 1
            randomnum = random.randrange(1, 31)
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
		
#----------------------------------------------------------------------------------------
##############################################################
# Taken from CP addon, localversioncheck is a variable sent  #
# to this function with details of the date held in a file   #
# which would be included in the downloaded keyword zip.     #
# For TLBB this will then check tlbb.me/<some_url>           #
# and return true or false as to whether or not a new        #
# update to the zip is available. If it is then offer to     #
# download it.                                               #
##############################################################    
def Check_For_Update(localversioncheck,id):
    BaseURL = 'http://noobsandnerds.com/TI/Community_Builds/buildupdate.php?id=%s' % (id)
    link    = Open_URL(BaseURL).replace('\n','').replace('\r','')
    
    if id != 'None':
        versioncheckmatch = re.compile('version="(.+?)"').findall(link)
        versioncheck  = versioncheckmatch[0] if (len(versioncheckmatch) > 0) else ''
    
        if  localversioncheck < versioncheck:
            return True
    
    else:
        return False
		
#----------------------------------------------------------------------------------------
##############################################################
# Taken from TBS addon, useful little function for splitting #
# a string into chunks. For example if you want to split the #
# string "Hello World" into chunks of 3 chars in length you  #
# would do the following:                                    #
# chunks("Hello World",3)                                    #
# ^output: ['Hel','lo ','Wor','ld']                          #
##############################################################    
def chunks(s, n):
    for start in range(0, len(s), n):
        yield s[start:start+n]
		
#----------------------------------------------------------------------------------------
##############################################################
# Walk through all sub-directories and change specific text  #
# in a specific filename. This example changes the special   #
# paths in all xml files.                                    #
##############################################################    
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
				 
#----------------------------------------------------------------------------------------
##############################################################
# Walk through all sub-directories and get the size of all   #
# files combined together. The size paramater can be set to  #
# zero if you have no other number you need to add it to.    #
##############################################################    
def Get_Size(path,size):
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            dp.update(0,"Calulating...",'[COLOR=dodgerblue]'+f+'[/COLOR]', 'Please Wait')
            fp = os.path.join(dirpath, f)
            size += os.path.getsize(fp)
    return size
	
#----------------------------------------------------------------------------------------
##############################################################
# Old function from Total Installer, never used. However we  #
# will need to create an artwork pack and main build pack so #
# might be useful.                                           #
##############################################################    
def Install_Art(path):
    background_art = os.path.join(HOME,'media')

# remove the whole media directory if it exists   
    if os.path.exists(background_art):
        shutil.rmtree(background_art)
    
    time.sleep(1)
    
    if not os.path.exists(background_art):
        os.makedirs(background_art)
    
    try:
        dp.create("Installing Artwork","Downloading artwork pack",'', 'Please Wait')
        artpack=os.path.join(USB, I1IiiI+'_artpack.zip')
        downloader.download(path, artpack, dp)
        time.sleep(1)
        dp.create("[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]","Checking ",'', 'Please Wait')
        dp.update(0,"", "Extracting Zip Please Wait")
        extract.all(artpack,background_art,dp)
    
    except:
        pass
		
#----------------------------------------------------------------------------------------
################################################################
# Doubt this will be any use but you never know it may come in #
# handy. Downloads everything from a URL including subfolders. #
################################################################  
def Recursive_Loop(recursive_location,remote_path):
    if not os.path.exists(recursive_location):
        os.makedirs(recursive_location)
    
    link   = Open_URL(remote_path).replace('\n','').replace('\r','')
    match  = re.compile('href="(.+?)"', re.DOTALL).findall(link)
    
    for href in match:
        filepath=xbmc.translatePath(os.path.join(recursive_location,href)) #works
        
        if '/' not in href:
            
            try:
                dp.update(0,"Downloading [COLOR=darkcyan]"+href+'[/COLOR]','','Please wait...')
                downloader.download(remote_path+href, filepath, dp)
            
            except:
                print"failed to install"+href
        
        if '/' in href and '..' not in href and 'http' not in href:
            remote_path2 = remote_path+href
            Recursive_Loop(filepath,remote_path2)
        
        else:
            pass
			
#----------------------------------------------------------------------------------------
################################################################
# Returns the current timestamp in a nice string format, great #
# for checking against other timestamps.                       #
################################################################  
def Timestamp():
    now = time.time()
    localtime = time.localtime(now)
    return time.strftime('%Y%m%d%H%M%S', localtime)
	
#----------------------------------------------------------------------------------------
################################################################
# Check against google.com and google.cn to see if device is   #
# managing to connect to the web ok.                           #
################################################################  
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