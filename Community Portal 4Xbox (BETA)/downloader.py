import xbmcgui
import urllib
import urllib2
import socket

def download(url, dest, dp = None):
    socket.setdefaulttimeout(30)
    if not dp:
        dp = xbmcgui.DialogProgress()
        dp.create("Status...","Downloading",' ', ' ')
    dp.update(0)
    urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))

def _pbhook(numblocks, blocksize, filesize, url, dp):
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
        dp.update(percent)
    
    except:
        percent = 100
        dp.update(percent)
    
    if dp.iscanceled(): 
        raise Exception("Cancelled")
        dp.close()
