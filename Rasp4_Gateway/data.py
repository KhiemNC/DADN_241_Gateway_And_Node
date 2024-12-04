import json
import format_message

rules = []
scenarios = []

class RuleItem:
    rule_id = ""
    enable = 0
    device_type_if = ""
    node_id_if = 0
    comparator_if = ""
    value_if = 0.0
    cmd = "" # format message

    def __init__(self, json_input):
        data = json.loads(json_input)

        self.rule_id = data["rule_id"]
        self.enable = 1
        self.device_type_if = data["value"]["device_type_if"]

        if (data["value"]["node_id_if"] == "CentralNode"):
            self.node_id_if = 0
        else: 
            self.node_id_if = 1

        self.comparator_if = data["value"]["comparator_if"]
        self.value_if = data["value"]["value_if"]

        device_type = data["value"]["device_type"]
        node_id = 0
        value = data["value"]["value"]
        if (data["value"]["node_id"] == "CentralNode"):
            node_id = 0
        else:
            node_id = 1

        self.cmd = format_message.serial_control_device(node_id, device_type, value)
# {
#   "command_id": "CMD00020",
#   "command_name": "CONTROL_RULE",
#   "type": "ADD",
#   "rule_id": "RULE0001",
#   "value": {
# 	  // IF
# 	  "device_type_if": "TEMP", // "DOOR", "TEMP, "HUMID, "ILLUM"
# 	  "node_id_if": "CentralNode",
# 	  "comparator_if": ">", // "<" ">=" "<=" "=" "OPEN" "CLOSE"
# 	  "value_if": "23", // co the "" neu comparator la "OPEN"/"CLOSE"
# 	  // THUC THI NEU DUNG
# 	  "device_type": "FAN", // "FAN" "RELAY" "LED_RGB"
# 	  "node_id": "CentralNode",
# 	  "value": "1" // BAT (1), TAT (0), hoac 0-100, hoac #ff00ff cho RGB
# 	}
# }

    
class ScenarioItem:
    scenario_id = ""
    enable = 0
    scenario_cmds = []

    def __init__(self, json_input):
        data = json.loads(json_input)

        self.scenario_id = data["scenario_id"]

        for cmd in data["value"]:
            node_id = cmd["node_id"]
            if (node_id == "CentralNode"):
                node_id = "0"
            else:
                node_id = "1"
            device_type = cmd["device_type"]
            value = cmd["value"]


            new_cmd = format_message.serial_control_device(node_id, device_type, value)
            
            self.scenario_cmds.append(new_cmd)
        
# {
#   "command_id": "CMD00030",
#   "command_name": "SCENARIO",
#   "type": "ADD",
#   "scenario_id": "SCENE001",
#   "value": [
# 	  {
# 	    "command_id": "CMD00010",
# 		  "command_name": "CONTROL_DEVICE",
# 		  "device_type": "LED_RGB", // "FAN", "RELAY", "LED_RGB"
# 		  "node_id": "CentralNode",
# 		  "value": "#ff00ff"
# 	  },
# 	  {
# 	    "command_id": "CMD00010",
# 		  "command_name": "CONTROL_DEVICE",
# 		  "device_type": "FAN", // "FAN", "RELAY", "LED_RGB"
# 		  "node_id": "CentralNode",
# 		  "value": "45"
# 	  },
# 	  {
# 	    "command_id": "CMD00010",
# 		  "command_name": "CONTROL_DEVICE",
# 		  "device_type": "RELAY", // "FAN", "RELAY", "LED_RGB"
# 		  "node_id": "CentralNode",
# 		  "value": "1"
# 	  }
#   ]
# }


