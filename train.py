from src.data_generator import AmbulanceDataGenerator
from src.artifact_handler import ArtifactHandler
import matplotlib.pyplot as plt

# Generate data
gen = AmbulanceDataGenerator()
df_raw = gen.generate()

# Clean data
handler = ArtifactHandler()
df_clean = handler.clean(df_raw)

# Plot comparison
plt.figure(figsize=(14,6))
plt.plot(df_raw["time"], df_raw["spo2"], label="Raw", alpha=0.5)
plt.plot(df_clean["time"], df_clean["spo2"], label="Cleaned", linewidth=2)
plt.title("SpO2 Before vs After Artifact Removal")
plt.xlabel("Time")
plt.ylabel("SpO2")
plt.legend()
plt.show()