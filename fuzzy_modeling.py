import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib
import csv
import sqlite3
import uuid
import datetime
import heapq
from enum import Enum

#Visualization parameters
VISUALIZATION_FUZZY_SETS = False #Visualize membership functions read from FILE_NAME_FUZZY_SETS, True = on, False = off
VISUALIZATION_INPUT_DATA = False #Visualize input data from FILE_NAME_TEST_DATA, True = on, False = off
VISUALIZATION_FUZZIFIED_DATA = True #Visualize fuzzified values, True = on, False = off #TODO
VISUALIZATION_WIDTH = 5 # How many times the std. dev. is the width of the visualization
VISUALIZATION_NO_POINTS = 200 # How many points are used for visualization

FILE_NAME_FUZZY_SETS = "examples/fuzzy_sets.txt" #Definitions for fuzzy sets
FILE_NAME_TEST_DATA = "test_data_set.csv" #Input data
FILE_NAME_DATA_BASE = "fuzzy_data.db" #Database location

class Conjuction_method(Enum):
    AVERAGE = 1

SELECTED_CONJUNCTION_METHOD = Conjuction_method.AVERAGE

class Variable_type(Enum):
    BINARY = 1
    NUMERIC = 2



#Read fuzzy set definitions from FILE_NAME_FUZZY_SETS
def read_fuzzy_sets():
    list_of_fuzzy_sets = [] # Structure [(Variable name, [(mu, sigma, [optional name for fuzzy set])]), (Variable name 2, [])]
    with open(FILE_NAME_FUZZY_SETS, "r") as f:
        for line in f:
            variable_name, *mf_functions = line.split(";")
            list_of_mf_functions = [] #list of tuples containing (mu, sigma, [optional name for fuzzy set]). Each tuple presents a single fuzzy set. If this list is empty, the variable is binary variable.
            for mf_function in mf_functions:
                if mf_function.strip() != "": #to prevent problems with extra ";" at the end of a line
                    items = mf_function.split(",")
                    items[0] = float(items[0].strip()) #Change mu to float
                    items[1] = float(items[1].strip()) #Change sigma to float
                    if len(items) == 3:
                        items[2] = items[2].strip()
                    list_of_mf_functions.append(tuple(items)) 
            list_of_fuzzy_sets.append(tuple([variable_name.strip(), list_of_mf_functions]))

    if VISUALIZATION_FUZZY_SETS:
        for variable in list_of_fuzzy_sets:
            visualize_membership_functions_of_variable(variable)
    print(list_of_fuzzy_sets)
    return list_of_fuzzy_sets

#TODO: Kirjoita data tietokantaan
def read_data_and_fuzzify(fuzzy_sets):
    #Read csv file row by row
    with open(FILE_NAME_TEST_DATA, "r") as f:
        reader = csv.reader(f, delimiter=";")
        fuzzified_data = [] #Data structure: [[timestamp, [membership grades of fuzzysets variable 1], [variable 2], [variable n]], [timestamp 2, [variable 1], [variable2], [variable 2]]]
        variable_names = next(reader)[1:]
        for row in reader:
            data_row = [] #Single row for fuzzified_data. Data structure: [timestamp, [membership grades of fuzzysets variable 1], [variable 2], [variable n]]
            timestamp = row[0]
            data_row.append(timestamp)
            for i in range(0, len(row) - 1):
                fuzzy_sets_mfs = fuzzy_sets[i][1] #Fuzzy sets' membership functions related to a single variable
                if len(fuzzy_sets_mfs) == 0: #Check if boolean variable
                    grades = [row[i + 1]] #Value tells if it is true or false. 1 = true, 0 = false
                else:
                    #calculate grade for fuzzy sets of a single variable
                    grades = []
                    for mf in fuzzy_sets_mfs:
                        grades.append(gaussian_func(float(row[i + 1]), mf[0], mf[1]))
                data_row.append(grades) #Add fuzzy set grades of a single into data_row
            fuzzified_data.append(data_row) #Add data row into the data structure TODO: replace this with writing to db
    
    #Write fuzzified data into database
    try:
    
        conn = sqlite3.connect(FILE_NAME_DATA_BASE)
        cursor = conn.cursor()
        print("Connected to database")
        

        for row in fuzzified_data:
            timestamp = row[0]
            highest_grade_fuzzy_sets = [] #Stores the highest order fuzzy sets for each variable with the associated grade. Structure [(ordinal number of variable 1, membership grade of variable 1), (ordinal number of variable 2, membership grade of variable 2)]
            second_highest_grade_fuzzy_sets = [] #Stores the second highest fuzzy sets for each variable
            for i in range(1, len(row)):
                #Find two highest grade fuzzy sets per variable
                    if len(row[i]) > 1:
                        two_highest_grades = heapq.nlargest(2, row[i])
                        ordinal_numbers_of_highest_grade_fuzzy_sets = [row[i].index(grade) + 1 for grade in two_highest_grades]
                        highest_grade_fuzzy_sets.append((two_highest_grades[0], ordinal_numbers_of_highest_grade_fuzzy_sets[0]))
                        second_highest_grade_fuzzy_sets.append((two_highest_grades[1], ordinal_numbers_of_highest_grade_fuzzy_sets[1]))
                    else:
                        #binary variable
                        highest_grade_fuzzy_sets.append((Variable_type.BINARY, row[i][0]))
                        second_highest_grade_fuzzy_sets.append((Variable_type.BINARY, row[i][0]))

            if SELECTED_CONJUNCTION_METHOD == Conjuction_method.AVERAGE:
                highest_weight = np.average(list(map(lambda grade_tuple: grade_tuple[0],  filter(lambda x: x[0] != Variable_type.BINARY, highest_grade_fuzzy_sets)))) #filter binary values out and select grades from tuple
                second_highest_weight = np.average(list(map(lambda grade_tuple: grade_tuple[0],  filter(lambda x: x[0] != Variable_type.BINARY, second_highest_grade_fuzzy_sets)))) #filter binary values out and select grades from tuple
                
            #Finally write into database
            print(highest_grade_fuzzy_sets, highest_weight)
            print(second_highest_grade_fuzzy_sets, second_highest_weight)

            #NOTE: This method of directly modifying query string is insecure and should ne modified for production version
            #Add first highest grade fuzzy sets into query and after that aa second highest grades
            insert_query = """INSERT INTO fuzzy_data
                                (id, Timestamp,""" + ",".join([variable_name.replace(" ", "") for variable_name in variable_names]) + """, Weight) 
                                Values (""" + timestamp + "," + ",".join([str(grade_tuple[1]) for grade_tuple in highest_grade_fuzzy_sets]) + "," + str(highest_weight) + """),
                                ("""+ timestamp + "," + ",".join([str(grade_tuple[1]) for grade_tuple in second_highest_grade_fuzzy_sets]) + "," + str(highest_weight) + ");"
            

        
            count = cursor.execute(insert_query)
            conn.commit()
            cursor.close()

    except sqlite3.Error as error:
        print("Fail", error)

    finally:
        #if conn:
            #conn.close()
        print("Connection to database closed")


#Helper function to visualize membership functions
def gaussian_func(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

#Draw all membership functions of a single variable into a single figure
def visualize_membership_functions_of_variable(variable):
    #variable structure ("Variable name", [(mu, sigma, [optional name]), (mu2, sigma2, [optional name 2])]). Contains functions of a single variable
    list_of_functions = variable[1]
    if len(list_of_functions) > 0:
        random_number = uuid.uuid4().int
        legends = []
        plt.figure(random_number) #We are creating multiple figures and eacn needs unique indentifier
        for gaussian_function in list_of_functions:
            x_values = np.linspace(gaussian_function[0] - gaussian_function[1] * VISUALIZATION_WIDTH, gaussian_function[0] + gaussian_function[1] * VISUALIZATION_WIDTH, VISUALIZATION_NO_POINTS)
            plt.plot(x_values, gaussian_func(x_values, gaussian_function[0], gaussian_function[1]))
            if len(gaussian_function) == 3:
                legends.append(gaussian_function[2])
            else:
                legends.append("Fuzzy set " + str(len(legends) + 1))
    else:
        legends = ["Binary variable"]
        plt.plot(1, 1)
    plt.title(variable[0])
    plt.legend(legends)
    plt.show()


#Visualize input data
def visualize_input_data():
    timestamps = [] #list of timestamps, used as x values
    variable_values = [] #two dimensional list [[variable 1 values], [variable 2 values]] used as y values

    #Read data from file
    with open(FILE_NAME_TEST_DATA, "r") as f:
        reader = csv.reader(f, delimiter=";")
        first_line = next(reader) #read column names
        variable_names = first_line[1:] #leave column out as it is timestamp
        variable_values = [[] for _ in range(len(variable_names))] #initialize list with an empty list for each variable
        for row in reader:
            year, month, day, hours, minutes, seconds, milliseconds = map(int, row[0].split("T")[0].split("-") + row[0][:-1].split("T")[1].split(".")[0].split(":") + [row[0][:-1].split(".")[1]]) #change timestamp into datetime object
            timestamps.append(datetime.datetime(year, month, day, hours, minutes, seconds, milliseconds * 1000))
            for i in range(1, len(row)):
                variable_values[i - 1].append(float(row[i]))

    #Plot data
    for i in range(len(variable_values)):
        plt.figure(variable_names[i]) #We are creating multiple figures and each needs unique indentifier
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%dT%H:%M:%S.%f'))
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.plot(timestamps, variable_values[i])
        plt.gcf().autofmt_xdate()
        plt.title(variable_names[i])
        plt.show()
    

#TODO: Visualize data in database
def visualize_data_in_database():
    pass

def main():
    fuzzy_sets = read_fuzzy_sets()
    read_data_and_fuzzify(fuzzy_sets)
    if VISUALIZATION_INPUT_DATA:
        visualize_input_data()

if __name__ == "__main__":
    main()