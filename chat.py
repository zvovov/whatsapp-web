#! /usr/bin/python3

import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# WW = Whatsapp Web = web.whatsapp.com
wwUrl = "https://web.whatsapp.com/"


def main():
    # setting up Chrome with selenium
    driver = webdriver.Chrome('/home/chirag/src/chromedriver/chromedriver')

    # open WW in browser
    driver.get(wwUrl)

    # prompt user to connect device to WW
    while True:
        isConnected = input("\n\t Phone connected? y/n: ")
        if isConnected.lower() == 'y':
            break

    assert "WhatsApp" in driver.title

    # search name of friend/group
    if len(sys.argv) > 1:
        friendName = ' '.join(sys.argv[1:])
        searchBar = driver.find_element(By.TAG_NAME, "input")
        searchBar.send_keys(friendName)
        searchBar.send_keys(Keys.RETURN)

        # getting true name of contact/group
        threadName = driver.find_element_by_xpath('//*[@id="main"]/header//span[contains(text(), {})]'.format(friendName))

        # sending multiple msgs to friendName
        print("Sending msgs to: ", threadName.text)
        while True:
            msg = input().strip()
            if msg == 'fuckoffnow' or msg == 'stopit':
                print("\t Press Enter to end.")
                break
            sendMsg(driver, msg)

    # open all contacts page
    # driver.find_element(By.TAG_NAME, "button").click()


def sendMsg(driver, msg):
    '''
    Type 'msg' in 'driver' and press RETURN
    '''
    action = ActionChains(driver)
    action.send_keys(msg)
    action.send_keys(Keys.RETURN)
    action.perform()


if __name__ == '__main__':
    main()
    input()
