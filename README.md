# Accumulated-charge-2024-plotter-pro
Accumulated charge 2024 plotter pro
This script processes text files containing daily charge delivery data
from CEBAF to compute and visualize the cumulative charge de-
posited on the photocathode, identifying resets via zero entries in
the charge column. For each .txt file in the specified directory, the
data is read into a DataFrame, sorted by date, and cleaned by remov-
ing duplicates. A running sum of the last non-zero charge values
before each reset is computed to quantify the accumulated charge.
The script then generates a dual-axis plot showing individual daily
charge deliveries alongside cumulative charge, with annotated mark-
ers for reset events. Each plot is saved with a filename derived from
the original data file.
