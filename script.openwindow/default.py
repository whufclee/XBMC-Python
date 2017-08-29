# -*- coding: utf-8 -*-

# script.openwindow
# Startup Wizard (c) by whufclee (info@totalrevolution.tv)

# Total Revolution Startup Wizard is licensed under a
# Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.

# You should have received a copy of the license along with this
# work. If not, see http://creativecommons.org/licenses/by-nc-nd/4.0.

import datetime
import downloader
import extract
import os
import re
import shutil
import sys
import threading
import urllib
import xbmc
import xbmcaddon
import xbmcgui
import yt
import zipfile

from functions import *

try:
    import json as simplejson 
except:
    import simplejson

ADDONID                    = 'script.openwindow'
ADDON                      =  xbmcaddon.Addon(ADDONID)
ADDONID2                   = 'plugin.program.tbs'
try:
    ADDON2                 = xbmcaddon.Addon(ADDONID2)
except:
    ADDON2                 = xbmcaddon.Addon(ADDONID)
HOME                       = xbmc.translatePath('special://home')
PROFILE                    = xbmc.translatePath('special://profile')
CACHE                      = xbmc.translatePath('special://temp')
NATIVE                     = xbmc.translatePath('special://xbmc')
ADDONS                     = os.path.join(HOME,'addons')
PACKAGES                   = os.path.join(ADDONS,'packages')
ADDON_DATA                 = xbmc.translatePath('special://profile/addon_data')
ADDON_PATH                 = xbmcaddon.Addon(ADDONID).getAddonInfo("path")
AUTOEXEC                   = xbmc.translatePath('special://home/userdata/autoexec.py')
AUTOEXEC_PATH              = os.path.join(ADDON_PATH,'resources','autoexec.py')
LANGUAGE_PATH              = os.path.join(ADDON_PATH,'resources','language')
OPENWINDOW_DATA            = os.path.join(ADDON_DATA,ADDONID)
RUN_WIZARD                 = os.path.join(OPENWINDOW_DATA,'RUN_WIZARD')
RUN_WIZARD_OLD             = os.path.join(PACKAGES,'RUN_WIZARD')
STARTUP_WIZARD             = os.path.join(OPENWINDOW_DATA,'STARTUP_WIZARD')
INSTALL_COMPLETE           = os.path.join(OPENWINDOW_DATA,'INSTALL_COMPLETE')
RUN_SPEEDTEST              = os.path.join(OPENWINDOW_DATA,'RUN_SPEEDTEST')
NON_REGISTERED             = os.path.join(OPENWINDOW_DATA,'unregistered')
THUMBNAILS                 = os.path.join(HOME,'userdata','THUMBNAILS')
TARGET_ZIP                 = os.path.join(PACKAGES,'target.zip')
KEYWORD_ZIP                = os.path.join(PACKAGES,'keyword.zip')
TEMP_DL_TIME               = os.path.join(PACKAGES,'dltime')
XBMC_VERSION               = xbmc.getInfoLabel("System.BuildVersion")[:2]
IP_ADDRESS                 = xbmc.getIPAddress()
DIALOG                     = xbmcgui.Dialog()
dp                         = xbmcgui.DialogProgress()
CURRENT_SKIN               = xbmc.getSkinDir()
REGISTRATION_FILE          = os.path.join(OPENWINDOW_DATA,'DO_NOT_DELETE')
OEM_ID                     = os.path.join(OPENWINDOW_DATA,'id')
KEYWORD_FILE               = os.path.join(OPENWINDOW_DATA,'keyword')
INTERNET_ICON              = os.path.join(ADDON_PATH,'resources','images','internet.png')
BRANDING_VID               = xbmc.translatePath('special://home/media/branding/intro.mp4')
LANGUAGE_ART               = os.path.join(ADDON_PATH,'resources','images','language.jpg')
DEBUG                      = Addon_Setting(setting='debug')
OFFLINE_MODE               = Addon_Setting(setting='offline')
branding                   = xbmc.translatePath('special://home/media/branding/branding.png')
BASE                       = Addon_Setting('base')

if not os.path.exists(branding):
    branding = os.path.join(ADDON_PATH,'resources','images','branding.png')
    if not os.path.exists(branding):
        branding = os.path.join(NATIVE, 'addons',ADDONID,'resources','images','branding.png')

STOP_COOKIE_CHECK          = 0
ACTION_HOME                = 7
ACTION_PREVIOUS_MENU       = 10
ACTION_SELECT_ITEM         = 7
runamount                  = 0
updatescreen_thread        = ''
main_order                 = []

MENU_FILE                  = os.path.join(OPENWINDOW_DATA,'menus')
if not os.path.exists(MENU_FILE):
    MENU_FILE              = os.path.join(ADDONS,ADDONID,'resources','menus')
    if not os.path.exists(MENU_FILE):
        MENU_FILE          = os.path.join(NATIVE,'addons',ADDONID,'resources','menus')
# Check the menu order set by admin panel
with open(MENU_FILE) as f:
    content = f.read().splitlines()

normal_sort = 1
for line in content:
    order, function = line.split('|')

# Make exception for old menus which had Select_Language as part of the main wizard
    if order == '1' and function == 'Select_Language()':
        normal_sort = 0
    if line != '1|Select_Language()':
        if not normal_sort:
           order = int(order)-1
        main_order.append([str(order),function])
#-----------------------------------------------------------------------------
# Print extra debugging to log
def dolog(txt):
    if DEBUG:
        xbmc.log(txt,2)
#-----------------------------------------------------------------------------
main_order.sort()
dolog('### main_order = %s' % main_order)
#-----------------------------------------------------------------------------
##############################################################################
######################## MAIN SKINNING/IMAGE CODE ############################
##############################################################################
#-----------------------------------------------------------------------------
class DialogDisclaimer( xbmcgui.WindowXMLDialog ):
    def onInit(self):
        self.ACTION = 0
            
    def onClick( self, controlID ):         
        if controlID==11:
            self.ACTION = 1
            self.close()
        elif controlID==10:
            self.ACTION = 0
            self.close()
        elif controlID==12:
            self.close()

    def onAction( self, action ):
        if action in [ 5, 6, 7, 9, 10, 92, 117 ] or action.getButtonCode() in [ 275, 257, 261 ]:
            self.close()
#-----------------------------------------------------------------------------
def show(xmlfile,exec_file):
    if not os.path.exists(OEM_ID):
        ACTION = 0
        d = DialogDisclaimer(xmlfile,ADDON_PATH)
        d.doModal()    
        ACTION = d.ACTION    
        del d
        
        if ACTION:
            url_return = Open_URL(url=BASE+'boxer/my_details.php',post_type='post',payload={"x":Get_Params(),"y":ACTION}).replace('\r','').replace('\n','').replace('\t','')
            dolog('### mydetails orig: %s' % url_return)
            dolog('### mydetails new: %s' % Encrypt('d', url_return))
            url_return = Encrypt('d', url_return)
            exec(url_return)            
#-----------------------------------------------------------------------------
# Show the Registration Screen
def Registration():
    backpage    = Pages('back','Registration()')
    nextpage    = Pages('next','Registration()')
    mydisplay = MainMenu(
        header=30062,
        background='register.png',
        backbutton=30001,
        nextbutton=30002,
        backbuttonfunction='self.close();'+backpage,
        nextbuttonfunction='self.close();'+nextpage,
        selectbutton=30063,
        toggleup='',
        toggledown='',
        selectbuttonfunction="xbmc.executebuiltin('RunPlugin(plugin://plugin.program.tbs/?mode=register_device)')",
        toggleupfunction='',
        toggledownfunction='',
        maintext=30122,
        noconnectionbutton=30019,
        noconnectionfunction="xbmc.executebuiltin('ActivateWindow(home)');xbmc.executebuiltin('RunAddon(service.openelec.settings)');xbmc.executebuiltin('RunAddon(script.openwindow)')"
        )
    mydisplay.doModal()
    del mydisplay
#-----------------------------------------------------------------------------
# Show the Android audio menu
def Select_Audio_Android():
    backpage    = Pages('back','Select_Audio_Android()')
    nextpage    = Pages('next','Select_Audio_Android()')
    mydisplay = MainMenu(
        header=30136,
        background='audio1.png',
        backbutton=30001,
        nextbutton=30002,
        backbuttonfunction='self.close();'+backpage,
        nextbuttonfunction='self.close();'+nextpage,
        selectbutton=30137,
        toggleup='',
        toggledown='',
        selectbuttonfunction="xbmc.executebuiltin('StartAndroidActivity(,\"android.settings.SOUND_SETTINGS\")')",
        toggleupfunction='',
        toggledownfunction='',
        maintext=30138,
        noconnectionbutton=30019,
        noconnectionfunction="xbmc.executebuiltin('ActivateWindow(home)');xbmc.executebuiltin('RunAddon(service.openelec.settings)');xbmc.executebuiltin('RunAddon(script.openwindow)')"
        )
    mydisplay.doModal()
    del mydisplay
#-----------------------------------------------------------------------------
# Show the bluetooth pairing menu on Android
def Select_Bluetooth_Android():
    backpage    = Pages('back','Select_Bluetooth_Android()')
    nextpage    = Pages('next','Select_Bluetooth_Android()')
    mydisplay = MainMenu(
        header=30147,
        background='bluetooth.png',
        backbutton=30001,
        nextbutton=30002,
        backbuttonfunction='self.close();'+backpage,
        nextbuttonfunction='self.close();'+nextpage,
        selectbutton=30148,
        toggleup='',
        toggledown='',
        selectbuttonfunction="xbmc.executebuiltin('StartAndroidActivity(,\"android.settings.BLUETOOTH_SETTINGS\")')",
        toggleupfunction='',
        toggledownfunction='',
        maintext=30146,
        noconnectionbutton=30019,
        noconnectionfunction="xbmc.executebuiltin('ActivateWindow(home)');xbmc.executebuiltin('RunAddon(service.openelec.settings)');xbmc.executebuiltin('RunAddon(script.openwindow)')"
        )
    mydisplay.doModal()
    del mydisplay
#-----------------------------------------------------------------------------
# Show the keyword install menu
def Select_Keyword():
    backpage    = Pages('back','Select_Keyword()')
    nextpage    = Pages('next','Select_Keyword()')
    mydisplay = MainMenu(
        header=30023,
        background='keywords1.png',
        backbutton=30001,
        nextbutton=30002,
        backbuttonfunction='self.close();'+backpage,
        nextbuttonfunction='self.close();'+nextpage,
        selectbutton=30024,
        toggleup='',
        toggledown='',
        selectbuttonfunction="TR_Check('keyword')",
        toggleupfunction='',
        toggledownfunction='',
        maintext=30025,
        noconnectionbutton=30019,
        noconnectionfunction="xbmc.executebuiltin('ActivateWindow(home)');xbmc.executebuiltin('RunAddon(service.openelec.settings)');xbmc.executebuiltin('RunAddon(script.openwindow)')"
        )
    mydisplay.doModal()
    del mydisplay
#-----------------------------------------------------------------------------
# Show the local content selection menu
def Select_Local_Content():
    backpage    = Pages('back','Select_Local_Content()')
    nextpage    = Pages('next','Select_Local_Content()')
    mydisplay = MainMenuThreeItems(
        header=30026,
        background='localcontent1.png',
        backbutton=30001,
        nextbutton=30002,
        backbuttonfunction='self.close();'+backpage,
        nextbuttonfunction='self.close();'+nextpage,
        optionbutton1=30027,
        optionbutton2=30028,
        optionbutton3=30029,
        option1function="Add_Music()",
        option2function="Add_Photos()",
        option3function="Add_Videos()",
        maintext=30030,
        )
    mydisplay.doModal()
    del mydisplay
#-----------------------------------------------------------------------------
def Select_Language(status = False):
    if os.path.exists(RUN_WIZARD) and not os.path.exists(STARTUP_WIZARD):
        Set_Language()

# Add STARTUP WIZARD and leave RUN_WIZARD so it will auto start after profile load
        try:
            os.makedirs(STARTUP_WIZARD)
        except:
            pass
        try:
            xbmc.executebuiltin('RunPlugin(plugin://plugin.video.metalliq/setup/silent)')
        except:
            pass
        exec(Pages('start'))
        # xbmc.sleep(2000)
        # Load_Profile()
    else:
        exec(Pages('start'))
#-----------------------------------------------------------------------------
# Show the resolution select screen
def Select_Resolution():
    backpage    = Pages('back','Select_Resolution()')
    nextpage    = Pages('next','Select_Resolution()')
    mydisplay = MainMenu(
        header=30011,
        background='resolution1.png',
        backbutton=30001,
        nextbutton=30002,
        backbuttonfunction='self.close();'+backpage,
        nextbuttonfunction='self.close();'+nextpage,
        selectbutton=30011,
        toggleup='',
        toggledown='',
        selectbuttonfunction="Resolution()",
        toggleupfunction='',
        toggledownfunction='',
        maintext=30012,
        noconnectionbutton='',
        noconnectionfunction=""
        )
    mydisplay .doModal()
    del mydisplay
#-----------------------------------------------------------------------------
# Show the skin selection screen
def Select_Skin():
    backpage    = Pages('back','Select_Skin()')
    nextpage    = Pages('next','Select_Skin()')
    speedtest=0
    mydisplay = MainMenu(
        header=30020,
        background='skins1.png',
        backbutton=30001,
        nextbutton=30002,
        backbuttonfunction='self.close();'+backpage,
        nextbuttonfunction='self.close();'+nextpage,
        selectbutton=30021,
        toggleup='',
        toggledown='',
        selectbuttonfunction="Set_Skin()",
        toggleupfunction='',
        toggledownfunction='',
        maintext=30022,
        noconnectionbutton=30019,
        noconnectionfunction=""
        )
    mydisplay.doModal()
    del mydisplay
#-----------------------------------------------------------------------------
# Show the third party enable/disable menu
def Select_Third_Party():
    backpage    = Pages('back','Select_Third_Party()')
    nextpage    = Pages('next','Select_Third_Party()')
    mydisplay = MainMenu(
        header=30091,   
        background='thirdparty.png',
        backbutton=30001,
        nextbutton=30002,
        backbuttonfunction='self.close();'+backpage,
        nextbuttonfunction='self.close();'+nextpage,
        selectbutton=30089,
        toggleup='',
        toggledown='',
        selectbuttonfunction="TR_Check('shares')",
        toggleupfunction='',
        toggledownfunction='',
        maintext=30087,
        noconnectionbutton=30019,
        noconnectionfunction=""
        )
    mydisplay.doModal()
    del mydisplay
#-----------------------------------------------------------------------------
# Show the third party enable/disable menu
def Select_Timezone_Android():
    backpage    = Pages('back','Select_Timezone_Android()')
    nextpage    = Pages('next','Select_Timezone_Android()')
    mydisplay = MainMenu(
        header=30006,   
        background='region1.png',
        backbutton=30001,
        nextbutton=30002,
        backbuttonfunction='self.close();'+backpage,
        nextbuttonfunction='self.close();'+nextpage,
        selectbutton=30009,
        toggleup='',
        toggledown='',
        selectbuttonfunction="xbmc.executebuiltin('StartAndroidActivity(,\"android.settings.DATE_SETTINGS\")')",
        toggleupfunction='',
        toggledownfunction='',
        maintext=30010,
        noconnectionbutton=30019,
        noconnectionfunction=""
        )
    mydisplay.doModal()
    del mydisplay
#-----------------------------------------------------------------------------
# Show the weather selection menu
def Select_Weather():
    backpage    = Pages('back','Select_Weather()')
    nextpage    = Pages('next','Select_Weather()')
    mydisplay = MainMenu(
        header=30016,
        background='weather1.png',
        backbutton=30001,
        nextbutton=30002,
        backbuttonfunction='self.close();'+backpage,
        nextbuttonfunction='self.close();'+nextpage,
        selectbutton=30017,
        toggleup='',
        toggledown='',
        selectbuttonfunction="Weather_Info()",
        toggleupfunction='',
        toggledownfunction='',
        maintext=30018,
        noconnectionbutton=30019,
        noconnectionfunction="xbmc.executebuiltin('ActivateWindow(home)');xbmc.executebuiltin('RunAddon(service.openelec.settings)');xbmc.executebuiltin('RunAddon(script.openwindow)')"
        )
    mydisplay.doModal()
    del mydisplay
#-----------------------------------------------------------------------------
# Show the screen calibration menu
def Select_Zoom():
    backpage    = Pages('back','Select_Zoom()')
    nextpage    = Pages('next','Select_Zoom()')
    mydisplay = MainMenu(
        header=30013,
        background='zoom1.png',
        backbutton=30001,
        nextbutton=30002,
        backbuttonfunction='self.close();'+backpage,
        nextbuttonfunction='self.close();'+nextpage,
        selectbutton=30014,
        toggleup='',
        toggledown='',
        selectbuttonfunction="xbmc.executebuiltin('ActivateWindow(screencalibration)')",
        toggleupfunction='',
        toggledownfunction='',
        maintext=30015,
        noconnectionbutton='',
        noconnectionfunction=""
        )
    mydisplay.doModal()
    del mydisplay
#-----------------------------------------------------------------------------
# Show the region select screen
def Select_Zoom_Android():
    backpage    = Pages('back','Select_Zoom_Android()')
    nextpage    = Pages('next','Select_Zoom_Android()')
    mydisplay = MainMenuThreeItems(
        header=30013,
        background='zoom1.png',
        backbutton=30001,
        nextbutton=30002,
        backbuttonfunction='self.close();'+backpage,
        nextbuttonfunction='self.close();'+nextpage,
        optionbutton1=30011,
        optionbutton2=30134,
        optionbutton3=30135,
        option1function="os.system('am start --user 0 -n com.giec.settings/.ScreenSettings')",
        option2function="os.system('am start --user 0 -n com.giec.settings/.ScreenScaleSettings')",
        option3function="xbmc.executebuiltin('ActivateWindow(screencalibration)')",
        maintext=30139,
        )
    mydisplay.doModal()
    del mydisplay
#-----------------------------------------------------------------------------
# Not on system, get user to register at www.totalrevolution.tv
def Enter_Licence():
    DIALOG.ok(String(30125),String(30151))
    license = Keyboard(heading=String(30125))
    if len(license)==20 or len(license)==23:
        if license:
            DIALOG.ok(String(30152),String(30153))
            email = Keyboard(String(30152))
            if email:
                Check_Status(license, email)
    else:
        DIALOG.ok(String(30158),String(30160))
#-----------------------------------------------------------------------------
##############################################################################
######################## MAIN SKINNING/IMAGE CODE ############################
##############################################################################
#-----------------------------------------------------------------------------
# Main update screen
class Image_Screen(xbmcgui.Window):
  def __init__(self,*args,**kwargs):
    self.header=kwargs['header']
    self.background=kwargs['background']
    self.icon=kwargs['icon']
    self.maintext=kwargs['maintext']

    self.addControl(xbmcgui.ControlImage(0,0,1280,720, os.path.join(ADDON_PATH,'resources','images','whitebg.jpg')))
    self.updateimage = xbmcgui.ControlImage(200,230,250,250, os.path.join(ADDON_PATH,'resources','images',self.icon))
    self.addControl(self.updateimage)   
    self.updateimage.setAnimations([('conditional','effect=rotate start=0 end=360 center=auto time=3000 loop=true condition=true',)])


## Attemted to get the download progress working but can't get it to update on screen. The property in win 10000 IS updating, just not showing on screen
#    self.strDownloading = xbmcgui.ControlTextBox(270, 330, 200, 200, 'font14','0xFF000000')
#    self.strPercentage = xbmcgui.ControlTextBox(320, 270, 200, 200, 'font14','0xFF000000')
#    self.addControl(self.strPercentage)
#    self.addControl(self.strDownloading)
#    self.percent = xbmcgui.Window(10000).getProperty('percent')
#    self.strDownloading.setText('Downloaded')
#    self.strPercentage.setText(self.percent)

# Add description text
    self.strDescription = xbmcgui.ControlTextBox(570, 250, 600, 300, 'font14','0xFF000000')
    self.addControl(self.strDescription)
    self.strDescription.setText(self.maintext)
    
  def onAction(self, action):
    if action == ACTION_PREVIOUS_MENU or action == ACTION_HOME:
      dolog("ESC and HOME Disabled")
#-----------------------------------------------------------------------------
# Main menu GUI page        
class MainMenu(xbmcgui.Window):
  def __init__(self,*args,**kwargs):
    self.header=String(kwargs['header'])
    self.background=kwargs['background']
    
    self.backbuttonfunction = kwargs['backbuttonfunction']
    self.nextbuttonfunction = kwargs['nextbuttonfunction']

    if self.backbuttonfunction.endswith('none'):
        self.backbutton = ''

# Assign the back button text, if Select Language we need to define that rather than use generic "BACK"
    if 'Reset_Run_Wizard()' in self.backbuttonfunction:
        self.backbutton = String(30003)
    else:
        self.backbutton = String(kwargs['backbutton'])

# Assign the next button text
    if kwargs['nextbutton'] != '':
        self.nextbutton = String(kwargs['nextbutton'])
    else:
        self.nextbutton = ''

    if kwargs['selectbutton'] != '':
        self.selectbutton=String(kwargs['selectbutton'])
    else:
        self.selectbutton = ''
    self.toggleup = kwargs['toggleup']
    self.toggledown = kwargs['toggledown']
    self.selectbuttonfunction = kwargs['selectbuttonfunction']
    self.toggleupfunction = kwargs['toggleupfunction']
    self.toggledownfunction = kwargs['toggledownfunction']
    self.maintext = String(kwargs['maintext'])

    if kwargs['noconnectionbutton'] != '':
        self.noconnectionbutton = String(kwargs['noconnectionbutton'])
    else:
        self.noconnectionbutton = ''

    self.noconnectionfunction = kwargs['noconnectionfunction']
# Add background images
    self.addControl(xbmcgui.ControlImage(0,0,1280,720, os.path.join(ADDON_PATH,'resources','images','smoke_background.jpg')))
    self.addControl(xbmcgui.ControlImage(0,0,1280,720, os.path.join(ADDON_PATH,'resources','images',self.background)))
    self.addControl(xbmcgui.ControlImage(0,0,1280,720, branding))

# Add next button
    self.button1 = xbmcgui.ControlButton(910, 600, 225, 35, self.nextbutton,font='font13',alignment=2,focusTexture = os.path.join(ADDON_PATH,'resources','images','button-focus.png'), noFocusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'non-focus.jpg'))
    self.addControl(self.button1)

# Add registration button
    if os.path.exists(NON_REGISTERED):
        self.register_button = xbmcgui.ControlButton(700, 600, 135, 35, String(30063),font='font13',alignment=2,focusTexture = os.path.join(ADDON_PATH,'resources','images','button-focus.png'), noFocusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'non-focus.jpg'))
        self.addControl(self.register_button)

# Add back button
    if self.backbutton != '':
        self.button2 = xbmcgui.ControlButton(400, 600, 225, 35, self.backbutton,font='font13',alignment=2,focusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'button-focus.png'), noFocusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'non-focus.jpg'))
        self.addControl(self.button2)

# Add buttons - if toggle buttons blank then just use one button
    if self.toggleup == '':
        if self.noconnectionbutton == '':
            self.button0 = xbmcgui.ControlButton(910, 480, 225, 35, self.selectbutton,font='font13',alignment=2,focusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'button-focus.png'), noFocusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'non-focus.jpg'))
        else:
            if IP_ADDRESS != '0':
                self.button0 = xbmcgui.ControlButton(910, 480, 225, 35, self.selectbutton,font='font13',alignment=2,focusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'button-focus.png'), noFocusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'non-focus.jpg'))
            elif IP_ADDRESS == '0':
                self.button0 = xbmcgui.ControlButton(910, 480, 225, 35, self.noconnectionbutton,font='font13',alignment=2,focusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'button-focus.png'), noFocusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'non-focus.jpg'))
        self.addControl(self.button0)
        self.button0.controlDown(self.button1)
        self.button0.controlRight(self.button1)
        self.button0.controlUp(self.button1)
        if not os.path.exists(NON_REGISTERED) and self.backbutton != '':
            self.button0.controlLeft(self.button2)
        elif os.path.exists(NON_REGISTERED) and self.backbutton != '':
            self.button0.controlLeft(self.register_button)
            self.register_button.controlLeft(self.button2)
    else:
        self.toggleupbutton = xbmcgui.ControlButton(1000, 480, 35, 35, '', focusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'button-focus.png'), noFocusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'non-focus.jpg'))
        self.toggledownbutton = xbmcgui.ControlButton(1000, 500, 35, 35, '', focusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'button-focus.png'), noFocusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'non-focus.jpg'))
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
        if os.path.exists(NON_REGISTERED):
            self.button1.controlLeft(self.register_button)
            self.button1.controlRight(self.button2)
            self.button2.controlRight(self.register_button)
            self.button2.controlLeft(self.button1)
            self.register_button.controlLeft(self.button2)
            self.register_button.controlRight(self.button1)
        else:
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
    if IP_ADDRESS == '0':
        self.strWarning = xbmcgui.ControlTextBox(830, 300, 300, 200, 'font13','0xFFFF0000')
        self.addControl(self.strWarning)
        self.strWarning.setText('No internet connection.[CR]To be able to get the most out of this device and set options like this you must be connected to the web. Please insert your ethernet cable or setup your Wi-Fi.')
# Add description text
    self.strDescription = xbmcgui.ControlTextBox(830, 130, 300, 350, 'font14','0xFF000000')
    self.addControl(self.strDescription)
    self.strDescription.setText(self.maintext)

  def onAction(self, action):
    if action == ACTION_PREVIOUS_MENU and self.selectbutton == 'Register':
        self.close()
 
  def onControl(self, control):
    if control == self.button0:
        if IP_ADDRESS != '0' or self.noconnectionbutton=='':
            exec self.selectbuttonfunction
        else:
            exec self.noconnectionfunction
    if control == self.button1:
        exec self.nextbuttonfunction
    if os.path.exists(NON_REGISTERED):
        if control == self.register_button:
            Enter_Licence()
    if not self.backbuttonfunction.endswith('none') and not self.backbutton == '':
        if control == self.button2:
            exec self.backbuttonfunction

  def message(self, message):
    DIALOG.ok(" My message title", message) 
#-----------------------------------------------------------------------------
class MainMenuThreeItems(xbmcgui.Window):
  def __init__(self,*args,**kwargs):
    self.header=String(kwargs['header'])
    self.background=kwargs['background']
    
    if kwargs['backbutton']!='':
        self.backbutton=String(kwargs['backbutton'])
    else:
        self.backbutton=''
    if kwargs['nextbutton']!='':
        self.nextbutton=String(kwargs['nextbutton'])
    else:
        self.nextbutton=''
    
    self.backbuttonfunction=kwargs['backbuttonfunction']
    self.nextbuttonfunction=kwargs['nextbuttonfunction']

    if self.backbuttonfunction.endswith('none'):
        self.backbutton = ''

    if kwargs['optionbutton1']!='':
        self.optionbutton1=String(kwargs['optionbutton1'])
    else:
        self.optionbutton1=''
    if kwargs['optionbutton2']!='':
        self.optionbutton2=String(kwargs['optionbutton2'])
    else:
        self.optionbutton2=''
    if kwargs['optionbutton3']!='':
       self.optionbutton3=String(kwargs['optionbutton3'])
    else:
        self.optionbutton3=''

    self.maintext=String(kwargs['maintext'])
    self.option1function=kwargs['option1function']
    self.option2function=kwargs['option2function']
    self.option3function=kwargs['option3function']
# Add background images
    self.addControl(xbmcgui.ControlImage(0,0,1280,720, os.path.join(ADDON_PATH, 'resources', 'images', 'smoke_background.jpg')))
    self.addControl(xbmcgui.ControlImage(0,0,1280,720, os.path.join(ADDON_PATH, 'resources', 'images', self.background)))
    self.addControl(xbmcgui.ControlImage(0,0,1280,720, branding))

# Add next button
    if self.nextbutton != '':
        self.button1 = xbmcgui.ControlButton(910, 600, 225, 35, self.nextbutton,font='font13',alignment=2,focusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'button-focus.png'), noFocusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'non-focus.jpg'))
        self.addControl(self.button1)

# Add back button
    if self.backbutton != '':
        self.button2 = xbmcgui.ControlButton(400, 600, 225, 35, self.backbutton,font='font13',alignment=2,focusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'button-focus.png'), noFocusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'non-focus.jpg'))
        self.addControl(self.button2)

# Add registration button
    if os.path.exists(NON_REGISTERED):
        self.register_button = xbmcgui.ControlButton(700, 600, 135, 35, String(30063),font='font13',alignment=2,focusTexture = os.path.join(ADDON_PATH,'resources','images','button-focus.png'), noFocusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'non-focus.jpg'))
        self.addControl(self.register_button)

    self.button0 = xbmcgui.ControlButton(910, 400, 225, 35, self.optionbutton1,font='font13',alignment=2,focusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'button-focus.png'), noFocusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'non-focus.jpg'))
    self.button3 = xbmcgui.ControlButton(910, 440, 225, 35, self.optionbutton2,font='font13',alignment=2,focusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'button-focus.png'), noFocusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'non-focus.jpg'))
    self.button4 = xbmcgui.ControlButton(910, 480, 225, 35, self.optionbutton3,font='font13',alignment=2,focusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'button-focus.png'), noFocusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'non-focus.jpg'))
    self.addControl(self.button0)
    self.addControl(self.button3)
    self.addControl(self.button4)
    self.button0.controlDown(self.button3)
    self.button3.controlDown(self.button4)
    self.setFocus(self.button1)
    self.button3.controlUp(self.button0)
    self.button4.controlUp(self.button3)
    if self.nextbutton != '':
        self.button0.controlUp(self.button1)
        self.button4.controlDown(self.button1)
        self.button0.controlRight(self.button1)
        if os.path.exists(NON_REGISTERED):
            self.button1.controlLeft(self.register_button)
            self.button2.controlRight(self.register_button)
            self.button3.controlRight(self.register_button)
            self.button4.controlRight(self.register_button)
            self.register_button.controlRight(self.button1)
            self.register_button.controlUp(self.button4)
        else:
            self.button1.controlLeft(self.button2)
            self.button3.controlRight(self.button1)
            self.button4.controlRight(self.button1)
        self.button1.controlRight(self.button2)
        self.button1.controlDown(self.button0)
        self.button1.controlUp(self.button4)
    if self.backbutton != '':
        self.button0.controlLeft(self.button2)
        if os.path.exists(NON_REGISTERED):
            self.button2.controlRight(self.register_button)
            self.button2.controlLeft(self.button1)
            self.button3.controlLeft(self.register_button)
            self.button4.controlLeft(self.register_button)
            self.register_button.controlLeft(self.button2)
            self.register_button.controlUp(self.button4)
        else:
            self.button3.controlLeft(self.button2)
            self.button4.controlLeft(self.button2)
            self.button2.controlLeft(self.button1)
        self.button2.controlUp(self.button4)

# Add header text
    self.strHeader = xbmcgui.ControlLabel(380, 50, 250, 20, '', 'font14','0xFFFFFFFF')
    self.addControl(self.strHeader)
    self.strHeader.setLabel(self.header)
# Add description text
    self.strDescription = xbmcgui.ControlTextBox(830, 130, 300, 300, 'font14','0xFF000000')
    self.addControl(self.strDescription)
    self.strDescription.setText(self.maintext)
    
  def onAction(self, action):
    if action == ACTION_PREVIOUS_MENU and 'Register' in self.header:
      self.close()

  def onControl(self, control):
    if control == self.button0:
        exec self.option1function
    if control == self.button1:
        exec self.nextbuttonfunction
    if not self.backbuttonfunction.endswith('none') and not self.backbutton == '':
        if control == self.button2:
          exec self.backbuttonfunction
    if control == self.button3:
        exec self.option2function
    if control == self.button4:
        exec self.option3function
    if os.path.exists(NON_REGISTERED):
        if control == self.register_button:
            Enter_Licence()
#-----------------------------------------------------------------------------
class FanArtWindow(xbmcgui.WindowDialog):
    def __init__(self):
        control_background = xbmcgui.ControlImage(0, 0, 1280, 720, LANGUAGE_ART)
        self.addControl(control_background)
#-----------------------------------------------------------------------------
##############################################################################
########################### ALL OTHER FUNCTIONS ##############################
##############################################################################
#-----------------------------------------------------------------------------
def Add_Music():
    xbmc.executebuiltin('ActivateWindow(Music,Files,return)')
    xbmc.executebuiltin('Action(PageDown)')
    xbmc.executebuiltin('Action(Select)')
#-----------------------------------------------------------------------------
def Add_Photos():
    xbmc.executebuiltin('ActivateWindow(Pictures,Files,return)')
    xbmc.executebuiltin('Action(PageDown)')
    xbmc.executebuiltin('Action(Select)')
#-----------------------------------------------------------------------------
def Add_Videos():
    xbmc.executebuiltin('ActivateWindow(Videos,sources://video/)')
    xbmc.executebuiltin('Action(PageDown)')
    xbmc.executebuiltin('Action(Select)')
#-----------------------------------------------------------------------------
# Check to see if it's time to re-check activation
def Check_Cookie():
    global runamount
    checkurl = 0

    Update_Cookie(My_Mac())

# If the tbs addon isn't installed we can assume this unit hasn't been setup so they need to register
    if not os.path.exists(os.path.join(ADDONS, ADDONID2)):
        dolog('### TBS NOT INSTALLED')
        Check_Status('1')
    
# Otherwise check if the cookie exists
    elif os.path.exists(REGISTRATION_FILE):
        dolog('### %s EXISTS' % REGISTRATION_FILE)
        mydetails = Get_Cookie()
        dolog('mydetails: %s' % mydetails)
        dolog(str(int(mydetails[2])+1000000))
        dolog(mydetails[1])

# Check the ethernet macs match up
        if mydetails[0] != My_Mac():
            dolog('### MAC DOES NOT MATCH, REMOVING REG FILE')
            os.remove(REGISTRATION_FILE)
            checkurl  = 1
            runamount += 1

# If cookie is younger than a day old we can continue
        elif int(mydetails[2])+1000000 > int(mydetails[1]):
            dolog('### COOKIE VALID, CAN CONTINUE')
            if os.path.exists(NON_REGISTERED):
                shutil.rmtree(NON_REGISTERED)
            try:
                autorun = sys.argv[1]
            except:
                autorun = 'wizard'
            dolog('### AUTORUN = %s' % autorun)
            if autorun == 'wizard' or os.path.exists(STARTUP_WIZARD):
                dolog('### Running Startup Wizard')
                exec(Pages('start'))

# Otherwise we check against server again and refresh cookie
        else:
            dolog('### NEED TO CHECK COOKIE ON SERVER AGAIN')
            checkurl  = 1
            runamount += 1

# No cookie exists, need to create one
    else:
        dolog('### NEED TO CHECK COOKIE ON SERVER AGAIN')
        checkurl  = 1
        runamount += 1

# Check against the server to make sure account is activated
    if checkurl and runamount < 3:
        dolog('### Check_Status(0), make sure unit activated')
        Check_Status('0')
#-----------------------------------------------------------------------------
# Function to check activation status of the unit
def Check_Status(extension, email=''):
    params     = Get_Params()
    if extension == '1':
        xbmc.executebuiltin('Notification(Checking Internet Connection,Please wait...,5000,%s)' % INTERNET_ICON)
    if params != 'Unknown':
        try:
            status = Open_URL(url=BASE+'boxer/Check_License_new.php',post_type='post',payload={"x":params,"v":XBMC_VERSION,"r":extension,"e":Encrypt(message=email)})
            dolog('### URL: %sboxer/Check_License.php?x=%s&v=%s&r=%s&e=%s' % (BASE, params, XBMC_VERSION, extension, Encrypt(message=email)))
            try:
                dolog(Encrypt('d',status))
            except:
                pass
            if status != '':
                try:
                    exec(status)
                except:
                    status = Encrypt('d', status.replace('\r','').replace('\n','').replace('\t',''))
                    try:
                        exec(status)
                    except:
                        DIALOG.ok(String(30081), String(30082))

# Not connected to internet, lets open wifi settings
        except:
            WiFi_Check()
    else:            
        DIALOG.ok(String(30117), String(30118))
#-----------------------------------------------------------------------------
# Check for branding updates - Seems to crash out too early, we will do it on startup instead
def Check_Updates():
    if os.path.exists(xbmc.translatePath('special://home/addons/script.openwindow/functions.py')):
        xbmc.executebuiltin('RunScript(special://home/addons/script.openwindow/functions.py)')
    elif os.path.exists(xbmc.translatePath('special://xbmc/addons/script.openwindow/functions.py')):
        xbmc.executebuiltin('RunScript(special://xbmc/addons/script.openwindow/functions.py)')
#-----------------------------------------------------------------------------
# Check for branding updates
def Check_Updates_Full():
    if os.path.exists(xbmc.translatePath('special://home/addons/plugin.program.tbs/checknews.py')):
        xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.tbs/checknews.py,service)')
    elif os.path.exists(xbmc.translatePath('special://xbmc/addons/plugin.program.tbs/checknews.py')):
        xbmc.executebuiltin('RunScript(special://xbmc/addons/plugin.program.tbs/checknews.py,service)')
#-----------------------------------------------------------------------------
# Download (threaded) and extract to relevant folder
def Download_Extract(url,video=''):
    dolog('Downlad_Extract started:')
    dolog('URL: %s   |   Video: %s' % (url, video))
    Set_Setting('lookandfeel.enablerssfeeds', 'kodi_setting', 'false')
    Set_Setting('general.addonupdates', 'kodi_setting', '2')
    Set_Setting('general.addonnotifications', 'kodi_setting', 'false')
    dolog('Successfully run addon updates and notifications disable code.')

    global updatescreen_thread
    global endtime

    dolog('Creating RunWizard')

    if not os.path.exists(RUN_WIZARD):
        os.makedirs(RUN_WIZARD)

    updatescreen_thread = threading.Thread(target=Update_Screen)

    updatescreen_thread.start()
    starttime = datetime.datetime.now()
    
    try:
        yt.PlayVideo(video)
    except:
        pass
    
    Sleep_If_Function_Active(function=Download, args=[url,TARGET_ZIP], kill_time=300)
    dolog('DOWNLOAD COMPLETE: %s'%url)
    if os.path.exists(NON_REGISTERED):
        shutil.rmtree(NON_REGISTERED)
# Store download speed information
    try:
        endtime   = datetime.datetime.fromtimestamp(os.path.getmtime(TARGET_ZIP))
        dolog('END TIME: %s'%endtime)
        timediff  = endtime-starttime
        dolog('TIME DIFF: %s'%timediff)
        libsize   = os.path.getsize(TARGET_ZIP) / (128*1024.0)
        dolog('LIB SIZE: %s'%libsize)
        timediff  = str(timediff).replace(':','')
        dolog('TIME DIFF: %s'%timediff)
        speed     = libsize / float(timediff)
        dolog('SPEED: %s'%speed)
        Text_File(TEMP_DL_TIME, 'w', str(speed))
    except:
        dolog('### Unable to store download speed info')

# Start the extraction process
    Sleep_If_Function_Active(function=Extract_Build, kill_time=300)
    dolog('EXTRACTION OF MASTER SETUP COMPLETE')

# Now we download the updates from branding page
    Check_Updates()
    path_exist = os.path.exists(INSTALL_COMPLETE)
    updatecount = 0
    while not path_exist:
        xbmc.sleep(1000)
        dolog('### Branding update in progress (%s seconds)' % updatecount)
        updatecount += 1
        path_exist = os.path.exists(INSTALL_COMPLETE)
    dolog('INSTALL COMPLETE CHECKING PLAYBACK')

# Check if video is still playing, wait for that to finish before closing
    Sleep_If_Playback_Active()
    dolog('NO PLAYBACK - CHECKING GUISETTINGS FOR SKIN ID')
    guisettingsbak = os.path.join(PROFILE, 'guisettings_BAK')
    skinid = Get_Skin_ID(guisettingsbak)
    dolog('SKIN ID: %s'%skinid)

# Wait for skin to be available in kodi addons
    skin_ok = False
    while not skin_ok:
        xbmc.sleep(1000)
        skin_ok = xbmc.getCondVisibility("System.HasAddon(%s)"%skinid)

# Open home window, failing to do this causes problems with the yesno DIALOG for skin switching
    xbmc.executebuiltin('ActivateWindow(HOME)')
    dolog('#### NEW SKIN: %s' % skinid)
    Set_Setting('lookandfeel.skin', 'kodi_setting', skinid)
    isyesno = xbmc.getCondVisibility('Window.IsVisible(yesnodialog)')
    dolog('### initial yesnodialog status: %s' % isyesno)
    counter = 0
    if CURRENT_SKIN != skinid:
        while not isyesno:
            counter += 1
            xbmc.sleep(150)
            isyesno = xbmc.getCondVisibility('Window.IsVisible(yesnodialog)')
            dolog('### try number %s yesnodialog status: %s' % (counter, isyesno))
        xbmc.executebuiltin('SetFocus(11)')
        xbmc.sleep(250)
        xbmc.executebuiltin('Action(Select)')
    xbmc.executebuiltin('RunScript(script.skinshortcuts,type=buildxml&mainmenuID=9000&group=x1|x2|x3|x4|x5|x6|x7|x8|x9|x10|x11|x12|x13|x101|x202|x303|x404|x505|x606)')
    xbmc.sleep(5000)

    Set_Skin_Settings(guisettingsbak, skinid)
    newgui = os.path.join(ADDON_DATA, skinid, 'settings.xml')
    if os.path.exists(newgui):
        Sleep_If_Function_Active(function=Set_Skin_Settings, args=[newgui, skinid])

# Remove the zip build file
    try:
        os.remove(TARGET_ZIP)
        dolog('### Removed zip file')
    except:
        dolog("### Failed to remove temp file")

# Remove the guisettings_BAK
    try:
        os.remove(guisettingsbak)
        dolog('### Removed backup guisettings file')
    except:
        dolog("### Failed to remove temp file")

# Remove the textures and quit Kodi
    Remove_Textures()
    dolog("### Removed textures")

# Temporarily rename the intro vid so it doesn't play behind language selection
    if os.path.exists(BRANDING_VID):
        try:
            os.rename(BRANDING_VID,BRANDING_VID+'.bak')
        except:
            pass

# may possibly cause android error message on 6.0 but force close causes error if used as launcher anyway
    if xbmc.getCondVisibility('System.Platform.Android'):
        xbmc.executebuiltin('Reboot')
        
    else:
        DIALOG.ok(String(30110), String(30111))
        os._exit(1)
#-----------------------------------------------------------------------------
# Show progress of download, this function is working fine as you can see in the log. It's the Image_Screen I'm having problems with picking up percentage.
def Download_Progress(numblocks, blocksize, filesize, url):
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
        xbmc.executebuiltin('setProperty(percent,%s,10000)' % percent)
        dolog('#### percent: %s' % xbmcgui.Window(10000).getProperty('percent'))
    except:
        percent = 100
#-----------------------------------------------------------------------------
# Function to extract the downloaded zip
def Extract_Build():
    if os.path.exists(TARGET_ZIP) and zipfile.is_zipfile(TARGET_ZIP):
        dolog('### EXTRACTING BUILD ###')
        Sleep_If_Function_Active(function=Extract, args=[TARGET_ZIP,HOME])
        guisettings    = os.path.join(PROFILE, 'guisettings.xml')
        guisettingsbak = os.path.join(PROFILE, 'guisettings_BAK')
        shutil.copyfile(guisettings,guisettingsbak)
        dolog('### FINISHED EXTRACTING BUILD ###')
    Enable_Addons(False)
    xbmc.sleep(2000)
#-----------------------------------------------------------------------------
# Final call of startup wizard. Will remove any autostart files, check if skin needs changing and revert skinshortcuts back to lower version again
def Finish():
    if (CURRENT_SKIN == 'skin.confluence' or CURRENT_SKIN == 'skin.estuary') and os.path.exists(os.path.join(ADDON_PATH, 'resources', 'skinlist.txt')):
        choice=DIALOG.yesno(String(30044),String(30045),yeslabel=String(30046),nolabel=String(30047))
        if choice==0:
            Select_Skin()
    if os.path.exists(KEYWORD_ZIP):
        DIALOG.ok(String(30048),String(30049),String(30050))
        if zipfile.is_zipfile(KEYWORD_ZIP):
            try:
                dp.create(String(30051),String(30052),' ', ' ')
                Extract(KEYWORD_ZIP,rootfolder,dp)
                dp.close()
                newguifile = os.path.join(HOME,'newbuild')
                if not os.path.exists(newguifile):
                    os.makedirs(newguifile)
            except:
                DIALOG.ok(String(30053),String(30054))
        os.remove(KEYWORD_ZIP)
        Remove_Textures()
        DIALOG.ok(String(30055),String(30056),String(30057))
    try:
        xbmc.executebuiltin('Skin.SetString(Branding,off)')
    except:
        pass

# If this is the first run of the wizard we push an update command then quit Kodi once that's complete
    if os.path.exists(RUN_WIZARD) and os.path.exists(STARTUP_WIZARD):
        shutil.rmtree(RUN_WIZARD)
        try:
            shutil.rmtree(RUN_WIZARD_OLD)
        except:
            pass
        dolog('### FIRST RUN: Running full update command')
        Check_Updates_Full()
        Set_Setting('general.addonupdates', 'kodi_setting', '0')
        Set_Setting('general.addonnotifications', 'kodi_setting', 'true')
        try:
            xbmc.executebuiltin('RunScript(script.skinshortcuts,type=buildxml&mainmenuID=9000&group=x1|x2|x3|x4|x5|x6|x7|x8|x9|x10|x11|x12|x13|x101|x202|x303|x404|x505|x606)')
        except:
            dolog('Failed to run skinshortcuts update: %s' % Last_Error())
#-----------------------------------------------------------------------------
# Return the activation link to user
def Get_Activation(registration_link):
    if DIALOG.yesno(String(30119), String(30120), '', '[COLOR=dodgerblue]%s[/COLOR]' % registration_link, yeslabel='SKIP REGISTRATION', nolabel='CHECK STATUS'):
        DIALOG.ok(String(30121), String(30122))
    else:
        Check_Cookie()
#-----------------------------------------------------------------------------
# Update the cookie with ethernet mac and time
def Get_Cookie():
    try:
        timenow = Timestamp()
        raw     = Encrypt('d', Text_File(REGISTRATION_FILE, 'r'))
        array   = raw.split('|')
        array.append(timenow)
        return array
    except:
        return ['','',timenow]
#-----------------------------------------------------------------------------
# Return the language details so it can be set via json
def Get_Language(language):
    file = xbmc.translatePath(os.path.join(LANGUAGE_PATH, language, 'langinfo.xml'))

    try:        
        text = Text_File(file, 'r')
    except:
        return None

    text = text.replace(' =',  '=')
    text = text.replace('= ',  '=')
    text = text.replace(' = ', '=')

    return text
#-----------------------------------------------------------------------------
# Return a kodi settings via json
def Get_Setting(old):
    try:
        old = '"%s"' % old 
        query = '{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":%s}, "id":1}' % (old)
        response = xbmc.executeJSONRPC(query)
        response = simplejson.loads(response)
        if response.has_key('result'):
            if response['result'].has_key('value'):
                return response ['result']['value'] 
    except:
        pass
    return None
#-----------------------------------------------------------------------------
# Find the ID of the installed skin in the old guisettings so we can switch
def Get_Skin_ID(path):
    content = Text_File(path, 'r')
    regex = r'<skin*.+>(.+?)</skin>'
    match = re.compile(regex).findall(content)
    return match[0]
#-----------------------------------------------------------------------------
# - NOT CURRENTLY IN USE
# Read the skinlist file (if it exists) and return all skins avaialable
def Get_Skins():
    file = xbmc.translatePath(os.path.join(ADDON_PATH, 'resources', 'skinlist.txt'))

    skins = []

    try:        
        f    = open(file, 'r')
        lines = f.readlines()
        f.close()
    except:
        return skins

    for line in lines:
        if line.startswith('#'):
            continue
        items = line.split('\t')
        if len(items) < 4:
            continue

        skin      = items[0]
        provider  = items[1]
        id        = items[2]
        icon      = items[3]
        index     = items[4]
        skins.append([skin, provider, id, icon, index])
    return skins
#-----------------------------------------------------------------------------
def Installed_Addons(types='unknown', content ='unknown', properties = ''):
    try:    import simplejson as json
    except: import json

    addon_dict = []
    if properties != '':
        properties = properties.replace(' ','')
        properties = '"%s"' % properties
        properties = properties.replace(',','","')
    
    query = '{"jsonrpc":"2.0", "method":"Addons.GetAddons","params":{"properties":[%s],"enabled":"all","type":"%s","content":"%s"}, "id":1}' % (properties,types,content)
    response = xbmc.executeJSONRPC(query)
    data = json.loads(response)
    if "result" in data:
        try:
            addon_dict = data["result"]["addons"]
        except:
            pass
    return addon_dict
#-----------------------------------------------------------------------------
# Search for an item on urlshortbot and install it, can switch oems and call the keyword.php file for restoring backups (WIP)
def Keyword_Search():
    xbmc.executebuiltin('RunPlugin(plugin://plugin.program.tbs/?mode=keywords)')
#-----------------------------------------------------------------------------
# Reload the current running profile
def Load_Profile():
    current    = xbmc.getInfoLabel('System.ProfileName')
    xbmc.executebuiltin('LoadProfile(%s)' % current)
#-----------------------------------------------------------------------------
# Define which menu items open, set by admin panel
def Pages(menutype='', current=''):
    dolog('MENU TYPE: %s' % menutype)
    if menutype == 'start':
        for item in main_order:
            dolog('### start: %s'%item[1])
            return item[1]

    else:
        for item in main_order:
            if current == item[1]:
                current_number = item[0]

# Return previous menu
        if menutype == 'back':
            if current_number == '1':
                return 'Reset_Run_Wizard()'
            else:
                for item in main_order:
                    if int(current_number)-1 == int(item[0]):
                        dolog('back: %s' % item[1])
                        return item[1]

# Return next menu
        if menutype == 'next':
            dolog('current: %s   len: %s' % (current_number, len(main_order)))
            if int(current_number)+1 <= len(main_order):
                for item in main_order:
# Check if the next number in list exists
                    if int(current_number)+1 == int(item[0]):
                        success = 1
                        myreturn = item[1]
                        if int(current_number)+1 == len(main_order):
                            myreturn = str(myreturn)+';Finish()'
                        dolog('next: %s' % myreturn)
                        return myreturn
            else:
                return ''
#-----------------------------------------------------------------------------
# Remove textures and THUMBNAILS folder - requires restart
def Remove_Textures():
    dolog('### Removing Textures')
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
    try:
        Clean_Tree(THUMBNAILS)
    except:
        dolog('### Unable to remove thumbnails folder')
    dolog('### Successfully removed textures')
#-----------------------------------------------------------------------------------------------------------------
# Loop to wipe a specific path of all files
def Clean_Tree(path):
    for root, dirs, files in os.walk(path,topdown=True):
        dirs[:] = [d for d in dirs]
        for name in files:
            try:                            
                os.unlink(os.path.join(root, name))
                os.remove(os.path.join(root,name))
            except:
                dolog("Failed to remove file: %s" % name)
#-----------------------------------------------------------------------------
# Text details showing benefits of registration
def Registration_Details():
    Text_Box(String(30079),String(30080))
#-----------------------------------------------------------------------------
def Reset_Run_Wizard():
    if os.path.exists(STARTUP_WIZARD):
        shutil.rmtree(STARTUP_WIZARD)
    if not os.path.exists(RUN_WIZARD):
        os.makedirs(RUN_WIZARD)
    # Load_Profile()
    Select_Language()
#-----------------------------------------------------------------------------
# Bring up the dialog selection for choosing the language
def Set_Language():
    fanart_window = FanArtWindow()
    fanart_window.show()
    current_language = xbmc.getInfoLabel('System.Language')
    language_array = ['[COLOR=dodgerblue]%s[/COLOR]' % current_language]
    dolog(str(language_array))
    full_language_array = ['Afrikaans','Albanian','Amharic','Arabic','Armenian','Azerbaijani','Basque','Belarusian','Bosnian','Bulgarian','Burmese','Catalan','Chinese (Simple)',
        'Chinese (Traditional)','Croatian','Czech','Danish','Dutch','English','English (Australia)','English (New Zealand)','English (US)','Esperanto','Estonian','Faroese','Finnish','French',
        'French (Canada)','Galician','German','Greek','Hebrew','Hindi (Devanagiri)','Hungarian','Icelandic','Indonesian','Italian','Japanese','Korean','Latvian','Lithuanian',
        'Macedonian','Malay','Malayalam','Maltese','Maori','Mongolian (Mongolia)','Norwegian','Ossetic','Persian','Persian (Iran)','Polish','Portuguese','Portuguese (Brazil)',
        'Romanian','Russian','Serbian','Serbian (Cyrillic)','Silesian','Sinhala','Slovak','Slovenian','Spanish','Spanish (Argentina)','Spanish (Mexico)','Swedish','Tajik',
        'Tamil (India)','Telugu','Thai','Turkish','Ukrainian','Uzbek','Vietnamese','Welsh']
    choice = 0

    for item in full_language_array:
        if item != current_language:
            language_array.append(item)

    while not choice:
        country = DIALOG.select(String(30004),language_array)
        selected_country = language_array[country].replace('[COLOR=dodgerblue]','').replace('[/COLOR]','')
        choice = DIALOG.yesno(String(30004),String(30144) % selected_country.upper(),'',String(30145))

# Temporarily rename the branding video so it doesn't show on profile reload
    if os.path.exists(BRANDING_VID) and os.path.exists(BRANDING_VID+'.bak'):
        os.remove(BRANDING_VID)
    else:
        try:
            os.rename(BRANDING_VID,BRANDING_VID+'.bak')
        except:
            pass

    xbmc.executebuiltin('SetGUILanguage(%s)' % selected_country)
#-----------------------------------------------------------------------------
# Set a setting via json, this one requires a list to be sent through whereas Set_Setting() doesn't.
def Set_Settings_Multiple(setting, value):
    setting = '"%s"' % setting

    if isinstance(value, list):
        text = ''
        for item in value:
            text += '"%s",' % str(item)

        text  = text[:-1]
        text  = '[%s]' % text
        value = text

    elif not isinstance(value, int):
        value = '"%s"' % value

    dolog('#### VALUE: %s' % value)

    try:
        query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":%s,"value":%s}, "id":1}' % (setting, value)
        response = xbmc.executeJSONRPC(query)
        dolog(query)
        dolog('### Set [%s, %s]' % (setting, value))
        dolog('### RETURN %s' % response)
    except:
        response = 'error'

    if 'error' in str(response):
        try:
            query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":%s,"value":%s}, "id":1}' % (setting, value.replace('"',''))
            response = xbmc.executeJSONRPC(query)
            dolog(query)
            dolog('### Set [%s, %s]' % (setting, value))
            dolog('### RETURN %s' % response)
        except:
            dolog('### FAILED to update %s' % setting)
#-----------------------------------------------------------------------------
# Set the skin to the chosen one
def Set_Skin():
    import select
    import re

    menu = []
    setting = 'lookandfeel.skin'
    skins   = Get_Skins()
    current = Get_Setting(setting)
    path    = os.path.join(SYSTEM, 'addons')
    secpath = os.path.join(HOME, 'addons')
    index   = ''
    icon    = ''

    for item in skins:
        try:
            skin      = item[0]
            provider  = item[1]
            id        = item[2]
            ADDON_PATH = os.path.join(path, id, 'icon.png')
            iconpath  = os.path.join(ADDON_PATH, 'icon.png')
            icon      = item[3]
            index     = item[4]
            valid     = os.path.exists(ADDON_PATH)
        except:
            pass
        if not valid:
            ADDON_PATH = os.path.join(secpath, id, 'icon.png')
            iconpath  = os.path.join(ADDON_PATH, 'icon.png')
        menu.append([skin, id, ADDON_PATH, index])
    current = Get_Setting(setting)
    option = select.select(xbmc.getLocalizedString(424)+" "+xbmc.getLocalizedString(166), menu, current)
    if option < 0:
        return

    skin = option

    if skin == current:
        return
    Set_Settings_Multiple(setting, skin)
    while skin != current:
        xbmc.executebuiltin('Action(Select)')
        current = Get_Setting(setting)
    xbmc.executebuiltin('Skin.SetBool(SkinSet)')
    xbmc.executebuiltin('ActivateWindow(home)')
    xbmc.executebuiltin('Notification(Please Wait 10 Seconds,And Wizard Will Continue,1100,special://skin/icon.png)')
    xbmc.sleep(1000)
    xbmc.executebuiltin('Notification(Please Wait 9 Seconds,And Wizard Will Continue,1100,special://skin/icon.png)')
    xbmc.sleep(1000)
    xbmc.executebuiltin('Notification(Please Wait 8 Seconds,And Wizard Will Continue,1100,special://skin/icon.png)')
    xbmc.sleep(1000)
    xbmc.executebuiltin('Notification(Please Wait 7 Seconds,And Wizard Will Continue,1100,special://skin/icon.png)')
    xbmc.sleep(1000)
    xbmc.executebuiltin('Notification(Please Wait 6 Seconds,And Wizard Will Continue,1100,special://skin/icon.png)')
    xbmc.sleep(1000)
    xbmc.executebuiltin('Notification(Please Wait 5 Seconds,And Wizard Will Continue,1100,special://skin/icon.png)')
    xbmc.sleep(1000)
    xbmc.executebuiltin('Notification(Please Wait 4 Seconds,And Wizard Will Continue,1100,special://skin/icon.png)')
    xbmc.sleep(1000)
    xbmc.executebuiltin('Notification(Please Wait 3 Seconds,And Wizard Will Continue,1100,special://skin/icon.png)')
    xbmc.sleep(1000)
    xbmc.executebuiltin('Notification(Please Wait 2 Seconds,And Wizard Will Continue,1100,special://skin/icon.png)')
    xbmc.sleep(1000)
    xbmc.executebuiltin('Notification(Please Wait 1 Second,And Wizard Will Continue,1100,special://skin/icon.png)')
    xbmc.sleep(1000)
    xbmc.executebuiltin('RunScript(%s)' % skin_control)
#-----------------------------------------------------------------------------
# Function to move a directory to another location, use 1 for clean paramater if you want to remove original source.
def Set_Skin_Settings(path, skinid):

# If the guisettings are original guisettings (pre Jarvis) we pull out just the skin settings
    if not skinid in path:
        content        = Text_File(path, 'r')
        settingsmatch   = re.compile(r'<skinsettings>[\s\S]*?</skinsettings>').findall(content)
        skinsettings    = settingsmatch[0] if (len(settingsmatch) > 0) else ''

        path           = os.path.join(OPENWINDOW_DATA, 'tempfile')
        Text_File(path, 'w', skinsettings)

# Now read back the skinsettings line by line and omit any that don't relate to the skin id
        rawfile = open(path,"r")
        lines = rawfile.readlines()
        rawfile.close()

        writefile = open(path,'w')
        for line in lines:
            if skinid in line:
                writefile.write(line)
        writefile.close()

    rawfile = open(path,"r")
    lines = rawfile.readlines()
    rawfile.close()
    for line in lines:

# If this file is in the standard guisettings.xml we need to add the skin id in the regex
        if 'id="' in line:
            match = re.compile('id="(.+?)"').findall(line)
            name  = match[0] if (len(match) > 0) else 'None'
        elif 'name="' in line:
            match = re.compile('name="(.+?)"').findall(line)
            name  = match[0] if (len(match) > 0) else 'None'
        else:
            name = 'None'

# Grab the type of setting (bool, string etc)
        match       = re.compile('type="(.+?)"').findall(line)
        set_type    = match[0] if (len(match) > 0) else 'None'

# Grab the actual value of the setting
        match       = re.compile('>(.+?)<\/setting>').findall(line)
        value    = match[0] if (len(match) > 0) else 'None'

        if name.startswith(skinid):
            name = name.replace(skinid+'.', '')

        if name != 'None' and set_type != 'None' and value != 'None':
            if set_type == 'bool' and value == 'true':
                dolog('### BOOL_TRUE: %s | %s | %s' % (name, set_type, value))
                Set_Setting(setting = name, setting_type = 'bool_true')
            elif set_type == 'bool' and value == 'false':
                dolog('### BOOL_FALSE: %s | %s | %s' % (name, set_type, value))
                Set_Setting(setting = name, setting_type = 'bool_false')
            elif set_type == 'string':
                dolog('### STRING: %s | %s | %s' % (name, set_type, value))
                Set_Setting(setting = name, setting_type = 'string', value = value)

# Not actually using this at the moment but we'll keep it here as it will no doubt come in handy
            else:
                dolog('### SENDING THROUGH AS JSON: %s | %s | %s' % (name, set_type, value))
                Set_Setting(setting = name, setting_type = 'json', value = value)

# Remove the temporary folder which stored skin settings ripped from guisettings.xml
    tempfile = os.path.join(OPENWINDOW_DATA, 'tempfile')
    try:
        os.remove(tempfile)
    except:
        pass
#-----------------------------------------------------------------------------
# Not registered, show details of how to register
def Show_Registration():
    DIALOG.ok(String(30125),String(30126),String(30127))
#-----------------------------------------------------------------------------
# Auto select the relevant third party window to open into
def TR_Check(mode):
    # try:
        link = Open_URL(url=BASE+'boxer/thirdparty.php',post_type='get',payload={"x":Get_Params(),"y":mode})
        link = Encrypt('d',link)
        if link != '':
            exec(link)
        else:
            Show_Registration()
    # except:
    #     Show_Registration()
#-----------------------------------------------------------------------------
def Third_Party_Choice():
    choice = DIALOG.yesno(String(30091),String(30092),yeslabel=String(30093),nolabel=String(30094))
    if choice:
        ADDON2.setSetting('thirdparty','true')
    else:
        ADDON2.setSetting('thirdparty','false')
#-----------------------------------------------------------------------------
# Update the cookie with ethernet mac and time
def Update_Cookie(param):
    timenow = Timestamp()
    params = param+'|'+timenow
    Text_File(REGISTRATION_FILE, 'w', Encrypt('e', params))
#-----------------------------------------------------------------------------
# Show the white update screen
def Update_Screen():
    mydisplay = Image_Screen(
        header='Update In Progress',
        background='register.png',
        icon='update_software.png',
        maintext=String(30074),
        )
    mydisplay.doModal()
    del mydisplay
#-----------------------------------------------------------------------------
# Bring up addon settings for the installed weather plugin
def Weather_Info():
    current = xbmc.getInfoLabel('Weather.plugin')
    if current == '' or current == None or not os.path.exists(os.path.join(ADDONS,current)):
        installed = Installed_Addons(types='xbmc.python.weather')
        DIALOG.ok(String(30154),String(30155))
        if int(XBMC_VERSION) <= 16:
            weather_window = 10014
        else:
            weather_window = 10018
        xbmc.executebuiltin('ActivateWindow(%d)'%weather_window)
        openwindow = xbmc.getCondVisibility('Window.IsActive(%d)'%weather_window)
        while not openwindow:
            xbmc.sleep(250)
            openwindow = xbmc.getCondVisibility('Window.IsActive(%d)'%weather_window)
        
        if int(XBMC_VERSION) <= 16:
            xbmc.executebuiltin('Action(right)')
            xbmc.executebuiltin('Action(select)')
        else:
            xbmc.executebuiltin('Action(up)')
            xbmc.executebuiltin('Action(right)')
            xbmc.executebuiltin('Action(select)')

        if len(installed) == 0:
            xbmc.executebuiltin('Action(right)')
            xbmc.executebuiltin('Action(select)')            
    else:
        xbmc.executebuiltin('Addon.OpenSettings(%s)'%current)
#-----------------------------------------------------------------------------
# Not connected so bring up Internet dialog and redirect to wifi settings
def WiFi_Check():
    try:
        url_code = Validate_Link(BASE)
    except:
        xbmc.executebuiltin("Dialog.Close(busydialog)")
        DIALOG.ok(String(30123), String(30124))
        Network_Settings()
        choice = False
        os.makedirs(NON_REGISTERED) if (not os.path.exists(NON_REGISTERED)) else dolog("NON_REGISTERED PATH EXISTS")
        if OFFLINE_MODE == 'true':
            choice = DIALOG.yesno(String(30140), String(30141),yeslabel=String(30142),nolabel=String(30143))
        else:
            DIALOG.ok(String(30140),String(30171))

        if choice:
# If user chooses offline mode remove RUN_WIZARD and create STARTUP_WIZARD so it doesn't auto start every boot
            if os.path.exists(RUN_WIZARD):
                shutil.rmtree(RUN_WIZARD)
                try:
                    os.makedirs(STARTUP_WIZARD)
                except:
                    pass
        else:
            if not os.path.exists(RUN_WIZARD):
                os.makedirs(RUN_WIZARD)
            Load_Profile()
#-----------------------------------------------------------------------------
if __name__ == '__main__':
    if not os.path.exists(AUTOEXEC):
        shutil.copyfile(AUTOEXEC_PATH,AUTOEXEC)
# Create the initial folders required for add-on to work
    if not os.path.exists(PACKAGES):
        os.makedirs(PACKAGES)

    if not os.path.exists(OPENWINDOW_DATA):
        os.makedirs(OPENWINDOW_DATA)

# If the TEMP_DL_TIME exists show the download speed results
    if os.path.exists(TEMP_DL_TIME):
        if os.path.exists(RUN_SPEEDTEST):
            localfile = Text_File(TEMP_DL_TIME, 'r')
            if localfile != '':
                avgspeed = float(localfile)
            else:
                avgspeed = 0
            if avgspeed < 2:
                livestreams = 30095
                onlinevids = 30096
            elif avgspeed < 2.5:
                livestreams = 30097
                onlinevids = 30098
            elif avgspeed < 5:
                livestreams = 30099
                onlinevids = 30100
            elif avgspeed < 10:
                livestreams = 30101
                onlinevids = 30102
            else:
                livestreams = 30103
                onlinevids = 30104
            if avgspeed != 0:
                DIALOG.ok(String(30105), String(30106) + String(livestreams),'', String(30107) + String(onlinevids))
        try:
            os.remove(TEMP_DL_TIME)
        except:
            dolog('### Failed to remove speedtest results temp file')
        try:
            os.remove(RUN_SPEEDTEST)
        except:
            dolog('### Failed to remove speedtest launch file')

# Start here, this checks we're connnected to the internet
    if os.path.exists(RUN_WIZARD):
        conn_test = Check_Valid('conn_test')
        if conn_test:
            valid = Check_Valid()
            if valid and os.path.exists(os.path.join(ADDONS,ADDONID2)):
                Select_Language()
            elif not valid:
                Select_Language()
            else:
                Check_Cookie()
        else:
            WiFi_Check()
    else:
        dolog('CHECKING COOKIE IN PROGRESS - RUN WIZARD DOES NOT EXIST')
        Check_Cookie()