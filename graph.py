from src.data_generator import AmbulanceDataGenerator
import matplotlib.pyplot as plt
import pandas as pd
df=pd.read_csv("data/simulated_patient.csv")
plt.figure(figsize=(14, 6))
plt.plot(df["time"], df["spo2"], label="SpO2")
plt.title("SpO2 Signal with Artifacts and Distress")
plt.xlabel("Time (seconds)")
plt.ylabel("SpO2")
plt.legend()
plt.show()

plt.figure(figsize=(14, 4))
plt.plot(df["motion"], label="Motion")
plt.title("Motion Signal")
plt.xlabel("Time (seconds)")
plt.legend()
plt.show()