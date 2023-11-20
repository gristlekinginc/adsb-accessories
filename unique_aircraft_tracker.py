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
    # Convert ranges to nautical miles
    ranges_nautical_miles = [r * 0.539957 for r in ranges]
    max_range = max(ranges_nautical_miles)
    avg_range = sum(ranges_nautical_miles) / len(ranges_nautical_miles)
    return max_range, avg_range

# Main Function
def main():
    file_path = '/run/readsb/aircraft.json'  # Updated file path
    data = read_json_file(file_path)

    # Filter data for the last 15 minutes (or your desired period)
    recent_aircraft = filter_data_by_time(data, minutes=15)

    # Find unique aircraft and ranges
    unique_aircraft, ranges = find_unique_aircraft_and_ranges(recent_aircraft)

    # Calculate maximum and average range
    max_range, avg_range = calculate_range_stats(ranges)

    print(f"Unique aircraft in the last 15 minutes: {len(unique_aircraft)}")
    print(f"Maximum range seen: {max_range:.1f} nautical miles")
    print(f"Average range seen: {avg_range:.1f} nautical miles")

if __name__ == "__main__":
    main()
