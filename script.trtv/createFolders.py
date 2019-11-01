# TRTV Folder Generator
# Copyright (C) 2016 Lee Randall (whufclee)
#

#  I M P O R T A N T :

#  You are free to use this code under the rules set out in the license below.
#  Should you wish to re-use this code please credit whufclee for the original work.
#  However under NO circumstances should you remove this license!

#  GPL:
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
#  along with this Program; see the file LICENSE.txt.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html

import xbmcgui
import xbmcaddon
import os, re, sys
import dixie
import sfile

AddonID        =  'script.trtv'
ADDON          =  xbmcaddon.Addon(id=AddonID)
ADDON_DATA     =  xbmc.translatePath('special://profile/addon_data')
SF_CHANNELS    =  ADDON.getSetting('SF_CHANNELS')
SF_METALLIQ    =  ADDON.getSetting('SF_METALLIQ')
PROVIDER_PATH  =  os.path.join(ADDON_DATA, 'plugin.video.metalliq', 'players')
OTT_CHANNELS   =  os.path.join(dixie.GetChannelFolder(), 'channels')
dialog         =  xbmcgui.Dialog()
#--------------------------------------------------------------------------------------------------
# Create favourites.xml file for the various providers
def Create_XML(name):
    favpath   = os.path.join(name,'favourites.xml')
    writefile = open(favpath,'w+')
    writefile.write('<favourites>\n')

    channels    = name.split(os.sep)
    channelorig = channels[len(channels)-1]
    channel     = channelorig.replace('__',' +').replace('_',' ')
    if channel == '/':
        channel = channels[len(channels)-2].replace('__',' +').replace('_',' ')

    if channel[-5:-3] == ' (':
        channel    = channel[:-5]
    counter    = 0
    for item in provider_array:

# Grab add-on thumb and add to array
        thumb           = xbmc.translatePath('special://home/addons/%s/icon.png') % provider_array[counter][2]
        args            = channel+'|'+provider_array[counter][1]+'|'+provider_array[counter][2]+'|'+provider_array[counter][3]+'|'+channelorig+'|'+provider_array[counter][0]
        command         = 'RunScript(special://home/addons/script.trtv/player.py, %s)' % args
        writefile.write('\t<favourite name="%s" thumb="%s">%s</favourite>\n' % (provider_array[counter][0], thumb, command))
        counter += 1

    writefile.write('</favourites>')
    writefile.close()
#--------------------------------------------------------------------------------------------------
# Function to grab details from the provier files
def Grab_Providers():
    fail        = 0
    final_array = []

# Walk through files in the providers folder
    if os.path.exists(PROVIDER_PATH):
        current, dirs, files = sfile.walk(PROVIDER_PATH)
        for file in files:
            if fail != 1:

    # Turn each line into an array then go through the array and search for keywords
                with open(os.path.join(PROVIDER_PATH, file),'rb') as fin:
                    content     = fin.read().splitlines()
                    name        = Find_In_Lines(content, '"name"', '"')
                    repository  = Find_In_Lines(content, '"repository"', '"')
                    plugin      = Find_In_Lines(content, '"plugin"', '"')
                    playertype  = Find_In_Lines(content, '"id"', '"')

    # If this is a valid live tv provider with relevant info we add to the array
                    for line in content:
                        if '"live"' in line and '[' in line and not ']' in line and plugin != 'Unknown' and repository != 'Unknown' and repository != 'na' and name != 'Unknown' and playertype != 'Unknown':
                            final_array.append([name, repository, plugin, playertype])
    return final_array
#--------------------------------------------------------------------------------------------------
# Loop through a list of lines looking for a keyword and a separator
def Find_In_Lines(content, keyword, splitchar):
    name = 'Unknown'
    for line in content:
        if keyword in line:
            name_array = line.split(splitchar)
            try:
                name       = name_array[len(name_array)-2]
            except:
                name       = 'Unknown'
                fail       = 1
    return name
#--------------------------------------------------------------------------------------------------
silent = 0
try:
    if sys.argv[1] == 'silent':
        silent = 1
except:
    silent = 0

xbmc.log('##### SILENT = %s' % sys.argv[1])


if SF_CHANNELS == '':
    dialog.ok('SF Folder Not Set', 'No Super Favourite location has been set, please set the folder location in your settings then run again.')
else:
    provider_array  =   Grab_Providers()
    if len(provider_array) > 0:
        if SF_CHANNELS.startswith('special://'):
            SF_CHANNELS = xbmc.translatePath(SF_CHANNELS)
            
        try:
            current, dirs, files = sfile.walk(OTT_CHANNELS)
        except Exception, e:
            dixie.log('Failed to run script: %s' % str(e))
            
        if SF_METALLIQ == 'true':
            try:
                for file in files:
                    if not os.path.exists(os.path.join(SF_CHANNELS, '-metalliq', file)):
                        try:
                            os.makedirs(os.path.join(SF_CHANNELS, '-metalliq', file))
                        except:
                            dixie.log('### Failed to create folder for: %s' % str(file))
                    dixie.log('## Creating xml for: %s' % file)
                    Create_XML(os.path.join(SF_CHANNELS, '-metalliq', file))
            except:
                pass
            if not silent:
                dialog.ok(ADDON.getLocalizedString(30809),ADDON.getLocalizedString(30970))

        elif not silent:
            dialog.ok(ADDON.getLocalizedString(30809),ADDON.getLocalizedString(30810))
    else:
        dialog.ok('No Providers Found', 'No MetalliQ providers could be found.', 'Please open up your MetalliQ add-on settings and check you have the Live TV providers setup and enabled.')