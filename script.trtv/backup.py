#
#      Copyright (C) 2014-15 Sean Poyser and Richard Dean (write2dixie@gmail.com)
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

import xbmcgui
import os
import re

import dixie
import sfile

import zipfile

ROOT          = dixie.PROFILE 
FILENAME      = 'trtv-backup.zip'
LINE1         = 'Backup file now being created.'
LINE2         = 'Please wait, this may take a while.'
temp_settings = os.path.join(ROOT, 'temp_settings.xml')

def doBackup():
    CUSTOM = '1'

    chanType = dixie.GetSetting('chan.type')
    logoType = dixie.GetSetting('logo.type')
    
    try:
        dixie.log('Backup Type: %s' % str(sys.argv[1]))
    except:
        pass
    dixie.log('Backup: Channel setting is %s' % chanType)
    dixie.log('Backup: Logo setting is %s' % logoType)

    if (chanType == CUSTOM) or (logoType == CUSTOM):
        dixie.DialogOK('It appears you are using a custom location', 'for your channels or logos (Home Networking).', 'Please back-up TRTV manually.')
        return

    try:
        folder = getFolder('Please select backup folder location')

        if not folder:
            return False

        filename = os.path.join(folder, FILENAME)

        dp = dixie.Progress(LINE1, LINE2)

        success = doZipfile(filename, dp)

        dp.close()

        if success: 
            dixie.DialogOK('Backup successfully created')
        else:
            dixie.DeleteFile(filename)

        return True

    except Exception, e:
        dixie.log(e)

    return False


def doZipfile(outputFile, dp):
    zip = None

    source  = ROOT
    relroot = os.path.abspath(os.path.join(source, os.pardir))
    cookies = os.path.join(dixie.ADDONID, 'cookies')

    total = float(0)
    index = float(0)

    for root, dirs, files in os.walk(source):
        total += 1
        for file in files:
            total += 1

    for root, dirs, files in os.walk(source):
        if zip == None:
            zip = zipfile.ZipFile(outputFile, 'w', zipfile.ZIP_DEFLATED)

        index   += 1
        percent  = int(index / total * 100)
        if not updateProgress(dp, percent):
            return False

        local = os.path.relpath(root, relroot)       
        if local == cookies:
            continue

        for file in files:
            index   += 1
            percent  = int(index / total * 100)
            if not updateProgress(dp, percent):
                return False

            arcname  = os.path.join(local, file)
            filename = os.path.join(root, file)           
            if sys.argv[1] == 'sync' and file == 'settings.xml':
                clear_conflicting_data(arcname,filename)
                zip.write(temp_settings, arcname)
                try:
                    os.remove(temp_settings)
                except:
                    pass
            else:
                zip.write(filename, arcname)

    return True


def clear_conflicting_data(arcname,filename):
    dixie.log('ARCNAME: %s' % arcname)
    dixie.log('FILENAME: %s' % filename)
    readfile = open(filename,'r')
    content  = readfile.read()
    readfile.close()

    username    = re.compile('username" value="(.+?)"').findall(content)
    password    = re.compile('password" value="(.+?)"').findall(content)
    u1          = re.compile('xmlpath1.url".*').findall(content)
    f1          = re.compile('xmlpath1.file".*').findall(content)
    u2          = re.compile('xmlpath2.url".*').findall(content)
    f2          = re.compile('xmlpath2.file".*').findall(content)
    u3          = re.compile('xmlpath3.url".*').findall(content)
    f3          = re.compile('xmlpath3.file".*').findall(content)
    u4          = re.compile('xmlpath4.url".*').findall(content)
    f4          = re.compile('xmlpath4.file".*').findall(content)
    u5          = re.compile('xmlpath5.url".*').findall(content)
    f5          = re.compile('xmlpath5.file".*').findall(content)
    u6          = re.compile('xmlpath6.url".*').findall(content)
    f6          = re.compile('xmlpath6.file".*').findall(content)
    u7          = re.compile('xmlpath7.url".*').findall(content)
    f7          = re.compile('xmlpath7.file".*').findall(content)
    u8          = re.compile('xmlpath8.url".*').findall(content)
    f8          = re.compile('xmlpath8.file".*').findall(content)
    u9          = re.compile('xmlpath9.url".*').findall(content)
    f9          = re.compile('xmlpath9.file".*').findall(content)
    u10         = re.compile('xmlpath10.url".*').findall(content)
    f10         = re.compile('xmlpath10.file".*').findall(content)
    dixie.log('u1: %s' % u1[0])
    dixie.log('u2: %s' % u2[0])
    dixie.log('u3: %s' % u3[0])
    dixie.log('u4: %s' % u4[0])
    dixie.log('u5: %s' % u5[0])
    dixie.log('u6: %s' % u6[0])
    dixie.log('u7: %s' % u7[0])
    dixie.log('u8: %s' % u8[0])
    dixie.log('u9: %s' % u9[0])
    dixie.log('u10: %s' % u10[0])
    dixie.log('f1: %s' % f1[0])
    dixie.log('f2: %s' % f2[0])
    dixie.log('f3: %s' % f3[0])
    dixie.log('f4: %s' % f4[0])
    dixie.log('f5: %s' % f5[0])
    dixie.log('f6: %s' % f6[0])
    dixie.log('f7: %s' % f7[0])
    dixie.log('f8: %s' % f8[0])
    dixie.log('f9: %s' % f9[0])
    dixie.log('f10: %s' % f10[0])

    writefile   = open(temp_settings,'w')
    replacefile = (content.replace(username[0],'').replace(password[0],'').replace(u1[0],'xmlpath1.url" value="" />').replace(f1[0],'xmlpath1.file" value="" />')
                    .replace(u2[0],'xmlpath2.url" value="" />').replace(f2[0],'xmlpath2.file" value="" />').replace(u3[0],'xmlpath3.url" value="" />')
                    .replace(f3[0],'xmlpath3.file" value="" />').replace(u4[0],'xmlpath4.url" value="" />').replace(f4[0],'xmlpath4.file" value="" />')
                    .replace(u5[0],'xmlpath5.url" value="" />').replace(f5[0],'xmlpath5.file" value="" />').replace(u6[0],'xmlpath6.url" value="" />')
                    .replace(f6[0],'xmlpath6.file" value="" />').replace(u7[0],'xmlpath7.url" value="" />').replace(f7[0],'xmlpath7.file" value="" />')
                    .replace(u8[0],'xmlpath8.url" value="" />').replace(f8[0],'xmlpath8.file" value="" />').replace(u9[0],'xmlpath9.url" value="" />')
                    .replace(f9[0],'xmlpath9.file" value="" />').replace(u10[0],'xmlpath10.url" value="" />').replace(f10[0],'xmlpath10.file" value="" />')
                    .replace('type" value="File"','type" value="None"').replace('type" value="URL"','type" value="None"'))
    writefile.write(str(replacefile))
    writefile.close()

def updateProgress(dp, percent):
    dp.update(percent, LINE1, LINE2)
    if not dp.iscanceled():
        return True

    return False


def getFolder(title):
    folder = xbmcgui.Dialog().browse(3, title, 'files', '', False, False, os.sep)

    return xbmc.translatePath(folder)



if __name__ == '__main__':
    try:    doBackup()
    except: pass

    dixie.ADDON.openSettings()
