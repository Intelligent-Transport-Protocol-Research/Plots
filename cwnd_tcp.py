import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Load the CSV data
data = pd.read_csv('tcp38_cwnd.csv')

# Group by timestamp and calculate the median snd_cwnd for each timestamp
median_data = data.groupby('timestamp')['snd_wnd'].median().reset_index()

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot((median_data['timestamp']-72), median_data['snd_wnd'], color='blue', linewidth=2, label='Congestion Window')

# Customize the plot
plt.xlabel('Timestamp (seconds)')
plt.ylabel('snd_cwnd (bytes)')
plt.title('TCP Congestion Window Over Time')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

# Format y-axis labels for better readability
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))

# Save the plot
plt.savefig('tcp_cwnd_plot.png')