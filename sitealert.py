import requests
from requests import Response
from requests.exceptions import HTTPError
import sys
from discord_webhook import DiscordWebhook, DiscordEmbed
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

def get_http_error_embed(response: Response, error):
	embed = DiscordEmbed(title='HTTP Error occured!', description=f'```{error}```', color='ff0000')
	embed.add_embed_field(name="Status code", value=f"{response.status_code}", inline=True)
	embed.add_embed_field(name="Response time", value=f"{response.elapsed}", inline=True)
	embed.set_timestamp()
	return embed

def get_exception_embed(error: Exception):
	embed = DiscordEmbed(title='An error with sitealert occured!', description=error, color='cc9b20')
	embed.set_timestamp()
	return embed

def send_to_discord(embed: DiscordEmbed):
	webhook = DiscordWebhook(url=config['Discord']['webhook_url'])
	webhook.add_embed(embed)
	webhook.execute()


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
		send_to_discord(get_http_error_embed(response, http_error))
	except Exception as err:
		print(f'Other exception occurred:\n{err}')
		send_to_discord(get_exception_embed(err))
	else:
		print(f'{url} returns {response.status_code}')

main()
