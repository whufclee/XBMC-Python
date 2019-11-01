import urllib, urllib2, xbmcgui, xbmc
#################################################
dialog         =  xbmcgui.Dialog()
#################################################
def Open_URL(url):
    req      = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link     = response.read()
    response.close()
    
    return link.replace('\r','').replace('\n','').replace('\t','')
#################################################    
isplaying = xbmc.Player().isPlaying()
if not isplaying:
    try:
        Open_URL('http://google.com')
    except:
        try:
            Open_URL('http://google.com')
        except:
            try:
                Open_URL('http://google.com')
            except:
                try:
                    Open_URL('http://google.cn')
                except:
                    try:
                        Open_URL('http://google.cn')
                    except:
                        try:
                            Open_URL('http://google.cn')
                        except:
                            dialog.ok("NOT CONNECTED",'This device is not connected to the internet','Please check your Wi-Fi settings or make sure','the ethernet cable is plugged in.')
                            
                            try:
                                xbmc.executebuiltin('RunAddon(service.openelec.settings)')
                            except:
                                pass