## Controll doors

### MQTT

Topic: `my_prefix/open`
Message can be any object, will be passed to access log.


## Manage cards database

### REPL

```
import cards_storage
cards_storage.save(int('1011011000001000110000100', 2), {'n': 'John Appleseed'})
cards_storage.save(int('1001110001101001100110100', 2), {'n': 'Veronika Ruzickova'})
```

```
import cards_imexport
cards_imexport.export_to_json('cards.json')
cards_imexport.import_from_json('cards.json')
```

### MQTT

Topic: `my_prefix/cards/fetch`
Reader will blink and read cards for 10 seconds. Then it will send to `my_prefix/cards/fetch/return` list of fetched cards:
```
[
  32126761,
  16372945,
  24780733
]
```

Topic: `my_prefix/cards/set`
Message:
```
{"uid": 16372945, "card": {"name": "Veronika Růžičková"}}
```

Topic: `my_prefix/cards/get`
Message:
```
{"uid": 16372945}
```
Will send reply to topic: `my_prefix/cards/get/return`
Message:
```
{"card": {"name": "Veronika Růžičková"}}
```

### HTTP API

Get all cards UIDs:
GET `/cards/list`

Get single card by UID:
GET `/cards/single?uid=123456`

Get uptime, storage and memory stats:
GET `/stats`

Get config.py:
GET `/config`

Get networks.json:
GET `/config/networks`
