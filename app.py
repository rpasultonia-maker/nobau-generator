import streamlit as st
import google.generativeai as genai
from PIL import Image

# Config Halaman
st.set_page_config(page_title="NOBAU Content & Prompt Generator", page_icon="⚡", layout="wide")

st.title("⚡ NOBAU Content & Prompt Generator")
st.caption("Otomatisasi pembuatan Ide Konten (Hook + Caption) & Prompt Detail Flow AI/Midjourney")

# Cek API Key dari Streamlit Secrets atau Sidebar
st.sidebar.header("🔑 Pengaturan API")

if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"]:
    api_key = st.secrets["GEMINI_API_KEY"]
    st.sidebar.success("✅ API Key Terhubung Otomatis!")
else:
    api_key = st.sidebar.text_input("Masukkan Gemini API Key:", type="password")

if not api_key:
    st.warning("Silakan masukkan Gemini API Key di sidebar untuk mulai menggunakan web app ini.")
    st.stop()

# Set API Key
genai.configure(api_key=api_key)

# Tampilan Upload Gambar (2 Slot)
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Scene Reference")
    scene_file = st.file_uploader("Upload foto pose / baju / background", type=["jpg", "jpeg", "png"], key="scene")
    if scene_file:
        scene_img = Image.open(scene_file)
        st.image(scene_img, use_container_width=True)

with col2:
    st.subheader("2. NOBAU Face Reference")
    face_file = st.file_uploader("Upload foto master wajah model NOBAU", type=["jpg", "jpeg", "png"], key="face")
    if face_file:
        face_img = Image.open(face_file)
        st.image(face_img, use_container_width=True)

# Master Prompt Instructions System (Ide Konten + Prompt Visual)
MASTER_PROMPT_TEMPLATE = """
You are an expert Content Creator Strategy & AI Prompt Engineer for NOBAU (an Indonesian brand specializing in odor eliminator / penghilang bau products with 8 product variants).

Analyze the two provided images:
- Image 1 is the SCENE REFERENCE (pose, framing, environment, lighting, casual selfie style).
- Image 2 is the NOBAU FACE REFERENCE (exact female model identity).

Deliver your response in TWO SECTIONS:

---
SECTION 1: IDE KONTEN NOBAU (Dalam Bahasa Indonesia)
Berdasarkan suasana/pose dari Image 1, buatkan ide konten harian kasual yang relevan dengan produk NOBAU:
1. **Sudut Pandang / Storyline:** (Penjelasan singkat situasi dalam foto ini cocok untuk promosi masalah bau apa, misal: bau sepatu, helm, studio, mobil, pakaian, dll).
2. **Hook Text On-Screen:** (Kalimat singkat 3-6 kata yang bikin orang berhenti scrolling, gaya kasual anak muda).
3. **Caption Instagram/TikTok:** (2-3 paragraf ramah, relateable, menyenggol masalah bau harian, lalu solusi dari produk NOBAU).
4. **Call to Action (CTA):** (Ajakan klik link bio / checkout).
5. **Hashtag:** (5 hashtag relevan).

---
SECTION 2: MASTER PROMPT VISUAL (English - for Flow AI / Midjourney)
Generate a highly structured, photorealistic AI image prompt:

Create a highly natural, photorealistic smartphone selfie photograph based on the uploaded reference images.

REFERENCE IMAGE ROLE:
Use Image 1 strictly for composition, camera perspective, body pose, clothing, background, and casual smartphone photography aesthetic.

FACE IDENTITY — CRITICAL:
Use Image 2 strictly for the female model's exact face identity, facial structure, skin tone, features, and hairstyle. Replace the face in Image 1 with Image 2's identity. Do NOT blend faces.

SUBJECT: A young Indonesian woman taking a casual smartphone selfie.
POSE: [Extract detailed pose from Image 1]
FACIAL EXPRESSION: Natural relaxed feminine expression, subtle smile, playful and confident.
HAIR: Preserve NOBAU model's hairstyle from Image 2 adjusting naturally to Image 1's pose.
CLOTHING: [Extract clothing details from Image 1]
ENVIRONMENT: [Extract background details from Image 1]
CAMERA: Authentic smartphone front-camera selfie perspective, high angle, 24–28mm equivalent.
LIGHTING: [Extract lighting from Image 1]
SKIN & REALISM: Natural realistic skin texture, pores, imperfections, no heavy beauty filters.
PHOTOGRAPHIC STYLE: Authentic Indonesian social-media selfie aesthetic, casual handheld photo.
IDENTITY PRIORITY: Image 2 = Face & Identity. Image 1 = Pose, Outfit, Scene, & Style.
FINAL IMAGE: Believable smartphone selfie of NOBAU female model in Image 1's exact visual context.
"""

# Tombol Action
st.markdown("---")
if st.button("🚀 Generate Ide Konten & Master Prompt NOBAU", type="primary", use_container_width=True):
    if not scene_file or not face_file:
        st.error("Harap upload KEDUA foto terlebih dahulu (Scene Reference & Face Reference)!")
    else:
        with st.spinner("AI sedang menyusun ide konten & meracik prompt visual..."):
            try:
                model = genai.GenerativeModel('gemini-3.8-flash')
                
                response = model.generate_content([
                    MASTER_PROMPT_TEMPLATE,
                    scene_img,
                    face_img
                ])
                
                st.success("Ide Konten & Prompt Berhasil Dibuat!")
                
                # Display Output
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")
