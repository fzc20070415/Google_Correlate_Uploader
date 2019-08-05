import correlate_demo_1
import login_demo_1
import config
import os

def main():
    print("="*40)

    # Set parameters
    base_folder = '../data'
    input_list = os.listdir(base_folder)
    noise_range = [0]
    time_range = [0]
    day_avg_range = [1]
    result_dir = '../output/result.csv'

    # Initialize result.csv
    print("Initializing result.csv")
    if os.path.exists(result_dir):
        decision = ''
        while decision != 'y' and decision != 'n':
            decision = input("Existing result.csv found. Overwrite?[y/n]")
        if decision == 'n':
            print("Aborting...")
            exit(1)
    result_file = open(result_dir, 'w')
    result_file.write("Original File Directory|Noise Level|Time Difference|Day Average|Results\n")
    result_file.close()
    result_file = open(result_dir, 'a')

    # Login to Google
    print("Login to Google")
    login_demo_1.login(config.USR, config.PWD)


    # Start looping
    for input_dir in input_list:
        for noise in noise_range:
            for time_difference in time_range:
                for day_avg in day_avg_range:
                    print("="*40)
                    print("Current Task Details:\n\tFile: {}\n\tNoise: {}\n\tTime Difference: {}\n\tSmoothing Window: {} days".format(input_dir, noise, time_difference, day_avg))
                    correlate_demo_1.process_data(os.path.join(base_folder, input_dir), time_difference, noise, AW=day_avg)
                    login_demo_1.upload_csv(correlate_demo_1.CSV_OUTPUT_DIR)
                    if login_demo_1.analyze_result():
                        print("-"*40)
                        print("Recording results")
                        result = login_demo_1.read_result()      # TODO: Should return a list
                        result_content = input_dir + '|' + noise + '|' + time_difference + '|' + day_avg + '|[' + ', '.join(result) + ']\n'
                        result_file.write(result_content)

    result_file.close()

if __name__ == "__main__":
    main()
