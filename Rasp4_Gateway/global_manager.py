import aws_mqtt
import data_processing
import serial_manager
import data

value_topics = ["values"]
receiving_topic = ["communicate/clienttoserver"]
transfering_topic = ["communicate/servertoclient"]
error_topics = ["dev/error"]
others_topics = ["others"]
all_topics = value_topics + receiving_topic + transfering_topic + error_topics + others_topics
need_to_subscribe = receiving_topic + error_topics

def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    print("RECEIVED MESSAGE FROM TOPIC '{}': {}".format(topic, payload))
    if (topic == receiving_topic[0]):
        data_processing.process_data_from_client_to_device(payload)

myAwsMqtt = aws_mqtt.AWS_MQTT(
    endpoint="a3pm7mxg4x4xbb-ats.iot.ap-southeast-2.amazonaws.com",
    ca_file="./AWS_Connection_Kit/root-CA.crt",
    cert_file="./AWS_Connection_Kit/DADN_Rasp4_Gateway.cert.pem",
    private_key="./AWS_Connection_Kit/DADN_Rasp4_Gateway.private.key",
    client_id="DADN-Python-Gateway",
    topic=need_to_subscribe,
    count=0,
    on_message_received=on_message_received
)

mySerialManager = None

myRules = data.Rules()
myScenarios = data.Scenarios()