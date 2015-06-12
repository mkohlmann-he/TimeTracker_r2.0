#6/10/2015
#Michael Kohlmann
#devCodeCamp - Personal Project


# This is the GUI handler for my time tracker widget, using wxPython.
# This is Rev 2.0. and a work in progress.

# Rev 1.0 adds a GUI and logs directly to a text file.
# Rev 2.0 adds a database connection for a MySQL server that is on the localhost.

# Non-Standard Library dependencies:
# GUI = wxPython
# DB  = MySQLdb


#Note, this is overly commented, because GUI's are a new topic to me. I want to be able to come back to it later and understand it.


#use the Try-Except for the import, because wxPython is not a default Library, if the user doesn't have it installed, it will throw an error.
try:
    import wx
except ImportError:
    raise ImportError,"The wxPython module is required to run this program"

try:
    from DataEntryClass import *
except ImportError:
    raise ImportError,"The DataEntryClass.py module is required to run this program"
    
#Start of GUIHandle Class. 
#wxPython has it's own class, that our GUI will inherit. 
#Then we add our own functions for building the exact window we want, and how we want to react to buttons.
class GUIHandle(wx.Frame):
    def __init__(self,parent,id,title): # GUI Class Constructor
        #GUI Control
        wx.Frame.__init__(self,parent,id,title) # wxPython Sub Constructor, inherits the wx Frame
        self.SetIcon(wx.Icon('stopwatch.ico'))
        self.parent = parent # remember to keep track of yours parents
        self.initialize() # Create the window and add buttons and objects
        #DataEntryControl
        self.dataEntry = DataEntry()

    def initialize(self):
        self.timeTrackerStatus = "STOP"
        sizer = wx.GridBagSizer() # Put button objects on Grid Spacing (GridBagSizer is the grid layout manager)
        
        # Create Object, then Add the object to the layout manager (sizer in this case), then bind it to event handler
        # Add TextBox for Task Comments
        self.entry = wx.TextCtrl(self, -1, value=u"Enter your task comments here.") # Creates the text box
        sizer.Add(self.entry, (0,0), (1,4), wx.EXPAND) # Adds the text box to the sizer manager
        
        # Add a Combo box for testing.
        self.projectCombo = wx.ComboBox(self, -1, choices=self.getProjectChoices(), style=wx.CB_READONLY)
        self.projectCombo.SetSelection(0)
        sizer.Add(self.projectCombo, (1,0), (1,1), wx.EXPAND)
        
        # Add START Button
        self.startButton = wx.Button(self, -1, label="START")
        self.startButton.SetForegroundColour(wx.BLACK)
        self.startButton.SetBackgroundColour(wx.GREEN)
        sizer.Add(self.startButton, (1,1))
        self.Bind(wx.EVT_BUTTON, self.onStartButtonClick, self.startButton) # Binds the event handler to the StartButton
        
        # Add PAUSE Button
        self.pauseButton = wx.Button(self, -1, label="PAUSE")
        self.pauseButton.SetBackgroundColour(wx.WHITE)
        self.pauseButton.SetForegroundColour(wx.RED)
        sizer.Add(self.pauseButton, (1,2))
        self.Bind(wx.EVT_BUTTON, self.onPauseButtonClick, self.pauseButton) # Binds the event handler to the StartButton
        
        # Add STOP Button
        self.stopButton = wx.Button(self, -1, label="STOP")
        self.stopButton.SetBackgroundColour(wx.WHITE)
        self.stopButton.SetForegroundColour(wx.RED)
        sizer.Add(self.stopButton, (1,3))
        self.Bind(wx.EVT_BUTTON, self.onStopButtonClick, self.stopButton) # Binds the event handler to the StartButton
        

        # Set which colums/rows you want expandable
        sizer.AddGrowableCol(0) # This command lets the sizer expand the columns and rows as the main window grows. Specifically Column 0, each one must be called out individually as a separate command.
        #sizer.AddGrowableCol(2) # This command lets the sizer expand the columns and rows as the main window grows. Specifically Column 3
        
        
        #Runs the sizer to build the control elements
        self.SetSizerAndFit(sizer) # This tells our GUI to use the sizer designated above when layout out the buttons.

        
        # Set which directions you want the window to be able to expand.
        self.SetSizeHints(-1,self.GetSize().y, -1, self.GetSize().y)
        #This command sets the minimum and maximum of the width and height. 
        #Width -1 means unconstrained. Height is set to the current height value. 
        #This has to be run after the sizer I think, because it needs to know the current height in order to set it.
        
        self.entry.SetFocus()
        self.entry.SetSelection(-1,-1)
        
        self.Show(True) # after the window is constructed, Show it.

    def onStartButtonClick(self, event):
        print("DEBUG: Start Button Pressed")
        if self.timeTrackerStatus == "STOP":
            #GUI Control
            self.timeTrackerStatus = "RUNNING"
            self.setButtonColors(self.timeTrackerStatus)
            #EntryControl       
            self.dataEntry.setTaskComment(self.entry.GetValue() )
            self.dataEntry.setProjectNumber(self.projectCombo.GetValue() )
            self.dataEntry.startTimer()
        else:
            print("^DEBUG: Start Button Pressed, while status is not 'STOP'")
        return
    
    def onPauseButtonClick(self, event):
        print("DEBUG: Pause Button Pressed")
        if self.timeTrackerStatus == "RUNNING":
            print("^DEBUG: ENTERING PAUSE MODE")
            #GUI Control
            self.timeTrackerStatus = "PAUSE"
            self.setButtonColors(self.timeTrackerStatus)
            #Data Entry Control
            self.dataEntry.pauseTimer()
        elif self.timeTrackerStatus == "PAUSE":
            print("^DEBUG: LEAVING PAUSE MODE")
            #GUI Control
            self.timeTrackerStatus = "RUNNING"
            self.setButtonColors(self.timeTrackerStatus)
            #Data Entry Control
            self.dataEntry.unpauseTimer()           
        else:
            print("^DEBUG: Start Button Pressed, while status is 'STOP'")        
        return
        
    def onStopButtonClick(self, event):
        print("DEBUG:Stop Button Pressed")
        if self.timeTrackerStatus == "RUNNING":
            #GUI Control
            self.timeTrackerStatus = "STOP"
            self.setButtonColors(self.timeTrackerStatus)
            #Data Entry Control       
            self.dataEntry.stopTimer() 
            self.dataEntry.exportToLogFile()
            self.dataEntry.exportToDatabase()
            self.dataEntry.debugPrintEntry()
            self.dataEntry.resetAll()
        else:
            print("^DEBUG: Sop Button Pressed, while status is 'Running'")        
        return
            
    def setButtonColors(self, status):
        if status == "RUNNING":
            self.startButton.SetForegroundColour("LIGHT GREY")
            self.startButton.SetBackgroundColour(wx.WHITE)
            self.pauseButton.SetForegroundColour(wx.BLACK)
            self.pauseButton.SetBackgroundColour(wx.YELLOW)
            self.stopButton.SetForegroundColour(wx.WHITE)
            self.stopButton.SetBackgroundColour(wx.RED)
            self.entry.SetEditable(False)
            self.entry.SetBackgroundColour("LIGHT GREY")
            self.projectCombo.Enable(False)
        elif status == "PAUSE":
            self.startButton.SetForegroundColour("LIGHT GREY")
            self.startButton.SetBackgroundColour(wx.WHITE)
            self.pauseButton.SetForegroundColour(wx.BLACK)
            self.pauseButton.SetBackgroundColour(wx.YELLOW)
            self.stopButton.SetForegroundColour("LIGHT GREY")
            self.stopButton.SetBackgroundColour(wx.WHITE)
        elif status == "STOP":
            self.startButton.SetForegroundColour(wx.BLACK)
            self.startButton.SetBackgroundColour(wx.GREEN)
            self.pauseButton.SetForegroundColour(wx.RED)
            self.pauseButton.SetBackgroundColour(wx.WHITE)
            self.stopButton.SetForegroundColour(wx.RED)
            self.stopButton.SetBackgroundColour(wx.WHITE)
            self.entry.SetEditable(True)
            self.entry.SetBackgroundColour(wx.WHITE)
            self.projectCombo.Enable(True)
            
            
    def getProjectChoices(self):
        projectFile_name = "project_list.txt"
        try:
            projectFile = open(projectFile_name, "r")
        except:
            raise ImportError,"The file 'project_list.txt' must be in the same directory as the main program"
                    
        projectList = [line.strip("\n") for line in projectFile.readlines()]
        return projectList


# Helper function to start the GUI (Used if starting from an external file)          
def startGUI():
    app = wx.App() #First need to construct the from the wxPython Library
    frame = GUIHandle(None,-1,"Time Tracker") #After that, we construct the actual frame.
    app.MainLoop() #The wxPython MainLoop is what scans and looks for event calls.
    
    
##### Start Main Process Here
if __name__ == "__main__":
    #Create the Data Entry Object to pass into the GUI
    startGUI()

