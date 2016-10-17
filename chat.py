#! /usr/bin/python3

import sched
import sys
import threading
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException as WebDriverException

# WW = Whatsapp Web = web.whatsapp.com
ww_url = "https://web.whatsapp.com/"

# for incoming msgs
get_msg_interval = 5
incoming_scheduler = sched.scheduler(time.time, time.sleep)

last_printed_msg_id = 0
last_thread_name = ''


# colors in terminal
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


try:
    def main():
        global last_thread_name

        if len(sys.argv) > 1:
            # setting up Chrome with selenium
            driver = webdriver.Chrome('/home/chirag/src/chromedriver/chromedriver')

            # open WW in browser
            driver.get(ww_url)

            # prompt user to connect device to WW
            while True:
                isConnected = input(bcolors.HEADER + "\n\tPhone connected? y/n: " + bcolors.ENDC)
                if isConnected.lower() == 'y':
                    break

            assert "WhatsApp" in driver.title

            chooseReceiver(driver)

            # getting true name of contact/group
            last_thread_name = driver.find_element(By.XPATH, '//*[@id="main"]/header//div[contains(@class, "chat-main")]').text

            # sending multiple msgs to friend_name
            print(bcolors.OKBLUE + "\n\tSending msgs to:", last_thread_name + bcolors.ENDC)

            # start background thread
            incoming_thread = threading.Thread(target=startGetMsg, args=(driver,))
            incoming_thread.start()

            while True:
                msg = input().strip()
                if len(msg) > 7 and 'sendto ' in msg[:7]:
                        chooseReceiver(driver, receiver=msg[7:])
                elif msg == 'stopsending':
                    print(bcolors.WARNING + "\tYou will only receive msgs now.\n\tPress Ctrl+C to exit." + bcolors.ENDC)
                    # TODO: stop the incoming_scheduler event
                    break
                else:
                    sendMsg(driver, msg)

        else:
            sys.exit(bcolors.FAIL + "\nError: Missing name of contact/group\npython chat.py <name>" + bcolors.ENDC)

        # open all contacts page
        # driver.find_element(By.TAG_NAME, "button").click()


    def sendMsg(driver, msg):
        """
        Type 'msg' in 'driver' and press RETURN
        """
        # select correct input box to type msg
        driver.find_element(By.XPATH, '//*[@id="main"]//footer//div[contains(@class, "input")]').click()

        action = ActionChains(driver)
        action.send_keys(msg)
        action.send_keys(Keys.RETURN)
        action.perform()


    def startGetMsg(driver):
        """
        Start schdeuler that gets incoming msgs every get_msg_interval seconds
        """
        incoming_scheduler.enter(get_msg_interval, 1, getMsg, (driver, incoming_scheduler))
        incoming_scheduler.run()


    def getMsg(driver, scheduler):
        """
        Get incoming msgs from the driver repeatedly
        """
        global last_printed_msg_id

        # print conversation name
        printThreadName(driver)

        # get incoming msgs
        all_msgs_text_only = driver.find_elements(By.XPATH, '//*[@id="main"]//div[contains(@class, "message-text")]')

        # check if last msg was outgoing.
        try:
            last_msg = all_msgs_text_only[-1]
            last_msg_id = last_msg.get_attribute('data-id')
        except IndexError:
            last_msg_id = None
        if last_msg_id:
            # if last msg was incoming
            if last_msg_id[:5] == 'false':
                # if last_msg is already printed
                if last_printed_msg_id == last_msg_id:
                    pass
                # else print new msgs
                else:
                    print_from = len(all_msgs_text_only)
                    # loop from last msg to first
                    for i, curr_msg in reversed(list(enumerate(all_msgs_text_only))):
                        # if curr_msg is outgoing OR if last_printed_msg_id is found
                        curr_msg_id = curr_msg.get_attribute('data-id')
                        if curr_msg_id[:4] == 'true' or curr_msg_id == last_printed_msg_id:
                            # break
                            print_from = i
                            break
                    # Print all msgs from last printed msg till newest msg
                    for i in range(print_from + 1, len(all_msgs_text_only)):
                        last_printed_msg_id = all_msgs_text_only[i].get_attribute('data-id')
                        print(bcolors.OKGREEN + all_msgs_text_only[i].text + bcolors.ENDC)

        # add the task to the scheduler again
        incoming_scheduler.enter(get_msg_interval, 1, getMsg, (driver, scheduler,))


    def printThreadName(driver):
        global last_thread_name
        curr_thread_name = driver.find_element(By.XPATH, '//*[@id="main"]/header//div[contains(@class, "chat-main")]').text
        if curr_thread_name != last_thread_name:
            last_thread_name = curr_thread_name
            print(bcolors.OKBLUE + "\n\tSending msgs to:", curr_thread_name + bcolors.ENDC)


    def chooseReceiver(driver, receiver=None):
        # search name of friend/group
        friend_name = receiver if receiver else ' '.join(sys.argv[1:])
        search_bar = driver.find_element(By.XPATH, '//*[@id="side"]//input')
        search_bar.send_keys(friend_name)
        search_bar.send_keys(Keys.RETURN)


    if __name__ == '__main__':
        main()

except (KeyboardInterrupt, WebDriverException):
    sys.exit(bcolors.WARNING + "\tBye!" + bcolors.ENDC)
