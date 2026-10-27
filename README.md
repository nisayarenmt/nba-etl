# 🏀 NBA ETL Pipeline

Resmî NBA istatistik API'sinden oyuncu verilerini çeken, temizleyip dönüştüren ve
hem **SQLite veritabanına** hem **CSV dosyasına** yükleyen uçtan uca bir ETL (Extract–Transform–Load) hattı.

## Akış

```
NBA Stats API  ──►  Extract  ──►  Transform  ──►  Load  ──►  nba_projesi.db (SQLite)
 (nba_api)          (pandas)      (temizleme,             └►  nba_temiz_veri.csv
                                   yeni metrik)
```

1. **Extract:** `nba_api` ile 2023-24 sezonu lider tablosu (`LeagueLeaders`) çekilir.
2. **Transform:**
   - Gerekli sütunlar seçilir (oyuncu, takım, maç, süre, sayı, asist, ribaund)
   - Sütun adları Türkçeleştirilir
   - Yeni metrik hesaplanır: **Maç Başına Sayı** (`Toplam_Sayi / Oynanan_Mac`)
3. **Load:** Veri `oyuncu_istatistikleri` tablosuna (SQLite) ve CSV dosyasına yazılır.

## Teknolojiler

Python · pandas · nba_api · SQLite

## Çıktı şeması: `oyuncu_istatistikleri`

| Sütun | Açıklama |
|---|---|
| `Oyuncu_ID` | NBA oyuncu kimliği |
| `Oyuncu_Adi` | Oyuncu adı |
| `Takim` | Takım kısaltması |
| `Oynanan_Mac` | Oynanan maç sayısı |
| `Sure` | Toplam süre (dakika) |
| `Toplam_Sayi` | Sezon toplam sayı |
| `Toplam_Asist` | Sezon toplam asist |
| `Toplam_Ribaund` | Sezon toplam ribaund |
| `Mac_Basina_Sayi` | Maç başına sayı ortalaması |

Hattın ürettiği örnek çıktılar (572 oyuncu) depoda yer alıyor: `nba_projesi.db` ve `nba_temiz_veri.csv`.

## Kurulum ve çalıştırma

```bash
git clone https://github.com/nisayarenmt/nba-etl.git
cd nba-etl

python -m venv env
# Windows: env\Scripts\activate   |   macOS/Linux: source env/bin/activate
pip install -r requirements.txt

python gercek_pipeline.py
```

## Örnek sorgu

```sql
SELECT Oyuncu_Adi, Takim, Mac_Basina_Sayi
FROM oyuncu_istatistikleri
ORDER BY Mac_Basina_Sayi DESC
LIMIT 5;
```

## Geliştirme fikirleri

- Sezonu komut satırı parametresi olarak almak
- Birden fazla sezonu çekip yıllar arası karşılaştırma yapmak
- Sonuçları bir Streamlit panosunda görselleştirmek
