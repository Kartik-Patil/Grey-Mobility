import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
#from data_generator import AmbulanceDataGenerator
#gen = AmbulanceDataGenerator()
df = pd.read_csv("data/simulated_patient.csv")

plt.figure(figsize=(12,8))
plt.plot(df["time"], df["spo2"])
plt.title("SpO2 Signal with Artifacts and Distress")
plt.show()