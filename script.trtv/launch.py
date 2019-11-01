#
#      Copyright (C) 2014 Sean Poyser and Richard Dean (write2dixie@gmail.com)
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

import xbmc
import xbmcaddon
import xbmcgui
import urllib
import urllib2
import socket
import os
import re
import shutil
import datetime
import download
import extract
import dixie
import filmon
import sfile
import source
import gui
import createDB
import settings


ADDON           = dixie.ADDON
HOME            = dixie.HOME
TITLE           = dixie.TITLE
VERSION         = dixie.VERSION
skin            = dixie.SKIN
addonpath       = dixie.RESOURCES
datapath        = dixie.PROFILE

SF_CHANNELS     = ADDON.getSetting('SF_CHANNELS')
showEPGonly     = ADDON.getSetting('showEPGonly')
inichansonly    = ADDON.getSetting('inichansonly')
showSFchannels  = ADDON.getSetting('showSFchannels')
add_sf_items    = ADDON.getSetting('add_sf_items')
usenanchan      = ADDON.getSetting('usenanchan')
usenancats      = ADDON.getSetting('usenancats')
image           = xbmcgui.ControlImage

chanpath        = os.path.join(datapath,   'channels')
extras          = os.path.join(datapath,   'extras')
skinfolder      = os.path.join(extras,     'skins')
dest            = os.path.join(skinfolder, 'skins.zip')
default_ini     = os.path.join(addonpath,  'addons.ini')
local_ini       = os.path.join(addonpath,  'local.ini')
current_ini     = os.path.join(datapath,   'addons.ini')
database        = os.path.join(datapath,   'program.db')
channel_xml     = os.path.join(addonpath,  'chan.xml')
xmlmaster       = os.path.join(addonpath,  'chan.xml')
catsmaster      = os.path.join(addonpath,  'cats.xml')
chanxml         = os.path.join(datapath,   'chan.xml')
catsxml         = os.path.join(datapath,   'cats.xml')
logofolder      = os.path.join(datapath,   'extras',    'logos',    'Colour Logo Pack')
#########################################################################################
def check_cats():
    dixie.log('##### CHECK CATS STARTED')
    xmlcats = []
    if os.path.exists(catsxml):
        readfile = open(catsxml,'r')
        content  = readfile.read()
        readfile.close()

# I know documentation says I should use elementtree but am doing a speed test vs regex
        channelsraw = re.compile('<cats>[\s\S]*?<\/cats>').findall(content)

        for item in channelsraw:
            category = re.compile('<category>(.+?)<\/category>').findall(item)
            category = category[0].replace('&amp;','&')
            channel  = re.compile('<channel>(.+?)<\/channel>').findall(item)
            channel  = channel[0].replace(' ','_').replace('+', '_PLUS').replace('*','STAR').replace('&amp;','&')
            xmlcats.append([channel,category])
        for item in xmlcats:
            channelpath = os.path.join(chanpath,item[0])
            if item[1] != 'Uncategorised' and os.path.exists(channelpath):
                readfile = open(channelpath,'r')
                content  = readfile.read()
                readfile.close()
                if 'Uncategorised' in content:
                    dixie.log('Editing new info... Channel: %s | Categories: %s'%(item[0],item[1]))
                    writefile = open(channelpath,'w')
                    writefile.write(content.replace('Uncategorised',item[1]))
                    writefile.close()
    else:
        dixie.log('### Not sure how that\'s happened but no cats.xml file exists! ###')
#########################################################################################
def CheckForIniChannels():
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

# Split at the = which gives us channel name then clean up
        for line in content:
            if '=' in line:
                try:
                    channel = CleanFilename(line.split('=')[0])
                    channel = channel.replace(' ','').replace('_','').replace('HD','').replace('1','ONE').replace('2','TWO').replace('3','THREE').replace('4','FOUR').replace('5','FIVE').replace('6','SIX').replace('7','SEVEN').replace('8','EIGHT').replace('9','NINE').replace('0','ZERO').replace('SPORTS','SPORT').replace('|','').replace(':','').replace('(','').replace(')','').replace('=','')
                    if len(channel) > 9:
                        channel = channel.replace('CINEMA','').replace('MOVIES','')

# If clean name is not in the ini array we add it
                    if not channel in ini_channel_array and channel != '':
                        ini_channel_array.append(channel)
                except Exception as e:
                    xbmc.log('Failed to pull channel name: %s' % e)

    return ini_channel_array
#########################################################################################
# Clean up the filename and remove chars that don't play nicely in python
def CleanFilename(text):
    text = text.replace('*', '_star')
    text = text.replace('+', '_plus')
    text = text.replace(' ', '_')

    text = re.sub('[:\\/?\<>|"]', '', text)
    text = text.strip()
    try:    text = text.encode('ascii', 'ignore')
    except: text = text.decode('utf-8').encode('ascii', 'ignore')

    return text.upper().replace('&AMP;','&').replace('&amp;','&')
#########################################################################################
# Add items in a list to the cats.xml and chan.xml files
def create_channels(sfchannels):
# Read main chan.xml into memory so we can add any new channels
    if not os.path.exists(chanxml):
        content      = ''
        writefile    = open(chanxml,'w+')
        dixie.log('### chan.xml created')
        writefile.write('<?xml version="1.0" encoding="UTF-8"?>\n<tv>\n')
    else:
        readfile     = open(chanxml,'r')
        content      = readfile.read()
        readfile.close()
        writefile    = open(chanxml,'w+')
        writefile.write(content.replace('</tv>',''))
        writefile.close()
        writefile    = open(chanxml,'a')

# Read cats.xml into memory so we can add any new channels
    if not os.path.exists(catsxml):
        content2     = ''
        writefile2   = open(catsxml,'w+')
        dixie.log('### cats.xml created')
        writefile2.write('<?xml version="1.0" encoding="UTF-8"?>\n<Document>\n')
    else:
        readfile     = open(catsxml,'r')
        content2     = readfile.read()
        readfile.close()
        writefile2    = open(catsxml,'w+')
        writefile2.write(content2.replace('</Document>',''))
        writefile2.close()
        writefile2   = open(catsxml,'a')

# Rename the items to xml friendly and loop through adding them to the xmls if they don't exist
    if len(sfchannels) > 0:
        for item in sfchannels:
            item = item.replace('_',' ').replace('_STAR',' *').replace('_PLUS',' +').replace('&', '&amp;')
# Add channel to chan.xml file
            if not '<channel id="'+item+'">' in content:
                writefile.write('  <channel id="'+item+'">\n    <display-name lang="en">'+item+'</display-name>\n  </channel>\n')
                dixie.log('Added %s to the chan.xml file' % item)
# Add channel to cats.xml file
            if not '<channel>'+item+'</channel>' in content2:
                writefile2.write(' <cats>\n    <category>Uncategorised</category>\n    <channel>'+item+'</channel>\n </cats>\n')
                dixie.log('Added %s to the cats.xml file' % item)

    writefile.write('</tv>')
    writefile.close()
    writefile2.write('</Document>')
    writefile2.close()
#########################################################################################
# Remove files from the channels folder which aren't in the channels folder
def Filter_EPG_Only():
    epg_list = createDB.Return_EPG_Only()

# If the user also wants SF items shown we add them to the array so the ordering from chan.xml isn't removed
    if add_sf_items == 'true':
        for item in os.listdir(SF_CHANNELS):
            try:
                if not item in epg_list:
                    epg_list.append(item)
            except Exception as e:
                xbmc.log('Error checking SF folder: %s' % e)

    for item in os.listdir(chanpath):
        if not item in epg_list:
            try:
                os.remove(os.path.join(chanpath,item))
            except Exception as e:
                xbmc.log('Failed to remove %s: %s' % (item, e))
#########################################################################################
# Remove files from the channels folder which aren't in the channels folder
def Filter_Valid_Ini_Only():
    tempini         = []
    temparray       = []
    final_matches   = []

# Grab a list of all channels in the channel directory and remove all formatting to make universal
    epg_list = {}
    epg_list.clear()
    for item in os.listdir(chanpath):
        newitem = item.replace(' ','').replace('_','').replace('HD','').replace('1','ONE').replace('2','TWO').replace('3','THREE').replace('4','FOUR').replace('5','FIVE').replace('6','SIX').replace('7','SEVEN').replace('8','EIGHT').replace('9','NINE').replace('0','ZERO').replace('SPORTS','SPORT').replace('|','').replace(':','').replace('(','').replace(')','').replace('=','')
        if len(newitem) > 9:
            newitem = newitem.replace('CINEMA','').replace('MOVIES','')
        epg_list[newitem] = item
        temparray.append(newitem)
    
    valid_inis = CheckForIniChannels()
    for channel in valid_inis:
        for key, value in epg_list.iteritems():
            if (channel in key) or (key in channel):
                final_matches.append(value)

# Loop through channels and remove any which don't have valid ini file matches
    for item in os.listdir(chanpath):
        real_chan = os.path.join(chanpath,item)
        sf_chan   = os.path.join(SF_CHANNELS, item)

        if not item in final_matches:
            xbmc.log('this is not in the final matches: %s' % item)

# If the option to show SF items is enabled but it's not a SF we remove those channels
            if add_sf_items == 'true' and not os.path.exists(sf_chan):
                try:
                    os.remove(real_chan)
                except:
                    xbmc.log('Failed to remove channel: %s' % item)

# If it's not in the SF list just remove it
            else:
                try:
                    os.remove(real_chan)
                except:

                    xbmc.log('Failed to remove channel: %s' % item)
#########################################################################################
# Start here, check to see if any new channels need adding
def main():
    try:
        readfile   = open(chanxml,'r')
        content    = readfile.read()
        readfile.close()
    except:
        content = ''

    channels    = re.compile('<channel id="(.+?)"').findall(content)
    totalchans  = len(channels)
    weight      = len(os.listdir(chanpath))

    for channel in channels:
        channel = channel.replace(' ','_').replace('+', '_PLUS').replace('*','STAR').replace('&amp;','&').replace('\/','&')
        filepath = os.path.join(chanpath,channel)

        if not os.path.exists(filepath):
            weight += 1
            chanlogo  = os.path.join(logofolder,'default.png')
            writefile = open(filepath,'w')
            writefile.write(channel+'\n'+channel+'\n'+chanlogo+'\n'+'\n'+'1\n'+str(weight)+'\n'+'Uncategorised\n0\n\n0\n')
            writefile.close()

# If we only want to show channels that exist in db (with EPG data)
    if showEPGonly == 'true':
        Filter_EPG_Only()

# If we only want to show channels that exist in the ini file(s)
    if inichansonly == 'true':
        Filter_Valid_Ini_Only()

# If we want to add SF items
    if add_sf_items == 'true':
        sf_check(channels,weight)

# Check to see if any new categories have been set
    check_cats()
    xbmc.executebuiltin("Dialog.Close(busydialog)")
    w = gui.TVGuide()
    w.doModal()
    del w
    xbmcgui.Window(10000).clearProperty('OTT_RUNNING')
    xbmcgui.Window(10000).clearProperty('OTT_WINDOW')
########################################################################################
# Check for super favourites that aren't yet in the EPG
def sf_check(channels,weight):
    sfchans     = []
    newchans    = []

# Grab a list of all the SF folders with a favourites.xml
    xbmc.log('### Checking for new SF folders')
    try:
        current, dirs, files = sfile.walk(SF_CHANNELS)
    except Exception, e:
        dixie.log('Error in getAllChannels - SF List: %s' % str(e))
    for dir in dirs:

# create an array of new folders not found in masterlist
        clean = CleanFilename(dir)
        dixie.log('CLEAN NAME: %s' % clean)
        if os.path.exists(os.path.join(SF_CHANNELS,dir,'favourites.xml')):
            sfchans.append(clean)
            if not clean in channels:
                newchans.append(clean)
            if dir != clean:
                try:
                    os.rename(os.path.join(SF_CHANNELS,dir),os.path.join(SF_CHANNELS,clean))
                    dixie.log('Renamed SF folder to: %s' % os.path.join(SF_CHANNELS,clean))
                except:
                    dixie.log('Failed to rename SF folder: %s' % os.path.join(SF_CHANNELS,dir))

# Create the channel files
    if len(newchans) > 0:
        for channel in newchans:
            channel = channel.replace(' ','_').replace('+', 'PLUS').replace('*','STAR').replace('&amp;','&')
            filepath = os.path.join(chanpath,channel)
            if not os.path.exists(filepath):
                weight += 1
                chanlogo  = os.path.join(logofolder,'default.png')
                writefile = open(filepath,'w')
                writefile.write(channel+'\n'+channel+'\n'+chanlogo+'\n'+'\n'+'1\n'+str(weight)+'\n'+'Uncategorised\n0\n\n0\n')
                writefile.close()
        create_channels(newchans)
##########################################################################################
def showChangelog(addonID=None):
    try:
        f     = open(ADDON.getAddonInfo('changelog'))
        text  = f.read()
        title = '%s - %s' % (xbmc.getLocalizedString(24054), ADDON.getAddonInfo('name'))

        showText(title, text)

    except:
        pass
#########################################################################################
def showText(heading, text):
    id = 10147

    xbmc.executebuiltin('ActivateWindow(%d)' % id)
    xbmc.sleep(100)

    win = xbmcgui.Window(id)

    retry = 50
    while (retry > 0):
        try:
            xbmc.sleep(10)
            retry -= 1
            win.getControl(1).setLabel(heading)
            win.getControl(5).setText(text)
            # return
        except:
            pass
#########################################################################################
xbmc.executebuiltin("ActivateWindow(busydialog)")
kodi = True
if xbmcgui.Window(10000).getProperty('OTT_KODI').lower() == 'false':
    kodi = False
xbmcgui.Window(10000).clearProperty('OTT_KODI')


#Reset Now/Next information
xbmcgui.Window(10000).setProperty('OTT_NOW_TITLE',  '')
xbmcgui.Window(10000).setProperty('OTT_NOW_TIME',   '')
xbmcgui.Window(10000).setProperty('OTT_NEXT_TITLE',  '')
xbmcgui.Window(10000).setProperty('OTT_NEXT_TIME',   '')


#Initialise the window ID that was used to launch OTT (needed for SF functionality)
xbmcgui.Window(10000).setProperty('OTT_LAUNCH_ID', str(xbmcgui.getCurrentWindowId()))

if not os.path.exists(chanxml) and usenanchan == 'true':
    dixie.log("Copying chan.xml to addon_data")
    shutil.copyfile(xmlmaster, chanxml)
else:
    dixie.log("Chan.xml file already exists in addon_data")

if not os.path.exists(catsxml) and usenancats == 'true':
    dixie.log("Copying cats.xml to addon_data")
    shutil.copyfile(catsmaster, catsxml)
else:
    dixie.log("Cats.xml file exists in addon_data")

main()

filmon.logout()