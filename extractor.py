from os import listdir, rename, makedirs, rmdir
from os.path import getmtime, isfile, join, exists
from time import gmtime
from shutil import move
from sys import argv

# 0	tm_year	(for example, 1993)
# 1	tm_mon	range [1, 12]
# 2	tm_mday	range [1, 31]
# 3	tm_hour	range [0, 23]
# 4	tm_min	range [0, 59]



def main():
    
    _origin =  ':\\Users\\aromeropenalba\\Desktop\\origin'
    _destiny = 'D:\\Temp\\nikon-test'
    _temp = join(_destiny, 'temp')
    _dates = []

    if argv.__len__() > 1:
        _origin = argv[1] + _origin
    else:
        print('IN YOUR FACE!!!')

    if not exists(_temp):
        makedirs(_temp)

    onlyfiles = [f for f in listdir(_origin) if isfile(join(_origin, f))]
    for f in onlyfiles:
        move(join(_origin, f), join(_temp, f))

    for f in onlyfiles:
        date = str(gmtime(getmtime(join(_temp, f)))[0])
        newPath = join(_destiny, date)
        if not exists(newPath):
            makedirs(newPath)
        rename(join(_temp, f), join(newPath, date + '-' + f))

    rmdir(_temp)

if __name__ == "__main__":
    main()
