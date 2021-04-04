import paho.mqtt.client as mqtt
import ssl

client=mqtt.Client()

client.connect("test.mosquitto.org", port=1883)

client.publish("IC.embedded/Power_Puff_Girls/test", "15 feb 2021")

# mqtt.error_string(MSG_INFO.rc) #MSG_INFO is result of publish()

client.tls_set(ca_certs="mosquitto.org.crt",
certfile="client.crt",keyfile="client.key",
tls_version=ssl.PROTOCOL_TLSv1_2)

def on_message(client,userdata,message):
    print("Received message:{} on topic{}".format(message.payload, message.topic))

client.on_message=on_message

client.subscribe("IC.embedded/Power_Puff_Girls/#")

client.loop()
