#6/10/2015
#Michael Kohlmann
#devCodeCamp - Personal Project

# This is the data base connection class for my time tracker widget.
# This is Rev 2.0. and a work in progress.

# Rev 1.0 adds a GUI and logs directly to a text file.
# Rev 2.0 adds a database connection for a MySQL server that is on the localhost.

# Non-Standard Library dependencies:
# GUI = wxPython
# DB  = MySQLdb

import MySQLdb
import os

##################
# Data Structure #
##################
"""
Service Name = MySQL56 #reference only, not actually used
Database Name = "PROJECT_MANAGEMENT"
Table Name = "TIME_TRACKER"
username = "testuser"
password = "test123"
table = "time_log"
Fields:
    - FIRST_NAME  CHAR(20) NOT NULL,
    - LAST_NAME  CHAR(20),
    - AGE INT,  
    - SEX CHAR(1),
    - INCOME FLOAT

"""

class MySQLCon:
    def __init__(self):
        # Open database connection
        # Hardcoded connection for testing. Later use a config file to testing.
        self.hostPath = "localhost"
        self.username = "testuser"
        self.password = "test123"
        self.database = "PROJECT_MANAGEMENT"
        #self.table = "TIME_TRACKER"
        
        
        
        self.db = MySQLdb.connect(self.hostPath, self.username, self.password, self.database)
        self.debug(self.db)
        
        # Prepare a cursor object using cursor() method
        self.cursor = self.db.cursor()
        

        
    #########################
    # Methods for Daily Use #
    #########################
    def insertTimeTrackerRecord(self, name, project, time, comment):
        # Prepare SQL query to INSERT a record into the database.
        self.sql = "INSERT INTO TIME_TRACKER (NAME, PROJECT, TIME, COMMENT) \
                    VALUES ('{0}', '{1}', '{2}', '{3}')".format(name, project, time, comment)
        self.debug("InsertRecord: sql created")
        self.debug(self.sql)
        
        try:
           # Execute the SQL command
            self.cursor.execute(self.sql)
            self.debug("InsertRecord: Cursor.Execute passed")
            # Commit your changes in the database
            self.db.commit()
            self.debug("InsertRecord: db.commit passed")
            self.db.close()
            return True
        except:
            # Rollback in case there is any error
            self.debug("InsertRecord: Failed in Try Catch for some reason")
            self.db.rollback()
            self.db.close()
            return False

           
    ##################
    # Helper Methods #    
    ##################
    def readAllRecords(self, tableName):
        # Prepare SQL query to INSERT a record into the database.
        self.sql = "SELECT * FROM {0}".format(tableName)
        self.debug("ReadRecord: sql created")
        self.debug(self.sql)
        try:
            # Execute the SQL command
            self.cursor.execute(self.sql)
            self.debug("ReadRecord: Cursor.Execute passed")
            # Fetch all the rows in a list of lists.
            results = self.cursor.fetchall()
            self.debug("ReadRecord: Cursor.Fetchall passed")
            #self.debug(results)
            self.db.close()
            return results
        except:
            print "Error: unable to fecth data"
            self.db.close()
            return False
            
            
    def deleteRecord(self):
        # Prepare SQL query to DELETE required records
        self.sql = "DELETE FROM TIME_TRACKER WHERE TIME > '%d'" % (60)
        self.debug("DeleteRecord: sql passed")
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            self.debug("DeleteRecord: cursor.execute(sql) passed")
            # Commit your changes in the database
            self.db.commit()
            self.debug("DeleteRecord: db.commit passed")
            self.db.close()
            return True
        except:
            # Rollback in case there is any error
            self.debug("DeleteRecord: Failed in Try Catch for some reason")
            self.db.rollback()
            self.db.close()
            return False
       
    def debug(self, message):
        DEBUG = True
        if DEBUG:
            print(message)
        return
        
        
    #############################
    # Database Creation Methods #
    #############################
    def CreateTable(self):
        
        #### WARNING: Only run this once. Running it will wipe out the previous table, and start from scratch.
        # Drop table if it already exist using execute() method.
        self.cursor.execute("DROP TABLE IF EXISTS TIME_TRACKER")
        self.debug("CreateTable: Cursor.Execute(Drop) passed")

        # Create table as per requirement
        self.sql = """CREATE TABLE TIME_TRACKER(
                      NAME  CHAR(30) NOT NULL,
                      PROJECT CHAR(30),
                      TIME INT,
                      COMMENT CHAR(200))
                      """
                      ### NEED TO FIGURE OUT HOW TO PUT A TIME STAMP
        self.debug("CreateTable: sql passed")
                      
        self.cursor.execute(self.sql)
        self.debug("CreateTable: Cursor.Execute(sql) passed")
        self.db.close()
        return True
    
    
if __name__ == "__main__":
    os.system("cls")
    # print(MySQLCon().CreateTable())
    # print(MySQLCon().insertRecord("Suzie", "TimeTracker R2", 100, "Working on DB"))
    # print(MySQLCon().insertRecord("Jane", "Joes Project", 23, "Working on Timer"))
    # print(MySQLCon().insertRecord("Josie", "Joes Project", 1000, "Working on timer"))
    # print(MySQLCon().insertRecord("Jill", "Joes Project", 200, "Working on Shit"))
    
    #Print all records
    records = (MySQLCon().readAllRecords(TIME_TRACKER))
    if records is not False:
        for each in records:
            print(str(each))

    # ans = MySQLCon().deleteRecord()
    # ans = MySQLCon().readAllRecords()