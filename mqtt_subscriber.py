import paho.mqtt.client as mqtt

# MQTT callback fonksiyonları
def on_connect(client, userdata, flags, rc):
    print("Bağlandı! Kod: " + str(rc))
    client.subscribe("sensor/mq3")  # "sensor/mq3" topic'ini dinle

def on_message(client, userdata, msg):
    print(f"Gelen mesaj: {msg.payload.decode()}")

# MQTT istemcisi oluştur
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# MQTT broker'a bağlan
client.connect("192.168.1.100", 1883, 60)  # Raspberry Pi'nin IP adresi

# Mesaj döngüsünü başlat
client.loop_forever()