import json
from datetime import datetime, timedelta

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def calculate_average_period(aircraft_data, target_flights=100):
    # Current time based on the "now" field in the JSON data
    current_time = datetime.fromtimestamp(aircraft_data['now'])

    # Filter aircraft with at least 2 messages
    filtered_aircraft = [ac for ac in aircraft_data['aircraft'] if ac.get('messages', 0) >= 2]

    # Sort by the 'seen' time (most recently seen first)
    filtered_aircraft.sort(key=lambda x: x['seen'])

    total_period = timedelta(0)
    count = 0

    for ac in filtered_aircraft:
        if count >= target_flights:
            break
        # Calculate the time when the aircraft was last seen
        last_seen_time = current_time - timedelta(seconds=ac['seen'])
        total_period += (current_time - last_seen_time)
        count += 1

    # Calculate average period in minutes
    if count > 0:
        average_period = total_period / count
        return average_period.total_seconds() / 60  # Convert to minutes
    else:
        return 0

def main():
    file_path = '/run/readsb/aircraft.json'
    aircraft_data = read_json_file(file_path)
    avg_period = calculate_average_period(aircraft_data)
    print(f"Average time period for receiving at least 2 messages from 100 unique flights: {avg_period} minutes")

if __name__ == "__main__":
    main()

