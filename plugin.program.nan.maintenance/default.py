import urllib, urllib2, re, xbmcplugin, xbmcgui, xbmc, xbmcaddon
import os, sys, time, xbmcvfs, glob, shutil, datetime, zipfile, ntpath
import subprocess, threading
import yt, downloader, checkPath
import binascii
import hashlib
import speedtest
import extract
import pyxbmct.addonwindow as pyxbmct
try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database

######################################################
AddonID='plugin.program.nan.maintenance'
AddonName='NaN Maintenance'
######################################################
ADDON            =  xbmcaddon.Addon(id=AddonID)
debug            =  ADDON.getSetting('debug')
USB              =  ADDON.getSetting('zip')
dialog           =  xbmcgui.Dialog()
dp               =  xbmcgui.DialogProgress()
HOME             =  xbmc.translatePath('special://home')
USERDATA         =  xbmc.translatePath(os.path.join('special://home/userdata'))
ADDON_DATA       =  os.path.join(USERDATA,'addon_data')
DATABASE         =  os.path.join(USERDATA,'Database')
THUMBNAILS       =  os.path.join(USERDATA,'Thumbnails')
ADDONS           =  xbmc.translatePath(os.path.join('special://home','addons'))
CBADDONPATH      =  os.path.join(ADDONS,AddonID,'default.py')
FANART           =  os.path.join(ADDONS,AddonID,'fanart.jpg')
GUI              =  os.path.join(USERDATA,'guisettings.xml')
GUIFIX           =  os.path.join(USERDATA,'guifix.xml')
ARTPATH          =  'http://www.noobsandnerds.com/TI/artwork/'
defaulticon      =  os.path.join(ADDONS,AddonID,'icon_menu.png')
FAVS             =  os.path.join(USERDATA,'favourites.xml')
SOURCE           =  os.path.join(USERDATA,'sources.xml')
ADVANCED         =  os.path.join(USERDATA,'advancedsettings.xml')
PROFILES         =  os.path.join(USERDATA,'profiles.xml')
RSS              =  os.path.join(USERDATA,'RssFeeds.xml')
KEYMAPS          =  os.path.join(USERDATA,'keymaps','keyboard.xml')
CBPATH           =  os.path.join(USB,'Kodi_Backup')
tempfile         =  os.path.join(ADDON_DATA,AddonID,'temp.xml')
ascii_results    =  os.path.join(ADDON_DATA,AddonID,'ascii_results')
ascii_results1   =  os.path.join(ADDON_DATA,AddonID,'ascii_results1')
ascii_results2   =  os.path.join(ADDON_DATA,AddonID,'ascii_results2')
notifyart        =  os.path.join(ADDONS,AddonID,'resources/')
skin             =  xbmc.getSkinDir()
log_path         =  xbmc.translatePath('special://logpath/')
backup_dir       =  '/storage/backup'
restore_dir      =  '/storage/.restore/'
userdatafolder   =  os.path.join(ADDON_DATA,AddonID)
GUINEW           =  os.path.join(userdatafolder,'guinew.xml')
guitemp          =  os.path.join(userdatafolder,'guitemp')
scriptfolder     =  os.path.join(ADDON_DATA,AddonID,'scripts')
tempdbpath       =  os.path.join(USB,'Database')
packages         =  os.path.join(ADDONS,'packages')
EXCLUDES         =  ['plugin.program.nan.maintenance','addons','addon_data','userdata','sources.xml','favourites.xml']
EXCLUDES2        =  ['plugin.program.nan.maintenance','addons','addon_data','userdata','sources.xml','favourites.xml','guisettings.xml','CP_Profiles','temp']
ACTION_MOVE_UP   =  3
ACTION_MOVE_DOWN =  4
BACKUP_DIRS      =  ['/storage/.kodi','/storage/.cache','/storage/.config','/storage/.ssh']
artpath          =  os.path.join(ADDONS,AddonID,'resources')
checkicon        =  os.path.join(artpath,'check.png')
updateicon       =  os.path.join(artpath,'update.png')
unknown_icon     =  os.path.join(artpath,'update.png')
dialog_bg        =  os.path.join(artpath,'background.png')
black            =  os.path.join(artpath,'black.png')
#---------------------------------------------------------------------------------------------------
#Add a standard directory and grab fanart and iconimage from artpath defined in global variables
def addDir(type,name,url,mode,iconimage = '',fanart = '',video = '',description = ''):
    if not 'addon' in type:

        if len(iconimage) > 0:
            iconimage = ARTPATH + iconimage
        
        else:
            iconimage = defaulticon

    if 'addon' in type:
        
        if len(iconimage) > 0:
            iconimage = iconimage
        else:
            iconimage = 'DefaultFolder.png'
    
    if fanart == '':
        fanart = FANART
    
    u   = sys.argv[0]
    u += "?url="            +urllib.quote_plus(url)
    u += "&mode="           +str(mode)
    u += "&name="           +urllib.quote_plus(name)
    u += "&iconimage="      +urllib.quote_plus(iconimage)
    u += "&fanart="         +urllib.quote_plus(fanart)
    u += "&video="          +urllib.quote_plus(video)
    u += "&description="    +urllib.quote_plus(description)
        
    ok  = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    
    liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
    liz.setProperty( "Fanart_Image", fanart )
    liz.setProperty( "Build.Video", video )
    if 'folder' in type:
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    
    else:
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    
    return ok
#---------------------------------------------------------------------------------------------------
def Addon_Check_Updates():
    Update_Repo()
    xbmc.executebuiltin('ActivateWindow(10040,"addons://outdated/",return)')
#---------------------------------------------------------------------------------------------------
# Add-on removal menu
def Addon_Removal_Menu():
    namearray = []
    iconarray = []
    descarray = []
    patharray = []
    finalpath = []

    for file in os.listdir(ADDONS):
        if os.path.isdir(os.path.join(ADDONS,file)) and os.path.exists(os.path.join(ADDONS,file,'addon.xml')):

# Read contents of addon.xml to memory and grab REAL addon id (for those who's folder names differ)
            readfile    = open(os.path.join(ADDONS,file,'addon.xml'), 'r')
            content     = readfile.read()
            readfile.close()
            tempaddonid = re.compile('id="(.+?)"').findall(content)[0]

            Addon       = xbmcaddon.Addon(tempaddonid)
            addontype   = Addon.getAddonInfo('type').replace('xbmc.','')
            name        = Addon.getAddonInfo('name')
            iconimage   = Addon.getAddonInfo('icon')
            description = Addon.getAddonInfo('description')
            filepath    = os.path.join(ADDONS,file)

            namearray.append('[COLOR=gold]%s:[/COLOR]  %s' % (addontype,name))
            iconarray.append(iconimage)
            descarray.append(description)
            patharray.append(filepath)

    finalarray = multiselect('Add-ons To Fully Remove',namearray,iconarray,descarray)
    for item in finalarray:
        newpath = patharray[item]
        newname = namearray[item]
        finalpath.append([newname,newpath])
    if len(finalpath) > 0:
        Remove_Addons(finalpath)
#-----------------------------------------------------------------------------------------------------------------
#Function to open addon settings
def Addon_Settings():
    ADDON.openSettings(sys.argv[0])
    xbmc.executebuiltin('Container.Refresh')
#-----------------------------------------------------------------------------------------------------------------
# Enable/disable the visibility of adult add-ons (use true or false)
def Adult_Filter(value):
    master_list = Open_URL('http://noobsandnerds.com/TI/AddonPortal/adult.php',10)
    id_list     = re.compile('i="(.+?)"').findall(master_list)

    for addon_id in id_list:
        addon_id = '"%s"' % addon_id
        query = '{"jsonrpc":"2.0", "method":"Addons.SetAddonEnabled","params":{"addonid":%s,"enabled":%s}, "id":1}' % (addon_id, value)
        response = xbmc.executeJSONRPC(query)
        xbmc.log(query)
        xbmc.log('### RETURN %s' % response)

    if value == 'false':
        filter_type = 'disabled'
    else:
        filter_type = 'enabled'
    dialog.ok('ADULT CONTENT %s' % filter_type.upper(), 'Your adult rated add-ons have now been %s' % filter_type)
#-----------------------------------------------------------------------------------------------------------------
def Android_Path_Check():
    content = Grab_Log()
    localstorage  = re.compile('External storage path = (.+?);').findall(content)
    localstorage  = localstorage[0] if (len(localstorage) > 0) else ''
    return localstorage
#-----------------------------------------------------------------------------------------------------------------
# Zip up the contents of a directory and all subdirectories, this will exclude the global excludes files such as guisettings.xml
def Archive_Tree(sourcefile, destfile, message_header, message1, message2, message3, exclude_dirs, exclude_files):
    zipobj       = zipfile.ZipFile(destfile , 'w', zipfile.ZIP_DEFLATED)
    rootlen      = len(sourcefile)
    for_progress = []
    ITEM         =[]
    
    dp.create(message_header, message1, message2, message3)
    
    for base, dirs, files in os.walk(sourcefile):
        
        for file in files:
            ITEM.append(file)
    
    N_ITEM =len(ITEM)
    
    for base, dirs, files in os.walk(sourcefile):
        
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        files[:] = [f for f in files if f not in exclude_files and not 'crashlog' in f and not 'stacktrace' in f]
        
        for file in files:
            
            try:
                for_progress.append(file) 
                progress = len(for_progress) / float(N_ITEM) * 100  
                dp.update(0,"Backing Up",'[COLOR yellow]%s[/COLOR]'%d, 'Please Wait')
                fn = os.path.join(base, file)
            
            except:
                xbmc.log("### Failed to backup %s" % file)
            
            if not 'temp' in dirs:
                
                if not AddonID in dirs:
                    
                    try:
                       FORCE= '01/01/1980'
                       FILE_DATE=time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(fn)))
                       
                       if FILE_DATE > FORCE:
                           zipobj.write(fn, fn[rootlen:])  
                    
                    except:
                        xbmc.log("Unable to backup file: %s" % file)
    
    zipobj.close()
    dp.close()
#---------------------------------------------------------------------------------------------------
# Zip up tree, essentially the same as above but doesn't exclude global excludes (such as guisettings & profiles)
def Archive_File(sourcefile, destfile):
    zipobj       = zipfile.ZipFile(destfile , 'w', zipfile.ZIP_DEFLATED)
    rootlen      = len(sourcefile)
    for_progress = []
    ITEM         = []
    
    dp.create("Backing Up Files","Archiving...",'', 'Please Wait')
    
    for base, dirs, files in os.walk(sourcefile):
        
        for file in files:
            ITEM.append(file)
    
    N_ITEM =len(ITEM)
    
    for base, dirs, files in os.walk(sourcefile):
        
        for file in files:
            for_progress.append(file) 
            progress = len(for_progress) / float(N_ITEM) * 100  
            dp.update(int(progress),"Backing Up",'[COLOR yellow]%s[/COLOR]'%file, 'Please Wait')
            fn       = os.path.join(base, file)
            
            if not 'temp' in dirs:
                
                if not AddonID in dirs:
                   
                   import time
                   FORCE= '01/01/1980'
                   FILE_DATE=time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(fn)))
                   
                   if FILE_DATE > FORCE:
                       zipobj.write(fn, fn[rootlen:])  
    zipobj.close()
    dp.close()
#---------------------------------------------------------------------------------------------------
# Check for non ascii files and folders
def ASCII_Check():
    sourcefile   = dialog.browse(3, 'Select the folder you want to scan', 'files', '', False, False)
    rootlen      = len(sourcefile)
    for_progress = []
    ITEM         = []
                
    dp.create('Checking File Structure','','Please wait...','')

    choice = dialog.yesno('Delete or Scan?','Do you want to delete all filenames with special characters or would you rather just scan and view the results in the log?',yeslabel='Delete',nolabel='Scan')
# Create temp files to store the deletion results in
    successascii = open(ascii_results1, mode='w+')
    failedascii  = open(ascii_results2, mode='w+')

    for base, dirs, files in os.walk(sourcefile):
        
        for file in files:
            ITEM.append(file)
    
    N_ITEM =len(ITEM)
    
    for base, dirs, files in os.walk(sourcefile):
        
        dirs[:] = [d for d in dirs]
        files[:] = [f for f in files]
        
        for file in files:

            for_progress.append(file) 
            progress = len(for_progress) / float(N_ITEM) * 100  
            dp.update(0,"Checking for non ASCII files",'[COLOR yellow]%s[/COLOR]'%d, 'Please Wait')
            
            try:
                file.encode('ascii')

            except UnicodeDecodeError:
                badfile = (str(base)+'/'+str(file)).replace('\\','/').replace(':/',':\\')
#                badfile = unicodedata.normalize('NFKD',unicode(badfile,"ISO-8859-1")).encode("ascii","ignore")
                print " non-ASCII file status logged successfully: " + badfile
                if choice != 1:
                    successascii.write('[COLOR=dodgerblue]Non-ASCII File:[/COLOR]\n')
                    for chunk in Chunks(badfile, 75):
                        successascii.write(chunk+'[CR]')
                    successascii.write('\n')
                if choice == 1:
                    try:
                        os.remove(badfile)
                        xbmc.log("### SUCCESS - deleted %s" % badfile)
                        successascii.write('[COLOR=dodgerblue]SUCCESSFULLY DELETED:[/COLOR]\n')
                        for chunk in Chunks(badfile, 75):
                            successascii.write(chunk+'[CR]')
                        successascii.write('\n')
                        
                    except:
                        xbmc.log("######## FAILED TO REMOVE: %s" % badfile)
                        xbmc.log("######## Make sure you manually remove this file ##########")
                        failedascii.write('[COLOR=red]FAILED TO DELETE:[/COLOR]\n')
                        for chunk in Chunks(badfile, 75):
                            failedascii.write(chunk+'[CR]')
                        failedascii.write('\n')

    failedascii.close()
    successascii.close()

# Create final results by merging success and failed together
    successascii = open(ascii_results1, mode='r')
    successcontent = successascii.read()
    successascii.close()
    failedascii = open(ascii_results2, mode='r')
    failedcontent = failedascii.read()
    failedascii.close()
    if successcontent == '' and failedcontent == '':
        dialog.ok('No Special Characters Found','Great news, all filenames in the path you scanned are ASCII based - no special characters found.' )
    else:
        finalresults = open(ascii_results, mode='w+')
        finalresults.write(successcontent+'\n\n'+failedcontent)
        finalresults.close()
        results = open(ascii_results, mode='r')
        resultscontent = results.read()
        results.close()
        Text_Boxes('Final Results',resultscontent)
        os.remove(ascii_results)
    os.remove(ascii_results1)
    os.remove(ascii_results2)
#---------------------------------------------------------------------------------------------------
# Create backup menu
def Backup_Option():
    addDir('','Backup Addons Only','addons','restore_zip','','','','Back Up Your Addons')
    addDir('','Backup Addon Data Only','addon_data','restore_zip','','','','Back Up Your Addon Userdata')
    addDir('','Backup Guisettings.xml',GUI,'restore_backup','','','','Back Up Your guisettings.xml')
    
    if os.path.exists(FAVS):
        addDir('','Backup Favourites.xml',FAVS,'restore_backup','Backup.png','','','Back Up Your favourites.xml')
    
    if os.path.exists(SOURCE):
        addDir('','Backup Source.xml',SOURCE,'restore_backup','Backup.png','','','Back Up Your sources.xml')
    
    if os.path.exists(ADVANCED):
        addDir('','Backup Advancedsettings.xml',ADVANCED,'restore_backup','Backup.png','','','Back Up Your advancedsettings.xml')
    
    if os.path.exists(KEYMAPS):
        addDir('','Backup Advancedsettings.xml',KEYMAPS,'restore_backup','Backup.png','','','Back Up Your keyboard.xml')
    
    if os.path.exists(RSS):
        addDir('','Backup RssFeeds.xml',RSS,'restore_backup','Backup.png','','','Back Up Your RssFeeds.xml')
#---------------------------------------------------------------------------------------------------
#Backup/Restore root menu
def Backup_Restore():
    addDir('folder','Backup My Content','none','backup_option','Backup.png','','','')
    addDir('folder','Restore My Content','none','restore_option','Restore.png','','','')
#---------------------------------------------------------------------------------------------------
#Browse pre-installed repo's via the kodi add-on browser
def Browse_Repos():
    xbmc.executebuiltin('ActivateWindow(10040,"addons://repos/",return)')
#---------------------------------------------------------------------------------------------------
# Gotham to helix skin function for keyboard fix, thanks to xunity maintenance for this code
def changekeys(skin):
    left       = '<onleft>%s</onleft>'
    right      = '<onright>%s</onright>'
    up         = '<onup>%s</onup>'
    down       = '<ondown>%s</ondown>'
    button     = '<control type="button" id="%s">'    

# New keyboard letter codes
    LETTER     = [
        ('65','140'),
        ('66','164'),
        ('67','162'),
        ('68','142'),
        ('69','122'),
        ('70','143'),
        ('71','144'),
        ('72','145'),
        ('73','127'),
        ('74','146'),
        ('75','147'),
        ('76','148'),
        ('77','166'),
        ('78','165'),
        ('79','128'),
        ('80','129'),
        ('81','120'),
        ('82','123'),
        ('83','141'),
        ('84','124'),
        ('85','126'),
        ('86','163'),
        ('87','121'),
        ('88','161'),
        ('89','125'),
        ('90','160')]
    
    for old , new in LETTER:
        a      = open(skin).read()  
        CHANGE = a.replace(button%old,button%new).replace(left%old,left%new).replace(right%old,right%new).replace(up%old,up%new).replace(down%old,down%new)
        f      = open(skin, mode='w')
        f.write(CHANGE)
        f.close()   
#---------------------------------------------------------------------------------------------------
def changenumber(u,skin):
    left   = '<onleft>%s</onleft>'
    right  = '<onright>%s</onright>'
    up     = '<onup>%s</onup>'
    down   = '<ondown>%s</ondown>'
    button = '<control type="button" id="%s">'
    
    if u < 49:
        NEW=u+ 61
    
    else:    
        NEW=u+ 51
    
    a       = open(skin).read()
    CHANGE  = a.replace(left%u,left%NEW).replace(right%u,right%NEW).replace(up%u,up%NEW).replace(down%u,down%NEW).replace(button%u,button%NEW)
    f       = open(skin, mode='w')
    f.write(CHANGE)
    f.close()
#-----------------------------------------------------------------------------------------------------------------
# Function to check the download path set in settings
def Check_Download_Path():
    path = os.path.join(USB,'testCBFolder')
    
    if not os.path.exists(USB):
        dialog.ok('Download/Storage Path Check','The download location you have stored does not exist .\nPlease update the addon settings and try again.') 
        ADDON.openSettings(sys.argv[0])
#---------------------------------------------------------------------------------------------------
# Check the storage path that's set in settings is actually writeable
def CheckPath():
    path = os.path.join(USB,'testCBFolder')
    
    try:
        os.makedirs(path)
        os.removedirs(path)
        dialog.ok('[COLOR=lime]SUCCESS[/COLOR]', 'Great news, the path you chose is writeable.', 'Some of these builds are rather big, we recommend a minimum of 1GB storage space.')
    
    except:
        dialog.ok('[COLOR=red]CANNOT WRITE TO PATH[/COLOR]', 'Kodi cannot write to the path you\'ve chosen. Please click OK in the settings menu to save the path then try again. Some devices give false results, we recommend using a USB stick as the backup path.')
#---------------------------------------------------------------------------------------------------
# Split string into arrays
def Chunks(s, n):
    for start in range(0, len(s), n):
        yield s[start:start+n]
#---------------------------------------------------------------------------------------------------
# Attempt to wipe the cache folder and purge addons*.db
def Clean_Addons():
    tempdir = xbmc.translatePath('special://temp')
    try:
        shutil.rmtree(tempdir)
    except:
        for item in os.listdir(tempdir):
            path = os.path.join(tempdir, item)
            try:
                os.remove(path)
            except:
                try:
                    shutil.rmtree(path)
                except:
                    xbmc.log('#### Failed to remove: %s' % path)
#---------------------------------------------------------------------------------------------------
# Function to clean HTML into plain text. Not perfect but it's better than raw html code!
def Clean_HTML(data):        
    data = data.replace('</p><p>','[CR][CR]').replace('&ndash;','-').replace('&mdash;','-').replace("\n", " ").replace("\r", " ").replace("&rsquo;", "'").replace("&rdquo;", '"').replace("</a>", " ").replace("&hellip;", '...').replace("&lsquo;", "'").replace("&ldquo;", '"')
    data = " ".join(data.split())   
    p    = re.compile(r'< script[^<>]*?>.*?< / script >')
    data = p.sub('', data)
    p    = re.compile(r'< style[^<>]*?>.*?< / style >')
    data = p.sub('', data)
    p    = re.compile(r'')
    data = p.sub('', data)
    p    = re.compile(r'<[^<]*?>')
    data = p.sub('', data)
    data = data.replace('&nbsp;',' ')
    return data
#---------------------------------------------------------------------------------------------------
# THIS IS A WIP, NOWHERE NEAR COMPLETE - JUST A PLACEHOLDER FOR THE REAL CODE
def Cleanup_Old_Addons(addon_ids):
    path           = xbmc.translatePath('special://home/userdata/Database')
    files          = glob.glob(os.path.join(path, 'Addons*.db'))
    ver            = 0
    dbPath         = ''

# Find the highest version number of database
    for file in files:
        dbversion = int(re.compile('Addons(.+?).db').findall(file)[0])
        if ver < dbversion:
            ver     = dbversion
            dbPath  = file

    db   = xbmc.translatePath(dbPath)
    conn = database.connect(db, timeout = 10, detect_types=database.PARSE_DECLTYPES, check_same_thread = False)
    conn.row_factory = database.Row
    c = conn.cursor()

    for id in addon_ids:
        c.execute("DELETE * FROM addons WHERE addonID = ?", (id,))
        xbmc.log('### Removed %s from addons' % id)

    c.execute("VACUUM")
    conn.commit()
    c.close()
#---------------------------------------------------------------------------------------------------
# Thanks to xunity maintenance tool for this code.
# It has been slightly edited and will remove old textures not used in past 14 days
def Cleanup_Old_Textures():
    path           = xbmc.translatePath('special://home/userdata/Database')
    files          = glob.glob(os.path.join(path, 'Textures*.db'))
    ver            = 0
    dbPath         = ''

# Find the highest version number of textures, it's always been textures13.db but you can never be too careful!
    for file in files:
        dbversion = int(re.compile('extures(.+?).db').findall(file)[0])
        if ver < dbversion:
            ver     = dbversion
            dbPath  = file

    db   = xbmc.translatePath(dbPath)
    conn = database.connect(db, timeout = 10, detect_types=database.PARSE_DECLTYPES, check_same_thread = False)
    conn.row_factory = database.Row
    c = conn.cursor()

# Set paramaters to check in db, cull = the datetime (we've set it to 14 days) and useCount is the amount of times the file has been accessed
    cull     = datetime.datetime.today() - datetime.timedelta(days = 14)
    useCount = 10

# Create an array to store paths for images and ids for database
    ids    = []
    images = []

    c.execute("SELECT idtexture FROM sizes WHERE usecount < ? AND lastusetime < ?", (useCount, str(cull)))

    for row in c:
        ids.append(row["idtexture"])

    for id in ids:
        c.execute("SELECT cachedurl FROM texture WHERE id = ?", (id,))
        for row in c:
            images.append(row["cachedurl"])

    print "### Community Portal Automatic Cache Removal: %d Old Textures removed" % len(images)

# Clean up database
    for id in ids:       
        c.execute("DELETE FROM sizes   WHERE idtexture = ?", (id,))
        c.execute("DELETE FROM texture WHERE id        = ?", (id,))

    c.execute("VACUUM")
    conn.commit()
    c.close()

    #delete files
    thumbfolder = xbmc.translatePath('special://home/userdata/Thumbnails')
    for image in images:
        path = os.path.join(thumbfolder, image)
        try:
            os.remove(path)
        except:
            pass
#---------------------------------------------------------------------------------------------------
# Function to clear all known cache files
def Clear_Cache():
    choice = xbmcgui.Dialog().yesno('Clear All Known Cache?', 'This will clear all known cache files and can help if you\'re encountering kick-outs during playback as well as other random issues. There is no harm in using this.', nolabel='Cancel',yeslabel='Delete')
    
    if choice == 1:
        Wipe_Cache()
        Remove_Textures_Dialog()
#---------------------------------------------------------------------------------------------------
# OLD METHOD to create a community (universal) backup - this renames paths to special:// and removes unwanted folders
def Community_Backup_OLD():
    guisuccess=1
    Check_Download_Path()
    choice = dialog.yesno('Are you sure?!!!','This is method is very dated and is only left here for LOCAL installs. For online backups you really should be using the NaN backup option which creates a much smaller file and allows for a much more reliable install process.')
    if choice == 0:
        return
    fullbackuppath  = os.path.join(CBPATH,'My_Builds','')
    myfullbackup    = os.path.join(CBPATH,'My_Builds','my_full_backup.zip')
    
    if not os.path.exists(fullbackuppath):
        os.makedirs(fullbackuppath)
    
    vq = Get_Keyboard( heading="Enter a name for this backup" )
    if ( not vq ):
        return False, 0
    
    title              = urllib.quote_plus(vq)
    backup_zip         = xbmc.translatePath(os.path.join(fullbackuppath,title+'.zip'))
    exclude_dirs_full  =  [AddonID]
    exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf','Thumbs.db','.gitignore']
    exclude_dirs       =  [AddonID, 'cache', 'system', 'Thumbnails', "peripheral_data",'library','keymaps']
    exclude_files      = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log","Textures13.db",'.DS_Store','.setup_complete','XBMCHelper.conf', 'advancedsettings.xml','Thumbs.db','.gitignore']
    message_header     = "Creating full backup of existing build"
    message_header2    = "Creating Community Build"
    message1           = "Archiving..."
    message2           = ""
    message3           = "Please Wait"
    
    choice = xbmcgui.Dialog().yesno("Do you want to include your addon_data folder?", 'This contains ALL addon settings including passwords but may also contain important information such as skin shortcuts. We recommend MANUALLY removing the addon_data folders that aren\'t required.', yeslabel='Yes',nolabel='No')
    
    if choice == 0:
        exclude_dirs = [AddonID, 'cache', 'system', 'peripheral_data','library','keymaps','addon_data','Thumbnails']

    elif choice == 1:
        pass
    
    Fix_Special(HOME)
    Delete_Packages()
    Archive_Tree(HOME, backup_zip, message_header2, message1, message2, message3, exclude_dirs, exclude_files)  
    time.sleep(1)

    GUIname = xbmc.translatePath(os.path.join(fullbackuppath, title+'_guisettings.zip'))
    zf      = zipfile.ZipFile(GUIname, mode='w')
    
    try:
        zf.write(GUI, 'guisettings.xml', zipfile.ZIP_DEFLATED) #Copy guisettings.xml
    except:
        guisuccess=0
    
    try:
        zf.write(xbmc.translatePath(os.path.join(HOME,'userdata','profiles.xml')), 'profiles.xml', zipfile.ZIP_DEFLATED) #Copy profiles.xml
    except:
        pass
    
    zf.close()
        
    if guisuccess == 0:
        dialog.ok("FAILED!", 'The guisettings.xml file could not be found on your system, please reboot and try again.', '','')
        
    else:
        dialog.ok("SUCCESS!", 'You Are Now Backed Up. Remember this should only be used for local backup purposes and is not recommended for sharing online. Use the far superior NaN CP backup method for online use.')
        dialog.ok("Build Location", 'Universal Backup:[CR][COLOR=dodgerblue]'+backup_zip+'[/COLOR]')
#---------------------------------------------------------------------------------------------------
# Open a database
def DB_Open(db_path):
    global cur
    global con
    con = database.connect(db_path)
    cur = con.cursor()
#-----------------------------------------------------------------------------------------------------------------
# Function to delete the userdata/addon_data folder
def DeleteAddonData():
    addon_data_path = xbmc.translatePath(os.path.join('special://home/userdata/addon_data', ''))
    
    for root, dirs, files in os.walk(addon_data_path):
        file_count = 0
        file_count += len(files)
        
        if file_count >= 0:
            
            for f in files:
                os.unlink(os.path.join(root, f))
            
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))        
#---------------------------------------------------------------------------------------------------
# Function to delete crash logs
def Delete_Logs():  
    for infile in glob.glob(os.path.join(log_path, 'xbmc_crashlog*.*')):
         File   = infile
         os.remove(infile)
         dialog = xbmcgui.Dialog()
         dialog.ok("Crash Logs Deleted", "Your old crash logs have now been deleted.")
#-----------------------------------------------------------------------------------------------------------------    
# Function to delete the packages folder
def Delete_Packages():
    packages_cache_path = xbmc.translatePath(os.path.join('special://home/addons/packages', ''))
    
    for root, dirs, files in os.walk(packages_cache_path):
        file_count = 0
        file_count += len(files)
        
        if file_count > 0:
            
            for f in files:
                os.unlink(os.path.join(root, f))
            
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
#---------------------------------------------------------------------------------------------------
# Function to wipe path
def Delete_Path(path):
    choice = dialog.yesno('Are you certain?','This will completely wipe this folder, are you absolutely certain you want to continue? There is NO going back after this!')
    if choice == 1:
        dp.create("[COLOR=orange]noobs[/COLOR][COLOR=dodgerblue]and[/COLOR][COLOR=orange]nerds[/COLOR]","Wiping...",'', 'Please Wait')
        shutil.rmtree(path, ignore_errors=True)
        dp.close()
        xbmc.executebuiltin('container.Refresh')
#-----------------------------------------------------------------------------------------------------------------  
# Function to delete the userdata/addon_data folder
def Delete_Userdata():
    addon_data_path = xbmc.translatePath(os.path.join('special://home/userdata/addon_data', ''))
    
    for root, dirs, files in os.walk(addon_data_path):
        file_count = 0
        file_count += len(files)
        
        if file_count >= 0:
            
            for f in files:
                os.unlink(os.path.join(root, f))
            
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
#-----------------------------------------------------------------------------------------------------------------  
# Function to do a full wipe.
def Destroy_Path(path):
    dp.create("[COLOR=orange]noobs[/COLOR][COLOR=dodgerblue]and[/COLOR][COLOR=orange]nerds[/COLOR]","Wiping...",'', 'Please Wait')
    shutil.rmtree(path, ignore_errors=True)
#---------------------------------------------------------------------------------------------------
# Convert physical paths to special paths
def Fix_Special(url):
    dp.create("Changing Physical Paths To Special","Renaming paths...",'', 'Please Wait')
    for root, dirs, files in os.walk(url):  #Search all xml files and replace physical with special
        for file in files:
            if file.endswith(".xml") or file.endswith(".hash") or file.endswith("properies"):
                dp.update(0,"Fixing",file, 'Please Wait')
                a = open((os.path.join(root, file))).read()
                encodedpath  = urllib.quote(HOME)
                encodedpath2  = urllib.quote(HOME).replace('%3A','%3a').replace('%5C','%5c')
                b = a.replace(HOME, 'special://home/').replace(encodedpath, 'special://home/').replace(encodedpath2, 'special://home/')
                f = open((os.path.join(root, file)), mode='w')
                f.write(str(b))
                f.close()
#---------------------------------------------------------------------------------------------------
# Clean up all known cache files
def Full_Clean():
    size                      = 0
    atv2_cache_a              = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
    atv2_cache_b              = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')        
    downloader_cache_path     = os.path.join(xbmc.translatePath('special://profile/addon_data/script.module.simple.downloader'), '')
    imageslideshow_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/script.image.music.slideshow/cache'), '')
    iplayer_cache_path        = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.iplayer/iplayer_http_cache'), '')
    itv_cache_path            = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.itv/Images'), '')
    navix_cache_path          = os.path.join(xbmc.translatePath('special://profile/addon_data/script.navi-x/cache'), '')
    phoenix_cache_path        = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.phstreams/Cache'), '')
    ramfm_cache_path          = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.audio.ramfm/cache'), '')
    wtf_cache_path            = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.whatthefurk/cache'), '')
    genesisCache              = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.genesis'), 'cache.db')
    tempdir                   = os.path.join(HOME,'temp')
    dp.create('Calculating Used Space','','Please wait','')

# For more accurate info we need to add a loop to only check folders with cache in the name. Actual wipe does this but getsize does not.
    if os.path.exists(atv2_cache_a):
        size = Get_Size(atv2_cache_a,size)
    if os.path.exists(atv2_cache_b):
        size = Get_Size(atv2_cache_b,size)
    if os.path.exists(downloader_cache_path):
        size = Get_Size(downloader_cache_path,size)
    if os.path.exists(imageslideshow_cache_path):
        size = Get_Size(imageslideshow_cache_path,size)
    if os.path.exists(iplayer_cache_path):
        size = Get_Size(iplayer_cache_path,size)
    if os.path.exists(itv_cache_path):
        size = Get_Size(itv_cache_path,size)
    if os.path.exists(navix_cache_path):
        size = Get_Size(navix_cache_path,size)
    if os.path.exists(phoenix_cache_path):
        size = Get_Size(phoenix_cache_path,size)
    if os.path.exists(ramfm_cache_path):
        size = Get_Size(ramfm_cache_path,size)
    if os.path.exists(wtf_cache_path):
        size = Get_Size(wtf_cache_path,size)
    if os.path.exists(genesisCache):
        size = Get_Size(genesisCache,size)
    if os.path.exists(tempdir):
        size = Get_Size(tempdir,size)
    size = Get_Size(THUMBNAILS,size)
    size = Get_Size(packages,size)/1000000
    choice = dialog.yesno('Results','You can free up [COLOR=dodgerblue]'+str(size)+'MB[/COLOR] of space if you run this cleanup program. Would you like to run the cleanup procedure?')
    if choice == 1:
        Wipe_Cache()
        try:
            shutil.rmtree(packages)
        except:
            pass
        choice = dialog.yesno('Thumbnail Cleanup','We highly recommend only wiping your OLD unused thumbnails. Do you want to clear just the old ones or all thumbnails?',yeslabel='ALL',nolabel='OLD ONLY')
        if choice == 1:
            Remove_Textures()
            Destroy_Path(THUMBNAILS)
            Kill_XBMC()
        else:
            Cleanup_Old_Textures()
#---------------------------------------------------------------------------------------------------
# Bring up a keyboard and return the input
def Get_Keyboard( default="", heading="", hidden=False ):
    keyboard = xbmc.Keyboard( default, heading, hidden )
    keyboard.doModal()
    if ( keyboard.isConfirmed() ):
        return unicode( keyboard.getText(), "utf-8" )
    return default
#-----------------------------------------------------------------------------------------------------------------  
def Get_Last_Error():
    import traceback
 #   errorstring = traceback.format_exc()
    errorstring = traceback.print_exc()
    xbmc.log('### ERROR STRING: %s' % errorstring)
#---------------------------------------------------------------------------------------------------
# Send a path and an initial size to increment to and it will scan total file sizes of all subfolders
def Get_Size(path,size):
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            dp.update(0,"Calculating...",'[COLOR=dodgerblue]'+f+'[/COLOR]', 'Please Wait')
            fp = os.path.join(dirpath, f)
            size += os.path.getsize(fp)
    return size
#---------------------------------------------------------------------------------------------------
# Get params and clean up into string or integer
def Get_Params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param
#-----------------------------------------------------------------------------------------------------------------
# Change python version in xml files to 2.1.0
def Gotham():
    path = xbmc.translatePath(os.path.join('special://home', 'addons'))
    dp   = xbmcgui.DialogProgress()
    dp.create("Gotham Addon Fix","Please wait whilst your addons",'', 'are being made Gotham compatible.')
    
    for infile in glob.glob(os.path.join(path, '*.*')):
        
        for file in glob.glob(os.path.join(infile, '*.*')):
            
            if 'addon.xml' in file:
                dp.update(0,"Fixing",file, 'Please Wait')
                a = open(file).read()
                b = a.replace('addon="xbmc.python" version="1.0"','addon="xbmc.python" version="2.1.0"').replace('addon="xbmc.python" version="2.0"','addon="xbmc.python" version="2.1.0"')
                f = open(file, mode='w')
                f.write(str(b))
                f.close()

    dialog = xbmcgui.Dialog()
    dialog.ok("Your addons have now been made compatible", "If you still find you have addons that aren't working please run the addon so it throws up a script error, upload a log and post details on the relevant support forum.")
#-----------------------------------------------------------------------------------------------------------------  
def Gotham_Confirm():
    if dialog.yesno('Convert Addons To Gotham', 'This will edit your addon.xml files so they show as Gotham compatible. It\'s doubtful this will have any effect on whether or not they work but it will get rid of the annoying incompatible pop-up message. Do you wish to continue?'):
        Gotham()
#---------------------------------------------------------------------------------------------------
# Grab contents of the log
def Grab_Log():
    finalfile = 0
    logfilepath = os.listdir(log_path)
    for item in logfilepath:
        if item.endswith('.log') and not item.endswith('.old.log'):
            mylog        = os.path.join(log_path,item)
            lastmodified = os.path.getmtime(mylog)
            if lastmodified>finalfile:
                finalfile = lastmodified
                logfile   = mylog
    
    filename    = open(logfile, 'r')
    logtext     = filename.read()
    filename.close()
    return logtext
#---------------------------------------------------------------------------------------------------
# Fix the blank on-screen keyboard when using Gotham skins on Helix.
# BIG THANKS TO THE AUTHOR OF XUNITY MAINTENANCE FOR THE MAJORITY OF THIS SECTION OF CODE
def Helix():
    skin = xbmc.getSkinDir()
    path = xbmc.translatePath(os.path.join(ADDONS, skin))
    
    for root, dirs, files in os.walk(path):
       
       for f in files:
            
            if 'DialogKeyboard.xml' in f:
                skin   = os.path.join(root, f)
                a      = open(skin).read()
                CHANGE = a.replace('<control type="label" id="310"','<control type="edit" id="312"')
                f      = open(skin, mode='w')
                f.write(CHANGE)
                f.close()     
                changekeys(skin)
                
                for i in range(48, 58):
                    changenumber(i,skin)
    
    dialog = xbmcgui.Dialog()
    dialog.ok("Skin Changes Successful", 'A BIG thank you to Mikey1234 for this fix. The code used for this function was ported from the Xunity Maintenance add-on')
    xbmc.executebuiltin('ReloadSkin()')   
#---------------------------------------------------------------------------------------------------
def Helix_Confirm():
    if dialog.yesno('Convert This Skin To Kodi (Helix)?', 'This will fix the problem with a blank on-screen keyboard showing in skins designed for Gotham (being run on Kodi). This will only affect the currently running skin.', nolabel='No, Cancel',yeslabel='Yes, Fix'):
        Helix()
#-----------------------------------------------------------------------------------------------------------------          
# Hide passwords in addon settings
# BIG THANKS TO THE AUTHOR OF XUNITY MAINTENANCE FOR THE MAJORITY OF THIS SECTION OF CODE
def Hide_Passwords():
    if dialog.yesno("Hide Passwords", "This will hide all your passwords in your", "add-on settings, are you sure you wish to continue?"):
        for root, dirs, files in os.walk(ADDONS):
            for f in files:
                if f =='settings.xml':
                    FILE=open(os.path.join(root, f)).read()
                    match=re.compile('<setting id=(.+?)>').findall (FILE)
                    for LINE in match:
                        if 'pass' in LINE:
                            if not 'option="hidden"' in LINE:
                                try:
                                    CHANGEME=LINE.replace('/',' option="hidden"/') 
                                    f = open(os.path.join(root, f), mode='w')
                                    f.write(str(FILE).replace(LINE,CHANGEME))
                                    f.close()
                                except:
                                    pass
        dialog.ok("Passwords Hidden", "Your passwords will now show as stars (hidden), if you want to undo this please use the option to unhide passwords.") 
#---------------------------------------------------------------------------------------------------
#Browse pre-installed repo's via the kodi add-on browser
def Install_From_Zip():
    xbmc.executebuiltin('ActivateWindow(10040,"addons://install/",return)')
#-----------------------------------------------------------------------------------------------------------------
# Return details about the IP address lookup       
def IP_Check():
    ip_site = ADDON.getSetting('ip_site')
    try:
        if ip_site == "whatismyipaddress.com":
           BaseURL       = 'http://whatismyipaddress.com/'
           link          = Open_URL(BaseURL, 30).replace('\n','').replace('\r','')
           if not 'Access Denied' in link:
               ipmatch       = re.compile('whatismyipaddress.com/ip/(.+?)"').findall(link)
               ipfinal       = ipmatch[0] if (len(ipmatch) > 0) else 'Unknown'
               xbmc.log(ipfinal)
               details       = re.compile('"font-size:14px;">(.+?)</td>').findall(link)
               xbmc.log(str(details))
               provider      = details[0] if (len(details) > 0) else 'Unknown'
               xbmc.log(provider)
               location      = details[1]+', '+details[2]+', '+details[3] if (len(details) > 2) else 'Unknown'
               xbmc.log(location)
               dialog.ok('www.whatismyipaddress.com',"[B][COLOR gold]Address: [/COLOR][/B] %s" % ipfinal, '[B][COLOR gold]Provider: [/COLOR][/B] %s' % provider, '[B][COLOR gold]Location: [/COLOR][/B] %s' % location)
        else:
            BaseURL       = 'https://www.iplocation.net/find-ip-address'
            link          = Open_URL(BaseURL, 30).replace('\n','').replace('\r','')
            xbmc.log(link)
            segment       = re.compile('<table class="iptable">(.+?)</table>').findall(link)
            xbmc.log(str(segment))
            ipmatch       = re.compile('font-weight: bold;">(.+?)</span>').findall(str(segment))
            xbmc.log(ipmatch)
            ipfinal       = ipmatch[0] if (len(ipmatch) > 0) else 'Unknown'
            providermatch = re.compile('Host Name</th><td>(.+?)</td>').findall(str(segment))
            hostname      = providermatch[0] if (len(providermatch) > 0) else 'Unknown'
            locationmatch = re.compile('IP Location</th><td>(.+?)&nbsp;').findall(str(segment))
            location      = locationmatch[0] if (len(locationmatch) > 0) else 'Unknown'
            dialog.ok('www.iplocation.net',"[B][COLOR gold]Address: [/COLOR][/B] %s" % ipfinal, '[B][COLOR gold]Host: [/COLOR][/B] %s' % hostname, '[B][COLOR gold]Location: [/COLOR][/B] %s' % location)
    except:
        dialog.ok('SERVICE UNAVAILABLE', 'It was not possible to contact the relevant website to check your details. Please check your internet connection and if that\'s ok try using an alternative site in the settings.')
#---------------------------------------------------------------------------------------------------
# Check to see if a specific dialog/window is active
def Is_Window_Active(window_type):
    windowactive = False
    counter = 0

    if window_type == 'yesnodialog':
        count = 50
    else:
        count = 10
    
    okwindow = xbmc.getCondVisibility('Window.IsActive(%s)' % window_type)

# Do not get stuck in an infinite loop. Check x amount of times and if condition isn't met after x amount it quits
    while not okwindow and counter < count:
        xbmc.sleep(100)
        okwindow = xbmc.getCondVisibility('Window.IsActive(%s)' % window_type)
        counter += 1
    while okwindow:
        windowactive = True
        okwindow = xbmc.getCondVisibility('Window.IsActive(%s)' % window_type)
        xbmc.sleep(250)
    return windowactive
#---------------------------------------------------------------------------------------------------
# Force close Kodi
def Kill_XBMC():
    os._exit(1)
#---------------------------------------------------------------------------------------------------
# Open Kodi Settings
def Kodi_Settings():
    xbmc.executebuiltin('ReplaceWindow(settings)')
#---------------------------------------------------------------------------------------------------
# Function to find the latest version of a database
def Latest_DB(DB):
    if DB in ['Addons', 'ADSP', 'Epg', 'MyMusic', 'MyVideos', 'Textures', 'TV', 'ViewModes']:
        match   = glob.glob(os.path.join(DATABASE,'%s*.db' % DB))
        comp    = '%s(.+?).db' % DB[1:]
        highest = 0
        for file in match:
            try:
                check = int(re.compile(comp).findall(file)[0])
            except:
                check = 0
            if highest < check:
                highest = check
        return '%s%s.db' % (DB, highest)
    else:
        return False
#-----------------------------------------------------------------------------------------------------------------
# View the log from within Kodi
def Log_Viewer():
    content = Grab_Log()
    Text_Boxes('Log Viewer', content)
#---------------------------------------------------------------------------------------------------
# Function to move a directory to another location, use 1 for clean paramater if you want to remove original source.
def Move_Tree(src,dst,clean):
    for src_dir, dirs, files in os.walk(src):
        dst_dir = src_dir.replace(src, dst, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.move(src_file, dst_dir)
    if clean == 1:
        try:
            shutil.rmtree(src)
        except:
            pass
#---------------------------------------------------------------------------------------------------
# Multiselect Dialog - works with gotham onwards
def multiselect(title, list, images, description):
    global pos
    global listicon
    class MultiChoiceDialog(pyxbmct.AddonDialogWindow):
        def __init__(self, title="", items=None, images=None, description=None):
            super(MultiChoiceDialog, self).__init__(title)
            self.setGeometry(1100, 700, 20, 20)
            self.selected = []
            self.set_controls()
            self.connect_controls()
            self.listing.addItems(items or [])
            self.set_navigation()
            self.connect(ACTION_MOVE_UP, self.update_list)
            self.connect(ACTION_MOVE_DOWN, self.update_list)
            
        def set_controls(self):
            Background  = pyxbmct.Image(dialog_bg, aspectRatio=0) # set aspect ratio to stretch
            Background.setImage(dialog_bg)
            self.listing = pyxbmct.List(_imageWidth=15)
            self.placeControl(Background, 0, 0, rowspan=20, columnspan=20)
            Icon=pyxbmct.Image(images[0], aspectRatio=2) # set aspect ratio to keep original
            Icon.setImage(images[0])
            self.placeControl(Icon, 0, 11, rowspan=8, columnspan=8, pad_x=10, pad_y=10)
            self.textbox = pyxbmct.TextBox()
            self.placeControl(self.textbox, 8, 11, rowspan=9, columnspan=9, pad_x=10, pad_y=10)
            self.textbox.setText(description[0])
            self.textbox.autoScroll(5000, 2000, 8000)
            self.ok_button = pyxbmct.Button("OK")
            self.placeControl(self.ok_button, 17, 13, pad_x=10, pad_y=10, rowspan=2, columnspan=3)
            self.cancel_button = pyxbmct.Button("Cancel")
            self.placeControl(self.cancel_button, 17, 16, pad_x=10, pad_y=10, rowspan=2, columnspan=3)
            self.placeControl(self.listing, 0, 0, rowspan=20, columnspan=10, pad_y=10) # grid reference, start top left and span 9 boxes down and 5 across

        def connect_controls(self):
            self.connect(self.listing, self.check_uncheck)
            self.connect(self.ok_button, self.ok)
            self.connect(self.cancel_button, self.close)

        def set_navigation(self):
            self.listing.controlLeft(self.ok_button)
            self.listing.controlRight(self.ok_button)
            self.ok_button.setNavigation(self.listing, self.listing, self.cancel_button, self.cancel_button)
            self.cancel_button.setNavigation(self.listing, self.listing, self.ok_button, self.ok_button)
            if self.listing.size():
                self.setFocus(self.listing)
            else:
                self.setFocus(self.cancel_button)
            
        def update_list(self):
            blackout = pyxbmct.Image(black, aspectRatio=0) # set aspect ratio to stretch
            blackout.setImage(black)
            self.placeControl(blackout, 0, 11, rowspan=8, columnspan=8, pad_x=10, pad_y=10)
            pos      = self.listing.getSelectedPosition()
            listicon = images[pos]
            Icon     = pyxbmct.Image(listicon, aspectRatio=2)
            Icon.setImage(listicon)
            self.placeControl(Icon, 0, 11, rowspan=8, columnspan=8, pad_x=10, pad_y=10)
            self.textbox.setText(description[pos])

        def check_uncheck(self):
            list_item = self.listing.getSelectedItem()
            if list_item.getLabel2() == "checked":
                list_item.setIconImage("")
                list_item.setLabel2("unchecked")
            else:
                list_item.setIconImage(checkicon)
                list_item.setLabel2("checked")

        def ok(self):
            self.selected = [index for index in xrange(self.listing.size())
                            if self.listing.getListItem(index).getLabel2() == "checked"]
            super(MultiChoiceDialog, self).close()

        def close(self):
            self.selected = []
            super(MultiChoiceDialog, self).close()
            
    dialog = MultiChoiceDialog(title, list, images, description)
    dialog.doModal()
    return dialog.selected
    del dialog
#---------------------------------------------------------------------------------------------------
# Simple shortcut to create a notification
def Notify(title,message,times,icon):
    icon = notifyart+icon
    xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")
#---------------------------------------------------------------------------------------------------
# Open Kodi File Manager
def Open_Filemanager():
    xbmc.executebuiltin('ActivateWindow(filemanager,return)')
    return
#---------------------------------------------------------------------------------------------------
# Open Kodi System Info
def Open_System_Info():
    xbmc.executebuiltin('ActivateWindow(systeminfo)')
#-----------------------------------------------------------------------------------------------------------------
# Function to open a URL and return the contents
def Open_URL(url, t):
    req = urllib2.Request(url)
    req.add_header('User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 10.0; WOW64; Windows NT 5.1; en-GB; rv:1.9.0.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36 Gecko/2008092417 Firefox/3.0.3')
# OLD ONE    req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    counter = 0
    success = False
    while counter < 5 and success == False: 
        response = urllib2.urlopen(req, timeout = t)
        link     = response.read()
        response.close()
        counter += 1
        if link != '':
            success = True
    if success == True:
        return link.replace('\r','').replace('\n','').replace('\t','')
    else:
        dialog.ok('Unable to contact server','There was a problem trying to access the server, please try again later.')
        return
#---------------------------------------------------------------------------------------------------
# Function to create an OE tar backup
def OpenELEC_Backup():
    import tarfile

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    dp.create("Creating Backup","Adding files... ",'', 'Please Wait')
    tar = tarfile.open(os.path.join(backup_dir, Timestamp()+'.tar'), 'w')
    
    for directory in BACKUP_DIRS:
        dp.update(0,"Backing Up",'[COLOR blue]%s[/COLOR]'%directory, 'Please Wait')
        tar.add(directory)
    
    tar.close()
    dp.close()
#---------------------------------------------------------------------------------------------------
# Check if system is OE or LE
def OpenELEC_Check():
    content = Grab_Log()
    if 'Running on OpenELEC' in content or 'Running on LibreELEC' in content:
        return True
#---------------------------------------------------------------------------------------------------
# Open OE Settings
def OpenELEC_Settings():
    try:
        xbmcaddon.Addon(id='service.openelec.settings').getAddonInfo('name')
        xbmc.executebuiltin('ActivateWindow(10025,plugin://service.openelec.settings,return)')
    except:
        xbmcaddon.Addon(id='service.libreelec.settings').getAddonInfo('name')
        xbmc.executebuiltin('ActivateWindow(10025,plugin://service.libreelec.settings,return)')
#---------------------------------------------------------------------------------------------------
# Recursive loop for downloading files from web
def Recursive_Loop(recursive_location,remote_path):
    if not os.path.exists(recursive_location):
        os.makedirs(recursive_location)
    
    link   = Open_URL(remote_path, 10).replace('\n','').replace('\r','')
    match  = re.compile('href="(.+?)"', re.DOTALL).findall(link)
    
    for href in match:
        filepath=xbmc.translatePath(os.path.join(recursive_location,href)) #works
        
        if '/' not in href:
            
            try:
                dp.update(0,"Downloading [COLOR=yellow]"+href+'[/COLOR]','','Please wait...')
                downloader.download(remote_path+href, filepath, dp)
            
            except:
                xbmc.log("failed to install  %s" % href)
        
        if '/' in href and '..' not in href and 'http' not in href:
            remote_path2 = remote_path+href
            Recursive_Loop(filepath,remote_path2)
        
        else:
            pass
#---------------------------------------------------------------------------------------------------
# Function to clear the addon_data
def Remove_Addon_Data():
    choice = dialog.yesno('DELETE ADD-ON DATA', 'Do you want to remove individual addon_data folders or wipe all addon_data?', yeslabel='EVERYTHING', nolabel='INDIVIDUAL ITEMS')
    
    if choice:
        choice = dialog.yesno('Are you ABSOLUTELY certain?','This will remove ALL your addon_data, there\'s no getting it back! Are you certain you want to continue?')
        if choice:
            Delete_Userdata()
            dialog.ok("Addon_Data Removed", '', 'Your addon_data folder has now been removed.','')
    else:
        namearray = []
        iconarray = []
        descarray = []
        patharray = []
        finalpath = []

        for file in os.listdir(ADDON_DATA):
            if os.path.isdir(os.path.join(ADDON_DATA,file)):
                try:
                    Addon       = xbmcaddon.Addon(file)
                    name        = Addon.getAddonInfo('name')
                    iconimage   = Addon.getAddonInfo('icon')
                    description = Addon.getAddonInfo('description')
                except:
                    name        = 'Unknown Add-on'
                    iconimage   =  unknown_icon
                    description = 'No add-on has been found on your system that matches this ID. The most likely scenario for this is you\'ve previously uninstalled this add-on and left the old addon_data on the system.'

            else:
                name        = 'Unknown Add-on'
                iconimage   =  unknown_icon
                description = 'No add-on has been found on your system that matches this ID. The most likely scenario for this is you\'ve previously uninstalled this add-on and left the old addon_data on the system.'

            filepath    = os.path.join(ADDON_DATA,file)
            namearray.append('%s [COLOR=gold](%s)[/COLOR]' % (file,name))
            iconarray.append(iconimage)
            descarray.append(description)
            patharray.append(filepath)

        finalarray = multiselect('Addon_Data To Remove',namearray,iconarray,descarray)
        for item in finalarray:
            newpath = patharray[item]
            newname = namearray[item]
            finalpath.append([newname,newpath])
        xbmc.log('FINAL: %s' % finalpath)
        if len(finalpath) > 0:
            Remove_Addons(finalpath)
#---------------------------------------------------------------------------------------------------
# Function to remove a list of addons including addon_data
def Remove_Addons(url):
    removed = 0
    for item in url:
        data_path = item[1].replace(ADDONS,ADDON_DATA)
        if 'addon_data' in item[1]:
            addontype = 'Addon_Data'
        else:
            addontype = 'Addon'
        if dialog.yesno("Remove %s" % addontype, "Do you want to Remove:",'[COLOR=dodgerblue]%s[/COLOR]'%item[0]):
            if not 'addon_data' in item[1]:
                removed = 1
            for root, dirs, files in os.walk(item[1]):
                
                for f in files:
                    os.unlink(os.path.join(root, f))
                
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
            os.rmdir(item[1])
            if not 'addon_data' in item[1]:
                if dialog.yesno('Remove Addon_Data?','Would you also like to remove the addon_data associated with this add-on? This contains your add-on settings and can contain personal information such as username/password.'):
                    try:
                        for root, dirs, files in os.walk(data_path):
                            for f in files:
                                os.unlink(os.path.join(root, f))
                            for d in dirs:
                                shutil.rmtree(os.path.join(root, d))
                        os.rmdir(data_path)
                    except:
                        pass
    if removed:
        xbmc.executebuiltin( 'UpdateLocalAddons' )
        xbmc.executebuiltin( 'UpdateAddonRepos' )
        Remove_Packages('nodialog')
        Clean_Addons()
# Need to create function to wipe relevant bits from db
#        Cleanup_Old_Addons()
        dialog.ok('REMOVAL COMPLETE','The addons database file now needs purging, to do so we need to restart. If prompted please agree to the deletion otherwise your add-ons may still appear in Kodi even if they don\'t physically exist.')
        Kill_XBMC('wipe')
#---------------------------------------------------------------------------------------------------
# Function to restore a zip file 
def Remove_Build():
    Check_Download_Path()
    filename = dialog.browse(1, 'Select the backup file you want to DELETE', 'files', '.zip', False, False, USB)
    
    if filename != USB:
        clean_title = ntpath.basename(filename)
        if dialog.yesno('Delete Backup File', 'This will completely remove '+clean_title, 'Are you sure you want to delete?', '', nolabel='No, Cancel',yeslabel='Yes, Delete'):
            os.remove(filename)
#---------------------------------------------------------------------------------------------------
# Function to clear the packages folder
def Remove_Crash_Logs():
    if dialog.yesno('Remove All Crash Logs?', 'There is absolutely no harm in doing this, these are log files generated when Kodi crashes and are only used for debugging purposes.', nolabel='Cancel',yeslabel='Delete'):
        Delete_Logs()
        dialog.ok("Crash Logs Removed", '', 'Your crash log files have now been removed.','')
#---------------------------------------------------------------------------------------------------
# Function to clear the packages folder
def Remove_Packages(url=''):
    if dialog.yesno('Delete Packages Folder', 'Do you wipe the packages folder? This will delete your old zip install files that are no longer in use. This will disable the ability to rollback but causes no harm', nolabel='Cancel',yeslabel='Delete'):
        Delete_Packages()
    if url == '':
        dialog.ok("Packages Removed", '', 'Your zip install files have now been removed.','')
#---------------------------------------------------------------------------------------------------
# Function to clear the packages folder
def Remove_Textures_Dialog():
    if dialog.yesno('Clear Cached Images?', 'This will clear your textures13.db file and remove your Thumbnails folder. These will automatically be repopulated after a restart.', nolabel='Cancel',yeslabel='Delete'):
        Remove_Textures()
        Destroy_Path(THUMBNAILS)
        
        if dialog.yesno('Quit Kodi Now?', 'Cache has been successfully deleted.', 'You must now restart Kodi, would you like to quit now?','', nolabel='I\'ll restart later',yeslabel='Yes, quit'):
            try:
                xbmc.executebuiltin("RestartApp")
            except:
                Kill_XBMC()
#---------------------------------------------------------------------------------------------------
# Function to remove textures13.db and thumbnails folder    
def Remove_Textures():
    textures = os.path.join(DATABASE, Latest_DB('Textures'))
    if os.path.exists(textures):
        try:
            textdb = database.connect(textures)
            textexe = textdb.cursor()
        except Exception, e:
            xbmc.log(str(e))
            return False
    else:
        xbmc.log('%s not found.' % textures)
        return False

    textexe.execute("""SELECT name FROM sqlite_master WHERE type = 'table';""")
    for table in textexe.fetchall():
        if table[0] == 'version': 
            xbmc.log('Data from table `%s` skipped.' % table[0])
        else:
            try:
                textexe.execute("""DELETE FROM %s""" % table[0])
                textdb.commit()
                xbmc.log('Data from table `%s` cleared.' % table[0])
            except e:
                xbmc.log(str(e))
    
    xbmc.log('%s DB Purging Complete.' % textures)
    show = textures.replace('\\', '/').split('/')
    Notify("Purge Database", "%s Complete" % show[len(show)-1])
#---------------------------------------------------------------------------------------------------
# Function to restore a backup xml file (guisettings, sources, RSS)
def Restore_Backup_XML(name,url,description):
    if 'Backup' in name:
        Check_Download_Path()
        TO_READ   = open(url).read()
        TO_WRITE  = os.path.join(USB,description.split('Your ')[1])
        f         = open(TO_WRITE, mode='w')
        f.write(TO_READ)
        f.close() 
    
    else:
        if 'guisettings.xml' in description:
            a     = open(os.path.join(USB,description.split('Your ')[1])).read()
            r     ='<setting type="(.+?)" name="%s.(.+?)">(.+?)</setting>'% skin
            match = re.compile(r).findall(a)
            
            for type,string,setting in match:
                setting=setting.replace('&quot;','') .replace('&amp;','&') 
                xbmc.executebuiltin("Skin.Set%s(%s,%s)"%(type.title(),string,setting))  
        
        else:    
            TO_WRITE = os.path.join(url)
            TO_READ  = open(os.path.join(USB,description.split('Your ')[1])).read()
            f        = open(TO_WRITE, mode='w')
            f.write(TO_READ)
            f.close()  

    dialog.ok("Restore Complete", "", 'All Done !','')
#---------------------------------------------------------------------------------------------------
# Function to restore a local backup
def Restore_Local_Community(url):
    exitfunction = 0
    choice4      = 0
    xbmc.log("### Local Build Restore Location: %s" % url)

    Check_Download_Path()

    if url == 'local':
        filename = xbmcgui.Dialog().browse(1, 'Select the backup file you want to restore', 'files', '.zip', False, False, USB)
        if filename == '':
            exitfunction = 1

    if exitfunction == 1:
        xbmc.log("### No file selected, quitting restore process ###")
        return
        
    if os.path.exists(GUINEW):
        if os.path.exists(GUI):
            os.remove(GUINEW)
        else:
            os.rename(GUINEW,GUI)
            
    if os.path.exists(GUIFIX):
        os.remove(GUIFIX)
        
# Function for debugging, creates a file that was created in previous call and subsequently deleted when run
    if not os.path.exists(tempfile):
        localfile = open(tempfile, mode='w+')
        
    if os.path.exists(guitemp):
        os.removedirs(guitemp)
        
# Rename guisettings.xml to guinew.xml so we can edit without XBMC interfering.
    try:
        os.rename(GUI,GUINEW)

    except:
        dialog.ok("NO GUISETTINGS!",'No guisettings.xml file has been found.', 'Please exit XBMC and try again','')
        return

    if dialog.yesno(name, 'We highly recommend backing up your existing build before installing any builds. Would you like to perform a backup first?', nolabel='Backup',yeslabel='Install'):
        mybackuppath = xbmc.translatePath(os.path.join(USB,'Community_Builds','My_Builds'))

        if not os.path.exists(mybackuppath):
            os.makedirs(mybackuppath)

        vq = Get_Keyboard( heading="Enter a name for this backup" )
        if ( not vq ):
            return False, 0
            
        title              = urllib.quote_plus(vq)
        backup_zip         = xbmc.translatePath(os.path.join(mybackuppath,title+'.zip'))
        exclude_dirs_full  =  [AddonID]
        exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf','.gitignore']
        message_header     = "Creating full backup of existing build"
        message1           = "Archiving..."
        message2           = ""
        message3           = "Please Wait"
        
        Archive_Tree(HOME, backup_zip, message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)
    choice3 =  dialog.yesno(name, 'Would you like to keep your existing database files or overwrite? Overwriting will wipe any existing music or video library you may have scanned in.', nolabel='Overwrite',yeslabel='Keep Existing')
    if choice3:
        if os.path.exists(tempdbpath):
            shutil.rmtree(tempdbpath)

        try:
            shutil.copytree(DATABASE, tempdbpath, symlinks=False, ignore=shutil.ignore_patterns("Textures13.db","Addons16.db","Addons15.db","saltscache.db-wal","saltscache.db-shm","saltscache.db","onechannelcache.db")) #Create temp folder for databases, give user option to overwrite existing library

        except:
            choice4 = dialog.yesno(name, 'There was an error trying to backup some databases. Continuing may wipe your existing library. Do you wish to continue?', nolabel='No, cancel',yeslabel='Yes, overwrite')
            if not choice4:
                exitfunction=1
                return

        backup_zip = xbmc.translatePath(os.path.join(USB,'Database.zip'))
        Archive_File(tempdbpath,backup_zip)
    
    if exitfunction == 1:
        xbmc.log("### User decided to exit restore function ###")
        return
    
    else:
        time.sleep(1)
        readfile         = open(CBADDONPATH, mode='r')
        default_contents = readfile.read()
        readfile.close()

# check to see if the dickheads have used some piece of shit backup program that includes logs, if they have re-zip it up PROPERLY!!!       
        xbmc.log("### Checking zip file structure ###")
        z = zipfile.ZipFile(filename)
        if 'xbmc.log' in z.namelist() or 'kodi.log' in z.namelist() or 'tvmc.log' in z.namelist() or 'spmc.log' in z.namelist() or '.git' in z.namelist() or '.svn' in z.namelist():
            print "### Whoever created this build has used completely the wrong backup method, lets try and fix it! ###"        
            dialog.ok('Fixing Bad Zip','Whoever created this build has used the wrong backup method, please wait while we fix it - this could take some time! Click OK to proceed')
            zin       = zipfile.ZipFile (filename, 'r')
            filename2 = os.path.join(CBPATH, 'fixed.zip')
            zout      = zipfile.ZipFile (filename2, 'w')

            dp.create("Fixing Build","Checking ",'', 'Please Wait')
            
            for item in zin.infolist():
                buffer = zin.read(item.filename)
                clean_file = str(item.filename)

                if (item.filename[-4:] != '.log') and not '.git' in clean_file and not '.svn' in clean_file:
                    zout.writestr(item, buffer)
                    dp.update(0,"Fixing...",'[COLOR yellow]%s[/COLOR]'%item.filename, 'Please Wait')
            
            dp.close()
            zout.close()
            zin.close()
            filename = filename2
            
        dp.create("Restoring Backup Build","Checking ",'', 'Please Wait')
        dp.update(0,"", "Extracting Zip Please Wait")
        
        try:
            extract.all(filename,HOME,dp)
        except:
            dialog.ok('ERROR IN BUILD ZIP','Please contact the build author, there are errors in this zip file that has caused the install process to fail. Most likely cause is it contains files with special characters in the name.')
            return
        
        time.sleep(1)

        if choice3:
            extract.all(backup_zip,DATABASE,dp) #This folder first needs zipping up
            
            if not choice4:
                shutil.rmtree(tempdbpath)
        
        cbdefaultpy = open(CBADDONPATH, mode='w+')
        cbdefaultpy.write(default_contents)
        cbdefaultpy.close()
        try:
            os.rename(GUI,GUIFIX)

        except:
            xbmc.log("NO GUISETTINGS DOWNLOADED")

        time.sleep(1)
        localfile = open(GUINEW, mode='r') #Read the original skinsettings tags and store in memory ready to replace in guinew.xml
        content = localfile.read()
        localfile.close()
        skinsettingsorig = re.compile('<skinsettings>[\s\S]*?<\/skinsettings>').findall(content)
        skinorig  = skinsettingsorig[0] if (len(skinsettingsorig) > 0) else ''
        skindefault = re.compile('<skin default[\s\S]*?<\/skin>').findall(content)
        skindefaultorig  = skindefault[0] if (len(skindefault) > 0) else ''
        lookandfeelorig = re.compile('<lookandfeel>[\s\S]*?<\/lookandfeel>').findall(content)
        lookandfeel  = lookandfeelorig[0] if (len(lookandfeelorig) > 0) else ''

        try:
            localfile2 = open(GUIFIX, mode='r')
            content2 = localfile2.read()
            localfile2.close()
            skinsettingscontent = re.compile('<skinsettings>[\s\S]*?<\/skinsettings>').findall(content2)
            skinsettingstext  = skinsettingscontent[0] if (len(skinsettingscontent) > 0) else ''
            skindefaultcontent = re.compile('<skin default[\s\S]*?<\/skin>').findall(content2)
            skindefaulttext  = skindefaultcontent[0] if (len(skindefaultcontent) > 0) else ''
            lookandfeelcontent = re.compile('<lookandfeel>[\s\S]*?<\/lookandfeel>').findall(content2)
            lookandfeeltext  = lookandfeelcontent[0] if (len(lookandfeelcontent) > 0) else ''
            replacefile = content.replace(skinorig,skinsettingstext).replace(lookandfeel,lookandfeeltext).replace(skindefaultorig,skindefaulttext)
            writefile = open(GUINEW, mode='w+')
            writefile.write(str(replacefile))
            writefile.close()

        except:
            xbmc.log("### NO GUISETTINGS DOWNLOADED")

        if os.path.exists(GUI):
            os.remove(GUI)
        
        os.rename(GUINEW,GUI)
        try:
            os.remove(GUIFIX)
        
        except:
            pass
        
        os.makedirs(guitemp)
        time.sleep(1)
        Kill_XBMC()
#---------------------------------------------------------------------------------------------------
#Function to restore a local copy of guisettings_fix
def Restore_Local_GUI():
    Check_Download_Path()
    guifilename = dialog.browse(1, 'Select the guisettings zip file you want to restore', 'files', '.zip', False, False, USB)

    if guifilename == '':
        return

    else:
        local=1
        GUI_Settings_Fix(guifilename,local)  
#---------------------------------------------------------------------------------------------------
# Function to restore an OE based community build
def Restore_OpenELEC_Local():
    exitfunction = 0
    if dialog.yesno('Full Wipe And New Install', 'This is a great option if you\'re encountering any issues with your device. This will wipe all your Kodi settings and restore with whatever is in the backup, do you wish to continue?', nolabel='Cancel',yeslabel='Accept'):
        filename = dialog.browse(1, 'Select the backup file you want to restore', 'files', '.tar', False, False, backup_dir)
        if filename == '':
            exitfunction = 1

        if exitfunction == 1:
            xbmc.log("### No file selected, quitting restore process ###")
            return
        path = os.path.join(restore_dir, Timestamp()+'.tar')
        if not os.path.exists(restore_dir):
            try:
                os.makedirs(restore_dir)
            except:
                pass
        dp.create('Copying File To Restore Folder','','Please wait...')
        shutil.copyfile(filename,path)
        xbmc.executebuiltin('Reboot')
#---------------------------------------------------------------------------------------------------
# Create restore menu
def Restore_Option():
    if os.path.exists(os.path.join(USB,'addons.zip')):   
        addDir('','Restore Your Addons','addons','restore_zip','Restore.png','','','Restore Your Addons')

    if os.path.exists(os.path.join(USB,'addon_data.zip')):   
        addDir('','Restore Your Addon UserData','addon_data','restore_zip','Restore.png','','','Restore Your Addon UserData')           

    if os.path.exists(os.path.join(USB,'guisettings.xml')):
        addDir('','Restore Guisettings.xml',GUI,'resore_backup','Restore.png','','','Restore Your guisettings.xml')
    
    if os.path.exists(os.path.join(USB,'favourites.xml')):
        addDir('','Restore Favourites.xml',FAVS,'resore_backup','Restore.png','','','Restore Your favourites.xml')
        
    if os.path.exists(os.path.join(USB,'sources.xml')):
        addDir('','Restore Source.xml',SOURCE,'resore_backup','Restore.png','','','Restore Your sources.xml')
        
    if os.path.exists(os.path.join(USB,'advancedsettings.xml')):
        addDir('','Restore Advancedsettings.xml',ADVANCED,'resore_backup','Restore.png','','','Restore Your advancedsettings.xml')        

    if os.path.exists(os.path.join(USB,'keyboard.xml')):
        addDir('','Restore Advancedsettings.xml',KEYMAPS,'resore_backup','Restore.png','','','Restore Your keyboard.xml')
        
    if os.path.exists(os.path.join(USB,'RssFeeds.xml')):
        addDir('','Restore RssFeeds.xml',RSS,'resore_backup','Restore.png','','','Restore Your RssFeeds.xml')    
#---------------------------------------------------------------------------------------------------
# Function to restore a previously backed up zip, this includes full backup, addons or addon_data.zip
def Restore_Zip_File(url):
    Check_Download_Path()
    if 'addons' in url:
        ZIPFILE    = xbmc.translatePath(os.path.join(USB,'addons.zip'))
        DIR        = ADDONS

    else:
        ZIPFILE = xbmc.translatePath(os.path.join(USB,'addon_data.zip'))
        DIR = ADDON_DATA

    if 'Backup' in name:
        Delete_Packages() 
        dp.create("Creating Backup","Backing Up",'', 'Please Wait')
        zipobj       = zipfile.ZipFile(ZIPFILE , 'w', zipfile.ZIP_DEFLATED)
        rootlen      = len(DIR)
        for_progress = []
        ITEM         = []

        for base, dirs, files in os.walk(DIR):
            for file in files:
                ITEM.append(file)
        N_ITEM = len(ITEM)
        for base, dirs, files in os.walk(DIR):
            for file in files:
                for_progress.append(file) 
                progress = len(for_progress) / float(N_ITEM) * 100  
                dp.update(int(progress),"Backing Up",'[COLOR yellow]%s[/COLOR]'%file, 'Please Wait')
                fn = os.path.join(base, file)
                if not 'temp' in dirs:
                    if not AddonID in dirs:
                       import time
                       FORCE= '01/01/1980'
                       FILE_DATE=time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(fn)))
                       if FILE_DATE > FORCE:
                           zipobj.write(fn, fn[rootlen:]) 
        zipobj.close()
        dp.close()
        dialog.ok("Backup Complete", "You Are Now Backed Up", '','')   

    else:
        dp.create("Extracting Zip","Checking ",'', 'Please Wait')
        dp.update(0,"", "Extracting Zip Please Wait")
        extract.all(ZIPFILE,DIR,dp)
        time.sleep(1)
        xbmc.executebuiltin('UpdateLocalAddons ')    
        xbmc.executebuiltin("UpdateAddonRepos")        

        if 'Backup' in name:
            dialog.ok("Install Complete", 'Kodi will now close. Just re-open Kodi and wait for all the updates to complete.')
            Kill_XBMC()

        else:
            dialog.ok("SUCCESS!", "You Are Now Restored", '','')        
#---------------------------------------------------------------------------------------------------
# Basic function to run an add-on
def Run_Addon(url):
    xbmc.executebuiltin('RunAddon(%s)' % url)
#---------------------------------------------------------------------------------------------------
#Instructions for the speed test
def Speed_Instructions():
    Text_Boxes('Speed Test Instructions', '[COLOR=blue][B]What file should I use: [/B][/COLOR][CR]This function will download a file and will work out your speed based on how long it took to download. You will then be notified of '
    'what quality streams you can expect to stream without buffering. You can choose to download a 10MB, 16MB, 32MB, 64MB or 128MB file to use with the test. Using the larger files will give you a better '
    'indication of how reliable your speeds are but obviously if you have a limited amount of bandwidth allowance you may want to opt for a smaller file.'
    '[CR][CR][COLOR=blue][B]How accurate is this speed test:[/B][/COLOR][CR]Not very accurate at all! As this test is based on downloading a file from a server it\'s reliant on the server not having a go-slow day '
    'but the servers used should be pretty reliable. The 10MB file is hosted on a different server to the others so if you\'re not getting the results expected please try another file. If you have a fast fiber '
    'connection the chances are your speed will show as considerably slower than your real download speed due to the server not being able to send the file as fast as your download speed allows. Essentially the '
    'test results will be limited by the speed of the server but you will at least be able to see if it\'s your connection that\'s causing buffering or if it\'s the host you\'re trying to stream from'
    '[CR][CR][COLOR=blue][B]What is the differnce between Live Streams and Online Video:[/COLOR][/B][CR]When you run the test you\'ll see results based on your speeds and these let you know the quality you should expect to '
    'be able stream with your connection. Live Streams as the title suggests are like traditional TV channels, they are being streamed live so for example if you wanted to watch CNN this would fall into this category. '
    'Online Videos relates to movies, tv shows, youtube clips etc. Basically anything that isn\'t live - if you\'re new to the world of streaming then think of it as On Demand content, this is content that\'s been recorded and stored on the web.'
    '[CR][CR][COLOR=blue][B]Why am I still getting buffering:[/COLOR][/B][CR]The results you get from this test are strictly based on your download speed, there are many other factors that can cause buffering and contrary to popular belief '
    'having a massively fast internet connection will not make any difference to your buffering issues if the server you\'re trying to get the content from is unable to send it fast enough. This can often happen and is usually '
    'down to heavy traffic (too many users accessing the same server). A 10 Mb/s connection should be plenty fast enough for almost all content as it\'s very rare a server can send it any quicker than that.'
    '[CR][CR][COLOR=blue][B]What\'s the difference between MB/s and Mb/s:[/COLOR][/B][CR]A lot of people think the speed they see advertised by their ISP is Megabytes (MB/S) per second - this is not true. Speeds are usually shown as Mb/s '
    'which is Megabit per second - there are 8 of these to a megabyte so if you want to work out how many megabytes per second you\'re getting you need to divide the speed by 8. It may sound sneaky but really it\'s just the unit that has always been used.'
    '[CR][CR]A direct link to the buffering thread explaining what you can do to improve your viewing experience can be found at [COLOR=yellow]http://bit.ly/bufferingfix[/COLOR]'
    '[CR][CR]Thank you, [COLOR=orange]noobs[/COLOR][COLOR=dodgerblue]and[/COLOR][COLOR=orange]nerds[/COLOR] Team.')
#-----------------------------------------------------------------------------------------------------------------
# Speedtest menu
def Speed_Test_Menu():
    addDir('','[COLOR=blue]Instructions - Read me first[/COLOR]', 'none', 'speed_instructions', '','','','')
    addDir('','Download 16MB file   - [COLOR=lime]Server 1[/COLOR]', 'https://totalrevolution.googlecode.com/svn/trunk/download%20files/16MB.txt', 'runtest', '','','','')
    addDir('','Download 32MB file   - [COLOR=lime]Server 1[/COLOR]', 'https://totalrevolution.googlecode.com/svn/trunk/download%20files/32MB.txt', 'runtest', '','','','')
    addDir('','Download 64MB file   - [COLOR=lime]Server 1[/COLOR]', 'https://totalrevolution.googlecode.com/svn/trunk/download%20files/64MB.txt', 'runtest', '','','','')
    addDir('','Download 128MB file - [COLOR=lime]Server 1[/COLOR]', 'https://totalrevolution.googlecode.com/svn/trunk/download%20files/128MB.txt', 'runtest', '','','','')
    addDir('','Download 10MB file   - [COLOR=yellow]Server 2[/COLOR]', 'http://www.wswd.net/testdownloadfiles/10MB.zip', 'runtest', '','','','')
#-----------------------------------------------------------------------------------------------------------------
# Create a standard text box
def Text_Boxes(heading,anounce):
  class TextBox():
    WINDOW=10147
    CONTROL_LABEL=1
    CONTROL_TEXTBOX=5
    def __init__(self,*args,**kwargs):
      xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, )) # activate the text viewer window
      self.win=xbmcgui.Window(self.WINDOW) # get window
      xbmc.sleep(500) # give window time to initialize
      self.setControls()
    def setControls(self):
      self.win.getControl(self.CONTROL_LABEL).setLabel(heading) # set heading
      try:
        f=open(anounce); text=f.read()
      except:
        text=anounce
      self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
      return
  TextBox()
  while xbmc.getCondVisibility('Window.IsVisible(10147)'):
      xbmc.sleep(500)
#-----------------------------------------------------------------------------------------------------------------
# Show full description of build
def Text_Guide(url):
    try:
        heading,text = url.split('|')
        Text_Boxes(heading, text)
    except:
        Text_Boxes('', url)
#---------------------------------------------------------------------------------------------------
# Get current timestamp in integer format
def Timestamp():
    now = time.time()
    localtime = time.localtime(now)
    return time.strftime('%Y%m%d%H%M%S', localtime)
#-----------------------------------------------------------------------------------------------------------------
# Maintenance section
def Tools():
    addDir('folder','Add-on Tools','none','tools_addons','','','','')
    addDir('folder','Backup/Restore','none','backup_restore','','','','')
    addDir('folder','Clean up my Kodi', '', 'tools_clean', '','','','')
    addDir('folder','Misc. Tools', '', 'tools_misc', '','','','')
    if OpenELEC_Check():
        addDir('','[COLOR=dodgerblue]Wi-Fi / OpenELEC Settings[/COLOR]','', 'openelec_settings', '','','','')
#-----------------------------------------------------------------------------------------------------------------
# Add-on based tools
def Tools_Addons():
    addDir('','Completely Remove An Add-on (inc. passwords)','plugin','addon_removal_menu', '','','','')
    addDir('','Delete Addon Data','url','remove_addon_data','','','','')
    addDir('','Make Add-ons Gotham/Helix Compatible','none','gotham', '','','','')
    addDir('','Make Skins Kodi (Helix) Compatible','none','helix', '','','','')
    addDir('','Passwords - Hide when typing in','none','hide_passwords', '','','','')
    addDir('','Passwords - Unhide when typing in','none','unhide_passwords', '','','','')
    addDir('','Update My Add-ons (Force Refresh)', 'none', 'update', '','','','')
#-----------------------------------------------------------------------------------------------------------------
# Clean Tools
def Tools_Clean():
    addDir('','[COLOR=gold]CLEAN MY KODI FOLDERS (Save Space)[/COLOR]', '', 'full_clean', '','','','')
    addDir('','Clear All Cache Folders','url','clear_cache','','','','')
    addDir('','Clear Cached Artwork (thumbnails & textures)', 'none', 'remove_textures', '','','','')
    addDir('','Clear Packages Folder','url','remove_packages','','','','')
    addDir('','Delete Old Builds/Zips From Device','url','remove_build','','','','')
    addDir('','Delete Old Crash Logs','url','remove_crash_logs','','','','')
    addDir('','Wipe My Install (Fresh Start)', '', 'wipe_xbmc', '','','','')
#-----------------------------------------------------------------------------------------------------------------
# Advanced Maintenance section
def Tools_Misc():
    addDir('','Check For Special Characters In Filenames','', 'ASCII_Check', '','','','')
    addDir('','Check My IP Address', 'none', 'ipcheck', '','','','')
    addDir('','Check XBMC/Kodi Version', 'none', 'xbmcversion', '','','','')
    addDir('','Convert Physical Paths To Special',HOME,'fix_special','','','','')
    addDir('','Force Close Kodi','url','kill_xbmc','','','','')
    addDir('','Upload Log','none','uploadlog', '','','','')
    addDir('','View My Log','none','log', '','','','')
#-----------------------------------------------------------------------------------------------------------------
#Unhide passwords in addon settings - THANKS TO MIKEY1234 FOR THIS CODE (taken from Xunity Maintenance)
def Unhide_Passwords():
    if dialog.yesno("Make Add-on Passwords Visible?", "This will make all your add-on passwords visible in the add-on settings. Are you sure you wish to continue?"):
        for root, dirs, files in os.walk(ADDONS):
            for f in files:
                if f =='settings.xml':
                    FILE=open(os.path.join(root, f)).read()
                    match=re.compile('<setting id=(.+?)>').findall(FILE)
                    for LINE in match:
                        if 'pass' in LINE:
                            if  'option="hidden"' in LINE:
                                try:
                                    CHANGEME=LINE.replace(' option="hidden"', '') 
                                    f = open(os.path.join(root, f), mode='w')
                                    f.write(str(FILE).replace(LINE,CHANGEME))
                                    f.close()
                                except:
                                    pass
        dialog.ok("Passwords Are now visible", "Your passwords will now be visible in your add-on settings. If you want to undo this please use the option to hide passwords.") 
#---------------------------------------------------------------------------------------------------
# Option to upload a log
def Upload_Log(): 
    if ADDON.getSetting('email')=='':
        dialog.ok("No Email Address Set", "A new window will Now open for you to enter your Email address. The logfile will be sent here")
        ADDON.openSettings()
    uploadLog.Main()
#---------------------------------------------------------------------------------------------------
# Simple function to force refresh the repo's and addons folder
def Update_Repo():
    xbmc.executebuiltin( 'UpdateLocalAddons' )
    xbmc.executebuiltin( 'UpdateAddonRepos' )    
    xbmcgui.Dialog().ok('Force Refresh Started Successfully', 'Depending on the speed of your device it could take a few minutes for the update to take effect.')
    return
#-----------------------------------------------------------------------------------------------------------------
# Check to see if we can ping google.com or google.cn
def Connectivity_Check():
    try:
        Open_URL('http://google.com', 5)
    except:
        try:
            Open_URL('http://google.com', 5)
        except:
            try:
                Open_URL('http://google.com', 5)
            except:
                try:
                    Open_URL('http://google.cn', 5)
                except:
                    try:
                        Open_URL('http://google.cn', 5)
                    except:
                        dialog.ok("FAILED",'We tried to ping google and got no response. It looks like this device isn\'t connected to the internet.')
                        return
    dialog.ok("SUCCESS",'We tried to ping google and got a response. Great news it looks like this device is connected to the internet.')
#-----------------------------------------------------------------------------------------------------------------
# Thanks to Mikey1234 for some of these paths and also lambda for the clear cache option in genesis.
def Wipe_Cache():
    PROFILE_ADDON_DATA = os.path.join(xbmc.translatePath(os.path.join('special://profile','addon_data')))

    cachelist = [
        (PROFILE_ADDON_DATA),
        (ADDON_DATA),
        (os.path.join(HOME,'cache')),
        (os.path.join(HOME,'temp')),
        (os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')),
        (os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')),
        (os.path.join(ADDON_DATA,'script.module.simple.downloader')),
        (os.path.join(xbmc.translatePath(os.path.join('special://profile','addon_data','script.module.simple.downloader')))),
        (os.path.join(ADDON_DATA,'plugin.video.itv','Images')),
        (os.path.join(xbmc.translatePath(os.path.join('special://profile','addon_data','plugin.video.itv','Images'))))]

    for item in cachelist:
        if os.path.exists(item) and item != ADDON_DATA and item != PROFILE_ADDON_DATA:
            for root, dirs, files in os.walk(item):
                file_count = 0
                file_count += len(files)
                if file_count > 0:
                    for f in files:
                        try:
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                            xbmc.log("### Successfully cleared %s files from %s" % (+str(file_count), os.path.join(item,d)))
                        except:
                            xbmc.log("### Failed to wipe cache in: %s " % os.path.join(item,d))
        else:
            for root, dirs, files in os.walk(item):
                for d in dirs:
                    if 'Cache' in d or 'cache' in d or 'CACHE' in d:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                            xbmc.log("### Successfully wiped %s" % os.path.join(item,d))
                        except:
                            xbmc.log("### Failed to wipe cache in: %s" % os.path.join(item,d))

# Genesis cache - held in database file
    try:
        genesisCache = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.genesis'), 'cache.db')
        dbcon = database.connect(genesisCache)
        dbcur = dbcon.cursor()
        dbcur.execute("DROP TABLE IF EXISTS rel_list")
        dbcur.execute("VACUUM")
        dbcon.commit()
        dbcur.execute("DROP TABLE IF EXISTS rel_lib")
        dbcur.execute("VACUUM")
        dbcon.commit()
    except:
        pass
#-----------------------------------------------------------------------------------------------------------------
# Function to clear the addon_data
def Wipe_Kodi():
    stop = 0
    if dialog.yesno("ABSOLUTELY CERTAIN?!!!", 'Are you absolutely certain you want to wipe?', '', 'All addons and settings will be completely wiped!', yeslabel='YES, WIPE',nolabel='NO, STOP!'):
# Check Confluence is running before doing a wipe
        if skin!= "skin.confluence":
            dialog.ok('Default Confluence Skin Required','Please switch to the default Confluence skin before performing a wipe.')
            xbmc.executebuiltin("ActivateWindow(appearancesettings,return)")
            return
        else:
# Give the option to do a full backup before wiping
            if dialog.yesno("BACKUP EXISTING BUILD", 'Would you like to create a backup of your existing setup before proceeding?'):
                if USB == '':
                    dialog.ok('Please set your backup location before proceeding','You have not set your backup storage folder.\nPlease update the addon settings and try again.')
                    ADDON.openSettings(sys.argv[0])
                    if ADDON.getSetting('zip') == '' or not os.path.exists(ADDON.getSetting('zip')):
                        stop = 1
                        return
                if not stop:
                    CBPATH       = ADDON.getSetting('zip')
                    mybackuppath = os.path.join(CBPATH,'My_Builds')
                    if not os.path.exists(mybackuppath):
                        os.makedirs(mybackuppath)
                    vq = Get_Keyboard( heading="Enter a name for this backup" )
                    if ( not vq ): return False, 0
                    title = urllib.quote_plus(vq)
                    backup_zip = xbmc.translatePath(os.path.join(mybackuppath,title+'.zip'))
                    exclude_dirs_full =  ['plugin.program.nan.maintenance','plugin.program.tbs']
                    exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf','.gitignore']
                    message_header = "Creating full backup of existing build"
                    message1 = "Archiving..."
                    message2 = ""
                    message3 = "Please Wait"
                    Archive_Tree(HOME, backup_zip, message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)
            if not stop:
                keeprepos = dialog.yesno('DELETE REPOSITORIES?','Do you want to delete your repositories? Keeping bad repositories can be the cause of many problems, we recommend running Security Shield if you\'re in doubt.', yeslabel = 'KEEP REPOS', nolabel = 'DELETE REPOS')
                Wipe_Home(EXCLUDES)
                Wipe_Userdata()
                Wipe_Addons(keeprepos)
                Wipe_Addon_Data()
                Wipe_Home2(EXCLUDES)
                Kill_XBMC('wipe')
    else:
        return
#-----------------------------------------------------------------------------------------------------------------
# For loop to wipe files in special://home but leave ones in EXCLUDES untouched
def Wipe_Home(excludefiles):
    dp.create("Wiping Existing Content",'','Please wait...', '')
    for root, dirs, files in os.walk(HOME,topdown=True):
        dirs[:] = [d for d in dirs if d not in EXCLUDES]
        for name in files:
            try:                            
                dp.update(0,"Removing [COLOR=yellow]"+name+'[/COLOR]','','Please wait...')
                os.unlink(os.path.join(root, name))
                os.remove(os.path.join(root,name))
                os.rmdir(os.path.join(root,name))
            except:
                xbmc.log("Failed to remove file: %s" % name)
#-----------------------------------------------------------------------------------------------------------------
# Remove userdata folder
def Wipe_Userdata():
    userdatadirs=[name for name in os.listdir(USERDATA) if os.path.isdir(os.path.join(USERDATA, name))]
    try:
        for name in userdatadirs:
            try:
                if name not in EXCLUDES:
                    dp.update(0,"Cleaning Directory: [COLOR=yellow]"+name+' [/COLOR]','','Please wait...')
                    shutil.rmtree(os.path.join(USERDATA,name))
            except:
                print "Failed to remove: "+name
    except:
        pass

# Clean up userdata and leave items untouched that were set in addon settings
    for root, dirs, files in os.walk(USERDATA,topdown=True):
       dirs[:] = [d for d in dirs if d not in EXCLUDES]
       for name in files:
           try:                            
               dp.update(0,"Removing [COLOR=yellow]"+name+'[/COLOR]','','Please wait...')
               os.unlink(os.path.join(root, name))
               os.remove(os.path.join(root,name))
           except:
               xbmc.log("Failed to remove file: %s" % name)
#-----------------------------------------------------------------------------------------------------------------
# Remove addon directories
def Wipe_Addons(keeprepos):
    for name in os.listdir(ADDONS):
        if not keeprepos:
            if name not in EXCLUDES and not 'repo' in name:
                try:
                    dp.update(0,"Removing Add-on: [COLOR=yellow]"+name+' [/COLOR]','','Please wait...')
                    shutil.rmtree(os.path.join(ADDONS,name))
                except:
                    try:
                        os.remove(os.path.join(ADDONS,name))
                    except:
                        xbmc.log("Failed to remove: %s" % name)

        else:
            try:
                if name not in EXCLUDES:
                    dp.update(0,"Removing Add-on: [COLOR=yellow]"+name+' [/COLOR]','','Please wait...')
                    shutil.rmtree(os.path.join(ADDONS,name))
            except:
                try:
                    os.remove(os.path.join(ADDONS,name))
                except:
                    xbmc.log("Failed to remove: %s" % name)
#-----------------------------------------------------------------------------------------------------------------
# Remove addon_data
def Wipe_Addon_Data():
    for name in os.listdir(ADDON_DATA):
        try:
            dp.update(0,"Removing Add-on Data: [COLOR=yellow]"+name+' [/COLOR]','','Please wait...')
            shutil.rmtree(os.path.join(ADDON_DATA,name))
        except:
            try:
                os.remove(os.path.join(ADDON_DATA,name))
            except:
                xbmc.log("Failed to remove: %s" % name)
#-----------------------------------------------------------------------------------------------------------------
# Clean up everything in the home path
def Wipe_Home2(excludefiles):
    homepath=[name for name in os.listdir(HOME) if os.path.isdir(os.path.join(HOME, name))]
    try:
        for name in homepath:
            try:
                if name not in excludefiles:
                    dp.update(0,"Cleaning Directory: [COLOR=yellow]"+name+' [/COLOR]','','Please wait...')
                    shutil.rmtree(os.path.join(HOME,name))
            except:
                print "Failed to remove: "+name
    except:
        pass
#-----------------------------------------------------------------------------------------------------------------
# Report back with the version of Kodi installed
def XBMC_Version(url):
    xbmc_version = xbmc.getInfoLabel("System.BuildVersion")
    version      = float(xbmc_version[:4])
    homearray    = HOME.split(os.sep)
    xbmc.log(str(homearray))
    arraylen     = len(homearray)
    koditype     = homearray[arraylen-1]
    if koditype == '':
        koditype = homearray[arraylen-2]
    koditype     = koditype.replace('.','').upper()
    dialog.ok('You are running: %s'%koditype, "Your version is: %s" % version)
#-----------------------------------------------------------------------------------------------------------------
#Addon starts here
params      = Get_Params()
description = None
fanart      = None
mode        = None
name        = None
url         = None
video       = None

try:
    description=urllib.unquote_plus(params["description"])
except:
    pass
try:
    fanart=urllib.unquote_plus(params["fanart"])
except:
    pass
try:
    iconimage=urllib.unquote_plus(params["iconimage"])
except:
    pass
try:
    mode=str(params["mode"])
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    pass
try:
    url=urllib.unquote_plus(params["url"])
except:
    pass
try:
    video=urllib.unquote_plus(params["video"])
except:
    pass


if mode == None : Tools()
elif mode == 'ASCII_Check'        : ASCII_Check()
elif mode == 'addon_removal_menu' : Addon_Removal_Menu()
elif mode == 'backup'             : BACKUP()
elif mode == 'backup_option'      : Backup_Option()
elif mode == 'backup_restore'     : Backup_Restore()
elif mode == 'browse_repos'       : Browse_Repos()
elif mode == 'check_storage'      : checkPath.check(direct)
elif mode == 'clear_cache'        : Clear_Cache()
elif mode == 'community_backup_2' : Community_Backup_OLD()
elif mode == 'delete_path'        : Delete_Path(url)
elif mode == 'fix_special'        : Fix_Special(url)
elif mode == 'full_backup'        : Full_Backup()
elif mode == 'full_clean'         : Full_Clean()
elif mode == 'gotham'             : Gotham_Confirm()
elif mode == 'helix'              : Helix_Confirm()
elif mode == 'hide_menu'          : Hide_Menu(url)
elif mode == 'hide_passwords'     : Hide_Passwords()
elif mode == 'ipcheck'            : IP_Check()
elif mode == 'install_from_zip'   : Install_From_Zip()
elif mode == 'kill_xbmc'          : Kill_XBMC()
elif mode == 'kodi_settings'      : Kodi_Settings()
elif mode == 'local_backup'       : Local_Backup()
elif mode == 'log'                : Log_Viewer()
elif mode == 'open_system_info'   : Open_System_Info()
elif mode == 'open_filemanager'   : Open_Filemanager()
elif mode == 'openelec_backup'    : OpenELEC_Backup()
elif mode == 'openelec_settings'  : OpenELEC_Settings()
elif mode == 'play_video'         : yt.PlayVideo(url)
elif mode == 'remove_addon_data'  : Remove_Addon_Data()
elif mode == 'remove_addons'      : Remove_Addons(url)
elif mode == 'remove_build'       : Remove_Build()
elif mode == 'remove_crash_logs'  : Remove_Crash_Logs()
elif mode == 'remove_packages'    : Remove_Packages()
elif mode == 'remove_textures'    : Remove_Textures_Dialog()
elif mode == 'restore_backup'     : Restore_Backup_XML(name,url,description)
elif mode == 'restore_local_CB'   : Restore_Local_Community(url)
elif mode == 'restore_local_gui'  : Restore_Local_GUI()
elif mode == 'restore_local_OE'   : Restore_OpenELEC_Local()
elif mode == 'restore_openelec'   : Restore_OpenELEC(name,url,video)
elif mode == 'restore_option'     : Restore_Option()
elif mode == 'restore_zip'        : Restore_Zip_File(url)         
elif mode == 'run_addon'          : Run_Addon(url)
elif mode == 'runtest'            : speedtest.runtest(url)
elif mode == 'speed_instructions' : Speed_Instructions()
elif mode == 'speedtest_menu'     : Speed_Test_Menu()
elif mode == 'text_guide'         : Text_Guide(url)
elif mode == 'tools'              : Tools()
elif mode == 'tools_addons'       : Tools_Addons()
elif mode == 'tools_clean'        : Tools_Clean()
elif mode == 'tools_misc'         : Tools_Misc()
elif mode == 'unhide_passwords'   : Unhide_Passwords()
elif mode == 'update'             : Update_Repo()
elif mode == 'uploadlog'          : Upload_Log()
elif mode == 'xbmcversion'        : XBMC_Version(url)
elif mode == 'wipe_xbmc'          : Wipe_Kodi()
xbmcplugin.endOfDirectory(int(sys.argv[1]))
