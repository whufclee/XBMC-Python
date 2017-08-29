# -*- coding: utf-8 -*-

# plugin.program.tbs
# Total Revolution Maintenance (c) by whufclee (info@totalrevolution.tv)

# Total Revolution Maintenance is licensed under a
# Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.

# You should have received a copy of the license along with this
# work. If not, see http://creativecommons.org/licenses/by-nc-nd/4.0.

import os

from koding import dolog, converthex, Addon_Setting
from default import Grab_Updates, Check_My_Shares

start_option    = 'normal'
BASE            = Addon_Setting(addon_id='script.openwindow',setting='base')
mastercheck     = Addon_Setting('master')

try:
    if sys.argv[1] == 'shares' and mastercheck == 'false':
        start_option = 'shares'
except:
    start_option  = 'normal'
    
if start_option == 'shares':
    dolog('### Checking for any updated local shares')
    Check_My_Shares()

else:
    dolog('### checknews initiated, checking for updates')
    Grab_Updates(BASE+converthex('626f7865722f636f6d6d5f6c6976652e7068703f783d'),'silent')