#include "EspMQTTClient.h"
#include "Adafruit_PN532.h"

#include <SoftwareSerial.h>
#include <PN532_SWHSU.h>
#include <PN532.h>
#include <NfcAdapter.h>


EspMQTTClient client(
  "maglab",//"TRON-IoT",
  "Nu5gnWiFi",//"?!Z^e=58pFbV?E53",
  "localhost",  // MQTT Broker server ip
  "",   // Can be omitted if not needed
  "",   // Can be omitted if not needed
  "MQTTClientDOOR"      // Client name that uniquely identify your device
);

  SoftwareSerial scanner(D2, D1); // RX | TX  
  PN532_SWHSU pn532hsu(scanner);
  PN532 nfc = PN532(pn532hsu);
  
void setup(void) {
  Serial.begin(115200);
  Serial.println("Hello!");

  nfc.begin();

  uint32_t versiondata = nfc.getFirmwareVersion();
  if (! versiondata) {
    Serial.print("Didn't find PN53x board");
    while (1); // halt
  }
  
  // Got ok data, print it out!
  Serial.print("Found chip PN5"); Serial.println((versiondata>>24) & 0xFF, HEX); 
  Serial.print("Firmware ver. "); Serial.print((versiondata>>16) & 0xFF, DEC); 
  Serial.print('.'); Serial.println((versiondata>>8) & 0xFF, DEC);
  
  // Set the max number of retry attempts to read from a card
  // This prevents us from waiting forever for a card, which is
  // the default behaviour of the PN532.
  nfc.setPassiveActivationRetries(0xFF);
  
  // configure board to read RFID tags
  nfc.SAMConfig();
    
  Serial.println("Waiting for an ISO14443A card");
}

void onConnectionEstablished() {

  client.subscribe("RFID/test", [] (const String &payload)  {
    Serial.println(payload);
  });
  client.subscribe("RFID/uidlookup/answer", [] (const String &payload) {
    if (payload == "uid validated") {
      Serial.println("uid validated");
    }
    else if (payload == "uid not validated") {
      Serial.println("uid not validated");
    }
    else if (payload == "open door") {
      Serial.println("open door");
    }
    else {
      Serial.println("och nö hat net funktioniert");
    }
  });

  client.publish("RFID/test", "This is a message");
}

void loop(void) {
  boolean success;
  uint8_t uid[] = { 0, 0, 0, 0, 0, 0, 0 };  // Buffer to store the returned UID
  uint8_t uidLength;                        // Length of the UID (4 or 7 bytes depending on ISO14443A card type)
  
  
  // Wait for an ISO14443A type cards (Mifare, etc.).  When one is found
  // 'uid' will be populated with the UID, and uidLength will indicate
  // if the uid is 4 bytes (Mifare Classic) or 7 bytes (Mifare Ultralight)
  success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, &uid[0], &uidLength);
  
  if (success) {
    char uidc[uidLength];
    Serial.println("Found a card!");
    Serial.print("UID Length: ");Serial.print(uidLength, DEC);Serial.println(" bytes");
    Serial.print("UID Value: ");
    for (uint8_t i=0; i < uidLength; i++) 
    {
      Serial.print(" 0x");Serial.print(uid[i], HEX); 
      uidc[i] = char(uid[i]);
    }
    Serial.println("");
    client.publish("RFID/test", String(uidc));
    // Wait 1 second before continuing
    delay(2000);
  }
  else
  {
    // PN532 probably timed out waiting for a card
    Serial.println("Timed out waiting for a card");
  }

}








//void onConnectionEstablished() {

//  client.subscribe("mytopic/test", [] (const String &payload)  {
//    Serial.println(payload);
//  });

//  client.publish("mytopic/test", "This is a message");
//}

//void loop() {
//  client.loop();
//}
