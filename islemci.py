import streamlit as st
from PIL import Image, ImageOps
import io
import os

# --- PANEL AYARLARI ---
st.set_page_config(page_title="Onail Tasarım Hattı", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .stButton>button { background-color: #000000; color: white; border-radius: 10px; width: 100%; height: 3.5em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("💅 Onail Marina Üretim Hattı")

# 1. FORMAT SEÇİMİ
format_secimi = st.radio("İçerik Formatı Seçin", ["Post (1080x1350)", "Story (1080x1920)"], horizontal=True)

# 2. FOTOĞRAF YÜKLEME
yuklenen_dosya = st.file_uploader("Bir fotoğraf yükleyin", type=['jpg', 'jpeg', 'png'])

if yuklenen_dosya:
    try:
        # Görseli aç ve RGB'ye çevir
        img = Image.open(yuklenen_dosya).convert("RGB")
        
        # Boyutlandırma
        hedef_boyut = (1080, 1350) if "Post" in format_secimi else (1080, 1920)
        img = ImageOps.fit(img, hedef_boyut, Image.Resampling.LANCZOS)
        
        # 3. LOGO YERLEŞTİRME
        logo_path = "onail_logo.png"
        if os.path.exists(logo_path):
            logo = Image.open(logo_path).convert("RGBA")
            
            # Logoyu genişliğe göre orantıla
            logo_genislik = hedef_boyut[0]
            oran = logo_genislik / float(logo.size[0])
            logo_yukseklik = int((float(logo.size[1]) * float(oran)))
            logo = logo.resize((logo_genislik, logo_yukseklik), Image.Resampling.LANCZOS)
            
            # Logoyu en alta yapıştır
            img.paste(logo, (0, hedef_boyut[1] - logo_yukseklik), logo)
        else:
            st.error("⚠️ onail_logo.png bulunamadı!")

        # 4. GÖSTERİM VE İNDİRME
        st.divider()
        
        # HATA VEREN KISIM BURADA DÜZELTİLDİ: 
        # use_container_width yerine eski sürüm uyumlu use_column_width kullanıldı.
        st.image(img, use_column_width=True)
        
        # İndirme Hazırlığı
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=95)
        st.download_button(
            label="📥 GÖRSELİ ŞİMDİ İNDİR",
            data=buf.getvalue(),
            file_name=f"onail_{format_secimi.split()[0].lower()}.jpg",
            mime="image/jpeg"
        )
            
    except Exception as e:
        st.error(f"Teknik bir sorun oluştu: {e}")

st.caption("DDS Ajans İş Akışı v2.1")
