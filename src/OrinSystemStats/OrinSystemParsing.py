import csv
from typing import Any

def open_and_read_file(file: str) -> [str]:
    raw_content = []
    with open(file, "r") as f:
        while True:
            line = f.readline()
            if not line:
                break
            raw_content.append(line)
    return raw_content

def pre_process_data(data: [str], column_names: [str]) -> [[str]]:
    unprocessed_data = [column_names]

    for line in data:
        line = line.strip()
        line_split = line.split(" ")
        raw_data = [line_split[1], line_split[3], line_split[5], line_split[9],
                    line_split[11], line_split[13], line_split[14],
                    line_split[15], line_split[16], line_split[17]]
        unprocessed_data.append(raw_data)

    return unprocessed_data

def process_data(pre_processed_data: [str]) -> Any:
    processed_data = [pre_processed_data[0]]
    for row in pre_processed_data[1:]:
        # RAM Utilization
        ram_util_raw = row[0][:-2]
        ram_util_split = ram_util_raw.split("/")
        ram_util_numer = float(ram_util_split[0])
        ram_util_denom = float(ram_util_split[1])
        ram_util_percent = 100 * ram_util_numer / ram_util_denom

        # Largest Free Block (lfb)
        lfb_raw = row[1].split("x")
        lfb_num = float(lfb_raw[0])

        # SWAP Space
        swap_raw = row[2][:-2]
        swap_split = swap_raw.split("/")
        swap_numer, swap_denom = float(swap_split[0]), float(swap_split[1])
        swap_percent = 100 * swap_numer / swap_denom

        # CPU Core Utilization
        cpu_core_raw = row[3][1:-1]
        cpu_core_split = cpu_core_raw.split(",")
        cpu_core_utils = [float(core.split("%")[0]) for core in cpu_core_split]

        # RAM Bus Utilization
        ram_bus_util_percent = float(row[4][:-1])

        # GPU Utilization
        gpu_util_percent = float(row[5][:-1])

        # Temperatures
        temp_pom_deg_cel = float(row[6].split("@")[1][:-1])
        temp_cpu_deg_cel = float(row[7].split("@")[1][:-1])
        temp_thermal_deg_cel = float(row[8].split("@")[1][:-1])
        temp_ao_deg_cel = float(row[9].split("@")[1][:-1])

        new_row = [ram_util_percent, lfb_num, swap_percent,
                   cpu_core_utils, ram_bus_util_percent,
                   gpu_util_percent, temp_pom_deg_cel, temp_cpu_deg_cel,
                   temp_thermal_deg_cel, temp_ao_deg_cel]
        
        processed_data.append(new_row)
    return processed_data

def display_averages(data: Any) -> None:
    col_names = data[0]
    num_rows = len(data) - 1

    if num_rows <= 0:
        print("No log data available to average.")
        return

    print("\n--- SYSTEM AVERAGES ---")

    padding = 30

    for col in range(len(col_names)):
        column_values = [row[col] for row in data[1:]]

        if col == 3:
            num_cores = len(column_values[0])
            core_sums = [0.0] * num_cores

            for i in range(num_cores):
                for cores_list in column_values:
                    core_util = cores_list[i]
                    core_sums[i] += core_util

            avg_per_core = [round(c_sum / num_rows, 2) for c_sum in core_sums]
            avg_core_util = sum(avg_per_core) / num_cores

            title = f"{col_names[col]}:"
            print(f"{title:<{padding}}{avg_per_core}  =>  {avg_core_util}%")

        else:
            avg_value = sum(column_values) / num_rows

            title = f"{col_names[col]}:"

            if "Temp" in col_names[col]:
                print(f"{title:<{padding}}{avg_value:.2f}°C")
            elif "Block" in col_names[col]:
                print(f"{title:<{padding}}{avg_value:.1f} blocks")
            else:
                print(f"{title:<{padding}}{avg_value:.2f}%")

def main():

    file_name = "sample_log.txt"

    raw_content = open_and_read_file(file_name)

    column_names = ['RAM Utilization', 'Largest Free Block (lfb)',
                    'SWAP Space (RAM handling)', 'CPU Utilization by core',
                    'RAM Bus Utilization (EMC)', 'GPU Utilization',
                    'Temp POM', 'Temp CPU', 'Temp thermal', 'Temp AO']

    unprocessed_data = pre_process_data(raw_content, column_names)
    processed_data = process_data(unprocessed_data)

    with open('data.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        for row in processed_data:
            csv_writer.writerow(row)

    display_averages(processed_data)

if __name__ == "__main__":
    main()
