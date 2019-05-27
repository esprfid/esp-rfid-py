from machine import Pin
#import uasyncio as asyncio
import utime
import logging
log = logging.getLogger("relay")
import events

RELAY_OPEN_DURATION = 1
# TODO: Use config and support multiple relays

pin = Pin(13, Pin.OUT)

@events.on('card.card_validated')
def on_card_validated(card):
	log.info("Opening relay for %d seconds", RELAY_OPEN_DURATION)
	pin.on()
	utime.sleep(RELAY_OPEN_DURATION)
	pin.off()
	# TODO: Use fast_io to turn off relay
	#asyncio.get_event_loop().call_later(RELAY_OPEN_DURATION, lambda: pin.off())
