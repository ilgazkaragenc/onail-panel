import streamlit as st
from PIL import Image, ImageOps
import google.generativeai as genai
import io

# --- YENİ API ANAHTARI VE MODEL BAĞLANTISI ---
API_KEY = "AIzaSyC7qOMoI8tjsC89mcH2fKVH6iNWM8ABmpc"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="Onail Otomasyon", layout="centered")

# Sadeleştirilmiş Arayüz
st.title("✨ Onail Marina İçerik Hattı")

format_secimi = st.segmented_control("Format Seçin", ["Post (1080x1350)", "Story (1080x1920)"], default="Post (1080x1350)")
yuklenen_dosya = st.file_uploader("Fotoğraf Yükle", type=['jpg', 'jpeg', 'png'], label_visibility="collapsed")

if yuklenen_dosya:
    img = Image.open(yuklenen_dosya).convert("RGB")
    hedef_boyut = (1080, 1350) if "Post" in format_secimi else (1080, 1920)
    img = ImageOps.fit(img, hedef_boyut, Image.Resampling.LANCZOS)
    
    # DİNAMİK LOGO YERLEŞİMİ
    try:
        logo = Image.open("onail_logo.png").convert("RGBA")
        logo_genislik = hedef_boyut[0]
        oran = logo_genislik / float(logo.size[0])
        logo_yukseklik = int((float(logo.size[1]) * float(oran)))
        logo = logo.resize((logo_genislik, logo_yukseklik), Image.Resampling.LANCZOS)
        
        # Logoyu tam alta yapıştır (Hangi format olursa olsun)
        img.paste(logo, (0, hedef_boyut[1] - logo_yukseklik), logo)
    except:
        st.warning("Logo (onail_logo.png) bulunamadı.")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.image(img, use_container_width=True)
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        st.download_button("✅ Görseli İndir", buf.getvalue(), file_name="onail_hazir.jpg")

    with col2:
        st.subheader("🤖 AI Metin Önerileri")
        try:
            # En güncel bağlama kodu
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = "Sen bir sosyal medya uzmanısın. Onail Marina tırnak tasarım görseli için 3 farklı etkileyici Instagram açıklaması yaz. Emojiler kullan."
            response = model.generate_content([prompt, img])
            st.write(response.text)
        except Exception as e:
            st.error("AI bağlantısında bir sorun var, lütfen API anahtarını kontrol et.")

st.caption("DDS Ajans v1.6")
