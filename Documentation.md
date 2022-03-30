## Files

### generate_test_data.py

### test_data_gaussians.txt
This file stores the parameters for gaussian distributions used to generate test data.
Each row of the file contains mu (excpected value) and sigma (standard deviation) separated by colon (for ex. 0, 1). These parameters are then given to random.gauss() function in the script `generate_test_data.py`. 
Each row corresponds to one variable and `generate_test_data.py` uses the first row as the first variable it creates, second row to the second variable, and so on. If not enough rows are defined, standard normal distribution mu=0, sigma=1 is used for the rest of the variables. Example of the `test_data_gaussians.txt` file below.

    0, 1
    3, 10
    1, 1
    2, 2
    0, 1


### fuzzy_modeling.py

### fuzzy_membership_functions.txt
This file defines the membership functions of fuzzy sets for the modeled variables. Currently, it is only possible to use gaussian functions for defining membership fucntions.
Each line contains the variable name and membership ship functions of its fuzzy sets separated by semicolons. Each function is described with mu (excpected value) and sigma (standard deviation). Optionally, a name for the fuzzy set can be given. Example of `fuzzy_membership_functions.txt` file below.

    Temperature; -10, 150, Cold; 20, 75, Warm; 35, 75, Hot
    Variable 1; 0, 1; 1, 1; 2, 1;
    Variable 2; -2, 2, low; 1, 2; 2, 2, rather high; 3, 2;
