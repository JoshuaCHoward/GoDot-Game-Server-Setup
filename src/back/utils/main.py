import json
def to_json(obj):
    return json.dumps(obj, default=lambda obj: obj.__dict__)

def to_dict(obj):
    return json.loads(json.dumps(obj, default=lambda o: o.__dict__))