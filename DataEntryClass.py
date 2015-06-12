#6/10/2015
#Michael Kohlmann
#devCodeCamp - Personal Project

# This is the data entry class for my time tracker widget.
# This is Rev 2.0. and a work in progress.

# Rev 1.0 adds a GUI and logs directly to a text file.
# Rev 2.0 adds a database connection for a MySQL server that is on the localhost.

# Non-Standard Library dependencies:
# GUI = wxPython
# DB  = MySQLdb


from datetime import *
#from time import *
from TimeTracker_DB_CON import *
import os


class DataEntry:
    def __init__(self):
        self.projectNumber = ""
        self.taskComment = ""
        self.startTime = time
        self.stopTime = time
        self.cumulativeTime = timedelta(0)

########    
# SETS #    
########
    def setProjectNumber(self,value):
        self.projectNumber = str(value)
        return
        
    def setTaskComment(self,value):
        self.taskComment = str(value)
        return

    def setStartTime(self,value):
        self.startTime = value
        return

    def setStopTime(self,value):
        self.stopTime = value
        return

########
# GETS #
########        
    def getProjectNumber(self):
        return self.projectNumber
        
    def getTaskComment(self):
        return self.taskComment

    def getStartTime(self):
        return self.startTime

    def getStopTime(self):
        return str(self.stopTime)

    def getCumulativeTime(self):
        return str(self.cumulativeTime)

###################        
# DEBUG FUNCTIONS #
###################
    def debugPrintEntry(self):
        print(">DEBUG: Log Entry Contains")
        print(">-------------------------")
        print(">Project number  = " + str(self.projectNumber))
        print(">Task Comment    = " + str(self.taskComment))
        print(">Start Time      = " + str(self.startTime))
        print(">Stop Time       = " + str(self.stopTime))
        print(">Cumulative Time = " + str(self.cumulativeTime))
        
        
####################
# HELPER FUNCTIONS #
####################
    def calculateCumulativeTime(self):
        self.cumulativeTime = (self.stopTime - self.startTime) + self.cumulativeTime
        return

    def exportToLogFile(self, fileName="time_log.txt"):
        timeStamp = datetime.now()
        logFile = open(fileName, "a+")
        entry = (str(timeStamp) + "\t" + 
                 self.projectNumber + "\t" + 
                 str(int(round(self.cumulativeTime.total_seconds())))+ "\t" + 
                 self.taskComment + "\n")
        logFile.writelines(entry)
        logFile.close()
        return True
        
            
    def exportToDatabase(self):
        results = MySQLCon().insertTimeTrackerRecord("Employee Name Holder", 
                                          self.projectNumber, 
                                          int(round(self.cumulativeTime.total_seconds())), 
                                          self.taskComment)
        records = (MySQLCon().readAllRecords("TIME_TRACKER"))
        print("\nDEBUG: Entries from DataBase\n----------------------------")
        if records is not False:
            for each in records:
                print(str(each))
        return results
    
    
    def resetAll(self):
        self.projectNumber = ""
        self.taskComment = ""
        self.startTime = time
        self.stopTime = time
        self.cumulativeTime = timedelta(0)
        return
    
    def startTimer(self):
        self.startTime = datetime.now()
        return
        
    def stopTimer(self):
        self.stopTime = datetime.now()
        self.calculateCumulativeTime()
        return
        
    def pauseTimer(self):
        self.stopTimer()
        return
    
    def unpauseTimer(self):
        self.startTimer()
        return

        

    