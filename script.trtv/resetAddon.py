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
import xbmcaddon
import os
import shutil
import sfile
import dixie

epgdata  = dixie.PROFILE
extras   = os.path.join(epgdata,'extras')
settings = xbmc.translatePath('special://profile/settings.bak')
hotkey   = xbmc.translatePath('special://profile/keymaps/ottv_hot.xml')


def resetAddon():
    deleteFiles()
    dixie.CloseBusy()


def deleteFiles():
    try:
        sfile.remove(settings)
        sfile.remove(hotkey)
        for item in os.listdir(epgdata):
            if item != 'extras':
                item = os.path.join(epgdata, item)
                try:
                    shutil.rmtree(item)
                    xbmc.log('### Successfully removed directory: %s' % item)
                except:
                    try:
                        os.remove(item)
                        xbmc.log('### Successfully removed file: %s' % item)
                    except:
                        xbmc.log('### Failed to remove %s' % item)

        if os.path.exists(extras):
            for item in os.listdir(extras):
                item = os.path.join(extras,item)
                try:
                    os.remove(item)
                    xbmc.log('### Successfully removed: %s' % item)
                except:
                    xbmc.log('### Failed to remove: %s' % item)

        dixie.DialogOK('TRTV successfully reset.', 'It will be recreated next time', 'you start the guide.')
        
    except Exception, e:
        error = str(e)
        dixie.log('%s :: Error resetting TRTV' % error)
        dixie.DialogOK('TRTV failed to reset.', error, 'Please restart Kodi and try again.')


if __name__ == '__main__':
    dixie.ShowBusy()
    resetAddon()