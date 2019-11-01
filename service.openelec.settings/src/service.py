################################################################################
#      This file is part of OpenELEC - http://www.openelec.tv
#      Copyright (C) 2009-2013 Stephan Raue (stephan@openelec.tv)
#      Copyright (C) 2013 Lutz Fiebach (lufie@openelec.tv)
#
#  This program is dual-licensed; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with OpenELEC; see the file COPYING.  If not, see
#  <http://www.gnu.org/licenses/>.
#
#  Alternatively, you can license this library under a commercial license,
#  please contact OpenELEC Licensing for more information.
#
#  For more information contact:
#  OpenELEC Licensing  <license@openelec.tv>  http://www.openelec.tv
################################################################################
# -*- coding: utf-8 -*-

import oe
import xbmc
import xbmcgui
import time
import threading
import socket
import os
import xbmcaddon
import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os,binascii,shutil
#import socket, fcntl, struct
import downloader
import extract


class service_thread(threading.Thread):

    def __init__(self, oeMain):
        try:
            oeMain.dbg_log('_service_::__init__', 'enter_function', 0)
            self.oe = oeMain
            self.wait_evt = threading.Event()
            self.socket_file = '/var/run/service.openelec.settings.sock'
            self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.sock.setblocking(1)
            if os.path.exists(self.socket_file):
                os.remove(self.socket_file)
            self.sock.bind(self.socket_file)
            self.sock.listen(1)
            self.stopped = False
            threading.Thread.__init__(self)
            self.daemon = True
            self.oe.dbg_log('_service_::__init__', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('_service_::__init__', 'ERROR: (' + repr(e) + ')')

    def stop(self):
        try:
            self.oe.dbg_log('_service_::stop', 'enter_function', 0)
            self.stopped = True
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.connect(self.socket_file)
            sock.send('exit')
            sock.close()
            self.sock.close()
            self.oe.dbg_log('_service_::stop', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('_service_::stop', 'ERROR: (' + repr(e) + ')')

    def run(self):
        try:
            self.oe.dbg_log('_service_::run', 'enter_function', 0)
            if self.oe.read_setting('openelec', 'wizard_completed') == None:
                threading.Thread(target=self.oe.openWizard).start()
            while self.stopped == False:
                self.oe.dbg_log('_service_::run', 'WAITING:', 1)
                (conn, addr) = self.sock.accept()
                message = conn.recv(1024)
                self.oe.dbg_log('_service_::run', 'MESSAGE:' + repr(message), 1)
                conn.close()
                if message == 'openConfigurationWindow':
                    if not hasattr(self.oe, 'winOeMain'):
                        threading.Thread(target=self.oe.openConfigurationWindow).start()
                    else:
                        if self.oe.winOeMain.visible != True:
                            threading.Thread(target=self.oe.openConfigurationWindow).start()
                if message == 'exit':
                    self.stopped = True
            self.oe.dbg_log('_service_::run', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('_service_::run', 'ERROR: (' + repr(e) + ')')


class cxbmcm(xbmc.Monitor):

    def __init__(self, *args, **kwargs):
        xbmc.Monitor.__init__(self)

    def onScreensaverActivated(self):
        oe.__oe__.dbg_log('c_xbmcm::onScreensaverActivated', 'enter_function', 0)
        if 'bluetooth' in oe.__oe__.dictModules:
            oe.__oe__.dictModules['bluetooth'].standby_devices()
        oe.__oe__.dbg_log('c_xbmcm::onScreensaverActivated', 'exit_function', 0)

    def onAbortRequested(self):
        pass

def wait_for_video():
    isplaying = xbmc.Player().isPlaying()
    if isplaying == 1:
        xbmc.sleep(500)
        print"Video Playing: Delay 1000ms"
        wait_for_video()
        
def Update_Check():
    print"######## UPDATE CHECK IN PLACE #########"
    ADDON = xbmcaddon.Addon(id='plugin.program.webinstaller')
    AddonID      =  'plugin.program.webinstaller'
    ADDONS       =  xbmc.translatePath(os.path.join('special://home','addons',''))
    dialog       =  xbmcgui.Dialog()
    dp           =  xbmcgui.DialogProgress()
    restore_dir  = '/storage/.restore'
    backup_dir   = '/storage/backup/'
    path         =  xbmc.translatePath(os.path.join('special://home/addons','packages'))
    checkurlraw='687474703a2f2f746f74616c78626d632e636f6d2f746f74616c7265766f6c7574696f6e2f636865636b5f54525f776562696e7374616c6c65722e747874'
    checkurl = binascii.unhexlify(checkurlraw)
    addonxml = xbmc.translatePath(os.path.join(ADDONS,AddonID,'addon.xml'))    
    localaddonversion = open(addonxml, mode='r')
    content = file.read(localaddonversion)
    file.close(localaddonversion)
    localaddonvermatch = re.compile('check="1" version="(.+?)"').findall(content)
    addonversion  = localaddonvermatch[0] if (len(localaddonvermatch) > 0) else '1.0'
    print"######## LOCAL VERSION : "+addonversion
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        link = Open_URL(checkurl)
        urlversionmatch = re.compile('version="(.+?)"').findall(link)
        urlzipmatch = re.compile('url="(.+?)"').findall(link)
        urlversion  = urlversionmatch[0] if (len(urlversionmatch) > 0) else '1.0'
        urlzip  = urlzipmatch[0] if (len(urlzipmatch) > 0) else ''
        if urlversion > addonversion:
            print"Downloading newer version"
            downloader.download(urlzip, path+'/plugin.program.webinstaller.zip', dp)
            Extract_all(path+'/plugin.program.webinstaller.zip', ADDONS, dp)
            time.sleep(1)
            xbmc.executebuiltin( 'UpdateLocalAddons' )
        else: print"###########  No update required, local version is: "+addonversion+" and online is: "+urlversion
    except: pass
    if os.path.exists(path+'/plugin.program.webinstaller.zip'):
        os.remove(path+'/plugin.program.webinstaller.zip')
    
def Open_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link     = response.read()
    response.close()
    return link.replace('\r','').replace('\n','').replace('\t','')

xbmcm = cxbmcm()
oe.load_modules()
oe.start_service()
wait_for_video()
monitor = service_thread(oe.__oe__)
monitor.start()
xbmcm.waitForAbort()

if hasattr(oe, 'winOeMain'):
    if oe.winOeMain.visible == True:
        oe.winOeMain.close()

oe.stop_service()
monitor.stop()
