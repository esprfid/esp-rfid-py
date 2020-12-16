import uasyncio as asyncio
import logging
log = logging.getLogger("mqtt_client")
import events
import ujson
import gc
from uos import statvfs
import utime
import mqtt_as

import config as config_all
config = config_all.modules['mqtt_client']

async def main(client):
	while True:
		try:
			await asyncio.sleep(5)
			await client.connect()
			break
		except OSError:
			log.warning("MQTT connection failed.")

	while True:
		await asyncio.sleep(5)
		log.debug("Sending heartbeat")
		fs = statvfs('/')
		# If conectivity is down the following will pause for the duration.
		await client.publish(
			config['topics_prefix'] + 'log/heartbeat',
			ujson.dumps({
				"storage_free": fs[0] * fs[3],
				"mem_free": gc.mem_free(),
				"time": utime.time()
			}),
			qos = 0
		)

async def conn_han(client):
	await client.subscribe(config['topics_prefix'] + 'open', 1)

def callback(topic, msg, retained):
	topic = topic.decode()
	log.debug("Received message: topic: %s, body: %s, retained: %s", topic, msg, retained)

	if topic == config['topics_prefix'] + 'open':
		events.fire('card.card_validated', { 'mqtt_msg': msg })


mqtt_as.LINUX = True # So it will not try to manage WiFi
mqtt_as.MQTTClient.DEBUG = True  # Optional: print diagnostic messages
client = mqtt_as.MQTTClient(**config['connection'], subs_cb=callback, connect_coro=conn_han)
loop = asyncio.get_event_loop()
try:
	loop.run_until_complete(main(client))
finally:
	client.close()  # Prevent LmacRxBlk:1 errors