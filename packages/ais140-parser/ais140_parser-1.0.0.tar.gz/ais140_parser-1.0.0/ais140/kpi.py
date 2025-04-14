import pandas as pd
from datetime import datetime, timedelta

class AIS140KPI:
    def __init__(self, tracking_df: pd.DataFrame, health_df: pd.DataFrame = None, logging_df: pd.DataFrame = None):
        self.tracking_df = tracking_df.copy() if tracking_df is not None else pd.DataFrame()
        self.health_df = health_df.copy() if health_df is not None else pd.DataFrame()
        self.logging_df = logging_df.copy() if logging_df is not None else pd.DataFrame()
        self._prepare_tracking_data()

    def _prepare_tracking_data(self):
        if self.tracking_df.empty:
            return
        # Parse timestamp from date & time fields
        self.tracking_df['timestamp'] = self.tracking_df.apply(self._combine_date_time, axis=1)
        self.tracking_df['speed'] = pd.to_numeric(self.tracking_df.get('speed', 0), errors='coerce')
        self.tracking_df['imei'] = self.tracking_df['imei'].astype(str)

    def _combine_date_time(self, row):
        try:
            date_str = row.get('date', '')  # ddmmyyyy
            time_str = row.get('time', '')  # HHMMSS
            dt_str = f"{date_str} {time_str}"
            return datetime.strptime(dt_str, "%d%m%Y %H%M%S")
        except Exception:
            return pd.NaT

    def total_devices(self):
        return self.tracking_df['imei'].nunique()

    def online_devices(self, threshold_minutes=5):
        now = datetime.utcnow()
        active = self.tracking_df[self.tracking_df['timestamp'] >= now - timedelta(minutes=threshold_minutes)]
        return active['imei'].nunique()

    def offline_devices(self, threshold_minutes=5):
        return self.total_devices() - self.online_devices(threshold_minutes)

    def average_speed(self):
        if 'speed' in self.tracking_df.columns:
            return self.tracking_df['speed'].mean()
        return 0.0

    def overspeeding_devices(self, speed_limit=60):
        overspeed_df = self.tracking_df[self.tracking_df['speed'] > speed_limit]
        return overspeed_df['imei'].nunique()

    def current_locations(self):
        if {'imei', 'latitude', 'longitude'}.issubset(self.tracking_df.columns):
            return self.tracking_df[['imei', 'latitude', 'longitude']].dropna()
        return pd.DataFrame()

    def get_health_status_summary(self):
        if self.health_df.empty:
            return "No health data available"
        return self.health_df['engine_status'].value_counts().to_dict()

    def get_logging_events_summary(self):
        if self.logging_df.empty:
            return "No logging data available"
        return self.logging_df['event'].value_counts().to_dict()

    def get_all_kpis(self):
        return {
            "Total Devices": self.total_devices(),
            "Online Devices": self.online_devices(),
            "Offline Devices": self.offline_devices(),
            "Average Speed": self.average_speed(),
            "Over-speeding Devices": self.overspeeding_devices(),
            "Health Status Summary": self.get_health_status_summary(),
            "Logging Events Summary": self.get_logging_events_summary(),
            "Current Locations": self.current_locations().to_dict(orient="records")
        }
