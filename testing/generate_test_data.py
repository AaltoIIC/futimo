"""This is a helper function to generate test data"""
import csv
import datetime
import random
import numpy as np

NUMBER_OF_VARIABLES = 10000 #Defines the number of variables in the generated test data
STARTDATE = "2023-10-20T11:35:40.000Z" #The starting timestamp for test data
TIME_INTERVAL = 200 #Time between data rows in millisecods
NUMBER_OF_ROWS = 100 #How many rows are generated
SIGMA = 20
MU = 60

#FILE_NAME_VARIABLE_DESCRIPTIONS = "examples/test_data_descriptions.txt" #File where variable descriptions are defined if this fiel does not exists gaussian distribution with user defined mu and sigma for each variable is used.
FILE_NAME_VARIABLE_DESCRIPTIONS = None

#FILE_NAME = "test_data_set.csv" #File name for the generated .csv file
FILE_NAME = "../examples/test_data_set_100_rows_10000_variables.csv"

#Read parameters from FILE_NAME_VARIABLE_DESCRIPTIONS for generating test data
def read_variable_descriptions(mu, sigma):
    variable_descriptions = [] #List structure [(mu1, sigma1), (propability of true value for binary variables), (mu3, sigma3)] the tuples of the correspond to the first, second, and third variable, and so on
    variable_names = [] #List structure ["variable name 1", "variable name 2", "variable name n"]. If name is not given, "Variable + <order of the variable>" is used. For example, "Variable 3"
    try:
        with open(FILE_NAME_VARIABLE_DESCRIPTIONS, "r") as f:
            i = 0
            for line in f:
                i += 1
                data = line.split(";")
                if len(data) == 1:
                    variable_names.append("Variable " + str(i))
                else:
                    variable_names.append(data[0].strip())
                data = data[-1].split(",")
                if len(data) == 2: #gaussian distribution
                    variable_descriptions.append(tuple([float(data[0].strip()), float(data[1].strip())]))
                elif len(data) == 1: #binary variable
                    variable_descriptions.append(tuple([float(data[0].strip())]))
    except:
        print(f"No variable description file found. Using gaussian distribution (mu = {mu} and sigma = {sigma}) for generating variables.")
        variable_names = variable_names = ["Variable" + str(i + 1) for i in range(NUMBER_OF_VARIABLES)]
    return variable_descriptions, variable_names

def generate_data(variable_descriptions, variable_names, mu, sigma):
    #create datetime object from STARTDATE
    year, month, day, hours, minutes, seconds, milliseconds = map(int, STARTDATE.split("T")[0].split("-") + STARTDATE[:-1].split("T")[1].split(".")[0].split(":") + [STARTDATE[:-1].split(".")[1]])
    start_date = datetime.datetime(year, month, day, hours, minutes, seconds, milliseconds * 1000)

    #Generate data using variable_descriptions and write to .csv file
    with open(FILE_NAME, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["Timestamp"] + [name for name in variable_names])
        for i in range(NUMBER_OF_ROWS):
            data_row = [start_date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"]
            defined_variables = len(variable_descriptions) #number of variables to which description is defined
            for i in range(NUMBER_OF_VARIABLES):
                if i < defined_variables: #if the distibution has been defined
                    if len(variable_descriptions[i]) == 2: #gaussian
                        data_row.append(random.gauss(variable_descriptions[i][0], variable_descriptions[i][1]))
                    elif len(variable_descriptions[i]) == 1: #binary
                        data_row.append(np.random.choice(2, p=[1-variable_descriptions[i][0], variable_descriptions[i][0]]))
                else:
                    #If there were not enough variables defined in FILE_NAME_VARIABLE_DESCRIPTIONS, use gaussian function with user-defined mu and sigma for the rest of variables
                    data_row.append(random.gauss(mu, sigma))
            writer.writerow(data_row)
            start_date = start_date + datetime.timedelta(milliseconds=TIME_INTERVAL)

if __name__ == "__main__":
    variable_descriptions, variable_names = read_variable_descriptions(MU, SIGMA)
    generate_data(variable_descriptions, variable_names, mu=MU, sigma=SIGMA)