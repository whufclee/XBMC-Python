# -*- coding: utf-8 -*-

# plugin.program.tbs
# Total Revolution Maintenance (c) by whufclee (info@totalrevolution.tv)

# Total Revolution Maintenance is licensed under a
# Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.

# You should have received a copy of the license along with this
# work. If not, see http://creativecommons.org/licenses/by-nc-nd/4.0.

import koding
import xbmc
import shutil

try:
    AddonID = xbmcaddon.Addon().getAddonInfo('id')
except:
    AddonID = koding.Caller()
   
def Wipe_Settings():
    path = xbmc.translatePath('special://profile/addon_data/'+AddonID)
    shutil.rmtree(path)   
    koding.OK_Dialog(String(30338),String(30339))


if __name__ == '__main__':
    koding.Busy_Dialog()
    Wipe_Settings()
    koding.Busy_Dialog(False)
    koding.Open_Settings()