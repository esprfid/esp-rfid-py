AIRTABLE_BASE = 'https://api.airtable.com/v0/'
AIRTABLE_KEY = ''
AIRTABLE_DEVICE_NAME = ''
AIRTABLE_DEVICE_ID = ''
AIRTABLE_FIELDS_SYNC = ['Open-close']
# TODO: Use config

import events
import logging
log = logging.getLogger("airtable")
import uasyncio as asyncio

def login():
	global AIRTABLE_DEVICE_ID
	r = request('GET', '/Devices?filterByFormula=Name%3D%27{}%27&fields[]=Name'.format(AIRTABLE_DEVICE_NAME))
	if r['records']:
		AIRTABLE_DEVICE_ID = r['records'][0]['id']
	else:
		r = request('POST', '/Devices', json={"fields": {"Name": AIRTABLE_DEVICE_NAME}})
		AIRTABLE_DEVICE_ID = r['id']
	log.info("Logged in as %s", AIRTABLE_DEVICE_ID)

asyncio.get_event_loop().call_soon(login)

@events.on('card.card_not_known')
def log_unknown_card(uid):
	record = {"fields": {
		"UID": str(uid),
		"Name": "Unknown tag",
		"Enabled": False,
		"Devices": [
			AIRTABLE_DEVICE_ID
		]
	}}
	log.debug("Adding unknown card.")
	request('POST', '/Tags', json=record)

def sync_cards(offset=None):
	import cards_storage

	filter = 'AND%28NOT%28UID%3D%27%27%29%2C%28FIND%28%27{}%27%2CDevices%29%29%3E%200%29'.format(AIRTABLE_DEVICE_NAME)
	params = 'filterByFormula={}&fields%5B%5D=UID&fields%5B%5D=Enabled&pageSize=3'.format(filter)
	if offset:
		params += '&offset=' + offset
	cards = request('GET', '/Tags?' + params)
	print(cards)

	for card in cards['records']:
		if 'Enabled' in card['fields']:
			cards_storage.save(card['fields']['UID'], {}) # TODO: Support configurable fields
		else:
			cards_storage.save(card['fields']['UID'], False)

	if 'offset' in cards:
		asyncio.get_event_loop().call_later(2, sync_cards, cards['offset'])

asyncio.get_event_loop().call_soon(sync_cards)

def request(method, query, json=None):
	global airtable_socket
	import uurequests
	r = uurequests.request(method, AIRTABLE_BASE + query, json=json, stream=airtable_socket, headers={"Authorization": "Bearer " + AIRTABLE_KEY})
	data = r.json()
	if r.status_code != 200:
		log.error("Request: %s %s, status code: %s, data: %s", method, query, r.status_code, data)
	airtable_socket = r.raw

	import gc
	gc.collect()

	return data

airtable_socket = False
