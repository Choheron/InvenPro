import os
from . import jsonUtils as JSONu

pcDict = {}
softDict = {}
officeDict = {}

def init(root):
    # Declare the PC Dictionary and its filepath to the Json
    global pcDict
    global pcJsonFilepath
    pcJsonFilepath = (os.getcwd() + '/driverBin/data/CPUData.json')
    pcDict = JSONu.loadJSON(pcJsonFilepath)

    # Declare the Software Dictionary and its filepath to the Json
    global softDict
    global softJsonFilepath
    softJsonFilepath = (os.getcwd() + '/driverBin/data/SoftwareData.json')
    softDict = JSONu.loadJSON(softJsonFilepath)

    # Declare the Office Dictionary and its filepath to the Json
    global officeDict
    global officeJsonFilepath
    officeJsonFilepath = (os.getcwd() + '/driverBin/data/OfficeData.json')
    officeDict = JSONu.loadJSON(officeJsonFilepath)

    # Declare the Field Dictionary and its filepath to the Json
    global fieldDict
    global fieldJsonFilepath
    fieldJsonFilepath = (os.getcwd() + '/driverBin/data/fieldInvData.json')
    fieldDict = JSONu.loadJSON(fieldJsonFilepath)

def savePCdict():
    global pcDict
    JSONu.dumpJSON(pcDict, pcJsonFilepath)
    pcDict = JSONu.loadJSON(pcJsonFilepath)

def loadPCdict():
    global pcDict
    pcDict = JSONu.loadJSON(pcJsonFilepath)

def saveSoftdict():
    global softDict
    JSONu.dumpJSON(softDict, softJsonFilepath)
    softDict = JSONu.loadJSON(softJsonFilepath)

def loadSoftdict():
    global softDict
    softDict = JSONu.loadJSON(softJsonFilepath)

def saveOfficedict():
    global officeDict
    JSONu.dumpJSON(officeDict, officeJsonFilepath)
    officeDict = JSONu.loadJSON(officeJsonFilepath)

def loadOfficedict():
    global officeDict
    officeDict = JSONu.loadJSON(officeJsonFilepath)

def saveFielddict():
    global fieldDict
    JSONu.dumpJSON(fieldDict, fieldJsonFilepath)
    fieldDict = JSONu.loadJSON(fieldJsonFilepath)

def loadFielddict():
    global fieldDict
    fieldDict = JSONu.loadJSON(fieldJsonFilepath)

def saveAdmindict():
    global adminDict
    JSONu.dumpJSON(adminDict, adminJsonFilepath)
    adminDict = JSONu.loadJSON(adminJsonFilepath)

def loadAdmindict():
    global adminDict
    adminDict = JSONu.loadJSON(adminJsonFilepath)

def setIconInvenPro(window):
    # Set Icon for Window
    window.iconbitmap(os.getcwd() + '/driverBin/images/icons/DesktopIcon 32x32.ico')