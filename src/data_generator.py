# src/data_generator.py

import numpy as np
import pandas as pd


class AmbulanceDataGenerator:
    def __init__(self, duration_minutes=30, sampling_rate=1, seed=42):
        np.random.seed(seed)
        self.duration_seconds = duration_minutes * 60
        self.sampling_rate = sampling_rate
        self.time = np.arange(0, self.duration_seconds, sampling_rate)

    def generate_baseline(self):
        hr = np.random.normal(80, 5, len(self.time))
        spo2 = np.random.normal(98, 1, len(self.time))
        bp_sys = np.random.normal(120, 8, len(self.time))
        bp_dia = np.random.normal(80, 5, len(self.time))
        motion = np.random.normal(0.2, 0.05, len(self.time))

        return hr, spo2, bp_sys, bp_dia, motion

    def inject_distress(self, hr, spo2, bp_sys):
        # gradual hypoxia after 15 minutes
        start = 15 * 60
        spo2[start:] -= np.linspace(0, 10, len(spo2[start:]))

        # shock scenario: BP drop
        bp_sys[start:] -= np.linspace(0, 25, len(bp_sys[start:]))

        # compensatory HR increase
        hr[start:] += np.linspace(0, 30, len(hr[start:]))

        return hr, spo2, bp_sys

    def inject_motion_artifacts(self, spo2, hr, motion):
        for _ in range(10):
            idx = np.random.randint(0, len(spo2) - 5)
            spo2[idx:idx+3] -= np.random.uniform(10, 20)  # fake drop
            hr[idx:idx+2] += np.random.uniform(20, 40)    # fake spike
            motion[idx:idx+3] += np.random.uniform(0.5, 1.0)

        return spo2, hr, motion

    def inject_missing_segments(self, df):
        for _ in range(3):
            idx = np.random.randint(0, len(df) - 10)
            df.iloc[idx:idx+5] = np.nan
        return df

    def generate(self):
        hr, spo2, bp_sys, bp_dia, motion = self.generate_baseline()

        hr, spo2, bp_sys = self.inject_distress(hr, spo2, bp_sys)
        spo2, hr, motion = self.inject_motion_artifacts(spo2, hr, motion)

        df = pd.DataFrame({
            "time": self.time,
            "hr": hr,
            "spo2": spo2,
            "bp_sys": bp_sys,
            "bp_dia": bp_dia,
            "motion": motion
        })

        df = self.inject_missing_segments(df)

        return df