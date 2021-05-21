import requests, os, sys

from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# img = open("testimg.jpeg","wb")
# response = requests.get('https://pbs.twimg.com/media/E1wg2SxVoAkwPIT?format=jpg&name=4096x4096')

# print("HEADERS:\n")
# print(response.headers)
# img.write(response.content)
# img.close()

def get():


    driver = webdriver.Chrome('/usr/local/bin/chromedriver')

    driver.get(f"https://twitter.com/{username}")

    # session = HTMLSession()

    # r = session.get('http://python-requests.org')

    # r.html.render()

    # user = requests.get('')
    # print(user,"\n")
    # print(user.headers) 
    # print(user.text)
    return


if __name__ == '__main__':
    username = sys.argv[1]
    sys.stdout = open("output.txt","w")
    get()
    sys.stdout.close()