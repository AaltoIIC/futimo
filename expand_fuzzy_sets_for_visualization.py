import csv
import functools
from fuzzy_modeling import TABLE_NAME, read_fuzzy_sets, aggregate_data_with_query

# File names
FILE_NAME_FUZZY_SETS = "examples/fuzzy_sets_crane_visualization.txt" #Definitions for fuzzy sets
FILE_NAME_DATA_BASE = "fuzzy_data.db" #Database location
OUTPUT_FILE = "data_for_visualization.csv"

#Select csv file delimiter
CSV_DELIMITER = ","

# Aggregate data
AGGREGATE_DATA = True #Fetch aggregated data from database
LIST_OF_AGGREGATED_VARIABLES = ["BridgePosition", "TrolleyPosition"] #["Temperature", "Voltage", "Motor speed rpm", "AlertOn", "Variable 5"] #Select aggregated variables
TABLE_NAME = "fuzzy_sets_crane"

def construct_output_file(data, fuzzy_sets, outputfile, delimiter, list_of_variables):
    with open(outputfile, "w") as f:
        writer = csv.writer(f, delimiter=delimiter)
        #Write headers
        headers = functools.reduce(lambda a, variable: a + [variable + "Mean", variable + "Sigma"], list_of_variables, []) + ['Weight']
        writer.writerow(headers)
        for row in data:
            data_row = []
            for i in range(len(row) - 1):
                ordinal_number = row[i]
                mean, sigma = fuzzy_sets[i][1][ordinal_number - 1]
                data_row.extend([mean, sigma])

            data_row.append(row[-1]) #Weight
            writer.writerow(data_row)


def main():
    fuzzy_sets = read_fuzzy_sets(FILE_NAME_FUZZY_SETS)
    if AGGREGATE_DATA:
        data = aggregate_data_with_query(LIST_OF_AGGREGATED_VARIABLES, FILE_NAME_DATA_BASE, TABLE_NAME)
    construct_output_file(data, fuzzy_sets, OUTPUT_FILE, CSV_DELIMITER, LIST_OF_AGGREGATED_VARIABLES)
    
if __name__ == "__main__":
    main()

