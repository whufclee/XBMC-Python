import xbmcgui
import urllib
import urllib2

def download(url, dest, dp = None):
    try:
        if not dp:
            dp = xbmcgui.DialogProgress()
            dp.create("Status...","Installing Files",'', 'Please wait...')
    
        dp.update(0)
        opener = urllib2.build_opener()
        opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')]
        f = opener.open(url)
        data = f.read()
        with open(dest, "wb") as code:
            code.write(data)
    except:
        raise

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
