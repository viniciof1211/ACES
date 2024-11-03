import json
from datetime import datetime

# Define the initial streak data
streak_data = {
    "streak": 0,
    "last_practice": datetime.now().isoformat()
}

# Save to 'streak_data.json'
output_path = 'streak_data.json'
with open(output_path, 'w') as f:
    json.dump(streak_data, f)

output_path
