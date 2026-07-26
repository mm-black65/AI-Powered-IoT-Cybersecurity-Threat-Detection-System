def telemetry_to_ml_features(data: dict) -> dict:
    """
    Convert ESP32 telemetry into the 38-feature format expected
    by the trained ML model (matches the CICIoT2023-style schema
    used in feature_mapper's original hardcoded sample).
    """

    packet_rate = float(data.get("packet_rate", 10))
    failed_login = int(data.get("failed_login", 0))
    wifi_signal = float(data.get("wifi_signal", -50))
    cpu_usage = float(data.get("cpu_usage", 20))
    heap = float(data.get("heap", 200000))

    # --- Derive proxy flags from telemetry ---
    # High failed_login count is treated as a signal for SYN-like /
    # brute-force flag activity (heuristic, not a real packet flag read).
    syn_flag_number = 1 if failed_login > 0 or packet_rate > 200 else 0
    rst_flag_number = 1 if failed_login > 5 else 0
    ack_flag_number = 1 if packet_rate > 50 else 0

    # High packet_rate relative to a "normal" baseline (~50) suggests flood-like traffic
    is_flood_like = packet_rate > 200

    # Weak/degrading wifi_signal (very negative dBm) can correlate with
    # deauth-style disruption, used as a light-weight proxy signal.
    signal_degraded = wifi_signal < -75

    features = {
        "flow_duration": 0,
        "Header_Length": 54,
        "Protocol Type": 6,          # TCP by convention here
        "Duration": 64,
        "Rate": packet_rate,
        "Srate": packet_rate,

        "fin_flag_number": 0,
        "syn_flag_number": syn_flag_number,
        "rst_flag_number": rst_flag_number,
        "psh_flag_number": 1 if is_flood_like else 0,
        "ack_flag_number": ack_flag_number,

        "ack_count": 1 if ack_flag_number else 0,
        "syn_count": failed_login,
        "fin_count": 0,
        "urg_count": 0,
        "rst_count": 1 if rst_flag_number else 0,

        "HTTP": 0,
        "HTTPS": 0,
        "DNS": 0,

        "TCP": 1,
        "UDP": 0,
        "ARP": 1 if signal_degraded else 0,
        "ICMP": 0,

        "IPv": 1,
        "LLC": 1,

        "Tot sum": packet_rate * 60,
        "Min": 60,
        "Max": 60 if not is_flood_like else 1500,
        "AVG": 60,
        "Std": 0 if not is_flood_like else 200,

        "Tot size": packet_rate * 60,
        "IAT": 0 if is_flood_like else 100,   # flood traffic = near-zero gaps between packets
        "Number": max(1, int(packet_rate / 25)),

        "Magnitue": 60,
        "Radius": 0,
        "Covariance": 0,
        "Variance": cpu_usage,       # proxy: higher CPU load under attack = higher variance signal
        "Weight": max(1.0, 15000 / max(heap, 1)),  # lower free heap -> higher "weight" signal
    }

    return features


if __name__ == "__main__":
    # Quick manual test with sample telemetry
    sample_telemetry = {
        "temperature": 31,
        "humidity": 55,
        "cpu_usage": 78,
        "wifi_signal": -80,
        "packet_rate": 450,
        "failed_login": 6,
        "heap": 90000,
    }

    features = telemetry_to_ml_features(sample_telemetry)
    for k, v in features.items():
        print(f"{k}: {v}")