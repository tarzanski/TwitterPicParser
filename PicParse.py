from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def get():


    driver = webdriver.Chrome('/usr/local/bin/chromedriver')

    driver.get(f"https://twitter.com/{username}")

    return


if __name__ == '__main__':
    username = sys.argv[1]
    sys.stdout = open("output.txt","w")
    get()
    sys.stdout.close()