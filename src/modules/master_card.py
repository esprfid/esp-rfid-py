import uasyncio as asyncio
import logging
log = logging.getLogger("master_card")
import events

adding_mode = False

@events.on('card.card_validated')
def on_card_validated(card):
	if 'master' in card and card['master']:
		log.info('Master card, waiting for card to add...')

		asyncio.get_event_loop().create_task(adding_mode_in_progress())

@events.on('card.card_not_known')
def on_card_not_known(uid):
	if adding_mode:
		import cards_storage
		if not cards_storage.get(uid):
			cards_storage.save(uid, {'n': 'Added by master as {}. card.'.format(sum(1 for e in cards_storage.db) + 1)})
			log.info('Card added.')


async def adding_mode_in_progress():
	from machine import Pin
	led = Pin(15, Pin.OUT) # TODO: Use config

	global adding_mode
	adding_mode = True

	for _ in range(40): # TODO: Use config
		led.value(1 if led.value() == 0 else 0)
		await asyncio.sleep(0.25)

	adding_mode = False
