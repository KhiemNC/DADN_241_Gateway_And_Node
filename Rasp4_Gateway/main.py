import aws_mqtt
import time
import json
import random

if __name__ == '__main__':
    value_topics = ["value/temperature",
                    "value/humidity",
                    "value/illuminance"]
    
    communicate_topics = ["communicate/clienttoserver",
                            "communicate/servertoclient"]
    
    error_topics = ["dev/error"]

    others_topics = ["others/1",
                    "others/2"]
    
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

    myAwsMqtt.connect()
    myAwsMqtt.subcribe()

    counter = 0;
    while (1):
        pass
        # random a number from 35.0 to 42.0
        # temperature = round(35.0 + (42.0 - 35.0) * random.random(), 2)
        # message = json.dumps({"temperature": temperature})
        # myAwsMqtt.publish("sdk/test/python", message)
        # time.sleep(5)
        # counter += 1

    myAwsMqtt.disconnect()