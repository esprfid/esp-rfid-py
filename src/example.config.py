# Config file for ESP-RFID.py

# Config for WiFi is in networks.json
# Config for WebREPL is in webrepl_cfg.py

# Lists modules and it's config what will be enabled. If you want to disable module, just comment it.
modules = {}

modules['cards'] = {
	'readers': [{
		'type': 'wiegand',
		'pin_d0': 4, # ESP-RFID Relay Board
		'pin_d1': 5
	}]
}

modules['relay'] = {
	'relays': [
		{
			'pin': 13, # ESP-RFID Relay Board
			'close_after': 1 # How long relay should be opened in seconds.
		},
		{
			'pin': 12,
			'open_after': 2, # Delay after second doors will be opened.
			'close_after': 0.5
		}
	]
}

# This module allows adding new tags by special "master card".
#
# This can be any card in a database, just to is's data `'master': true`, then
# this card will trigger adding mode.

modules['master_card'] = {
	'status_led': 15, # LED on this pin will blink in adding mode.
	'adding_mode_duration': 10 # How many seconds it will listen for cards to be added.
}

# Synchronize card database with an Airtable.com database.
#
# Your ESP-RFID boards can be managed by Artable UI, so you can comfortably manage
# cards database for many doors. You can name cards, so you always know what card
# to disable when needed. When unknown tag is used it will be appended to cards table
# in disabled state with timestamp, so you can easilly add new users (just fill Label
# and check Enabled).
#
# Your database have to have structure from this template:

# EXPERIMENTAL - Not tested well. Currently runs out of memory too often to be useable (because of HTTPS).

# SECURITY WARNING: ESP8266 can not verify HTTPS certificates, so communication with
# Airtable API is vulnerable to MITM attack which can lead to API keys disclosure.
# If you use Airtable module you have to use private WiFi and trust your ISP!

#modules['airtable'] = {
#	'base': 'https://api.airtable.com/v0/app123456789', # You can find it there: https://airtable.com/api
#	'key': 'key123456789', # API key, you can find there: https://airtable.com/account
#	'device_name': 'Klubovna', # After start will be added to Devices table.
#	'fields_sync': [ # What fields will be synchronized and how mapped to local database. UID will be always synced.
#		('Label': 'name'),
#		('Permanent open-close': 'permanent')
#	],
#	'empty_means_everywhere': true # Will sync tag even if Devices column is empty - user can go everywhere.
#}
