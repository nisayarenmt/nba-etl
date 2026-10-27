import pandas as pd
import sqlite3
from nba_api.stats.endpoints import leagueleaders

print("1. API üzerinden veriler çekiliyor... (Bu işlem birkaç saniye sürebilir)")

# 2023-24 sezonu verilerini çekiyoruz
leaders = leagueleaders.LeagueLeaders(season='2023-24')
df = leaders.get_data_frames()[0]

print("2. Veriler temizleniyor ve dönüştürülüyor...")

# İhtiyacımız olan sütunları seçiyoruz
gerekli_sutunlar = ['PLAYER_ID', 'PLAYER', 'TEAM', 'GP', 'MIN', 'PTS', 'AST', 'REB']
df_temiz = df[gerekli_sutunlar].copy()

# Sütun isimlerini Türkçeleştirip düzenliyoruz
df_temiz.rename(columns={
    'PLAYER_ID': 'Oyuncu_ID',
    'PLAYER': 'Oyuncu_Adi',
    'TEAM': 'Takim',
    'GP': 'Oynanan_Mac',
    'MIN': 'Sure',
    'PTS': 'Toplam_Sayi',
    'AST': 'Toplam_Asist',
    'REB': 'Toplam_Ribaund'
}, inplace=True)

# Yeni metrik: Maç başına sayı ortalaması
df_temiz['Mac_Basina_Sayi'] = (df_temiz['Toplam_Sayi'] / df_temiz['Oynanan_Mac']).round(2)

print("3. Veriler kaydediliyor...")

# SQL Veritabanına kaydet
baglanti = sqlite3.connect('nba_projesi.db')
df_temiz.to_sql('oyuncu_istatistikleri', baglanti, if_exists='replace', index=False)
baglanti.close()

# CSV olarak kaydet
df_temiz.to_csv('nba_temiz_veri.csv', index=False)

print("Tebrikler! İşlem tamamlandı. Sol taraftaki klasörünü kontrol et.")