import csv
import functools
from fuzzy_modeling import read_fuzzy_sets, aggregate_data_with_query

# File names
#FILE_NAME_FUZZY_SETS = "examples/fuzzy_sets.txt" #Definitions for fuzzy sets
FILE_NAME_FUZZY_SETS = "examples/fuzzy_sets_crane.txt" #Definitions for fuzzy sets
FILE_NAME_DATA_BASE = "fuzzy_data.db" #Database location
OUTPUT_FILE = "data_for_visualization.csv"

# Select csv file delimiter
CSV_DELIMITER = ";"

# Aggregate data
AGGREGATE_DATA = True #Fetch aggregated data from database

#Select aggregated variables
#LIST_OF_AGGREGATED_VARIABLES = ["Temperature", "Voltage", "Motor speed rpm", "AlertOn", "Variable 5"] #The order of variables MUST BE same as in the database/fuzzy sets description file
LIST_OF_AGGREGATED_VARIABLES = ["BridgePosition", "LoadTare", "HoistPosition", "TrolleyPosition", "AlarmOn"]

#TABLE_NAME = "fuzzy_sets"
TABLE_NAME = "crane_data"

def construct_output_file(data, fuzzy_sets, outputfile, delimiter, list_of_variables):
    with open(outputfile, "w") as f:
        writer = csv.writer(f, delimiter=delimiter)
        #Write headers
        headers = functools.reduce(lambda a, variable: a + [variable.replace(" ", "") + "Mean", variable.replace(" ", "") + "Sigma"], list_of_variables, []) + ['Weight']
        writer.writerow(headers)
        for row in data:
            data_row = []
            for i in range(len(row) - 1):
                ordinal_number = row[i]
                try:
                    mean, sigma = fuzzy_sets[i][1][ordinal_number - 1][:2]
                except IndexError:
                    #Binary variable
                    mean, sigma = 1, -1 #sigma -1 indicates that binary variable
                data_row.extend([mean, sigma])
            data_row.append(row[-1]) #Weight
            writer.writerow(data_row)


def main():
    fuzzy_sets = read_fuzzy_sets(FILE_NAME_FUZZY_SETS)
    # Select only necessary fuzzy sets
    fuzzy_sets = list(filter(lambda fuzzy_set: fuzzy_set[0] in LIST_OF_AGGREGATED_VARIABLES, fuzzy_sets))
    if AGGREGATE_DATA:
        data = aggregate_data_with_query(LIST_OF_AGGREGATED_VARIABLES, FILE_NAME_DATA_BASE, TABLE_NAME)
    construct_output_file(data, fuzzy_sets, OUTPUT_FILE, CSV_DELIMITER, LIST_OF_AGGREGATED_VARIABLES)
    
if __name__ == "__main__":
    main()

