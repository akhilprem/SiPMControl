# Copied from http://stackoverflow.com/a/1925836

class Event(object):
    pass

class SCDObservable(object):
    def __init__(self):
        self.callbacks = []
        
    def subscribe(self, callback):
        self.callbacks.append(callback)
        
    def fire(self, **attrs):
        e = Event()
        e.source = self

        for k, v in attrs.iteritems():
            setattr(e, k, v)
        for fn in self.callbacks:
            fn(e)
