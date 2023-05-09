# sitealert

Checks if the given URL does not return the 4xx or 5xx status.

## Usage

Tested on Python 3.11.

Install requirements
```bash
pip install -r requirements.txt
```

Run the script
```bash
python sitealert.py -u https://example.com -w https://your.webhook.url/here
```

Currently only Discord webhooks are supported.
