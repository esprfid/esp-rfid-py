import uasyncio as asyncio
import logging
log = logging.getLogger("mqtt_client")
import cards
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
	await client.subscribe(config['topics_prefix'] + 'cards/+', 1)

def callback(topic, msg, retained):
	topic = topic.decode()
	try:
		msg = ujson.loads(msg)
	except ValueError:
		msg = {}
	log.debug("Received message: topic: %s, body: %s, retained: %s", topic, msg, retained)

	if topic == config['topics_prefix'] + 'open':
		events.fire('card.card_validated', msg)

	if topic == config['topics_prefix'] + 'cards/fetch':
		asyncio.get_event_loop().create_task(cards.fetch_cards(send_fetched_cards, msg))

	if topic == config['topics_prefix'] + 'cards/list':
		uids = [int.from_bytes(uid, "little") for uid in cards.storage.db]
		loop.create_task(client.publish(
			config['topics_prefix'] + 'cards/list/return',
			ujson.dumps({"cards": uids}),
			qos = 1
		))

	if topic == config['topics_prefix'] + 'cards/get':
		loop.create_task(client.publish(
			config['topics_prefix'] + 'cards/get/return',
			ujson.dumps({"card": cards.storage.get(msg['uid'])}),
			qos = 1
		))

	if topic == config['topics_prefix'] + 'cards/set':
		cards.storage.set(msg['uid'], msg['card'])


def send_fetched_cards(cards, metadata):
	metadata['cards'] = cards
	loop.create_task(client.publish(
		config['topics_prefix'] + 'cards/fetch/return',
		ujson.dumps(metadata),
		qos = 1
	))


@events.on('card.card_validated')
def send_access_log(data):
	loop.create_task(client.publish(
		config['topics_prefix'] + 'log/access',
		ujson.dumps(data),
		qos = 0
	))

mqtt_as.LINUX = True # So it will not try to manage WiFi
mqtt_as.MQTTClient.DEBUG = True  # Print diagnostic messages
client = mqtt_as.MQTTClient(**config['connection'], subs_cb=callback, connect_coro=conn_han)

loop = asyncio.get_event_loop()
try:
	loop.create_task(main(client))
finally:
	client.close()  # Prevent LmacRxBlk:1 errors
