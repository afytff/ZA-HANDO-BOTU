import os
import requests
from flask import Flask, render_template_string

app = Flask(__name__)

# Wolvesville API Bilgilerin
# Güvenlik için Render panelinde tanımlayacağımız gizli değişkenleri çeker
BOT_TOKEN = os.environ.get("BOT_TOKEN", "BURAYA_GİZLİ_TOKENİ_YAZABİLİRSİN")
CLAN_ID = os.environ.get("CLAN_ID", "BURAYA_KLAN_ID_YAZABİLİRSİN")

@app.route('/')
def klan_paneli():
    url = f"https://api.wolvesville.com/clans/{CLAN_ID}"
    headers = {
        "Authorization": f"Bot {BOT_TOKEN}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            klan_verisi = response.json()
            
            html_tasarimi = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Za Hando Klan Paneli</title>
                <style>
                    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #121212; color: #e0e0e0; text-align: center; padding: 50px; margin: 0; }
                    .card { background: linear-gradient(145deg, #1e1e1e, #252525); padding: 30px; border-radius: 15px; display: inline-block; box-shadow: 0 8px 16px rgba(0,0,0,0.6); border: 1px solid #333; max-width: 400px; width: 100%; }
                    h1 { color: #ffcc00; margin-bottom: 20px; font-size: 28px; text-transform: uppercase; letter-spacing: 2px; }
                    .info { font-size: 18px; margin: 15px 0; padding-bottom: 10px; border-bottom: 1px solid #2d2d2d; text-align: left; }
                    .info strong { color: #ffcc00; }
                    .footer { margin-top: 20px; font-size: 12px; color: #666; }
                </style>
            </head>
            <body>
                <div class="card">
                    <h1>🛡️ {{ veri.get('name', 'Klan Adı') }} 🛡️</h1>
                    <div class="info"><strong>Açıklama:</strong> {{ veri.get('description', 'Yok') }}</div>
                    <div class="info"><strong>Mevcut XP:</strong> {{ veri.get('xp', 0) }}</div>
                    <div class="info"><strong>Üye Sayısı:</strong> {{ veri.get('memberCount', 0) }} / 50</div>
                    <div class="footer">Za Hando Klan Bot Altyapısı</div>
                </div>
            </body>
            </html>
            """
            return render_template_string(html_tasarimi, veri=klan_verisi)
        else:
            return f"Wolvesville API hatası! Kod: {response.status_code}"
    except Exception as e:
        return f"Bir hata oluştu: {str(e)}"

if __name__ == '__main__':
    # Render'ın port ayarını otomatik alması için gerekli
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
