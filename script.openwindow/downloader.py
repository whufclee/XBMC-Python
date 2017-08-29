import xbmcaddon
import xbmcgui
import urllib

ADDONID                    = 'script.openwindow'
ADDON                      = xbmcaddon.Addon(ADDONID)

def download(url, dest, dp = None):
    urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
 
def _pbhook(numblocks, blocksize, filesize, url, dp):
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
        dp.update(percent)
    
    except:
        percent = 100
        if dp:
            dp.update(percent)
    
            if dp.iscanceled(): 
                raise Exception("Cancelled")
    # if dp:
    #     dp.close()