import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_smoothed_distributions(csv_file, labels=None):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Filter the DataFrame columns based on the provided labels
    if labels is not None:
        df = df[labels]

    # Set the plot style
    sns.set(style="whitegrid")

    # Create the plot
    plt.figure(figsize=(12, 6))

    for column in df.columns:
        sns.kdeplot(df[column], label=column, fill=False, alpha=0.7, linewidth=2)

    plt.xlabel('Fight Duration (ticks)')
    plt.ylabel('Density')
    plt.title('Fight Duration Distributions')
    plt.legend(title='Setup Names')
    plt.grid(True)
    plt.show()

# Call the function with the CSV file and specific labels
plot_smoothed_distributions('fight_durations.csv', labels=['std_weapons_mage', 'std_weapons_mage_dart'])
