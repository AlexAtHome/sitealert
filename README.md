# sitealert

Checks if the given URL does not return the 4xx or 5xx status.

## Usage

Tested on Python 3.9.9.

Create file `config.ini` with the following content:
```ini
[Discord]
webhook_url="your_discord_webhook_url_here"
```

Install requirements
```bash
pip install -r requirements.txt
```

Run the script
```bash
python sitealert.py https://example.com
```
