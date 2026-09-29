import streamlit as st
import google.generativeai as genai
from PIL import Image

# Config Halaman
st.set_page_config(page_title="NOBAU Content Prompt Generator", page_icon="⚡", layout="wide")

st.title("⚡ NOBAU Content Prompt Generator")
st.caption("Otomatisasi pembuatan prompt detail Flow AI / Midjourney berdasarkan Scene & Wajah Model NOBAU")

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

# Master Prompt Instructions System
MASTER_PROMPT_TEMPLATE = """
You are an expert AI prompt engineer. Analyze the two provided images:
- Image 1 is the SCENE REFERENCE (for pose, composition, framing, outfit, background, lighting, and casual smartphone selfie aesthetic).
- Image 2 is the NOBAU FACE REFERENCE (for the exact female model's face identity, facial structure, skin tone, features, and hairstyle).

Generate a highly structured, photorealistic AI image generation prompt following this EXACT template:

Create a highly natural, photorealistic smartphone selfie photograph based on the uploaded reference images.

REFERENCE IMAGE ROLE:
Use the scene reference image (Image 1) as the strict reference for:
- overall composition
- camera position / selfie perspective
- body pose, arm and hand positioning, head tilt, facial direction
- clothing style, fit, and fabric texture
- background environment and lighting
- casual smartphone photography aesthetic

FACE IDENTITY — CRITICAL:
The woman's face and identity must come strictly from the NOBAU female model reference image (Image 2).
Replace the face/identity of the woman in the scene reference with the NOBAU female model's exact facial identity.
Preserve the NOBAU model's:
- facial structure, face proportions, eyes, eyebrows, nose, lips, jawline, cheek structure, skin tone, natural facial asymmetry, and recognizable identity.
Do NOT blend the two faces. Do NOT average the identities. Do NOT create a new face.

SUBJECT:
A young Indonesian woman taking a casual smartphone selfie.

POSE:
[Extract and describe the precise pose from Image 1 in detail, including head tilt, arm placement, hand placement/gestures, and overall posture]

FACIAL EXPRESSION:
Natural relaxed feminine expression with a subtle soft smile, playful and confident. Natural eyes looking toward the smartphone camera.

HAIR:
Preserve the NOBAU model's recognizable hairstyle from Image 2 while allowing it to naturally adjust to the pose in Image 1.

CLOTHING:
[Extract and describe the exact clothing style, fabric type, colors, and textures visible in Image 1]

ACCESSORIES:
[Extract and describe any visible accessories/jewelry from Image 1]

ENVIRONMENT:
[Extract and describe the exact background, environment, location, paving/flooring, buildings, foliage, or surrounding elements visible in Image 1]

CAMERA:
Authentic smartphone front-camera selfie perspective. High-angle selfie, 24–28mm equivalent lens perspective, close framing with natural perspective distortion.

LIGHTING:
[Extract and describe the lighting quality from Image 1, e.g., natural outdoor daylight, soft overcast, diffused daylight]

SKIN & REALISM:
Natural realistic skin texture with visible pores and subtle imperfections. No plastic skin, no heavy beauty filters, no airbrushed skin.

PHOTOGRAPHIC STYLE:
Authentic Indonesian/Asian social-media selfie aesthetic. Casual handheld smartphone photograph, spontaneous feeling, realistic dynamic range.

IDENTITY PRIORITY:
NOBAU female model reference (Image 2) = identity and face.
Scene reference (Image 1) = pose, composition, camera perspective, clothing, environment, and photographic style.

FINAL IMAGE:
A believable, spontaneous smartphone selfie of the NOBAU female model in the exact visual situation of the scene reference image.
"""

# Tombol Action
st.markdown("---")
if st.button("🚀 Generate Master Prompt NOBAU", type="primary", use_container_width=True):
    if not scene_file or not face_file:
        st.error("Harap upload KEDUA foto terlebih dahulu (Scene Reference & Face Reference)!")
    else:
        with st.spinner("AI sedang menganalisis kedua gambar dan meracik prompt..."):
            try:
                # Menggunakan model Gemini 2.5 Flash terbaru
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # Memproses gambar & prompt
                response = model.generate_content([
                    MASTER_PROMPT_TEMPLATE,
                    scene_img,
                    face_img
                ])
                
                st.success("Prompt Berhasil Dibuat!")
                
                # Display Output
                st.subheader("📋 Hasil Prompt Detail (Tinggal Copy-Paste):")
                st.code(response.text, language="text")
                
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")
