import ParseTegrastats as tegra
import numpy as np
import pandas as pd
import random
import streamlit as st
import time

# initialize dataframe
df = pd.DataFrame(columns=tegra.column_names)

st.set_page_config(layout="wide")
progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()

left_col, right_col = st.columns(2)
with left_col:
    st.subheader("CPU & Chip Temperatures", text_alignment="center")
    top_left = st.empty()
    st.subheader("GPU Temperature", text_alignment="center")
    middle_left = st.empty()
    st.subheader("CPU Core Utilization", text_alignment="center")
    bottom_left = st.empty()

with right_col:
    st.subheader("Power Consumption", text_alignment="center")
    top_right = st.empty()
    st.subheader("GPU Utilization", text_alignment="center")
    middle_right = st.empty()
    st.subheader("RAM Utilization", text_alignment="center")
    bottom_right = st.empty()

# Generate initial lists
line = tegra.random_generator()
parsed_line = tegra.parse_tegrastats(line)
tegra.update_DataFrame(df, new_row=parsed_line)

cpu_chip_temps = df[["Temp CPU (C)", "Temp SOC2 (C)", "Temp SOC0 (C)", "Temp TJ (C)", "Temp SOC1 (C)"]]
gpu_temp = df["Temp GPU (C)"]
gpu_util = df["GPU Util (%)"]
ram_used, ram_total = df["RAM Used (MB)"], df["RAM Total (MB)"]
ram_util = 100 * ram_used / ram_total

num_cores = 6
core_data = df["CPU Core Utilizations (%)"]
core_split = pd.DataFrame(core_data, columns=[f'Core {i}' for i in range(1, num_cores+1)])

power_consumps = df[["VDD_IN Current (mW)", "VDD_CPU_GPU_CV Current (mW)", "VDD_SOC Current (mW)"]]

top_left.line_chart(
        cpu_chip_temps,
        x_label="time (s)",
        y_label="temperature (C)",
        y=["Temp CPU (C)", "Temp SOC2 (C)", "Temp SOC0 (C)", "Temp TJ (C)", "Temp SOC1 (C)"]
        )
middle_left.line_chart(gpu_temp, x_label="time (s)", y_label="temperature (C)")
bottom_left.line_chart(
        core_split,
        x_label="time (s)",
        y_label="utilization (%)",
        y=[f'Core {i}' for i in range(1, num_cores+1)]
        )

top_right.line_chart(
        power_consumps,
        x_label="time (s)",
        y_label="power (mW)",
        y=["VDD_IN Current (mW)", "VDD_CPU_GPU_CV Current (mW)", "VDD_SOC Current (mW)"]
        )
middle_right.line_chart(gpu_util, x_label="time (s)", y_label="utilization (%)")
bottom_right.line_chart(ram_util, x_label="time (s)", y_label="utilization (%)")

for i in range(1, 201):
    line = tegra.random_generator()
    parsed_line = tegra.parse_tegrastats(line)
    tegra.update_DataFrame(df, new_row=parsed_line)

    cpu_chip_temps = df[["Temp CPU (C)", "Temp SOC2 (C)", "Temp SOC0 (C)", "Temp TJ (C)", "Temp SOC1 (C)"]]
    gpu_temp = df["Temp GPU (C)"]
    gpu_util = df["GPU Util (%)"]
    ram_used, ram_total = df["RAM Used (MB)"], df["RAM Total (MB)"]
    ram_util = 100 * ram_used / ram_total

    num_cores = 6
    core_data = df["CPU Core Utilizations (%)"]
    core_split = pd.DataFrame(core_data, columns=[f'Core {i}' for i in range(1, num_cores+1)])

    power_consumps = df[["VDD_IN Current (mW)", "VDD_CPU_GPU_CV Current (mW)", "VDD_SOC Current (mW)"]]

    top_left.line_chart(
            cpu_chip_temps,
            x_label="time (s)",
            y_label="temperature (C)",
            y=["Temp CPU (C)", "Temp SOC2 (C)", "Temp SOC0 (C)", "Temp TJ (C)", "Temp SOC1 (C)"]
            )
    middle_left.line_chart(gpu_temp, x_label="time (s)", y_label="temperature (C)")
    bottom_left.line_chart(
            core_split,
            x_label="time (s)",
            y_label="utilization (%)",
            y=[f'Core {i}' for i in range(1, num_cores+1)]
            )

    top_right.line_chart(
            power_consumps,
            x_label="time (s)",
            y_label="power (mW)",
            y=["VDD_IN Current (mW)", "VDD_CPU_GPU_CV Current (mW)", "VDD_SOC Current (mW)"]
            )
    middle_right.line_chart(gpu_util, x_label="time (s)", y_label="utilization (%)")
    bottom_right.line_chart(ram_util, x_label="time (s)", y_label="utilization (%)")

    # Scale progress to show 0-100%
    progress = i // 2
    status_text.text(f"{progress}% complete")
    progress_bar.progress(progress)
    time.sleep(1)

progress_bar.empty()
st.button("Rerun")
