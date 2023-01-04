import json
import os
import re

import pytz

directory_path = os.path.dirname(os.path.abspath(os.path.abspath(__file__)))
new_path = os.path.join(directory_path, "text.json")

with open(new_path, "r", encoding="utf-8") as fp:
    text = json.load(fp)

kyiv_tz = os.getenv("TIME_ZONE", "Europe/Kiev")
TIME_ZONE = pytz.timezone(kyiv_tz)