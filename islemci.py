import streamlit as st
from PIL import Image, ImageOps
import google.generativeai as genai
import io

# --- KRİTİK AYAR: YAPAY ZEKA ---
# En güncel ve hata vermeyen model ismini sabitledik.
API_KEY = "AIzaSyCuvX2B0Mcj4vPShDM_lPqpC9Y4w_6NV3g"
genai.configure(api_key=API_KEY)

# --- PANEL TASARIMI (SADE VE ŞIK) ---
st.set_page_config(page_title="Onail Marina Otomasyon", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .stButton>button { background-color: #000000; color: white; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("✨ Onail Marina İçerik Otomasyonu")

# Format Seçimi (Üstte, sade)
format_secimi = st.segmented_control("İçerik Görsel Formatı Seçin", ["Post (1080x1350)", "Story (1080x1920)"], default="Post (1080x1350)")

yuklenen_dosya = st.file_uploader("Bir fotoğraf yükleyin", type=['jpg', 'jpeg', 'png'], label_visibility="collapsed")

if yuklenen_dosya:
    # 1. Görseli İşleme
    img = Image.open(yuklenen_dosya).convert("RGB")
    hedef_boyut = (1080, 1350) if "Post" in format_secimi else (1080, 1920)
    img = ImageOps.fit(img, hedef_boyut, Image.Resampling.LANCZOS)
    
    # 2. Logo Yerleştirme (Boyuta göre dinamik konumlandırma)
    try:
        logo = Image.open("onail_logo.png").convert("RGBA")
        # Logoyu görselin genişliğine göre orantıla
        logo_genislik = hedef_boyut[0] 
        oran = logo_genislik / float(logo.size[0])
        logo_yukseklik = int((float(logo.size[1]) * float(oran)))
        logo = logo.resize((logo_genislik, logo_yukseklik), Image.Resampling.LANCZOS)
        
        # Logoyu TAM ALTA yapıştır (Yükseklik farkı gözetmeksizin)
        img.paste(logo, (0, hedef_boyut[1] - logo_yukseklik), logo)
    except:
        st.warning("Logo dosyası (onail_logo.png) bulunamadı.")

    # 3. Ekranı İkiye Böl (Görsel ve Metin yan yana)
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.image(img, use_container_width=True, caption="İşlenen Görsel")
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        st.download_button("✅ Görseli İndir", buf.getvalue(), file_name="onail_hazir.jpg")

    with col2:
        st.subheader("🤖 Yapay Zeka Metin Önerileri")
        try:
            # HATA BURADAYDI: Model ismini 'gemini-1.5-flash' yaparak çözdük.
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = "Sen Onail Marina için bir sosyal medya uzmanısın. Instagram için 3 farklı dikkat çekici, samimi ve tırnak tasarımına uygun açıklama yaz. Emojiler kullan."
            response = model.generate_content([prompt, img])
            st.write(response.text)
        except Exception as e:
            st.error("Metinler şu an hazırlanamadı ama görseliniz yukarıda hazır!")

st.caption("DDS Ajans İş Akışı v1.5")
