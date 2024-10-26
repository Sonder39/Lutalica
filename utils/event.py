class Event:
    def __init__(self):
        self._listeners = []

    def registerListener(self, listener):
        self._listeners.append(listener)

    def trigger(self, *args, **kwargs):
        for listener in self._listeners:
            listener(*args, **kwargs)
