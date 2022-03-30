import csv
import datetime
import random

NUMBER_OF_VARIABLES = 5
STARTDATE = "2022-03-20T11:35:40.000Z"
TIME_INTERVAL = 200 #milliseconds
NUMBER_OF_ROWS = 10

FILE_NAME = "test_data_set.csv"

def main():
    year, month, day, hours, minutes, seconds, milliseconds = map(int, STARTDATE.split("T")[0].split("-") + STARTDATE[:-1].split("T")[1].split(".")[0].split(":") + [STARTDATE[:-1].split(".")[1]])
    #print(year, month, day, hours, minutes, seconds, milliseconds)
    start_date = datetime.datetime(year, month, day, hours, minutes, seconds, milliseconds)
    with open(FILE_NAME, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["Timestamp"] + ["Variable {}".format(i + 1) for i in range(NUMBER_OF_VARIABLES)])
        for i in range(NUMBER_OF_ROWS):
            writer.writerow([start_date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"] + [random.random() for i in range(NUMBER_OF_VARIABLES)])
            start_date = start_date + datetime.timedelta(milliseconds=TIME_INTERVAL)

    #print(start_date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z")
    #start_date = start_date + datetime.timedelta(milliseconds=TIME_INTERVAL)
    #print(start_date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z")

if __name__ == "__main__":
    main()