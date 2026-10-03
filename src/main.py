from gpx_reader import read_gpx
from src.activity_analyzer import analyze_activity
from formatters import format_pace

gpx = read_gpx("../data/Bieg10km.gpx")
stats = analyze_activity(gpx)
print(stats)
print(format_pace(stats.average_pace))

for split in stats.splits:
    print(f"{split.kilometer} | {format_pace(split.pace)} | {split.average_heart_rate} | {split.average_cadence}")

print(f"{stats.elevation_gain:.1f} m")

# print(stats.average_heart_rate,
#       stats.max_heart_rate,
#       stats.average_cadence,
#       stats.max_cadence
#       )
