import gc
from uos import statvfs
import utime
import uasyncio as asyncio
from web import WebApp, jsonify
import cards_storage

webapp = WebApp()


@webapp.route('/', method='GET')
def index(request, response):
	gc.collect()
	yield from start_response(writer)
	yield from writer.awrite("""
		<!DOCTYPE html>
		<html lang="en">
		<head>
			<meta charset="UTF-8">
			<meta name="viewport" content="width=device-width, initial-scale=1.0">
			<title>ESP-RFID.py</title>
		</head>
		<body>
	""")
	yield from writer.awrite("""
		</body>
		</html>
	""")

@webapp.route('/cards/list', method='GET')
def get_tags(request, response):
	gc.collect()
	cards = [card for card in cards_storage.db]
	yield from jsonify(response, {"cards": cards})

@webapp.route('/cards/single', method='GET')
def get_tag(request, response):
	gc.collect()
	uid = request.parse_qs()['uid']
	yield from jsonify(response, {"card": cards_storage.get(uid)})

@webapp.route('/cards/single', method='POST')
def set_tag(request, response):
	pass

@webapp.route('/stats', method='GET')
def get_stats(request, response):
	fs = statvfs('/')
	yield from jsonify(response, {
		"storage_total": fs[0] * fs[2],
		"storage_free": fs[0] * fs[3],
		"mem_used": gc.mem_alloc(),
		"mem_free": gc.mem_free(),
		"time": utime.time()
	})

@webapp.route('/config', method='GET')
def get_config(request, response):
	yield from webapp.sendfile(response, '/config.py')

@webapp.route('/config', method='POST')
def set_config(request, response):
	pass

@webapp.route('/config/networks', method='GET')
def get_networks(request, response):
	yield from webapp.sendfile(response, '/networks.json')

@webapp.route('/config/networks', method='POST')
def set_networks(request, response):
	pass


loop = asyncio.get_event_loop()
loop.create_task(asyncio.start_server(webapp.handle, '0.0.0.0', 80))
