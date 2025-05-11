import matplotlib.pyplot as plt
from datetime import datetime
import re
import csv
from statistics import median

# Function to parse log and extract timestamp and cwnd
def parse_log(log_lines):
    cwnd_data = []
    pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6}).*cwnd: (\d+)"
    
    for line in log_lines:
        # If the CSV has a single column, line is a string; if multiple, line is a list
        log_line = line[0] if isinstance(line, list) else line
        match = re.search(pattern, log_line)
        if match:
            timestamp = datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S.%f")
            cwnd = int(match.group(2))
            cwnd_data.append((timestamp, cwnd))
    
    return cwnd_data

# Function to aggregate cwnd by second (compute median)
def aggregate_by_second(cwnd_data):
    if not cwnd_data:
        return [], []
    
    # Find the earliest timestamp to normalize time to start at 0
    base_time = cwnd_data[0][0]
    
    # Dictionary to store lists of cwnd values per second
    cwnd_per_second = {}
    
    for timestamp, cwnd in cwnd_data:
        # Calculate seconds since base_time
        seconds = int((timestamp - base_time).total_seconds())
        if(seconds<85):
            if seconds not in cwnd_per_second:
                cwnd_per_second[seconds] = []
            cwnd_per_second[seconds].append(cwnd)
    
    # Compute median for each second
    seconds = sorted(cwnd_per_second.keys())
    cwnd_medians = [median(cwnd_per_second[sec]) for sec in seconds]
    
    return seconds, cwnd_medians

# Read the CSV file
log_lines = []
try:
    with open('quic38_cwnd.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        log_lines = [row for row in reader if row]  # Skip empty rows
except FileNotFoundError:
    print("Error: The file 'quic38_cwnd.csv' was not found.")
    exit(1)
except Exception as e:
    print(f"Error reading the file: {e}")
    exit(1)

# Parse and aggregate data
cwnd_data = parse_log(log_lines)
if not cwnd_data:
    print("No valid cwnd data found in the file.")
    exit(1)

seconds, cwnd_medians = aggregate_by_second(cwnd_data)

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(seconds, cwnd_medians, 'b-', label='Median Congestion Window')
plt.title('QUIC Congestion Window (cwnd) Over Time')
plt.xlabel('Time (seconds)')
plt.ylabel('Median cwnd')
plt.grid(True)
plt.legend()

# Save the plot to a file
plt.savefig('quic_cwnd_plot.png')
plt.close()
print("Plot saved as 'cwnd_plot.png'")