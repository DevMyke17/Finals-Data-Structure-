import json
import os
from collections import Counter

# --- Utility Functions for File Management ---

def create_dummy_json(filename):
    """
    Creates a sample JSON file containing car accident data.
    """
    # Sample data reflecting accidents
    data = [
        {'id': 1, 'car': 'Toyota Camry', 'location': 'Main St, Anytown', 'city': 'Anytown', 'date_time': '2024-10-25 08:30'},
        {'id': 2, 'car': 'Honda Civic', 'location': 'Highway 101', 'city': 'Springfield', 'date_time': '2024-10-25 15:45'},
        {'id': 3, 'car': 'Ford F-150', 'location': 'Industrial Park Blvd', 'city': 'Anytown', 'date_time': '2024-10-26 10:00'},
        {'id': 4, 'car': 'Toyota Camry', 'location': 'Downtown Loop', 'city': 'Metropolis', 'date_time': '2024-10-26 19:20'},
        {'id': 5, 'car': 'Tesla Model 3', 'location': 'Residential Zone A', 'city': 'Springfield', 'date_time': '2024-10-27 06:15'},
        {'id': 6, 'car': 'Honda Civic', 'location': 'Main St, Anytown', 'city': 'Anytown', 'date_time': '2024-10-27 12:00'},
        {'id': 7, 'car': 'Toyota Camry', 'location': 'Highway 101', 'city': 'Springfield', 'date_time': '2024-10-27 17:50'},
        {'id': 8, 'car': 'Ford F-150', 'location': 'Ocean View Drive', 'city': 'Anytown', 'date_time': '2024-10-28 14:00'},
    ]
    
    try:
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=4)
        print(f"Successfully created dummy accident data file: {filename}")
    except IOError as e:
        print(f"Error creating file: {e}")

# --- Data Analysis Functions ---

def search_accidents(data_list, search_key, search_value):
    """
    Finds accidents where a specific key (e.g., 'city', 'date_time') matches the value.
    
    :param data_list: The list of accident dictionaries.
    :param search_key: The field name to search within ('city', 'location', 'date_time', etc.).
    :param search_value: The value to match (case-insensitive for strings).
    :return: A list of dictionaries that match the search criteria.
    """
    results = []
    
    # We check if the search_key actually exists in the first record
    if not data_list or search_key not in data_list[0]:
        print(f"Error: Search key '{search_key}' not found in data.")
        return results

    # Convert the search value to a string for robust comparison, especially for partial matches
    search_term = str(search_value).lower()
    
    for record in data_list:
        # Check for the key and convert its value to string/lowercase for comparison
        record_value = str(record.get(search_key, '')).lower()
        
        # We use 'in' to allow for partial searches (e.g., searching for '2024-10-27' 
        # finds all accidents on that date)
        if search_term in record_value:
            results.append(record)
            
    return results

def find_most_frequent_by_key(data_list, key):
    """
    Calculates the frequency of values for a given key and returns the most common one.
    This function handles both 'car' and 'city' requests.
    
    :param data_list: The list of accident dictionaries.
    :param key: The field name to analyze ('car', 'city', etc.).
    :return: A tuple containing (most_common_item, count). Returns (None, 0) if data is empty.
    """
    if not data_list:
        return (None, 0)
        
    # Extract all values for the specified key
    items = [record.get(key) for record in data_list if record.get(key) is not None]
    
    if not items:
        return (None, 0)
        
    # Use the Counter object to count frequencies
    counts = Counter(items)
    
    # most_common(1) returns a list of the single most common element: [('item', count)]
    most_common = counts.most_common(1)
    
    if most_common:
        return most_common[0]  # Returns ('item', count)
    else:
        return (None, 0)

# --- Main Execution ---

def read_and_analyze_json_file(filename):
    """
    Reads the JSON file and performs the required analysis.
    """
    print(f"\n--- Reading content from {filename} for analysis ---")
    
    if not os.path.exists(filename):
        print(f"Error: File not found at {filename}")
        return

    try:
        with open(filename, mode='r', encoding='utf-8') as jsonfile:
            data_list = json.load(jsonfile)
            
            if not isinstance(data_list, list):
                print("Warning: JSON structure is not a list of records. Analysis stopped.")
                return

            print(f"Total accident records loaded: {len(data_list)}")
            print("-" * 40)
            
            # 1. Search Function Demonstration
            search_term = 'Anytown'
            search_results = search_accidents(data_list, 'city', search_term)
            print(f"Analysis 1: Finding accidents in '{search_term}' ({len(search_results)} found):")
            for result in search_results:
                print(f"  - ID {result['id']}: Car: {result['car']} at {result['date_time']}")
            print("-" * 40)

            # 2. Most Frequent Location (City)
            most_common_city, city_count = find_most_frequent_by_key(data_list, 'city')
            print(f"Analysis 2: Most frequent accident city:")
            print(f"  - City: {most_common_city} with {city_count} accidents.")
            print("-" * 40)

            # 3. Most Frequent Car
            most_common_car, car_count = find_most_frequent_by_key(data_list, 'car')
            print(f"Analysis 3: Most frequently crashed car model:")
            print(f"  - Car: {most_common_car} with {car_count} crashes.")
            print("-" * 40)


    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file {filename} is not valid JSON.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Optional: Clean up the dummy file
        if os.path.exists(filename):
            os.remove(filename)
            print(f"\nCleaned up and deleted {filename}.")


if __name__ == "__main__":
    json_filename = 'sample_accident_data.json'
    
    # Step 1: Create the file
    create_dummy_json(json_filename)
    
    # Step 2: Read and analyze the file
    read_and_analyze_json_file(json_filename)