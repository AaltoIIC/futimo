import sys, os
sys.path.append('..')
from fuzzy_modeling import model_data, aggregate_data_with_query
import time

RESULTS_FILE_NAME = "test_results_new_test12.csv"
RESULTS_FILE_NAME_QUERY = "test_results_query_test12.csv"
NUMBER_OF_TESTS = 2
DIVIDER = 10**9

def test_modeling_and_querying(rows=100, variables=100):
    print(f"Starting test rows={rows}, variables={variables}")
    file_name_fuzzy_sets = f"../examples/fuzzy_sets_{variables}.txt"
    file_name_data = f"../examples/test_data_set_{rows}_rows_{variables}_variables.csv"
    file_name_db = f"db_{rows}_x_{variables}.db"
    table_name = f"table_{rows}_x_{variables}"
    list_of_variables = ["Variable1", "Variable2", "Variable3"]
    i = 0
    results = [] #Two dimensional list. Format [[time_modeling 1, time_query 1], ... [time_modeling n, time_query n]]
    while i < NUMBER_OF_TESTS:
        print(f"TEST ROUND: {i + 1}, rows={rows}, variables={variables}")
        time.sleep(0.5)
        start_time = time.monotonic_ns()
        model_data(file_name_fuzzy_sets, file_name_data, file_name_db, table_name)
        time_query_start = time.monotonic_ns()
        data = aggregate_data_with_query(list_of_variables, file_name_db, table_name)
        time_query_end = time.monotonic_ns()
        #print(data) #For debugging
        os.remove(file_name_db) #remove database
        results.append([time_query_start-start_time, time_query_end-time_query_start])
        time.sleep(0.5)
        i += 1
    return {f'{rows}_rows_{variables}_variables': results}

def test_querying(rows=100000, variables=1000, number_of_variables = [1, 5, 10, 50, 100, 500, 1000]):
    print(f"Starting test rows={rows}, variables={variables}")
    file_name_fuzzy_sets = f"../examples/fuzzy_sets_{variables}.txt"
    file_name_data = f"../examples/test_data_set_{rows}_rows_{variables}_variables.csv"
    file_name_db = f"db_{rows}_x_{variables}.db"
    table_name = f"table_{rows}_x_{variables}"
    #model_data(file_name_fuzzy_sets, file_name_data, file_name_db, table_name)
    results = {} #Key = number of variables queried, value = list of measurements
    for number_of_queried_variables in number_of_variables:
        print("Number of queried variables", number_of_queried_variables)
        list_of_variables = ["Variable" + str(i) for i in range(number_of_queried_variables)]
        results[str(number_of_queried_variables)] = []
        i = 0
        while i < NUMBER_OF_TESTS:
            print(f"TEST ROUND QUERY: {i + 1}, rows={rows}, variables={variables}")
            time.sleep(0.1)
            time_query_start = time.monotonic_ns()
            data = aggregate_data_with_query(list_of_variables, file_name_db, table_name)
            time_query_end = time.monotonic_ns()
            #print(data) #For debugging
            results[str(number_of_queried_variables)].append(time_query_end-time_query_start)
            time.sleep(0.1)
            i += 1
    #os.remove(file_name_db) #remove database
    return results




def run_tests():
    results = {}
    query_results = None
    
    """TEST CASE 1: 100 variables, scalability with different number of rows"""
    
    """
    results.update(test_modeling_and_querying(rows=10000, variables=100))
    results.update(test_modeling_and_querying(rows=25000, variables=100))
    results.update(test_modeling_and_querying(rows=50000, variables=100))
    results.update(test_modeling_and_querying(rows=75000, variables=100))
    results.update(test_modeling_and_querying(rows=100000, variables=100))
    """
    
    """TEST CASE 2: 1 million data points, scalability with different number of variables"""
    """
    results.update(test_modeling_and_querying(rows=100000, variables=10))
    results.update(test_modeling_and_querying(rows=20000, variables=50))
    results.update(test_modeling_and_querying(rows=2000, variables=500))
    results.update(test_modeling_and_querying(rows=1000, variables=1000))
    """
    results.update(test_modeling_and_querying(rows=100, variables=10000))
    
    """TEST CASE 3: 10 million data points, scalability with different number of variables"""
    """
    results.update(test_modeling_and_querying(rows=1000000, variables=10))
    results.update(test_modeling_and_querying(rows=200000, variables=50))
    results.update(test_modeling_and_querying(rows=20000, variables=500))
    results.update(test_modeling_and_querying(rows=10000, variables=1000))
    """
    
    """TEST CASE 4: Querying different number of variables"""
    #query_results = test_querying(rows=100000, variables=1000, number_of_variables=[1, 3, 5, 7, 10, 50, 100, 500, 1000])
    
    return results, query_results
    

def write_results(results):
    with open(RESULTS_FILE_NAME, "w") as f:
        keys = list(results.keys())
        for i in range(len(keys)):
            key = keys[i]
            if i == len(keys) - 1:
                f.write(f"{key}Modeling;{key}Querying;{key}Total")
            else:
                f.write(f"{key}Modeling;{key}Querying;{key}Total;")
        f.write("\n")
        for i in range(NUMBER_OF_TESTS):
            for j in range(len(keys)):
                key = keys[j]
                if j == len(keys) - 1:
                    f.write(f"{results[key][i][0]/DIVIDER};{results[key][i][1]/DIVIDER};{(results[key][i][0] + results[key][i][1]) / DIVIDER}")
                else:
                    f.write(f"{results[key][i][0]/DIVIDER};{results[key][i][1]/DIVIDER};{(results[key][i][0] + results[key][i][1]) / DIVIDER};")
            f.write("\n")
            
def write_results_query(query_results):
    print(query_results)
    with open(RESULTS_FILE_NAME_QUERY, "w") as f:
        keys = list(query_results.keys())
        for i in range(len(keys)):
            key = keys[i]
            if i == len(keys) - 1:
                f.write(f"{key}Querying")
            else:
                f.write(f"{key}Querying;")
        f.write("\n")
        for i in range(NUMBER_OF_TESTS):
            for j in range(len(keys)):
                key = keys[j]
                if j == len(keys) - 1:
                    f.write(f"{query_results[key][i]/DIVIDER}")
                else:
                    f.write(f"{query_results[key][i]/DIVIDER};")
            f.write("\n")
            
def main():
    print("Start tests")
    #start_time = time.monotonic_ns()
    results, query_results = run_tests()
    write_results(results)
    #write_results_query(query_results)
    #print(results)
    #print(f"TOTAL time in seconds: {(start_time - time.monotonic_ns())/DIVIDER}")
    print("Finish tests")
    
if __name__ == "__main__":
    main()