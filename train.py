from src.data_generator import AmbulanceDataGenerator

gen = AmbulanceDataGenerator()
df = gen.generate()

print(df.head())
df.to_csv("data/simulated_patient.csv", index=False)