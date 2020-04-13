import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("main")

# WiFi
log.debug('Start WiFiManager')
from wifi_manager import WifiManager
WifiManager.start_managing()

# Modules
log.debug('Import modules')
import cards
log.debug('Import module relay')
import relay
log.debug('Import module master')
import master_card
#import airtable  # EXPERIMENTAL - Not tested well. Currently runs out of memory too often to be useable (because of HTTPS).

# Start event loop
log.debug('Start event loop')
import uasyncio as asyncio
loop = asyncio.get_event_loop()
loop.run_forever()
