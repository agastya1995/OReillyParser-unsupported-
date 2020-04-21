from safariDownloader import SafariBookParser, metadata, create_archive
import sys
import os
import shutil
import tempfile

if __name__=='__main__':
    args = len(sys.argv)-1

    helpDocs = '''
    Usage - python bookDownloader.py book_url email password image_size(optional)

    You can also run the file without any arguments and enter the information at the prompt. 
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
        print(helpDocs)
        sys.exit()  

    
    currentFolder = os.getcwd()
    isbn = bookLink.split(r'/')[-2]

    # Checks if the folder already exists or not (in case the program crashed earlier)
    tempFolder = None
    for folder in os.listdir(tempfile.gettempdir()):
        if folder.endswith(isbn):
            tempFolder = os.path.join(tempfile.gettempdir(), folder)
            break
        
    if tempFolder == None:
        tempFolder = tempfile.mkdtemp(suffix='__'+isbn)

    os.chdir(tempFolder)

    print('\nOpening Selenium Browser\n')
    parser = SafariBookParser()  

    print('\nLogging In \n')
    parser.logIn(user, pwd)

    print('Parsing Book. This could take between 5-25 minutes, depending on the size of the book. \n')
    title = parser.parseBook(bookLink, maxImageSize=imageSize)

    metadata(tempFolder)
    create_archive(title+'.epub', tempFolder)
    parser.closeDriver()

    print('\nCompleted')

    # Copy epub to the main folder and delete the temp folder
    shutil.copy(os.path.join(tempFolder, title +'.epub'), currentFolder)
    shutil.rmtree(tempFolder)
