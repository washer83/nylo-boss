import pandas as pd
import numpy as np

def calculate_percentiles(csv_file):
    data = pd.read_csv(csv_file)
    percentiles = {}

    for column in data.columns:
        percentiles[column] = np.percentile(data[column], np.arange(0, 101, 1))  # Calculate percentiles from 0 to 100

    return percentiles

def find_percentile(time, setup_name, percentiles):
    if setup_name not in percentiles:
        raise ValueError(f"Setup name '{setup_name}' not found in the data.")
    
    setup_percentiles = percentiles[setup_name]
    # Find the percentile for the given time
    for i in range(len(setup_percentiles) - 1):
        if setup_percentiles[i] <= time < setup_percentiles[i + 1]:
            return i
    
    return 100 if time >= setup_percentiles[-1] else 0  # Return 100 if time is greater than max percentile

def main():
    csv_file = 'fight_durations.csv'  # Replace with your CSV file path
    time = 120  # Replace with the time in ticks you want to check
    setup_name = 'std_weapons_mage'  # Replace with the setup name you want to check

    percentiles = calculate_percentiles(csv_file)
    percentile = find_percentile(time, setup_name, percentiles)

    print(f"The time {time} ticks falls in the {percentile}th percentile for the setup '{setup_name}'.")

if __name__ == "__main__":
    main()
