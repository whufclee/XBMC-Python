#
#      Copyright (C) 2014 Richard Dean
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
import xbmcgui
import xbmcaddon
import os
import sfile

import dixie

showdialogs = True

def resetChannels():
    AddonID =  'script.trtv'
    dialog  = xbmcgui.Dialog()
    path    = dixie.GetChannelFolder()
    chan    = os.path.join(path, 'channels')
    chanchk = xbmc.translatePath(os.path.join('special://profile/addon_data/',AddonID,'chan.xml'))
    catsxml = xbmc.translatePath(os.path.join('special://profile/addon_data/',AddonID,'cats.xml'))
    success = 0

    try:
        os.remove(chanchk)
    except:
        dixie.log("### IMPORTANT ### Failed to remove the chanchk file in addon_data, please manually remove if it's still there")

    if sfile.exists(chan):
        xbmc.executebuiltin('Dialog.Show(busydialog)')
        sfile.rmtree(chan)
        xbmc.executebuiltin('Dialog.Close(busydialog)')
        success = 1

    if success == 1 and showdialogs:
        dialog.ok('TRTV - Reset Channels', 'TRTV Channels successfully reset.', 'They will be re-created next time', 'you start the guide')

    if success == 0 and showdialogs:
        dialog.ok('TRTV - Reset Channels', 'There was nothing to reset, please try running the add-on again so it can repopulate your channels.')

    if os.path.exists(catsxml):
        if showdialogs:
            choice = dialog.yesno('Do You Need To Reset Categories?','It\'s highly unlikely you\'ll need to use this but if your main categories list has become corrupt it can cause problems. Would you like to reset the categories to the defaults?')
        else:
            choice = 1
        if choice == 1:
            try:
                os.remove(catsxml)
                if showdialogs:
                    dialog.ok('TRTV - Reset Categories', 'TRTV Categories successfully reset to addon defaults. Any customisations you previously had are now lost.')
            except:
                if showdialogs:
                    dialog.ok('TRTV - Reset Categories', 'There was nothing to reset, please try running the add-on again so it can repopulate your categories.')
                dixie.log("### IMPORTANT ### Unable to remove the cats.xml file in your addon_data folder. Please manually delete")
if __name__ == '__main__':
    try:
        if sys.argv[1] == 'wipeEPG':
            showdialogs = False
    except:
        showdialogs = True

    resetChannels()