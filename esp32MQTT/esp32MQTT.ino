#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <DHT.h>

#define DHT_SENSOR_PIN 35 // Pin connected to the DHT sensor
#define DHT_SENSOR_TYPE DHT11  // DHT11 or DHT22
DHT dht(DHT_SENSOR_TYPE, DHT_SENSOR_TYPE);

const int lightPin = 34; // pin 34

// Replace the next variables with your SSID/Password comValbination
const char* ssid = "TP-Link_2AD8";
const char* password = "14730078";

//const char* ssid = "Patrick Starfish";
//const char* password = "mankirat1";

//const char* ssid = "Sarwara";
//const char* password = "Aprajit1";

//const char* ssid = "Vladimir Computin 2.4 GHz";
//const char* password = "whatpassword";

// Add your MQTT Broker IP address, example
const char* mqtt_server = "192.168.0.189";
//const char* mqtt_server = "10.0.0.100";
//const char* mqtt_server = "10.0.0.247";
//const char* mqtt_server = "172.20.10.4";


WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(2400);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

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

//prints the message and depending on the message, turns the led on or off.
void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();
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
 // put your main code here, to run repeatedly:
  if (!client.connected()) {
    reconnect();
  }

 // Reading all the values needed.
 int lightValue = analogRead(lightPin);
 Serial.print("Light: ");
 Serial.println(lightValue);

 char lightString[8];
 dtostrf(lightValue, 1, 2, lightString);
  
 client.publish("light", lightString);
  
 client.disconnect();  // disconnect from the MQTT broker
 delay(1000*1);       // print new values every 1 Second

}



  
