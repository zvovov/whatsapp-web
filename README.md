# whatsapp-web

Yo! Use WhatsApp from the command line.

Chat everywhere you couldn't before... like at your desk. Hah  :frog:

You can ~~only send messages~~. You can send and receive messages.

### Features

  - Send and receive messages to and from any contact/group in your WhatsApp *from command line*.
  - Switch between different chats *from command line*.
  - You can only send/receive text messages. Emoji, image, audio, video or anything else is not supported right now. Yeah, it sucks, I know. But.. but it's **command-line**. :neckbeard:

## Requirements

- Python 3
- [selenium](http://selenium-python.readthedocs.io/installation.html) Tested with 2.53.6
- [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) Tested with 2.24

## Installation

1.  Clone this repository. `$ git clone https://github.com/zvovov/whatsapp-web.git`  
2.  Install selenium. `$ pip install selenium`
3.  Download and extract [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads).zip
4.  Put path to ChromeDriver executable in the line `'chromedriver_path': '/path/to/chromedriver'` in `chat.py` file of this repository.  

## Usage

#### Start Chatting  

`$ python chat.py <name>`
  
1.  Replace `<name>` with the name of a contact or a group in your WhatsApp. Even partial names will work.
2.  Scan the QR code displayed on screen from the WhatsApp mobile app.
3.  Press `y` in console after WhatsApp Web is done loading.
4.  Chat. Chat. Chat.

#### Switch to another chat

`sendto <name>`

1.  Type it while `chat.py` is running.
1.  Replace `<name>` with the name of the contact/group you want to chat with now. Again, partial names will work.
2.  You can switch between chats as many times you want. Unread messages will be displayed to you every time.

#### Stop sending messages and only receive messages

`stopsending`

1.  Type it while `chat.py` is running.
1.  This will allow you to only see incoming messages. Your messages won't be sent. To send messages again, restart the script.

#### Configuration

```
config = {
    'chromedriver_path': '/path/to/chromedriver',
    'get_msg_interval': 5,  # Time (seconds). Recommended value: 5
    'colors': True,  # True/False. True prints colorful msgs in console
    ...
}
```

Parameter             | Use
`'chromedriver_path'` | Path to the chromedriver executable on your system
`'get_msg_interval'`  | *Time in seconds between each check for new incoming messages.* Eg. `'get_msg_interval': 5` would check the active chat for any new messages every `5` seconds.
`'colors'`            | *Boolean flag for coloured console output.* If you want colorful messages in console, different colors for incoming and outgoing messages, set this to `True`. Otherwise, if you're seeing weird symbols like `[92m`, `[0m` around each message, set this to `False`.

#### Exit

Press `Ctrl+C` two times.


### Disclaimer

Not affiliated with WhatsApp.
