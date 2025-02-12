from datetime import datetime
import json
import os
import paho.mqtt.client as mqtt
import time

# **MQTT Broker Bilgileri**
MQTT_BROKER = "192.168.1.100"
MQTT_PORT = 1883
HEARTBEAT_TOPIC = "device/heartbeat"
TEMP_TOPIC = "device/temperature"
HUM_TOPIC = "device/humidity"
LOG_FILE = "sensor_data.json"

# **Heartbeat Timeout Süresi**
HEARTBEAT_TIMEOUT = 10  # saniye
last_heartbeat = time.time()

def save_to_file(temperature, humidity):
    """Sensör verisini dosyaya JSON formatında kaydeder"""
    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": temperature,
        "humidity": humidity
    }

    print(f"📌 Dosyaya yazılıyor: {data}")  # Debug için
    print(f" Flask Çalışma Dizini: {os.getcwd()}")

    try:
        with open(LOG_FILE, "a+") as file:  # "a" modu ile ekleme yapar
            file.write(json.dumps(data) + "\n")
    except Exception as e:
        print(f"⚠️ Hata: {e}")  # Eğer hata alırsan burada görünecek.

# **MQTT'den Gelen Mesajları İşleyici**
def on_message(client, userdata, message):
    global last_heartbeat
    topic = message.topic
    payload = message.payload.decode()

    if topic == HEARTBEAT_TOPIC:
        print(f"✅ [HEARTBEAT] Cihaz canlı! - {payload}")
        last_heartbeat = time.time()

    elif topic == TEMP_TOPIC:
        print(f"🌡️ [Sıcaklık] {payload}°C")

    elif topic == HUM_TOPIC:
        print(f"💧 [Nem] {payload}%")
    ## TODO burada jsona yazılacak 





# **MQTT Bağlantı Fonksiyonu**
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ MQTT Broker'a bağlandı!")
        client.subscribe(HEARTBEAT_TOPIC)
        client.subscribe(TEMP_TOPIC)
        client.subscribe(HUM_TOPIC)
    else:
        print(f"❌ Bağlantı hatası! Kod: {rc}")

# **MQTT Client Oluştur**
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)

client.loop_start()

# **Heartbeat Kontrol Mekanizması**
while True:
    current_time = time.time()
    if current_time - last_heartbeat > HEARTBEAT_TIMEOUT:
        print("⚠️ Bağlantı koptu! Cihazdan haber alınamıyor!")
    time.sleep(5)