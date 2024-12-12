import global_manager
import format_message
import json
import serial_manager

VALUE_TYPE_TO_TOPIC_VALUES = ["TEMP", "HUMI", "LUMO"] # values_topic
VALUE_TYPE_TO_TOPIC_CLIENTS = ["LED_RGB", "RELAY", "FAN", "DOOR", "DOOR_PASS"] # transfering_topic

def split_cmd_from_node(data):
    # !1:TEMP:23.4#
    data = data.replace("!", "")
    data = data.replace("#", "")
    split_data = data.split(":")
    if len(split_data) != 3:
        return None, None, None
    return split_data[0], split_data[1], split_data[2]

def process_data_from_node_to_topics(new_message):
    # message in type: !NODE_ID:VALUE_TYPE:VALUE#
    node_id, value_type, value = split_cmd_from_node(new_message)

    # Publish change
    pub_node_id = node_id
    pub_value_type = value_type
    if (node_id == "0"):
        pub_node_id = "CentralNode"
    else:
        pub_node_id = "Node" + node_id

    if (value_type in VALUE_TYPE_TO_TOPIC_VALUES):
        if (value_type == "TEMP"):
            pub_value_type = "temperature"
        elif (value_type == "HUMI"):
            pub_value_type = "humidity"
        elif (value_type == "LUMO"):
            pub_value_type = "illuminance"
        global_manager.myAwsMqtt.publish("values", format_message.json_publish_values(pub_node_id, pub_value_type, value))
    
    elif (value_type in VALUE_TYPE_TO_TOPIC_CLIENTS):
        global_manager.myAwsMqtt.publish("communicate/servertoclient",
                                         format_message.json_publish_update_device_status(pub_node_id, pub_value_type, value))
        
    # RULES execution
    node_id = int(node_id)
    if (value_type == "TEMP" or value_type == "HUMI" or value_type == "LUMO"):
        if (value_type == "HUMI"):
            value_type = "HUMID"
        elif (value_type == "LUMO"):
            value_type = "ILLUM"

        global_manager.myRules.execute_rule_value(node_id, value_type, float(value))
    elif (value_type == "DOOR"):
        if (int(value) == 1):
            value = "OPEN"
        else:
            value = "CLOSE"
        global_manager.myRules.execute_rule_door(value)


def CMD00010_control_device(data):
    # Example message:
    # {
    #     "command_id": "CMD00010",
    #     "command_name": "CONTROL_DEVICE",
    #     "device_type": "LED_RGB",
    #     "node_id": "Node1",
    #     "value": "ON"
    # }
    node_id = data["node_id"]
    if (node_id == "CentralNode"):
        node_id = "0"
    else:
        node_id = node_id.replace("Node", "")

    device_type = data["device_type"]
    if (device_type == "LED_RGB"):
        device_type = "1"
    elif (device_type == "RELAY"):
        device_type = "2"
    elif (device_type == "FAN"):
        device_type = "3"
    elif (device_type == "DOOR"):
        device_type = "4"
    elif (device_type == "DOOR_PASS"):
        device_type = "5"

    value = data["value"]

    cmd = format_message.serial_control_device(node_id, device_type, value)
    # Debug
    print(cmd)
    # End debug
    global_manager.mySerialManager.write(cmd)

def CMD00020_control_rule(data):
    if data["type"] == "ADD":
        global_manager.myRules.add_rule(data)

        # Debug
        global_manager.myRules.print_rules()
        # End debug

        global_manager.myAwsMqtt.publish("communicate/servertoclient",
                                         format_message.json_publish_update_control_rule("ADD_RESPONSE", data["rule_id"], "SUCCESS"))
    elif data["type"] == "DELETE":
        result = global_manager.myRules.remove_rule(data["rule_id"])

        # Debug
        global_manager.myRules.print_rules()
        # End debug

        if (result == 1):
            global_manager.myAwsMqtt.publish("communicate/servertoclient",
                                         format_message.json_publish_update_control_rule("DELETE_RESPONSE", data["rule_id"], "SUCCESS"))

def CMD00030_scenario(data):
    if data["type"] == "ADD":
        global_manager.myScenarios.add_scenario(data)

        # Debug
        global_manager.myScenarios.print_scenarios()
        # End debug

        global_manager.myAwsMqtt.publish("communicate/servertoclient",
                                         format_message.json_publish_update_scenario("ADD_RESPONSE", data["scenario_id"], "SUCCESS"))

    elif data["type"] == "DELETE":
        result = global_manager.myScenarios.remove_scenario(data["scenario_id"])
        if (result == 1):
            global_manager.myAwsMqtt.publish("communicate/servertoclient",
                                         format_message.json_publish_update_scenario("DELETE_RESPONSE", data["scenario_id"], "SUCCESS"))

    elif data["type"] == "RUN":
        result = global_manager.myScenarios.execute_scenario(data["scenario_id"])
        if (result == 1):
            global_manager.myAwsMqtt.publish("communicate/servertoclient",
                                         format_message.json_publish_update_scenario("RUN_RESPONSE", data["scenario_id"], "SUCCESS"))


def process_data_from_client_to_device(message):
    # Example message:
    # {
    #     "command_id": "CMD00010",
    #     "command_name": "CONTROL_DEVICE",
    #     ...
    # }
    # Extract the json data from the message
    data = json.loads(message)

    if (data["command_id"] == "CMD00010"):
        CMD00010_control_device(data)
    elif (data["command_id"] == "CMD00020"):
        CMD00020_control_rule(data)
    elif (data["command_id"] == "CMD00030"):
        CMD00030_scenario(data)