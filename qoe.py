import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import re

def calculate_qoe(file_path, bin_size=1):
    """
    Calculate QoE metrics from dash log data and generate plots
    
    Args:
        file_path: Path to the CSV file containing dash logs
        bin_size: Size of bins in seconds (default: 1)
    """
    try:
        # Extract protocol and number from file path
        if '\\' in file_path:
            # Windows path
            path_parts = file_path.split('\\')
        else:
            # Unix path
            path_parts = file_path.split('/')
            
        # Find the part containing quic or tcp
        protocol = None
        protocol_num = None
        for part in path_parts:
            if 'quic' in part.lower():
                protocol = 'quic'
                match = re.search(r'quic(\d+)', part.lower())
                if match:
                    protocol_num = match.group(1)
                break
            elif 'tcp' in part.lower():
                protocol = 'tcp'
                match = re.search(r'tcp(\d+)', part.lower())
                if match:
                    protocol_num = match.group(1)
                break
        
        if not protocol or not protocol_num:
            print("Warning: Could not detect protocol type from path. Using default naming.")
            protocol = "unknown"
            protocol_num = ""
        
        # Set color based on protocol
        plot_color = 'red' if protocol == 'quic' else 'blue'
        
        # Output filename
        output_filename = f"qoe_{protocol}{protocol_num}"
        
        # Load data
        df = pd.read_csv(file_path)
        
        # Parameters
        max_bitrate = 698834
        p = max_bitrate
        c = 1
        
        # Convert timestamp to seconds (if not already in seconds)
        df['ts'] = df['ts'] - df['ts'].min()  # Normalize timestamps to start from 0
        
        # Create bins
        df['bin'] = (df['ts'] // bin_size).astype(int)
        
        # Group by bin and compute metrics
        binned_data = df.groupby('bin').agg(
            total_stall_time=('videoBufferLength', lambda x: np.sum(x <= 1) / len(x) * bin_size),
            average_bitrate=('videoBitrate', 'mean'),
            quality_switches=('videoBitrate', lambda x: np.sum(np.abs(np.diff(x))))
        ).reset_index()
        
        # Compute QoE for each bin
        binned_data['QoE'] = (
            binned_data['average_bitrate']
            - p * binned_data['total_stall_time']
            - c * binned_data['quality_switches']
        )
        
        # Print average & median QoE
        mean_qoe = binned_data['QoE'].mean()
        median_qoe = binned_data['QoE'].median()
        print(f"Average QoE across all bins: {mean_qoe:.2f}")
        print(f"Median QoE across all bins:  {median_qoe:.2f}")
        
        # Plot QoE over time
        plt.figure(figsize=(10, 6))
        plt.plot(binned_data['bin'] * bin_size, binned_data['QoE'], 
                 label='QoE', marker='o', color=plot_color)
        plt.xlabel('Time (seconds)')
        plt.ylabel('QoE')
        plt.title(f'QoE Over Time ({bin_size} sec)({protocol}{protocol_num})')
        plt.legend()
        plt.grid()
        plt.savefig(output_filename)
        print(f"Plot saved as {output_filename}")
        plt.close()
        
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
        
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python qoe_script.py <path_to_csv_file> [bin_size]")
    else:
        file_path = sys.argv[1]
        bin_size = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        calculate_qoe(file_path, bin_size)