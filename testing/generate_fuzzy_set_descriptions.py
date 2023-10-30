"""This is a helper function to generate fuzzy set descriptions file"""

import numpy as np

FILE_NAME = "../examples/fuzzy_sets_500.txt"
NUMBER_OF_VARIABLES = 500 #Number of variables
NUMBER_OF_FUZZY_SETS = 10 #Number of fuzzy sets
START = 0 #First mean for gaussian function
END = 120 #Last mean for gaussian function
SIGMA = 5.6621 #Sigma for the membership function

def generate_membership_functions(file_name, number_of_variables, number_of_fuzzy_sets, start, end, sigma):
    with open(file_name, "w") as f:
        for i in range(number_of_variables):
            means = np.linspace(start, end, number_of_fuzzy_sets)
            #Uses generic variable name
            string = f"Variable{i + 1}; "
            string += "; ".join([str(mean) + ", " + str(sigma) for mean in means])
            string += "\n"
            f.write(string)

def main():
    #Examples for crane bridge
    #generate_membership_functions(26, 0, 26, 0.5)
    #Example load tare
    #generate_membership_functions(3, 0, 2, 0.4)
    #Example hoist position
    #generate_membership_functions(10, 0, 3, 0.15)
    #Crane trolley
    #generate_membership_functions(10, 0, 10, 0.5)
    #This function uses parameters defined at the beginning
    generate_membership_functions(FILE_NAME, NUMBER_OF_VARIABLES, NUMBER_OF_FUZZY_SETS, START, END, SIGMA)

if __name__ == "__main__":
    main()

