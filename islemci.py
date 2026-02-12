import streamlit as st
from PIL import Image, ImageOps
import google.generativeai as genai
import os

# --- YAPILANDIRMA ---
API_KEY = "AIzaSyCuvX2B0Mcj4vPShDM_lPqpC9Y4w_6NV3g"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Meta Business Suite Estetiği
st.set_page_config(page_title="DDS Content Studio", page_icon="💅", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f0f2f5; }
    .stButton>button { width: 100%; border-radius: 5px; background-color: #1877f2; color: white; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.title("Yönetim Paneli")
    marka = st.selectbox("Marka", ["Onail Marina"])
    format_secimi = st.radio("Format", ["Post (1080x1350)", "Story (1080x1920)"])
    st.info("DDS Ajans Otomasyonu v1.0")

st.header(f"🚀 {marka} Üretim Hattı")
col1, col2 = st.columns([1, 1])

with col1:
    yuklenen_dosya = st.file_uploader("Fotoğrafı Buraya Bırak", type=['jpg', 'jpeg', 'png'])

if yuklenen_dosya:
    img = Image.open(yuklenen_dosya)
    hedef_boyut = (1080, 1350) if "Post" in format_secimi else (1080, 1920)
    img = ImageOps.fit(img, hedef_boyut, Image.Resampling.LANCZOS)
    
    logo_path = "onail_logo.png"
    if os.path.exists(logo_path):
        logo = Image.open(logo_path)
        img.paste(logo, (0, 0), logo)
        
        with col1:
            st.image(img, use_container_width=True)
            img.save("onail_output.jpg")
            with open("onail_output.jpg", "rb") as f:
                st.download_button("Görseli İndir", f, file_name="onail_hazir.jpg")

        with col2:
            st.subheader("🤖 AI Metin Önerileri")
            with st.spinner('Gemini analiz ediyor...'):
                img.save("ai_temp.jpg")
                img_to_ai = genai.upload_file("ai_temp.jpg")
                prompt = f"{marka} için 3 farklı tonda Instagram açıklaması yaz. Emojiler ve hashtagler dahil olsun."
                response = model.generate_content([prompt, img_to_ai])
                st.write(response.text)
