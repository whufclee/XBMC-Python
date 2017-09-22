# - coding: utf-8 -*-

# script.openwindow
# Startup Wizard (c) by whufclee (info@totalrevolution.tv)

# Total Revolution Startup Wizard is licensed under a
# Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.

# You should have received a copy of the license along with this
# work. If not, see http://creativecommons.org/licenses/by-nc-nd/4.0.

import os
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

ADDONID                    = 'script.openwindow'
ADDON                      =  xbmcaddon.Addon(ADDONID)
ADDONID2                   = 'plugin.program.tbs'
try:
    ADDON2                 = xbmcaddon.Addon(ADDONID2)
except:
    ADDON2                 = xbmcaddon.Addon(ADDONID)
HOME                       = xbmc.translatePath('special://home')
NATIVE                     = xbmc.translatePath('special://xbmc')
ADDONS                     = os.path.join(HOME,'addons')
PACKAGES                   = os.path.join(ADDONS,'packages')
ADDON_DATA                 = xbmc.translatePath('special://profile/addon_data')
ADDON_PATH                 = xbmcaddon.Addon(ADDONID).getAddonInfo("path")
OPENWINDOW_DATA            = os.path.join(ADDON_DATA,ADDONID)
INSTALL_COMPLETE           = os.path.join(OPENWINDOW_DATA,'INSTALL_COMPLETE')
RUN_SPEEDTEST              = os.path.join(OPENWINDOW_DATA,'RUN_SPEEDTEST')
NON_REGISTERED             = os.path.join(OPENWINDOW_DATA,'unregistered')
TARGET_ZIP                 = os.path.join(PACKAGES,'target.zip')
TEMP_DL_TIME               = os.path.join(PACKAGES,'dltime')
XBMC_VERSION               = xbmc.getInfoLabel("System.BuildVersion")[:2]
IP_ADDRESS                 = xbmc.getIPAddress()
CURRENT_SKIN               = xbmc.getSkinDir()
KEYWORD_FILE               = os.path.join(OPENWINDOW_DATA,'keyword')
INTERNET_ICON              = os.path.join(ADDON_PATH,'resources','images','internet.png')
BRANDING_VID               = xbmc.translatePath('special://home/media/branding/intro.mp4')
LANGUAGE_ART               = os.path.join(ADDON_PATH,'resources','images','language.jpg')
DEBUG                      = Addon_Setting(setting='debug')
OFFLINE_MODE               = Addon_Setting(setting='offline')
BASE                       = Addon_Setting(setting='base')
BASE2                      = '687474703a2f2f6e6f6f6273616e646e657264732e636f6d2f'
adult_store                = xbmc.translatePath('special://profile/addon_data/script.module.python.koding.aio/adult_store')
zip_path                   = xbmc.translatePath('special://home/addons/packages/~~ZIPS~~')
OWSETTINGS                 = xbmc.translatePath('special://profile/addon_data/script.openwindow/settings.xml')
branding                   = xbmc.translatePath('special://home/media/branding/branding.png')
if not os.path.exists(adult_store):
    os.makedirs(adult_store)
if BASE == '':
    Addon_Setting(setting='base',value='http://totalrevolution.xyz/')
    BASE = 'http://totalrevolution.xyz/'

STOP_COOKIE_CHECK          = 0
ACTION_HOME                = 7
ACTION_PREVIOUS_MENU       = 10
ACTION_SELECT_ITEM         = 7
regmode                    = 3
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
main_order.sort()
dolog('### main_order = %s' % main_order)
#-----------------------------------------------------------------------------
##############################################################################
######################## MAIN SKINNING/IMAGE CODE ############################
##############################################################################
#-----------------------------------------------------------------------------
# Show the Registration Screen
def Registration():
    mypages     = Pages('Registration()')
    backpage    = mypages[0]
    nextpage    = mypages[1]
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
    mypages     = Pages('Select_Audio_Android()')
    backpage    = mypages[0]
    nextpage    = mypages[1]
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
    mypages     = Pages('Select_Bluetooth_Android()')
    backpage    = mypages[0]
    nextpage    = mypages[1]
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
    mypages     = Pages('Select_Keyword()')
    backpage    = mypages[0]
    nextpage    = mypages[1]
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
    mypages     = Pages('Select_Local_Content()')
    backpage    = mypages[0]
    nextpage    = mypages[1]
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
def Select_Language(new_order=main_order):
    xbmc.executebuiltin("Skin.SetString(Wizard,inprogress)")
    global main_order
    if new_order:
        main_order = new_order
    main_order = new_order
    Set_Language()
#-----------------------------------------------------------------------------
# Show the resolution select screen
def Select_Resolution():
    mypages     = Pages('Select_Resolution()')
    backpage    = mypages[0]
    nextpage    = mypages[1]
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
# Show the third party enable/disable menu
def Select_Third_Party():
    mypages     = Pages('Select_Third_Party()')
    backpage    = mypages[0]
    nextpage    = mypages[1]
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
    mypages     = Pages('Select_Timezone_Android()')
    backpage    = mypages[0]
    nextpage    = mypages[1]
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
    mypages     = Pages('Select_Weather()')
    backpage    = mypages[0]
    nextpage    = mypages[1]
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
    mypages     = Pages('Select_Zoom()')
    backpage    = mypages[0]
    nextpage    = mypages[1]
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
    mypages     = Pages('Select_Zoom_Android()')
    backpage    = mypages[0]
    nextpage    = mypages[1]
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
    global branding
    if not os.path.exists(branding):
        branding = os.path.join(ADDON_PATH,'resources','images','branding.png')
        if not os.path.exists(branding):
            branding = os.path.join(NATIVE, 'addons',ADDONID,'resources','images','branding.png')
    self.header=String(kwargs['header'])
    self.background=kwargs['background']
    
    self.backbuttonfunction = kwargs['backbuttonfunction']
    self.nextbuttonfunction = kwargs['nextbuttonfunction']

    if self.backbuttonfunction.endswith('none'):
        self.backbutton = ''

# Assign the back button text, if Select Language we need to define that rather than use generic "BACK"
    if 'Select_Language()' in self.backbuttonfunction:
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
#-----------------------------------------------------------------------------
class MainMenuThreeItems(xbmcgui.Window):
  def __init__(self,*args,**kwargs):
    global branding
    if not os.path.exists(branding):
        branding = os.path.join(ADDON_PATH,'resources','images','branding.png')
        if not os.path.exists(branding):
            branding = os.path.join(NATIVE, 'addons',ADDONID,'resources','images','branding.png')
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
# Function to check activation status of the unit
def Check_Status(extension, email=''):
    params     = Get_Params()
    if email != '':
        status = Open_URL(url=BASE+'boxer/Check_License_new.php',post_type='post',payload={"x":params,"v":XBMC_VERSION,"r":extension,"e":Encrypt(message=email)})
    else:
        status = Open_URL(url=BASE+'boxer/Check_License_new.php',post_type='post',payload={"x":params,"v":XBMC_VERSION,"r":extension})
    if status:
        try:
            status = (Encrypt('d',status))
        except:
            pass
        exec(status)
    else:
        OK_Dialog(String(30123),String(30124))
        Network_Settings()
#-----------------------------------------------------------------------------
# Not on system, get user to register at www.totalrevolution.tv
def Enter_Licence():
    OK_Dialog(String(30125),String(30151))
    license = Keyboard(heading=String(30125))
    if len(license)==20 or len(license)==23:
        if license:
            OK_Dialog(String(30152),String(30153))
            email = Keyboard(String(30152))
            if email:
                Check_Status(license, email)
    else:
        OK_Dialog(String(30158),String(30160))
#-----------------------------------------------------------------------------
# Search for an item on urlshortbot and install it, can switch oems and call the keyword.php file for restoring backups (WIP)
def Keyword_Search():
    xbmc.executebuiltin('RunPlugin(plugin://plugin.program.tbs/?mode=keywords)')
#-----------------------------------------------------------------------------
# Define which menu items open, set by admin panel
def Pages(current=''):
    if current == 'start':
    # Run first item in list - called from Select_Language
        for item in main_order:
            return item[1]
    else:
        for item in main_order:
            if current == item[1]:
                current_number = int(item[0])-1

        if current_number == 0:
            back_function = 'Select_Language()'
        else:
            back_function = main_order[current_number-1][1]
        if current_number+1 == len(main_order):
            next_function = 'xbmc.executebuiltin("Skin.Reset(Wizard)")'

        else:
            next_function = main_order[current_number+1][1]
        return [back_function,next_function]
#-----------------------------------------------------------------------------
# Bring up the dialog selection for choosing the language
def Set_Language():
    fanart_window = FanArtWindow()
    fanart_window.show()
    current_language = xbmc.getInfoLabel('System.Language')
    language_array = ['[COLOR=dodgerblue]%s[/COLOR]' % current_language]
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
        country = Select_Dialog(String(30004),language_array)
        selected_country = language_array[country].replace('[COLOR=dodgerblue]','').replace('[/COLOR]','')
        choice = YesNo_Dialog(String(30004),String(30144) % selected_country.upper()+'\n'+String(30145))
    xbmc.executebuiltin('SetGUILanguage(%s)' % selected_country)
#-----------------------------------------------------------------------------
# Not registered, show details of how to register
def Show_Registration():
    OK_Dialog( String(30125),'%s\n%s'%(String(30126),String(30127)) )
#-----------------------------------------------------------------------------
# Auto select the relevant third party window to open into
def TR_Check(mode):
    link = Open_URL(url=BASE+'boxer/thirdparty.php',post_type='get',payload={"x":Get_Params(),"y":mode})
    link = Encrypt('d',link)
    if link != '':
        exec(link)
    else:
        Show_Registration()
#-----------------------------------------------------------------------------
#### TODO - Add option for enabling third party content
def Third_Party_Choice():
    choice = YesNo_Dialog(String(30091),String(30092),String(30093),String(30094))
    if choice:
        ADDON2.setSetting('thirdparty','true')
    else:
        ADDON2.setSetting('thirdparty','false')
#----------------------------------------------------------------    
# Bring up addon settings for the installed weather plugin
def Weather_Info():
    current = xbmc.getInfoLabel('Weather.plugin')
    if current == '' or current == None or not os.path.exists(os.path.join(ADDONS,current)):
        installed = Installed_Addons(types='xbmc.python.weather')
        OK_Dialog(String(30154),String(30155))
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
if __name__ == '__main__':
    xbmc.executebuiltin("Skin.Reset(Wizard)")
    xbmcgui.Window(10000).clearProperty('update_screen')
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
                OK_Dialog( String(30105), '%s\n%s'%( String(30106)+String(livestreams), String(30107)+String(onlinevids)) )
        try:
            os.remove(TEMP_DL_TIME)
        except:
            dolog('### Failed to remove speedtest results temp file')
        try:
            os.remove(RUN_SPEEDTEST)
        except:
            dolog('### Failed to remove speedtest launch file')

    if not os.path.exists(INSTALL_COMPLETE):
        regmode = 1
    elif len(sys.argv)>0 and os.path.exists(INSTALL_COMPLETE):
        if sys.argv[len(sys.argv)-1] == 'full':
            regmode = 1
        elif sys.argv[len(sys.argv)-1] == 'update':
            regmode = 3
        elif sys.argv[len(sys.argv)-1] == 'update_shares':
            regmode = 4
        else:
            regmode = 2
    Check_Status(regmode)