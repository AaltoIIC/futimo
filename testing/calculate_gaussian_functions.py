"This is a helper script to calculate the gaussian membership functions if the functions should intersect 0.5 membership level"

import csv
import math

#INPUT_CSV = "vehicle_data_modified/time_bucketed.csv"
INPUT_CSV = "time_bucketed_car.csv"
OUTPUT_TXT = "fuzzy_sets_car.txt"

def read_csv(filename):
    data = {}
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        for header in headers[1:]:
            data[header] = []
        for row in reader:
            for header, value in zip(headers[1:], row[1:]):
                data[header].append(float(value))
    return data

def determine_rounding(value):
    if value == 0:
        return 2
    order_of_magnitude = math.floor(math.log10(abs(value)))
    return max(8 - order_of_magnitude, 0)

def calculate_gaussian_parameters(min_val, max_val, num_sets=10):
    step = (max_val - min_val) / (num_sets - 1)
    sigma = step / (2 * math.sqrt(2 * math.log(2)))
    peaks = [min_val + step * i for i in range(num_sets)]
    
    rounding = determine_rounding(max(abs(min_val), abs(max_val)))
    peaks = [round(peak, rounding) for peak in peaks]
    sigma = round(sigma, rounding)
    
    return peaks, sigma

def write_to_file(filename, data):
    with open(filename, 'w') as file:
        for variable, values in data.items():
            peaks, sigma = calculate_gaussian_parameters(min(values), max(values))
            file.write(variable + "; " + "; ".join([f"{peak}, {sigma}" for peak in peaks]) + "\n")

if __name__ == "__main__":
    print(calculate_gaussian_parameters(0, 140, 10))
    #data = read_csv(INPUT_CSV)
    #write_to_file(OUTPUT_TXT, data)