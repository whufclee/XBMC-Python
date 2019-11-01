import os, xbmc, xbmcgui, shutil, sys, re
import requests
from time import gmtime, strftime

ADDON_ID    = 'plugin.program.linktester'

HOME        = xbmc.translatePath('special://home')
ADDONS      = os.path.join(HOME, 'addons')
ADDON_DATA  = os.path.join(HOME, 'userdata','addon_data')
SF_FOLDER   = os.path.join(ADDON_DATA, 'plugin.program.super.favourites','Super Favourites','HOME_LIVE_TV')
BAD_TXT     = os.path.join(HOME, 'Need_Fixing.txt')
dp          =  xbmcgui.DialogProgress()

GOOD_LINKS  = []
BAD_LINKS   = [strftime("%Y-%m-%d %H:%M:%S", gmtime())]
ALL_LINKS   = []

def tidy(cmd):
    cmd = cmd.replace('&quot;', '')
    cmd = cmd.replace('&amp;', '&')
    cmd = removeSFOptions(cmd)

    if cmd.startswith('RunScript'):
        cmd = cmd.replace('?content_type=', '&content_type=')
        cmd = re.sub('/&content_type=(.+?)"\)', '")', cmd)

    if cmd.endswith('/")'):
        cmd = cmd.replace('/")', '")')

    if cmd.endswith(')")'):
        cmd = cmd.replace(')")', ')')

    return cmd

def removeSFOptions(cmd):
    if 'sf_options=' not in cmd:
        return cmd

    cmd = cmd.replace('?sf_options=', '&sf_options=')
    cmd = re.sub('&sf_options=(.+?)_options_sf"\)', '")',               cmd)
    cmd = re.sub('&sf_options=(.+?)_options_sf",return\)', '",return)', cmd)
    cmd = re.sub('&sf_options=(.+?)_options_sf',    '',                 cmd)
    cmd = cmd.replace('/")', '")')

    return cmd

def XML_Loop(favepath, item):
    global GOOD_LINKS
    global ALL_LINKS
    xbmc.executebuiltin('PlayerControl(Stop)')
    XML_File = open(favepath,'r')
    content  = XML_File.read().splitlines()
    XML_File.close()

# Grab each favourite and clean up into a playable link
    for line in content:
        line = line.lstrip()
        if line.startswith('<favourite name'):
            favourite = line.replace('</favourite>','').rstrip()
            favourite = favourite.split('>')
            item_name = re.compile('<favourite name="(.+?)"').findall(favourite[0])
            favourite = favourite[1]
            favourite = tidy(favourite)

# If we successfully pulled a name for this item we assign the clean name
            if len(item_name)>0:
                item_name = item_name[0]
# If no clean name was found we assign the item name to the playable path
            else:
                item_name = favourite
            xbmc.executebuiltin("XBMC.Notification("+item+","+item_name+",3000)")

            if not 'plugin.video.phstreams' in favourite:
                ALL_LINKS.append(item_name)

    # Clean up the label so we can return that to the results
                xbmc.executebuiltin('%s' % favourite)
                xbmc.sleep(1500)
     
    # Check if the progress window is active and wait for playback
                isdialog = True
                counter = 1
                while isdialog:
                    xbmc.log('### Current Window: %s' % xbmc.getInfoLabel('System.CurrentWindow'))
                    xbmc.log('### Current XML: %s' % xbmc.getInfoLabel('Window.Property(xmlfile)'))
                    xbmc.log('### Progress Dialog active, sleeping for %s seconds' % counter)
                    xbmc.sleep(1000)
                    if xbmc.getCondVisibility('Window.IsActive(progressdialog)') or (xbmc.getInfoLabel('Window.Property(xmlfile)') == 'DialogProgress.xml'):
                        isdialog = True
                    else:
                        isdialog = False
                    counter += 1
                    if counter == 10:
                        try:
                            xbmc.executebuiltin('SendClick()')
                            if dp.iscanceled():
                                dp.close()
                        except:
                            xbmc.log('### FAILED TO CLOSE DP')

                isplaying = xbmc.Player().isPlaying()
                counter   = 1
     
    # If xbmc player is not yet active give it some time to initialise
                while not isplaying and counter <10:
                    xbmc.sleep(1000)
                    isplaying = xbmc.Player().isPlaying()
                    xbmc.log('### XBMC Player not yet active, sleeping for %s seconds' % counter)
                    counter += 1

                success = 0
                counter = 0

    # If it's playing give it time to physically start streaming hten attempt to pull some info
                if isplaying:
                    xbmc.sleep(1000)
                    while not success and counter < 10:
                        try:
                            infotag = xbmc.Player().getVideoInfoTag()
                            xbmc.log('### %s infotag: %s' % (item_name, infotag))
                            vidtime = xbmc.Player().getTime()
                            xbmc.log('### time: %s' % vidtime)
                            if vidtime > 0:
                                GOOD_LINKS.append('Folder: %s  |  Item: %s' % (item, item_name))
                                success = 1

        # If playback doesn't start automatically (buffering) we force it to play
                            else:
                                xbmc.log('### Playback active but time at zero, trying to unpause')
                                xbmc.executebuiltin('PlayerControl(Play)')
                                xbmc.sleep(2000)
                                vidtime = xbmc.Player().getTime()
                                if vidtime > 0:
                                    xbmc.log('### time: %s' % vidtime)
                                    GOOD_LINKS.append('Folder: %s  |  Item: %s' % (item, item_name))
                                    success = 1

         # If no infotag or time could be pulled then we assume playback failed, try and stop the xbmc.player
                        except:
                            counter += 1
                            xbmc.sleep(1000)
                    xbmc.executebuiltin('PlayerControl(Stop)')

                if not success:
                    xbmc.executebuiltin('PlayerControl(Stop)')
                    BAD_LINKS.append('Folder: %s | %s' % (item, item_name))

# Check if the busy dialog is still active from previous locked up playback attempt
            isbusy  = xbmc.getCondVisibility('Window.IsActive(busydialog)')
            counter   = 1
            while isbusy:
                xbmc.log('### Busy dialog active, sleeping for %ss' % counter)
                xbmc.sleep(1000)
                isbusy  = xbmc.getCondVisibility('Window.IsActive(busydialog)')
                counter += 1
                if counter == 5:
                    xbmc.executebuiltin('Dialog.Close(busydialog)')

# Mute the volume, we don't want to hear any playback if running in background
xbmc.executebuiltin('Action(Mute)')

# Check playback only for SF folers that contain a favourites.xml
for item in os.listdir(SF_FOLDER):
    folderpath = os.path.join(SF_FOLDER,item)
    if os.path.isdir(folderpath):
        favepath = os.path.join(folderpath, 'favourites.xml')
        if os.path.exists(favepath):
            XML_Loop(favepath, item)

# Before continuing make sure the player has finished testing last link
is_player_active = xbmc.Player().isPlaying()
while is_player_active:
    xbmc.sleep(1000)
    is_player_active = xbmc.Player().isPlaying()

# Unmute the volume as we're now done testing playback
xbmc.executebuiltin('Action(Mute)')

# If we have a list of bad links we write them to a local file and alert user
if len(BAD_LINKS)>1:
    writefile = open(BAD_TXT,'w')
    writefile.write('THESE LINKS NEED FIXING (%s):\n\n' % strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    
    for item in BAD_LINKS:
        writefile.write('%s\n' % item)
    writefile.close()
    xbmcgui.Dialog().ok('%s BAD LINKS' % len(BAD_LINKS), 'A total of [COLOR=dodgerblue]%s[/COLOR] bad links have been found out of [COLOR=dodgerblue]%s[/COLOR] links tested.' % (len(BAD_LINKS),len(ALL_LINKS)),'','Open the [COLOR=dodgerblue]Need_Fixing.txt[/COLOR] file in the root of your kodi folder for full details.')
    badlist = '\n\n'.join(BAD_LINKS)
    badlist = badlist+'\n\nTotal Scanned: %s\nGood Links: %s\nBad Links: %s' % (len(ALL_LINKS),len(GOOD_LINKS),len(BAD_LINKS))
    r = requests.post("http://noobsandnerds.com/TI/login/playbackcheck.php", data={'badlist': badlist})
    xbmc.log('### CODE: %s   |   REASON: %s' % (r.status_code, r.reason))
    xbmc.log(r.text[:300] + '...')