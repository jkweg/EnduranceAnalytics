def format_pace(pace_seconds):
    minutes = int(pace_seconds // 60)
    seconds = int(pace_seconds % 60)

    return f"{minutes}:{seconds:02d}"