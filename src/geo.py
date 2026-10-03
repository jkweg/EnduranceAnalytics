from math import radians, sin, cos, sqrt, atan2

def calculate_distance(point1, point2):
    lat1 = radians(point1.latitude)
    lon1 = radians(point1.longitude)

    lat2 = radians(point2.latitude)
    lon2 = radians(point2.longitude)

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    a = (
            sin(delta_lat / 2) ** 2
            + cos(lat1) * cos(lat2) * sin(delta_lon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    earth_radius = 6371000

    return earth_radius * c

def calculate_elevation_gain(previous_point, point, threshold=1.0):
    elevation_diff = point.elevation - previous_point.elevation

    if elevation_diff > threshold:
        return elevation_diff
    else:
        return 0

def smooth_elevations(elevations, window_size=5):
    smoothed = []

    for i in range(len(elevations)):
        start = max(0, i - window_size // 2)
        end = min(len(elevations), i + window_size // 2 + 1)

        window = elevations[start:end]
        average = sum(window) / len(window)

        smoothed.append(average)

    return smoothed

def calculate_total_elevation_gain(elevations,threshold=1.0):
    gain = 0
    reference_elevation = elevations[0]

    for elevation in elevations[1:]:
        diff = elevation - reference_elevation

        if diff >= threshold:
            gain += diff
            reference_elevation = elevation

        elif diff <= -threshold:
            reference_elevation = elevation

    return gain
