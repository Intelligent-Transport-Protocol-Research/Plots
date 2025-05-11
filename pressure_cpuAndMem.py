import matplotlib.pyplot as plt
import pandas as pd
import sys
import os
import re

def visualize_cpu_memory_from_csv(file_path):
    """
    Visualizes CPU and Memory avg10 and avg60 from a CSV file.

    Args:
        file_path: The path to the CSV file.
    """
    try:
        # Extract the base file name without extension
        base_file_name = os.path.basename(file_path)
        
        # Determine output file prefixes based on the input file name
        if "quic" in base_file_name:
            protocol = "quic"
            # Extract number after "quic" (e.g., "quic4" -> "4")
            match = re.search(r'quic(\d+)', base_file_name)
            number = match.group(1) if match else ""
        elif "tcp" in base_file_name:
            protocol = "tcp"
            # Extract number after "tcp" (e.g., "tcp3" -> "3")
            match = re.search(r'tcp(\d+)', base_file_name)
            number = match.group(1) if match else ""
        else:
            protocol = "unknown"
            number = ""
        
        output_prefix_cpu = f"{protocol}_cpu_pressure{number}"
        output_prefix_mem = f"{protocol}_mem_pressure{number}"

        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(file_path)

        # Extract CPU and Memory data
        cpu_data = df['CPU'].str.split(' ', expand=True)
        memory_data = df['Memory'].str.split(' ', expand=True)

        # Extract avg10 and avg60 values
        cpu_avg10 = cpu_data[1].str.split('=', expand=True)[1].astype(float)
        cpu_avg60 = cpu_data[2].str.split('=', expand=True)[1].astype(float)

        memory_avg10_some = memory_data[1].str.split('=', expand=True)[1].astype(float)
        memory_avg60_some = memory_data[2].str.split('=', expand=True)[1].astype(float)
        memory_avg10_full = memory_data[5].str.split('=', expand=True)[1].astype(float)
        memory_avg60_full = memory_data[6].str.split('=', expand=True)[1].astype(float)

        # Convert timestamps to seconds starting from 1
        timestamps = pd.to_datetime(df['Timestamp'])
        seconds = (timestamps - timestamps.min()).dt.total_seconds() + 1

        # Plot CPU avg10 and avg60
        plt.figure(figsize=(10, 5))
        plt.plot(seconds, cpu_avg10, label='CPU avg10')
        plt.plot(seconds, cpu_avg60, label='CPU avg60')
        plt.xlabel('Time (seconds)')
        plt.ylabel('CPU Average')
        plt.title('CPU avg10 and avg60 Over Time')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(output_prefix_cpu)
        plt.close()

        # Plot Memory avg10 and avg60
        plt.figure(figsize=(10, 5))
        plt.plot(seconds, memory_avg10_some, label='Memory some avg10')
        plt.plot(seconds, memory_avg60_some, label='Memory some avg60')
        plt.plot(seconds, memory_avg10_full, label='Memory full avg10')
        plt.plot(seconds, memory_avg60_full, label='Memory full avg60')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Memory Average')
        plt.title('Memory avg10 and avg60 Over Time')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(output_prefix_mem)
        plt.close()

        print(f"Visualization complete. Saved as {output_prefix_cpu} and {output_prefix_mem}")

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <path_to_csv_file>")
    else:
        file_path = sys.argv[1]
        visualize_cpu_memory_from_csv(file_path)