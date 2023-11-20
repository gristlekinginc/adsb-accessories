import json
from datetime import datetime, timedelta

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def calculate_average_period(aircraft_data, target_flights=100):
    current_time = datetime.fromtimestamp(aircraft_data['now'])
    aircraft_list = aircraft_data['aircraft']

    # Diagnostic information
    total_aircraft = len(aircraft_list)
    unique_aircraft = len(set(ac['hex'] for ac in aircraft_list if 'hex' in ac))
    min_seen = min(aircraft_list, key=lambda x: x.get('seen', float('inf')))['seen']
    max_seen = max(aircraft_list, key=lambda x: x.get('seen', float('-inf')))['seen']

    # Time period calculation
    earliest_time = current_time - timedelta(seconds=max_seen) if max_seen is not None else None
    time_period_length_minutes = (current_time - earliest_time).total_seconds() / 60 if earliest_time else 0

    filtered_aircraft = [ac for ac in aircraft_list if ac.get('messages', 0) >= 2]
    total_period = timedelta(0)
    count = 0

    for ac in filtered_aircraft:
        if count >= target_flights:
            break
        last_seen_time = current_time - timedelta(seconds=ac['seen'])
        total_period += (current_time - last_seen_time)
        count += 1

    if count > 0:
        average_period = total_period / count
        average_period_minutes = average_period.total_seconds() / 60
    else:
        average_period_minutes = 0

    # Print diagnostic information
    print(f"Total aircraft processed: {total_aircraft}")
    print(f"Time period: {earliest_time.strftime('%Y-%m-%d %H:%M:%S')} to {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Length of time period: {time_period_length_minutes:.3f} minutes")
    print(f"Number of unique aircraft: {unique_aircraft}")
    print(f"Minimum 'seen' value: {min_seen} seconds")
    print(f"Maximum 'seen' value: {max_seen} seconds")
    print(f"Average time period for receiving at least 2 messages from 100 unique flights: {average_period_minutes:.1f} minutes")

def main():
    file_path = '/run/readsb/aircraft.json'
    aircraft_data = read_json_file(file_path)
    calculate_average_period(aircraft_data)

if __name__ == "__main__":
    main()
