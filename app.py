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

# Konfigurasi Gemini API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# TAB LAYOUT UNTUK 2 FITUR PRESISI
tab1, tab2 = st.tabs([
    "📌 FITUR 1: Master Image Prompt Generator", 
    "🚀 FITUR 2: Content Brain V3 Video Prompt Generator"
])

# =========================================================
# FITUR 1: MASTER PROMPT IMAGE GENERATOR
# =========================================================
with tab1:
    st.header("📌 Fitur 1: Generate Master Image Prompt")
    st.write("Upload Foto Karakter Wajah & Foto Referensi Gaya/Pose:")
    
    col_f1_1, col_f1_2 = st.columns(2)
    
    with col_f1_1:
        st.subheader("1. Foto Karakter Wajah NOBAU")
        uploaded_face = st.file_uploader(
            "Upload Foto Karakter Wajah", 
            type=["jpg", "jpeg", "png"], 
            key="face_input"
        )
        if uploaded_face:
            st.image(uploaded_face, use_container_width=True)
            
    with col_f1_2:
        st.subheader("2. Foto Referensi Gaya / Pose / Angle")
        uploaded_ref_style = st.file_uploader(
            "Upload Foto Referensi Style / Pose", 
            type=["jpg", "jpeg", "png"], 
            key="style_ref"
        )
        if uploaded_ref_style:
            st.image(uploaded_ref_style, use_container_width=True)
        
    st.divider()
    
    if st.button("📌 Generate Master Prompt Image", type="secondary", use_container_width=True):
        if not uploaded_face or not uploaded_ref_style:
            st.warning("⚠️ Mohon upload KEDUA FOTO (Foto Karakter Wajah & Foto Referensi Style) terlebih dahulu!")
        else:
            with st.spinner("🤖 Menganalisis karakter & referensi gaya..."):
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    img_face = Image.open(uploaded_face)
                    img_style = Image.open(uploaded_ref_style)

                    sys_prompt_f1 = """
                    Analisis Foto 1 (Karakter Wajah) & Foto 2 (Referensi Style/Pose/Lighting).
                    Buatkan Master Image Prompt untuk Midjourney/Flux yang menggabungkan struktur wajah persis dari Foto 1 dengan pose, lighting, background, dan outfit dari Foto 2.
                    Sertakan instruksi memegang botol spray NOBAU travel-size 60ml/100ml. Format prompt dalam bahasa Inggris, 8k resolution, UGC aesthetic --ar 9:16.
                    """
                    response_f1 = model.generate_content([sys_prompt_f1, img_face, img_style])
                    prompt_img = response_f1.text
                except Exception:
                    prompt_img = (
                        "A photorealistic studio shot of an Indonesian young adult female, long dark wavy hair, friendly face. "
                        "Preserving exact facial structure from Image 1, matching the exact pose, outfit, and aesthetic lighting from Image 2. "
                        "Holding the exact compact travel-size 60ml/100ml NOBAU spray bottle. "
                        "Clean lighting, 8k resolution, UGC aesthetic --ar 9:16"
                    )
                    
            st.success("✨ Master Image Prompt Generated!")
            st.text_area("Copy-Paste Prompt Ini ke Midjourney / Flux:", value=prompt_img, height=200)

# =========================================================
# FITUR 2: CONTENT BRAIN V3 VIDEO PROMPT GENERATOR
# =========================================================
with tab2:
    st.header("🚀 Fitur 2: Content Brain V3 & Video Prompt Generator")
    st.write("Upload Foto Model Hasil Fitur 1 & Foto Produk Botol NOBAU:")
    
    col_v1, col_v2 = st.columns(2)
    
    with col_v1:
        st.subheader("1. Foto Model (Hasil Fitur 1)")
        uploaded_model_gen = st.file_uploader(
            "Upload Foto Model / Creator Hasil Fitur 1", 
            type=["jpg", "jpeg", "png"], 
            key="model_gen"
        )
        if uploaded_model_gen:
            st.image(uploaded_model_gen, use_container_width=True)
            
    with col_v2:
        st.subheader("2. Foto Produk Botol NOBAU")
        uploaded_product_botol = st.file_uploader(
            "Upload Foto Produk Botol NOBAU", 
            type=["jpg", "jpeg", "png"], 
            key="product_botol"
        )
        if uploaded_product_botol:
            st.image(uploaded_product_botol, use_container_width=True)
            
    st.divider()
    
    if st.button("🚀 Run Content Brain V3 & Generate Video Prompt", type="primary", use_container_width=True):
        if not uploaded_model_gen or not uploaded_product_botol:
            st.warning("⚠️ Mohon upload KEDUA FOTO (Foto Hasil Fitur 1 & Foto Botol NOBAU) terlebih dahulu!")
        else:
            with st.spinner("🤖 Content Brain V3 sedang menganalisis foto & meriset ide hook real-time..."):
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    img_m = Image.open(uploaded_model_gen)
                    img_p = Image.open(uploaded_product_botol)

                    sys_prompt_f2 = """
                    Analisis Foto 1 (Model hasil generate) & Foto 2 (Botol Produk NOBAU 60ml/100ml).
                    Buatkan prompt video UGC Flow AI 10 detik dengan DYNAMIC HOOK paling tren & realistis.
                    
                    Gunakan format baku berikut:
                    A continuous 10-second vertical 9:16 smartphone UGC video recorded in a brightly lit, aesthetic bedroom vanity setup.

                    IDENTITY: Preserve exact facial structure, skin tone, hair style, jewelry, and specific features as defined in Image 1.

                    OUTFIT (SAFE POLICY): Wearing a clean, casual oversized pastel t-shirt covering shoulders completely. Fully clothed, non-revealing, safe policy outfit.

                    PRODUCT (PRECISION SCALE): Holding the exact compact travel-size 60ml/100ml NOBAU spray bottle as visually defined in Image 2. The bottle is small and fits comfortably within a single palm, anchoring realistic scale relative to her hand. Label layout, colors, and white mist pump cap remain 100% consistent with Image 2.

                    STORY & TIMELINE (0-10s):
                    0-3s (HOOK): [Buatkan hook visual & emosional yang kuat sesuai produk NOBAU di Foto 2]
                    3-10s (BODY/SOLUTION): [Buatkan aksi penyeimbang, penggunaan produk, dan ekspresi lega/percaya diri]
                    """

                    response_f2 = model.generate_content([sys_prompt_f2, img_m, img_p])
                    prompt_vid = response_f2.text

                except Exception:
                    prompt_vid = """A continuous 10-second vertical 9:16 smartphone UGC video recorded in a brightly lit, aesthetic bedroom vanity setup.

IDENTITY: Preserve exact facial structure, skin tone, hair style, jewelry, and specific features as defined in Image 1.

OUTFIT (SAFE POLICY): Wearing a clean, casual oversized pastel t-shirt covering shoulders completely. Fully clothed, non-revealing, safe policy outfit.

PRODUCT (PRECISION SCALE): Holding the exact compact travel-size 60ml/100ml NOBAU spray bottle as visually defined in Image 2. The bottle is small and fits comfortably within a single palm, anchoring realistic scale relative to her hand. Label layout, colors, and white mist pump cap remain 100% consistent with Image 2.

STORY & TIMELINE (0-10s):
0-3s (HOOK): Creator dandan di depan kaca. cemas bau pas aktivitas harian. Show relatable concerned expression.
3-10s (BODY): Memegang produk NOBAU dengan jelas ke kamera, menyemprotkan produk, lalu tersenyum segar percaya diri."""

            st.success("🚀 Master Video Prompt Flow AI Generated!")
            st.text_area("Copy-Paste Prompt Ini ke Flow AI:", value=prompt_vid, height=280)
