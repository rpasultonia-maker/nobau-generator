import streamlit as st
from google import genai
from PIL import Image

st.set_page_config(page_title="NOBAU AI Content Generator", page_icon="🧪", layout="wide")

st.title("🧪 NOBAU AI Content Brain & Prompt Studio")

# Inisialisasi SDK baru
client = None
if "GEMINI_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

tab1, tab2 = st.tabs([
    "📌 FITUR 1: Master Image Prompt", 
    "🚀 FITUR 2: Content Brain V3 Video Prompt"
])

# FITUR 1
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        up_style = st.file_uploader("Upload Style/Pose (Image 1)", type=["jpg", "png"], key="s1")
        if up_style: st.image(up_style, use_container_width=True)
    with col2:
        up_face = st.file_uploader("Upload Wajah NOBAU (Image 2)", type=["jpg", "png"], key="f1")
        if up_face: st.image(up_face, use_container_width=True)
        
    if st.button("📌 Generate Master Prompt Image", use_container_width=True):
        if not up_style or not up_face:
            st.warning("Mohon upload kedua foto!")
        elif not client:
            st.error("API Key belum terpasang!")
        else:
            with st.spinner("Menganalisis gambar..."):
                try:
                    sys_f1 = """
                    Analisis Image 1 (Style/Pose) & Image 2 (Wajah NOBAU).
                    Hasilkan Master Image Prompt baku:
                    - Gunakan Image 1 HANYA untuk pose, outfit, lighting, dan environment.
                    - Gunakan Image 2 HANYA untuk identitas wajah (Zero-Morphing).
                    - Format: Photorealistic selfie, detail wajah Image 2, pose & outfit Image 1, 8k resolution, UGC aesthetic --ar 9:16 --cw 100.
                    """
                    res = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=[sys_f1, Image.open(up_style), Image.open(up_face)]
                    )
                    st.text_area("Master Image Prompt:", value=res.text, height=350)
                except Exception as e:
                    st.error(f"Error API: {e}")

# FITUR 2
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        up_model = st.file_uploader("Upload Model Hasil Fitur 1 (Image 1)", type=["jpg", "png"], key="m2")
        if up_model: st.image(up_model, use_container_width=True)
    with col2:
        up_prod = st.file_uploader("Upload Botol NOBAU 60ml (Image 2)", type=["jpg", "png"], key="p2")
        if up_prod: st.image(up_prod, use_container_width=True)
        
    if st.button("🚀 Run Content Brain V3", use_container_width=True):
        if not up_model or not up_prod:
            st.warning("Mohon upload kedua foto!")
        elif not client:
            st.error("API Key belum terpasang!")
        else:
            with st.spinner("Menganalisis gambar..."):
                try:
                    sys_f2 = """
                    Analisis Image 1 (Model) & Image 2 (Botol NOBAU).
                    Hasilkan Master Video Prompt Flow AI 10s:
                    - Latar & Outfit dari Image 1.
                    - Produk 60ml dari Image 2.
                    - Timeline: 0-3s Hook masalah bau, 3-6s Action spray, 6-8s Payoff, 8-10s CTA.
                    - Sertakan 1 kalimat Dialogue Bahasa Indonesia yang relevan.
                    """
                    res = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=[sys_f2, Image.open(up_model), Image.open(up_prod)]
                    )
                    st.text_area("Video Prompt Flow AI:", value=res.text, height=350)
                except Exception as e:
                    st.error(f"Error API: {e}")
