import ParseTegrastats as tegra
import numpy as np
import pandas as pd
import streamlit as st
import time

# Initialize global dataframe using your module's headers
df = pd.DataFrame(columns=tegra.column_names)

st.set_page_config(layout="wide")
progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()

# --- LAYOUT DEFINITION ---
left_col, right_col = st.columns(2)
with left_col:
    st.markdown("<h3 style='text-align: center;'>CPU & Chip Temperatures</h3>", unsafe_allow_html=True)
    top_left = st.empty()
    st.markdown("<h3 style='text-align: center;'>GPU Temperature</h3>", unsafe_allow_html=True)
    middle_left = st.empty()
    st.markdown("<h3 style='text-align: center;'>CPU Core Utilization</h3>", unsafe_allow_html=True)
    bottom_left = st.empty()

with right_col:
    st.markdown("<h3 style='text-align: center;'>Power Consumption</h3>", unsafe_allow_html=True)
    top_right = st.empty()
    st.markdown("<h3 style='text-align: center;'>GPU Utilization</h3>", unsafe_allow_html=True)
    middle_right = st.empty()
    st.markdown("<h3 style='text-align: center;'>RAM Utilization</h3>", unsafe_allow_html=True)
    bottom_right = st.empty()


def render_dashboard_charts():
    """Extracts dataframe slices and forces UI element updates securely."""
    cpu_chip_temps = df[["Temp CPU (C)", "Temp SOC2 (C)", "Temp SOC0 (C)", "Temp TJ (C)", "Temp SOC1 (C)"]]
    gpu_temp = df["Temp GPU (C)"]
    gpu_util = df["GPU Util (%)"]

    ram_used, ram_total = df["RAM Used (MB)"], df["RAM Total (MB)"]
    ram_util = 100 * ram_used / ram_total

    num_cores = 6
    core_data = df["CPU Core Utilizations (%)"]
    # Unpack nested list structure gracefully via .tolist()
    core_split = pd.DataFrame(core_data.tolist(), columns=[f'Core {i}' for i in range(1, num_cores+1)])

    power_consumps = df[["VDD_IN Current (mW)", "VDD_CPU_GPU_CV Current (mW)", "VDD_SOC Current (mW)"]]

    # Render Left Columns
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

    # Render Right Columns
    top_right.line_chart(
        power_consumps,
        x_label="time (s)",
        y_label="power (mW)",
        y=["VDD_IN Current (mW)", "VDD_CPU_GPU_CV Current (mW)", "VDD_SOC Current (mW)"]
    )
    middle_right.line_chart(gpu_util, x_label="time (s)", y_label="utilization (%)")
    bottom_right.line_chart(ram_util, x_label="time (s)", y_label="utilization (%)")


# --- GENERATE INITIAL SEED DATA ---
line = tegra.random_generator()
parsed_line = tegra.parse_tegrastats(line)
tegra.update_DataFrame(df, new_row=parsed_line)
render_dashboard_charts()

# --- LIVE REFRESH LOOP ---
for i in range(1, 201):
    line = tegra.random_generator()
    parsed_line = tegra.parse_tegrastats(line)
    tegra.update_DataFrame(df, new_row=parsed_line)

    # Refresh charts with extracted method
    render_dashboard_charts()

    # Progress Calculation (0-100%)
    progress = i // 2
    status_text.text(f"{progress}% complete")
    progress_bar.progress(progress)
    time.sleep(1)

progress_bar.empty()
st.button("Rerun")
