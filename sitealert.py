import requests
from requests import Response
from requests.exceptions import HTTPError
import sys, os
from discord_webhook import DiscordWebhook, DiscordEmbed
import configparser
from selenium import webdriver
from time import sleep

config = configparser.ConfigParser()
config.read("config.ini")
webhook_url = config['Webhook']['url']

screenshotFile = "screenshot.png"

options = webdriver.FirefoxOptions()
options.headless = True
driver = webdriver.Firefox(options=options)

def main():
	if len(sys.argv) != 2:
		raise ValueError("Please provide the URL to watch!")

	url = sys.argv[1]
	print(f"Checking the url {url}...")

	response = requests.head(url)

	try:
		response.raise_for_status()
	except HTTPError as http_error:
		print(f"An HTTP error occurred:\n{http_error}")
		send_webhook(url, get_http_error_message_body(response, http_error))
	except Exception as error:
		print(f"Other exception occurred:\n{error}")
		send_webhook(url, get_exception_message_body(error))
	else:
		print(f"{url} returns {response.status_code}")

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

def remove_screenshot():
	os.remove(screenshotFile)

def send_webhook(url: str, embed: DiscordEmbed):
	webhook = DiscordWebhook(url=webhook_url)

	driver.get(url)
	driver.get_screenshot_as_file(screenshotFile)
	with open(screenshotFile, "rb") as f:
		webhook.add_file(file=f.read(), filename=screenshotFile)
	embed.set_image(url=f"attachment://{screenshotFile}")

	# TODO: Send a simple HTTP request with the 'requests' module
	webhook.add_embed(embed)
	webhook.execute(remove_files=True)

	remove_screenshot()

	driver.quit()

main()
