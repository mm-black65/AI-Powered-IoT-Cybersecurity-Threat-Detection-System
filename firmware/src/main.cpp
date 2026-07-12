#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <DHT.h>

//============================
// WiFi Credentials
//============================
const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";

//============================
// MQTT
//============================
const char* mqtt_server = "192.168.1.100";   // Replace with YOUR PC IP

WiFiClient espClient;
PubSubClient client(espClient);

//============================
// DHT11
//============================
#define DHTPIN 4
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

//============================
// LDR
//============================
#define LDR_PIN 34

//============================

void setupWiFi()
{
    Serial.println();
    Serial.print("Connecting to WiFi");

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }

    Serial.println("\nConnected!");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
}

void reconnect()
{
    while (!client.connected())
    {
        Serial.print("Connecting MQTT...");

        if (client.connect("ESP32_Client"))
        {
            Serial.println("Connected");
        }
        else
        {
            Serial.print("Failed rc=");
            Serial.print(client.state());
            Serial.println(" Retry...");
            delay(2000);
        }
    }
}

void setup()
{
    Serial.begin(115200);

    dht.begin();

    setupWiFi();

    client.setServer(mqtt_server, 1883);
}

void loop()
{
    if (!client.connected())
    {
        reconnect();
    }

    client.loop();

    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();

    int ldr = analogRead(LDR_PIN);

    StaticJsonDocument<256> doc;

    doc["device"] = "ESP32";
    doc["temperature"] = temperature;
    doc["humidity"] = humidity;
    doc["ldr"] = ldr;
    doc["rssi"] = WiFi.RSSI();
    doc["heap"] = ESP.getFreeHeap();
    doc["uptime"] = millis()/1000;

    char buffer[256];

    serializeJson(doc, buffer);

    client.publish("iot/telemetry", buffer);

    Serial.println(buffer);

    delay(2000);
}