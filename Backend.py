import paho.mqtt.client as mqtt
import time


# a callback function
def on_message_uidlookuprequest(client, userdata, msg):
    # Message is an object and the payload property contains the message data which is binary data.
    # The actual message payload is a binary buffer. 
    # In order to decode this payload you need to know what type of data was sent.
    # If it is JSON formatted data then you decode it as a string and then decode the JSON string as follows:
    # decoded_message=str(message.payload.decode("utf-8")))
    # msg=json.loads(decoded_message)
    print('Received a new UID lookup request ', str(msg.payload.decode('utf-8')))
    print('message topic=', msg.topic)
    decoded_payload = msg.payload.decode('utf-8')
    



# Give a name to this MQTT client
client = mqtt.Client('RFID_UID_Server')
client.message_callback_add('RFID/uidlookup/request', on_message_uidlookuprequest)
client.message_callback_add('RFID/uidlookup/answer', on_message_uidlookupanswer)


# IP address of your MQTT broker, using ipconfig to look up it  
client.connect('192.168.110.11', 1883)
client.subscribe('RFID/#')
client.loop_start()

def ()
msg = "UID accepted"
client.publish('RFID/uidlookup', payload=msg.encode('utf-8'), qos=0, retain=False)

while True:
    msg = "UID accepted"
    info = client.publish(
        topic='RFID/uidlookup',
        payload=msg.encode('utf-8'),
        qos=0,
    )
    # Because published() is not synchronous,
    # it returns false while he is not aware of delivery that's why calling wait_for_publish() is mandatory.
    info.wait_for_publish()
    print(info.is_published())
    time.sleep(3)
    
# stop the loop
# client.loop_stop()