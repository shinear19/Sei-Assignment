from flask import Blueprint, request, jsonify
from app.models import db, Trigger, Event
from datetime import datetime

trigger_blueprint = Blueprint('trigger', __name__)

# Create a new trigger
@trigger_blueprint.route('/triggers', methods=['POST'])
def create_trigger():
    data = request.json
    trigger_type = data.get("trigger_type")
    payload = data.get("payload")
    interval = data.get("interval")
    scheduled_time = data.get("scheduled_time")

    trigger = Trigger(trigger_type, payload, interval, scheduled_time)
    db.db.triggers.insert_one(trigger.to_dict())

    return jsonify({"message": "Trigger created successfully"}), 201

# List all triggers
@trigger_blueprint.route('/triggers', methods=['GET'])
def get_triggers():
    triggers = list(db.db.triggers.find())
    return jsonify(triggers), 200

# Test trigger (manual)
@trigger_blueprint.route('/test_trigger', methods=['POST'])
def test_trigger():
    trigger_id = request.json.get("trigger_id")
    trigger = db.db.triggers.find_one({"_id": trigger_id})
    event = Event(trigger_id=trigger['_id'], triggered_at=datetime.utcnow(), event_type="manual")
    db.db.events.insert_one(event.to_dict())
    
    return jsonify({"message": "Trigger fired successfully for testing"}), 200
