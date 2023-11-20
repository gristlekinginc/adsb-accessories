import json

# Define the Time Period for Analysis
TIME_PERIOD_MINUTES = 15  # Change this value to alter the time period

# Read and parse the JSON data
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Filter Aircraft based on defined time period
def filter_data_by_time(data):
    recent_aircraft = []
    for aircraft in data['aircraft']:
        if 'seen' in aircraft and aircraft['seen'] <= TIME_PERIOD_MINUTES * 60:
            recent_aircraft.append(aircraft)
    return recent_aircraft

# Identify Unique Aircraft and Calculate Ranges
def find_unique_aircraft_and_ranges(aircraft_list):
    unique_hex_codes = set()
    ranges = []
    for aircraft in aircraft_list:
        if 'hex' in aircraft:
            unique_hex_codes.add(aircraft['hex'])
            if 'r_dst' in aircraft:
                ranges.append(aircraft['r_dst'])
    return unique_hex_codes, ranges

# Calculate Maximum and Average Range
def calculate_range_stats(ranges):
    if not ranges:
        return 0, 0
    ranges_nautical_miles = [r * 0.539957 for r in ranges]
    max_range = max(ranges_nautical_miles)
    avg_range = sum(ranges_nautical_miles) / len(ranges_nautical_miles)
    return max_range, avg_range

# Main Function
def main():
    file_path = '/run/readsb/aircraft.json'  # Updated file path
    data = read_json_file(file_path)

    # Filter data for the specified time period
    recent_aircraft = filter_data_by_time(data)

    # Find unique aircraft and ranges
    unique_aircraft, ranges = find_unique_aircraft_and_ranges(recent_aircraft)

    # Calculate maximum and average range
    max_range, avg_range = calculate_range_stats(ranges)

    print(f"Unique aircraft in the last {TIME_PERIOD_MINUTES} minutes: {len(unique_aircraft)}")
    print(f"Maximum range seen: {max_range:.1f} nautical miles")
    print(f"Average range seen: {avg_range:.1f} nautical miles")

if __name__ == "__main__":
    main()
