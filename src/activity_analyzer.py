from geo import calculate_distance, smooth_elevations, calculate_total_elevation_gain
from models import ActivityStats, Split
from sensors import get_sensor_data


def analyze_activity(gpx):
    point_counter = 0
    first_point = None
    last_point = None

    previous_point = None
    total_distance = 0

    splits = []
    distance_since_last_split = 0
    split_number = 1
    split_heart_rates = []
    split_cadences = []

    total_elevation_gain = 0
    elevations = []

    moving_time_seconds = 0

    heart_rates = []
    cadences = []

    for track in gpx.tracks:
        for segment in track.segments:
            previous_point = None
            for point in segment.points:

                hr, cadence = get_sensor_data(point)
                if hr is not None:
                    heart_rates.append(hr)
                    split_heart_rates.append(hr)
                if cadence is not None:
                    cadences.append(cadence)
                    split_cadences.append(cadence)

                if first_point is None:
                    first_point = point
                    split_start_time = first_point.time
                last_point = point

                if point.elevation is not None:
                    elevations.append(point.elevation)

                if previous_point is not None:

                    time_diff = (point.time - previous_point.time).total_seconds()

                    distance = calculate_distance(previous_point, point)
                    total_distance += distance
                    distance_since_last_split += distance

                    # total_elevation_gain += calculate_elevation_gain(previous_point,point)

                    if time_diff > 0:
                        speed = distance / time_diff
                        if speed > 0.5:
                            moving_time_seconds += time_diff

                if distance_since_last_split >= 1000:
                    split_time = point.time - split_start_time

                    if not split_heart_rates:
                        split_average_heart_rate = None
                    else:
                        split_average_heart_rate = sum(split_heart_rates) / len(split_heart_rates)
                    if not split_cadences:
                        split_average_cadence = None
                    else:
                        split_average_cadence = sum(split_cadences) / len(split_cadences)

                    splits.append(
                        Split(
                            kilometer = split_number,
                            time_seconds = split_time.total_seconds(),
                            pace = split_time.total_seconds(),
                            average_heart_rate = split_average_heart_rate,
                            average_cadence = split_average_cadence
                        )
                    )

                    split_number += 1
                    distance_since_last_split -= 1000
                    split_start_time = point.time
                    split_heart_rates = []
                    split_cadences = []

                previous_point = point
                point_counter += 1

    duration = last_point.time - first_point.time

    distance_km = total_distance / 1000
    pace_seconds_per_km = moving_time_seconds/ distance_km

    smoothed_elevations = smooth_elevations(elevations)
    total_elevation_gain = calculate_total_elevation_gain(smoothed_elevations)

    if not heart_rates:
        average_hr = None
        max_hr = None
    else:
        average_hr = sum(heart_rates) / len(heart_rates)
        max_hr = max(heart_rates)

    if not cadences:
        average_cadence = None
        max_cadence = None
    else:
        average_cadence = sum(cadences) / len(cadences)
        max_cadence = max(cadences)

    return ActivityStats(point_count = point_counter,
                         first_point = first_point ,
                         last_point = last_point,
                         total_distance = total_distance ,
                         duration = duration,
                         average_pace = pace_seconds_per_km,
                         splits = splits,
                         elevation_gain = total_elevation_gain,
                         moving_time = moving_time_seconds,
                         average_heart_rate = average_hr,
                         average_cadence = average_cadence,
                         max_heart_rate = max_hr,
                         max_cadence = max_cadence,

    )