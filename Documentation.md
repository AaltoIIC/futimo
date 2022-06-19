## Files

### generate_test_data.py
This script can be used to generate test data.

A .txt file can be used to define the distributions of generated data. The structure of this file is desribed in [test_data_descriptions.txt](#test_data_descriptions.txt) below. If there are not enough variables gaussian distribution with mu = 0 and sigma = 1 is used to generate variable values.

The structure of the generated .csv file is as follows
    Timestamp 1;Variable 1 value;Variable 2 value;Variable n value
    Timestamp 2;Variable 1 value;Variable 2 value;Variable n value
    Timestamp n;Variable 1 value;Variable 2 value;Variable n value

### test_data_descriptions.txt
This file stores the parameters for gaussian distributions used to generate test data. In addition, it is possible to define binary variables.
Each row of the file contains variable name (optional) separated with semicolon (;) from distribution parameters mu (excpected value) and sigma (standard deviation) separated by a colon (for ex. 0, 1). These parameters are then given to random.gauss() function in the script `generate_test_data.py`. To define binary function, give a propability of True value. For example, 0.581. (58.1%)
Each row corresponds to one variable and `generate_test_data.py` uses the first row as the first variable it creates, second row to the second variable, and so on. If not enough rows are defined, standard normal distribution mu=0, sigma=1 is used for the rest of the variables. The name of the variable can be left out as demonstarted in the last row of below. In this case only mu and sigma are given. (Note: In the fuzzification process, names for the variables are read from [test_data_descriptions.txt](#test_data_descriptions.txt) file.) Example of the `test_data_descriptions.txt` file:

    Temperature; 30, 15
    Voltage; 1, 3
    Motor speed rpm; 500, 100
    AlertOn; 0.581
    Variable 5; 2, 5
    0, 1


### fuzzy_modeling.py
This script is used to fuzzify data and store it in SQLite database. 

### fuzzy_sets.txt
This file defines the membership functions of fuzzy sets for the modeled variables. Currently, it is only possible to use gaussian functions for defining membership functions.
Each line contains the variable name and membership functions of its fuzzy sets separated by semicolons. Each function is described with mu (excpected value) and sigma (standard deviation). Optionally, names for fuzzy sets can be given. If name is not given, a fuzzy set is referenced with its ordinal number. To model binary variables (that have only true or false state), give only variable name such as "AlertOn" in the example below. The order of the fuzzy sets defines for which column in the test data they are used. First row is used for the second column (first column is timestamp), second row for third column and so on. Example of `fuzzy_sets.txt` file below.

    Temperature; -10, 11.8, Cold; 20, 8.5, Warm; 35, 8.5, Hot
    Voltage; 0, 1; 1, 1; 2, 1
    Motor speed rpm; 200, 30, low; 400, 30; 600, 30, rather high; 800, 30
    AlertOn;
    Variable 5; -5, 1; -3, 1; -1, 1

### expand_fuzzy_sets_for_visualization.py
This script is used to export data from database to a csv file that can be used by other programs (such as MATLAB) to visualize data. The idea is that it includes the parameters of the fuzzy sets' membership functions into the cdv file.
The output format of the file produced by the script is as follows:

    (Optionally timestamp 1), MeanOfMembershipFunction of first variable, SigmaOfMembershipFunction of first variable, MeanOfMembershipFunction of second variable, SigmaOfMembershipFunction of second variable, ..., Weight
    (Optionally timestamp 2), MeanOfMembershipFunction of first variable, SigmaOfMembershipFunction of first variable, MeanOfMembershipFunction of second variable, SigmaOfMembershipFunction of second variable, ..., Weight

The script uses [fuzzy_sets.txt](#fuzzy_sets.txt) file for definition.

### generate_fuzzy_sets.py
This script is used to generate selected number of fuzzy sets and their membership functions. The result is printed to console and cane be copy-pasted into fuzzy_sets.txt