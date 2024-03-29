# Copyright (C) 2016 Lee Randall (whufclee)
#
#  IMPORTANT:
#  You are free to use this code under the rules set our in the license below
#  however under NO circumstances should you remove this license!
#
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

# Global imports
import xbmc, xbmcgui, os, xbmcaddon
import time, datetime
import xml.etree.ElementTree as ET
from sqlite3 import dbapi2 as sqlite

# Global variables
AddonID     =  'script.tvportal'
ADDON       =  xbmcaddon.Addon(id=AddonID)
ADDONS      =  xbmc.translatePath('special://home/addons/')
USERDATA    =  xbmc.translatePath('special://profile/')
ADDON_DATA  =  xbmc.translatePath(os.path.join(USERDATA,'addon_data'))
dbpath      =  xbmc.translatePath(os.path.join(ADDON_DATA,AddonID,'program.db'))
xmlpath     =  ADDON.getSetting('xmlpath')
dialog      =  xbmcgui.Dialog()
updateicon  =  os.path.join(ADDONS,AddonID,'resources','update.png')
stop        =  0
chanchange  =  0
catschange  =  0
listpercent =  1
listcount   =  1

##########################################################################################
# Function to convert timestamp into proper integer that can be used for schedules
def Time_Convert(starttime):
# Split the time from the string that also contains the time difference
    starttime, diff  = starttime.split(' ')

    year             = starttime[:4]
    month            = starttime[4:6]
    day              = starttime[6:8]
    hour             = starttime[8:10]
    minute           = starttime[10:12]
    secs             = starttime[12:14]

# Convert the time diff factor into an integer we can work with
    diff             = int(diff[:-2])

    starttime        = datetime.datetime(int(year),int(month),int(day),int(hour),int(minute),int(secs))
    starttime        = starttime + datetime.timedelta(hours=diff)
    starttime        = time.mktime(starttime.timetuple())

    return int(starttime)
##########################################################################################
# Initialise the database calls
def DB_Open():
    global cur
    global con
    con = sqlite.connect(dbpath)
    cur = con.cursor()
##########################################################################################
# Main insert/update sqlite queries
def updateDB(chanlist):
    entryexists = 0
    cur.execute('PRAGMA temp_store=MEMORY;')
    cur.execute('PRAGMA journal_mode=MEMORY;')
#    cur.execute('PRAGMA synchronous=OFF;')
    cur.execute('select channel, start_date, image_small from programs where channel LIKE "'+str(chanlist[0])+'" and start_date="'+str(chanlist[2])+'";')
    try:
        row = cur.fetchone()
        if row:
            entryexists = 1
    except:
        pass

    if entryexists == 1:
        try:
            cur.execute('update programs set channel=?, title=?, start_date=?, end_date=?, description=?, image_large=?, image_small=?, source=?, subTitle=? where channel LIKE "'+str(chanlist[0])+'" and start_date="'+str(chanlist[2])+'";', chanlist)
            con.commit()
        except:
            pass

    else:
        try:
            cur.execute("insert into programs (channel, title, start_date, end_date, description, image_large, image_small, source, subTitle) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", chanlist )
            con.commit()
        except:
            pass
##########################################################################################
### ADDON STARTS HERE ###
# Check database isn't locked and continue if possible
try:
    os.remove(os.path.join(ADDON_DATA, AddonID, 'settings.cfg'))
except:
    print"No settings.cfg file to remove"
if os.path.exists(dbpath):
    try:
        os.rename(dbpath,dbpath+'1')
        os.rename(dbpath+'1',dbpath)
        print"Database not in use, we can continue"
    except:
        print"### Database in use, Kodi needs a restart, if that doesn't work you'll need to restart your system."
        dialog.ok(ADDON.getLocalizedString(30813),ADDON.getLocalizedString(30814))
        stop = 1

if stop == 0:
    xbmc.executebuiltin("XBMC.Notification("+ADDON.getLocalizedString(30807)+","+ADDON.getLocalizedString(30811)+",10000,"+updateicon+")")
#    xbmc.executebuiltin("ActivateWindow(busydialog)")
    tree        =  ET.parse(xmlpath)
    root        =  tree.getroot()
    channels     = root.findall("./channel")
    channelcount = len(channels)
    programmes   = root.findall("./programme")
    listingcount = len(programmes)
    choice = 0
    try:
        cur.close()
        con.close()
    except:
        print "Database not open, we can continue"
    if os.path.exists(dbpath):
        choice = dialog.yesno('Fresh Listings OR Update?','[COLOR=dodgerblue]'+str(listingcount)+"[/COLOR] programmes in [COLOR=dodgerblue]"+str(channelcount)+"[/COLOR] channels found.",'Do you want to do a clean update of the listings or are you just adding more channels from another xml?',yeslabel='Fresh Listings',nolabel='Adding Channels')
        if choice == 1:
            try:
                os.remove(dbpath)
                print "### Successfully deleted database"
            except:
                print "### FAILED: Database in use, Kodi needs a restart. If that doesn't work you'll need to restart your system."
                dialog.ok(ADDON.getLocalizedString(30813),ADDON.getLocalizedString(30814))
                stop = 1
    xbmc.executebuiltin("Dialog.Close(busydialog)")
    if (choice == 1) or (not os.path.exists(dbpath)):
# Create the main database
        DB_Open()
        try:
            cur.execute('create table programs(channel TEXT, title TEXT, start_date TIMESTAMP, end_date TIMESTAMP, description TEXT, image_large TEXT, image_small TEXT, source TEXT, subTitle TEXT)')
        except:
            print"### Valid program.db file exists"
        cur.close()
        con.close()

# If database is not locked lets continue
    if stop == 0:

# Read main chan.xml into memory so we can add any new channels
        chanxml     = open(os.path.join(ADDON_DATA,AddonID,'chan.xml'),'r')
        content     = chanxml.read()
        chanxml.close()

        writefile   = open(os.path.join(ADDON_DATA,AddonID,'chan.xml'),'w+')
        replacefile = content.replace('</tv>','')
        writefile.write(replacefile)
        writefile.close()
        writefile   = open(os.path.join(ADDON_DATA,AddonID,'chan.xml'),'a')

# Read cats.xml into memory so we can add any new channels
        catsxml     = open(os.path.join(ADDON_DATA,AddonID,'cats.xml'),'r')
        content2    = catsxml.read()
        catsxml.close()

        writefile2  = open(os.path.join(ADDON_DATA,AddonID,'cats.xml'),'w+')
        replacefile = content2.replace('</Document>','')
        writefile2.write(replacefile)
        writefile2.close()
        writefile2  = open(os.path.join(ADDON_DATA,AddonID,'cats.xml'),'a')

# Set a temporary list matching channel id with real name
        print "Creating List of channels"
        tempchans    = []
        print"### Channels Found: "+str(channelcount)
        xbmc.executebuiltin("XBMC.Notification("+ADDON.getLocalizedString(30816)+str(channelcount)+","+ADDON.getLocalizedString(30812)+",10000,"+updateicon+")")
        for channel in channels:
            channelid = channel.get("id")
            displayname = channel.find('display-name').text.encode('ascii', 'ignore')

# Block no longer used, we could put a rule in to check if every channel starts with a digit. If it does then rename accordingly
# Strip out any starting digits but only if the digits are followed by a space
#            if displayname[0].isdigit() and displayname[1] == ' ':
#                displayname = displayname[2:]
#            if displayname[0].isdigit() and displayname[1].isdigit() and displayname[2] == ' ':
#                displayname = displayname[3:]
#            if displayname[0].isdigit() and displayname[1].isdigit() and displayname[2].isdigit() and displayname[3] == ' ':
#                displayname = displayname[4:]
#            if displayname[0].isdigit() and displayname[1].isdigit() and displayname[2].isdigit() and displayname[3].isdigit() and displayname[4] == ' ':
#                displayname = displayname[4:]
            tempchans.append([channelid,displayname])
# Add channel to chan.xml file
            if not displayname in content:
                writefile.write('  <channel id="'+displayname+'">\n\t<display-name lang="en">'+displayname+'</display-name>\n  </channel>\n')
# Add channel to cats.xml file
            if not displayname in content2:
                writefile2.write(' <cats>\n\t<category>Uncategorised</category>\n\t<channel>'+displayname+'</channel>\n </cats>\n')

        writefile.write('</tv>')
        writefile.close()
        writefile2.write('</Document>')
        writefile2.close()
# Open database ready for writing contents
        DB_Open()

# Loop through and grab each channel listing and add to array
        xbmc.executebuiltin("XBMC.Notification("+ADDON.getLocalizedString(30815)+","+ADDON.getLocalizedString(30812)+",10000,"+updateicon+")")
        currentlist  = []
        print"### Total Listings to scan in: "+str(listingcount)
        xbmc.executebuiltin("XBMC.Notification("+ADDON.getLocalizedString(30816)+"[COLOR=dodgerblue]"+str(listingcount)+"[/COLOR],"+ADDON.getLocalizedString(30812)+",10000,"+updateicon+")")
        for programme in programmes:
            try:
                icon = 'special://home/addons/'+AddonID+'/resources/dummy.png'
                starttime  = programme.get("start")
                starttime2 = Time_Convert(starttime)
                endtime    = programme.get("stop")
                endtime2   = Time_Convert(endtime)
                channel    = programme.get("channel").encode('ascii', 'ignore')
#                print "### Channel: "+channel
                try:
                    title  = programme.find('title').text.encode('ascii', 'ignore')
                except:
                    title = "No information available"
#                print"### Title: "+title
                try:
                    subtitle = programme.find('sub-title').text.encode('ascii', 'ignore')
                except:
                    subtitle = ''
#                print"### Subtitle: "+subtitle
#                try:
                desc = programme.findtext('desc', default='No programme information available').encode('ascii', 'ignore')
                for icon in programme.iter('icon'):
                    icon = str(icon.attrib).replace("{'src': '",'').replace("'}",'')

# Convert the channel id to real channel name
                for matching in tempchans:
                    if matching[0] == channel:
                        currentlist.append(matching[1])

# Add rest of data to list
                currentlist.extend([title, starttime2, endtime2, desc, '', icon, 'dixie.ALL CHANNELS', ''])
                updateDB(currentlist)
                currentlist[:] = []
                listcount += 1

            except:
                try:
                    print"### FAILED to pull details for item: "+str(title)+": "+str(subtitle)
                except:
                    print"### FAILED to import #"+str(listcount)
                listcount += 1

                if listcount == int(listingcount/100):
                    print"### "+str(listpercent)+" percent of TV guide imported"
                    xbmc.executebuiltin('Notification('+ADDON.getLocalizedString(30815)+','+str(listpercent)+' percent of scan complete,5000,'+updateicon+')')
                    listcount = 0
                    listpercent = listpercent+1
#        cur.execute('PRAGMA synchronous=1;')
        cur.close()
        con.close()
        openepg = dialog.yesno(ADDON.getLocalizedString(30819),ADDON.getLocalizedString(30820))
        if openepg:
            xbmc.executebuiltin('RunAddon('+AddonID+")'")