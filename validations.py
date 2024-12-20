from datetime import datetime

# Validate datetime format
def is_valid_datetime(dt_str):
    try:
        datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")  # Example format: 2024-12-20 14:30:00
        return True
    except ValueError:
        return False

# Validate status
def is_valid_status(status):
    return status in ['pending', 'in_progress', 'completed', 'archived']

# Validate priority
def is_valid_priority(priority):
    return priority in ['low', 'medium', 'high']