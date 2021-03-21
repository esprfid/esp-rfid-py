## Manage cards database

Examples of management by REPL:

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
