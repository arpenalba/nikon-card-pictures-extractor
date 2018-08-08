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
                fileId = 0
            else:
                fileId = getFileIdFromFolder(join(DESTINATION_PATH, folder))

            for file in listdir(join(TEMP_PATH, folder)):
                if isfile(join(join(TEMP_PATH, folder), file)):
                    newFileName = GetNewFileName(file, folder, fileId)
                    rename(join(join(TEMP_PATH, folder), file), join(join(DESTINATION_PATH, folder), newFileName))
                else:
                    print('WARNING 03: Found folder ' + join(join(TEMP_PATH, folder), file) + ' and wasn\'t expected , please check it.')
                    quit()
        else:
            print('WARNING 02: Found file ' + join(TEMP_PATH, folder) + ' and wasn\'t expected , please check it.')
            
def GetNewFileName(originalName, dateString, fileId):
    print ('GetNewFileName ' + originalName + ' ' + dateString + ' ' + fileId)
    
def getFileIdFromFolder(path):
    print ('GetFileIdFromFolder ' + path)


def MoveFilesToTemp(originPath):
    for file in listdir(originPath):
        if isfile(join(originPath, file)):
            originFileDate = gmtime(getmtime(join(originPath, file)))
            path2move = join(TEMP_PATH, str(originFileDate)[0] + str(originFileDate)[1] + str(originFileDate)[2])
            CreateFolder(path2move)
            move(join(originPath, file), join(path2move, file))
        else:
            print('WARNING 01: Found folder ' + join(originPath, file) + ' and wasn\'t expected , please check it.')
        

def CreateFolder(path):
    if not exists(path):
        makedirs(path)
        return True
    else:
        return False

def CreateTemporalFolder():
    if not CreateFolder(TEMP_PATH):
        if listdir(TEMP_PATH).__len__ > 0:
            print('ERROR 03: ' + TEMP_PATH + ' was expected to be empty, please check it.')
            quit()


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
