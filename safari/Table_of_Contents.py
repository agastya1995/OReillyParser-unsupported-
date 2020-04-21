import os
import datetime
import xml


class NCX_Table_of_Contents():
    def __init__(self, Directory = '.'):
        self.Path = 'Table_of_Contents.ncx'
        self.NCX_File = open(os.path.join(Directory, self.Path), 'w')
    
    def Start_File(self, level=1):
        print(
f'''<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns:mbp="http://mobipocket.com/ns/mbp" xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="en-GB">
<head>
    <meta content="urn:uuid:112358132134" name="dtb:uid"/>
    <meta content="{level}" name="dtb:depth"/>
    <meta content="0" name="dtb:totalPageCount"/>
    <meta content="0" name="dtb:maxPageNumber"/>
</head>
<docTitle>
    <text>News</text>
</docTitle>
<docAuthor>s
    <text>Kindle News Reader</text>
</docAuthor>
<navMap>
    ''', file=self.NCX_File)

    def PlayOrder(self, count, heading, filelink):
        ASCII_Heading = xml.sax.saxutils.escape(heading.encode('utf-8', errors='ignore').decode('ascii', errors='ignore'),{'&quot;':'"', '&apos;':"'"})
        ASCII_Filelink = xml.sax.saxutils.escape(filelink.encode('utf-8', errors='ignore').decode('ascii', errors='ignore'),{'&quot;':'"', '&apos;':"'"})
        '''
        Count - item number, starts from 1 onwards
        description - Title Heading
        filename - the actual filename (must be in the same folder)
        '''
        print(f'''
    <navPoint playOrder="{count}" class="article" id="item{count}">
    <navLabel>
        <text>{ASCII_Heading}</text>
    </navLabel>
    <content src="{ASCII_Filelink}" />''', file=self.NCX_File)

    def End_File(self):
        '''Closes out the navpoints, navmap and ncx headings'''
        print(f'''
    </navPoint>
  </navMap>
</ncx>
''', file=self.NCX_File)

    def Append_String(self, string):
        print(string, file=self.NCX_File)

    def Close_File(self):
        self.NCX_File.close()


class HTML_Table_of_Contents():
    def __init__(self, Directory = '.'):
        self.Path = 'HTML_Table_of_Contents.xhtml'
        self.HTML_File = open(os.path.join(Directory ,self.Path), 'w')
    
    def Start(self):
        print(
'''<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta content="text/html" http-equiv="Content-Type"/>
    <title>Table of Contents</title>
  </head>
  <body>
  <h1> Table of Contents </h1>
  <ul>
''', file=self.HTML_File)

    def Append_String(self, string):
        print(string, file=self.HTML_File)
    
    def Add_Link(self, FileName, Title):
        ASCII_Filename = FileName.encode('utf-8',errors='ignore').decode('ascii', errors='ignore')
        ASCII_Title = Title.encode('utf-8',errors='ignore').decode('ascii', errors='ignore')
        print(f'<li> <a href="{ASCII_Filename}.xhtml">{ASCII_Title} </a></li>', file=self.HTML_File) 
    
    def End_File(self):
        print(f'''
        </ul>
    </body>
</html>'''	, file=self.HTML_File) 

    def Close_File(self):
        self.HTML_File.close()


