#
#       Copyright (C) 2015
#       Json Edits and Various tweaks by OpenELEQ (OpenELEQ@gmail.com)
#       Based on original work by:
#       Lee Randall (info@totalrevolution.tv)
#
#  This software is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International Public License
#  You can find a copy of the license in the add-on folder

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
installfile                = '/usr/share/kodi/addons/script.openwindow/default.py'
if not os.path.exists(installfile):
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
testdebug                  = ADDON.getSetting('testdebug')
email = ''
download_thread = ''

if not os.path.exists(addonfolder):
    addonfolder = xbmc.translatePath('special://xbmc/addons/script.openwindow/')

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

if OpenELEC_Check():
    rootfolder                 = '/storage'
    venzpath                   = '/storage/downloads'
    if not os.path.exists(restore_dir):
        os.makedirs(restore_dir)
else:
    rootfolder = HOME
    venzpath   = HOME[:-6]
    venzpath   = xbmc.translatePath(os.path.join(venzpath, 'temp_download'))
    if testdebug == 'true':
        print "### venzpath: "+venzpath

if not os.path.exists(venzpath):
    os.makedirs(venzpath)
lib = os.path.join(venzpath,'target.zip')

if not os.path.exists(PACKAGES):
    os.makedirs(PACKAGES)


class Image_Screen(xbmcgui.Window):
  def __init__(self,*args,**kwargs):
    global download_thread
    self.header=kwargs['header']
    self.background=kwargs['background']
    self.icon=kwargs['icon']
    self.maintext=kwargs['maintext']

    if not os.path.exists(branding_update):
        self.addControl(xbmcgui.ControlImage(0,0,1280,720, addonfolder+'resources/images/whitebg.jpg'))
#    self.addControl(xbmcgui.ControlImage(0,0,1280,720, addonfolder+'resources/images/'+self.background))
    self.addControl(xbmcgui.ControlImage(0,0,1280,720, branding_update))
    self.updateimage = xbmcgui.ControlImage(200,230,250,250, addonfolder+'resources/images/'+self.icon)
    self.addControl(self.updateimage)   
    self.updateimage.setAnimations([('conditional','effect=rotate start=0 end=360 center=auto time=3000 loop=true condition=true',)])

# Add header text
#    self.strHeader = xbmcgui.ControlLabel(350, 150, 250, 20, '', 'font14','0xFF000000')
#    self.addControl(self.strHeader)
#    self.strHeader.setLabel(self.header)
# Add description text
    if not os.path.exists(branding_update):
        self.strDescription = xbmcgui.ControlTextBox(570, 250, 600, 300, 'font14','0xFF000000')
        self.addControl(self.strDescription)
        self.strDescription.setText(self.maintext)
    
  def onAction(self, action):
    if action == ACTION_PREVIOUS_MENU or action == ACTION_HOME:
      print"ESC and HOME Disabled"

        
class MainMenu(xbmcgui.Window):
  def __init__(self,*args,**kwargs):
    self.header=kwargs['header']
    self.background=kwargs['background']
    
    if kwargs['backbutton'] != '':
        self.backbutton=kwargs['backbutton']
    else:
        self.backbutton=''
    if kwargs['nextbutton'] != '':
        self.nextbutton=kwargs['nextbutton']
    else:
        self.nextbutton=''

    self.backbuttonfunction=kwargs['backbuttonfunction']
    self.nextbuttonfunction=kwargs['nextbuttonfunction']

    if kwargs['selectbutton'] != '':
        self.selectbutton=kwargs['selectbutton']
    else:
        self.selectbutton=''
    self.toggleup=kwargs['toggleup']
    self.toggledown=kwargs['toggledown']
    self.selectbuttonfunction=kwargs['selectbuttonfunction']
    self.toggleupfunction=kwargs['toggleupfunction']
    self.toggledownfunction=kwargs['toggledownfunction']
    self.maintext=kwargs['maintext']

    if kwargs['noconnectionbutton'] != '':
        self.noconnectionbutton=kwargs['noconnectionbutton']
    else:
        self.noconnectionbutton=''

    self.noconnectionfunction=kwargs['noconnectionfunction']
# Add background images
    self.addControl(xbmcgui.ControlImage(0,0,1280,720, addonfolder+'resources/images/smoke_background.jpg'))
    self.addControl(xbmcgui.ControlImage(0,0,1280,720, addonfolder+'resources/images/'+self.background))
    self.addControl(xbmcgui.ControlImage(0,0,1280,720, 'special://home/media/branding/branding.png'))

# Add next button
    self.button1 = xbmcgui.ControlButton(910, 600, 225, 35, self.nextbutton,font='font13',alignment=2,focusTexture=addonfolder+'resources/images/button-focus.png',noFocusTexture=addonfolder+'resources/images/non-focus.jpg')
    self.addControl(self.button1)

# Add back button
    if self.backbutton != '':
        self.button2 = xbmcgui.ControlButton(400, 600, 225, 35, self.backbutton,font='font13',alignment=2,focusTexture=addonfolder+'resources/images/button-focus.png',noFocusTexture=addonfolder+'resources/images/non-focus.jpg')
        self.addControl(self.button2)

# Add buttons - if toggle buttons blank then just use one button
    if self.toggleup=='':
        if self.noconnectionbutton=='':
            self.button0 = xbmcgui.ControlButton(910, 480, 225, 35, self.selectbutton,font='font13',alignment=2,focusTexture=addonfolder+'resources/images/button-focus.png',noFocusTexture=addonfolder+'resources/images/non-focus.jpg')
        else:
            if ipaddress != '0':
                self.button0 = xbmcgui.ControlButton(910, 480, 225, 35, self.selectbutton,font='font13',alignment=2,focusTexture=addonfolder+'resources/images/button-focus.png',noFocusTexture=addonfolder+'resources/images/non-focus.jpg')
            elif ipaddress == '0':
                self.button0 = xbmcgui.ControlButton(910, 480, 225, 35, self.noconnectionbutton,font='font13',alignment=2,focusTexture=addonfolder+'resources/images/button-focus.png',noFocusTexture=addonfolder+'resources/images/non-focus.jpg')
        self.addControl(self.button0)
        self.button0.controlDown(self.button1)
        self.button0.controlRight(self.button1)
        self.button0.controlUp(self.button1)
        if self.backbutton != '':
            self.button0.controlLeft(self.button2)
    else:
        self.toggleupbutton = xbmcgui.ControlButton(1000, 480, 35, 35, '', focusTexture=addonfolder+'resources/images/button-focus.png',noFocusTexture=addonfolder+'resources/images/non-focus.jpg')
        self.toggledownbutton = xbmcgui.ControlButton(1000, 500, 35, 35, '', focusTexture=addonfolder+'resources/images/button-focus.png',noFocusTexture=addonfolder+'resources/images/non-focus.jpg')
        self.addControl(self.toggleupbutton)
        self.addControl(self.toggledownbutton)
        self.strToggleUp = xbmcgui.ControlLabel(380, 50, 250, 20, '', 'font13','0xFFFFFFFF')
        self.strToggleDown = xbmcgui.ControlLabel(380, 50, 250, 20, '', 'font13','0xFFFFFFFF')
        self.addControl(self.strToggleUp)
        self.addControl(self.strToggleDown)
        self.strToggleUp.setLabel(self.toggleup)
        self.strToggleDown.setLabel(self.toggledown)
        self.toggleupbutton.controlDown(self.toggledownbutton)
        if self.backbutton != '':
            self.toggleupbutton.controlLeft(self.button2)
            self.toggledownbutton.controlLeft(self.button2)
        self.toggledownbutton.controlUp(self.toggleupbutton)
        self.toggledownbutton.controlDown(self.button1)
        
    if self.toggleup=='':
        self.setFocus(self.button1)
    else:
        self.setFocus(self.toggleupbutton)

    if self.backbutton != '':
        self.button1.controlLeft(self.button2)
        self.button1.controlRight(self.button2)
        self.button2.controlRight(self.button1)
        self.button2.controlLeft(self.button1)
    if self.toggleup=='':
        self.button1.controlUp(self.button0)
        if self.backbutton != '':
            self.button2.controlUp(self.button0)
    else:
        self.button1.controlUp(self.toggledownbutton)
        if self.backbutton != '':
            self.button2.controlUp(self.toggledownbutton)
        

# Add header text
    self.strHeader = xbmcgui.ControlLabel(380, 50, 250, 20, '', 'font14','0xFFFFFFFF')
    self.addControl(self.strHeader)
    self.strHeader.setLabel(self.header)
# Add internet warning text (only visible if not connected)
    if ipaddress == '0':
        self.strWarning = xbmcgui.ControlTextBox(830, 300, 300, 200, 'font13','0xFFFF0000')
        self.addControl(self.strWarning)
        self.strWarning.setText('No internet connection.[CR]To be able to get the most out of this device and set options like this you must be connected to the web. Please insert your ethernet cable or setup your Wi-Fi.')
# Add description text
    self.strDescription = xbmcgui.ControlTextBox(800, 130, 320, 300, 'font14','0xFF000000')
    self.addControl(self.strDescription)
    self.strDescription.setText(self.maintext)
    
  def onAction(self, action):
    if action == ACTION_PREVIOUS_MENU and self.selectbutton == 'Register':
      self.close()
      Skip_Registration()
 
  def onControl(self, control):
    if control == self.button0:
        if ipaddress != '0' or self.noconnectionbutton=='':
            exec self.selectbuttonfunction
        else:
            exec self.noconnectionfunction
    if control == self.button1:
      exec self.nextbuttonfunction
    if self.backbutton != '':
        if control == self.button2:
          exec self.backbuttonfunction

  def message(self, message):
    dialog = xbmcgui.Dialog()
    dialog.ok(" My message title", message) 

    
def Get_Activation(mode):
    if mode == 'check':
        if Check_Status():
            statusinfo = ADDON.getLocalizedString(30065)
        else:
            statusinfo = ADDON.getLocalizedString(30066)
    else:
        statusinfo = ''
        registration_link = mode
    mydisplay = MainMenu(
        header=ADDON.getLocalizedString(30062),
        background='register.png',
        backbutton=ADDON.getLocalizedString(30067),
        nextbutton=ADDON.getLocalizedString(30002),
        backbuttonfunction='self.close();Skip_Registration()',
        nextbuttonfunction='self.close();Check_Status()',
        selectbutton=ADDON.getLocalizedString(30068),
        toggleup='',
        toggledown='',
        selectbuttonfunction="self.close();Check_Status()",
        toggleupfunction='',
        toggledownfunction='',
        maintext=ADDON.getLocalizedString(30069)+registration_link+'[/COLOR]'+statusinfo,
        noconnectionbutton='ADDON.getLocalizedString(30019)',
        noconnectionfunction="xbmc.executebuiltin('ActivateWindow(home)');xbmc.executebuiltin('RunAddon(service.openelec.settings)');xbmc.executebuiltin('RunAddon(script.openwindow)')"
        )
    mydisplay .doModal()
    del mydisplay


def Skip_Registration():
    print"Skip_Registration"
    mydisplay = MainMenu(
        header=ADDON.getLocalizedString(30067),
        background='donotregister.png',
        backbutton=ADDON.getLocalizedString(30070),
        nextbutton=ADDON.getLocalizedString(30071),
        backbuttonfunction='xbmc.executebuiltin("Skin.SetString(Branding,off)");self.close()',
        nextbuttonfunction='Check_Status()',
        selectbutton=ADDON.getLocalizedString(30072),
        toggleup='',
        toggledown='',
        selectbuttonfunction="Registration_Details()",
        toggleupfunction='',
        toggledownfunction='',
        maintext=ADDON.getLocalizedString(30073),
        noconnectionbutton=ADDON.getLocalizedString(30019),
        noconnectionfunction="xbmc.executebuiltin('ActivateWindow(home)');xbmc.executebuiltin('RunAddon(service.openelec.settings)');xbmc.executebuiltin('RunAddon(script.openwindow)')"
        )
    mydisplay .doModal()
    del mydisplay

    
def Update_Screen():
    mydisplay = Image_Screen(
        header='Update In Progress',
        background='register.png',
        icon='update_software.png',
        maintext=ADDON.getLocalizedString(30074),
        )
    mydisplay .doModal()
    del mydisplay


def Registration_Details():
    print"Registration_Details"
    Text_Boxes(ADDON.getLocalizedString(30079),ADDON.getLocalizedString(30080))


def Download_Function(url):
    try:
        urllib.urlretrieve(url,lib)
        print"###Download Started"
    except:
        dialog.ok('Error','Unable to download updates from server. Please try opening a web browser on your PC to make sure your internet is working correctly. Click OK to try again.')
        if os.path.exists(addondata):
            shutil.rmtree(addondata)
        xbmc.executebuiltin('reboot')
    
    
def Download_Extract(url,video):
    global download_thread
    global endtime
    if not os.path.exists(RunWizard):
        os.makedirs(RunWizard)
    download_thread = threading.Thread(target=Download_Function, args=[url])
    updatescreen_thread = threading.Thread(target=Update_Screen)
    download_thread.start()
    starttime = datetime.datetime.now()
    try:
        yt.PlayVideo(video)
    except:
        pass
    while xbmc.Player().isPlaying():
        xbmc.sleep(500)
    updatescreen_thread.start()
    while download_thread.isAlive():
        xbmc.sleep(500)
    endtime   = datetime.datetime.fromtimestamp(os.path.getmtime(lib))
    timediff  = endtime-starttime
    libsize   = os.path.getsize(lib) / (128*1024.0)
    timediff = str(timediff).replace(':','')
    speed = libsize / float(timediff)
    writefile = open(timepath, mode='w+')
    writefile.write(str(speed))
    writefile.close()

    if os.path.exists(lib) and zipfile.is_zipfile(lib):
        zin = zipfile.ZipFile(lib, 'r')
        zin.extractall(rootfolder)
        try:
            os.remove(lib)
        except:
            print"### Failed to remove temp file"
        Remove_Textures()
        print"### Removed textures"
        KILL_KODI()


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


def Check_Status():
    print"Check_Status"
# Function to check activation status of the unit
    url   = ''
    video = ''
    status = Activate()
    if '~' in status:
        url,video = status.split('~')
        url = encryptme('d',url)
        video = encryptme('d',video)
    else:
        try:
            url = encryptme('d',status)
        except:
            url = "fail"
# If activation sends back vanilla
    print"### URL="+url
    try:
        print"### Video="+video
    except:
        print"### No Video"
    if  url==encryptme('d','595d515c110b0d1804'):
        mode = 'quit'

# If activation sends back registration
    if '~' in status and not os.path.exists(xbmc.translatePath(os.path.join(HOME,'media','branding'))) and (encryptme('d','5b6767632d2222675f555521605804060d1006') in url or 'venztech.com' in url):
        if 'http' in video:
            try:
                urllib.urlretrieve(video,lib)
            except:
                print"### Unable to download branding"
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


def Build_Info():
    Build = ''
    if os.path.exists('/etc/release'):
        readfile = open('/etc/release','r')
        Build    = readfile.read()
        readfile.close()
    if Build == '':
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
    
def Activate():
    link    = ''
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
    if testdebug == 'true':
        print "### params: "+urlparams
    xbmc.executebuiltin("ActivateWindow(busydialog)")
    while counter <3 and success == 0:
#        try:
            counter += 1
            try:
                link = Open_URL('http://tlbb.me/Add.php?'+encryptme('e',urlparams))
            except:
                try:
                    link = Open_URL('http://venztech.com/admin/Add.php?'+encryptme('e',urlparams))
                except:
                    try:
                        link = Open_URL('http://thelittleblackbox.com/admin/Add.php?'+encryptme('e',urlparams))
                    except:
                        pass
            if '~' in link:
                dl,vid = link.split('~')
                print"### link: "+encryptme('d',dl)
            elif link != '':
                dl = link
                print"### link: "+encryptme('d',dl)
            if not '<body' in link and link != '':
                if 'http' in encryptme('d',dl):
                    success = 1
            else:
                print"### Failed to get response from servers, attempt number "+str(counter)
 #       except:
  #          dialog.ok(ADDON.getLocalizedString(30075),ADDON.getLocalizedString(30076))
    try:
        xbmc.executebuiltin("Dialog.Close(busydialog)")
    except:
        pass
    if success == 1:
        return link
    else:
        choice = dialog.yesno(ADDON.getLocalizedString(30075),ADDON.getLocalizedString(30077))
        if choice == 1:
            dialog.ok(ADDON.getLocalizedString(30075),ADDON.getLocalizedString(30078))
            try:
                shutil.rmtree(addondata)
            except:
                xbmc.executebuiltin('Skin.SetString(Branding,off)')
            return '595d515c110b0d1804'
        else:
            return 'back'

def Open_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 10.0; WOW64; Windows NT 5.1; en-GB; rv:1.9.0.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36 Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req, timeout = 10)
    link     = response.read()
    response.close()
    return link.replace('\r','').replace('\n','').replace('\t','')

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

###### Main Script Starts Here ######
xmlfile = binascii.unhexlify('6164646f6e2e786d6c')
addonxml = '/usr/share/kodi/addons/script.openwindow/addon.xml'
if not os.path.exists(addonxml):
    addonxml = xbmc.translatePath(os.path.join(ADDONS,ADDONID,xmlfile))
localaddonversion = open(addonxml, mode='r')
content = file.read(localaddonversion)
file.close(localaddonversion)
localaddonvermatch = re.compile('<ref>(.+?)</ref>').findall(content)
addonversion  = localaddonvermatch[0] if (len(localaddonvermatch) > 0) else ''
localcheck = hashlib.md5(open(installfile,'rb').read()).hexdigest()
#if addonversion != localcheck:
#    try:
#       os.remove(installfile)
#    except:
#       pass

mode = None
if mode == None:
    print"### URL@ "+encryptme('d','5e6a6a663025250b1c0a0506')
#    if os.path.exists(lib):
#        os.remove(lib)
    Check_Status()

elif mode =='quit':
    xbmc.executebuiltin('Skin.SetString(Branding,off)')
    xbmc.executebuiltin('StopScript(script.openwindow)')
    xbmc.executebuiltin('ActivateWindow(home)')