from os import listdir, rename, makedirs, rmdir
from os.path import getmtime, isfile, join, exists, isdir
from time import gmtime
from shutil import move
from sys import argv
from config import ORIGIN_PATH, DESTINATION_PATH, TEMP_PATH

# 0	tm_year	(for example, 1993)
# 1	tm_mon	range [1, 12]
# 2	tm_mday	range [1, 31]
# 3	tm_hour	range [0, 23]
# 4	tm_min	range [0, 59]

def RenameAndMoveToDestinantionFolder():
    for folder in listdir(TEMP_PATH):
        if isdir(join(TEMP_PATH, folder)):

            if CreateFolder(join(DESTINATION_PATH, folder)):
                fileId = 1
            else:
                fileId = getFileIdFromFolder(join(DESTINATION_PATH, folder))

            for f in listdir(join(TEMP_PATH, folder)):
                if isfile(join(join(TEMP_PATH, folder), f)):
                    newFileName = GetNewFileName(f, folder, fileId)
                    rename(join(join(TEMP_PATH, folder), f), join(join(DESTINATION_PATH, folder), newFileName))
                else:
                    print('WARNING 03: Found folder ' + join(join(TEMP_PATH, folder), f) + ' and wasn\'t expected , please check it.')
                    quit()
        else:
            print('WARNING 02: Found f ' + join(TEMP_PATH, folder) + ' and wasn\'t expected , please check it.')

def GetStringFileId(fileId):
    if fileId < 10:
        return '000' + str(fileId)
    elif fileId < 100:
        return '00' + str(fileId)
    elif fileId < 1000:
        return '0' + str(fileId)
    else:
        return str(fileId)
            
def GetNewFileName(originalName, dateString, fileId):
    stringFileId = GetStringFileId(fileId)
    return dateString + '-' + stringFileId + '-' + originalName[0] + originalName[1] + originalName[2] + '.' + originalName.split('.')[1]
    
def getFileIdFromFolder(path):
    fileId = 1
    for f in listdir(path):
        if isfile(join(path, f)):
            if int(f.split('-')[1]) >= fileId:
                fileId=int(f.split('-')[1])+1
        else:
            print('WARNING 04: Found folder ' + join(originPath, f) + ' and wasn\'t expected , please check it.')



def MoveFilesToTemp(originPath):
    for f in listdir(originPath):
        if isfile(join(originPath, f)):
            path2move = join(TEMP_PATH, GetDateString(join(originPath, f)))
            CreateFolder(path2move)
            move(join(originPath, f), join(path2move, f))
        else:
            print('WARNING 01: Found folder ' + join(originPath, f) + ' and wasn\'t expected , please check it.')

def GetDateString(path):
    fileDate = gmtime(getmtime(path))

    year = str(fileDate[0])

    if fileDate[1] < 10:
        month = '0' + str(fileDate[1])
    else:
        month = str(fileDate[1])

    if fileDate[2] < 10:
        day = '0' + str(fileDate[2])
    else:
        day = str(fileDate[2])

    return year + month + day

def CreateTemporalFolder():
    if not CreateFolder(TEMP_PATH):
        if listdir(TEMP_PATH).__len__() > 0:
            print('ERROR 03: ' + TEMP_PATH + ' was expected to be empty, please check it.')
            quit()
        
def CreateFolder(path):
    if not exists(path):
        makedirs(path)
        return True
    else:
        return False

def GetOriginPath():
    if argv.__len__() < 2:
        print('ERROR 01: Argument not passed')
        quit()
    
    fullpath = argv[1] + ORIGIN_PATH

    if not exists(fullpath):
        print('ERROR 02: Origin path ' + fullpath + ' doesn\'t exist')
        quit()

    return fullpath

def main():
    
    # Obtain the origin path of the files on the SD card
    _origin = GetOriginPath()

    # Create the temporal folder on destiny in case it doesn't exist
    CreateTemporalFolder()

    # Move files to each dated folder inside temp from the card
    MoveFilesToTemp(_origin)

    # Rename the files and move to their destination folder
    RenameAndMoveToDestinantionFolder()

    rmdir(TEMP_PATH)

if __name__ == "__main__":
    main()
