# Greg Jordan-Detamore
# CSCI 0931
# Project 2


import re

def cleanXML(file):
    '''Given an XML file with a year's worth of Brown Daily Herald articles,
this function will remove the extraneous code at the beginning and end of the file.
The inputs are the XML file name and the desired name of the output file, both in string formats.
The output is a stringe with the extraneous code removed.'''
    fileName = file
    myFile = open(fileName,'r')
    myString = myFile.read()
    myFile.close()
    myString = myString.lower()
    text = re.compile(r'<\?xml ver.+generator>\n\n',re.S) # extra code at beginning of file
    myString = text.sub('',myString)
    text = re.compile(r'\n</channel>\n</rss>',re.S) # extra code at end of file
    myString = text.sub('',myString)
    return myString


# Claim: Senior Staff Writers have written a greater percentage of the articles in 2012 than in 2010.

def countAuthorType(string):
    '''Given a string with a year's worth of artilces (the string will be the one we produced using cleanXML),
this function will calculate the number of authors of each type.
The outputs are all integers: numbers of authors of each type, plus the percent of articles written by senior staff writers.'''
    Articles = 0
    SSW = 0
    SW = 0
    CW = 0
    Editor = 0
    Opinions = 0
    matches = re.finditer(r'bdh_reporter_type',string)
    for match in matches:
        Articles = Articles + 1
    matchesSSW = re.finditer(r'cdata\[senior staff writer\]',string)
    for match in matchesSSW:
        SSW = SSW + 1
    matchesSW = re.finditer(r'cdata\[staff writer\]',string)
    for match in matchesSW:
        SW = SW + 1
    matchesCW = re.finditer(r'cdata\[contributing writer\]',string)
    for match in matchesCW:
        CW = CW + 1
    matchesE = re.finditer(r'cdata\[news editor\]|cdata\[science editor\]|cdata\[features editor\]|cdata\[sports editor\]|cdata\[assistant sports editor\]|cdata\[arts & culture editor\]|cdata\[city & state editor\]',string)
    for match in matchesE:
        Editor = Editor + 1
    matchesO = re.finditer(r'cdata\[opinions columnist\]|cdata\[opinions editor\]|cdata\[guest columnist\]',string)
    for match in matchesO:
        Opinions = Opinions + 1
    Articles = Articles - Opinions # eliminates opinions columns from our total article count
    print Articles, 'total articles'
    print SSW, 'articles written by Senior Staff Writers'
    print SW, 'articles written by Staff Writers'
    print CW, 'articles written by Contributing Writers'
    print Editor, 'articles written by section editors'
    print int((float(SSW)/float(Articles))*100), ' percent of articles written by Senior Staff Writers'
    return


# Run the program

string2010 = cleanXML('browndailyherald.wordpress.2010.xml')
string2012 = cleanXML('browndailyherald.wordpress.2012.xml')

print '2010'
countAuthorType(string2010)
print'\n2012'
countAuthorType(string2012)
