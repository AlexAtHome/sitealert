import requests
from requests.exceptions import HTTPError
import sys

def main():
	if len(sys.argv) != 2:
		raise ValueError('Please provide the URL!')
	url = sys.argv[1]
	print(f'Checking the url {url}')
	response = requests.head(url)
	try:
		response.raise_for_status()
	except HTTPError as http_error:
		print(f'HTTP error occurred:\n{http_error}')
	except Exception as err:
		print(f'Other exception occurred:\n{err}')
	else:
		print(f'{url} returns {response.status_code}')

main()
