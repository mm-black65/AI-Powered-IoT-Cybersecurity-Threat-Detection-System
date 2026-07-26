#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <DHT.h>

//============================
// WiFi Credentials
//============================
const char* ssid = "mahi";
const char* password = "123456788";

//============================
// MQTT
//============================
const char* mqtt_server = "192.168.1.100";   // Replace with your broker IP
const int mqtt_port = 1883;

const char* TELEMETRY_TOPIC = "iot/device01/telemetry";
const char* ALERT_TOPIC     = "iot/device01/alert";

WiFiClient espClient;
PubSubClient client(espClient);

//============================
// DHT11
//============================
#define DHTPIN 4
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

//============================
// LDR (used here as a stand-in "packet activity" sensor if you
// don't have a real network sniffer input — replace later if needed)
//============================
#define LDR_PIN 34

//============================
// Simple failed-login counter (increment this wherever you
// simulate/track failed auth attempts, e.g. a fake login button
// or a serial command for demo purposes)
//============================
int failedLoginCount = 0;

//============================
// WiFi Setup
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

//============================
// MQTT Callback — handles incoming ALERT_TOPIC messages
//============================
void callback(char* topic, byte* payload, unsigned int length)
{
    String message;
    for (unsigned int i = 0; i < length; i++)
    {
        message += (char)payload[i];
    }

    Serial.print("Message arrived on [");
    Serial.print(topic);
    Serial.print("]: ");
    Serial.println(message);

    if (String(topic) == ALERT_TOPIC)
    {
        if (message == "ATTACK")
        {
            Serial.println("!!! ATTACK ALERT RECEIVED !!!");
            // Optional: blink an onboard LED, buzzer, etc.
            // digitalWrite(LED_BUILTIN, HIGH);
        }
        else if (message == "SAFE")
        {
            Serial.println("Status: Safe");
            // digitalWrite(LED_BUILTIN, LOW);
        }
    }
}

//============================
// MQTT Reconnect
//============================
void reconnect()
{
    while (!client.connected())
    {
        Serial.print("Connecting MQTT...");

        if (client.connect("ESP32_Client"))
        {
            Serial.println("Connected");

            // Re-subscribe every time we (re)connect
            client.subscribe(ALERT_TOPIC);
            Serial.print("Subscribed to: ");
            Serial.println(ALERT_TOPIC);
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

    client.setServer(mqtt_server, mqtt_port);
    client.setCallback(callback);
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

    // --- CPU load approximation ---
    // ESP32 has no built-in "CPU %". This is a simple proxy using
    // loop timing; replace/improve later if needed.
    static unsigned long lastLoopTime = 0;
    unsigned long now = millis();
    unsigned long loopDelta = now - lastLoopTime;
    lastLoopTime = now;
    int cpu_usage = constrain(map(loopDelta, 0, 2000, 100, 0), 0, 100);

    // --- Packet rate proxy ---
    // Using LDR reading scaled as a stand-in signal for now.
    // Swap this out once real network-layer counting is added.
    int packet_rate = ldr / 4;

    // --- Build JSON payload matching what feature_mapper.py / app.py expect ---
    StaticJsonDocument<256> doc;

    doc["device"]        = "ESP32";
    doc["temperature"]   = temperature;
    doc["humidity"]      = humidity;
    doc["cpu_usage"]     = cpu_usage;
    doc["wifi_signal"]   = WiFi.RSSI();
    doc["packet_rate"]   = packet_rate;
    doc["failed_login"]  = failedLoginCount;
    doc["heap"]          = ESP.getFreeHeap();
    doc["uptime"]        = millis() / 1000;

    char buffer[256];
    serializeJson(doc, buffer);

    client.publish(TELEMETRY_TOPIC, buffer);

    Serial.println(buffer);

    delay(2000);
}