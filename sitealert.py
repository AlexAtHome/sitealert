import requests
from requests import Response
from requests.exceptions import HTTPError
from discord_webhook import DiscordWebhook, DiscordEmbed
from selenium import webdriver
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-u", "--url", help="URL to test", required=True)
parser.add_argument("-w", "--webhook", help="Webhook URL", required=True)

args = parser.parse_args()

def main():
	print(f"Checking the url {args.url}...")

	response = requests.head(args.url)

	try:
		response.raise_for_status()
	except HTTPError as http_error:
		print(f"An HTTP error occurred:\n{http_error}")
		send_webhook(get_http_error_message_body(response, http_error))
	except Exception as error:
		print(f"Other exception occurred:\n{error}")
		send_webhook(get_exception_message_body(error))
	else:
		print(f"{args.url} returns {response.status_code}")

def get_http_error_message_body(response: Response, error: HTTPError):
	# TODO: Form a plain object instead of a whole Discord related class
	embed = DiscordEmbed(title="HTTP Error occured!", description=f"```{error}```", color="f9e2af")
	embed.add_embed_field(name="Status code", value=f"{response.status_code}", inline=True)
	embed.add_embed_field(name="Response time", value=f"{response.elapsed}", inline=True)
	embed.set_timestamp()
	return embed

def get_exception_message_body(error: Exception):
	embed = DiscordEmbed(title="An error with sitealert occured!", description=error, color="f38ba8")
	embed.set_timestamp()
	return embed

def get_driver():
	try:
		options = webdriver.FirefoxOptions()
		options.headless = True
		return webdriver.Firefox(options=options)
	except Exception as e:
		raise RuntimeError('Unable to run geckodriver.', e)

def send_webhook(embed: DiscordEmbed):
	webhook = DiscordWebhook(url=args.webhook)
	driver = get_driver()

	driver.get(args.url)
	webhook.add_file(file=driver.get_screenshot_as_png(), filename='screenshot.png')
	embed.set_image(url="attachment://screenshot.png")

	# TODO: Send a simple HTTP request with the 'requests' module
	webhook.add_embed(embed)
	webhook.execute(remove_files=True)

	driver.quit()

main()
