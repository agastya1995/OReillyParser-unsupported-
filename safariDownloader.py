import requests
import bs4
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException, WebDriverException
import time
import wget
import os
import re
from requests.auth import HTTPBasicAuth
from xml.sax.saxutils import escape
from metadata_strings import toc_start, toc_end, opf_start, html_start, html_end
from EPUB import metadata, create_archive
import multiprocessing
from urllib.error import HTTPError
import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TOC_and_Metadata():
    def __init__(self, link, username, password):
        req = requests.get(link, auth=HTTPBasicAuth(username, password))
        self.soup = bs4.BeautifulSoup(req.text, features='html.parser')


    def create_TOC(self, file_name = 'toc.xhtml'):
        
        #Creates a well formed html table of contents. Returns the first link of the table
        
        toc = self.soup.find('ol', class_='detail-toc')
        list_items = (toc.find_all('li'))
        table_data = []

        for i in list_items: 
            table_data.append([escape(i.find('a')['href'], {'&quot;':'"', '&apos;':"'"}), 
                            escape(i.find('a').text, {'&quot;':'"', '&apos;':"'"}),
                            int(i['class'][0].split("toc-level-")[-1])])

        first_link = table_data[0][0]
        current_level = 1

        with open(file_name, 'w') as f:
            print(toc_start(), file=f)

            for i in range(len(table_data)):
                current_level = table_data[i][2]

                link = table_data[i][0].split(r'/')[-1]
                try:
                    next_level = table_data[i+1][2]
                except(IndexError):
                    next_level = table_data[i][2]
                    pass

                # If on the same level
                if table_data[i][2] == current_level and next_level == current_level:
                    print(f'<li> <a href="{link}"> {table_data[i][1]}</a> </li>', file=f)

                # If the next item is one level down
                if table_data[i][2] == current_level and next_level > current_level:
                    print(f'<li> <a href="{link}"> {table_data[i][1]}</a>', file=f)
                    print('<ol>', file=f)
                
                # If the next item is a level (or more) up 
                if table_data[i][2] == current_level and next_level < current_level:
                    print(f'<li> <a href="{link}"> {table_data[i][1]}</a> </li>', file=f)
                    for j in range(current_level-next_level):
                        print('</ol>', file=f) # Close the tag(s)
                        print('</li>', file=f)
                    
            for i in range(current_level):
                print('</ol>', file=f)
            print(toc_end(), file=f)
        return first_link


    def parse_metadata(self):
        '''
        Returns a list of title, author and publisher
        '''

        metadata_elem = self.soup.find('div', class_='metadata')

        author = metadata_elem.find(class_='author t-author').text.split('\n')[1].strip()
        title = metadata_elem.find(class_='title t-title').text
        publisher = metadata_elem.find(class_='publisher t-publisher').text.split('\n')[1].strip()

        return(title, author, publisher)


class OPFCreator():
    def __init__(self):
        # Create two files - one for the spine and one for the manifest, then join them later
        self.manifest = open('manifest.txt', 'w+')
        self.manifest.write('<manifest>\n<item id="toc" properties="nav" media-type="application/xhtml+xml" href="toc.xhtml"/>\n')
        self.spine = open('spine.txt', 'w+')
        self.spine.write('<spine>\n')


    def Add_Items(self, id, link=None, image=None):

        # add html links to both the spine and the manifest
        if link is not None:
            self.manifest.write(
                f'<item href="{link}" id="{id}" media-type="application/xhtml+xml"/>\n')
            self.spine.write(f'<itemref idref="{id}"/>\n')

        if image is not None:
            self.manifest.write(
                f'<item href="{image}" id="{id}" media-type="image/jpeg"/>\n')


    def Merge_into_OPF(self, title, author, isbn, publisher, language):

        opf = open('content.opf', 'w')
        opf.write(opf_start(title, author, isbn, publisher, language))

        # Seek start of manifest and spine, and copy them to the opf
        self.spine.seek(0)
        self.manifest.seek(0)
        opf.write(self.manifest.read())
        opf.write('\n</manifest>\n')
        opf.write(self.spine.read())
        opf.write('\n</spine>\n')
        opf.write('</package>\n')

        self.spine.close()
        self.manifest.close()
        opf.close()


class SafariBookParser():
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('log-level=3')
        try:
            self.driver = webdriver.Chrome(chrome_options=chrome_options)
        except(WebDriverException):
            print('Chrome driver needs to be in PATH. Please see https://sites.google.com/a/chromium.org/chromedriver/home.')
            print('Exiting')
            sys.exit()


    def logIn(self, username, password):
        # Log in to selenium - method needs to be changed
        signInPage = r'https://www.oreilly.com/member/'
        self.driver.get(signInPage)

        # Check if the log in page has loaded. If not, refresh
        while True:
            try:
                username_field = self.driver.find_element_by_name('email')
                break
            except(NoSuchElementException):
                self.driver.refresh()

        username_field.clear()
        username_field.send_keys(username)

        password_field = self.driver.find_element_by_name('password')
        password_field.clear()
        password_field.send_keys(password)

        # Click the log in button
        self.driver.find_element_by_tag_name('button').click()

        # See if credentials are correct by seeing if the page has moved forward or not. 5 seconds timeout
        try:
            WebDriverWait(self.driver, 5).until(EC.url_changes(signInPage))
            self.auth = HTTPBasicAuth(username, password)
        except(TimeoutException):
            print('Wrong credentials provided. Please check your username and password and try again')
            sys.exit()


    def closeDriver(self):
        self.driver.close()

    @staticmethod
    def wget(link):
        # Downloads a file using wget. Returns None in case of HTTP error
        try:
            return wget.download(link)
        except(HTTPError):
            return None


    def parseBook(self, page_url, maxImageSize=0):
        '''
        Parses each html page, saves it as an html file and adds the details to the opf and table of contents
        If Max Image Size is set, all images will be proportionately decreased to the maximum level specified. 
        Returns the ISBN (the folder name)
        '''
        #base_page = (r'/').join(page_url.split(r'/')[:-1])+r'/'
        ISBN = page_url.split(r'/')[-2]
        domain = r'https://learning.oreilly.com'

        # First link of the table of contents
        toc = TOC_and_Metadata(page_url, self.auth.username, self.auth.password)
        first_toc_link = toc.create_TOC()
        title, author, publisher = toc.parse_metadata()
        
        self.driver.get(page_url)

        # Click on the first link onto the table of contents, then move backwords till the program reaches the first page
        self.driver.get(domain+first_toc_link)

        while True:
            self.driver.refresh()
            try:
                self.driver.find_element_by_xpath(
                    r'//*[@id="container"]/div[2]/section/div[1]/a').click()
            except(NoSuchElementException):
                break

        # Create opf file
        opf = OPFCreator()
        id = 0

        while True:
            self.driver.refresh()
            currentURL = self.driver.current_url
            page_source = self.driver.page_source
            soup = bs4.BeautifulSoup(page_source, features='html.parser')

            id_elem = soup.find(class_='annotator-wrapper')
            # If the text is not parsed
            if id_elem == None:
                continue
            try:
                imageElements = id_elem.findAll(['img']) # List of all elements
            except(AttributeError):
                imageElements = None

            if imageElements is not None:
                fullImageLinkList = [r'https://learning.oreilly.com'+i['src'] for i in imageElements] # Full link for downloading
                imageNameList = [i['src'].split(r'/')[-1] for i in imageElements] # Name of image (will be saved using this name)

                # Add images to opf
                for image in imageNameList:
                    opf.Add_Items(id=id, image=image)
                    id +=1

                # Check if image exists in folder. If it does, delete from the list of images to be downloaded
                for i in reversed(range(len(imageNameList))):
                    if os.path.isfile(imageNameList[i]):
                        imageNameList.pop(i)
                        fullImageLinkList.pop(i)

                # Download all images using wget 
                if len(fullImageLinkList) >0:  
                    print(f'\n Download {len(fullImageLinkList)} images')      
                    processes = multiprocessing.Pool()
                    processes.map(SafariBookParser.wget, fullImageLinkList)
                    processes.close()
                    processes.join()
            
            # Change the 'src' of images in the downloaded html file to point to images in the folder.
            # Also, change the width and height to the max limit 
            for elem in id_elem:
                try:
                    for imageElem in elem.findAll('img'):
                        imageElem['src'] = imageElem['src'].split(r'/')[-1]
                        
                        if maxImageSize > 0:
                            width, height = int(imageElem['width']), int(imageElem['height'])
                            if width > maxImageSize or height > maxImageSize: 
                                if width >= height:
                                    imageRatio = width/height
                                    imageElem['width'] = str(maxImageSize)
                                    imageElem['height'] = str(maxImageSize/imageRatio)
                                else:
                                    imageRatio = height/width
                                    imageElem['height'] = str(maxImageSize)
                                    imageElem['width'] = str(maxImageSize/imageRatio)
                except(AttributeError):
                    pass

            # Open file, save the required metadata and then the contents to an html file
            page_name = currentURL.split(r'/')[-1]
            opf.Add_Items(id=id, link=page_name)
            id += 1
            
            with open(page_name, 'w', encoding='utf-8') as f:
                print(html_start(), file=f)

                # Print content. Break when it reaches a certain class
                for i in id_elem.children:
                    try:
                        break_point = i.find(
                            class_='annotator-widget annotator-listing')
                    except(TypeError):
                        break_point = None

                    if break_point is not None:
                        break
                    else:
                        print(i, file=f)  # Escape xml characters

                print(html_end(), file=f)

            # Next Page
            try:
                self.driver.find_element_by_xpath(
                    r'//*[@id="container"]/div[2]/section/div[2]/a').click()
            except(NoSuchElementException):  # End of book
                opf.Merge_into_OPF(title, author, ISBN, publisher, 'en')
                os.chdir(os.pardir)
                return title
