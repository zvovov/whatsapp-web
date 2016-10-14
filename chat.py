#! /usr/bin/python3

import sched
import sys
import threading
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# WW = Whatsapp Web = web.whatsapp.com
wwUrl = "https://web.whatsapp.com/"

# for incoming msgs
getMsgInterval = 5
incomingScheduler = sched.scheduler(time.time, time.sleep)


def main():
    if len(sys.argv) > 1:
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

        friendName = ' '.join(sys.argv[1:])
        searchBar = driver.find_element(By.TAG_NAME, "input")
        searchBar.send_keys(friendName)
        searchBar.send_keys(Keys.RETURN)

        # getting true name of contact/group
        threadName = driver.find_element_by_xpath('//*[@id="main"]/header//span[contains(text(), {})]'.format(friendName))

        # TODO: verify threadName after every 10 msgs or 30 seconds

        # sending multiple msgs to friendName
        print("\n\tSending msgs to:", threadName.text)

        # start background thread
        incomingThread = threading.Thread(target=startGetMsg, args=(driver,))
        incomingThread.start()

        while True:
            msg = input().strip()
            if msg == 'fuckoffnow' or msg == 'stopit':
                print("\t Press Enter to end.")
                # TODO: stop the incomingScheduler event
                break
            sendMsg(driver, msg)

    else:
        sys.exit("\nError: Missing name of contact/group\npython chat.py <name>")

    # open all contacts page
    # driver.find_element(By.TAG_NAME, "button").click()


def sendMsg(driver, msg):
    """
    Type 'msg' in 'driver' and press RETURN
    """
    action = ActionChains(driver)
    action.send_keys(msg)
    action.send_keys(Keys.RETURN)
    action.perform()


def startGetMsg(driver):
    """
    Start schdeuler that gets incoming msgs every getMsgInterval seconds
    """
    incomingScheduler.enter(getMsgInterval, 1, getMsg, (driver, incomingScheduler))
    incomingScheduler.run()


def getMsg(driver, scheduler):
    """
    Get incoming msgs from the driver repeatedly
    """
    # print("...")

    # get incoming msgs
    allMsgs = driver.find_element_by_xpath('//*[@id="main"]//div[contains(@class, "message-list")]')
    print(allMsgs.text)

    # add the task to the scheduler again
    incomingScheduler.enter(getMsgInterval, 1, getMsg, (driver, scheduler,))


if __name__ == '__main__':
    main()
    input()
