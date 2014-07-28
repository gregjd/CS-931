# Greg Jordan-Detamore
# CSCI 0931
# Final Project


import csv

# COMPILING A SYSTEM SCHEDULE

dayCodesToNames = {'WKD':'Weekday','SAT':'Saturday','SUN':'Sunday'}
dayNamesToCodes = {'Weekday':'WKD','Saturday':'SAT','Sunday':'SUN'}

file = 'stop_times.txt'

def systemSchedule(file):
    '''Given an input text file with the system schedule (stop_times.txt, as per GTFS standard), this function creates a dictionary with the system schedule.'''
    schedule = {} # will contain a system schedule
    # Structure: Route (1, 2, A, B, etc.) > Direction > Day of week (WKD, SAT, SUN) > Unique Train Identifier > Station > Time
    with open(file, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == 'trip_id': # this just applies to the first line of the file; we want to ignore this line
                pass
            else:
                if row[0][21] == '.':
                    route = row[0][20]
                else: # if row[0][21] <> '.':
                    route = row[0][20:22]
                if route not in schedule:
                    schedule[route] = {} # creates route dictionary
                    # print 'Compiling route',route,'...' (if we wanted status indicators)
                direction = row[0][23]
                if direction not in schedule[route]:
                    schedule[route][direction] = {} # creates direction dictionary
                day = dayCodesToNames[row[0][9:12]]
                if day not in schedule[route][direction]:
                    schedule[route][direction][day] = {} # creates day dictionary
                trainID = row[0]
                if trainID not in schedule[route][direction][day]:
                    schedule[route][direction][day][trainID] = {} # creates train ID dictionary
                station = row[3]
                if station not in schedule[route][direction][day][trainID]:
                    schedule[route][direction][day][trainID][station] = 0 # creates station dictionary
                time = row[2]
                schedule[route][direction][day][trainID][station] = time
    csvfile.close()
    return schedule

print 'Creating system timetable dictionary ...'
schedule = systemSchedule(file)
print 'System timetable dictionary compiled.'



# LINES OF INTEREST

# This section establishes basic information for each line: the north and south points, which routes are local and express, and the long and short names.

# Note: Lines are things like the Broadway Line and the Brighton Line. Routes are things like N, Q, and R.

allLines = {}

# 8th Avenue IND: A, C, E
allLines['Eighth'] = {}
allLines['Eighth']['shortname'] = 'Eighth'
allLines['Eighth']['name'] = '8th Avenue IND'
allLines['Eighth']['loc'] = ['C','E']
allLines['Eighth']['exp'] = ['A']
allLines['Eighth']['N'] = ['A27'] # 42 St - Port Authority Bus Terminal
allLines['Eighth']['S'] = ['A34'] # Canal St # Alternatively, A36 (Chambers St) and E01 (World Trade Center)
allLines['Eighth']['localstop'] = ['A30'] # 23 St

# 7th Avenue IRT: 1, 2, 3
allLines['Seventh'] = {}
allLines['Seventh']['shortname'] = 'Seventh'
allLines['Seventh']['name'] = '7th Avenue IRT'
allLines['Seventh']['loc'] = ['1']
allLines['Seventh']['exp'] = ['2','3']
allLines['Seventh']['N'] = ['120'] # 96 St
allLines['Seventh']['S'] = ['137'] # Chambers St
allLines['Seventh']['localstop'] = ['130'] # 23 St

# 6th Avenue IND: B, D, F, M
allLines['Sixth'] = {}
allLines['Sixth']['shortname'] = 'Sixth'
allLines['Sixth']['name'] = '6th Avenue IND'
allLines['Sixth']['loc'] = ['F','M']
allLines['Sixth']['exp'] = ['B','D']
allLines['Sixth']['N'] = ['D15'] # 47 - 50 Sts - Rockefeller Ctr
allLines['Sixth']['S'] = ['D21'] # Broadway - Lafayette St
allLines['Sixth']['localstop'] = ['D18'] # 23 St

# Broadway BMT: N, Q, R
allLines['Broadway'] = {}
allLines['Broadway']['shortname'] = 'Broadway'
allLines['Broadway']['name'] = 'Broadway BMT'
allLines['Broadway']['loc'] = ['N','R']
allLines['Broadway']['exp'] = ['Q']
allLines['Broadway']['N'] = ['R16'] # Times Sq - 42 St
allLines['Broadway']['S'] = ['R23', 'Q01'] # Canal St # Alternatively, R20 (14 St - Union Sq)
allLines['Broadway']['localstop'] = ['R19'] # 23 St

# Lexington Ave IRT: 4, 5, 6
allLines['Lexington'] = {}
allLines['Lexington']['shortname'] = 'Lexington'
allLines['Lexington']['name'] = 'Lexington Ave IRT'
allLines['Lexington']['loc'] = ['6']
allLines['Lexington']['exp'] = ['4','5']
allLines['Lexington']['N'] = ['621'] # 125 St
allLines['Lexington']['S'] = ['640'] # Brooklyn Bridge - City Hall
allLines['Lexington']['localstop'] = ['634'] # 23 St


# stopToLine: takes the stations in allLines and creates a dictionary with those stations as keys and their respective lines as values.
# stopToDirection: takes a station of origin and determines the direction of travel.
stopToLine = {}
stopToDirection = {}
for line in allLines:
    for key in allLines[line].keys():
        if key == 'N' or key == 'S':
            stops = allLines[line][key]
            for stop in stops:
                stopToLine[stop] = line
                if key == 'N':
                    stopToDirection[stop] = 'S'
                if key == 'S':
                    stopToDirection[stop] = 'N'



# COMPARISON

def runAll():
    '''Given no input, runs the times function on each line and direction, and prints the results.'''
    print 'This analysis will take approximately 20 minutes.\n'
    for line in allLines:
        print allLines[line]['name'],',','Northbound'
        if times(line,'N')=='local':
            print 'On average, it is faster to take the local train if it comes first.\n'
        if times(line,'N')=='express':
            print 'On average, it is faster to wait for the express train.\n'
        print allLines[line]['name'],',','Southbound'
        if times(line,'S')=='local':
            print 'On average, it is faster to take the local train if it comes first.\n'
        if times(line,'S')=='express':
            print 'On average, it is faster to wait for the express train.\n'
    return

def runTest():
    '''Given no input, runs the times function on two sample lines, and prints the results.'''
    print allLines['Seventh']['name'],',','Northbound'
    if times('Seventh','N')=='local':
        print 'On average, it is faster to take the local train if it comes first.\n'
    if times('Seventh','N')=='express':
        print 'On average, it is faster to wait for the express train.\n'
    print allLines['Eighth']['name'],',','Southbound'
    if times('Eighth','S')=='local':
        print 'On average, it is faster to take the local train if it comes first.\n'
    if times('Eighth','S')=='express':
        print 'On average, it is faster to wait for the express train.\n'
    return

def times(line,direction,daysToTest=['Weekday','Saturday','Sunday'],startTime='07:00:00',endTime='22:00:00'): # default days and times
    '''Given a line name (string) and direction (string, 'N' or 'S'), this function will iterate through the entire day
at 6-second intervals and run the versus function (below) on each time. It will keep a tally of the results of the versus function,
and give an output that is a string: 'local' if taking the local is faster the majority of the time, or 'express' if it is not.'''
    # It if wouldn't make the program too much slower, I might actually like to try 1-second intervals.
    localFirst = 0 # the number of times the local train comes first
    localWin = 0 # the number of times taking the local train gets you there faster
    if type(startTime) is int:
        pass
    elif type(startTime) is str:
        startTime = convertToSeconds(startTime)
    else:
        print 'ERROR: Start time is in incorrect format. Must be integer (seconds) or string (HH:MM:SS).'
        return
    if type(endTime) is int:
        pass
    elif type(endTime) is str:
        endTime = convertToSeconds(endTime)
    else:
        print 'ERROR: End time is in incorrect format. Must be integer (seconds) or string (HH:MM:SS).'
        return
    north_names = ['N','n','North','north','Northbound','northbound','Uptown','uptown']
    south_names = ['S','s','South','south','Southbound','southbound','Downtown','downtown']
    if direction in north_names:
        origin = allLines[line]['S']
        destination = allLines[line]['N']
    elif direction in south_names:
        origin = allLines[line]['N']
        destination = allLines[line]['S']
    else:
        print "ERROR: Invalid direction. Please use 'N' or 'S'."
        return
    if type(daysToTest) is not list:
        print 'ERROR: The variable daysToTest must be a list.'
        return
    for day in daysToTest:
        if day=='Weekday' or day=='Saturday' or day=='Sunday':
            pass
        elif day=='WKD' or day=='SAT' or day=='SUN':
            day = dayCodesToNames[day]
        else:
            print 'ERROR: Incorrect day format.'
            return
        for time in range(startTime,endTime,10):
            if time>97200:
                print 'ERROR: Time is too large.'
                return
            result = versus(time,day,origin,destination)
            localFirst = localFirst + result[0]
            if result[0] == 1:
                localWin = localWin + result[1]
    if localWin > float(0.5*localFirst): # taking the local first wins the majority of the time
        return 'local'
    else:
        return 'express'

def versus(time,day,origin,destination):
    '''Given a time (integer), day (integer), origin (list), and destination (list), determines whether it is faster to take that local train or the next express train.
The output will be a set of integers, depending on the result of this test.
Compares the lenth of time the local train takes to get to its destination vs. the time difference to wait for the express train
plus the length of time the express train takes to get to its destination.'''
    originLocTime,originLocHMS,originLocID = nextTrain(time,day,origin,destination,'loc')
    if nextTrain(time,day,origin,destination,'exp') == 'EXPRESS_ERROR':
        print 'ERROR: At the given time, there is no next express train at the specified station of origin.'
        return
    else:
        originExpTime,originExpHMS,originExpID = nextTrain(time,day,origin,destination,'exp')
    if originExpTime > originLocTime: # the local train comes first; these are the cases we care about
        timeLoc = travelTime(originLocID,origin,destination)
        timeExp = travelTime(originExpID,origin,destination) + waitExp(originLocTime,originExpTime)
        if timeLoc < timeExp: # taking the local wins
            return [1,1]
        else: # tie, or taking the express wins
            return [1,0]
    else: # either the times are the same or the express train comes first; we don't care about these cases
        return [0]

def travelTime(trainID,origin,destination): # can extract route, direction, and day from train ID
    '''Given the train ID of the train in question (string) and the stations of origin and destination (lists),
finds the time that train arrives at the destination station (string), and subtracts the origin station time from that to produce a travel time (integer).'''
    if trainID[21] == '.':
        route = trainID[20]
    else: # if trainID[21] <> '.':
        route = trainID[20:22]
    direction = trainID[23]
    day = dayCodesToNames[trainID[9:12]]
    trainID_dict = schedule[route][direction][day][trainID]
    if origin[0]+direction in trainID_dict.keys():
        originTime = convertToSeconds(trainID_dict[origin[0]+direction])
    else:
        originTime = convertToSeconds(trainID_dict[origin[1]+direction])
    if destination[0]+direction in trainID_dict.keys():
        endTime = convertToSeconds(trainID_dict[destination[0]+direction])
    else:
        endTime = convertToSeconds(trainID_dict[destination[1]+direction])
    timeToDestination = endTime - originTime
    return timeToDestination

def nextTrain(time,day,origin,destination,type='all'):
    '''Given a time (int), day (string), origin (string), destination (string), and type (string; optional, with default of 'all'),
this function finds the time of the next train (local, express, or the default of any) that will arrive. Output is a time (int) and a train ID (string).'''
    if type=='local' or type=='loc':
        pass
    elif type=='express' or type=='exp':
        pass
    elif type=='all' or type=='both' or type=='either':
        pass
    else:
        print 'ERROR: Incorrect train type given.'
        return
    direction = stopToDirection[origin[0]] # determines direction from the origin stop
    time_HMS = convertToHMS(time) # converts time from seconds to HMS so it will match the values found in the schedule dictionary
    nextTrain = 150000 # an arbitratily high number; any train will have a time that is less than this
    nextTrainID = ''
    lineToTest = stopToLine[origin[0]]
    localTest = allLines[lineToTest]['localstop'][0]+direction
    routesToTestDictionary = {}
    for key in allLines[lineToTest].keys():
        if key == 'loc' or key == 'exp':
            routes = allLines[lineToTest][key]
            for route in routes:
                routesToTestDictionary[route] = ''
    routesToTest = routesToTestDictionary.keys() # creates a list of the routes whose schedules should be searched through
    for route in routesToTest:
        if day in schedule[route][direction].keys():
            for train in schedule[route][direction][day]:
                trainStops = schedule[route][direction][day][train].keys()
                origin_dir = [station+direction for station in origin]
                destination_dir = [station+direction for station in destination]
                if len(origin_dir)==1 and origin_dir[0] not in trainStops:
                    pass
                elif len(origin_dir)==2 and origin_dir[0] not in trainStops and origin_dir[1] not in trainStops:
                    pass
                elif len(destination_dir)==1 and destination_dir[0] not in trainStops:
                    pass
                elif len(destination_dir)==2 and destination_dir[0] not in trainStops and destination_dir[1] not in trainStops:
                    pass
                else:
                    if type=='local' or type=='loc':
                        if localTest in trainStops:
                            nextTrain, nextTrainID = nextTrainTest(time,origin_dir,route,direction,day,train,nextTrain,nextTrainID)
                    elif type=='express' or type=='exp':
                        if localTest not in trainStops:
                            nextTrain, nextTrainID = nextTrainTest(time,origin_dir,route,direction,day,train,nextTrain,nextTrainID)
                    elif type=='all' or type=='both':
                        nextTrain, nextTrainID = nextTrainTest(time,origin_dir,route,direction,day,train,nextTrain,nextTrainID)
    if nextTrain == 150000:
        return 'EXPRESS_ERROR'
    return nextTrain, convertToHMS(nextTrain), nextTrainID

def nextTrainTest(time,origin_dir,route,direction,day,train,nextTrain,nextTrainID):
    '''Given the time (integer), station(s) of origin (list of strings), route (string), direction (string), day (string), train ID (string),
the time of next known train (integer), and the train ID of the next known train (string), outputs the time (integer) and train ID (string) of the next train.
If the train being tested is after the next known train, no variables change values.'''
    for station in origin_dir:
        if station in schedule[route][direction][day][train].keys():
            trainTime = convertToSeconds(schedule[route][direction][day][train][station])
            if trainTime < nextTrain and trainTime >= time:
                nextTrain = trainTime
                nextTrainID = train
    return nextTrain, nextTrainID

def waitExp(originLocTime,originExpTime):
    '''Given times (integer) that the next local and express trains are supposed to arrive, this function subtracts the local train time
from the express train time to get the time (integer) that you need to wait after the local train comes until the express train comes.'''
    waitTime = originExpTime - originLocTime
    return waitTime # in seconds

def convertToSeconds(HMS):
    '''Given a time written in a string format of 'HH:MM:SS', returns a time (integer) in seconds.'''
    splitTime = HMS.split(':')
    h, m, s = splitTime[0], splitTime[1], splitTime[2]
    seconds = (int(h)*3600) + (int(m)*60) + (int(s))
    return seconds

def convertToHMS(seconds):
    '''Given a time written in a integer format of seconds, returns a time in string format of 'HH:MM:SS'.'''
    h = str(seconds/3600)
    if len(h) == 1:
        h = '0'+h
    secondsNoHours = seconds % 3600
    m = str(secondsNoHours/60)
    if len(m) == 1:
        m = '0'+m
    s = str(secondsNoHours % 60)
    if len(s) == 1:
        s = '0'+s
    HMS_list = [h,m,s]
    HMS = ':'.join(HMS_list)
    return HMS



# RUN COMPARISON ON OUR LINES OF INTEREST

# Runs a sample of two of the lines
print 'Running a sample of two lines:\n'
testLines = runTest()

# Tells the user the lines available to test, as well as their short names (which are used in the functions).
print '\n\nLines to test:'
print '\nShort name:\tDescription:\t\tLocal:\t\tExpress:'
for line in allLines:
    print '%-10s\t%-20s\t%-10s\t%s' % (allLines[line]['shortname'],allLines[line]['name'],allLines[line]['loc'],allLines[line]['exp'])

print "\nNow it's your turn. Try testing one or more of these lines!"
print 'If you want to try all lines, then enter: runAll()'
print 'Note that this takes approximately 20 minutes.'
print 'If you want to try a specific line, you can choose from the lines listed above. You must select a direction.'
print 'Enter in this format: times(line,direction,days,startTime,endTime)'
print "Example: times('Lexington','S',['Weekday','Saturday'],'06:00:00','08:00:00')"
print 'Line = the short name given in the table above'
print "Direction = 'N' or 'S'"
print 'Days = Choose one or more of Weekday, Saturday, Sunday (Optional; Default is all three)'
print "startTime = starting time (Optional; Default is '07:00:00')"
print "endTime = ending time (Optional; Default is '22:00:00')"



### END ###

