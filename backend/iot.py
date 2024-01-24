import car as functions
import time
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import json,sys
import logging,threading


logging.basicConfig(filename="car.log",format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
received_count = 0
received_all_event = threading.Event()

client_id="qwertcgh"
endpoint = "a306k6kli6x56q-ats.iot.ap-south-1.amazonaws.com"
thing_name = "car"
port = 8883
root_ca = "certificates/AmazonRootCA1.pem"
cert = "certificates/7a6638708c7cae9634d3d68d2be6a978e93d800336aa4869334ce4501db9de81-certificate.pem.crt"
key= "certificates/7a6638708c7cae9634d3d68d2be6a978e93d800336aa4869334ce4501db9de81-private.pem.key"


template={
    "start":functions.start_engine,
    "stop":functions.stop_engine,
    "accelerate":functions.accelerate,
    "break":functions.brake,
    "steer":functions.steer,
    "relaese":functions.release_steer,
    "reverse":functions.reverse
    }






def on_connection_interrupted(connection, error, **kwargs):
   
    logger.info(connection)
    logger.info("Disconnected  due to no network",error)

def on_connection_resumed(connection, return_code, session_present, **kwargs):


    if return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present:
        resubscribe_future, _ = connection.resubscribe_existing_topics()

        resubscribe_future.add_done_callback(on_resubscribe_complete)
    print("Reconnect Sucessfull")


def on_resubscribe_complete(resubscribe_future):
        resubscribe_results = resubscribe_future.result()
        logger.info("Resubscribe results: {}".format(resubscribe_results))

        for topic, qos in resubscribe_results['topics']:
            if qos is None:
                sys.exit("Server rejected resubscribe to topic: {}".format(topic))

def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    payload = payload.decode('utf-8')
    logger.info("Received message from topic '{}': {}".format(topic, str(payload)))
    message = json.loads(str(payload))
    try:

        template[message["command"]]()

    except Exception as e:
        print("Error in car")



if __name__=="__main__":
    global connection
    while True:
        try:
          
            event_loop_group = io.EventLoopGroup(1)
            host_resolver = io.DefaultHostResolver(event_loop_group)
            client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

            proxy_options = None
            if False:
                proxy_options = http.HttpProxyOptions(host_name=args.proxy_host, port=args.proxy_port)

            if False:
                credentials_provider = auth.AwsCredentialsProvider.new_default_chain(client_bootstrap)
                mqtt_connection = mqtt_connection_builder.websockets_with_default_aws_signing(
                    endpoint=endpoint,
                    client_bootstrap=client_bootstrap,
                    region="ap-south-1",
                    credentials_provider=credentials_provider,
                    http_proxy_options=proxy_options,
                    ca_filepath=root_ca,
                    on_connection_interrupted=on_connection_interrupted,
                    on_connection_resumed=on_connection_resumed,
                    client_id=client_id,
                    clean_session=False,
                    keep_alive_secs=30)

            else:
                mqtt_connection = mqtt_connection_builder.mtls_from_path(
                    endpoint=endpoint,
                    port=port,
                    cert_filepath=cert,
                    pri_key_filepath=key,
                    client_bootstrap=client_bootstrap,
                    ca_filepath=root_ca,
                    on_connection_interrupted=on_connection_interrupted,
                    on_connection_resumed=on_connection_resumed,
                    client_id=client_id,
                    clean_session=False,
                    keep_alive_secs=30,
                    http_proxy_options=proxy_options)

            logger.info("Connecting to {} with client ID '{}'...".format(
                endpoint, client_id))

            connect_future = mqtt_connection.connect()
         

            break
        except Exception as e:
         
            logger.info(f"Exception occured: {e}")
        time.sleep(15)

    logger.info("Connected!")


    topic="aws/things/car/shadow/1/accepted"
    subscribe_future, packet_id = mqtt_connection.subscribe(
        topic=topic,
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_message_received)
    logger.info("Subscribing to topic '{}'...".format(topic))
    while subscribe_future.done is not True:
        logger.info(subscribe_future)
        logger.info(subscribe_future.done)
        time.sleep(3)


    connection=mqtt_connection
    logger.info("Done")
    count=10
    if count != 0 and not received_all_event.is_set():
        logger.info("Waiting for all messages to be received...")

    received_all_event.wait()
    logger.info("{} message(s) received.".format(received_count))


    logger.info("Disconnecting...")
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    logger.info("Disconnected!")
