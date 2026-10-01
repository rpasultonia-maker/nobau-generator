import streamlit as st
from google import genai
from PIL import Image
import time

st.set_page_config(page_title="NOBAU AI Content Generator", page_icon="🧪", layout="wide")

st.title("🧪 NOBAU AI Content Brain & Prompt Studio")
st.caption("Automation Studio for Scale 1.000 Affiliate UGC Videos")

client = None
if "GEMINI_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

tab1, tab2 = st.tabs([
    "📌 FITUR 1: Master Image Prompt", 
    "🚀 FITUR 2: Content Brain V3 Video Prompt"
])

def call_gemini_robust(client, prompt, images):
    # Senarai model mengikut keutamaan
    models_to_try = ['gemini-3.8-flash', 'gemini-2.5-flash', 'gemini-1.5-flash']
    last_err = None
    
    for model_id in models_to_try:
        # Cuba sehingga 3 kali bagi setiap model jika menerima ralat 503/server busy
        for attempt in range(3):
            try:
                res = client.models.generate_content(
                    model=model_id,
                    contents=[prompt] + images
                )
                return res.text
            except Exception as e:
                last_err = e
                err_msg = str(e)
                # Jika pelayan sibuk (503/UNAVAILABLE), tunggu sebentar dan cuba lagi
                if "503" in err_msg or "UNAVAILABLE" in err_msg or "high demand" in err_msg:
                    time.sleep(2 * (attempt + 1))  # Tunggu 2s, kemudian 4s
                    continue
                else:
                    # Jika ralat model tidak wujud (404), terus tukar ke model seterusnya
                    break
                    
    raise last_err

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
            with st.spinner("Menganalisis mikro-detail wajah & pose..."):
                try:
                    sys_f1 = """
                    Analisis Image 1 (Style & Pose) dan Image 2 (Identitas Wajah Karakter NOBAU).
                    Hasilkan Master Image Prompt baku:
                    - Bedah Image 2 untuk detail spesifik wajah (mata, alis, hidung, bibir, rahang, skin tone).
                    - Bedah Image 1 HANYA untuk composition, pose, outfit, environment, dan lighting.
                    - Format output:
                      Create a natural photorealistic smartphone selfie based on the uploaded reference images.
                      REFERENCE IMAGE ROLE: Image 1 = Pose, outfit, lighting, background. Image 2 = Face & Head identity ONLY.
                      FACE IDENTITY: Replace the head and face in Image 1 entirely with Image 2's exact identity. Zero morphing/blending.
                      EXACT FACE DETAILS FROM IMAGE 2: [Uraikan detail fisik wajah dari Image 2]
                      SUBJECT & POSE: [Deskripsikan pose dari Image 1]
                      CLOTHING & ACCESSORIES: [Deskripsikan pakaian & aksesori dari Image 1]
                      ENVIRONMENT & LIGHTING: [Deskripsikan latar dari Image 1]
                      SKIN REALISM: Hyper-realistic natural skin texture, visible pores, raw photograph, shot on iPhone front camera, 8k resolution, UGC aesthetic --ar 9:16 --cw 100
                    """
                    prompt_out = call_gemini_robust(client, sys_f1, [Image.open(up_style), Image.open(up_face)])
                    st.text_area("Master Image Prompt (Midjourney / Flux):", value=prompt_out, height=380)
                except Exception as e:
                    st.error(f"Gagal memanggil Gemini API: Pelayan sibuk atau ralat API ({e})")

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
            with st.spinner("Menganalisis latar, produk & meriset hook..."):
                try:
                    sys_f2 = """
                    Analisis Image 1 (Model) dan Image 2 (Botol Produk NOBAU 60ml).
                    Hasilkan Master Video Prompt Flow AI 10 detik:
                    - SETTING & OUTFIT: Ekstrak dari Image 1.
                    - PRODUCT: Botol 60ml travel-size dari Image 2.
                    - TIMELINE (0-10s): 0-3s Hook masalah bau yang relevan, 3-6s Action spray, 6-8s Payoff segar, 8-10s CTA.
                    - DIALOGUE: 1 kalimat Bahasa Indonesia yang catchy & relevan dengan varian produk di Image 2.
                    """
                    prompt_out = call_gemini_robust(client, sys_f2, [Image.open(up_model), Image.open(up_prod)])
                    st.text_area("Video Prompt Flow AI:", value=prompt_out, height=380)
                except Exception as e:
                    st.error(f"Gagal memanggil Gemini API: Pelayan sibuk atau ralat API ({e})")
