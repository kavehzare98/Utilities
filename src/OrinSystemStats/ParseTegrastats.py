import csv
import random
import re
from datetime import datetime

column_names = ["Timestamp", "RAM Used (MB)", "RAM Total (MB)", "LFB Count",
    "LFB Size (MB)", "SWAP Used (MB)", "SWAP Total (MB)",
    "CPU Core Utilizations (%)", "CPU Core Clocks (MHz)",   "EMC Util (%)",
    "GPU Util (%)", "GPU Clock (MHz)", "NVDEC Active", "NVJPG Active",
    "NVJPG1 Active", "VIC Active", "OFA Active", "APE Clock (MHz)",
    "Temp CPU (C)", "Temp SOC2 (C)", "Temp SOC0 (C)", "Temp GPU (C)",
    "Temp TJ (C)", "Temp SOC1 (C)", "VDD_IN Current (mW)",
    "VDD_CPU_GPU_CV Current (mW)", "VDD_SOC Current (mW)" ]

def parse_tegrastats(line: str):
    data = []

    time_stamp = re.match(r"^(\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2})", line)
    if time_stamp:
        data.append(time_stamp.group(1))

    ram_util = re.search(r"RAM (\d+)/(\d+)MB", line)
    if ram_util:
        ram_used = int(ram_util.group(1))
        ram_avail = int(ram_util.group(2))
        data.append(ram_used)
        data.append(ram_avail)

    largest_free_block = re.search(r"lfb (\d+)x(\d+)MB", line)
    if largest_free_block:
        num_lfbs = int(largest_free_block.group(1))
        size_lfb = int(largest_free_block.group(2))
        data.append(num_lfbs)
        data.append(size_lfb)

    swap = re.search(r"SWAP (\d+)/(\d+)MB", line)
    if swap:
        swap_used = int(swap.group(1))
        swap_avail = int(swap.group(2))
        data.append(swap_used)
        data.append(swap_avail)

    cpu_util = re.search(r"CPU \[(.*?)\]", line)
    if cpu_util:
        core_data = cpu_util.group(1)
        core_split = core_data.split(",")

        core_utils = [int(core.split("%@")[0]) for core in core_split]
        core_clk_mhz = [int(core.split("%@")[1]) for core in core_split]
        data.append(core_utils)
        data.append(core_clk_mhz)

    emc_freq = re.search(r"EMC_FREQ (\d+)%@(\d+)", line)
    if emc_freq:
        emc_used_percent = int(emc_freq.group(1))
        emc_clk_mhz = int(emc_freq.group(2))
        data.append(emc_used_percent)


    gpu_util = re.search(r"GR3D_FREQ (\d+)%@\[(\d+)\]", line)
    if gpu_util:
        gpu_util_percent = int(gpu_util.group(1))
        gpu_clk_mhz = int(gpu_util.group(2))
        data.append(gpu_util_percent)
        data.append(gpu_clk_mhz)

    status = re.search(r"NVDEC (\w+) NVJPG (\w+) NVJPG1 (\w+) VIC (\w+) OFA (\w+)", line)
    if status:
        nvdec = 0 if status.group(1) == "off" else 1
        nvjpg = 0 if status.group(2) == "off" else 1
        nvjpg1 = 0 if status.group(3) == "off" else 1
        vic = 0 if status.group(4) == "off" else 1
        ofa = 0 if status.group(5) == "off" else 1
        data.append(nvdec)
        data.append(nvjpg)
        data.append(nvjpg1)
        data.append(vic)
        data.append(ofa)

    ape = re.search(r"APE (\d+)", line)
    if ape:
        ape_num = int(ape.group(1))
        data.append(ape_num)

    temps = re.search(r"cpu@(\d+\.\d+)C soc2@(\d+\.\d+)C soc0@(\d+\.\d+)C gpu@(\d+\.\d+)C tj@(\d+\.\d+)C soc1@(\d+\.\d+)C", line)
    if temps:
        temp_cpu = float(temps.group(1))
        temp_soc2 = float(temps.group(2))
        temp_soc0 = float(temps.group(3))
        temp_gpu = float(temps.group(4))
        temp_tj = float(temps.group(5))
        temp_soc1 = float(temps.group(6))
        data.append(temp_cpu)
        data.append(temp_soc2)
        data.append(temp_soc0)
        data.append(temp_gpu)
        data.append(temp_tj)
        data.append(temp_soc1)

    vdd_in = re.search(r"VDD_IN (\d+)mW", line)
    if vdd_in:
        vdd_in_mW = int(vdd_in.group(1))
        data.append(vdd_in_mW)

    vdd_cpu_gpu_cv = re.search(r"VDD_CPU_GPU_CV (\d+)mW", line)
    if vdd_cpu_gpu_cv:
        vdd_cpu_gpu_cv_mW = int(vdd_cpu_gpu_cv.group(1))
        data.append(vdd_cpu_gpu_cv_mW)

    vdd_soc = re.search(r"VDD_SOC (\d+)mW", line)
    if vdd_soc:
        vdd_soc_mW = int(vdd_soc.group(1))
        data.append(vdd_soc_mW)

    return data

def random_generator() -> str:
    now = datetime.now()
    time = now.strftime("%m-%d-%Y %H:%M:%S")
    max_temp = 80 # degrees Celsius

    cpu = max_temp * random.random()
    gpu = max_temp * random.random()
    soc0 = max_temp * random.random()
    soc1 = max_temp * random.random()
    soc2= max_temp * random.random()
    tj = max_temp * random.random()

    sample = f"{time} RAM {random.randint(1,7607)}/7607MB (lfb {random.randint(1,5)}x4MB) SWAP 0/3804MB (cached 0MB) CPU [{random.randint(0,100)}%@729,{random.randint(0,100)}%@729,{random.randint(0,100)}%@729,{random.randint(0,100)}%@729,{random.randint(0,100)}%@729,{random.randint(0,100)}%@729] EMC_FREQ 0%@2133 GR3D_FREQ 0%@[305] NVDEC off NVJPG off NVJPG1 off VIC off OFA off APE 200 cpu@{cpu}C soc2@{soc2}C soc0@{soc0}C gpu@{gpu}C tj@{tj}C soc1@{soc1}C VDD_IN {random.randint(1000,12000)}mW/4647mW VDD_CPU_GPU_CV {random.randint(1000,12000)}mW/520mW VDD_SOC {random.randint(1000,12000)}mW/1442mW"
    return sample

def update_DataFrame(df, new_row):
    df.loc[len(df)] = new_row

def main():
    file_name = "actual_log.txt"
    parsed_file_content = [column_names]

    with open(file_name, "r") as f:
        while True:
            line = f.readline()
            if not line:
                break
            parsed_line = parse_tegrastats(line)
            parsed_file_content.append(parsed_line)


    with open('data.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        for row in parsed_file_content:
            csv_writer.writerow(row)

if __name__ == "__main__":
    main()
