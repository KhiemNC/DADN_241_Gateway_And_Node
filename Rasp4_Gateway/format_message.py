import json

def json_publish_values(node_id, value_type, value):
    #value is a double
    value = float(value)
    data = {
        "node_id": node_id,
        "value_type": value_type,
        "value": value
    }
    return json.dumps(data)

def json_publish_update_device_status(node_id, device_type, value):
    data = {
        "command_id": "CMD00011",
        "command_name": "UPDATE_DEVICE_STATUS",
        "device_type": device_type,
        "node_id": node_id,
        "value": value
    }
    return json.dumps(data)

def serial_control_device(id, device_type, value):
    # Example serial string:
    # !0:1:123456#
    # This has exactly 12 characters

    # Ensure id is 1 character long
    id = str(id)
    if (len(id) > 1):
        print("serial_control_device(): id is too long")
        return
    
    # Ensure device_type is 1 character long
    device_type = str(device_type)
    if (len(device_type) > 1):
        print("serial_control_device(): device_type is too long")
        return
    
    # Ensure value is 6 characters long
    value = str(value)
    if (len(value) > 6):
        print("serial_control_device(): value is too long")
        return
    elif (len(value) < 6):
        value = value + "0" * (6 - len(value))
    
    return "!" + id + ":" + device_type + ":" + value + "#"