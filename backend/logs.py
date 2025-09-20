import json
import os
from datetime import datetime
from hashing import create_hash_chain_entry, verify_hash_chain

LOGS_FILE = '../logs/logs.json'

def initialize_logs():
    """Initialize logs file if it doesn't exist"""
    try:
        if not os.path.exists(LOGS_FILE):
            os.makedirs(os.path.dirname(LOGS_FILE), exist_ok=True)
            
            # Create initial log entry
            initial_log = {
                "id": 1,
                "event": "system_init",
                "user": "system",
                "exam_id": None,
                "timestamp": datetime.now().isoformat(),
                "details": "EduSecure system initialized",
                "prev_hash": "0000",
                "hash": ""
            }
            
            # Calculate hash for initial entry
            data_for_hash = {
                'id': initial_log['id'],
                'event': initial_log['event'],
                'user': initial_log['user'],
                'exam_id': initial_log['exam_id'],
                'timestamp': initial_log['timestamp'],
                'details': initial_log['details']
            }
            
            initial_log['hash'] = create_hash_chain_entry(initial_log['prev_hash'], data_for_hash)
            
            with open(LOGS_FILE, 'w') as f:
                json.dump([initial_log], f, indent=2)
            
            return True
        
        return True
        
    except Exception as e:
        print(f"Error initializing logs: {e}")
        return False

def append_log(event, user, exam_id, details=""):
    """Append a new log entry to the tamper-proof log chain"""
    try:
        # Ensure logs file exists
        initialize_logs()
        
        # Load existing logs
        with open(LOGS_FILE, 'r') as f:
            logs = json.load(f)
        
        # Get the last log entry for chaining
        last_log = logs[-1] if logs else None
        prev_hash = last_log['hash'] if last_log else "0000"
        new_id = (last_log['id'] + 1) if last_log else 1
        
        # Create new log entry
        new_log = {
            "id": new_id,
            "event": event,
            "user": user,
            "exam_id": exam_id,
            "timestamp": datetime.now().isoformat(),
            "details": details,
            "prev_hash": prev_hash,
            "hash": ""
        }
        
        # Calculate hash for new entry
        data_for_hash = {
            'id': new_log['id'],
            'event': new_log['event'],
            'user': new_log['user'],
            'exam_id': new_log['exam_id'],
            'timestamp': new_log['timestamp'],
            'details': new_log['details']
        }
        
        new_log['hash'] = create_hash_chain_entry(prev_hash, data_for_hash)
        
        # Append to logs
        logs.append(new_log)
        
        # Save updated logs
        with open(LOGS_FILE, 'w') as f:
            json.dump(logs, f, indent=2)
        
        return True, new_log
        
    except Exception as e:
        print(f"Error appending log: {e}")
        return False, None

def get_logs(limit=None, event_filter=None, user_filter=None, exam_filter=None):
    """Get logs with optional filtering"""
    try:
        if not os.path.exists(LOGS_FILE):
            return []
        
        with open(LOGS_FILE, 'r') as f:
            logs = json.load(f)
        
        # Apply filters
        filtered_logs = logs
        
        if event_filter:
            filtered_logs = [log for log in filtered_logs if log['event'] == event_filter]
        
        if user_filter:
            filtered_logs = [log for log in filtered_logs if log['user'] == user_filter]
        
        if exam_filter:
            filtered_logs = [log for log in filtered_logs if log['exam_id'] == exam_filter]
        
        # Apply limit
        if limit:
            filtered_logs = filtered_logs[-limit:]  # Get most recent entries
        
        return filtered_logs
        
    except Exception as e:
        print(f"Error getting logs: {e}")
        return []

def verify_log_chain(logs=None):
    """Verify the integrity of the log chain"""
    try:
        if logs is None:
            if not os.path.exists(LOGS_FILE):
                return True  # Empty log is valid
            
            with open(LOGS_FILE, 'r') as f:
                logs = json.load(f)
        
        return verify_hash_chain(logs)
        
    except Exception as e:
        print(f"Error verifying log chain: {e}")
        return False

def get_log_statistics():
    """Get statistics about the logs"""
    try:
        if not os.path.exists(LOGS_FILE):
            return {
                'total_entries': 0,
                'events': {},
                'users': {},
                'chain_valid': True
            }
        
        with open(LOGS_FILE, 'r') as f:
            logs = json.load(f)
        
        # Count events
        events = {}
        users = {}
        
        for log in logs:
            event = log['event']
            user = log['user']
            
            events[event] = events.get(event, 0) + 1
            users[user] = users.get(user, 0) + 1
        
        # Verify chain integrity
        chain_valid = verify_log_chain(logs)
        
        return {
            'total_entries': len(logs),
            'events': events,
            'users': users,
            'chain_valid': chain_valid,
            'first_entry': logs[0]['timestamp'] if logs else None,
            'last_entry': logs[-1]['timestamp'] if logs else None
        }
        
    except Exception as e:
        print(f"Error getting log statistics: {e}")
        return {'error': str(e)}

def get_exam_logs(exam_id):
    """Get all logs related to a specific exam"""
    try:
        return get_logs(exam_filter=exam_id)
        
    except Exception as e:
        print(f"Error getting exam logs: {e}")
        return []

def get_user_logs(username, limit=50):
    """Get logs for a specific user"""
    try:
        return get_logs(limit=limit, user_filter=username)
        
    except Exception as e:
        print(f"Error getting user logs: {e}")
        return []

def detect_tampering():
    """Detect if logs have been tampered with"""
    try:
        if not os.path.exists(LOGS_FILE):
            return False, "No logs file found"
        
        with open(LOGS_FILE, 'r') as f:
            logs = json.load(f)
        
        chain_valid = verify_log_chain(logs)
        
        if not chain_valid:
            return True, "Log chain integrity compromised - tampering detected"
        
        return False, "Log chain integrity verified - no tampering detected"
        
    except Exception as e:
        return True, f"Error detecting tampering: {e}"

def export_logs(output_file, format='json'):
    """Export logs to a file"""
    try:
        if not os.path.exists(LOGS_FILE):
            return False, "No logs to export"
        
        with open(LOGS_FILE, 'r') as f:
            logs = json.load(f)
        
        if format.lower() == 'json':
            with open(output_file, 'w') as f:
                json.dump(logs, f, indent=2)
        
        elif format.lower() == 'csv':
            import csv
            with open(output_file, 'w', newline='') as f:
                if logs:
                    writer = csv.DictWriter(f, fieldnames=logs[0].keys())
                    writer.writeheader()
                    writer.writerows(logs)
        
        else:
            return False, "Unsupported format. Use 'json' or 'csv'"
        
        return True, f"Logs exported to {output_file}"
        
    except Exception as e:
        return False, f"Error exporting logs: {e}"

# Initialize logs when module is imported
initialize_logs()