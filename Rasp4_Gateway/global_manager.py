import aws_mqtt

value_topics = ["values"]
communicate_topics = ["communicate/clienttoserver", "communicate/servertoclient"]
error_topics = ["dev/error"]
others_topics = ["others"]
all_topics = value_topics + communicate_topics + error_topics + others_topics

myAwsMqtt = aws_mqtt.AWS_MQTT(
    endpoint="a3pm7mxg4x4xbb-ats.iot.ap-southeast-2.amazonaws.com",
    ca_file="./AWS_Connection_Kit/root-CA.crt",
    cert_file="./AWS_Connection_Kit/DADN_Rasp4_Gateway.cert.pem",
    private_key="./AWS_Connection_Kit/DADN_Rasp4_Gateway.private.key",
    client_id="DADN-Python-Gateway",
    topic=all_topics,
    count=0
)
