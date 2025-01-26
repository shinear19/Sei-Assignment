from flask_pymongo import PyMongo
from datetime import datetime, timedelta

db = PyMongo()

class Trigger:
    def __init__(self, trigger_type, payload=None, interval=None, scheduled_time=None):
        self.trigger_type = trigger_type
        self.payload = payload
        self.interval = interval
        self.scheduled_time = scheduled_time
        self.creation_time = datetime.utcnow()

    def to_dict(self):
        return {
            'trigger_type': self.trigger_type,
            'payload': self.payload,
            'interval': self.interval,
            'scheduled_time': self.scheduled_time,
            'creation_time': self.creation_time
        }

class Event:
    def __init__(self, trigger_id, triggered_at, payload=None, event_type="manual"):
        self.trigger_id = trigger_id
        self.triggered_at = triggered_at
        self.payload = payload
        self.event_type = event_type
        self.expiry_time = triggered_at + timedelta(hours=48)

    def to_dict(self):
        return {
            'trigger_id': self.trigger_id,
            'triggered_at': self.triggered_at,
            'payload': self.payload,
            'event_type': self.event_type,
            'expiry_time': self.expiry_time
        }
