import ujson
import cards_storage

# Example JSON file:
#
# {
#   "47669875": { "n": "John Appleseed" },
#   "6088984": { "n": "Veronika Ruzickova", "d": true }
# }

def export_to_json(filename):
	data = { int.from_bytes(uid, "little"): ujson.loads(cards_storage.db[uid]) for uid in cards_storage.db }
	with open(filename, 'w') as f:
		f.write(ujson.dumps(data))

def import_from_json(filename):
	with open(filename, 'r') as f:
		data = ujson.load(f)
	for suid in data:
		cards_storage.set(int(suid), data[suid], flush=False)
	cards_storage.db.flush()
