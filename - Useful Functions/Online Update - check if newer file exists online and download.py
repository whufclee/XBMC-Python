#
#      Copyright (C) 2016 Lee Randall (whufclee)
#
#  Feel free to use this code under the GPL2 but DO NOT remove the license
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
import time, shutil, zipfile

HOME             =  '' # WHERE DO YOU WANT IT TO EXTRACT TO
updateurl        =  '' # ENTER LOCATION OF ONLINE ZIP
updatedst        =  '' # WHAT DO YOU WANT THE TEMPORARY DOWNLOAD FILE PATH TO BE (PROBABLY A FILE IN PACKAGES)
dp               =  xbmcgui.DialogProgress()

# Check the last modified date of online file against our locally stored text file date
def Check_File_Date(url, datefile, localdate, dst):
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        conn = urllib2.urlopen(req)
        last_modified = conn.info().getdate('last-modified')
        last_modified = time.strftime('%Y%m%d%H%M%S', last_modified)
        if int(last_modified) > int(localdate):
            urllib.urlretrieve(url,dst)
            extract(dst,HOME)
            writefile = open(datefile, 'w+')
            writefile.write(last_modified)
            writefile.close()
        try:
            if os.path.exists(dst):
                os.remove(dst)
        except:
            pass
    except:
        print"Failed with update: "+str(url)

# Grab the date stored locally and parse through to the main online check function
def Check_Updates(url, datefile, dst):
    if os.path.exists(datefile):
        readfile = open(datefile,'r')
        localdate = readfile.read()
        readfile.close()
    else:
        localdate = 0
    Check_File_Date(url, datefile, int(localdate), dst)

# Extract a zip with progress
def extract(_in, _out):
    dp.create('Extracting Zip File','','','')
    zin    = zipfile.ZipFile(_in,  'r')
    nFiles = float(len(zin.infolist()))
    count  = 0

    for item in zin.infolist():
        try:
            count += 1
            update = count / nFiles * 100
            dp.update(int(update))
            zin.extract(item, _out)
    
        except Exception, e:
            xbmc.log(str(e))

###################################################################
# OTHER USEFUL FUNCTIONS YOU MAY WANT TO USE WITH THIS IN YOUR CODE
###################################################################
# Download a zip with progress bar
def download(url, dest):
    dp = xbmcgui.DialogProgress()
    dp.create("Status...","Downloading Content",' ', ' ')
    dp.update(0)
    start_time=time.time()
    urllib.urlretrieve(url, dest, lambda nb, bs, fs: _pbhook(nb, bs, fs, dp, start_time))

# Dialog showing percentage of download complete and ETA  
def _pbhook(numblocks, blocksize, filesize, dp, start_time):
    try: 
        percent = min(numblocks * blocksize * 100 / filesize, 100) 
        currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
        kbps_speed = numblocks * blocksize / (time.time() - start_time) 
        if kbps_speed > 0: 
            eta = (filesize - numblocks * blocksize) / kbps_speed 
        else: 
            eta = 0 
        kbps_speed = kbps_speed / 1024 
        total = float(filesize) / (1024 * 1024) 
        mbs = '%.02f MB of %.02f MB' % (currently_downloaded, total) 
        e = 'Speed: %.02f Kb/s ' % kbps_speed 
        e += 'ETA: %02d:%02d' % divmod(eta, 60) 
        dp.update(percent, mbs, e)
    except: 
        percent = 100 
        dp.update(percent) 
    if dp.iscanceled(): 
        dp.close()

# Basic function for reading the URL
def Open_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 10.0; WOW64; Windows NT 5.1; en-GB; rv:1.9.0.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36 Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link     = response.read()
    response.close()
    return link.replace('\r','').replace('\n','').replace('\t','')

# Create a timestamp that matches the format of what we're grabbing from online, we'll store this each time we download a new one
def Timestamp():
    now = time.time()
    localtime = time.localtime(now)
    return time.strftime('%Y%m%d%H%M%S', localtime)

# Example of calling the update from a service
xbmc.log("### UPDATE SERVICE ###")
Check_Updates(updateurl, xbmc.translatePath('special://profile/addon_data/plugin.program.myaddon/updatechk'), updatedst)