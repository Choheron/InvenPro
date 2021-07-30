import os
from . import jsonUtils as JSONu

pcDict = {}
softDict = {}
officeDict = {}

def init(root):
    # Declare the PC Dictionary and its filepath to the Json
    global pcDict
    global pcJsonFilepath
    pcJsonFilepath = (os.getcwd() + '/driverBin/storage/CPUData.json')
    pcDict = JSONu.loadJSON(pcJsonFilepath)
    # Check if 'cpuCount' field exists, make one if there isnt one - TODO: Move and make less messy
    if(not(pcDict['admin'].has_key('cpuCount'))):
        pcDict['admin']['cpuCount'] = 0

    # Declare the Software Dictionary and its filepath to the Json
    global softDict
    global softJsonFilepath
    softJsonFilepath = (os.getcwd() + '/driverBin/storage/SoftwareData.json')
    softDict = JSONu.loadJSON(softJsonFilepath)

    # Declare the Office Dictionary and its filepath to the Json
    global officeDict
    global officeJsonFilepath
    officeJsonFilepath = (os.getcwd() + '/driverBin/storage/OfficeData.json')
    officeDict = JSONu.loadJSON(officeJsonFilepath)

    # Declare the Field Dictionary and its filepath to the Json
    global fieldDict
    global fieldJsonFilepath
    fieldJsonFilepath = (os.getcwd() + '/driverBin/storage/fieldInvData.json')
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

def setIconInvenPro(window):
    # Set Icon for Window
    window.iconbitmap(os.getcwd() + '/driverBin/images/icons/DesktopIcon 32x32.ico')