# If twitter changes so much as a single thing in the API or HTML then there's 
# a very good chance that this entire program will break

import requests, sys, os, time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

##########################################
# Globals and Classes
##########################################

# Globals for really long class names
VIEW_NO_HOVER = 'css-18t94o4 css-1dbjc4n r-1niwhzg r-42olwf r-sdzlij r-1phboty \
r-rs99b7 r-1w2pmg r-15ysp7h r-gafmid r-1ny4l3l r-1e081e0 r-o7ynqc r-6416eg r-lrvibr'

VIEW_WITH_HOVER = 'css-18t94o4 css-1dbjc4n r-1l6q6pb r-42olwf r-sdzlij r-1phboty\
 r-rs99b7 r-1w2pmg r-15ysp7h r-gafmid r-1ny4l3l r-1e081e0 r-o7ynqc r-6416eg r-lrvibr'

DUMB_BANNER = 'css-1dbjc4n r-aqfbo4 r-1p0dtai r-1d2f490 r-12vffkv r-1xcajam r-zchlnj'

# Global for keeping track of last element postition when downloading. 
# Needed since clicking "view" will cause position to change
# LAST_ELEMENT = None

class PicIDSet:
    def __init__(self):
        self.ID_set = set()
        self.pic_count = 0

    def add_pic(self,picID):
        self.ID_set.add(picID)
        self.pic_count += 1

    def get_count(self):
        return self.pic_count

# i am ashamed that i actually made this

##########################################
# Code
##########################################

# function that gets all elements currently loaded in HTML and downloads them
def download_loaded(driver,content,IDset):
    # looping through each element of content
    count = 0
    last = None
    for element in content:
       # getting element src field
       link = element.get_property("src")
       # finding image ID, adding to set
       picID = link.split("media/")[1].split("?format")[0]
       # saving last element used
       last = element
       # don't want to load image if already in the set
       if picID in IDset.ID_set:
           print("ALREADY IN ID SET")
           continue
       # finding image format
       format_start = link.find("format=")
       mutable = link[format_start:]
       img_format = mutable.split("&name=",1)[0][7:]
       # changing image size to large (could be 4096x4096 for max size) 
       no_name = link.split("name=",1)[0]
       sized_link = no_name + "name=large" 
       print(sized_link)
       # requesting image 
       f = open(f"pictures/img{IDset.pic_count}.{img_format}","wb")
       pic = requests.get(sized_link)
       f.write(pic.content)
       f.close()
       # adding to ID set, increments internal counter
       IDset.add_pic(picID)
    ActionChains(driver).move_to_element(last).perform()
    # returning last to save location
    return last

# wrapper function for the download procedure for a certain block of loaded tweets
def download(driver, IDset, last):
    # have to save the previous element that the cursor is at, since this will change it
    view_buttons = driver.find_elements(By.XPATH, f"//div[@class='{VIEW_NO_HOVER}']")
    print("CHECKING BUTTON ELEMENTS")
    # clicking all of the view buttons
    for button in view_buttons:
        ActionChains(driver).move_to_element(button).click(button).perform()
        print("clicked")
    print(f"Last element: {last}")
    if (last != None):
        ActionChains(driver).move_to_element(last).perform()
    time.sleep(3)
    content = driver.find_elements(By.XPATH,"//img[@alt='Image']")
    last = download_loaded(driver,content,IDset)
    return last


# top function for the 
def parse(driver,IDset,imagenum):
    # first thing we want to do is delete that dumb twitter banner at the bottom of the screen
    dumb_banner = driver.find_element(By.XPATH,f"//div[@class='{DUMB_BANNER}']")
    # two lines of javascript is two lines too many
    driver.execute_script("""
    var element = arguments[0];
    element.parentNode.removeChild(element);
    """, dumb_banner)
    # a couple of download commands to see how it runs
    last = None
    while (IDset.pic_count < imagenum):
        last = download(driver,IDset,last)
    return


def init(imagenum):
    # class for set of images
    IDset = PicIDSet()

    # initialize webdriver, pass in path to chromedriver binary
    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    driver.get(f"https://twitter.com/{username}")

    # waiting 10 seconds for page to load first picture with certain class name
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//img[@alt='Image']"))
        )
    finally:
        parse(driver, IDset, imagenum)

    # quitting after parsing
    driver.quit()
    return


if __name__ == '__main__':
    username = sys.argv[1]
    imagenum = int(sys.argv[2])
    sys.stdout = open("output.txt","w")
    init(imagenum)
    sys.stdout.close()