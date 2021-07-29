from datetime import datetime
import json, os.path
from os import path
from datetime import datetime

def loadJSON(filepath):
    # Create file if it does not exist, saves the date of file creation
    if(not(os.path.exists(filepath))):
        tempDict = {}
        tempDict['admin'] = {}
        tempDict['admin']['created'] = (str)(datetime.now())[:-7]
        tempDict['admin']['updated'] = (str)(datetime.now())[:-7]
        temp = open(filepath, "w")
        temp.write(json.dumps(tempDict, indent = 4))
        temp.close()
    # Open file and read json into return value
    JsonFile = open(filepath, "r")
    jsonOut = json.load(JsonFile)
    JsonFile.close()
    return jsonOut

def dumpJSON(jsonIn, filepath):
    if(jsonIn['admin'] == None):
        jsonIn['admin'] = {}
    jsonIn['admin']['updated'] = (str)(datetime.now())[:-7]
    outObj = json.dumps(jsonIn, indent = 4)
    outputFile = open(filepath, "w")
    outputFile.write(outObj)
    outputFile.close()
    return True