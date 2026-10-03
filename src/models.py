from dataclasses import dataclass
from datetime import timedelta

import gpxpy

@dataclass
class Split:
    kilometer: int
    time_seconds: float
    pace: float
    average_heart_rate: float| None
    average_cadence: float| None


@dataclass
class ActivityStats:
    point_count: int
    first_point: gpxpy.gpx.GPXTrackPoint
    last_point: gpxpy.gpx.GPXTrackPoint
    total_distance: float
    duration: timedelta
    average_pace: float
    splits: list[Split]
    elevation_gain: float
    moving_time: float
    average_heart_rate: float| None
    max_heart_rate: int| None
    average_cadence: float | None
    max_cadence: int| None
