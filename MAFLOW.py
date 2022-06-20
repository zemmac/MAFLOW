import datetime
import os
import shutil


def traverseInside(path):
    # lP - licznikPlikow
    # lB - licznikBledow
    # lBF - licznikBledowFolder
    listaZawartosci = os.listdir(path)
    for i in listaZawartosci:
        if os.path.isdir(path+'\\'+i):
            traverseInside(path+'\\'+i)
        else:
            if 'nok' not in i.lower() and 'error' not in i.lower():
                t = os.stat(path+'\\'+i)[8] # [8] - creation timestamp stored here
                if dzis.timestamp().__round__() - t > 15768000:
                    try:
                        os.remove(path+'\\'+i)
                        plikLog.write(path + '\\' + i + '       removed.        OK\n')
                    except OSError as error:
                        plikLog.write('\n' + path + '\\' + i + '    Unable to remove file ' + str(error) + '\\n')

    if len(os.listdir(path)) == 0:
        try:
            os.rmdir(path)
            plikLog.write(path + '  Folder removed.         OK\n')
        except OSError as error:
            plikLog.write(path + '      Unable to remove folder.    ' + str(error) + '\\n')


def insertHeadSorting(plik):
    head = '****************************************\n' \
           'Log file: ' + logName + '\n' + \
           '****************************************\n' \
           '\n' \
           'Sorting section\n' \
           '####################\n'
    # 40
    plik.write(head)


def SummarySorting(plik):
    bottom = '\n####################\n' \
             'Sorting section summary\n' \
             '****************************************\n' \
             'Total files: ' + str(licznikPlikow) + '\n' + \
             'Files moved: ' + str(licznikPlikow - licznikBledow) + '\n' + \
             'Errors:  ' + str(licznikBledow) + '\n' \
             '****************************************\n\n\n'  # 40
    plik.write(bottom)


def insertHeadDelOKs(plik):
    head = '\n\n###############################\n' \
           'Delete OKs older than 182 days\n' \
           '###############################\n' \
           '\n\n'

    plik.write(head)


def SummaryDelOKs(plik):
    bottom = '\n\n####################\n' \
             'Delete OKs summary\n' \
             '****************************************\n' \
             'Total files: ' + str(licznikPlikow) + '\n' + \
             'Errors:  ' + str(licznikBledow) + '\n' \
             '****************************************\n\n\n'  # 40
    plik.write(bottom)


def folderCreation(nowyKatalog):
    ####
    # Folder creation
    ####
    try:
        os.makedirs(nowyKatalog, exist_ok=True)
    except OSError as error:
        msg = 'Unable to create a new folder!  '
        plikLog.write(msg + str(error))


def nameCreation(data):
    if data.day < 10:
        dzien = str('0'+str(data.day))
    else:
        dzien = str(data.day)
    if data.month < 10:
        miesiac = str('0'+str(data.month))
    else:
        miesiac = str(data.month)

    return str(data.year)+miesiac+dzien+'_'+str(data.hour)+'h'+str(data.minute)+'m'


# Path to network disk where images are stored
#path = "C:\\PRACA\\Python\\MAFLOW\\TEST\\"
path = 'K:\\'

logName = nameCreation(datetime.datetime.today())

# new log file creation
if os.path.isdir(path+'log\\'):
    plikLog = open(path+'log\\'+'log'+logName+'.txt', "w")
else:
    folderCreation(path+'log\\')
    plikLog = open(path+'log\\'+'log'+logName+'.txt', "w")

insertHeadSorting(plikLog)

#####
# Move files to correct folders
#####
listaPlikow = os.listdir(path)
licznikPlikow = 0
licznikBledow = 0
for i in listaPlikow:
    sciezkaPliku = path + i

    if i == 'archiv':
        continue
    if os.path.isdir(sciezkaPliku):
        continue
    if '.bmp' in i.lower() or '.jpg' in i.lower():
        licznikPlikow += 1
        znakCzasu = os.stat(sciezkaPliku)[8]
        dataUtworzenia = datetime.datetime.fromtimestamp(znakCzasu)

        # According to file creation date - create folder name
        rok = str(dataUtworzenia.year)

        # Get the shift number according to creation hour
        # If a file was created during III shift after midnight - subtract one day
        if dataUtworzenia.hour < 6:
            znakCzasu = os.stat(sciezkaPliku)[8] - 86400
            dataUtworzenia = datetime.datetime.fromtimestamp(znakCzasu)
            zmiana = '\\III'
        elif 6 <= dataUtworzenia.hour < 14:
            zmiana = '\\I'
        elif 14 <= dataUtworzenia.hour < 22:
            zmiana = '\\II'
        elif dataUtworzenia.hour >= 22:
            zmiana = '\\III'
        else:
            zmiana = ''

        if dataUtworzenia.month < 10:
            miesiac = '0'+str(dataUtworzenia.month)
        else:
            miesiac = str(dataUtworzenia.month)

        if dataUtworzenia.day < 10:
            dzien = '0'+str(dataUtworzenia.day)
        else:
            dzien = str(dataUtworzenia.day)

        # Path to folder where current file should be stored
        sciezkaKatalogu = path+'archiv\\'+rok+miesiac+dzien+zmiana

        # Check if this path exists. If not - create folder
        if os.path.exists(sciezkaKatalogu):

            try:
                shutil.move(sciezkaPliku, sciezkaKatalogu+'\\'+i)
                plikLog.write(str(licznikPlikow)+': ' + i + '       moved to:   ' + sciezkaKatalogu + '\\'+'    OK\n')
            except OSError as error:
                plikLog.write('\n' + str(licznikPlikow) + ': ' + i + '     Unable to move file! ' + str(error) + '\n\n')
                licznikBledow += 1

        else:
            folderCreation(sciezkaKatalogu)
            try:
                shutil.move(sciezkaPliku, sciezkaKatalogu+'\\'+i)
                plikLog.write(str(licznikPlikow)+': ' + i + '       moved to:   ' + sciezkaKatalogu + '\\'+'    OK\n')
            except OSError as error:
                plikLog.write('\n' + str(licznikPlikow) + ': ' + i + '     Unable to move file! ' + str(error) + '\n\n')
                licznikBledow += 1

    else:
        try:
            os.remove(sciezkaPliku)
            plikLog.write(str(licznikPlikow)+': ' + i + '       removed.        OK\n')
        except OSError as error:
            plikLog.write('\n' + str(licznikPlikow) + ': ' + i + '  Unable to remove file! ' + str(error) + '\n\n')
            licznikBledow += 1

SummarySorting(plikLog)

####
# Traversing 'archiv' folder and delete OK's older than 6Mo
####

insertHeadDelOKs(plikLog)

pathArchiv = path+'archiv\\'
licznikPlikow = 0
licznikBledow = 0
licznikBledowFolder = 0

if os.path.exists(pathArchiv):
    listaFolderow = sorted(os.listdir(pathArchiv))
    dzis = datetime.datetime.today()

    for i in listaFolderow:

        # Format YYYYMMDD
        if i.isnumeric() and len(i) == 8:
            folderRok = int(i[:4])
            folderMiesiac = int(i[4:6])
            folderDzien = int(i[6:8])
            ta = datetime.\
                datetime.\
                __new__(datetime.datetime, folderRok, folderMiesiac, folderDzien, 23, 59, 59).\
                timestamp().\
                __round__()

            if dzis.timestamp().__round__() - ta > 1576800:

                ####
                # If folder is older than 182days traverse inside it and delete OKs
                ####
                if os.path.isdir(pathArchiv+i):
                    traverseInside(pathArchiv+i)
        else:
            plikLog.write('\n' + path + '\\' + i + '     Wrong folder name!\n\n')


#SummaryDelOKs(plikLog)

plikLog.close()
