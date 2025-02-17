import os
from flask import Flask, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

LOG_FILE = "sensor_data.json"

# 📌 Eğer dosya yoksa, boş bir JSON listesiyle oluştur
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as file:
        json.dump([], file)

def save_to_file(temperature, humidity):
    """Sensör verisini JSON formatında kaydeder"""
    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": temperature,
        "humidity": humidity
    }

    print(f"📌 Dosyaya yazılacak veri: {data}")
    print(f"📂 Flask Çalışma Dizini: {os.getcwd()}")

    try:
        with open(LOG_FILE, "r+") as file:
            try:
                records = json.load(file)  # 📌 Mevcut verileri oku
            except json.JSONDecodeError:
                records = []  # 📌 Eğer JSON hatalıysa, yeni bir liste başlat

            records.append(data)  # 📌 Yeni veriyi listeye ekle
            file.seek(0)  # 📌 Dosyanın başına git
            json.dump(records, file, indent=4)  # 📌 JSON formatında tekrar yaz
            file.truncate()  # 📌 Eski verileri silip yeni JSON'u yaz
        print("✅ Veri dosyaya başarıyla yazıldı!")
    except Exception as e:
        print(f"⚠️ Dosyaya yazma hatası: {e}")

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
            records = json.load(file)  # 📌 Tüm kayıtları oku
            if records:
                last_entry = records[-1]  # 📌 Son JSON kaydını al
                print(f"📌 Son Kaydedilen Veri: {last_entry}")
                return jsonify(last_entry), 200
            else:
                return jsonify({"status": "error", "message": "Henüz veri yok"}), 404
    except json.JSONDecodeError:
        return jsonify({"status": "error", "message": "Dosya bozuk veya JSON hatası"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)