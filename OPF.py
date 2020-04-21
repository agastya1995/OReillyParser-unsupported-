import os
import datetime
import random


class OPF_Creator():
    '''
    Creates an opf file (to create the mobi file)
    '''
    def __init__(self, Directory = '.', NCX_File = None, HTML_TOC = None):
        self.OPF_File = open(os.path.join(Directory,'content.opf'), 'w')
        self.NCX_File = NCX_File
        self.HTML_TOC = HTML_TOC
        self.HTML_ID = 'HTML_Table_of_Contents'
        self.NCX_ID = 'NCX_Table_of_Contents'
    
    def Start_File(self, DocumentTitle='News', Author='Author'):
        ''' Write metadata and other heading information '''
        print(
f'''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" 
xmlns:dc="http://purl.org/dc/elements/1.1/"
version="2.0" unique-identifier="BookId">

<metadata>
    <dc:title>{DocumentTitle}</dc:title>
    <dc:language>en</dc:language>
     <dc:identifier id="BookId"> urn:uuid:112358132134</dc:identifier>
    <meta name="cover" content="My_Cover" />
    <dc:creator>{Author}</dc:creator>
</metadata>

<manifest>''', file=self.OPF_File)

    def Add_HTML_ItemID(self, id, link):
        # All links should be in ascii
        ASCII_Link = link.encode('utf-8', errors='ignore').decode('ascii', errors='ignore')
        '''
        Adds item to the manifest, linking it with the idrefs in the manifest
        '''
        print(f'<item id="item{id}" media-type="application/xhtml+xml" href="{ASCII_Link}"/>', file=self.OPF_File)
    

    def Add_Image_ID(self, id, link):
        ASCII_Link = link.encode('utf-8', errors='ignore').decode('ascii', errors='ignore')
        print(f'<item id="item{id}" media-type="image/png" href="{ASCII_Link}"/>', file=self.OPF_File)




    def EndItemID(self, ):
        print(f'''<item id="{self.HTML_ID}" media-type="application/xhtml+xml" href="{self.HTML_TOC}"/>
    <item id="{self.NCX_ID}"  media-type="application/x-dtbncx+xml"  href="{self.NCX_File}"/>
</manifest>
<spine toc="{self.NCX_ID}">
    ''', file=self.OPF_File)

    def Append_String(self, string):
        print(string, file=self.OPF_File)
    
    def Add_ItemRef(self, id):
        print(f'<itemref idref = "item{id}"/>', file=self.OPF_File)
    
    def End_File(self):      
        print(f'''
    </spine>
</package>
''', file=self.OPF_File)

    def CloseFile(self):
        self.OPF_File.close()

'''
    <guide>
        <reference type="toc" title="{self.NCX_ID}" href="{self.NCX_File}" />
    </guide>
'''

