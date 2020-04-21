from safariDownloader import SafariBookParser, metadata, create_archive
import sys
import os
import shutil
import tempfile

args = len(sys.argv)-1

helpDocs = '''
TO ensure the program works corectly, put the arguments within single quotes 
Fill it up
'''

if args == 0:
    bookLink = input('Enter link to the home page of the book\n')
    user = input('Enter Username \n')
    pwd = input('Enter Password \n')
    imageSize = 600

elif args == 1:
    if sys.argv[1] == '--help' or sys.argv[1] == '-h':
        print(helpDocs)
    else:
        print('Command Not Found. Use --help for commands')
    sys.exit()

elif args == 3:
    bookLink = sys.argv[1]
    user = sys.argv[2]
    pwd = sys.argv[3]
    imageSize = 600

elif args == 4:
    bookLink = sys.argv[1]
    user = sys.argv[2]
    pwd = sys.argv[3]
    imageSize = int(sys.argv[4])

else:
    print('Wrong number of arguments. Use -h or --help for help')
    sys.exit()  


currentFolder = os.getcwd()
tempFolder = tempfile.mkdtemp()

os.chdir(tempFolder)

print('\nLogging In \n')
parser = SafariBookParser()  
parser.logIn(user, pwd)

print('Parsing Book. This could take between 5-25 minutes, depending on the size of the book. \n')
isbn, title = parser.parseBook(bookLink, maxImageSize=imageSize)

metadata(isbn)
create_archive(title+'.epub', isbn)
parser.closeDriver()

print('\nCompleted')

# Copy epub to the main folder and delete the temp folder
shutil.copy(os.path.join(tempFolder, isbn, title+'.epub'), currentFolder)
