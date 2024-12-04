import json
import format_message
import global_manager

class Rules:
    rules_values = []
    rules_door = []

    def __init__(self):
        pass

    def add_rule(self, data):
        new_rule = RuleItem(data)

        if (new_rule.device_type_if == "TEMP" or new_rule.device_type_if == "HUMID" or new_rule.device_type_if == "ILLUM"):
            self.rules_values.append(new_rule)
        elif (new_rule.device_type_if == "DOOR"):
            self.rules_door.append(new_rule)
        return 1

    def execute_rule_value(self, node_id, value_type, value):
        for rule in self.rules_values:
            if (rule.device_type_if == value_type and rule.node_id_if == node_id and rule.enable == 1):
                isExecute = 0
                if (rule.comparator_if == ">"):
                    if (value > rule.value_if):
                        isExecute = 1
                elif (rule.comparator_if == "<"):
                    if (value < rule.value_if):
                        isExecute = 1
                elif (rule.comparator_if == ">="):
                    if (value >= rule.value_if):
                        isExecute = 1
                elif (rule.comparator_if == "<="):
                    if (value <= rule.value_if):
                        isExecute = 1
                elif (rule.comparator_if == "="):
                    if (value == rule.value_if):
                        isExecute = 1
                
                if (isExecute == 1):
                    # EXECUTE RULE HERE
                    global_manager.mySerialManager.write(rule.cmd)
                    global_manager.myAwsMqtt.publish("communicate/servertoclient",
                                         format_message.json_publish_update_control_rule("EXECUTED", rule.rule_id, "SUCCESS"))
    
    def execute_rule_door(self, value):
        for rule in self.rules_door:
            if (rule.enable == 1):
                isExecute = 0
                if (rule.comparator_if == value):
                    if (value == "OPEN"):
                        isExecute = 1
                
                if (isExecute == 1):
                    # EXECUTE RULE HERE
                    global_manager.mySerialManager.write(rule.cmd)
                    global_manager.myAwsMqtt.publish("communicate/servertoclient",
                                         format_message.json_publish_update_control_rule("EXECUTED", rule.rule_id, "SUCCESS"))


    def remove_rule(self, rule_id):
        for rule in self.rules_values:
            if (rule.rule_id == rule_id):
                # set enable to 0
                rule.enable = 0
                return 1
        for rule in self.rules_door:
            if (rule.rule_id == rule_id):
                # set enable to 0
                rule.enable = 0
                return 1
        return 0
    
    def print_rules(self):
        print("RULES:---------------------------------")
        print("---RULES VALUES---")
        for rule in self.rules_values:
            print(rule.to_string())
        print("---RULES DOOR---")
        for rule in self.rules_door:
            print(rule.to_string())
        print("END RULES:---------------------------------")
        return 1

class RuleItem:
    rule_id = ""
    enable = 0
    device_type_if = ""
    node_id_if = 0
    comparator_if = ""
    value_if = 0.0
    cmd = "" # format message

    def __init__(self, data):
        # data is a json after json.loads()
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
        if (device_type == "LED_RGB"):
            device_type = "1"
        elif (device_type == "RELAY"):
            device_type = "2"
        elif (device_type == "FAN"):
            device_type = "3"

        if (data["value"]["node_id"] == "CentralNode"):
            node_id = 0
        else:
            node_id = 1

        self.cmd = format_message.serial_control_device(node_id, device_type, value)
    
    def to_string(self):
        return "Rule ID: " + self.rule_id + ", Enable: " + str(self.enable) + ", Device Type IF: " + self.device_type_if + ", Node ID IF: " + str(self.node_id_if) + ", Comparator IF: " + self.comparator_if + ", Value IF: " + str(self.value_if) + ", Command: " + self.cmd
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

class Scenarios:
    scenarios = []

    def __init__(self):
        pass

    def add_scenario(self, data):
        new_scenario = ScenarioItem(data)
        self.scenarios.append(new_scenario)
        return 1

    def execute_scenario(self, scenario_id):
        for scenario in self.scenarios:
            if (scenario.scenario_id == scenario_id):
                if (scenario.enable == 1):
                    # EXECUTE SCENARIO HERE
                    return 1 
        return 0
    
    def remove_scenario(self, scenario_id):
        for scenario in self.scenarios:
            if (scenario.scenario_id == scenario_id):
                # set enable to 0
                scenario.enable = 0
                return 1
        return 0
    
class ScenarioItem:
    scenario_id = ""
    enable = 0
    scenario_cmds = []

    def __init__(self, data):
        data = json.loads(data)

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


