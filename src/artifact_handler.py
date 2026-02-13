import numpy as np
import pandas as pd


class ArtifactHandler:
    def __init__(self, motion_threshold=0.6, drop_threshold=5, max_artifact_duration=4):
        self.motion_threshold = motion_threshold
        self.drop_threshold = drop_threshold
        self.max_artifact_duration = max_artifact_duration

    # ----------------------------------------
    # Detect sudden drops
    # ----------------------------------------
    def detect_sudden_drops(self, df):
        df = df.copy()
        df["spo2_diff"] = df["spo2"].diff()

        df["possible_artifact"] = (
            (df["spo2_diff"] < -self.drop_threshold) &
            (df["motion"] > self.motion_threshold)
        )

        return df

    # ----------------------------------------
    # Remove short duration artifacts
    # ----------------------------------------
    def remove_short_spikes(self, df):
        df = df.copy()

        artifact_indices = df[df["possible_artifact"]].index

        for idx in artifact_indices:
            window = df.loc[idx:idx + self.max_artifact_duration]

            if window["possible_artifact"].sum() <= self.max_artifact_duration:
                df.loc[idx:idx + self.max_artifact_duration, "spo2"] = np.nan

        return df

    # ----------------------------------------
    # Handle missing data
    # ----------------------------------------
    def handle_missing(self, df):
        df = df.copy()

        # Interpolate small gaps
        df["spo2"] = df["spo2"].interpolate(limit=5)

        # Forward fill remaining small NaNs
        df["spo2"] = df["spo2"].fillna(method="ffill")

        return df

    # ----------------------------------------
    # Full cleaning pipeline
    # ----------------------------------------
    def clean(self, df):
        df = self.detect_sudden_drops(df)
        df = self.remove_short_spikes(df)
        df = self.handle_missing(df)

        df.drop(columns=["spo2_diff", "possible_artifact"], inplace=True)

        return df