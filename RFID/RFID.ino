//Libraries
#include <SPI.h>//https://www.arduino.cc/en/reference/SPI
#include <MFRC522.h>//https://github.com/miguelbalboa/rfid
#include <WiFi.h>
#include <PubSubClient.h>

//Constants
#define SS_PIN 27
#define RST_PIN 25

//Parameters
//const int ipaddress[4] = {103, 97, 67, 25};

//Variables
byte nuidPICC[4] = {0, 0, 0, 0};
MFRC522::MIFARE_Key key;
MFRC522 rfid = MFRC522(SS_PIN, RST_PIN);

// WiFi
const char* ssid = "Vladimir Computin 2.4 GHz";                 // Your personal network SSID
const char* wifi_password = "whatpassword"; // Your personal network password

// MQTT
const char* mqtt_server = "10.0.0.100";  // IP of the MQTT broker
const char* user_rfid_topic = "user_rfid";
//const char* mqtt_username = "cdavid"; // MQTT username
//const char* mqtt_password = "cdavid"; // MQTT password
const char* clientID = "Client"; // MQTT client ID

// Initialise the WiFi and MQTT Client objects
WiFiClient wifiClient;
// 1883 is the listener port for the Broker
PubSubClient client(mqtt_server, 1883, wifiClient); 


void setup() {
 //Init Serial USB
 Serial.begin(115200);
 Serial.println(F("Initialize System"));
 setup_wifi();
 SPI.begin();
 rfid.PCD_Init();
 Serial.print(F("Reader :"));
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
    if (client.connect("ESP8266Client")) {
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

void loop() {
  if (!client.connected()) {
    reconnect();
  }
 readRFID();
}

void readRFID(void ) { /* function readRFID */
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
   Helper routine to dump a byte array as hex values to Serial.
*/
void printHex(byte *buffer, byte bufferSize) {
 for (byte i = 0; i < bufferSize; i++) {
   Serial.print(buffer[i] < 0x10 ? " 0" : " ");
   Serial.print(buffer[i], HEX);
 }
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
