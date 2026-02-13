import numpy as np
import pandas as pd


class AmbulanceDataGenerator:
    """
    Generates synthetic ambulance patient vital data
    with:
    - Normal transport phase
    - Gradual distress scenario
    - Motion-correlated artifacts
    - Missing data segments
    """

    def __init__(self, duration_minutes=30, sampling_rate=1, seed=42):
        np.random.seed(seed)

        self.duration_seconds = duration_minutes * 60
        self.sampling_rate = sampling_rate
        self.time = np.arange(0, self.duration_seconds, sampling_rate)

    # --------------------------------------------------
    # BASELINE SIGNAL GENERATION
    # --------------------------------------------------

    def generate_baseline(self):
        hr = np.random.normal(80, 5, len(self.time))
        spo2 = np.random.normal(98, 1, len(self.time))
        bp_sys = np.random.normal(120, 8, len(self.time))
        bp_dia = np.random.normal(80, 5, len(self.time))
        motion = np.random.normal(0.2, 0.05, len(self.time))

        # Clip to physiological limits
        spo2 = np.clip(spo2, 85, 100)
        hr = np.clip(hr, 40, 180)
        bp_sys = np.clip(bp_sys, 70, 200)
        bp_dia = np.clip(bp_dia, 40, 120)

        return hr, spo2, bp_sys, bp_dia, motion

    # --------------------------------------------------
    # DISTRESS INJECTION (Non-linear realistic decline)
    # --------------------------------------------------

    def inject_distress(self, hr, spo2, bp_sys):
        start = 15 * 60  # 15-minute mark

        # Non-linear hypoxia progression
        decay = np.linspace(0, 1, len(spo2[start:]))
        spo2[start:] -= 10 * (decay ** 1.5)
        spo2[start:] += np.random.normal(0, 0.5, len(spo2[start:]))

        # Shock: BP drop
        bp_sys[start:] -= 25 * (decay ** 1.2)
        bp_sys[start:] += np.random.normal(0, 1.0, len(bp_sys[start:]))

        # Compensatory tachycardia
        hr[start:] += 30 * (decay ** 1.3)
        hr[start:] += np.random.normal(0, 1.5, len(hr[start:]))

        # Re-clip
        spo2 = np.clip(spo2, 70, 100)
        hr = np.clip(hr, 40, 180)
        bp_sys = np.clip(bp_sys, 60, 200)

        return hr, spo2, bp_sys

    # --------------------------------------------------
    # MOTION ARTIFACT INJECTION
    # --------------------------------------------------

    def inject_motion_artifacts(self, spo2, hr, motion):
        for _ in range(12):
            idx = np.random.randint(0, len(spo2) - 5)

            # Motion spike
            motion[idx:idx+3] += np.random.uniform(0.6, 1.2)

            # Short false SpO2 drop
            spo2[idx:idx+3] -= np.random.uniform(10, 20)

            # HR spike from vibration
            hr[idx:idx+2] += np.random.uniform(20, 40)

        spo2 = np.clip(spo2, 60, 100)
        hr = np.clip(hr, 40, 200)

        return spo2, hr, motion

    # --------------------------------------------------
    # MISSING DATA SIMULATION
    # --------------------------------------------------

    def inject_missing_segments(self, df):
        for _ in range(3):
            idx = np.random.randint(0, len(df) - 10)
            df.iloc[idx:idx+5] = np.nan
        return df

    # --------------------------------------------------
    # FULL PIPELINE
    # --------------------------------------------------

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