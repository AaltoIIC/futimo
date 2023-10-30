import csv
import functools
import sqlite3
from fuzzy_modeling import read_fuzzy_sets, aggregate_data_with_query

# File names
#FILE_NAME_FUZZY_SETS = "examples/fuzzy_sets.txt" #Definitions for fuzzy sets
FILE_NAME_FUZZY_SETS = "examples/fuzzy_sets_car.txt"
FILE_NAME_DATA_BASE = "fuzzy_data.db" #Database location
OUTPUT_FILE = "data_for_visualization.csv"

# Select csv file delimiter
CSV_DELIMITER = ";"

#Select aggregated variables
#LIST_OF_AGGREGATED_VARIABLES = ["Temperature", "Voltage", "Motor speed rpm", "AlertOn", "Variable 5"] #The order of variables MUST BE same as in the database/fuzzy sets description file
#LIST_OF_AGGREGATED_VARIABLES = ["BridgePosition", "LoadTare", "HoistPosition", "TrolleyPosition"]

# OR

USE_ALL_VARIABLES = True #Use all variables in aggregation

#TABLE_NAME = "fuzzy_sets"
#TABLE_NAME = "crane_data"
TABLE_NAME = "car_data"

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

def get_variable_names(database_file, table_name):
    try:
        # Connect to database
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()
        print("Connected to database")
        
        # NOTE: This method of directly modifying query string is insecure and should ne modified for production version
        # Get all columns
        query = 'SELECT * FROM ' + table_name
        cursor.execute(query)
        names = list(map(lambda x: x[0], cursor.description))[2:-1]
        return names


    except sqlite3.Error as error:
        print("Error with database", error)

    finally:
        cursor.close()
        if conn:
            conn.close()
        print("Connection to database closed, visualization")


def main():
    fuzzy_sets = read_fuzzy_sets(FILE_NAME_FUZZY_SETS)
    if USE_ALL_VARIABLES:
        names = get_variable_names(FILE_NAME_DATA_BASE, TABLE_NAME)
        data = aggregate_data_with_query(names, FILE_NAME_DATA_BASE, TABLE_NAME)       
    else:
        names = LIST_OF_AGGREGATED_VARIABLES
        # Select only necessary fuzzy sets
        fuzzy_sets = list(filter(lambda fuzzy_set: fuzzy_set[0] in names, fuzzy_sets))
        data = aggregate_data_with_query(LIST_OF_AGGREGATED_VARIABLES, FILE_NAME_DATA_BASE, TABLE_NAME)
    construct_output_file(data, fuzzy_sets, OUTPUT_FILE, CSV_DELIMITER, names)
    
if __name__ == "__main__":
    main()

