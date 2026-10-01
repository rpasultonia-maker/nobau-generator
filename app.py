import streamlit as st
from google import genai
from PIL import Image
import time

st.set_page_config(
    page_title="NOBAU AI Content Generator",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 NOBAU AI Content Brain & Prompt Studio")
st.caption("Automation Studio for Scale 1.000 Affiliate UGC Videos")

# Inisialisasi Client Gemini dari Secrets Streamlit Cloud
client = None
if "GEMINI_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

tab1, tab2 = st.tabs([
    "📌 FITUR 1: Master Image Prompt (Swap Face & Style)", 
    "🚀 FITUR 2: Content Brain V3 Video Prompt (Flow AI)"
])

# Fungsi pintar pemanggilan Gemini dengan Auto-Retry & Fallback Model
def generate_content_safe(client, prompt, images):
    models_to_try = ['gemini-3.8-flash', 'gemini-2.5-flash', 'gemini-1.5-flash']
    
    last_exception = None
    for model_name in models_to_try:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=[prompt] + images
                )
                return response.text
            except Exception as e:
                last_exception = e
                err_str = str(e)
                if "503" in err_str or "UNAVAILABLE" in err_str:
                    time.sleep(1.5)
                    continue
                else:
                    break
                    
    raise last_exception

# =========================================================
# FITUR 1: MASTER PROMPT IMAGE GENERATOR (TAJAM & KONSISTEN)
# =========================================================
with tab1:
    st.header("📌 Fitur 1: Generate Master Image Prompt")
    st.write("Upload Foto Referensi Style/Pose & Foto Wajah Karakter NOBAU:")
    
    col_f1_1, col_f1_2 = st.columns(2)
    
    with col_f1_1:
        st.subheader("1. Referensi Pose / Outfit / Style (Image 1)")
        uploaded_style = st.file_uploader(
            "Upload Foto Referensi Style & Pose", 
            type=["jpg", "jpeg", "png"], 
            key="style_ref"
        )
        if uploaded_style:
            st.image(uploaded_style, use_container_width=True)
            
    with col_f1_2:
        st.subheader("2. Identitas Wajah Karakter NOBAU (Image 2)")
        uploaded_face = st.file_uploader(
            "Upload Foto Wajah / Karakter NOBAU", 
            type=["jpg", "jpeg", "png"], 
            key="face_input"
        )
        if uploaded_face:
            st.image(uploaded_face, use_container_width=True)
        
    st.divider()
    
    if st.button("📌 Generate Master Prompt Image", type="secondary", use_container_width=True):
        if not uploaded_style or not uploaded_face:
            st.warning("⚠️ Mohon upload KEDUA FOTO (Image 1: Referensi Style & Image 2: Wajah Karakter) terlebih dahulu!")
        elif not client:
            st.error("⚠️ GEMINI_API_KEY belum terpasang di Streamlit Secrets!")
        else:
            with st.spinner("🤖 Gemini Vision sedang mengekstrak mikro-detail wajah Image 2 & pose Image 1..."):
                try:
                    img1_pil = Image.open(uploaded_style)
                    img2_pil = Image.open(uploaded_face)

                    sys_prompt_f1 = """
                    Analisis Image 1 (Referensi Style & Pose) dan Image 2 (Identitas Wajah Karakter NOBAU).
                    Tugasmu adalah menghasilkan Master Image Prompt baku yang SANGAT PRESISI dalam mentransfer wajah Image 2 ke Image 1.

                    Instruksi Analisis:
                    1. Bedah Image 2 dan sebutkan fitur mikroskopis wajahnya (bentuk mata, alis, bentuk hidung, bibir, rahang, skin tone, dan ciri khas).
                    2. Bedah Image 1 untuk POSE, OUTFIT, LIGHTING, CAMERA, dan ENVIRONMENT.

                    FORMAT OUTPUT (WAJIB DIIKUTI PERSIS):
                    Create a natural photorealistic smartphone selfie based on the uploaded reference images.

                    REFERENCE IMAGE ROLE:
                    Image 1 = Composition, camera angle, body pose, clothing style, background environment, and lighting ONLY.
                    Image 2 = CRITICAL FACE IDENTITY & HEAD ONLY.

                    FACE IDENTITY & CHARACTER FUSION (STRICT ZERO-MORPHING):
                    Replace the head and face of the person in Image 1 entirely with the exact facial identity from Image 2. 
                    Preserve Image 2's exact facial structure, eye shape, nose bridge, lip shape, jawline contour, skin tone, and facial proportions. 
                    DO NOT blend, mix, or merge facial features from Image 1 into Image 2. The final facial identity must be 100% recognizable as the NOBAU model in Image 2.

                    EXACT FACE DETAILS FROM IMAGE 2:
                    [Sebutkan detail fisik spesifik wajah dari Image 2 yang kamu analisis, contoh: almond-shaped dark brown eyes, soft defined jawline, natural fair Indonesian skin tone, natural full lips]

                    SUBJECT & POSE (DERIVED FROM IMAGE 1):
                    [Deskripsikan pose tangan, posisi tubuh, dan gesture dari Image 1 secara presisi]

                    HAIR STYLE:
                    Preserve the NOBAU model's recognizable hairstyle from Image 2: [Deskripsikan gaya/warna rambut dari Image 2 secara presisi].

                    CLOTHING & ACCESSORIES (DERIVED FROM IMAGE 1):
                    [Deskripsikan pakaian, warna, bahan, serta aksesori seperti kalung/jam tangan dari Image 1 secara presisi]

                    ENVIRONMENT & LIGHTING (DERIVED FROM IMAGE 1):
                    [Deskripsikan ruangan/latar belakang dan lighting dari Image 1 secara presisi]

                    SKIN REALISM & QUALITY:
                    Hyper-realistic natural skin texture, visible pores, realistic lighting reflections, raw photograph, shot on iPhone front camera, 8k resolution, UGC aesthetic, no smooth plastic skin filter --ar 9:16 --cw 100
                    """

                    prompt_img = generate_content_safe(client, sys_prompt_f1, [img1_pil, img2_pil])
                    st.success("✨ Master Image Prompt Generated!")
                    st.text_area("Copy-Paste Prompt Ini ke Midjourney / Flux:", value=prompt_img, height=420)
                except Exception as e:
                    st.error(f"Gagal memanggil Gemini API: {e}")

# =========================================================
# FITUR 2: CONTENT BRAIN V3 VIDEO PROMPT GENERATOR (GEMINI VISION DYNAMIC)
# =========================================================
with tab2:
    st.header("🚀 Fitur 2: Content Brain V3 & Video Prompt Generator")
    st.write("Upload Foto Model Hasil Fitur 1 & Foto Produk Botol NOBAU:")
    
    col_v1, col_v2 = st.columns(2)
    
    with col_v1:
        st.subheader("1. Foto Model (Hasil Fitur 1 / Image 1)")
        uploaded_model_gen = st.file_uploader(
            "Upload Foto Model Hasil Fitur 1", 
            type=["jpg", "jpeg", "png"], 
            key="model_gen"
        )
        if uploaded_model_gen:
            st.image(uploaded_model_gen, use_container_width=True)
            
    with col_v2:
        st.subheader("2. Foto Produk Botol NOBAU (Image 2)")
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
            st.warning("⚠️ Mohon upload KEDUA FOTO (Image 1: Model Hasil Fitur 1 & Image 2: Botol NOBAU) terlebih dahulu!")
        elif not client:
            st.error("⚠️ GEMINI_API_KEY belum terpasang di Streamlit Secrets!")
        else:
            with st.spinner("🤖 Gemini Vision sedang meriset settingan, varian produk & ide hook real-time..."):
                try:
                    img_m_pil = Image.open(uploaded_model_gen)
                    img_p_pil = Image.open(uploaded_product_botol)

                    sys_prompt_f2 = """
                    Analisis Image 1 (Model) dan Image 2 (Botol Produk NOBAU).
                    Tugasmu adalah meriset visualnya lalu menghasilkan Master Video Prompt UGC 10 detik sesuai format baku berikut.
                    Isi detail SETTING, OUTFIT, VARIANT LABEL PRODUK, DYNAMIC HOOK (0-3s), ACTION (3-6s), PAYOFF (6-8s), CTA (8-10s), dan DIALOGUE Bahasa Indonesia secara OTOMATIS & RELEVAN berdasarkan produk & latar di Image 1 & Image 2!

                    FORMAT OUTPUT (WAJIB DIIKUTI):
                    A continuous 10-second vertical 9:16 smartphone UGC video recorded inside [Deskripsikan lokasi/latar dari Image 1 secara presisi], matching the exact setting of Image 1.

                    IDENTITY: Preserve exact facial structure, identity, hair style, skin tone, [Deskripsikan outfit dan aksesori dari Image 1 secara presisi], and natural makeup matching Image 1.

                    PRODUCT: Holding the exact compact travel-size 60ml NOBAU spray bottle as visually defined in Image 2. The bottle is small and fits comfortably within a single palm, matching realistic 60ml bottle scale relative to her hand. [Deskripsikan detail visual label, warna, teks varian produk NOBAU dari Image 2 secara presisi].

                    STORY & TIMELINE (0-10s):
                    0-3s (HOOK): [Buatkan ide hook visual & reaksi masalah bau yang relevan dengan varian produk/latar dari Image 1 & Image 2]
                    3-6s (ACTION): [Aksi mengambil produk, memegang di telapak tangan, menyemprotkan produk sambil bicara ke kamera]
                    6-8s (PAYOFF): [Reaksi lega/segar setelah menyemprotkan produk]
                    8-10s (CTA): [Memajukan botol 60ml ke kamera dan mengangguk setuju]

                    DIALOGUE (Spoken natively in conversational Indonesian, EXACTLY):
                    "[Buatkan 1 kalimat dialogue UGC singkat, natural, catchy dalam Bahasa Indonesia yang langsung relevan dengan varian produk di Image 2]"

                    CAMERA & STYLE: Authentic Indonesian TikTok creator aesthetic, natural handheld camera shake, soft natural daylight, casual front-facing selfie camera angle.

                    CONTINUITY: One continuous generation, no camera cuts, fully clothed, no face morphing, no product redesign, no trigger spray mechanism, no floating limbs, no text or graphics.
                    """

                    prompt_vid = generate_content_safe(client, sys_prompt_f2, [img_m_pil, img_p_pil])
                    st.success("🚀 Master Video Prompt Flow AI Generated!")
                    st.text_area("Copy-Paste Prompt Ini ke Flow AI:", value=prompt_vid, height=380)
                except Exception as e:
                    st.error(f"Gagal memanggil Gemini API: {e}")
