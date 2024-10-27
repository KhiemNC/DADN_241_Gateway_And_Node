from awscrt import mqtt, http
from awsiot import mqtt_connection_builder
import sys
import threading
# from utils.command_line_utils import CommandLineUtils

# This class is contain all the methods to working with AWS IoT throught 
# MQTT protocol. It will save the key, cert, ca, endpoint, port, client_id,
# ....
class AWS_MQTT:
    # The server endpoint to connect to.
    __endpoint = None
    # ca_file
    __ca_file = None
    # cert_file
    __cert_file = None
    # private_key
    __private_key = None
    # client_id
    __client_id = None
    # topic. Expected a array of topic
    __topic = [None]
    # count
    __count = None

    # callback function
    __on_connection_interrupted = None
    __on_connection_resumed = None
    __on_resubscribe_complete = None
    __on_message_received = None
    __on_connection_success = None
    __on_connection_failure = None
    __on_connection_closed = None

    proxy_options = None
    mqtt_connection = None

    received_count = 0
    received_all_event = threading.Event()

    # Default Callback when connection is accidentally lost.
    def default_on_connection_interrupted(self, connection, error, **kwargs):
        print("DEFAULT MQTT: Connection interrupted. error: {}".format(error))

    # Default Callback when an interrupted connection is re-established.
    def default_on_resubscribe_complete(self, resubscribe_future):
        resubscribe_results = resubscribe_future.result()
        print("DEFAULT MQTT: Resubscribe results: {}".format(resubscribe_results))

        for topic, qos in resubscribe_results['topics']:
            if qos is None:
                sys.exit("DEFAULT MQTT: Server rejected resubscribe to topic: {}".format(topic))

    def default_on_connection_resumed(self, connection, return_code, session_present, **kwargs):
        print("DEFAULT MQTT: Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))

        if return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present:
            print("DEFAULT MQTT: Session did not persist. Resubscribing to existing topics...")
            resubscribe_future, _ = connection.resubscribe_existing_topics()

            # Cannot synchronously wait for resubscribe result because we're on the connection's event-loop thread,
            # evaluate result with a callback instead.
            resubscribe_future.add_done_callback(self.__on_resubscribe_complete)
    
    # Default Callback when the subscribed topic receives a message
    def default_on_message_received(self, topic, payload, dup, qos, retain, **kwargs):
        print("DEFAULT MQTT: Received message from topic '{}': {}".format(topic, payload))
        # global received_count
        # received_count += 1
        # if received_count == self.__count:
        #     self.received_all_event.set()

    # Default Callback when the connection successfully connects
    def default_on_connection_success(self, connection, callback_data):
        assert isinstance(callback_data, mqtt.OnConnectionSuccessData)
        print("DEFAULT MQTT: Connection Successful with return code: {} session present: {}".format(callback_data.return_code, callback_data.session_present))

    # Default Callback when a connection attempt fails
    def default_on_connection_failure(self, connection, callback_data):
        assert isinstance(callback_data, mqtt.OnConnectionFailureData)
        print("DEFAULT MQTT: Connection failed with error code: {}".format(callback_data.error))

    # Default Callback when a connection has been disconnected or shutdown successfully
    def default_on_connection_closed(self, connection, callback_data):
        print("DEFAULT MQTT: Connection closed")
        
    def __init__(self, 
                endpoint, 
                ca_file, 
                cert_file, 
                private_key, 
                client_id, 
                topic, 
                count,
                on_connection_interrupted=None,
                on_connection_resumed=None,
                on_resubscribe_complete=None,
                on_connection_received=None,
                on_connection_success=None,
                on_connection_failure=None,
                on_connection_closed=None,
                ):
        self.__endpoint = endpoint
        self.__ca_file = ca_file
        self.__cert_file = cert_file
        self.__private_key = private_key
        self.__client_id = client_id
        self.__topic = topic
        self.__count = count

        self.__on_connection_interrupted = on_connection_interrupted if on_connection_interrupted is not None else self.default_on_connection_interrupted
        self.__on_connection_resumed = on_connection_resumed if on_connection_resumed is not None else self.default_on_connection_resumed
        self.__on_resubscribe_complete = on_resubscribe_complete if on_resubscribe_complete is not None else self.default_on_resubscribe_complete
        self.__on_message_received = on_connection_received if on_connection_received is not None else self.default_on_message_received
        self.__on_connection_success = on_connection_success if on_connection_success is not None else self.default_on_connection_success
        self.__on_connection_failure = on_connection_failure if on_connection_failure is not None else self.default_on_connection_failure
        self.__on_connection_closed = on_connection_closed if on_connection_closed is not None else self.default_on_connection_closed

    def connect(self):
        self.mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=self.__endpoint,
            cert_filepath=self.__cert_file,
            pri_key_filepath=self.__private_key,
            ca_filepath=self.__ca_file,
            on_connection_interrupted=self.__on_connection_interrupted,
            on_connection_resumed=self.__on_connection_resumed,
            client_id=self.__client_id,
            clean_session=False,
            keep_alive_secs=30,
            http_proxy_options=None,
            on_connection_success=self.__on_connection_success,
            on_connection_failure=self.__on_connection_failure,
            on_connection_closed=self.__on_connection_closed)
        
        print(f"Connecting to {self.__endpoint} with client ID '{self.__client_id}'")
        connect_future = self.mqtt_connection.connect()
        connect_future.result()
        print("Connected!")

    def subcribe(self):
        print("Subscribing to topic '{}'...".format(self.__topic))
        for topic in self.__topic:
            print("Subscribing to topic '{}'...".format(topic))
            subscribe_future, packet_id = self.mqtt_connection.subscribe(
                topic=topic,
                qos=mqtt.QoS.AT_LEAST_ONCE,
                callback=self.__on_message_received) 
            subscribe_result = subscribe_future.result()
            print("Subscribed with {}".format(str(subscribe_result['qos'])))
        print("Subscribed to all topics!")
        
    def publish(self, topic, message):
        # if the topic is not in the list of topic, return
        # if topic not in self.__topic:
        #     return
        print("Publishing message to topic '{}': {}".format(topic, message))
        self.mqtt_connection.publish(
            topic=topic,
            payload=message,
            qos=mqtt.QoS.AT_LEAST_ONCE)

    def disconnect(self):
        print("Disconnecting...")
        disconnect_future = self.mqtt_connection.disconnect()
        disconnect_future.result()
        print("Disconnected!")      