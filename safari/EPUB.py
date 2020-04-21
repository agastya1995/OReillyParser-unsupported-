import zipfile, os
import shutil

def metadata(path='.'):  
    Old_Working_Directory = os.getcwd() 
    '''
    Create files needed by epub
    '''
    os.chdir(path)
    os.mkdir('OPS')

    for file in os.listdir('.'):
        if file == 'OPS':
            continue
        shutil.move(file, os.path.join('OPS', file))
    os.mkdir('META-INF')
    with open (os.path.join('META-INF', 'container.xml'), 'w') as f:
        print('''<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OPS/content.opf"
     media-type="application/oebps-package+xml" />
  </rootfiles>
</container>
        ''', file=f)
    
    with open('mimetype', 'w') as f:
        print('application/epub+zip', sep='', file=f)
    os.chdir(Old_Working_Directory)


def create_archive(epub_name, path='.'):
    '''Create the ZIP archive.  The mimetype must be the first file in the archive 
    and it must not be compressed.'''

    # Open a new zipfile for writing
    os.chdir(path)

    epub = zipfile.ZipFile(epub_name, 'w')
 
    # Add the mimetype file first and set it to be uncompressed
    epub.write('mimetype', compress_type=zipfile.ZIP_STORED)
     
    # For the remaining paths in the EPUB, add all of their files
    # using normal ZIP compression
    for p in os.listdir('.'):
        if os.path.isdir(p):
            for f in os.listdir(p):
                epub.write(os.path.join(p, f), compress_type=zipfile.ZIP_STORED)
    epub.close()


