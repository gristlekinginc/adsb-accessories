# Import necessary libraries
import json

# Read and parse the JSON data
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Define the Time Period for Analysis and Filter Aircraft
def filter_data_by_time(data, minutes=15):
    recent_aircraft = []
    for aircraft in data['aircraft']:
        if 'seen' in aircraft and aircraft['seen'] <= minutes * 60:
            recent_aircraft.append(aircraft)
    return recent_aircraft

# Identify Unique Aircraft
def find_unique_aircraft(aircraft_list):
    unique_hex_codes = set()
    for aircraft in aircraft_list:
        if 'hex' in aircraft:
            unique_hex_codes.add(aircraft['hex'])
    return unique_hex_codes

# Main Function
def main():
    file_path = '/run/readsb/aircraft.json'  # Updated file path
    data = read_json_file(file_path)

    # Filter data for the last 15 minutes (or your desired period)
    recent_aircraft = filter_data_by_time(data, minutes=15)

    # Find unique aircraft
    unique_aircraft = find_unique_aircraft(recent_aircraft)
    print(f"Unique aircraft in the last 15 minutes: {len(unique_aircraft)}")
    # print(unique_aircraft)

if __name__ == "__main__":
    main()

