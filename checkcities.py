import csv

RUN_FILE = 'cities.csv'  # this is a test file
CITY_FILE = 'worldcitiespop.txt'
MERGED_CITIES_FILE = 'merged_cities.csv'
ERROR_CITIES_FILE = 'error_cities_file.csv'
GOOD_CITIES_FILE = 'good_cities.csv'
BAD_CITIES_FILE = 'bad_cities.csv'
print(RUN_FILE)


def save_results(raw_file, results):
    #  results_file = open(raw_file, 'w')
    with open(raw_file, "w") as f:
        writer = csv.writer(f)
        writer.writerows(results)
    f.close()
    return


def parse(raw_file, delimiter):
    """
    :param raw_file: probably csv file
    :param delimiter: specify delimiter #TODO add default arg : ','
    :return: parsed data
    Parses a raw CSV file to a JSON-line object.
    """
    #  open csv file
    opened_file = open(raw_file, encoding="Latin-1")
    #  read csv file
    csv_data = csv.reader(opened_file, delimiter=delimiter)  # first delimiter is csv.reader variable name
    #  csv_data object is now an iterator meaning we can get each element one at a time
    #  print(csv_data)
    #  build data structure to return parsed data
    parsed_data = []  # this list will store every row of data
    fields = csv_data.__next__()  # this will be the column headers; we can use .next() because csv_data is an iterator
    for row in csv_data:
        if row[1] == "":  # there is no text in the field so no data to process
            pass
        else:
            parsed_data.append(dict(zip(fields, row)))  # Creates a new dict item for each row with col header as key and stores in a list
        #  city_count += 1
    #  print("data list is: ", parsed_data)
    #  print("Type of parsed_data is: ", type(parsed_data))
    # close csv file
    opened_file.close()
    return parsed_data


def check_cities(city_data, world_cities):
    our_cities = city_data
    world_cities = world_cities
    merged_cities = []
    error_cities = []
    error_count = 0
    success_count = 0
    errors_changed = 0
    cities_tested = 0
    for city1 in our_cities:
        cities_tested += 1
        for city2 in world_cities:
            if city1['RowKey'].lower() == city2['City'].lower() and city1['CountryCode'].lower() == city2['Country'].lower():
                city_info = [city1['RowKey'], city1['PartitionKey'], city1['CountryCode'], city2['City'], city2['Country']]
                merged_cities.append(city_info)
                success_count += 1
                if cities_tested - success_count != errors_changed:  # record error city
                    error_cities.append(city_info)
                    errors_changed = cities_tested - success_count
                    print('error found')

    print('potential errors found', success_count - error_count)
    return merged_cities, error_cities


def find_bad_cities(city_data, good_city):
    our_cities = city_data
    good_cities = good_city
    bad_cities = []
    city_status = 'bad'
    for city1 in our_cities:
        city_status = 'bad'
        for city2 in good_cities:
            if city1['RowKey'].lower() == city2['City'].lower() and city1['CountryCode'].lower() == city2['Country'].lower():
                city_status = 'good'
                break
        if city_status == 'bad':
                city_info = [city1['RowKey'], city1['PartitionKey'], city1['CountryCode'], city2['City'], city2['Country']]
                bad_cities.append(city_info)
    return bad_cities


def main():
    # Call our parse function with required file an delimiter
    city_data = parse(RUN_FILE, ',')
    #  print(city_data)
    print("keys for our city data are:", city_data[0].keys())
    #  world_cities = parse(CITY_FILE, ',')
    #  print("keys for world cities are: ", world_cities[0].keys())
    good_cities = parse(GOOD_CITIES_FILE, ',')
    #  print(overlaps)
    #  merged_cities, error_cities = check_cities(city_data, world_cities)
    bad_cities = find_bad_cities(city_data, good_cities)
    #  save_results(MERGED_CITIES_FILE, merged_cities)
    #  save_results(ERROR_CITIES_FILE, error_cities)
    save_results(BAD_CITIES_FILE, bad_cities)

if __name__ == "__main__":
    main()
