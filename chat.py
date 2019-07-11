#! /usr/bin/python3

### Created by Chirag Khatri
### github.com/zvovov
### updated by Ismael Viejo

import sched
import sys
import threading
import time
import os
from operator import itemgetter

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException as WebDriverException

config = {
    #'chromedriver_path': "{0}/bin/chromedriver".format(os.environ['HOME']),
    #'chromedriver_path': "{0}/whatsapp-web/chromedriver.exe".format(os.environ['UserProfile']),
    'chromedriver_path': "{0}/whatsapp-web/chromedriver.exe".format(os.getcwd()),
    #'chromedriver_path': "D:/iviejo/Documents/Personal/whatsapp-web/chromedriver.exe".format(os.environ['UserProfile']),
    'get_msg_interval': 5,  # Time (seconds). Recommended value: 5
    'colors': True,  # True/False. True prints colorful msgs in console
    'ww_url': "https://web.whatsapp.com/"
}

incoming_scheduler = sched.scheduler(time.time, time.sleep)
last_printed_msg = None
last_thread_name = ''
last_get_msg_allchats = time.localtime()
last_printed_allchat_msg=None

# colors in console
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
        print('Folder: %s' %config['chromedriver_path'])
        
        if len(sys.argv) > 1:
            # Use a data directory so that we can persist cookies per session and not have to
            # authorize this application every time.
            # NOTE: This gets created in your home directory and can get quite large over time.
            # To fix this, simply delete this directory and re-authorize your WhatsApp Web session.
            chrome_data_dir_directory = "{0}/.chrome/data_dir/whatsapp_web_cli".format(os.environ['UserProfile'])
            if not os.path.exists(chrome_data_dir_directory):
                os.makedirs(chrome_data_dir_directory)

            driver_options = webdriver.ChromeOptions()
            driver_options.add_argument("user-data-dir={0}".format(chrome_data_dir_directory))


            
            
            #Open in background
            if sys.argv[1]=='-b':
                print('Activated Background mode')
                background=True
                driver_options.add_argument("--headless")
                #driver_options.add_argument("headless")
                driver_options.add_argument("--disable-gpu") 
            else:
                background=False


            # setting up Chrome with selenium
            driver = webdriver.Chrome(config['chromedriver_path'], chrome_options=driver_options)

            # minimize
            if not background:
                driver.minimize_window()


            # open WW in browser
            driver.get(config['ww_url'])

            # prompt user to connect device to WW
            print(decorateMsg("\n\tBe sure that the phone is connected. ", bcolors.HEADER))
            # while True:
                # isConnected = input(decorateMsg("\n\tPhone connected? y/n: ", bcolors.HEADER))
                # if isConnected.lower() == 'y':
                    # break
                # else:
                    # sys.exit(decorateMsg("\nError: Please, connect and execute again the command", bcolors.FAIL))
                    
            # Add a time to wait to be sure that everything is loaded
            print(decorateMsg('\n\tOpening session, wait a little bit.', bcolors.HEADER))
            time.sleep(15)
            
            assert "WhatsApp" in driver.title

            #PRINT HELP
            print(decorateMsg('\n\t HELP:\n\t\t-To change use: sendto <Name>\n\t\t-To only hear use: stopsending \n\t\t-To exit use: exit', bcolors.HEADER))

            # Starting
            if background:
                receiver=' '.join(sys.argv[2:])
            else:
                receiver=' '.join(sys.argv[1:])
            #print('Connecting to user %s' %receiver)
            chooseReceiver(driver,receiver=receiver)
            status='sendto'

            # getting true name of contact/group
            last_thread_name = driver.find_element(By.XPATH, '//*[@id="main"]/header//span[contains(@dir, "auto")]').text
            # print('last_thread_name=%s' %last_thread_name)
                        
            ##
            # IV
            time.sleep(10)
            # unread=get_print_last_messages(driver)
            unread_nchats, unread_nmsgs, data=get_msg_allchats(driver)
            # print(data)
            print_last_messages(data)
            ###   
            
            ###
            
            # start background thread
            incoming_thread = threading.Thread(target=startGetMsg, args=(driver,))
            incoming_thread.start()

            # Loop to find 
            while True:
                if status != 'sendto':
                    #print('asking message outside')
                    msg = input().strip()
                    #status=run_send(driver, receiver=receiver)
                else:
                    msg='sendto %s' %receiver
                if len(msg) > 7 and 'sendto ' in msg[:7]:
                    status='sendto'
                    status=run_send(driver, receiver=msg[7:])
                    #print('%s' %status)
                else:
                    status=msg
                if status == 'stopsending':
                    print(decorateMsg("\tYou will only receive msgs now.\n\tPress Ctrl+C to exit or sendto <name> to activate again.", bcolors.WARNING))
                    # TODO: stop the incoming_scheduler event
                    #break
                elif status == 'exit':
                    print('Starting closing')
                    incoming_thread.join(timeout=15.0)
                    #time.sleep(15)
                    print("Thread is: %s" %(incoming_thread.isAlive()))
                    driver.quit()
                    print("Thread is: %s" %(incoming_thread.isAlive()))
                    incoming_thread.kill = True
                    print("Thread is: %s" %(incoming_thread.isAlive()))
                    print('Closing - Clic Ctr+C')
                    time.sleep(5)
                    sys.exit(decorateMsg("\nClosing program ...", bcolors.FAIL))
                # else:
                    # sendMsg(driver, msg)
                
        else:
            sys.exit(decorateMsg("\nError: Missing name of contact/group\npython chat.py <name>", bcolors.FAIL))

        # open all contacts page
        # driver.find_element(By.TAG_NAME, "button").click()


    def sendMsg(driver, msg):
        '''
        Type 'msg' in 'driver' and press RETURN
        '''
        # select correct input box to type msg
        input_box = driver.find_element(By.XPATH, '//*[@id="main"]//footer//div[contains(@contenteditable, "true")]')
        # input_box.clear()
        input_box.click()

        action = ActionChains(driver)
        action.send_keys(msg)
        action.send_keys(Keys.RETURN)
        action.perform()


    def startGetMsg(driver):
        '''
        Start schdeuler that gets incoming msgs every get_msg_interval seconds
        '''
        incoming_scheduler.enter(config['get_msg_interval'], 1, getMsg, (driver, incoming_scheduler))
        incoming_scheduler.run()


    def getMsg(driver, scheduler):
        '''
        Get incoming msgs from the driver repeatedly
        Updated iviejo@gmail
        '''
        #print('inside getMsg')
        global last_printed_msg
        global last_get_msg_allchats
        
        # # Different minute
        # if int(time.strftime("%M", time.localtime()))-int(time.strftime("%M",last_get_msg_allchats))>0:
            # unread_nchats, unread_nmsgs, data=get_msg_allchats(driver)
            # #
            # print_last_messages(data)
        unread_nchats, unread_nmsgs, data=get_msg_allchats(driver)
        print_last_messages(data)
            
        
        # print conversation name
        curr_thread_name = printThreadName(driver)

        try:
            # get all msgs
            all_msgs = driver.find_elements(By.XPATH, '//*[@id="main"]//div[contains(@class, "message")]')

            # print('There is %i' %len(all_msgs))
            # check if there is atleast one message in the chat
            if len(all_msgs) >= 1:
                last_msg_outgoing = outgoingMsgCheck(all_msgs[-1])
                last_msg_sender, last_msg_text = getMsgMetaInfo(all_msgs[-1])
                #
                msgs_present = True
            else:
                msgs_present = False
            # print('%s' %msgs_present)
        except Exception as e:
            print(e)
            msgs_present = False
        
      
        if msgs_present:
            # if last msg was incoming
            if not last_msg_outgoing:
                # if last_msg is already printed
                if last_printed_msg == last_msg_sender + last_msg_text:
                    pass
                # else print new msgs
                else:
                    # print('There is %i ingoing' %len(all_msgs))
                    print_from = 0
                    # loop from last msg to first
                    for i, curr_msg in reversed(list(enumerate(all_msgs))):
                        curr_msg_outgoing = outgoingMsgCheck(curr_msg)
                        curr_msg_sender, curr_msg_text = getMsgMetaInfo(curr_msg)

                        # if curr_msg is outgoing OR if last_printed_msg is found
                        if curr_msg_outgoing or last_printed_msg == curr_msg_sender + curr_msg_text:
                            # break
                            print_from = i
                            break
                    # Print all msgs from last printed msg till newest msg
                    for i in range(print_from + 1, len(all_msgs)):
                        msg_sender, msg_text = getMsgMetaInfo(all_msgs[i])
                        last_printed_msg = msg_sender + msg_text
                        print(decorateMsg(msg_sender + msg_text, bcolors.OKGREEN))

        # add the task to the scheduler again
        incoming_scheduler.enter(config['get_msg_interval'], 1, getMsg, (driver, scheduler,))


    def outgoingMsgCheck(webdriver_element):
        '''
        Returns True if the selenium webdriver_element has "message-out" in its class.
        False, otherwise.
        '''
        for _class in webdriver_element.get_attribute('class').split():
            if _class == "message-out":
                return True
        return False

    def ingoingMsgCheck(webdriver_element):
        '''
        Returns True if the selenium webdriver_element has "message-out" in its class.
        False, otherwise.
        '''
        for _class in webdriver_element.get_attribute('class').split():
            if _class == "message-in":
                return True
        return False

    def getMsgMetaInfo(webdriver_element):
        '''
        Returns webdriver_element's sender and message text.
        Message Text is a blank string, if it is a non-text message
        TODO: Identify msg type and print accordingly
        '''
        # check for non-text message
        try:
            msg = webdriver_element.find_element(By.XPATH, './/div[contains(@class, "copyable-text")]')
            msg_sender = msg.get_attribute('data-pre-plain-text')
            msg_text = msg.find_elements(By.XPATH, './/span[contains(@class, "selectable-text")]')[-1].text
        except IndexError:
            msg_text = ""
        except Exception:
            msg_sender = ""
            msg_text = ""

        return msg_sender, msg_text


    def decorateMsg(msg, color=None):
        '''
        Returns:
                colored msg, if colors are enabled in config and a color is provided for msg
                msg, otherwise
        '''
        msg_string = msg
        if config['colors']:
            if color:
                msg_string = color + msg + bcolors.ENDC

        return msg_string


    def printThreadName(driver):
        global last_thread_name
        curr_thread_name = driver.find_element(By.XPATH, '//*[@id="main"]/header//span[contains(@dir, "auto")]').text
        if curr_thread_name != last_thread_name:
            last_thread_name = curr_thread_name
            print(decorateMsg("\n\tSending msgs to:", bcolors.OKBLUE), curr_thread_name)
        return curr_thread_name


    def chooseReceiver(driver, receiver=None):
        # search name of friend/group
        friend_name = receiver if receiver else ' '.join(sys.argv[1:])
        input_box = driver.find_element(By.XPATH, '//*[@id="side"]//input')
        input_box.clear()
        input_box.click()
        input_box.send_keys(friend_name)
        input_box.send_keys(Keys.RETURN)
        printThreadName(driver)

        
    #### IV functions
    def run_send(driver, receiver=None):
        '''
        Function to control sending
        '''
        # print('In function')
        init=True
        msg='sendto %s' %receiver
        while True:
            if not init:
                #print('asking message in function')
                msg = input().strip()
            else:
                init=False
            if len(msg) > 7 and 'sendto ' in msg[:7]:
                #print('inside function sendto')
                chooseReceiver(driver, receiver=msg[7:])
            elif msg == 'stopsending':
                #print(decorateMsg("\tYou will only receive msgs now.\n\tPress Ctrl+C to exit or sendto <name> to activate again.", bcolors.WARNING))
                # TODO: stop the incoming_scheduler event
                #break
                return 'stopsending'
            elif msg == 'exit':
                return 'exit'
            else:
                sendMsg(driver, msg)
        #print('End function')

    def get_print_last_messages(driver):
        '''
        Obtain last messages from driver
        and print
        by: iviejo@gmail.com
        '''
        
        ###
        # IV: getting the unread chats
        unread_names = driver.find_elements_by_css_selector('span.OUeyt')
        if len(unread_names)>0:
            unread=True
            print('Total unread chats: %s' %len(unread_names))
            j=0
            for i,unread_name in enumerate(unread_names):
                try:
                    j+=int(unread_name.text)
                except:
                    j+=1
                # print('Number of unread messages: %s' %(unread_name.text))
            print('Number of unread messages: %s' %(j))
        else:
            unread=False
        
        # Obtain number of messages (WORK)
        tmp_chats = driver.find_elements_by_class_name('_3j7s9')
        for i,chat_info in enumerate(tmp_chats):
            info=chat_info.text.split('\n')
            if len(info)==5:
                mesg_print=('%s messages unread - Last messages in group %s at %s from %s: %s' %(info[4],info[0],info[1],info[2],info[3][:20]))
            elif len(info)==4:
                try:
                    unread_msg=int(info[3])
                    mesg_print=('%s messages unread - Last messages from %s at %s: %s' %(info[3],info[0],info[1],info[2][:20]))
                except:
                    mesg_print=('Last messages in group %s at %s from %s: %s' %(info[0],info[1],info[2],info[3][:20]))
            elif len(info)==3:
                mesg_print=('Last messages from %s at %s: %s' %(info[0],info[1],info[2][:20]))
            elif len(info)==2:
                mesg_print=('Last messages from %s at %s' %(info[0],info[1]))
            else:
                mesg_print=('Unrecognize data %s' %info)
                
            print(decorateMsg(mesg_print, bcolors.OKGREEN))
            
        
        return unread
        
    def get_msg_allchats(driver):
        '''
        Obtain last messages from driver
        and save to a structure
        by: iviejo@gmail.com
        '''
        ###
        global last_get_msg_allchats
        ###
        # IV: getting the unread chats
        unread_names = driver.find_elements_by_css_selector('span.OUeyt')
        if len(unread_names)>0:
            unread=True
            unread_nchats=len(unread_names)
            unread_nmsgs=0
            for i,unread_name in enumerate(unread_names):
                try:
                    unread_nmsgs+=int(unread_name.text)
                except:
                    unread_nmsgs+=1
        else:
            unread_nchats=0
            unread_nmsgs=0
        
        # Obtain the chat and corresponding last message
        #print('Previous find')
        tmp_chats = driver.find_elements_by_class_name('_3j7s9')
        #print('then find')
        data=[]
        '''
        Save data in a list with follow structure
        [group, person, %Y%m%d%H%M, message, unread, n_unread]
        '''
        for i,chat_info in enumerate(tmp_chats):
            info=chat_info.text.split('\n')
            if len(info)==5:
                # Save in data structure
                data.append([])
                data[-1].append(info[0]) #group
                data[-1].append(info[2]) #person
                data[-1].append(convert_string_time(info[1])) #date_time
                data[-1].append(info[3]) #message
                data[-1].append(True) #unread
                data[-1].append(info[4]) #n_unread
                #mesg_print=('%s messages unread - Last messages in group %s at %s from %s: %s' %(info[4],info[0],info[1],info[2],info[3][:20]))
            elif len(info)==4:
                try:
                    a=int(info[3])
                    # Save in data structure
                    data.append([])
                    data[-1].append(None) #group
                    data[-1].append(info[0]) #person
                    data[-1].append(convert_string_time(info[1])) #date_time
                    data[-1].append(info[2]) #message
                    data[-1].append(True) #unread
                    data[-1].append(info[3]) #n_unread
                    #mesg_print=('%s messages unread - Last messages from %s at %s: %s' %(info[3],info[0],info[1],info[2][:20]))
                except:
                    # Save in data structure
                    data.append([])
                    data[-1].append(info[0]) #group
                    data[-1].append(info[2]) #person
                    data[-1].append(convert_string_time(info[1])) #date_time
                    data[-1].append(info[3]) #message
                    data[-1].append(False) #unread
                    data[-1].append("") #n_unread
                    # mesg_print=('Last messages in group %s at %s from %s: %s' %(info[0],info[1],info[2],info[3][:20]))
            elif len(info)==3:
                # Save in data structure
                data.append([])
                data[-1].append(None) #group
                data[-1].append(info[0]) #person
                data[-1].append(convert_string_time(info[1])) #date_time
                data[-1].append(info[2]) #message
                data[-1].append(False) #unread
                data[-1].append("") #n_unread
                mesg_print=('Last messages from %s at %s: %s' %(info[0],info[1],info[2][:20]))
            elif len(info)==2:
                mesg_print=('Last messages from %s at %s' %(info[0],info[1]))
                # Save in data structure
                data.append([])
                data[-1].append(None) #group
                data[-1].append(info[0]) #person
                data[-1].append(convert_string_time(info[1])) #date_time
                data[-1].append("") #message
                data[-1].append(False) #unread
                data[-1].append("") #n_unread
            else:
                mesg_print=('Unrecognize data in last messages: %s' %info)
                
            # print(decorateMsg(mesg_print, bcolors.OKGREEN))
            
        
        last_get_msg_allchats = time.localtime()
        
        return unread_nchats, unread_nmsgs, data


    def print_last_messages(data):
        '''
        given the data with messages print all of them
        data in a list with follow structure
        [group, person, %Y%m%d%H%M, message, unread, n_unread]
        by: iviejo@gmail.com
        '''
        ###
        global last_printed_allchat_msg
        global last_thread_name
        ###
        today=time.strftime("%Y%m%d", time.localtime())
        yesterday=time.strftime("%Y%m%d", time.localtime(time.mktime(time.localtime())-86400))
        #
        # Sort data
        tmp=sorted(data, key=itemgetter(2))
        #
        # Print
        # for i,case in enumerate(tmp):
            # print(case)

        # Check if print or not
        if last_printed_allchat_msg is None:
            idx_print=[True]*len(tmp)
            print(decorateMsg('\n\nPRINTING ALL OLD CHATS:\n', bcolors.OKBLUE))
        else:
            idx_print=[not k in last_printed_allchat_msg for k in tmp]
            # No print activated chat
            # Check if group or personal chat
            idx=[k for k,case in enumerate(tmp) if (last_thread_name==case[0] or (case[0]==None and last_thread_name==case[1]))]
            if len(idx)==1:
                idx_print[idx[0]]=False
            # Print header
            if sum(idx_print)>=1:
                print(decorateMsg('\n\nNEW MESSAGES:', bcolors.OKBLUE))


        
        for i,case in enumerate(tmp):
            if idx_print[i]:
                #time
                day=case[2][:8]
                hour=case[2][8:10]
                min=case[2][10:]
                #
                #
                msg_print=''
                if case[4]:
                    #unread
                    msg_print+=decorateMsg('%s messages unread - ' %case[5], bcolors.WARNING)
                msg_print+=decorateMsg('Last messages from ', bcolors.OKBLUE)
                if case[0] is not None:
                    #group
                    msg_print+=decorateMsg(' %s by ' %case[0], bcolors.OKGREEN)
                #person
                msg_print+=decorateMsg(' %s ' %case[1], bcolors.OKGREEN)
                #
                if day==today:
                    msg_print+=decorateMsg(' Today at %s:%s ' %(hour,min), bcolors.OKBLUE)
                elif day==yesterday:
                    msg_print+=decorateMsg(' Yesterday: ', bcolors.OKBLUE)
                else:
                    msg_print+=decorateMsg(' in %s: ' %day, bcolors.OKBLUE)
                #message
                msg_print+='%s' %(case[3])
                # msg_print+='%s' %(case[3][:30])
            
                #print
                print(msg_print)
        if sum(idx_print)>=1:
            print(decorateMsg("\n\tSending msgs to:", bcolors.OKBLUE), last_thread_name)
            print(decorateMsg('\tTo change use: sendto <Name>\n', bcolors.HEADER))
        # Save last message
        last_printed_allchat_msg=tmp
            

    def convert_string_time(tmp):
        '''
        Given a time write in format of driver convert to %Y%m%d%H%M
        by: iviejo@gmail
        '''
        # Convert time
        if len(tmp.split(':'))==2:
            #date_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            day=time.strftime("%Y%m%d", time.localtime())
            hour='%s%s' %(tmp.split(':')[0],tmp.split(':')[1])
            date_time=day+hour
        elif len(tmp.split('/'))==3:
            day='%s%s%s' %(tmp.split('/')[2],tmp.split('/')[1],tmp.split('/')[0])
            hour='0000'
            date_time=day+hour
        else:
            day=time.strftime("%Y%m%d", time.localtime(time.mktime(time.localtime())-86400))
            hour='0000'
            date_time=day+hour
            
        return date_time
    #####################################
        
        
        
        
    if __name__ == '__main__':
        main()

        
except AssertionError as e:
    sys.exit(decorateMsg("\n\tCannot open Whatsapp web URL.", bcolors.WARNING))

except KeyboardInterrupt as e:
    sys.exit(decorateMsg("\n\tPress Ctrl+C again to exit.", bcolors.WARNING))

except WebDriverException as e:
    sys.exit(print(e, decorateMsg("\n\tChromedriver Error. Read the above error (if any), then\n\tCheck if installed chromedriver version is compatible with installed Chrome version.", bcolors.WARNING)))
