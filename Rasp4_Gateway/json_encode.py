import json

def json_publish(node_id, value_type, value):
    #value is a double
    value = float(value)
    data = {
        "node_id": node_id,
        "value_type": value_type,
        "value": value
    }
    return json.dumps(data)