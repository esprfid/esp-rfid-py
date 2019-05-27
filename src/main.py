# Reverse import dir, so you can override frozen modules by local module.
import sys
sys.path.reverse()

# WiFi
from wifi_manager import WifiManager
WifiManager.start_managing()

# Modules
import cards
import master_card
import relay
#import airtable
# TODO: Autoloading

# Start event loop
import uasyncio as asyncio
asyncio.get_event_loop().run_forever()
