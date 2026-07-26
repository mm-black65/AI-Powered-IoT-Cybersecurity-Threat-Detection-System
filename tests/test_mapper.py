from backend.feature_mapper import telemetry_to_ml_features

# Sample ESP32 telemetry
telemetry = {
    "temperature": 30.5,
    "humidity": 65,
    "ldr": 850,
    "rssi": -58,
    "heap": 210000,
    "packet_count": 18
}

# Convert to ML features
features = telemetry_to_ml_features(telemetry)

print("\n========== ESP32 Telemetry ==========\n")
print(telemetry)

print("\n========== ML Features ==========\n")

for key, value in features.items():
    print(f"{key:<20} : {value}")

print("\n===================================")
print(f"Total Features Generated : {len(features)}")
print("===================================")