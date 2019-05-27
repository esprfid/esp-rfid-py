# Inspired by event_emitter by leemin and pymitter by riga.

events_listeners = {}

def on(event_name, listener=None):
	def _on(listener):
		if event_name not in events_listeners:
			events_listeners[event_name] = []

		events_listeners[event_name].append(listener)

	# If func is not used then assume it is used as decorator
	if listener is None:
		return _on
	else:
		return _on(listener)

def off(event_name, listener):
	if event_name in events_listeners:
		events_listeners[event_name].remove(listener)

def fire(event_name, *args):
	listeners = events_listeners.get(event_name)

	return_values = []
	if listeners is not None:
		for listener in listeners:
			return_values.append(listener(*args))
	return return_values
