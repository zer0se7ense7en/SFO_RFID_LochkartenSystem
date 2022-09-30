from math import perm
import paho.mqtt.client as mqtt
import time
import csv

# a callback function
def on_message_uidlookuprequest(client, userdata, msg):
    
    decoded_payload = msg.payload.decode('utf-8') # decode the payload uid
    permission_list = load_current_permissions() # load csv file into a list[][]
    print(permission_list) # print it for debugging
    
    for i in range(len(permission_list)):
        if permission_list[i][0] == decoded_payload: # compare all uids to uid in decoded payload
            # if uid has been found
            if permission_list[i][3] == '1': # check if the uid also got the access bit linked
                # if uid is related to Accessbit 1: OPEN DOOR
                write_to_log(permission_list[i][0],permission_list[i][2]) # write uid and ownername to log via write_to_log function
                publish_message_answer('open door') # give answer via mqtt to open the door BLUE FLASHING LIGHT
                print('door opened for', permission_list[i][2]) # debugging
            else: # otherwise just log the owner in the logfile
                write_to_log(permission_list[i][0],permission_list[i][2]) # write uid and ownername to log via write_to_log function
                publish_message_answer('uid validated') # feedback via mqtt for GREEN LED
                print('valid uid presented', permission_list[i][0],permission_list[i][2]) # debugging
                
        else: # UID NOT FOUND
            write_to_log('unknown UID','unknown owner') # write to logfile that an unkown card got scanned
            publish_message_answer('uid not validated') # give answer via mqtt for RED LIGHT
            print('unkown uid: ', decoded_payload) # debugging

    # [rows][columns]
    
def load_current_permissions(): # load currrent permissions from permissions.csv file
    with open('Permissions.csv', newline='') as csvfile:
        data = list(csv.reader(csvfile))
    return data # and return them as a list

def write_to_log(uid,currentowner): # write the log info to the log file
    time = time.ctime()
    fields = [time,uid,currentowner]
    with open('log.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)

def publish_message_answer(msg):
    client.publish('RFID/uidlookup/answer', payload=msg.encode('utf-8'), qos=0, retain=False)


# Give a name to this MQTT client
client = mqtt.Client('RFID_UID_Server')
client.message_callback_add('RFID/uidlookup/request', on_message_uidlookuprequest)


# IP address of your MQTT broker, using ipconfig to look up it  
client.connect('192.168.110.10', 1883)
client.subscribe('RFID/#')
client.loop_start()
    
# stop the loop
# client.loop_stop()

#
#   TO DO:
#   - test: everything ^^
#   - implement: check for already scannned in logs and give feedback ORANGE LIGHT / GREEN FLASHING LIGHT
#   - better time format