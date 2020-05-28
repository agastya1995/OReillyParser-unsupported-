# OReillyParser

#### A simple script that scrapes the book from O'Reilly Media and saves it as an epub. ####


## USAGE: ##

` python bookDownloader.py URL USERNAME PASSWORD IMAGE_SIZE `

If no arguments are given, the script will prompt for an input.

##### Requirements #####

Apart from the required python libraries (given in the requirements.txt file), you will also need to download chromedriver from [here](https://sites.google.com/a/chromium.org/chromedriver/home). The version of the chrome driver should be the same as your version of google chrome. Additionally, the chromedriver executable must be in your PATH.

##### Arguments #####

Url - The url to the book to download. It should be the home page of the book. The format is 
"https://learning.oreilly.com/library/view/book_name/isbn/". 
The link will always end with a 10 digit book id (isbn). 

Username - The email used to sign up. Your username must be valid and should have premium access (on signing up, you will get a 15 day free trial). ##### Do not use your Google/Linkedin or any other OAuth account to sign up, but instead manually fill up the sign up form. I recommend using disposable emails like this one[10minutemail.com] #### 
Password - The password of the abovementioned user id. Please note that the password is not hidden.

Image Size - (Optional) - The maximum dimmension (either length or width) of the images in the book. Default is 600 pixels. 

In case no arguments are entered, the program will ask for the url, username and password.



