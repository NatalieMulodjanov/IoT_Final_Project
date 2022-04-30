//Libraries
#include <SPI.h>//https://www.arduino.cc/en/reference/SPI
#include <MFRC522.h>//https://github.com/miguelbalboa/rfid
#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <DHT.h>

//Constants
#define SS_PIN 5
#define RST_PIN 0

#define DHT_SENSOR_PIN 35 // Pin connected to the DHT sensor
#define DHT_SENSOR_TYPE DHT11  // DHT11 or DHT22

const int lightPin = 34; // pin 34

//const char* ssid = "Vladimir Computin 2.4 GHz";                 // Your personal network SSID
//const char* wifi_password = "whatpassword"; // Your personal network password

const char* ssid = "Sarwara";
const char* wifi_password = "Aprajit1";


//const char* ssid = "TP-Link_2AD8";
//const char* password = "14730078";


//const char* mqtt_server = "10.0.0.100";  // IP of the MQTT broker
const char* mqtt_server = "10.0.0.247";

const char* user_rfid_topic = "user_rfid";
const char* light_topic = "light";
const char* temperature_topic = "temperature";
const char* humidity_topic = "humidity";
const char* clientID = "ESP32Client";

// Initialise the WiFi and MQTT Client objects
WiFiClient wifiClient;
// 1883 is the listener port for the Broker
PubSubClient client(mqtt_server, 1883, wifiClient); 

DHT dht(DHT_SENSOR_PIN, DHT_SENSOR_TYPE);

byte nuidPICC[4] = {0, 0, 0, 0};
MFRC522::MIFARE_Key key;
MFRC522 rfid = MFRC522(SS_PIN, RST_PIN);

void setup() {
 //Init Serial USB
 Serial.begin(115200);
 Serial.println(F("Initialize System"));
 setup_wifi();
 SPI.begin();
 dht.begin();
 rfid.PCD_Init();
 Serial.print(F("RFID Reader :"));
 rfid.PCD_DumpVersionToSerial();
}

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, wifi_password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    Serial.print(WiFi.status());
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect(clientID)) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void readLight() {
 // Reading all the values needed for light.
 int lightValue = analogRead(lightPin);
 Serial.print("Light: ");
 Serial.println(lightValue);

 char lightString[8];
 dtostrf(lightValue, 1, 2, lightString);
  
 client.publish("light", lightString);
  
}

void readDHT() {
    float h = dht.readHumidity();
    float t = dht.readTemperature();

    Serial.print("Humidity: ");
    Serial.print(h);
    Serial.println(" %");
    Serial.print("Temperature: ");
    Serial.print(t);
    Serial.println(" *C");

    // MQTT can only transmit strings
    String hs="Hum: "+String((float)h)+" % ";
    String ts="Temp: "+String((float)t)+" C ";

    // PUBLISH to the MQTT Broker (topic = Temperature, defined at the beginning)
    if (client.publish(temperature_topic, String(t).c_str())) {
    Serial.println("Temperature sent!");
    }
    // Again, client.publish will return a boolean value depending on whether it succeded or not.
    // If the message failed to send, we will try again, as the connection may have broken.
    else {
    Serial.println("Temperature failed to send. Reconnecting to MQTT Broker and trying again");
    client.connect(clientID);
    delay(10); // This delay ensures that client.publish doesn't clash with the client.connect call
    client.publish(temperature_topic, String(t).c_str());
    }

    // PUBLISH to the MQTT Broker (topic = Humidity, defined at the beginning)
    if (client.publish(humidity_topic, String(h).c_str())) {
    Serial.println("Humidity sent!");
    }
    // Again, client.publish will return a boolean value depending on whether it succeded or not.
    // If the message failed to send, we will try again, as the connection may have broken.
    else {
    Serial.println("Humidity failed to send. Reconnecting to MQTT Broker and trying again");
    client.connect(clientID);
    delay(10); // This delay ensures that client.publish doesn't clash with the client.connect call
    client.publish(humidity_topic, String(h).c_str());
    }
}

void loop() {
    // put your main code here, to run repeatedly:
    if (!client.connected()) {
    reconnect();
    }
    readLight();
    readRFID();
    //readDHT();

    client.disconnect();  // disconnect from the MQTT broker
    delay(1000*1); 
}

void readRFID(void ) { /* function readRFID */

    Serial.println("Reading RFID");
    ////Read RFID card
    for (byte i = 0; i < 6; i++) {
    key.keyByte[i] = 0xFF;
    }
    // Look for new 1 cards
    if ( ! rfid.PICC_IsNewCardPresent())
    return;
    // Verify if the NUID has been readed
    if (  !rfid.PICC_ReadCardSerial())
    return;
    // Store NUID into nuidPICC array
    for (byte i = 0; i < 4; i++) {
    nuidPICC[i] = rfid.uid.uidByte[i];
    }
    Serial.print(F("RFID In dec: "));
    String result = printDec(rfid.uid.uidByte, rfid.uid.size);
    char buffer[30];
    result.toCharArray(buffer, result.length());
    client.publish(user_rfid_topic, buffer);
    Serial.println();
    // Halt PICC
    rfid.PICC_HaltA();
    // Stop encryption on PCD
    rfid.PCD_StopCrypto1();

}

/**
   Helper routine to dump a byte array as dec values to Serial.
*/
String printDec(byte *buffer, byte bufferSize) {
 String  rfid = "";
 for (byte i = 0; i < bufferSize; i++) {
   rfid = rfid + (buffer[i] < 0x10 ? " 0" : " ");
   rfid = rfid + buffer[i];
 }
 Serial.print(rfid);
 return rfid;
}  
