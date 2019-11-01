import xbmcgui
import urllib
import time

def download(url, dest, dp = None):
    dp.create(ADDON.getLocalizedString(30058),ADDON.getLocalizedString(30034))
    dp.update(0)
    start_time=time.time()
    urllib.urlretrieve(url, dest)