# -*- coding: utf-8 -*-

# plugin.program.tbs
# Total Revolution Maintenance (c) by whufclee (info@totalrevolution.tv)

# Total Revolution Maintenance is licensed under a
# Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.

# You should have received a copy of the license along with this
# work. If not, see http://creativecommons.org/licenses/by-nc-nd/4.0.

import os
import xbmc

from koding import Addon_Setting,Open_Settings,OK_Dialog,String

storage_path =  Addon_Setting('zip')
path         =  xbmc.translatePath(os.path.join(storage_path,'testfolder'))

def check(direct):
    try:
        os.makedirs(path)
        os.removedirs(path)
        OK_Dialog(String(30334),String(30335))    
        if direct!='maintenance':
            Open_Settings()
    
    except:
        OK_Dialog(String(30336),String(30337))
        Open_Settings()
        
if __name__ == '__main__':
    check('settings')