import paho.mqtt.client as mqtt
import time
import csv

# a callback function
def on_message_uidlookuprequest(client, userdata, msg):
    decoded_payload = msg.payload.decode('utf-8')
    permission_array = load_current_permissions()
    print(permission_array)
    
    
def load_current_permissions():
    with open('Permissions.csv', newline='') as csvfile:
        data = list(csv.reader(csvfile))
    return data

def publish_message(msg):
    client.publish('RFID/uidlookup/answer', payload=msg.encode('utf-8'), qos=0, retain=False)
    info.wait_for_publish()
    time.sleep(2)


# Give a name to this MQTT client
client = mqtt.Client('RFID_UID_Server')
client.message_callback_add('RFID/uidlookup/request', on_message_uidlookuprequest)


# IP address of your MQTT broker, using ipconfig to look up it  
client.connect('192.168.110.11', 1883)
client.subscribe('RFID/#')
client.loop_start()
    
# stop the loop
# client.loop_stop()