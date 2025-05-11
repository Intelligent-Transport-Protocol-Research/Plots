import pandas as pd
import matplotlib.pyplot as plt
import re
import sys
import os

def analyze_cpu_utilization(file_path, start_time=2):
    """
    Analyze CPU utilization from log file and create plot.
    
    Args:
        file_path (str): Path to the CSV file with CPU utilization data
        start_time (int): Start time in seconds for filtering logs
    """
    try:
        # Extract protocol info from filename
        filename = os.path.basename(file_path)
        
        # Detect protocol (quic or tcp) and its number
        if "quic" in filename.lower():
            protocol = "quic"
            match = re.search(r"quic(\d+)", filename.lower())
            protocol_num = match.group(1) if match else ""
            color = "red"  # Red for QUIC
        elif "tcp" in filename.lower():
            protocol = "tcp"
            match = re.search(r"tcp(\d+)", filename.lower())
            protocol_num = match.group(1) if match else ""
            color = "blue"  # Blue for TCP
        else:
            protocol = "unknown"
            protocol_num = ""
            color = "green"  # Default color
        
        # Output filename
        output_filename = f"cpu_util_{protocol}{protocol_num}"
        
        # Read the file
        with open(file_path, "r") as f:
            lines = f.readlines()

        # Extract CPU utilization values from each line
        cpu_data = []
        time_counter = 0  # Assuming logs are recorded every second

        for line in lines:
            # Use regex to find CPU utilization percentage
            match = re.search(r"Total CPU Utilization:\s*([\d.]+)%", line)
            if match:
                cpu_usage = float(match.group(1))  # Extract CPU utilization as float
                cpu_data.append((time_counter, cpu_usage))
                time_counter += 1  # Increment the time for each line

        # Convert extracted data to a DataFrame
        cpu_df = pd.DataFrame(cpu_data, columns=["Time (s)", "CPU Utilization (%)"])

        # Filter logs where time is >= start_time
        filtered_cpu_df = cpu_df[cpu_df["Time (s)"] >= start_time]

        # Plot CPU Utilization over time
        plt.figure(figsize=(10, 5))
        plt.plot(filtered_cpu_df["Time (s)"], filtered_cpu_df["CPU Utilization (%)"], 
                 marker='o', linestyle='-', color=color)

        # Labels and title
        plt.xlabel("Time (seconds)")
        plt.ylabel("CPU Utilization (%)")
        plt.title(f"CPU {protocol}{protocol_num} Utilization Over Time (Starting from {start_time} seconds)")
        plt.grid(True)
        plt.savefig(output_filename)
        plt.close()
        
        print(f"Plot saved as {output_filename}")
        
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python cpu_util_script.py <path_to_csv_file> [start_time]")
    else:
        file_path = sys.argv[1]
        start_time = int(sys.argv[2]) if len(sys.argv) > 2 else 2  # Default start time is 2
        analyze_cpu_utilization(file_path, start_time)