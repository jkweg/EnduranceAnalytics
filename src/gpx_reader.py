import gpxpy


def read_gpx(file_path):
    with open(file_path, "r") as file:
        gpx = gpxpy.parse(file)
        return gpx