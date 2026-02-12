import streamlit as st
from PIL import Image, ImageOps
import google.generativeai as genai
import io

# --- YAPAY ZEKA AYARI ---
API_KEY = "AIzaSyCuvX2B0Mcj4vPShDM_lPqpC9Y4w_6NV3g"
genai.configure(api_key=API_KEY)

# --- PANEL AYARLARI ---
st.set_page_config(page_title="Onail Üretim Hattı", page_icon="💅", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; background-color: #1877f2; color: white; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.title("⚙️ Kontrol Paneli")
    format_secimi = st.radio("İçerik Formatı", ["Post (1080x1350)", "Story (1080x1920)"])
    st.divider()
    st.info("DDS Otomasyon Sistemi v1.2")

st.header("🚀 Onail Marina İçerik Üretim Hattı")
col1, col2 = st.columns([1, 1])

with col1:
    yuklenen_dosya = st.file_uploader("Bir fotoğraf yükleyin", type=['jpg', 'jpeg', 'png'])

if yuklenen_dosya:
    # Görseli işleme
    img = Image.open(yuklenen_dosya).convert("RGB")
    hedef_boyut = (1080, 1350) if "Post" in format_secimi else (1080, 1920)
    img = ImageOps.fit(img, hedef_boyut, Image.Resampling.LANCZOS)
    
    # Logo Yerleştirme
    try:
        logo = Image.open("onail_logo.png").convert("RGBA")
        img.paste(logo, (0, 0), logo)
    except:
        st.warning("Logo dosyası bulunamadı, logosuz devam ediliyor.")
        
    st.image(img, use_container_width=True, caption="İşlenen Görsel")
    
    # İndirme Butonu (Hatasız Yöntem)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    st.download_button("✅ Görseli Bilgisayarına İndir", buf.getvalue(), file_name="onail_hazir.jpg", mime="image/jpeg")

    with col2:
        st.subheader("🤖 Yapay Zeka Metin Önerileri")
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = "Bir profesyonel sosyal medya uzmanı gibi davran. Bu Onail Marina güzellik merkezi tırnak tasarım görseli için etkileyici, samimi ve harekete geçirici 3 farklı Instagram açıklaması yaz. Emojiler ve popüler hashtagler kullan."
            response = model.generate_content([prompt, img])
            st.write(response.text)
        except Exception as e:
            st.error("Metin üretilirken bir hata oluştu. Lütfen tekrar deneyin.")
