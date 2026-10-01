import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(
    page_title="NOBAU AI Content Generator",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 NOBAU AI Content Brain & Prompt Studio")
st.caption("Automation Studio for Scale 1.000 Affiliate UGC Videos")

# Konfigurasi Gemini API jika tersedia di Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# =========================================================
# 1. UPLOAD 2 FOTO (LANGSUNG TAMPIL DI DEPAN)
# =========================================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Foto Model / Creator")
    uploaded_model = st.file_uploader("Upload Foto Model / Creator", type=["jpg", "jpeg", "png"], key="model")
    if uploaded_model:
        st.image(uploaded_model, use_container_width=True)

with col2:
    st.subheader("2. Foto Produk NOBAU")
    uploaded_product = st.file_uploader("Upload Foto Produk NOBAU", type=["jpg", "jpeg", "png"], key="product")
    if uploaded_product:
        st.image(uploaded_product, use_container_width=True)

st.divider()

# =========================================================
# 2. TOMBOL 2 FITUR UTAMA
# =========================================================
col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    btn_image = st.button("📌 Generate Master Prompt Image", type="secondary", use_container_width=True)

with col_btn2:
    btn_video = st.button("🚀 Run Content Brain V3 & Generate Video Prompt", type="primary", use_container_width=True)

st.divider()

# =========================================================
# 3. LOGIKA OTOMATIS GENERATE + GEMINI AI HOOK ENGINE
# =========================================================
if btn_image:
    if not uploaded_model or not uploaded_product:
        st.warning("⚠️ Mohon upload Foto Model dan Foto Produk terlebih dahulu!")
    else:
        st.success("✨ Master Image Prompt Generated!")
        prompt_img = (
            "A photorealistic studio shot of an Indonesian young adult female, long dark wavy hair, friendly face. "
            "Holding the exact compact travel-size NOBAU spray bottle as visually defined in Image 2. "
            "Clean lighting, 8k resolution, UGC aesthetic --ar 9:16"
        )
        st.text_area("Copy-Paste Image Prompt Ini ke Midjourney / Flux:", value=prompt_img, height=180)

if btn_video:
    if not uploaded_model or not uploaded_product:
        st.warning("⚠️ Mohon upload Foto Model dan Foto Produk terlebih dahulu!")
    else:
        with st.spinner("🤖 Content Brain V3 sedang meriset ide hook real-time dari foto..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                img_model_pil = Image.open(uploaded_model)
                img_product_pil = Image.open(uploaded_product)

                sys_prompt = """
                Analisis kedua foto ini (Foto 1: Model, Foto 2: Produk NOBAU).
                Buatkan prompt video UGC Flow AI 10 detik dengan DYNAMIC HOOK paling tren berdasarkan produk & karakter di foto.
                Gunakan format baku berikut:

                A continuous 10-second vertical 9:16 smartphone UGC video recorded in a brightly lit, aesthetic bedroom vanity setup.

                IDENTITY: Preserve exact facial structure, skin tone, hair style, jewelry, and specific features as defined in Image 1.

                OUTFIT (SAFE POLICY): Wearing a clean, casual oversized pastel t-shirt covering shoulders completely. Fully clothed, non-revealing, safe policy outfit.

                PRODUCT (PRECISION SCALE): Holding the exact compact travel-size 60ml/100ml NOBAU spray bottle as visually defined in Image 2. The bottle is small and fits comfortably within a single palm, anchoring realistic scale relative to her hand. Label layout, colors, and white mist pump cap remain 100% consistent with Image 2.

                STORY & TIMELINE (0-10s):
                0-3s (HOOK): [Buatkan hook visual & emosional yang kuat sesuai produk NOBAU di Foto 2]
                3-10s (BODY/SOLUTION): [Buatkan aksi penyeimbang, penggunaan produk, dan ekspresi lega/percaya diri]
                """

                response = model.generate_content([sys_prompt, img_model_pil, img_product_pil])
                prompt_vid = response.text

            except Exception:
                prompt_vid = """A continuous 10-second vertical 9:16 smartphone UGC video recorded in a brightly lit, aesthetic bedroom vanity setup.

IDENTITY: Preserve exact facial structure, skin tone, hair style, jewelry, and specific features as defined in Image 1.

OUTFIT (SAFE POLICY): Wearing a clean, casual oversized pastel t-shirt covering shoulders completely. Fully clothed, non-revealing, safe policy outfit.

PRODUCT (PRECISION SCALE): Holding the exact compact travel-size 60ml/100ml NOBAU spray bottle as visually defined in Image 2. The bottle is small and fits comfortably within a single palm, anchoring realistic scale relative to her hand. Label layout, colors, and white mist pump cap remain 100% consistent with Image 2.

STORY & TIMELINE (0-10s):
0-3s (HOOK): Creator dandan di depan kaca. cemas ketiak/ruangan bau pas aktivitas harian. Show relatable concerned or daily routine expression.
3-10s (BODY): Memegang produk NOBAU dengan jelas ke kamera, menyemprotkan produk, lalu tersenyum segar percaya diri."""

        st.success("🚀 Master Video Prompt Flow AI Generated!")
        st.text_area("Copy-Paste Prompt Ini ke Flow AI:", value=prompt_vid, height=280)
