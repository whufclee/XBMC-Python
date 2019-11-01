import xbmc, xbmcgui, xbmcaddon
import os, sys, shutil, re
import urllib, urllib2

# Setup the real physical HOME path of Kodi so we can save the CSV file there
HOME    = xbmc.translatePath('special://home')

# Add your XML file path here, either url or local file
xml     = os.path.join(HOME,'All_Movies.xml')

# Add the tags you want to scan for in here
tags    = 'title'

# Set the location of the CSV file we want to export to
csvfile = os.path.join(HOME,'export.csv')

##############################################################################################
# Function to open a local file and store contents in memory
def Open_File(source):

# Open the source file in read mode
    readfile = open(source, 'r')

# Store read the contents and store then to the variable 'content'
    content  = readfile.read()

# Close the readfile
    readfile.close()

# Return the value of content back to whatever called this function
    return content

##############################################################################################
# Function to open a URL and store the contents in memory
def OPEN_URL(url):

 # Assign req to the urllib2.Request function and also add the url variable in there, makes it cleaner to read in a while
    req = urllib2.Request(url)

# Add a header, some websites block python so we want to spoof ourselves as a real browser
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')

# We create a variable called 'response', when called this will open the webpage
    response = urllib2.urlopen(req)

# Create a variable called 'link', we're calling the above function which opens the page and then we're reading it into memory
    link     = response.read()

# Just like when we open local files we also need to close online files we open too. Failing to do this will result in excessive memory useage.
    response.close()

# Return the contents of the webpage back to whatever called this function
    return link

##############################################################################################
# Function to read the source file into memory then pass it through to the Grab_Data function
def Readfile(source, tags):

# If the source is a url we call the Open_URL function
    if source.startswith('http://'):
        link = Open_URL(source)

# Otherwise we presume it's a local file and call the Open_File function
    else:
        link = Open_File(source)

# Call function to grab the relevant data from our text file
    Grab_Data(link, tags)

##############################################################################################
# Loop through the file in memory and pull the relevant tags out
def Grab_Data(link, tags):

# Do some regex and grab all instances of the tag, this will put it into a list called tag_list
    tag_list  = re.compile('<%s>(.+?)<\/%s>' % (tags,tags)).findall(link)

# Create a new CSV file, we'll write our values from the tag_list into this
    writefile = open(csvfile,'w') # As we're writing we use the 'w' and if we were reading from it we'd use 'r'

# Loop through each entry in the tag_list and write it to the CSV file
    for tag in tag_list:

# Print each item in the list to the log so we can check it's grabbing the correct stuff
        xbmc.log('Adding to CSV: %s' % tag)

# write the tag followed by a comma to the CSV file
        writefile.write(tag+',')

# Close our CSV file we opened, you always need to close a file after finished reading/writing to it
    writefile.close()

##############################################################################################

# Add-on starts here:
Readfile(xml, tags)