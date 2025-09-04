from datetime import datetime, timedelta
import json
import os

def check_release_time(scheduled_time_str):
    """Check if it's time to release the chaos key"""
    try:
        scheduled_time = datetime.fromisoformat(scheduled_time_str)
        current_time = datetime.now()
        
        # Allow release if current time is at or after scheduled time
        return current_time >= scheduled_time
        
    except Exception as e:
        print(f"Error checking release time: {e}")
        return False

def schedule_release(exam_id, scheduled_time_str, upload_folder):
    """Schedule key release for an exam"""
    try:
        exam_dir = os.path.join(upload_folder, exam_id)
        metadata_path = os.path.join(exam_dir, 'metadata.json')
        
        if not os.path.exists(metadata_path):
            return False, "Exam not found"
        
        # Validate scheduled time format
        try:
            scheduled_time = datetime.fromisoformat(scheduled_time_str)
        except ValueError:
            return False, "Invalid time format"
        
        # Check if scheduled time is in the future
        if scheduled_time <= datetime.now():
            return False, "Scheduled time must be in the future"
        
        # Update metadata
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        metadata['scheduled_time'] = scheduled_time_str
        metadata['schedule_updated'] = datetime.now().isoformat()
        
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return True, "Release scheduled successfully"
        
    except Exception as e:
        return False, f"Error scheduling release: {e}"

def get_time_until_release(scheduled_time_str):
    """Get time remaining until release"""
    try:
        scheduled_time = datetime.fromisoformat(scheduled_time_str)
        current_time = datetime.now()
        
        if current_time >= scheduled_time:
            return {
                'ready': True,
                'time_remaining': 0,
                'message': 'Ready for release'
            }
        
        time_diff = scheduled_time - current_time
        
        return {
            'ready': False,
            'time_remaining': time_diff.total_seconds(),
            'time_remaining_str': str(time_diff),
            'scheduled_time': scheduled_time_str,
            'current_time': current_time.isoformat(),
            'message': f'Release in {time_diff}'
        }
        
    except Exception as e:
        return {
            'ready': False,
            'error': f"Error calculating time until release: {e}"
        }

def is_exam_active(exam_id, upload_folder, duration_hours=3):
    """Check if exam is currently active (within exam duration)"""
    try:
        exam_dir = os.path.join(upload_folder, exam_id)
        metadata_path = os.path.join(exam_dir, 'metadata.json')
        
        if not os.path.exists(metadata_path):
            return False, "Exam not found"
        
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        scheduled_time_str = metadata.get('scheduled_time')
        if not scheduled_time_str:
            return False, "No scheduled time found"
        
        scheduled_time = datetime.fromisoformat(scheduled_time_str)
        current_time = datetime.now()
        exam_end_time = scheduled_time + timedelta(hours=duration_hours)
        
        # Exam is active if current time is between scheduled time and end time
        is_active = scheduled_time <= current_time <= exam_end_time
        
        return is_active, {
            'scheduled_time': scheduled_time_str,
            'exam_end_time': exam_end_time.isoformat(),
            'current_time': current_time.isoformat(),
            'is_active': is_active,
            'time_remaining': (exam_end_time - current_time).total_seconds() if is_active else 0
        }
        
    except Exception as e:
        return False, f"Error checking exam status: {e}"

def get_exam_schedule_info(exam_id, upload_folder):
    """Get comprehensive schedule information for an exam"""
    try:
        exam_dir = os.path.join(upload_folder, exam_id)
        metadata_path = os.path.join(exam_dir, 'metadata.json')
        
        if not os.path.exists(metadata_path):
            return None
        
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        scheduled_time_str = metadata.get('scheduled_time')
        key_released = metadata.get('key_released', False)
        release_time = metadata.get('release_time')
        
        if not scheduled_time_str:
            return None
        
        scheduled_time = datetime.fromisoformat(scheduled_time_str)
        current_time = datetime.now()
        
        # Calculate various time states
        time_until_release = get_time_until_release(scheduled_time_str)
        is_active, exam_status = is_exam_active(exam_id, upload_folder)
        
        return {
            'exam_id': exam_id,
            'scheduled_time': scheduled_time_str,
            'current_time': current_time.isoformat(),
            'key_released': key_released,
            'release_time': release_time,
            'can_release': time_until_release['ready'],
            'time_until_release': time_until_release,
            'exam_active': is_active,
            'exam_status': exam_status if isinstance(exam_status, dict) else {}
        }
        
    except Exception as e:
        print(f"Error getting exam schedule info: {e}")
        return None

def validate_schedule_time(scheduled_time_str, min_advance_minutes=30):
    """Validate that scheduled time is reasonable"""
    try:
        scheduled_time = datetime.fromisoformat(scheduled_time_str)
        current_time = datetime.now()
        min_advance_time = current_time + timedelta(minutes=min_advance_minutes)
        
        if scheduled_time <= current_time:
            return False, "Scheduled time must be in the future"
        
        if scheduled_time < min_advance_time:
            return False, f"Scheduled time must be at least {min_advance_minutes} minutes in advance"
        
        # Check if scheduled time is too far in the future (e.g., more than 1 year)
        max_advance_time = current_time + timedelta(days=365)
        if scheduled_time > max_advance_time:
            return False, "Scheduled time cannot be more than 1 year in advance"
        
        return True, "Valid schedule time"
        
    except ValueError:
        return False, "Invalid time format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"
    except Exception as e:
        return False, f"Error validating schedule time: {e}"

def get_all_scheduled_exams(upload_folder):
    """Get schedule information for all exams"""
    try:
        scheduled_exams = []
        
        if not os.path.exists(upload_folder):
            return scheduled_exams
        
        for exam_folder in os.listdir(upload_folder):
            exam_path = os.path.join(upload_folder, exam_folder)
            if os.path.isdir(exam_path):
                schedule_info = get_exam_schedule_info(exam_folder, upload_folder)
                if schedule_info:
                    scheduled_exams.append(schedule_info)
        
        # Sort by scheduled time
        scheduled_exams.sort(key=lambda x: x['scheduled_time'])
        
        return scheduled_exams
        
    except Exception as e:
        print(f"Error getting all scheduled exams: {e}")
        return []