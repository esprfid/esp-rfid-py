# Reverse import dir, so you can override frozen modules by local module.
import sys
sys.path.reverse()

# WiFi
from wifi_manager import WifiManager
WifiManager.start_managing()

# Modules
import cards
import relay
import master_card
#import airtable  # EXPERIMENTAL - Not tested well. Currently runs out of memory too often to be useable (because of HTTPS).

# Start event loop
import uasyncio as asyncio
asyncio.get_event_loop().run_forever()
