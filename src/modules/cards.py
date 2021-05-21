import logging
log = logging.getLogger("cards")

import ujson
import uasyncio as asyncio
import events
import cards_storage as storage

cards_fetching = False

import config
readers = config.modules['cards']['readers']

# Multiple cards readers not supported yet
if len(readers) > 1:
	raise NotImplementedError

# Only wiegand reader is supported supported yet
if readers[0]['type'] != 'wiegand.py':
	raise NotImplementedError


def on_card(card_number, facility_code, cards_read):
	log.info("Card UID: %s", "{0:b} {0}".format(reader.last_card))

	if not reader.last_card:
		log.error("Card UID not valid.")
		return

	if isinstance(cards_fetching, list):
		cards_fetching.append(reader.last_card)
		return

	card = storage.get(reader.last_card)
	if not card:
		log.error("Card not known.")
		events.fire('card.card_not_known', reader.last_card)
		return
	log.info("Card found.")
	if 'd' in card and card['d']:
		log.error("Card is disabled.")
		return
	events.fire('card.card_validated', card)


from wiegand import Wiegand
reader = Wiegand(readers[0]['pin_d1'], readers[0]['pin_d0'], on_card)
# TODO: Use config and support multiple readers


# For fetching multiple cards at once.
# Will flash status LED when reading to indicate active fetching.
async def fetch_cards(callback, metadata, timeout = 10):
	from machine import Pin
	led = Pin(config.status_led['pin'], Pin.OUT, value=config.status_led['invert'])

	global cards_fetching
	cards_fetching = []

	# LED blinking
	for _ in range(timeout * 4):
		led.value(1 if led.value() == 0 else 0)
		await asyncio.sleep(0.25)

	callback(cards_fetching, metadata)
	cards_fetching = False
