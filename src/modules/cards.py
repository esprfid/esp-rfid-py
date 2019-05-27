import logging
log = logging.getLogger("cards")

import ujson
import uasyncio as asyncio
import events
import cards_storage as storage
import config

def on_card(card_number, facility_code, cards_read):
	log.info("Card UID: %s", reader.last_card)

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
reader = Wiegand(5, 4, on_card)
# TODO: Use config and support multiple readers
