import numpy as np
import matplotlib.pyplot as plt
import csv
import sqlite3

FILE_NAME = "test_data_set.csv"

def read_functions():
    pass

def read_data_and_store_db():
    #Read csv file row by row

    with open(FILE_NAME, "r") as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            print(row)


def main():
    read_data_and_store_db()

if __name__ == "__main__":
    main()