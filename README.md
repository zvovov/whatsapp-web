# whatsapp-web

Yo! Use WhatsApp from the command line.

Chat everywhere you couldn't before... like at your desk. Hah  :frog:

You can ~~only send messages~~. You can send and receive messages.

### Features

  - Send and receive messages to and from any contact/group in your WhatsApp *from command line*.
  - Switch between different chats *from command line*.
  - You can only send/receive text messages. Emoji, image, audio, video or anything else is not supported right now. Yeah, it sucks, I know. But.. but it's **command-line**. :neckbeard:


## Requirements

- Python 3.3+
- [selenium](http://selenium-python.readthedocs.io/installation.html) Tested with 2.53.6
- [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) Tested with 2.24


## Installation

1.  Clone this repository `git clone https://github.com/zvovov/whatsapp-web.git`  
2.  `pip install selenium`
3.  Download and extract [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads).zip
4.  Put path to ChromeDriver binary in the line `driver = webdriver.Chrome('/path/to/chromedriver')` in `chat.py` file of this repository.  

## Usage

#### Start Chatting

`python chat.py <name>`
  
    Replace `<name>` with the name of a contact or a group in your WhatsApp. Even partial names will work.
2.  Scan the QR code displayed on screen from the WhatsApp mobile app.
3.  Press `y` in console after WhatsApp Web is done loading.
4.  Chat. Chat. Chat.

#### Switch to another chat

`sendto <name>`

    Replace `<name>` with the name of the contact/group you want to chat with now. Again, partial names will work.
2.  You can switch between chats as many times you want. Unread messages will be displayed to you every time.

#### Stop sending messages and only receive messages

`stopsending`

    This will allow you to only see incoming messages. Your messages won't be sent. To send messages again, restart the script.

#### Exit

Press `Ctrl+C` two times. 


### Disclaimer

Not affiliated with WhatsApp.
