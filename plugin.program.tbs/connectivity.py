# -*- coding: utf-8 -*-

# plugin.program.tbs
# Total Revolution Maintenance (c) by whufclee (info@totalrevolution.tv)

# Total Revolution Maintenance is licensed under a
# Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.

# You should have received a copy of the license along with this
# work. If not, see http://creativecommons.org/licenses/by-nc-nd/4.0.

import requests
import koding

from koding import Network_Settings, Sleep_If_Playback_Active, String, YesNo_Dialog

isplaying = xbmc.Player().isPlaying()
Sleep_If_Playback_Active()
try:
    r    = requests.get('http://google.com')
    code = r.status_code
except:
    if YesNo_Dialog(String(30332),String(30333)):
        Network_Settings()