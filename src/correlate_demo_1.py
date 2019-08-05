import csv
import math
import argparse
import numpy as np
import random
import requests
import re
import lxml.etree as etree
import lxml.html as html


CSV_OUTPUT_DIR = '../output/output.csv'

def process_data(input_dir, time_difference, noise_level=0, random=False, AW=0):
    print("-"*40)
    print("Processing data:")

    # Open cvs file
    print("\tReading csv file")
    csvfile =  open(input_dir)
    spamreader = csv.reader(csvfile)

    ts = np.array(list(spamreader))
    # print("Input:")
    # print(ts)

    # Close cvs file
    csvfile.close()

    # Extract data
    print("\tExtracting data")
    date = ts[:,0]
    # data = ts[:,1]
    data = list(map(float, ts[:,1]))
    # print(data)

    # Use X-day-average
    if AW > 1:
        lower = int(AW/2)
        upper = int((AW+1)/2)
        length = len(data)
        print("\tAdd {}-day-average".format(AW))
        new_data = []
        for i in range(length):
            # print(max(0,i-lower),min(length, i+upper))
            new_data.append(np.mean(data[max(0,i-lower):min(length, i+upper)]))
        data = new_data
    else:
        print("\tSkipping smoothing...")

    # Add noise
    print("\tAdding noise")
    if noise_level != 0:
        if random:
            noise = (np.random.random(size=len(data))-0.5) * noise_level * 2
            data = np.array(noise + np.array(data, dtype=float), dtype="<U32")
        else:   # NORMAL
            noise = np.random.normal(size=len(data), scale=noise_level)
            data = np.array(noise + np.array(data, dtype=float), dtype="<U32")

    # Shift time diffence and Merge data
    print("\tShifting time difference")
    output_ts = np.zeros([len(ts)-time_difference, 2])
    output_ts = np.array(output_ts, dtype="<U32")
    output_ts[:,0] = date[:len(ts)-time_difference]
    output_ts[:,1] = data[time_difference:]
    # print("Output:")
    # print(output_ts)

    # Write output
    print("-"*40, "\nWriting into output file at", CSV_OUTPUT_DIR)
    with open(CSV_OUTPUT_DIR, 'w', newline="") as output_csv:
        writer = csv.writer(output_csv)
        writer.writerows(output_ts)

def main():
    # Construct argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="path to input csv")
    ap.add_argument("-d", "--time_difference", required=True, help="input a non-negative integer", type=int)
    ap.add_argument("-n", "--noise_level", help="input a float", type=float)
    ap.add_argument("-r", "--random", action="store_true", help="use random noise instead of normal noise")
    ap.add_argument("-a", "--day_average", type=int, help="select X-day-average")
    args = vars(ap.parse_args())

    noise_level = 0
    AW=0
    RANDOM = False

    input_dir = args["input"]
    time_difference = int(args["time_difference"])
    if args["noise_level"]:
        noise_level = float(args["noise_level"])
        if noise_level <= 0:
            print("ERROR: noise_level value has to be a positive float.")
            exit()
    if args["random"]:
        RANDOM = True
    if args['day_average']:
        AW = args['day_average']
        if AW <= 0:
            print("ERROR: day_average value has to be a positive integer.")
            exit()

    print("Verifying inputs:\n\tTime difference = {}\n\tNoise Level = {}\n\tUse random noise = {}".format(time_difference, noise_level, args["random"]))
    if time_difference < 0:
        print("ERROR: Time difference must be non-negative.")
        exit(1)

    process_data(input_dir, time_difference, noise_level, RANDOM, AW)


if __name__ == "__main__":
    ### DEBUG: File List
    # input_dir = '../data/weekly_s&p.csv'
    ###
    main()

    # 3-day/5-day average
