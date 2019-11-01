# -*- coding: utf-8 -*-
#
#      Copyright (C) 2014 Sean Poyser and Richard Dean (write2dixie@gmail.com) - With acknowledgement to some original code by twinther (Tommy Winther)

import xbmc
import xbmcaddon
import xbmcgui
import os
import dixie
import download
import extract
import koding

ADDON           = xbmcaddon.Addon(id = 'script.trtv')
HOME            = ADDON.getAddonInfo('path')
ICON            = os.path.join(HOME, 'icon.png')
ICON            = xbmc.translatePath(ICON)
ADDONS          = xbmc.translatePath('special://home/addons')
PACKAGES        = os.path.join(ADDONS, 'packages')
SF_CHANNELS     = ADDON.getSetting('SF_CHANNELS')
CLEAN_STREAMS   = ADDON.getSetting('clean_streams')
dialog          = xbmcgui.Dialog()
dp              = xbmcgui.DialogProgress()

#---------------------------------------------------------------------------------------------------
def CheckIdle(maxIdle):
    if maxIdle == 0:
        return
    
    idle = xbmc.getGlobalIdleTime()
    if idle < maxIdle:
        return

    delay = 60
    count = delay
    dp.create("TRTV","Streaming will automatically quit in %d seconds" % count, "Press Cancel to contine viewing")
    dp.update(0)
              
    while xbmc.Player().isPlaying() and count > 0 and not dp.iscanceled():
        xbmc.sleep(1000)
        count -= 1
        perc = int(((delay - count) / float(delay)) * 100)
        if count > 1:
            dp.update(perc,"Streaming will automatically quit in %d seconds" % count, "Press Cancel to contine viewing")
        else:
            dp.update(perc,"Streaming will automatically quit in %d second" % count, "Press Cancel to contine viewing")            

    if not dp.iscanceled():
        xbmc.Player().stop()
#---------------------------------------------------------------------------------------------------
# Remove failed stream from ini files
def clean_ini(url):
    import streaming
    streamingService = streaming.StreamsService()
    ini_channel_array = []
# Grab a list of ini entries
    inifiles = streamingService.getIniFiles()
    for inifile in inifiles:
        xbmc.log('### checking ini file for streams: %s' % inifile)

# Split eaach line into array so we can grab channel names
        with open(inifile) as f:
            content = f.readlines()

        writefile = open(inifile, 'w')
        for line in content:
            if not url in line:
                writefile.write(line)
        writefile.close()
#---------------------------------------------------------------------------------------------------
def get_params(p):
    param=[]
    paramstring=p
    if len(paramstring)>=2:
        params=p
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
           params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
    return param
#---------------------------------------------------------------------------------------------------
def playSF(url):
    launchID = '10025'
    if xbmcgui.Window(10000).getProperty('OTT_LAUNCH_ID') == launchID:
        url = url.replace('ActivateWindow(%s' % launchID, 'ActivateWindow(10501')
        launchID = '10501'

    try:
        if url.startswith('__SF__'):
            url = url.replace('__SF__', '')

        if url.lower().startswith('playmedia'):
            xbmc.executebuiltin(url)
            return True, ''

        if url.lower().startswith('runscript'):
            xbmc.executebuiltin(url)
            return True, ''


        if url.lower().startswith('activatewindow'):
            import sys
            sfAddon = xbmcaddon.Addon(id = 'plugin.program.super.favourites')
            sfPath  = sfAddon.getAddonInfo('path')
            sys.path.insert(0, sfPath)

            import favourite
            import re
            import urllib

            original = re.compile('"(.+?)"').search(url).group(1)

            original = original.replace('%26', 'SF_AMP_SF') #protect '&' within parameters

            cmd = urllib.unquote_plus(original)

            try:    noFanart = favourite.removeFanart(cmd)
            except: pass

            try:    noFanart = favourite.removeSFOptions(cmd)
            except: pass

            if noFanart.endswith(os.path.sep):
               noFanart = noFanart[:-1]

            noFanart = noFanart.replace('+', '%2B')
            noFanart = noFanart.replace(' ', '+')

            url = url.replace(original, noFanart)
            url = url.replace('SF_AMP_SF', '%26') #put '&' back

            xbmc.executebuiltin(url)
            return True, ''

        import urllib
        params = url.split('?', 1)[-1]
        params = get_params(params)

        try:    mode = int(urllib.unquote_plus(params['mode']))
        except: return False, url

        if mode != 400:
            return False, url
        
        try:    path = urllib.unquote_plus(params['path'])
        except: path = None

        dirs = []
        if path:
            try:    current, dirs, files = os.walk(path).next()
            except: pass
            
            if len(dirs) == 0:
                import sys

                path = os.path.join(path, 'favourites.xml')

                sfAddon = xbmcaddon.Addon(id = 'plugin.program.super.favourites')
                sfPath  = sfAddon.getAddonInfo('path')

                sys.path.insert(0, sfPath)

                import favourite
                faves = favourite.getFavourites(path)

                if len(faves) == 1:
                    fave = faves[0][2]
                    if fave.lower().startswith('playmedia'):
                        import re
                        cmd = re.compile('"(.+?)"').search(fave).group(1)
                        return False, cmd

    except Exception, e:
        print str(e)
        pass

    url = 'ActivateWindow(%s,%s)' % (launchID, url)
    xbmc.executebuiltin(url)
    return True, ''
#---------------------------------------------------------------------------------------------------
def play(url, windowed, name=None):
    handled = False
    
    getIdle = int(ADDON.getSetting('idle').replace('Never', '0'))
    maxIdle = getIdle * 60 * 60

    dixie.SetSetting('streamURL', url)
 
    if 'tv/play_by_name_only_guide/' in url or 'movies/play_by_name_guide' in url or 'tv/play_by_name_guide/' in url:
        dixie.removeKepmap()
        xbmc.executebuiltin('XBMC.ActivateWindow(10025,%s)' % url)
        CheckIdle(maxIdle)

    else:
        dixie.loadKepmap()
    
        if url.startswith('HDTV'):
            import hdtv
            delay  = 5
            stream = hdtv.getURL(url)
            
            if not playAndWait(stream, windowed, maxIdle, delay=delay):
                dixie.SetSetting('LOGIN_HDTV', '2001-01-01 00:00:00')
                stream = hdtv.getURL(url)
                playAndWait(stream, windowed, maxIdle, delay=delay)
            return

        if url.startswith('IPLAY'):
            import iplayer
            stream = iplayer.getURL(url)
            playAndWait(stream, windowed, maxIdle)
            return

        if url.startswith('IPTV:'):
            import iptv
            url = iptv.getURL(url)
            dixie.log(url)
            xbmc.executebuiltin('XBMC.RunPlugin(%s)' % url)
            return

        if url.startswith('UKTV'):
            import uktv
            stream = uktv.getURL(url)
            dixie.log(stream)
            playAndWait(stream, windowed, maxIdle)
            return
     
        if url.isdigit():
            command = ('{"jsonrpc": "2.0", "id":"1", "method": "Player.Open","params":{"item":{"channelid":%s}}}' % url)
            xbmc.executeJSONRPC(command)
            return
        
        if (url.startswith('__SF__')) or ('plugin://plugin.program.super.favourites' in url.lower()):
            handled, url = playSF(url)
            if handled:
                return

        if not checkForAlternateStreaming(url):
            my_playback = koding.Play_Video(url)
            if not my_playback:
                if CLEAN_STREAMS == 'true':
                    clean_ini(url)
            koding.Notify(title='PLAYBACK FAILED', message='Please try another link', duration=5000)
#---------------------------------------------------------------------------------------------------
def playAndWait(url, windowed, maxIdle, delay=0):
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    playlist.add(url, xbmcgui.ListItem(''))
    try:
        xbmc.Player().play(playlist, windowed=windowed)
    except: pass

    if delay == 0:
        wait(maxIdle)
        return True

    delay *= 4
    while (delay >= 0) and (not xbmc.Player().isPlaying()):
        delay -= 1
        xbmc.sleep(250)

    if not xbmc.Player().isPlaying():
        return False
    
    wait(maxIdle)
    return True
#---------------------------------------------------------------------------------------------------
def wait(maxIdle):
    while xbmc.Player().isPlaying():
        xbmc.sleep(1000)
        CheckIdle(maxIdle)
#---------------------------------------------------------------------------------------------------
def checkForAlternateStreaming(url):
    if 'plugin.video.expattv' in url:
        return alternateStream(url)

    if 'plugin.video.filmon' in url:
        return alternateStream(url)

    if 'plugin.video.notfilmon' in url:
        return alternateStream(url)
        
    if 'plugin.video.itv' in url:        
        return alternateStream(url)
        
    if 'plugin.video.iplayerwww' in url:
        return alternateStream(url)
        
    # if 'plugin.video.uktvfrance' in url:
    #     return alternateStream(url)
        
    if 'plugin.video.muzu.tv' in url:        
        return alternateStream(url)
        
    if 'plugin.audio.ramfm' in url:        
        return alternateStream(url)
        
    if 'plugin.video.movie25' in url:
        return alternateStream(url)
        
    if 'plugin.video.irishtv' in url:
        return alternateStream(url)
        
    if 'plugin.video.F.T.V' in url:        
        return alternateStream(url)

    if 'plugin.video.sportsaholic' in url:        
        return alternateStream(url)
        
    if 'plugin.video.navi-x' in url:        
        return alternateStream(url)

    if 'plugin.video.mxnews' in url:        
        return alternateStream(url)

    if 'plugin.program.skygo.launcher' in url:        
        return alternateStream(url)

    if 'plugin.program.advanced.launcher' in url:        
        return alternateStream(url)

    if 'plugin.video.iplayer' in url:        
        return alternateStream(url)

    if 'plugin.video.stalker' in url:
        return alternateStream(url)

    if 'plugin.video.stealthplus' in url:
        return alternateStream(url)

    return False
#---------------------------------------------------------------------------------------------------
# Search text box
def Search(title, searchtext):
        keyboard = xbmc.Keyboard(searchtext, title)
        search_entered = ''
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered =  keyboard.getText()
            if search_entered == None:
                return False          
        return search_entered    
#---------------------------------------------------------------------------------------------------
def Edit_Search(channel, repository, plugin, playertype, channelorig, name):
    newname = Search('Edit Channel Name', channel)
    newarray = newname+'|'+repository+'|'+plugin+'|'+playertype+'|'+channelorig+'|'+name
    metalliq_play(newarray)
#---------------------------------------------------------------------------------------------------
def Edit_SF_Name(status, playertype, channelorig, name):
    SF_Path  = os.path.join(SF_CHANNELS, '-metalliq', channelorig, 'favourites.xml')
    readfile = open(SF_Path, 'r')
    content  = readfile.read()
    readfile.close()

    writefile = open(SF_Path, 'w')
# If playback worked mark with a tick
    if status == 'good':
        if name.startswith('[COLOR=red][B](X)[/B] [/COLOR]'):
            tempname   = name.replace('[COLOR=red][B](X)[/B] [/COLOR]', '[COLOR=lime][B](+)[/B] [/COLOR]')
            content = content.replace(name, tempname)
        elif not name.startswith('[COLOR=lime][B](+)[/B] [/COLOR]'):
            tempname   = '[COLOR=lime][B](+)[/B] [/COLOR]'+name
            content = content.replace(name, tempname)

# If playback failed mark with a cross
    if status == 'bad':
        if name.startswith('[COLOR=lime][B](+)[/B] [/COLOR]'):
            tempname   = name.replace('[COLOR=lime][B](+)[/B] [/COLOR]', '[COLOR=red][B](X)[/B] [/COLOR]')
            content = content.replace(name, tempname)
        elif not name.startswith('[COLOR=red][B](X)[/B] [/COLOR]'):
            tempname   = '[COLOR=red][B](X)[/B] [/COLOR]'+name
            content = content.replace(name, tempname)

    writefile.write(content)
    writefile.close()
    xbmc.executebuiltin('Container.Refresh')
#---------------------------------------------------------------------------------------------------
def alternateStream(url):
    # dixie.CloseBusy()
    xbmc.executebuiltin('XBMC.RunPlugin(%s)' % url)
    print '***** trtv alternateStream *****', url
    
    retries = 10
    while retries > 0 and not xbmc.Player().isPlaying():
        retries -= 1
        xbmc.sleep(1000)
        
    return True
#---------------------------------------------------------------------------------------------------
def metalliq_play(args):
    run        = 0
    windowopen = 0
    dixie.log('### metalliq play args: %s' % args)
    channel, repository, plugin, playertype, channel_orig, itemname = args.split('|')
    dixie.log('### %s' % channel)
    dixie.log('### %s' % repository)
    dixie.log('### %s' % plugin)
    dixie.log('### %s' % playertype)

# Check if add-on is installed
    try:
        addonid         = xbmcaddon.Addon(id=plugin)
        addonname       = addonid.getAddonInfo('name')
# If not then install the relevant addon
    except:
        koding.Addon_Install(addon_id=addonid,confirm=True,silent=0,repo_install=0)
# Update enabled metalliq players
        xbmc.executebuiltin('RunPlugin(plugin://plugin.video.metalliq/settings/channelers)')

    updateicon      = Addon_Info('icon')
    xbmc.executebuiltin("XBMC.Notification(Please Wait...,Searching for  [COLOR=dodgerblue]"+channel+"[/COLOR] ,5000,"+updateicon+")")
    my_playback     = koding.Play_Video('plugin://plugin.video.metalliq/live_guide/%s/None/en/%s' % (channel, playertype))
    if not my_playback:
        if dialog.yesno('Edit Search Term?','Would you like to edit the channel name? It may be this add-on has a slightly different spelling of [COLOR=dodgerblue]%s[/COLOR]' % channel):
            Edit_Search(channel, repository, plugin, playertype, channel_orig, itemname)
        else:
            Edit_SF_Name('bad', playertype, channel_orig, itemname)
    else:
        Edit_SF_Name('good', playertype, channel_orig, itemname)
#---------------------------------------------------------------------------------------------------
args = sys.argv[1]
if '|' in args:
    metalliq_play(args)

elif __name__ == '__main__':
    name = None
    if len(sys.argv) > 3:
        name = sys.argv[3]
    xbmc.log('sys[1]: %s | sys[2]: %s | sys[3]: %s' % (sys.argv[1],sys.argv[2],name))
    play(sys.argv[1], sys.argv[2] == 1, name)
