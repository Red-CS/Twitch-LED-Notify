import json

class Write():
    """Writes objects to JSON files"""

    def write(data, file):
        with open(file, 'r') as f:
            keys = json.load(f)
            keys[list(data.keys())[0]] = list(data.values())[0]

        with open(file, 'w') as f:
            f.write(json.dumps(keys, indent=2))
