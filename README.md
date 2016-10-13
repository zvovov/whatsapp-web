# whatsapp-web
Yo! Use WhatsApp from the command line. No :phone: required.

Chat everywhere you couldn't before... like at your desk. Hah  :frog:

You can only send messages. So unless you can talk to yourself, technically, it won't be a conversation.


## Requirements

- [selenium](http://selenium-python.readthedocs.io/installation.html) Tested with 2.53.6
- [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) Tested with 2.24

## Installation

1.  Clone this repository `git clone https://github.com/zvovov/whatsapp-web.git`  
2.  `pip install selenium`
3.  Download and extract [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads).zip
4.  Put path to ChromeDriver binary in the line `driver = webdriver.Chrome('/path/to/chromedriver')` in `chat.py` file of this repository.  

## Usage

1.  `python chat.py <name>`
  
    Replace `<name>` with the name of a contact or a group in your WhatsApp. Even partial names will work.
2.  Scan the QR code displayed on screen from the WhatsApp mobile app.
3.  Press `y` in console after WhatsApp Web is done loading.
4.  Chat. Chat. Chat.

#### Disclaimer

Not affiliated with WhatsApp.
