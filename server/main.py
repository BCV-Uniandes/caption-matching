import json
import os
import random

from flask import Flask, abort, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Path to the file containing all descriptions
DESCRIPTIONS_FILE = "/media/SSD6/cigonzalez/data/caption-matching/ids.json"
# Directory where individual annotation files will be saved
ANNOTATIONS_DIR = "/media/SSD6/cigonzalez/data/caption-matching"
METHODS = ["osprey", "ours"]

# List of valid categories (add or remove according to your Cityscapes setup)
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
    "None of the above",
]


# Load descriptions
with open(DESCRIPTIONS_FILE, "r", encoding="utf-8") as f:
    descriptions = json.load(f)


@app.route("/api/<string:method>/ids", methods=["GET"])
def get_next_annotation(method):
    """Return the next unannotated description."""
    # Filter out descriptions that already have an annotation file
    pending = [d for d in descriptions[method] if d["annotated"] is False]
    if not pending:
        return jsonify({"message": "No descriptions left to annotate."}), 200
    return jsonify(pending), 200


@app.route("/api/<string:method>/<string:item_id>", methods=["GET"])
def get_annotation_by_id(method, item_id):
    """Return the description matching the given ID."""
    # Load descriptions
    with open(
        os.path.join(ANNOTATIONS_DIR, method, "{:}.json".format(item_id)),
        "r",
        encoding="utf-8",
    ) as f:
        description = json.load(f)
    return jsonify(description), 200


@app.route("/api/<string:method>/<string:item_id>", methods=["POST"])
def post_annotation(method, item_id):
    """Receive the assigned category and save the annotation file."""
    data = request.get_json()
    if not data or "category" not in data:
        return jsonify({"error": "Request JSON must include a 'category' field"}), 400

    category = data["category"]
    if category not in CATEGORIES:
        return (
            jsonify({"error": f"Invalid category. Must be one of: {CATEGORIES}"}),
            400,
        )

    out_path = os.path.join(ANNOTATIONS_DIR, method, f"{item_id}.json")
    # Load existing data if it exists
    with open(out_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Update the category
    data["category"] = CATEGORIES.index(category)
    # Mark the description as annotated
    for d in descriptions[method]:
        if d["id"] == item_id:
            d["annotated"] = True
            break
    # Save the updated description
    with open(DESCRIPTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(descriptions, f, ensure_ascii=False, indent=2)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return jsonify({"message": "Annotation saved successfully."}), 200


if __name__ == "__main__":

    # Run in development mode; use Gunicorn/Uvicorn or another WSGI server in production
    # app.run(host="0.0.0.0", port=5001, debug=True)
    app.run()
