import csv

RUN_FILE = 'cities.csv'  # this is a test file
RESULTS_FILE = 'overlapping-cities.csv'
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
    opened_file = open(raw_file)
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


def overlap(r1, r2):
    # Overlapping rectangles overlap both horizontally & vertically
    inside_right = float(r1['SW_Lon']) <= float(r2['NE_Lon'])
    outside_left = float(r1['NE_Lon']) >= float(r2['SW_Lon'])
    under_top = float(r1['SW_Lat']) <= float(r2['NE_Lat'])
    above_bottom = float(r1['NE_Lat']) >= float(r2['SW_Lat'])
    h_overlaps = inside_right and outside_left
    v_overlaps = under_top and above_bottom
    return h_overlaps and v_overlaps


def find_overlaps(city_data):
    list1 = city_data
    list2 = city_data
    overlapping_cities = []
    overlap_count = 0
    for city1 in list1:
        # print(city1)
        for city2 in list2:
            #  print(city2)
            if city1['RowKey'] != city2['RowKey']:
                overlap_result = overlap(city1, city2)
                if overlap_result:
                    overlap_count += 1
                    overlapping_cities.append([city1, city2])
    print('net overlaps found;', overlap_count/2)
    return overlapping_cities


def main():
    # Call our parse function with required file an delimiter
    city_data = parse(RUN_FILE, ',')
    #  print(city_data)
    print("keys are:", city_data[0].keys())
    r1 = city_data[1]
    r2 = city_data[2]
    print('The result for r1[RowKey] and r2[RowKey] is: ', overlap(r1, r2))
    overlaps = find_overlaps(city_data)
    #  print(overlaps)
    results = []
    for city_pair in overlaps:
        result = city_pair[0]['CountryCode'], city_pair[0]['RowKey'], 'overlaps with', city_pair[0]['CountryCode'], city_pair[1]['RowKey']
        results.append(result)
    print(results)
    save_results(RESULTS_FILE, results)

if __name__ == "__main__":
    main()
