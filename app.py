import os
from flask import Flask, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

LOG_FILE = "sensor_data.json"

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
        with open(LOG_FILE, "a") as file:  # "a" modu ile ekleme yapar
            file.write(json.dumps(data) + "\n")
    except Exception as e:
        print(f"⚠️ Hata: {e}")  # Eğer hata alırsan burada görünecek.

@app.route('/')
def home():
    return "Flask API Çalışıyor!"

@app.route('/sensor', methods=['POST'])
def receive_sensor_data():
    """ESP32 veya başka bir cihazdan gelen sensör verisini alır ve kaydeder"""
    data = request.json  # JSON verisini al

    if 'temperature' in data and 'humidity' in data:
        temperature = data['temperature']
        humidity = data['humidity']
        print(f"✅ Alınan Veri -> Sıcaklık: {temperature}°C, Nem: {humidity}%")

        # 📌 Sensör verisini dosyaya kaydet
        save_to_file(temperature, humidity)

        return jsonify({"status": "success", "temperature": temperature, "humidity": humidity}), 200
    else:
        return jsonify({"status": "error", "message": "Eksik veri"}), 400

@app.route('/sensor/latest', methods=['GET'])
def get_latest_sensor_data():
    """Dosyada kayıtlı en son sensör verisini JSON formatında döndürür"""
    try:
        with open(LOG_FILE, "r") as file:
            lines = file.readlines()
            if lines:
                last_entry = json.loads(lines[-1])  # Son JSON kaydını al
                print(f"📌 Son Kaydedilen Veri: {last_entry}")  # Debug için
                return jsonify(last_entry), 200
            else:
                return jsonify({"status": "error", "message": "Henüz veri yok"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)