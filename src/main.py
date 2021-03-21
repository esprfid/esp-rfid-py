import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("main")

# WiFi
if 'wifi' in config.modules:
	log.debug('Start WiFiManager')
	from wifi_manager import WifiManager
	WifiManager.start_managing()

# Modules
log.debug('Import modules')
import cards
log.debug('Import module relay')
import relay
log.debug('Import module mqtt_client')
import mqtt_client

# Start event loop
log.debug('Start event loop')
import uasyncio as asyncio
loop = asyncio.get_event_loop()
loop.run_forever()
