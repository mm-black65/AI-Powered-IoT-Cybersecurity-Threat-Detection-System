#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <DHT.h>

// ===========================
// WiFi Credentials
// ===========================
const char* ssid = "xxx"; //Replace
const char* password = "xxx"; //Replace

// ===========================
// MQTT Broker
// ===========================
const char* mqtt_server = "xxx"; //Replace
const int mqtt_port = 1883;

// ===========================
// MQTT Topics
// ===========================
const char* telemetry_topic = "iot/device01/telemetry";
const char* alert_topic = "iot/device01/alert";

// ===========================
// Pin Configuration
// ===========================
#define DHTPIN 4
#define DHTTYPE DHT11

#define LDR_PIN 34
#define LED_PIN 2
#define BUZZER_PIN 27

// ===========================

DHT dht(DHTPIN, DHTTYPE);

WiFiClient espClient;
PubSubClient client(espClient);

unsigned long packetCount = 0;

// ===================================================
// MQTT Callback
// ===================================================

void callback(char* topic, byte* payload, unsigned int length)
{
    String message = "";

    for (unsigned int i = 0; i < length; i++)
    {
        message += (char)payload[i];
    }

    Serial.println();
    Serial.print("Alert Received : ");
    Serial.println(message);

    if (message == "ATTACK")
    {
        Serial.println(">>> ATTACK DETECTED <<<");

        digitalWrite(LED_PIN, HIGH);

        for (int i = 0; i < 3; i++)
        {
            digitalWrite(BUZZER_PIN, HIGH);
            delay(200);
            digitalWrite(BUZZER_PIN, LOW);
            delay(200);
        }
    }
    else if (message == "SAFE")
    {
        Serial.println("System Safe");

        digitalWrite(LED_PIN, LOW);
        digitalWrite(BUZZER_PIN, LOW);
    }
}

// ===================================================
// WiFi
// ===================================================

void connectWiFi()
{
    Serial.print("Connecting to WiFi");

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED)
    {
        Serial.print(".");
        delay(500);
    }

    Serial.println();

    Serial.println("WiFi Connected");
    Serial.print("IP Address : ");
    Serial.println(WiFi.localIP());
}

// ===================================================
// MQTT
// ===================================================

void reconnectMQTT()
{
    while (!client.connected())
    {
        String clientId = "ESP32-";
        clientId += String((uint32_t)ESP.getEfuseMac(), HEX);

        Serial.print("Connecting MQTT...");

        if (client.connect(clientId.c_str()))
        {
            Serial.println("Connected");

            client.subscribe(alert_topic);

            Serial.println("Subscribed to alert topic");
        }
        else
        {
            Serial.print("Failed. State=");
            Serial.println(client.state());

            delay(3000);
        }
    }
}

// ===================================================

void setup()
{
    Serial.begin(115200);

    pinMode(LED_PIN, OUTPUT);
    pinMode(BUZZER_PIN, OUTPUT);

    digitalWrite(LED_PIN, LOW);
    digitalWrite(BUZZER_PIN, LOW);

    dht.begin();

    connectWiFi();

    client.setServer(mqtt_server, mqtt_port);
    client.setCallback(callback);
}

// ===================================================

void loop()
{
    if (WiFi.status() != WL_CONNECTED)
    {
        Serial.println("WiFi Lost");

        connectWiFi();
    }

    if (!client.connected())
    {
        reconnectMQTT();
    }

    client.loop();

    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();

    if (isnan(temperature) || isnan(humidity))
    {
        Serial.println("Failed to read DHT11");
        delay(2000);
        return;
    }

    int ldr = analogRead(LDR_PIN);

    packetCount++;

    StaticJsonDocument<512> doc;

    doc["device"] = "ESP32_Device01";

    doc["temperature"] = temperature;
    doc["humidity"] = humidity;
    doc["ldr"] = ldr;

    doc["rssi"] = WiFi.RSSI();
    doc["wifi_channel"] = WiFi.channel();

    doc["heap"] = ESP.getFreeHeap();
    doc["min_heap"] = ESP.getMinFreeHeap();

    doc["uptime"] = millis() / 1000;

    doc["packet_count"] = packetCount;

    doc["ip"] = WiFi.localIP().toString();
    doc["mac"] = WiFi.macAddress();

    char buffer[512];

    serializeJson(doc, buffer);

    if (client.publish(telemetry_topic, buffer))
    {
        Serial.println("-------------------------------");
        Serial.println("Telemetry Published");
        Serial.println(buffer);
    }
    else
    {
        Serial.println("Publish Failed");
    }

    delay(5000);
}