# If twitter changes so much as a single thing in the API or HTML then there's 
# a very good chance that this entire program will break

import requests, sys, os, time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException

##########################################
# Globals and Classes
##########################################

# Globals for really long class names
VIEW_NO_HOVER = 'css-18t94o4 css-1dbjc4n r-1niwhzg r-42olwf r-sdzlij r-1phboty \
r-rs99b7 r-1w2pmg r-15ysp7h r-gafmid r-1ny4l3l r-1e081e0 r-o7ynqc r-6416eg r-lrvibr'

VIEW_WITH_HOVER = 'css-18t94o4 css-1dbjc4n r-1l6q6pb r-42olwf r-sdzlij r-1phboty\
 r-rs99b7 r-1w2pmg r-15ysp7h r-gafmid r-1ny4l3l r-1e081e0 r-o7ynqc r-6416eg r-lrvibr'

DUMB_BANNER = 'css-1dbjc4n r-aqfbo4 r-1p0dtai r-1d2f490 r-12vffkv r-1xcajam r-zchlnj'

class PicIDSet:
    def __init__(self):
        self.ID_set = set()
        self.pic_count = 0
        self.repeat_count = 0
        self.repeat_set = set()

    def add_pic(self,picID):
        self.ID_set.add(picID)
        self.pic_count += 1
        return

    def get_count(self):
        return self.pic_count
    
    def add_repeat(self,picID):
        self.repeat_set.add(picID)
        self.repeat_count += 1
        return

##########################################
# Code
##########################################

# function that gets all elements currently loaded in HTML and downloads them
def download_loaded(driver,content,IDset):
    # looping through each element of content
    count = 0
    last = None
    last_ID_2_3 = None
    last_format = None
    group = -1
    nonew = True
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
            if picID not in IDset.repeat_set:
                IDset.add_repeat(picID)
            continue

        nonew = False
        # finding image format
        format_start = link.find("format=")
        mutable = link[format_start:]
        img_format = mutable.split("&name=",1)[0][7:]
        # changing image size to large (could be 4096x4096 for max size) 
        no_name = link.split("name=",1)[0]
        sized_link = no_name + "name=large" 
        print(sized_link)

        ID_2_3 = picID[2:4]

        if (ID_2_3 == last_ID_2_3):
            # then matches prev, need to see if group exists or not
            print("matches prev")
            if (group != -1):
                # then group dir already exists
                print("group already exists")
                f = open(f"pictures/group{group}/img{IDset.pic_count}.{img_format}","wb")
                pic = requests.get(sized_link)
                f.write(pic.content)
                f.close()
            else:
                # group dir does not exist yet
                print("group doesn't exist")
                group = IDset.pic_count - 1
                # creating directory and moving prev file, making new file
                os.mkdir(f"pictures/group{group}")
                os.rename(f"pictures/img{group}.{last_format}",f"pictures/group{group}/img{group}.{last_format}")
                f = open(f"pictures/group{group}/img{IDset.pic_count}.{img_format}","wb")
                pic = requests.get(sized_link)
                f.write(pic.content)
                f.close()
        else:
            group = -1 
            f = open(f"pictures/img{IDset.pic_count}.{img_format}","wb")
            pic = requests.get(sized_link)
            f.write(pic.content)
            f.close()

        last_format = img_format
        last_ID_2_3 = ID_2_3
        IDset.add_pic(picID)
    ActionChains(driver).move_to_element(last).perform()
    # returning last to save location
    return last, nonew

# wrapper function for the download procedure for a certain block of loaded tweets
def download(driver, IDset, last):
    # have to save the previous element that the cursor is at, since this will change it
    view_buttons = driver.find_elements(By.XPATH, f"//div[@class='{VIEW_NO_HOVER}']")
    print("CHECKING BUTTON ELEMENTS")
    # clicking all of the view buttons
    for button in view_buttons:
        try:
            ActionChains(driver).move_to_element(button).click(button).perform()
        except StaleElementReferenceException:
            print("CAUGHT EXCEPTION")
            time.sleep(2)
            try:
                ActionChains(driver).move_to_element(button).click(button).perform()
            except:
                print("Double exception, giving up on image")
            continue
        print("clicked")
    print(f"Last element: {last}")
    # returning to prev element
    if (last != None):
        ActionChains(driver).move_to_element(last).perform()
    print(f"Current picture: {IDset.pic_count}")
    print(f"Current repeat:  {IDset.repeat_count}")
    time.sleep(1.5)
    content = driver.find_elements(By.XPATH,"//img[@alt='Image']")
    last, nonew = download_loaded(driver,content,IDset)
    return last, nonew


# top function for the 
def parse(driver,IDset,imagenum):
    # first thing we want to do is delete that dumb twitter banner at the bottom of the screen
    dumb_banner = driver.find_element(By.XPATH,f"//div[@class='{DUMB_BANNER}']")
    # two lines of javascript is two lines too many
    driver.execute_script("""
    var element = arguments[0];
    element.parentNode.removeChild(element);
    """, dumb_banner)
    # running until accumulated number specified in arg
    last = None
    # need to run the loop one more time to make sure that you're at the very 
    doubleCheck = False
    while (IDset.pic_count < imagenum):
        last, nonew = download(driver,IDset,last)
        # breaking loop if no new images are found
        if ((nonew == True) and (IDset.repeat_count >= IDset.pic_count)):
            if (doubleCheck == True):
                print("No new images found")
                print(f"RC: {IDset.repeat_count}")
                break
            else: 
                print("Double checking if at end...")    
                doubleCheck = True
    return


def init(imagenum):
    # class for set of images
    IDset = PicIDSet()

    # try to grab set from set.txt file
    grab_set(IDset)

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

    # dumping set info to file
    dump_set(IDset)

    # quitting after parsing
    driver.quit()
    return

def dump_set(IDset):
    setfile = open("pictures/set.txt","w")
    for ID in IDset.ID_set:
        setfile.write(f"{ID}\n")
    setfile.close()
    return

def grab_set(IDset):
    path = "pictures/set.txt"
    # checking if file exists and isn't empty
    if (os.path.exists(path) and (os.stat(path).st_size != 0)):
        setfile = open(path,"r")
        setlist = setfile.readlines()
        for setElem in setlist:
            IDset.add_pic(setElem.split("\n")[0])
    
    print(IDset.pic_count)
    return

if __name__ == '__main__':
    username = sys.argv[1]
    imagenum = int(sys.argv[2])
    sys.stdout = open("output.txt","w")
    init(imagenum)
    sys.stdout.close()