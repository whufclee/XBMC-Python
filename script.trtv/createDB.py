# TotalRevolution TV EPG Converter
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

# Global imports
import xbmc, xbmcgui, os, xbmcaddon, sys, urllib2, urllib
import time, datetime, re, shutil, csv, hashlib, binascii
import dixie, sfile, download
import calendar as cal
import koding

from sqlite3 import dbapi2 as sqlite
from time import mktime

import sys, traceback

# Global variables
AddonID      =  'script.trtv'
ADDON        =  xbmcaddon.Addon(id=AddonID)
ADDONS       =  xbmc.translatePath('special://home/addons/')
USERDATA     =  xbmc.translatePath('special://profile/')
ADDON_DATA   =  os.path.join(USERDATA,'addon_data')
dbpath       =  os.path.join(ADDON_DATA,AddonID,'program.db')
dialog       =  xbmcgui.Dialog()
dp           =  xbmcgui.DialogProgress()
updateicon   =  os.path.join(ADDONS,AddonID,'resources','update.png')
chanxmlfile  =  os.path.join(ADDON_DATA,AddonID,'chan.xml')
catsxfile    =  os.path.join(ADDON_DATA,AddonID,'cats.xml')
xmlmaster    =  os.path.join(ADDONS,AddonID,'resources','chan.xml')
catsmaster   =  os.path.join(ADDONS,AddonID,'resources','cats.xml')
csvfile      =  os.path.join(ADDON_DATA,AddonID,'programs.csv')
tempxml      =  os.path.join(ADDON_DATA,AddonID,'temp.xml')
tempurl      =  os.path.join(ADDON_DATA,AddonID,'listcheck')
path         =  dixie.GetChannelFolder()
chan         =  os.path.join(path, 'channels')
log_path     =  xbmc.translatePath('special://logpath/')
stop         =  0
chanchange   =  0
catschange   =  0
errorlist    = ['none']

countryarray =  [['AF','Afghanistan'],['AL','Albania'],['DZ','Algeria'],['AO','Angola'],['AR','Argentina'],['AM','Armenia'],['AU','Australia'],
                ['AT','Austria'],['AZ','Azerbaijan'],['BS','Bahamas'],['BY','Belarus'],['BE','Belgium'],['BO','Bolivia'],['BA','Bosnia'],['BR','Brazil'],
                ['BG','Bulgaria'],['KM','Cambodia'],['CM','Cameroon'],['CA','Canada'],['CL','Chile'],['CN','China'],['CO','Colombia'],['CR','Costa Rica'],
                ['HR','Croatia'],['CU','Cuba'],['CY','Cyprus'],['CZ','Czech Republic'],['DK','Denmark'],['DO','Dominican Republic'],['EC','Ecuador'],['EG','Egypt'],
                ['SV','El Salvador'],['EE','Estonia'],['ET','Ethiopia'],['FI','Finland'],['FR','France'],['GA','Gabon'],['GM','Gambia'],['GE','Georgia'],
                ['DE','Germany'],['GH','Ghana'],['GR','Greece'],['GT','Guatemala'],['GN','Guinea'],['HT','Haiti'],['HN','Honduras'],['HK','Hong Kong'],
                ['HU','Hungary'],['IS','Iceland'],['IN','India'],['ID','Indonesia'],['IR','Iran'],['IQ','Iraq'],['IE','Ireland'],['IL','Israel'],['IT','Italy'],
                ['CI','Ivory Coast'],['JM','Jamaica'],['JP','Japan'],['JO','Jordan'],['KZ','Kazakhstan'],['KE','Kenya'],['XK','Kosovo'],['KW','Kuwait'],
                ['KG','Kyrgyzstan'],['LA','Laos'],['LV','Latvia'],['LB','Lebanon'],['LR','Liberia'],['LY','Libya'],['LI','Liechstenstein'],['LT','Lithuania'],
                ['LU','Luxembourg'],['MK','Macedonia'],['MG','Madagascar'],['MW','Malawi'],['MY','Malaysia'],['ML','Mali'],['MT','Malta'],['MU','Mauritius'],
                ['MX','Mexico'],['MD','Moldova'],['MN','Mongolia'],['ME','Montenegro'],['MA','Morocco'],['MZ','Mozambique'],['MM','Myanmar'],['NA','Namibia'],
                ['NP','Nepal'],['NL','Netherlands'],['NZ','New Zealand'],['NI','Nicaragua'],['NE','Niger'],['NG','Nigeria'],['NO','Norway'],['OM','Oman'],
                ['PK','Pakistan'],['PS','Palestine'],['PA','Panama'],['PY','Paraguay'],['PE','Peru'],['PH','Philippines'],['PL','Poland'],['PT','Portugal'],
                ['PR','Puerto Rico'],['QA','Qatar'],['RO','Romania'],['RU','Russia'],['RW','Rwanda'],['SA','Saudi Arabia'],['SN','Senegal'],['RS','Serbia'],
                ['SL','Sierra Leone'],['SG','Singapore'],['SK','Slovakia'],['SI','Slovenia'],['SO','Somalia'],['ZA','South Africa'],['KR','South Korea'],
                ['SS','South Sudan'],['ES','Spain'],['LK','Sri Lanka'],['SD','Sudan'],['SR','Suriname'],['SE','Sweden'],['CH','Switzerland'],['SY','Syria'],
                ['TW','Taiwan'],['TJ','Tajikistan'],['TZ','Tanzania'],['TH','Thailand'],['TG','Togo'],['TT','Trinidad and Tobago'],['TN','Tunisia'],['TR','Turkey'],
                ['TM','Turkmenistan'],['UG','Uganda'],['UA','Ukraine'],['AE','United Arab Emireates'],['GB','United Kingdom'],['US','United States'],['UY','Uruguay'],
                ['UZ','Uzbekistan'],['VE','Venezuela'],['VN','Vietnam'],['YE','Yemen'],['ZM','Zambia'],['ZW','Zimbabwe']]
##########################################################################################
# Check if the online file date has changed
def Check_Date(url):
    if not 'github' in url:
        req = urllib2.Request(url)
        req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        conn = urllib2.urlopen(req)
        last_modified = conn.info().getdate('last-modified')
        last_modified = time.strftime('%Y%m%d%H%M%S', last_modified)
        dixie.log("Last modified: "+last_modified)

    else:
        url = url.replace('raw.githubusercontent', 'github').replace('master/','blob/master/')
        content = Open_URL(url).replace('\r','').replace('\n','').replace('\t','')
        update_match = re.compile('<relative-time datetime="(.+?)"').findall(content)
        try:
            last_modified = update_match[0]
        except:
            last_modified = '0'

    return last_modified
##########################################################################################
# Clean up the database and remove stale listings
def Clean_DB():
# Set paramaters to check in db, cull = the datetime (we've set it to 12 hours in past)
    starttime = datetime.datetime.today() - datetime.timedelta(hours=12)
    cull      = int(time.mktime(starttime.timetuple()))

    DB_Open()
    xbmc.executebuiltin("ActivateWindow(busydialog)")
    xbmc.executebuiltin("XBMC.Notification("+ADDON.getLocalizedString(30837)+","+ADDON.getLocalizedString(30838)+",5000,"+updateicon+")")
    cur.execute("DELETE FROM programs WHERE end_date < "+str(cull))
    cur.execute("VACUUM")
    con.commit()
    cur.close()
    xbmc.executebuiltin('Dialog.Close(busydialog)')
##########################################################################################
# Return a clean filename that won't cause errors
def CleanFilename(text):
    text = text.replace(' *',                  '*')
    text = text.replace(' +',                  '+')
    text = text.replace(' HDTV',                '')
    text = text.replace(' HD',                  '')
    text = text.replace(' SDTV',                '')
    text = text.replace(' SD ',                 '')
    text = text.replace(' (EAST)',              '')
    text = text.replace(' (WEST)',              '')
    text = text.replace('ROGERS ',              '')
    text = text.replace('THE SPORTS NETWORK','TSN')
    text = text.replace(' CANADA',              '')
    text = text.replace('(CANADA)',             '')
    text = text.replace('>',                    '')
    text = text.replace('_',                   ' ')

    text = re.sub('[:\\/?\<>|"]', '', text)
    text = text.strip()
    try:
        text = text.encode('ascii', 'ignore')
    except:
        text = text.decode('utf-8').encode('ascii', 'ignore')
    text = text.upper()
    return text.replace('&AMP;','&amp;').replace('&GT;','&gt;')
##########################################################################################
# Return a clean filename that won't cause errors
def CleanDBname(text):
    text = text.replace('*', '_STAR')
    text = text.replace('+', '_PLUS')
    text = text.replace(' ', '_')

    try:
        text = text.encode('ascii', 'ignore')
    except:
        text = text.decode('utf-8').encode('ascii', 'ignore')
    text = text.upper()
    dixie.log('Converted: %s'%text.replace('&AMP;','&'))
    return text.replace('&AMP;','&')
#########################################################################################
def Convert_ISO(mycountry):
    for iso in countryarray:
        if mycountry == iso[1]:
            mycountry = iso[0]
            break
    return mycountry
#########################################################################################
# Create the main database
def Create_DB():
    if not os.path.exists(dbpath):
        DB_Open()
        versionvalues = [1,4,1]
        try:
            cur.execute('CREATE TABLE programs(channel TEXT, title TEXT, start_date TIMESTAMP, end_date TIMESTAMP, description TEXT, image_large TEXT, image_small TEXT, source TEXT, subTitle TEXT, season TEXT, episode TEXT, is_movie TEXT, language TEXT)')
            con.commit()
            cur.execute('create table updates(id INTEGER, source TEXT, date TEXT, programs_updated TIMESTAMP, PRIMARY KEY(id));')
            con.commit()
            cur.execute('create table version(major INTEGER, minor INTEGER, patch INTEGER);')
            con.commit()
            cur.execute('create table xmls(id INTEGER, size INTEGER);')
            con.commit()
            cur.execute("insert into version (major, minor, patch) values (?, ?, ?);", versionvalues)
            con.commit()

        except:
            dixie.log("### Valid program.db file exists")

        cur.close()
        con.close()
##########################################################################################
# Create CSV for import and update chan.xml and cats.xml
def Create_CSV(channels,channelcount,listingcount,programmes,xsource,offset,xnumber):
    listpercent =  1
    listcount   =  1
    mode        =  1
    usecountry  =  ADDON.getSetting('usecountry%s' % xnumber)
    country     =  ADDON.getSetting('country%s' % xnumber)
    dixie.log('### country: %s' % country)
    for item in countryarray:
        if item[1] == country:
            country =  item[0]
    dixie.log('### country code: %s' % country)
    if os.path.exists(dbpath):
        mode = 2
    xbmc.executebuiltin("Dialog.Close(busydialog)")

# Read main chan.xml into memory so we can add any new channels
    if not os.path.exists(chanxmlfile):
        writefile   = open(chanxmlfile,'w+')
        writefile.write('<?xml version="1.0" encoding="UTF-8"?>\n<tv>\n</tv>\n')
        writefile.close()

    if not os.path.exists(catsxfile):
        writefile   = open(catsxfile,'w+')
        writefile.write('<?xml version="1.0" encoding="UTF-8"?>\n<Document>\n</Document>\n')
        writefile.close()

    chanxml     =  open(chanxmlfile,'r')
    content     = chanxml.read()
    chanxml.close()

    writefile   = open(chanxmlfile,'w+')
    replacefile = content.replace('</tv>','')
    writefile.write(replacefile)
    writefile.close()
    writefile   = open(chanxmlfile,'a')

# Read cats.xml into memory so we can add any new channels
    catsxml     = open(catsxfile,'r')
    content2    = catsxml.read()
    catsxml.close()

    writefile2  = open(catsxfile,'w+')
    replacefile = content2.replace('</Document>','')
    writefile2.write(replacefile)
    writefile2.close()
    writefile2  = open(catsxfile,'a')

# Set a temporary list matching channel id with real name
    dixie.log("Creating List of channels")
    tempchans   = []
    idarray     = []
    newchans    = []
    dixie.log("Channels Found: "+str(channelcount))
    xbmc.executebuiltin("XBMC.Notification("+ADDON.getLocalizedString(30816)+str(channelcount)+","+ADDON.getLocalizedString(30812)+",10000,"+updateicon+")")
    for channel in channels:
        donotadd    = 0
        channelid   = re.compile('channel id="(.+?)"').findall(channel)[0]
        displayname = re.compile('<display-name.*>(.+?)<\/display-name>').findall(channel)

        if xsource.replace("'",'') == 'BDS' or len(displayname) < 4:
            displayname = displayname[0].encode('ascii', 'ignore').replace('\n','').replace("'",'').replace(",",'').replace(".",'').upper().replace('&','&amp;')
        else:
            displayname = displayname[3].encode('ascii', 'ignore').replace('\n','').replace("'",'').replace(",",'').replace(".",'').upper().replace('&','&amp;')
        if  displayname=='INDEPENDENT' or 'AFFILIATE' in displayname or displayname=='SATELLITE' or displayname=='SPORTS SATELLITE' or 'PPV' in displayname or 'SKYCUST' in displayname or 'PAID PROGRAMMING' in displayname or 'VOD ' in displayname:
            donotadd = 1
        newdisplay = CleanFilename(displayname)
        if usecountry == 'true' or int(xnumber) > 10:
            newdisplay += (' (%s)' % country)
        if not newdisplay in newchans and donotadd == 0:

# Add channel to chan.xml file
            if not '<channel id="'+str(newdisplay)+'">' in content:
                writefile.write('  <channel id="'+newdisplay+'">\n    <display-name lang="en">'+newdisplay+'</display-name>\n  </channel>\n')
# Add channel to cats.xml file
            if not '<channel>'+str(newdisplay)+'</channel>' in content2:
                writefile2.write(' <cats>\n    <category>Uncategorised</category>\n    <channel>'+newdisplay+'</channel>\n </cats>\n')
            tempchans.append([channelid,newdisplay,displayname])
            newchans.append(newdisplay)
            idarray.append(channelid)
        else:
            dixie.log("### Duplicate channel - skipping "+str(newdisplay))
    
    xbmc.log('#### idarray: %s' % idarray)

    writefile.write('</tv>')
    writefile.close()
    writefile2.write('</Document>')
    writefile2.close()

# Loop through and grab each channel listing and add to array
    xbmc.executebuiltin("XBMC.Notification("+ADDON.getLocalizedString(30815)+","+ADDON.getLocalizedString(30812)+",10000,"+updateicon+")")
    currentlist  = []
    dixie.log("Total Listings to scan in: "+str(listingcount))
    xbmc.executebuiltin("XBMC.Notification("+ADDON.getLocalizedString(30818)+"[COLOR=dodgerblue]"+str(listingcount)+"[/COLOR],"+ADDON.getLocalizedString(30812)+",10000,"+updateicon+")")
    writetofile = open(csvfile,'w+')
    dp.create(ADDON.getLocalizedString(30984),'',ADDON.getLocalizedString(30815),'')
    writetofile.write('channel,title,start_date,end_date,description,image_large,image_small,source,subTitle,season,'
                      'episode,is_movie,language')
    for programme in programmes:
        try:
            channel    = re.compile('channel="(.+?)"').findall(programme)[0]
            if channel in str(idarray):
#                channel = channel.encode('ascii', 'ignore').replace(' ','_')
                starttime  = re.compile('start="(.+?)"').findall(programme)[0]
                starttime2 = Time_Convert(starttime,xsource,offset)
                endtime    = re.compile('stop="(.+?)"').findall(programme)[0]
                endtime2   = Time_Convert(endtime,xsource,offset)
                try:
                    title  = re.compile('title.*">(.+?)<\/title>').findall(programme)[0].encode('ascii', 'ignore').replace(',','.').replace('"','&quot;')
                except:
                    title = "No information available"
                try:
                    subtitle = re.compile('<sub-title.*>(.+?)<\/sub-title>').findall(programme)[0].encode('ascii', 'ignore').replace(',','.').replace('"','&quot;')
                except:
                    subtitle = ''
                try:
                    desc = re.compile('<desc.*>(.+?)<\/desc>').findall(programme)[0].encode('ascii', 'ignore').replace(',','.').replace('"','&quot;')
                except:
                    desc = 'No information available'
                try:
                    icon = re.compile('<icon src="(.+?)"').findall(programme)[0]
                except:
                    icon = 'special://home/addons/'+AddonID+'/resources/dummy.png'

                season = "None"
                episode = "None"
                is_movie = "None"
                language = re.compile('title.*lang="(.*).*">.+?<\/title>').findall(programme)[0]
                episode_nums = re.compile('<episode-num.*>(.+?)<\/episode-num>').findall(programme)
                program_categories = re.compile('<category.*>(.+?)<\/category>').findall(programme)
                for category in program_categories:
                    if "movie" in category.lower() or channel.lower().find("sky movies") != -1 \
                            or "film" in category.lower():
                        is_movie = "Movie"
                        break

                for episode_num in episode_nums:
                    episode_num = episode_num.encode('ascii', 'ignore')
                    if str.find(episode_num, ".") != -1:
                        splitted = str.split(episode_num, ".")
                        if splitted[0] != "":
                            season = str(int(splitted[0]) + 1)
                            is_movie = "None"  # fix for misclassification
                            if str.find(splitted[1], "/") != -1:
                                episode = str(int(splitted[1].split("/")[0]) + 1)
                            elif splitted[1] != "":
                                episode = str(int(splitted[1]) + 1)
                        break

                    elif str.find(episode_num.lower(), "season") != -1 and episode_num != "Season ,Episode ":
                        pattern = re.compile(r"Season\s(\d+).*?Episode\s+(\d+).*", re.I | re.U)
                        season = re.sub(pattern, r"\1", episode_num)
                        episode = re.sub(pattern, r"\2", episode_num)
                        break


# Convert the channel id to real channel name
                for matching in tempchans:
                    if matching[0] == channel:
                        cleanchan = CleanDBname(matching[1])
                        writetofile.write('\n"'+str(cleanchan)+'","'+str(title)+'",'+str(starttime2)+','+str(endtime2)+',"'+str(desc)+'",,'+str(icon)+',dixie.ALL CHANNELS,'+subtitle+',"'+
                                          season+'","'+episode+'","'+is_movie+'","'+language+'",')

                listcount += 1
                if listcount == int(listingcount/100):
                    listcount = 0
                    dp.update(listpercent,'','','')
                    listpercent +=1
            else:
                listcount += 1
                if listcount == int(listingcount/100):
                    listcount = 0
                    dp.update(listpercent,'','','')
                    listpercent +=1

        except:
            try:
                dixie.log("FAILED to pull details for item: "+str(title)+": "+str(subtitle))
            except:
                dixie.log("FAILED to import #"+str(listcount))
                listcount += 1
                if listcount == int(listingcount/100):
                    listcount = 0
                    dp.update(listpercent,'','','')
                    listpercent +=1
    writetofile.close()
    Import_CSV(mode)
##########################################################################################
# Initialise the database calls
def DB_Open():
    global cur
    global con
    con = sqlite.connect(dbpath)
    cur = con.cursor()
##########################################################################################
# Attempt to fix badly formed XML files with special characters in
def Fix_XML(errorline):
    dixie.log("FIX_XML Function started")
    counter = 1
    rawfile = open(xmlpath,"r")
    lines = rawfile.readlines()
    rawfile.close()

    newfile = open(xmlpath,'w')
    for line in lines:
        counterstr = str(counter)
        if counterstr == errorline:
            dixie.log("Removing Line "+counterstr)
        else:
            newfile.write(line)
        counter += 1
##########################################################################################
# Work out how many days worth of guides we have available
def Get_Dates():
    DB_Open()
    emptydb  = 0
    datelist = []
    cur.execute("SELECT MIN(start_date) FROM programs;")
    mindate  = cur.fetchone()[0]

    mindate = datetime.datetime.fromtimestamp(mindate)
    year1   = str(mindate)[:4]
    month1  = str(mindate)[5:7]
    day1    = str(mindate)[8:10]


    cur.execute("SELECT MAX(start_date) FROM programs;")
    maxdate = cur.fetchone()[0]
    dixie.log("maxdate: "+str(maxdate))

    maxdate = datetime.datetime.fromtimestamp(maxdate)
    year2   = str(maxdate)[:4]
    month2  = str(maxdate)[5:7]
    day2    = str(maxdate)[8:10]

    d1      = datetime.date(int(year1), int(month1), int(day1))
    d2      = datetime.date(int(year2), int(month2), int(day2))
    diff    = d2 - d1
    dixie.log("Successfully grabbed dates, now inserting into db")

# Grab the time now so we can update the db with timestamp
    nowtime     = cal.timegm(datetime.datetime.timetuple(datetime.datetime.now()))
    cleantime   = str(nowtime)

# Insert our dates into the db so the epg can scroll forward in time
    for i in range(diff.days + 1):
        newdate = (d1 + datetime.timedelta(i)).isoformat()
        cur.execute("SELECT COUNT(*) from updates where date LIKE '"+newdate+"';")
        data = cur.fetchone()[0]
        if data:
            dixie.log("Attempting to update records for: "+str(newdate))
            cur.execute('update updates set source=?, date=?, programs_updated=? where date LIKE "'+str(newdate)+'";', ['dixie.ALL CHANNELS',str(newdate),cleantime])
            con.commit()
            dixie.log("Successfully updated rows")
        else:
            dixie.log("New date in db, lets create new entries")
            cur.execute("insert into updates (source, date, programs_updated) values (?, ?, ?)", ['dixie.ALL CHANNELS',str(newdate),cleantime] )
            con.commit()
            dixie.log("Successfully inserted rows")
    cur.close()
    con.close()
#########################################################################################
# Grab the urls
def Grab_URL():
    with open(tempurl) as f:
        content = f.read().splitlines()
        return content
##########################################################################################
# Grab XML paths and offsets
def Grab_XML_Settings(xnumber):
    isurl      = 0
    addxmltodb = 1
    xmltype    = ADDON.getSetting('xmlpath%s.type' % xnumber)
    offset     = ADDON.getSetting('offset%s' % xnumber)
    countryxml = ADDON.getSetting('country%s' % xnumber)
    xmlpath    = 'None'

# Convert full country name into ISO code
    countryxml = Convert_ISO(countryxml)
    dixie.log('#### Country%s: %s' % (xnumber, countryxml))

# If the XML type is a local file    
    if xmltype == 'File':
        dixie.log("XML"+xnumber+': Local File')
        xmlpath = ADDON.getSetting('xmlpath%s.file' % xnumber)
        localcheck = hashlib.md5(open(xmlpath,'rb').read()).hexdigest()
    
# If the XML type is an online file
    elif xmltype == 'URL':
        isurl   = 1
        xmlpath = ADDON.getSetting('xmlpath%s.url' % xnumber)
        dixie.log("XML"+xnumber+': URL')
        localcheck = Check_Date(xmlpath)

# Otherwise it's not a valid entry so we skip adding to db
    else:
        dixie.log("XML"+xnumber+': None')
        addxmltodb = 0

# Try to access the db, if it's locked we wait 5s and try again
    if addxmltodb == 1 and xmlpath != 'None':
        try:
            DB_Open()
            cur.execute("SELECT COUNT(*) from xmls where id LIKE '"+xnumber+"';")
            data = cur.fetchone()[0]
            dixie.log('### Data: %s' % data)
            if data:
                cur.execute("SELECT size FROM xmls WHERE id=?", (xnumber,))
                newdata = str(cur.fetchone()[0])
                dixie.log('### Existing entry size: '+str(newdata))
            else:
                newdata = 0
            cur.close()
            con.close()
        except:
            dixie.log('### Failed to open db, running again')
            xbmc.sleep(5000)
            Grab_XML_Settings(xnumber)

        if addxmltodb == 1 and newdata != localcheck:
            Start(xmlpath, offset, isurl, xnumber)
            if data != 0:
                DB_Open()
                dixie.log('Updating XML'+xnumber+' size in db to '+localcheck)
                cur.execute("update xmls set size='"+localcheck+"' where id LIKE '"+xnumber+"';")
            else:
                DB_Open()
                dixie.log('Adding XML'+xnumber+' size to db - '+localcheck)
                cur.execute("insert into xmls (id, size) values ('"+xnumber+"','"+localcheck+"');")
            con.commit()
            cur.close()
            con.close()
##########################################################################################
# Attempt to grab the contents of the XML and fix if badly formed
def Grab_XML_Tree(xpath):
    stop = 0
    while stop == 0:
        try:
            tree = ET.parse(xpath)
            stop = 1
        except:
            dixie.log("Badly formed XML file, trying to fix...")
#            traceback.print_exc()
            traceerror = Last_Error()
            dixie.log("Error List: "+str(errorlist))
            dixie.log("Current Error: "+str(traceerror))
            dixie.log("Error -1: "+errorlist[-1])
            if traceerror == errorlist[-1]:
                dixie.log("Error matched one in array, lets stop the while loop")
                tree = ET.parse(xmlpath)
                stop = 1
            else:
                dixie.log("New error, adding to array: "+traceerror)
                errorlist.append(traceerror)
                dialog.ok('Badly Formed XML File','You have an error on line [COLOR=dodgerblue]'+str(traceerror)+'[/COLOR] of your XML file. Press OK to continue scanning, we will then try and fix any errors.')
                Fix_XML(traceerror)
    return tree
##########################################################################################
# Import the newly created csv file
def Import_CSV(mode):
    with open(csvfile,'rb') as fin:
        dr = csv.DictReader(fin) # comma is default delimiter
        to_db = [(i['channel'], i['title'],i['start_date'], i['end_date'], i['description'],i['image_large'], i['image_small'], i['source'], i['subTitle'],
                  i['season'], i['episode'], i['is_movie'], i['language']) for i in dr]

    DB_Open()
    cur.executemany("INSERT INTO programs (channel,title,start_date,end_date,description,image_large,image_small,source,subTitle,"
                    "season, episode, is_movie, language) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
    con.commit()
    cur.execute("DELETE FROM programs WHERE RowID NOT IN (SELECT MIN(RowID) FROM programs GROUP BY channel,start_date,end_date);")
    con.commit()
    cur.close()
    con.close()

# Insert relevant records into the updates table, if we don't do this we can't move forward in time in the EPG
    Get_Dates()
    if os.path.exists(csvfile):
        try:
            os.remove(csvfile)
        except:
            dixie.log("Unable to remove csv file, must be in use still")

    if os.path.exists(tempxml):
        try:
            os.remove(tempxml)
        except:
            dixie.log("Unable to remove temp xml file, must be in use still")
##########################################################################################
# Return the last error
def Last_Error():
    errorstring = traceback.format_exc()
    dixie.log("ERROR: "+errorstring)
    errorlinematch  = re.compile(': line (.+?),').findall(errorstring)
    errormatch      = errorlinematch[0] if (len(errorlinematch) > 0) else ''
    return errormatch
##########################################################################################
## Function to open a URL
def Open_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link     = response.read()
    response.close()
    return link.decode('utf-8', 'ignore')
##########################################################################################
# Work out how many days worth of guides we have available
def Return_EPG_Only():
    DB_Open()
    EPG_channel_list = ['-_ADD_OR_REMOVE_CHANNELS']
    try:
        cur.execute("SELECT DISTINCT(channel) from programs;")
        final_array = cur.fetchall()
        for row in final_array:
            try:
                EPG_channel_list.append(str(row[0]))
            except Exception as e:
                xbmc.log('Error: %s' % e)
    except Exception as e:
        xbmc.log('Error: %s' % e)
    cur.close()
    return EPG_channel_list
##########################################################################################
# Remove the channel folders so we can repopulate. All mappings will be lost unless set in the master chan.xml
def Start(xpath, offset, isurl, xnumber):
    stop    = 0
    dixie.log("### XPATH: "+xpath)
    try:
        os.remove(os.path.join(ADDON_DATA, AddonID, 'settings.cfg'))
    except:
        dixie.log("### No settings.cfg file to remove")

# Check database isn't locked and continue if possible
    if os.path.exists(dbpath):
        try:
            os.rename(dbpath,dbpath+'1')
            os.rename(dbpath+'1',dbpath)
            dixie.log("Database not in use, we can continue")
        except:
            dixie.log("### Database in use, Kodi needs a restart, if that doesn't work you'll need to restart your system.")
            dialog.ok(ADDON.getLocalizedString(30813),ADDON.getLocalizedString(30814))
            stop = 1

    if stop == 0:
        xbmc.executebuiltin("XBMC.Notification("+ADDON.getLocalizedString(30807)+","+ADDON.getLocalizedString(30811)+",10000,"+updateicon+")")
        xbmc.executebuiltin("ActivateWindow(busydialog)")

# Download the online xml file
        if isurl:
            dixie.log('File is URL, downloading to temp.xml')
            download.download(xpath, tempxml)
            if xpath.endswith('.zip'):
                extract_path = os.path.join(ADDON_DATA,AddonID,'temp%s.xml'%xnumber)
                koding.Extract(tempxml, extract_path)
                os.remove(tempxml)
                for item in os.listdir(extract_path):
                    if item.endswith('.xml'):
                        os.rename(os.path.join(extract_path,item),tempxml)
                        shutil.rmtree(extract_path)
            xpath = tempxml

# Read contents of xml
        readfile = open(xpath, 'r')
        content  = readfile.read().decode('utf-8', 'ignore')
        readfile.close()

        xmlsource = re.compile('source-info-name="(.+?)"').findall(content)
        try:
            xmlsource = xmlsource[0]
        except:
            xmlsource = 'unknown'

            dixie.log("XML TV SOURCE: "+xmlsource)
        channels   = re.compile('<channel id="[\s\S]*?<\/channel').findall(content)
        programmes = re.compile('<programme[\s\S]*?<\/programme').findall(content)

# Get total amount of channels
        channelcount =  len(channels)

# Get total amount of programmes
        listingcount =  len(programmes)
        xbmc.executebuiltin('Dialog.Close(busydialog)')

        try:
            cur.close()
            con.close()
        except:
            dixie.log("### Database not open, we can continue")
        Create_CSV(channels,channelcount,listingcount,programmes,xmlsource,offset,xnumber)
##########################################################################################
# Function to convert timestamp into proper integer that can be used for schedules
def Time_Convert(starttime,xsource,offset):
# Split the time from the string that also contains the time difference
    starttime, diff  = starttime.split(' ')

    year             = starttime[:4]
    month            = starttime[4:6]
    day              = starttime[6:8]
    hour             = starttime[8:10]
    minute           = starttime[10:12]
    secs             = starttime[12:14]

# Convert the time diff factor into an integer we can work with
    if xsource.replace("'",'') == "zap2it.com":
        diff         = int(diff[:-2])-1+int(offset) # The -1 is to bring in line with BST
    else:
        diff         = int(diff[:-2])+1+int(offset) # The +1 is to convert from UTC format
    starttime        = datetime.datetime(int(year),int(month),int(day),int(hour),int(minute),int(secs))
    starttime        = starttime + datetime.timedelta(hours=diff)
    starttime        = time.mktime(starttime.timetuple())

    return int(starttime)
##########################################################################################
# Check if item already exists in database
def updateDB(chan, s_date):
    entryexists = 0

# Changed start_date from = to LIKE (03.05.16)
    cur.execute('select channel, start_date from programs where channel LIKE "'+chan+'" and start_date LIKE "'+s_date+'";')
    try:
        row = cur.fetchone()
        if row:
            return True
    except:
        return False
##########################################################################################
# Clear the stored xml sizes so we can force an update scan
def Wipe_XML_Sizes():
    try:
        DB_Open()
        cur.execute("DELETE FROM xmls WHERE id > 0")
        cur.execute("VACUUM")
        con.commit()
        cur.close()
    except:
        pass
############### SCRIPT STARTS HERE ###############
if __name__ == "__main__":
    inprogress = os.path.join(ADDON_DATA,AddonID,'xml_scan_in_progress')
    try:
        os.makedirs(inprogress)
    except:
        pass

# Allow update to take place if set off from settings menu even if music/video is playing
    try:
        xbmc.log('###### TRTV MODE: '+sys.argv[1])
    except:
        sys.argv[1] = 'normal'
        xbmc.log('### TRTV MODE IS NORMAL')

    if sys.argv[1]=='normal' or sys.argv[1]=='rescan' or sys.argv[1]=='update':
        isplaying = xbmc.Player().isPlaying()
        while isplaying:
            xbmc.sleep(5000)
            isplaying = xbmc.Player().isPlaying()

# Force a rescan of the channel listings
    if sys.argv[1]=='rescan':
        Wipe_XML_Sizes()

    if sys.argv[1]=='full':
        dixie.log('### START CHECK ###')
        dixie.log('Checking for updated listings and clearing out old data')

    xbmc.executebuiltin("XBMC.Notification("+ADDON.getLocalizedString(30837)+","+ADDON.getLocalizedString(30838)+",5000,"+updateicon+")")
    Create_DB()
    Grab_XML_Settings('1')
    Grab_XML_Settings('2')
    Grab_XML_Settings('3')
    Grab_XML_Settings('4')
    Grab_XML_Settings('5')
    Grab_XML_Settings('6')
    Grab_XML_Settings('7')
    Grab_XML_Settings('8')
    Grab_XML_Settings('9')
    Grab_XML_Settings('10')
    if sys.argv[1]!='normal':
        Clean_DB()
        xbmc.executebuiltin("XBMC.Notification("+ADDON.getLocalizedString(30839)+","+ADDON.getLocalizedString(30840)+",5000,"+updateicon+")")
    else:
        try:
            xbmc.executebuiltin('Dialog.Close(busydialog)')
        except:
            pass

    if sys.argv[1]=='full':
        dixie.log('### END CHECK ###')
        dixie.log('Listings updates and database clean is complete.')

    try:
        shutil.rmtree(inprogress)
    except:
        pass
