# AGENTS.md

## Cursor Cloud specific instructions

### Overview

This is a single-file Python CLI tool (`chat.py`) that automates WhatsApp Web via Selenium + Chrome. It allows sending and receiving WhatsApp text messages from the terminal.

### Development Environment

- **Python**: 3.12 (system Python at `/usr/bin/python3`)
- **Virtual environment**: `/workspace/venv` (activate with `source venv/bin/activate`)
- **Key dependency**: `selenium` (installed in venv)
- **Chrome**: Pre-installed system-wide (`google-chrome`)
- **ChromeDriver**: Auto-managed by Selenium 4's built-in driver manager; also symlinked at `~/bin/chromedriver`

### Running the application

```bash
source venv/bin/activate
python chat.py <contact_name>
```

The script requires a live WhatsApp session (QR code scanning via mobile app), so fully interactive testing is not possible in headless CI environments.

### Testing without WhatsApp auth

To verify the environment works (Chrome + Selenium + ChromeDriver):

```bash
source venv/bin/activate
python3 -c "
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
opts = Options()
opts.add_argument('--headless')
opts.add_argument('--no-sandbox')
opts.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=opts)
driver.get('https://web.whatsapp.com/')
assert 'WhatsApp' in driver.title
driver.quit()
print('Environment OK')
"
```

### Important caveats

- The script uses the old Selenium 3 API for instantiating WebDriver (`webdriver.Chrome(path, options=...)`). Selenium 4 still supports this but emits deprecation warnings; the `Service` object is the modern approach.
- `chat.py` expects ChromeDriver at `$HOME/bin/chromedriver`. The update script symlinks the Selenium-managed driver there.
- There are no automated tests, no linter config, no `requirements.txt`, and no build step in this repository.
- The `--headless` flag is not configured in `chat.py` — it runs Chrome with a visible browser window. For headless testing, add that option programmatically.
- No lint or type-checking is configured for this project. You can run `python3 -m py_compile chat.py` for basic syntax validation.
