from math import radians, sin, cos, sqrt, atan2
import gpxpy

point_counter = 0
first_point = None
last_point = None

previous_point = None
total_distance = 0

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



with open("../data/Bieg10km.gpx" , "r" ) as gpx_file:
    gpx = gpxpy.parse(gpx_file)

    for track in gpx.tracks:
        for segment in track.segments:
            previous_point = None
            for point in segment.points:
                if first_point is None:
                    first_point = point
                last_point = point

                if previous_point is not None:
                    distance = calculate_distance(previous_point, point)
                    total_distance += distance

                previous_point = point
                # print(
                #     point.latitude,
                #     point.longitude,
                #     point.elevation,
                #     point.time
                # )
                point_counter += 1

print(point_counter)

print("START")
print(
    first_point.latitude,
    first_point.longitude,
    first_point.elevation,
    first_point.time
)
print("END")
print(
    last_point.latitude,
    last_point.longitude,
    last_point.elevation,
    last_point.time
)

duration = last_point.time - first_point.time
print(duration)
print(duration.total_seconds())
print(type(duration))

print("Distance:", total_distance, "m")
print("Distance:", total_distance / 1000, "km")