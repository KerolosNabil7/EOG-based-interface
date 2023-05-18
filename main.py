# Imports
import os
import statistics
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import signal
from scipy.signal import butter, filtfilt
import preprocessing as pp

# Read Files
path = "3-class"

def read_sig(folder_path):
    signals_f = []
    signals_name_f = []
    channel_f = []
    list_of_classes = ["asagi", "kirp", "sag", "sol", "yukari"]  # The classes name we interested in [down, blink, right, left, up]
    files = os.listdir(path)

    for file in files:
        temp_sig = []
        for class_name in list_of_classes:
            if file.startswith(class_name):
                name = file.split('.')
                channel_f.append(name[0][-1])  # list ['h' , 'v' , 'h' ,'v' , .....]
                with open(path + "\\" + file, 'r') as f:
                    for line in f:
                        s = line.strip()  # Remove the newline character
                        temp_sig.append(int(s))
                signals_f.append(temp_sig)  # list of signals N x 251 where N is number of signals in 3-class file
                signals_name_f.append(class_name)  # signal class ("asagi", "kirp", "sag", "sol", "yukari")
                break
    return signals_f, signals_name_f, channel_f


signals, signals_name, channel = read_sig(path)

# preprocessing
filtered_signals = []
resampled_signals = []
removedDC_component_signals = []
for i in range(len(signals)):
    # 1- Signals Filtering
    filtered_signals.append(pp.butter_bandpass_filter(signals[i], Low_Cutoff=0.5, High_Cutoff=20.0, Sampling_Rate=176, order=2))
    # 2- Signals resampling
    resampled_signals.append(pp.Resampling(filtered_signals[i]))
    # 3- Signals DC removal
    removedDC_component_signals.append((pp.DC_removal(resampled_signals[i])))


# Concatenation
signals_concat = []
for i in range(0, len(signals), 2):
    signals_concat.append(removedDC_component_signals[i]+removedDC_component_signals[i+1])


# Feature Extraction in Time Domain

