def get_sensor_data(point):

    heart_rate = None
    cadence = None

    for extension in point.extensions:
        for child in extension:
            tag_name = child.tag.split("}")[-1]
            if tag_name == "hr":
                heart_rate = int(child.text)
            if tag_name == "cad":
                cadence = int(child.text)

    return heart_rate, cadence