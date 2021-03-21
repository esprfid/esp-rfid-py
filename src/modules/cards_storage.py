import ujson

DB_FILE_NAME = "cards.db"

# Users schema:
# uid: {
# 	n: name
# 	d: disabled
# }
# One char keys reserved for core, modules should use longer keys to avoud collisions.


import btree
try:
	f = open(DB_FILE_NAME, "r+b")
except OSError:
	f = open(DB_FILE_NAME, "w+b")
db = btree.open(f)


def set(uid, data, flush=True):
	euid = encode_uid(uid)
	if data == False:
		if euid in db:
			del db[euid]
	elif type(data) is dict:
		db[euid] = ujson.dumps(data).encode()
	else:
		raise TypeError
	if flush:
		db.flush()


def get(uid):
	buid = encode_uid(uid)
	return ujson.loads(db[buid]) if buid in db else False


def encode_uid(uid):
	if type(uid) is int:
		return uid.to_bytes(5, "little") # 5 bytes - enough room for 34 bit UID
	else:
		return uid.encode()
