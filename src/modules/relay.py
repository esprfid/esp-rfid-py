from machine import Pin
import uasyncio as asyncio
loop = asyncio.get_event_loop()
import utime
import logging
log = logging.getLogger("relay")
import events


# Load config and initiate pins
import config
relays = config.modules['relay']['relays']
for r in relays:
	r.update({
		'pin_obj': Pin(r['pin'], Pin.OUT)
	})


@events.on('card.card_validated')
def on_card_validated(card):
	for config in relays:
		loop.create_task(relay_task(config, card))
	# TODO: Solve delay before relay_task is actally started.


async def relay_task(config, card):
	if 'open_after' in config:
		log.info("Will open relay on pin %d in %d seconds", config['pin'], config['open_after'])
		await asyncio.sleep(config['open_after'])

	log.info("Opening relay on pin %d for %d seconds", config['pin'], config['close_after'])
	config['pin_obj'].on()
	await asyncio.sleep(config['close_after'])
	config['pin_obj'].off()
