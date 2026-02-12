import streamlit as st
from PIL import Image, ImageOps
import io
import os

# --- PANEL AYARLARI ---
st.set_page_config(page_title="Onail Tasarım Hattı", page_icon="💅", layout="centered")

# Meta Business Suite Estetiği (Sadeleştirilmiş)
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .stButton>button { background-color: #000000; color: white; border-radius: 10px; width: 100%; height: 3.5em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("💅 Onail Marina Üretim Hattı")
st.subheader("Hızlı Görsel Hazırlama Paneli (V2.0)")

# 1. ADIM: FORMAT SEÇİMİ
format_secimi = st.radio("İçerik Formatı Seçin", ["Post (1080x1350)", "Story (1080x1920)"], horizontal=True)

# 2. ADIM: FOTOĞRAF YÜKLEME
yuklenen_dosya = st.file_uploader("Bir fotoğraf yükleyin", type=['jpg', 'jpeg', 'png'], label_visibility="collapsed")

if yuklenen_dosya:
    try:
        # Görseli aç ve standart formata getir (iPhone/Android uyumu)
        img = Image.open(yuklenen_dosya).convert("RGB")
        
        # Seçilen formata göre tam boyutlandırma (Fit)
        hedef_boyut = (1080, 1350) if "Post" in format_secimi else (1080, 1920)
        img = ImageOps.fit(img, hedef_boyut, Image.Resampling.LANCZOS)
        
        # 3. ADIM: LOGO YERLEŞTİRME (DİNAMİK)
        logo_path = "onail_logo.png"
        if os.path.exists(logo_path):
            logo = Image.open(logo_path).convert("RGBA")
            
            # Logoyu genişliğe göre orantıla (1080px genişliğe yay)
            logo_genislik = hedef_boyut[0]
            oran = logo_genislik / float(logo.size[0])
            logo_yukseklik = int((float(logo.size[1]) * float(oran)))
            logo = logo.resize((logo_genislik, logo_yukseklik), Image.Resampling.LANCZOS)
            
            # KRİTİK NOKTA: Logoyu Story veya Post fark etmeksizin en alta yapıştır
            img.paste(logo, (0, hedef_boyut[1] - logo_yukseklik), logo)
        else:
            st.error("⚠️ onail_logo.png dosyası GitHub deposunda bulunamadı!")

        # 4. ADIM: GÖSTERİM VE İNDİRME
        st.divider()
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(img, use_container_width=True, caption="Hazırlanan Görsel")
        
        with col2:
            st.info("✅ Görseliniz profesyonel formatta boyutlandırıldı ve logonuz eklendi.")
            
            # Güvenli İndirme (Hafıza üzerinden)
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

st.caption("DDS Ajans İş Akışı v2.0 - Tasarım Modu Aktif")
