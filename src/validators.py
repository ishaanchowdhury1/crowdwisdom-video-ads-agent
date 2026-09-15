from pathlib import Path
import json

REQUIRED = {"title", "duration_seconds", "target_icp", "pain_point", "visual_hook", "scenes", "cta", "disclaimer"}

def validate_script(path: str):
    data = json.loads(Path(path).read_text())
    missing = REQUIRED - set(data)
    if missing:
        raise ValueError(f"Missing script fields: {sorted(missing)}")
    if not 30 <= int(data["duration_seconds"]) <= 60:
        raise ValueError("Ad duration must be 30–60 seconds")
    if not data["scenes"]:
        raise ValueError("Storyboard needs scenes")
    return True
