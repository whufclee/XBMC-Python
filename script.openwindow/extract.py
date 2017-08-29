import os
import xbmc
import xbmcgui
import zipfile

def all(_in, _out, dp = None):
    if dp:
        dp.create('Installing Content','Please wait...')
    if os.path.exists(_in):
        zin    = zipfile.ZipFile(_in,  'r')
        nFiles = float(len(zin.infolist()))
        count  = 0

        for item in zin.infolist():
            try:
                count += 1
                update = count / nFiles * 100
                if dp:
                    dp.update(int(update))
                zin.extract(item, _out)
        
            except Exception, e:
                xbmc.log(str(e))

        if dp:
            dp.close()

        return True