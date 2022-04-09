#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#define LIGHT_SENSOR_PIN 34 // ESP32 pin GIOP34 (ADC0)


// Replace the next variables with your SSID/Password comValbination
//const char* ssid = "TP-Link_2AD8";
//const char* password = "14730078";

const char* ssid = "Sarwara";
const char* password = "Aprajit1";

// Add your MQTT Broker IP address, example
//const char* mqtt_server = "192.168.0.189";
const char* mqtt_server = "10.0.0.248";


WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
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
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

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

  // Feel free to add more if statements to control more GPIOs with MQTT

  // If a message is received on the topic esp32/output, you check if the message is either "on" or "off". 
  // Changes the output state according to the message
//  if (String(topic) == "esp32/output") {
//    Serial.print("Changing output to ");
//    if(messageTemp == "on"){
//      Serial.println("on");
//      digitalWrite(ledPin, HIGH);
//    }
//    else if(messageTemp == "off"){
//      Serial.println("off");
//      digitalWrite(ledPin, LOW);
    }
//  }
//}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");
      // Subscribe
      client.subscribe("esp32/output");
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
  client.loop();
  
  int analogValue = getLight();
  
  delay(1000);
 
  char lightString[8];
  dtostrf(analogValue, 1, 2, lightString);

  client.publish("light", lightString);

}

int getLight(){
  return analogRead(LIGHT_SENSOR_PIN);
}



  
