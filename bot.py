import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Eskişehir Odunpazarı / Uluçayır Yaklaşık Koordinatları
LAT = 39.75
LON = 30.50

def get_weather():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max&current_weather=true&timezone=Europe%2FIstanbul"
    
    try:
        resp = requests.get(url, timeout=10).json()
        
        # Anlık Hava
        current_temp = resp['current_weather']['temperature']
        wind_speed = resp['current_weather']['windspeed']
        
        # Günlük Tahminler (Bugün)
        today_max = resp['daily']['temperature_2m_max'][0]
        today_min = resp['daily']['temperature_2m_min'][0]
        rain_sum = resp['daily']['precipitation_sum'][0]
        
        # Zirai Don Kontrolü
        don_uyarisi = ""
        if today_min <= 0:
            don_uyarisi = "🚨 <b>DİKKAT: ŞİDDETLİ ZİRAİ DON RİSKİ!</b> (Sıcaklık 0°C veya altında!)\n\n"
        elif today_min <= 3:
            don_uyarisi = "⚠️ <b>UYARI: Hafif Zirai Don/Hafif Kırağı Riski!</b>\n\n"
        else:
            don_uyarisi = "✅ <b>Zirai Don Riski Yok.</b>\n\n"
            
        # Yağış Durumu
        yagis_metni = f"☔ <b>Beklenen Yağış:</b> {rain_sum} mm\n" if rain_sum > 0 else "☀️ <b>Yağış Beklenmiyor.</b>\n"
        
        msg = (
            f"🌾 <b>ESKİŞEHİR ZİRAİ & İKLİM HAVA RAPORU</b> 🌾\n\n"
            f"{don_uyarisi}"
            f"🌡️ <b>Anlık Sıcaklık:</b> {current_temp}°C\n"
            f"📈 <b>Günün En Yüksek:</b> {today_max}°C\n"
            f"📉 <b>Günün En Düşük:</b> {today_min}°C\n"
            f"💨 <b>Rüzgar Hızı:</b> {wind_speed} km/s\n"
            f"{yagis_metni}"
        )
        return msg
    except Exception as e:
        print(f"Hava durumu çekilemedi: {e}")
        return None

def send_telegram(message):
    if not message:
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, data=payload, timeout=10)

if __name__ == "__main__":
    report = get_weather()
    send_telegram(report)
