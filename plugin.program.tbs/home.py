# -*- coding: utf-8 -*-

# plugin.program.tbs
# Total Revolution Maintenance (c) by TOTALREVOLUTION LTD (support@trmc.freshdesk.com)

# Total Revolution Maintenance is licensed under a
# Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.

# You should have received a copy of the license along with this
# work. If not, see http://creativecommons.org/licenses/by-nc-nd/4.0.

import binascii
import default
import koding
import os
import sys
import threading
import urllib
import xbmc
import xbmcaddon
import xbmcgui

from default import encryptme, Addon_Browser, Install_Addons, Share_Install,\
                    Share_Removal, Sleep_If_Function_Active, Toggle_Addons

from koding import  dolog, converthex, Addon_Genre, Addon_Setting, Get_Contents, Get_Addon_ID,\
                    Keyboard, List_From_Dict, Physical_Path, String, System, Text_File

if os.path.exists(xbmc.translatePath('special://home/userdata/addon_data/script.trtv/skip.txt')):
    tvgskip = 1
else:
    tvgskip = 0

dialog           = xbmcgui.Dialog()
success          = True
runcode          = ''
redirects        = xbmc.translatePath('special://home/userdata/addon_data/plugin.program.tbs/redirects')
ADDONS           = xbmc.translatePath('special://home/addons')
realname         = Addon_Setting('script.openwindow','realname')
BASE             = Addon_Setting(addon_id='script.openwindow',setting='base')
BASE2            = '687474703a2f2f6e6f6f6273616e646e657264732e636f6d2f'
settings_clean   = sys.argv[1].replace('_DIALOG_PLUS_USER','').replace('_DIALOG_USER','').replace('_EXEC_USER','').replace('_SF','')

# If it's a home menu convert addon setting into redirect file
if sys.argv[1].startswith('HOME_'):
    redirect_setting = Addon_Setting(setting=settings_clean,addon_id='plugin.program.tbs')
    if redirect_setting == 'tvg_dialog_plus':
        redirect_setting = sys.argv[1]+'_TVG_DIALOG_PLUS'
    elif redirect_setting == 'dialog_plus':
        redirect_setting = sys.argv[1]+'_DIALOG_PLUS'
    elif redirect_setting == 'dialog':
        redirect_setting = sys.argv[1]+'_DIALOG'
    elif redirect_setting == 'executable':
        redirect_setting = sys.argv[1]+'_EXEC'
    elif redirect_setting.startswith('super_faves'):
        redirect_setting = sys.argv[1]+'_SF'
    elif redirect_setting == 'dialog_plus_user':
        redirect_setting = sys.argv[1]+'_DIALOG_PLUS_USER'
    elif redirect_setting == 'dialog_user':
        redirect_setting = sys.argv[1]+'_DIALOG_USER'
    elif redirect_setting == 'executable_user':
        redirect_setting = sys.argv[1]+'_EXEC_USER'
    elif redirect_setting == '':
        redirect_setting = sys.argv[1]

# If it's a submenu and not a main home menu we use the args
else:
    redirect_setting = sys.argv[1]
dolog('REDIRECT SETTING: %s'%redirect_setting)
# Set the main redirect file
redirect_file = os.path.join(redirects, redirect_setting)

if not os.path.exists(redirects):
    os.makedirs(redirects)

# Check the contents of the redirect file
legacy_path = os.path.join(redirects,settings_clean)
if os.path.exists(redirect_file):
    runcode = Text_File(redirect_file,'r').replace('\r','')
elif os.path.exists(legacy_path):
    runcode = Text_File(legacy_path,'r').replace('\r','')

cleanname = sys.argv[1].replace("HOME_",'').replace('SUBMENU_','').replace('_DIALOG_USER','').replace('_DIALOG_PLUS_USER','').replace('_EXEC_USER','')
cleanname = cleanname.replace('DIALOG','').replace('_TVG','')
cleanname = cleanname.lower()
mymenu    = cleanname.replace('_','').replace(' ','')
if mymenu == 'xxx':
    mymenu = 'adult'
if mymenu == 'technology':
    mymenu = 'tech'
if mymenu == 'cooking':
    mymenu = 'food'
if mymenu == 'fitness':
    mymenu = 'health'
# Set the folder path to check
folderpath = xbmc.translatePath(os.path.join('special://profile/addon_data/plugin.program.super.favourites/Super Favourites/', settings_clean.replace('SUBMENU_','HOME_')))
#---------------------------------------------------------------------------------------------------
def Skin_String(menu,setting='Label'):
    final_list = {
    'comedy'       : 'Custom6HomeItem',
    'cooking'      : 'Custom3HomeItem',
    'fitness'      : 'Custom4HomeItem',
    'gaming'       : 'Custom5HomeItem',
    'kids'         : 'FavoritesHomeItem',
    'livetv'       : 'LiveTVHomeItem',
    'movies'       : 'MovieHomeItem',
    'news'         : 'ProgramsHomeItem',
    'sports'       : 'VideosHomeItem',
    'system'       : 'SettingsHomeItem',
    'technology'   : 'Custom2HomeItem',
    'travel'       : 'WeatherHomeItem',
    'tvshows'      : 'TVShowHomeItem',
    'world'        : 'PicturesHomeItem',
    'youtube'      : 'ShutdownHomeItem',
    'xxx'          : 'MusicVideoHomeItem'
    }

    home_menus = eval(Addon_Setting(addon_id='plugin.program.tbs',setting='home_menus'))
    mysettings = home_menus[menu]
    if mysettings[0].startswith('String('):
        menu_name = eval(mysettings[0])
    else:
        menu_name = mysettings[0]
    return menu_name
#---------------------------------------------------------------------------------------------------
def Add_Content(id_array):
    choice = dialog.select(String(30314),[String(30170),String(30323),String(30313),String(30354)])
    if choice >= 0:
        my_text = Text_File(redirect_file+'_CUST','r')
        if choice == 0:
            if dialog.yesno(String(30507),String(30508),yeslabel=String(30510),nolabel=String(30509)):
                addon_id = Keyboard(String(30511))
                dolog('SEARCHING ONLINE FOR: %s'%addon_id)
                Sleep_If_Function_Active(function=Install_Addons,args=[encryptme('e',addon_id)],show_busy=False,kill_time=120)
                # xbmc.executebuiltin('UpdateLocalAddons')
                Toggle_Addons(addon=addon_id)
                if xbmc.getCondVisibility('System.HasAddon(%s)'%addon_id):
                    dialog.ok(String(30334),String(30512)%addon_id)
            else:
                include_list = Addon_Browser(browser_type='list', header=String(30306), skiparray=id_array)
                for item in include_list:
                    if not my_text.endswith('\n'):
                        my_text += '\n'
                    my_text += 'addon~%s~%s\n'%(item[0],item[1])
            Text_File(redirect_file+'_CUST','w',str(my_text))
        elif choice == 1:
            myfav = Favourite_Select(my_text)
            my_text += myfav
            Text_File(redirect_file+'_CUST','w',str(my_text))
        elif choice == 2:
# List of QP modes
            full_array = [String(30318),String(30315),String(30319),String(30316),String(30320),String(30321),String(30317),String(30322)]
            qp_dict    = {
            String(30318) : 'RunScript(script.qlickplay,info=list,type=movie)',
            String(30315) : 'RunScript(script.qlickplay,info=list,type=movie,query=qqqqq)',
            String(30319) : 'RunScript(script.qlickplay,info=list,type=tv)',
            String(30316) : 'RunScript(script.qlickplay,info=list,type=tv,query=qqqqq)',
            String(30320) : 'RunScript(script.qlickplay,info=list,type=video)',
            String(30321) : 'RunScript(script.qlickplay,info=list,type=video,query=qqqqq)',
            String(30317) : 'RunScript(script.qlickplay,info=list,type=channel)',
            String(30322) : 'RunScript(script.qlickplay,info=list,type=channel,query=qqqqq)'
            }

            my_array = []

# Populate the list of QP items but don't show ones already installed
            for item in full_array:
                if not item in my_text:
                    my_array.append(item)
            
            choice = dialog.select(String(30314),my_array)
            if choice >= 0:
                my_text += '-exec~%s~%s\n'%(my_array[choice],qp_dict[my_array[choice]])
                Text_File(redirect_file+'_CUST','w',str(my_text))
        elif choice == 3:
            dolog('%s - running share_install'%settings_clean)
            Share_Install(settings_clean)
#---------------------------------------------------------------------------------------------------
def Favourite_Select(installed_content=''):
    import re
    import urllib
    import HTMLParser

    html_parser  = HTMLParser.HTMLParser()
    final_array  = []
    dialog_array = []
    favourites_path = xbmc.translatePath('special://profile/favourites.xml')
    if os.path.exists(favourites_path):
        contents = Text_File(favourites_path,'r')
        match = re.compile('<favourite name="(.+?)".+?>(.+?)<\/favourite>', re.DOTALL).findall(contents)
        for name, command in match:

            if '-fav~%s~%s\n'%(String(30326)%html_parser.unescape(name),html_parser.unescape(command)) not in installed_content:
                final_array.append('-fav~%s~%s\n'%(String(30326)%html_parser.unescape(name),html_parser.unescape(command)))
                dialog_array.append(html_parser.unescape(name))
        choice = dialog.select(String(30323),dialog_array)
        if choice >= 0:
            xbmc.log('FAV CHOICE: %s'%final_array[choice],2)
            return final_array[choice]
    else:
        dialog.ok(String(30324),String(30325))

    return ''
#---------------------------------------------------------------------------------------------------
def Remove_Content(id_array=[]):
    remove_list = []
    social_shares = False
# If Super Favourites exist add option to remove a social share
    sf_path = xbmc.translatePath('special://profile/addon_data/plugin.program.super.favourites/Super Favourites/%s'%settings_clean)
    sf_len = Get_Contents(sf_path)
    if len(sf_len)>0:
        social_shares = True
        remove_list.append(String(30354))

    my_text = Text_File(redirect_file+'_CUST','r')
    xbmc.log('redirect_file: %s'%redirect_file,2)
    for item in id_array:
        if item[0] == 'apk':
            remove_list.append(String(30304) % item[1])
        elif item[0] == 'addon':
            remove_list.append(String(30305) % item[1])
        elif item[0] == '-exec' or item[0] == '-fav':
            remove_list.append(item[1])
    choice = dialog.select(String(30307), remove_list)
    if choice >= 0:
        if remove_list[choice]!=String(30354):
            if not social_shares:
                remove_line  = '%s~%s~%s\n'%(id_array[choice][0], id_array[choice][1], id_array[choice][2])
            else:
                remove_line  = '%s~%s~%s\n'%(id_array[choice-1][0], id_array[choice-1][1], id_array[choice-1][2])
            if remove_line in my_text:
                replace_file = my_text.replace(remove_line,'')
                Text_File(redirect_file+'_CUST','w',replace_file)
            else:
                dialog.ok('DEFAULT ITEM','It\'s only possible to delete items you\'ve added, you cannot delete default items. If you want to create your own custom list set this menu as a custom list via the main +- button')
    # Social share removal
        else:
            default.Share_Removal(settings_clean)
#---------------------------------------------------------------------------------------------------
def execute(command):
    xbmc.executebuiltin(command)
#---------------------------------------------------------------------------------------------------
def showlist(usenan = False):
    from operator import itemgetter
    myapps = koding.My_Apps()
    runcode_array    = runcode.splitlines()
    delete_array     = []
    final_array      = []
    genre_array      = []
    id_array         = []
    cust_array       = []
    if os.path.exists(redirect_file+'_CUST'):
        temp_array = Text_File(redirect_file+'_CUST','r').splitlines()
        for line in temp_array:
            cust_array.append(line+'~custom')        

    sf_path = Physical_Path('special://profile/addon_data/plugin.program.super.favourites/Super Favourites/%s'%settings_clean)
    if os.path.exists(sf_path):
        for item in os.listdir(sf_path):
            fullpath = os.path.join(sf_path,item)
            if os.path.isdir(fullpath):
                genre_array.append('share~'+item.replace('_',' ')+'~'+item)
    if usenan:
        try:
            addon_list = Addon_Genre(genre=mymenu, custom_url=BASE+'addons/addon_list_new.txt')
        except:
            try:
                addon_list = Addon_Genre(genre=mymenu)
            except:
                addon_list = {}
        if addon_list:
            my_addons = Get_Contents(path=ADDONS, exclude_list=['packages','temp'],full_path=False)
            addons_matching_genre = List_From_Dict(addon_list)
            for item in my_addons:
                try:
                    addon_id = Get_Addon_ID(item)
                    if addon_id in addons_matching_genre:
                        name = koding.Cleanup_String(addon_list[addon_id])
                        genre_array.append('addon~'+name+'~'+addon_id)
                except:
                    pass
# Add genre list to our custom list    
    runcode_array += genre_array
    runcode_array += cust_array
    xbmc.log(repr(runcode_array),2)
    if 'HOME_LIVE_TV_TVG_DIALOG_PLUS' in redirect_setting:
        final_array.append(['-exec',String(code=30993,source='script.trtv'),"xbmc.executebuiltin('RunScript(special://home/addons/script.trtv/addon.py)')"])

    for line in runcode_array:
        if '~' in line:
            raw_split = line.split('~')
            app_type   = raw_split[0]
            clean_name = raw_split[1]

# Make an exception for paths which contain tilda
            raw_split.pop(0)
            raw_split.pop(0)
            app_id = ''
            for item in raw_split:
                if item != 'custom':
                    app_id += item

            if app_type == '-exec':
                final_array.append([app_type, clean_name, app_id])
                if '~custom' in line:
                    delete_array.append([app_type, clean_name, app_id])

            if app_type == 'share':
                final_array.append([app_type, clean_name, app_id])

            if app_type == '-fav':
                final_array.append([app_type, clean_name, app_id])
                if '~custom' in line:
                    delete_array.append([app_type, clean_name, app_id])

# Check the addon is installed, if it is add to the list
            if app_type == 'addon':
                try:
                    myaddon = xbmcaddon.Addon(app_id)
                    name    = myaddon.getAddonInfo('name')
                    if realname == 'true':
                        clean_name = name
                    final_array.append([app_type, clean_name, app_id])
                    if '~custom' in line:
                        delete_array.append([app_type, clean_name, app_id])
                    id_array.append(app_id)
                except:
                    pass

            if app_type == 'apk' and app_id in myapps:
                final_array.append([app_type, clean_name, app_id])

    app_array   = []
    if len(final_array) > 0:
        final_array = sorted(final_array, key=itemgetter(0,1))
        for item in final_array:
            if item[0] == 'apk':
                app_array.append(String(30304) % item[1])
            elif item[0] == 'share':
                app_array.append(String(30565) % item[1])
            elif item[0] == 'addon':
                app_array.append(String(30305) % item[1])
            elif item[0] == '-exec' or item[0] == '-fav':
                app_array.append(item[1])
        app_array.append('------------------------------')
        final_array.append(['blank','------------------------------',''])
    app_array.append(String(30301))
    final_array.append(['add',String(30301),'Add_Content(id_array=%s)'%id_array])
    app_array.append(String(30302))
    final_array.append(['remove',String(30302),'Remove_Content(id_array=%s)'%delete_array])

    choice  = dialog.select(Skin_String(cleanname.replace('_','')), app_array)
    xbmc.log('delete array: %s'%delete_array,2)
    if choice < 0:
        return
    else:
        run_app = final_array[choice]
        if run_app[0] == 'apk':
            xbmc.executebuiltin('StartAndroidActivity(%s)' % run_app[2])
        elif run_app[0] == 'addon':
            xbmc.executebuiltin('RunAddon(%s)' % run_app[2])
        elif run_app[0] == 'share':
            xbmc.executebuiltin('ActivateWindow(10001,"plugin://plugin.program.super.favourites/?folder=%s/%s",return)'%(settings_clean,urllib.quote_plus(run_app[2])))
            SF_Single_Entry()
        else:
            try:
                exec(run_app[2])
            except:
                xbmc.executebuiltin(run_app[2])
#---------------------------------------------------------------------------------------------------
def showlist_sf():
    from operator import itemgetter
    runcode_array = runcode.splitlines()
    genre_array   = []    
    final_array   = []    
    sf_path = xbmc.translatePath('special://profile/addon_data/plugin.program.super.favourites/Super Favourites/%s'%settings_clean)
    for item in os.listdir(sf_path):
        fullpath = os.path.join(sf_path,item)
        if os.path.isdir(fullpath):
            genre_array.append('share~'+item.replace('_',' ')+'~'+item)

# Add genre list to our custom list
    runcode_array += genre_array

    if 'HOME_LIVE_TV_TVG_DIALOG_PLUS' in redirect_setting:
        final_array.append(['-exec',String(code=30993,source='script.trtv'),"xbmc.executebuiltin('RunScript(special://home/addons/script.trtv/addon.py)')"])

    for line in runcode_array:
        if '~' in line:
            raw_split = line.split('~')
            app_type   = raw_split[0]
            clean_name = raw_split[1]

        # Make an exception for paths which contain tilda
            raw_split.pop(0)
            raw_split.pop(0)
            app_id = ''
            for item in raw_split:
                app_id += item

            final_array.append([app_type, clean_name, app_id])

    app_array   = []
    if len(final_array) > 0:
        final_array = sorted(final_array, key=itemgetter(0,1))
        for item in final_array:
            app_array.append(String(30565) % item[1])
        app_array.append('------------------------------')
        final_array.append(['blank','------------------------------',''])
    app_array.append(String(30301))
    final_array.append(['add',String(30301),'Share_Install("%s")'%settings_clean])
    app_array.append(String(30302))
    final_array.append(['remove',String(30302),'Share_Removal("%s")'%settings_clean])

    choice  = dialog.select(cleanname.upper().replace('_', ' '), app_array)
    if choice < 0:
        return
    else:
        run_app = final_array[choice]
        if run_app[0] == 'share':
            xbmc.executebuiltin('ActivateWindow(10001,"plugin://plugin.program.super.favourites/?folder=%s/%s",return)'%(settings_clean,run_app[2]))
            SF_Single_Entry()
        else:
            exec(run_app[2])
#---------------------------------------------------------------------------------------------------
def SF_Single_Entry():
    window = 'Home.xml'
    counter = 0
    while window != 'MyPrograms.xml' and counter < 10:
        window = xbmc.getInfoLabel('Window.Property(xmlfile)')
        xbmc.sleep(200)
        counter += 1
    xbmc.sleep(250)
    list_count = System('numitems')
    if list_count == '1':
        xbmc.executebuiltin('Action(PageDown)')
        xbmc.executebuiltin('Action(Select)')
#---------------------------------------------------------------------------------------------------
def foldercheck(path):
    directories = 0
    for dirs in os.walk(folderpath):
        directories += len(dirs[1])
    return directories
#---------------------------------------------------------------------------------------------------
def epgtools():
    from koding import String
    dialog_array     = []
    exec_array       = []
    enable_selector  = koding.Addon_Setting(setting='usecustom',addon_id='script.trtv')
    custom_config    = koding.Addon_Setting(setting='custom.config.links',addon_id='script.trtv')
    custom_reset     = koding.Addon_Setting(setting='custom.reset',addon_id='script.trtv')
    custom_settings  = koding.Addon_Setting(setting='custom.settings',addon_id='script.trtv')
    custom_update    = koding.Addon_Setting(setting='custom.update.links',addon_id='script.trtv')
    custom_url       = koding.Addon_Setting(setting='custom.url',addon_id='script.trtv')
    custom_vpn       = koding.Addon_Setting(setting='custom.vpn',addon_id='script.trtv')
    if enable_selector == 'true':
        if custom_vpn == 'true' and xbmc.getCondVisibility('System.HasAddon(service.vpn.manager)'):
            exec_array.append('xbmc.executebuiltin(\'ActivateWindow(10025,"plugin://service.vpn.manager/?toplevel",return)\')')
            dialog_array.append(String(code=30842,source='script.trtv'))
        if 'http' in custom_url:
            dialog_array.append(String(code=30829,source='script.trtv'))
            exec_array.append('xbmc.executebuiltin("RunScript(special://home/addons/plugin.program.tbs/epg.py,listings,silent)")')
        if custom_update == 'true':
            dialog_array.append(String(code=30825,source='script.trtv'))
            exec_array.append('xbmc.executebuiltin("RunScript(special://home/addons/script.trtv/updateini.py)")')
        if custom_config == 'true':
            dialog_array.append(String(code=30826,source='script.trtv'))
            exec_array.append('xbmc.executebuiltin(\'ActivateWindow(10025,"plugin://plugin.video.addons.ini.creator",return)\')')
        if custom_reset == 'true':
            dialog_array.append(String(code=30827,source='script.trtv'))
            if sys.argv[-1] == 'epg':
                exec_array.append('xbmc.executebuiltin("RunScript(special://home/addons/script.trtv/deleteDB.py,wipeEPG)");xbmc.executebuiltin("ActivateWindow(home)");xbmc.executebuiltin("StopScript(script.trtv)")')
            else:
                exec_array.append('xbmc.executebuiltin("RunScript(special://home/addons/script.trtv/deleteDB.py,wipeEPG)")')
        if custom_settings == 'true':
            dialog_array.append(String(code=30828,source='script.trtv'))
            exec_array.append('xbmc.executebuiltin("RunScript(special://home/addons/script.trtv/openSettings.py,std)")')
        if len(dialog_array) > 0:
            choice = dialog.select(String(code=30805,source='script.trtv'),dialog_array)
            if choice >=0:
                exec(exec_array[choice])
    else:
        dialog.ok(String(code=30830,source='script.trtv'),String(code=30831,source='script.trtv'))
        koding.Open_Settings(addon_id='script.trtv',focus='3.11',click=True)
#---------------------------------------------------------------------------------------------------
folders = foldercheck(folderpath)
if sys.argv[1] == "SUBMENU_EPG_TOOLS":
    if not os.path.exists(os.path.join(redirect_file,'SUBMENU_EPG_TOOLS')):
        epgtools()
        sys.exit()

# If we're opening HOME_XXX make them do the adult password check first
if settings_clean.startswith('HOME_XXX') or settings_clean.startswith('SUBMENU_XXX'):
    success = default.Adult_Filter('true','menu')

if success:

    dolog('redirect_file: %s'%redirect_file)
    dolog('redirect_setting: %s'%redirect_setting)

# Support for submenu opening into dialog
    if redirect_setting.startswith('SUBMENU') and redirect_setting.endswith('DIALOG'):
        runcode = '# Select List Use NaN'

# If no runcode exists and the item is HOME_SYSTEM
    if sys.argv[1] == 'HOME_SYSTEM' and not os.path.exists(redirect_file):
        xbmc.executebuiltin('ActivateWindow(settings)')
# Legacy support
    elif runcode.startswith('# Select List Use NaN'):
        showlist(True)
    elif runcode.startswith('# Select List'):
        showlist()

# If it's opening into the SF social sharing menu
    elif redirect_setting.endswith('_SF') or not os.path.exists(redirect_file):
        showlist_sf()
# If it's a custom dialog using NaN filtered addons
    elif redirect_setting.endswith('_DIALOG_PLUS') or redirect_setting.endswith('_DIALOG_PLUS_USER'):
        showlist(True)

# If it's a custom dialog without the NaN filtered addons
    elif redirect_setting.endswith('_DIALOG') or redirect_setting.endswith('_DIALOG_USER'):
        showlist()

# If it's an executable file
    elif redirect_setting.endswith('_EXEC') or redirect_setting.endswith('_EXEC_USER'):
        try:
            exec(runcode)
        except:
            try:
                xbmc.executebuiltin('%s'%runcode)
            except:
                pass
    else:
        try:
            exec(runcode)
        except Exception as e:
            dialog.ok('ERROR','Please contact support for help with this error:',str(e))
