#       Copyright (C) 2016 noobsandnerds.com
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with XBMC; see the file COPYING.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#

import xbmc, xbmcaddon, xbmcgui, os, re, urllib, urllib2
import utils
import time
import extract, download

AddonID          =  'script.community.portal'
ADDON            =  xbmcaddon.Addon(id=AddonID)
USERDATA         =  xbmc.translatePath(os.path.join('special://home/userdata',''))
ADDON_DATA       =  xbmc.translatePath(os.path.join(USERDATA,'addon_data'))
cookie           =  xbmc.translatePath(os.path.join(ADDON_DATA,AddonID,'temp'))
username         =  ADDON.getSetting('username').replace(' ','%20')
password         =  ADDON.getSetting('password')
dialog           =  xbmcgui.Dialog()
skinurl          = 'http://noobsandnerds.com/CP_Stuff/community_portal_skin.jpeg'
skindst          = xbmc.translatePath('special://home/addons/packages/tvps')

# update.checkUpdate()

def Check_File_Date(url, datefile, localdate, dst):
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    conn = urllib2.urlopen(req)
    last_modified = conn.info().getdate('last-modified')
    last_modified = time.strftime('%Y%m%d%H%M%S', last_modified)
    if int(last_modified) > int(localdate):
        download.download(url,dst)
        extract.all(dst,xbmc.translatePath('special://profile/addon_data'))
        writefile = open(datefile, 'w+')
        writefile.write(last_modified)
        writefile.close()
    try:
        if os.path.exists(dst):
            os.remove(dst)
    except:
        pass

def Check_Updates(url, datefile, dst):
    if os.path.exists(datefile):
        readfile = open(datefile,'r')
        localdate = readfile.read()
        readfile.close()
    else:
        localdate = 0
    Check_File_Date(url, datefile, int(localdate), dst)

def Open_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 10.0; WOW64; Windows NT 5.1; en-GB; rv:1.9.0.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36 Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link     = response.read()
    response.close()
    return link.replace('\r','').replace('\n','').replace('\t','')

def Timestamp():
    now = time.time()
    localtime = time.localtime(now)
    return time.strftime('%Y%m%d%H%M%S', localtime)

def User_Info():
    BaseURL       = 'http://noobsandnerds.com/TI/login/login_details.php?user=%s&pass=%s' % (username, password)
    link          = Open_URL(BaseURL).replace('\n','').replace('\r','')
    welcomematch  = re.compile('login_msg="(.+?)"').findall(link)
    welcometext   = welcomematch[0] if (len(welcomematch) > 0) else ''
    if not 'REGISTER FOR FREE' in welcometext:
        writefile = open(cookie, mode='w+')
        writefile.write('d="'+Timestamp()+'"\nlogin_msg="'+welcometext+'"')
        writefile.close()
        Check_Updates(skinurl, xbmc.translatePath('special://profile/addon_data/script.community.portal/skinchk'), skindst)
        param = None

        if len(sys.argv) > 1:
            param = sys.argv[1]

        xbmc.executebuiltin('Dialog.Close(busydialog)')
        utils.Launch(param)
    else:
        dialog.ok('INCORRECT LOGIN INFO','You need valid forum login credentials to use this addon.','If you haven\'t already done so you can register for FREE at [COLOR=gold]www.noobsandnerds.com[/COLOR]')
        ADDON.openSettings()
        
def verify():
    if not os.path.exists(cookie):
        User_Info()

    else:
        localfile3          = open(cookie, mode='r')
        content3            = localfile3.read()
        localfile3.close()
    
        userdatematch       = re.compile('d="(.+?)"').findall(content3)
        loginmatch          = re.compile('login_msg="(.+?)"').findall(content3)
        updatecheck         = userdatematch[0] if (len(userdatematch) > 0) else '0'
        welcometext         = loginmatch[0] if (len(loginmatch) > 0) else ''
        
        if int(updatecheck)+2000000 > int(Timestamp()):
            Check_Updates(skinurl, xbmc.translatePath('special://profile/addon_data/script.community.portal/skinchk'), skindst)

            param = None

            if len(sys.argv) > 1:
                param = sys.argv[1]

            xbmc.executebuiltin('Dialog.Close(busydialog)')
            utils.Launch(param)
        
        else:
            User_Info()       


if __name__ == '__main__':
    verify()
