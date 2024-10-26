import gateway
import time
import json
import random

if __name__ == '__main__':
    topic_list = ["sdk/test/python", "sdk/test/python1", "sdk/test/python2"]

    myAwsMqtt = gateway.AWS_MQTT(
        endpoint="a3pm7mxg4x4xbb-ats.iot.ap-southeast-2.amazonaws.com",
        ca_file="./AWS_Connection_Kit/root-CA.crt",
        cert_file="./AWS_Connection_Kit/demo_gateway.cert.pem",
        private_key="./AWS_Connection_Kit/demo_gateway.private.key",
        client_id="basicPubSub",
        topic=topic_list,
        count=0
    )

    myAwsMqtt.connect()
    myAwsMqtt.subcribe()

    counter = 0;
    while (1):
        # random a number from 35.0 to 42.0
        temperature = round(35.0 + (42.0 - 35.0) * random.random(), 2)
        message = json.dumps({"temperature": temperature})
        myAwsMqtt.publish("sdk/test/python1", message)
        time.sleep(5)
        counter += 1

    myAwsMqtt.disconnect()