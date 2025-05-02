import json
import os
import random

# File and directory names
DESCRIPTIONS_FILE = "../data/ids.json"
ANNOTATIONS_DIR = "../data"
METHODS = ["osprey", "ours"]

# Sample Cityscapes categories (plus background)
CATEGORIES = [
    "road",
    "sidewalk",
    "building",
    "wall",
    "fence",
    "pole",
    "traffic light",
    "traffic sign",
    "vegetation",
    "terrain",
    "sky",
    "person",
    "rider",
    "car",
    "truck",
    "bus",
    "train",
    "motorcycle",
    "bicycle",
    "background",
]

# Example segment descriptions for testing
sample_descriptions = [
    {"id": 1, "description": "Red car stopped at a traffic light"},
    {"id": 2, "description": "Group of pedestrians on the sidewalk"},
    {"id": 3, "description": "Cyclist riding across the intersection"},
    {"id": 4, "description": "Bus pulling up to a bus stop"},
    {"id": 5, "description": "Trees and grass beside the road"},
]


def save_ids(descriptions, filepath):
    """Write the list of descriptions ids to a JSON file."""
    ids = {
        m: [{"id": d["id"], "annotated": False} for d in descriptions] for m in METHODS
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(ids, f, ensure_ascii=False, indent=2)


def save_sample_annotations(descriptions, out_dir):
    """Create one annotation file per description, picking a random category."""
    for m in METHODS:
        method_out_dir = os.path.join(out_dir, m)
        os.makedirs(method_out_dir, exist_ok=True)
        for item in descriptions:
            annotation = {
                "id": item["id"],
                "description": item["description"],
                "category": None,
            }
            out_path = os.path.join(method_out_dir, f"{item['id']}.json")
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(annotation, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # Generate ids.json
    save_ids(sample_descriptions, DESCRIPTIONS_FILE)
    # Generate one sample annotation per description
    save_sample_annotations(sample_descriptions, ANNOTATIONS_DIR)
