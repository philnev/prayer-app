
import json
from datetime import datetime
from pathlib import Path
import random

index_path = "index.html"
json_path = "weekly_readings_filled.json"

with open(json_path, "r") as f:
    readings = json.load(f)

today = datetime.today().date()
selected = None
for entry in readings:
    entry_date = datetime.strptime(entry["date"], "%Y-%m-%d").date()
    if today >= entry_date:
        selected = entry
    else:
        break

if not selected:
    raise ValueError("No applicable reading found for today.")

# Simulate AI-style prayer and exercise
prayer = (
    "God of new beginnings, meet us in the ordinary and the unexpected this week. "
    "Help us to recognise your grace in the small spaces, and let our words and silence "
    "both be prayers. Amen."
)

exercises = [
    "Take 10 minutes outside each day. Notice three things you've never paid attention to before.",
    "Each morning, name one thing you’re thankful for, and carry it with you into the day.",
    "Before bed, light a candle and sit in silence. Let your breath slow and say: ‘Thank you, God, for today.’",
    "Take a slow walk and with each step say quietly: ‘Here I am, God. I’m listening.’"
]
exercise = random.choice(exercises)

# Build new sections
reading_block = f"""<section>
  <h2>Reading for the Week</h2>
  <h3>{selected["reading"]} ({selected["version"]})</h3>
  <p>{selected["text"]}</p>
  <p><strong>Reflection:</strong> {selected["reflection"]}</p>
  <p><em>{selected["question"]}</em></p>
</section>"""

prayer_block = f"""<section>
  <h2>Prayer for the Week</h2>
  <p>{prayer}</p>
</section>"""

exercise_block = f"""<section>
  <h2>Spiritual Exercise</h2>
  <p>{exercise}</p>
</section>"""

# Read the HTML
with open(index_path, "r") as f:
    html = f.read()

# Update prayer
p_start = html.find("<!-- START OF PRAYER -->")
p_end = html.find("<!-- END OF PRAYER -->") + len("<!-- END OF PRAYER -->")
html = html[:p_start] + "<!-- START OF PRAYER -->\n" + prayer_block + "\n<!-- END OF PRAYER -->" + html[p_end:]

# Update exercise
e_start = html.find("<!-- START OF EXERCISE -->")
e_end = html.find("<!-- END OF EXERCISE -->") + len("<!-- END OF EXERCISE -->")
html = html[:e_start] + "<!-- START OF EXERCISE -->\n" + exercise_block + "\n<!-- END OF EXERCISE -->" + html[e_end:]

# Archive and update reading
r_start = html.find("<!-- START OF CURRENT READING -->")
r_end = html.find("<!-- END OF CURRENT READING -->") + len("<!-- END OF CURRENT READING -->")
archive_marker = "<!-- START OF READING ARCHIVE -->"
old_reading = html[r_start:r_end]
archive_index = html.find(archive_marker)
html = html[:archive_index] + old_reading + "\n" + archive_marker + html[archive_index + len(archive_marker):]
html = html[:r_start] + "<!-- START OF CURRENT READING -->\n" + reading_block + "\n<!-- END OF CURRENT READING -->" + html[r_end:]

# Save
with open(index_path, "w") as f:
    f.write(html)
