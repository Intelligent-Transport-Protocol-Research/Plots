# Plots Repository

This repository contains Python scripts for visualizing and analyzing performance metrics related to network protocols (TCP and QUIC) from CSV log files. Each script generates plots to help analyze metrics such as CPU utilization, memory pressure, congestion window, and Quality of Experience (QoE). Below is a description of each script and instructions on how to run them.

Scritps to log the values that the script needs is present in different repository named LoggingScripts

## Prerequisites
- Python 3.x
- Required libraries: `pandas`, `matplotlib`, `numpy`. Install them using:
  ```bash
  pip install pandas matplotlib numpy
  ```
- CSV files containing the relevant log data (e.g., `tcp38_cwnd.csv`).

## Scripts

### 1. `pressure_cpuAndMem.py`
**Purpose**: Visualizes CPU and Memory pressure (avg10 and avg60 metrics) over time from a CSV file. It generates two plots: one for CPU pressure and one for Memory pressure.

**Run Command**:
```bash
python pressure_cpuAndMem.py <path_to_csv_file>
```
- **Argument**: `<path_to_csv_file>` is the path to a CSV file containing CPU and Memory pressure data (e.g., `data2/tcp13_pressure.csv`).
- **Output**: Two PNG files (e.g., `quic_cpu_pressure4.png`, `quic_mem_pressure4.png`) based on the protocol (QUIC/TCP) and number extracted from the filename.

### 2. `cwnd_tcp.py`
**Purpose**: Plots the median TCP congestion window (`snd_wnd`) over time from a CSV file.

**Run Command**:
```bash
python cwnd_tcp.py
```
- **Argument**: No command-line argument is required. The script reads from a hardcoded file `tcp38_cwnd.csv`.
- **Output**: A PNG file named `tcp_cwnd_plot.png`.

### 3. `cpu_utilization_plot.py`
**Purpose**: Analyzes and plots CPU utilization over time from a log file, filtering data starting from a specified time (default: 2 seconds).

**Run Command**:
```bash
python cpu_utilization_plot.py <path_to_log_file> [start_time]
```
- **Arguments**:
  - `<path_to_log_file>`: Path to a log file containing CPU utilization data (e.g., `data2/tcp13.csv`).
  - `[start_time]` (optional): Start time in seconds for filtering logs (default: 2).
- **Output**: A PNG file (e.g., `cpu_util_quic4.png`) based on the protocol and number in the filename.

### 4. `cwnd_quic.py`
**Purpose**: Plots the median QUIC congestion window (`cwnd`) over time from a CSV file containing log data.

**Run Command**:
```bash
python cwnd_quic.py
```
- **Argument**: No command-line argument is required. The script reads from a hardcoded file `quic38_cwnd.csv`.
- **Output**: A PNG file named `quic_cwnd_plot.png`.

### 5. `pressureAll.py`
**Purpose**: Visualizes CPU, Memory, and IO pressure (avg10 and avg60 metrics) over time from a CSV file. It generates three plots: one each for CPU, Memory, and IO pressure.

**Run Command**:
```bash
python pressureAll.py <path_to_csv_file>
```
- **Argument**: `<path_to_csv_file>` is the path to a CSV file containing CPU, Memory, and IO pressure data (e.g., `data2/tcp13_pressure.csv`).
- **Output**: Three PNG files (e.g., `quic_cpu_pressure4.png`, `quic_mem_pressure4.png`, `quic_io_pressure4.png`) based on the protocol and number.

### 6. `qoe.py`
**Purpose**: Calculates and plots Quality of Experience (QoE) metrics over time from a CSV file containing dash log data, using a specified bin size (default: 1 second) and OBOE formula. Modify the Maximum bitrate in accordance to the OBOE formula.

*NOTE*: delete the first log entry from dash_logs.csv, sometimes that entry has wrong timestamp that leads to distorted plots.
**Run Command**:
```bash
python qoe.py <path_to_csv_file> [bin_size]
```
- **Arguments**:
  - `<path_to_csv_file>`: Path to a CSV file containing dash log data (e.g., `data2/dash_logs.csv`).
  - `[bin_size]` (optional): Size of time bins in seconds (default: 1).
- **Output**: A PNG file (e.g., `qoe_quic4.png`) and prints average and median QoE values.

## Notes
- Ensure the CSV/log files are in the correct format as expected by each script (e.g., columns like `Timestamp`, `CPU`, `Memory`, `snd_wnd`, etc.).
- The scripts automatically detect the protocol (QUIC or TCP) and number from the input filename for naming output files.
- For `cwnd_tcp.py` and `cwnd_quic.py`, update the hardcoded file paths in the scripts if using different CSV files.
