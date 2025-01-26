from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from bson.objectid import ObjectId
import threading
import time

app = Flask(__name__)

# Enable CORS for frontend at http://localhost:5173 only
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

# MongoDB connection URI
app.config["MONGO_URI"] = "mongodb+srv://rohit960211:Rohit@cluster0.qfbl9nq.mongodb.net/test?retryWrites=true&w=majority"
client = MongoClient(app.config["MONGO_URI"], serverSelectionTimeoutMS=5000)
db = client.get_database()

# Test MongoDB connection
try:
    client.admin.command('ping')
    print("✅ MongoDB connection successful!")
except ServerSelectionTimeoutError:
    print("❌ MongoDB connection failed. Please check your URI and database status.")

# Helper functions

def log_event(trigger_id, trigger_type, payload=None, is_test=False):
    events_collection = db.events
    event = {
        "trigger_id": trigger_id,
        "trigger_type": trigger_type,
        "payload": payload,
        "is_test": is_test,
        "status": "active",
        "triggered_at": datetime.utcnow(),
    }
    events_collection.insert_one(event)

def archive_and_cleanup_events():
    while True:
        now = datetime.utcnow()
        events_collection = db.events

        # Archive events older than 2 hours
        events_collection.update_many(
            {"status": "active", "triggered_at": {"$lte": now - timedelta(hours=2)}},
            {"$set": {"status": "archived"}},
        )

        # Delete events older than 48 hours
        events_collection.delete_many({"triggered_at": {"$lte": now - timedelta(hours=48)}})

        time.sleep(3600)  # Run every hour

def execute_trigger(trigger_id, trigger_type, payload, is_test=False):
    """
    Executes the actual trigger functionality and logs the event.
    """
    try:
        # Log the event as triggered
        log_event(trigger_id, trigger_type, payload, is_test)
        print(f"✅ Trigger {trigger_id} executed successfully (type: {trigger_type}).")
    except Exception as e:
        print(f"❌ Error executing trigger {trigger_id}: {e}")

def schedule_trigger(trigger_id, delay, payload):
    """
    Handles scheduled trigger execution after a delay.
    """
    try:
        print(f"⏳ Scheduled trigger {trigger_id} will execute after {delay} seconds.")
        time.sleep(delay)
        execute_trigger(trigger_id, "scheduled", payload)
    except Exception as e:
        print(f"❌ Error in scheduled trigger {trigger_id}: {e}")

# API Endpoints

@app.route("/api/triggers", methods=["POST"])
def create_trigger_route():
    data = request.json
    trigger_type = data.get("type")
    time_info = data.get("time")
    payload = data.get("payload", {})

    if trigger_type not in ["scheduled", "api"]:
        return jsonify({"message": "Invalid trigger type."}), 400

    # Validate time info for scheduled triggers
    if trigger_type == "scheduled":
        delay = time_info.get("delay")
        if delay is None or not isinstance(delay, int) or delay <= 0:
            return jsonify({"message": "Invalid or missing delay for scheduled trigger."}), 400

    trigger = {
        "type": trigger_type,
        "time": time_info,
        "payload": payload,
        "created_at": datetime.utcnow(),
    }

    trigger_id = str(db.triggers.insert_one(trigger).inserted_id)

    if trigger_type == "scheduled":
        # Start a thread to handle the scheduled trigger
        threading.Thread(
            target=schedule_trigger, args=(trigger_id, delay, payload), daemon=True
        ).start()

    return jsonify({"message": "Trigger created", "trigger_id": trigger_id}), 201

@app.route("/api/triggers", methods=["GET"])
def fetch_triggers():
    triggers = list(db.triggers.find())
    return jsonify([
        {
            "trigger_id": str(trigger["_id"]),
            "type": trigger["type"],
            "time": trigger["time"],
            "payload": trigger.get("payload", {}),
        }
        for trigger in triggers
    ])

@app.route("/api/triggers/<trigger_id>", methods=["DELETE"])
def delete_trigger(trigger_id):
    result = db.triggers.delete_one({"_id": ObjectId(trigger_id)})
    if result.deleted_count == 0:
        return jsonify({"message": "Trigger not found."}), 404

    return jsonify({"message": "Trigger deleted."}), 200

@app.route("/api/events", methods=["GET"])
def fetch_events():
    status_filter = request.args.get("status", "active")
    events = list(db.events.find({"status": status_filter}))
    return jsonify([
        {
            "event_id": str(event["_id"]),
            "trigger_id": str(event["trigger_id"]),
            "trigger_type": event["trigger_type"],
            "payload": event.get("payload"),
            "is_test": event["is_test"],
            "status": event["status"],
            "triggered_at": event["triggered_at"].isoformat(),
        }
        for event in events
    ])

@app.route("/api/test-trigger", methods=["POST"])
def test_trigger():
    """
    Manually tests a trigger by executing it after a specified delay or immediately.
    """
    data = request.json
    trigger_id = data.get("trigger_id")
    payload = data.get("payload", {})

    if not trigger_id:
        return jsonify({"message": "trigger_id is required."}), 400

    # Fetch the trigger type from the database (optional for validation)
    trigger = db.triggers.find_one({"_id": ObjectId(trigger_id)})
    if not trigger:
        return jsonify({"message": "Trigger not found."}), 404

    trigger_type = trigger["type"]

    # For testing, we use an immediate thread execution (simulate a delay of 10 seconds if needed)
    delay = data.get("delay", 10)  # Default delay for test-trigger is 10 seconds
    threading.Thread(
        target=schedule_trigger, args=(trigger_id, delay, payload), daemon=True
    ).start()

    return jsonify({"message": f"Test trigger {trigger_id} initiated. It will execute after {delay} seconds."}), 200

# Start background thread for archiving and cleanup
threading.Thread(target=archive_and_cleanup_events, daemon=True).start()

# Start the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
