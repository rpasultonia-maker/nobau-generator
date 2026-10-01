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
# FITUR 1: MASTER PROMPT IMAGE GENERATOR (GEMINI VISION DYNAMIC)
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
            with st.spinner("🤖 Gemini Vision sedang menganalisis pose, outfit, lighting & lingkungan Image 1..."):
                try:
                    img1_pil = Image.open(uploaded_style)
                    img2_pil = Image.open(uploaded_face)

                    sys_prompt_f1 = """
                    Analisis Image 1 (Referensi Style & Pose) dan Image 2 (Identitas Wajah NOBAU).
                    Tugasmu adalah menghasilkan Master Image Prompt baku sesuai format persis di bawah ini.
                    Isi detail POSE, FACIAL EXPRESSION, CLOTHING, ENVIRONMENT, LIGHTING, CAMERA secara SANGAT SPESIFIK dan AKURAT berdasarkan elemen visual asli yang kamu lihat di Image 1!

                    FORMAT OUTPUT (WAJIB DIIKUTI):
                    Create a natural smartphone selfie photograph based on the uploaded reference images.

                    REFERENCE IMAGE ROLE:
                    Use Image 1 strictly for composition, camera perspective, body pose, clothing style, background environment, lighting, and casual smartphone photography aesthetic.

                    FACE IDENTITY — CRITICAL:
                    The woman's face and identity must come strictly from Image 2. Replace the face in Image 1 with Image 2's exact identity. Preserve exact facial structure, eyes, nose, lips, jawline, skin tone, and specific facial proportions extracted from Image 2 [Sebutkan secara ringkas detail fisik wajah Image 2 di sini]. Do NOT blend faces.

                    SUBJECT: A young Indonesian woman taking a casual smartphone selfie.
                    POSE: [Deskripsikan pose tangan, posisi tubuh, dan gesture dari Image 1 secara presisi]
                    FACIAL EXPRESSION: [Deskripsikan ekspresi wajah dari Image 1]
                    HAIR: Preserve NOBAU model's recognizable hairstyle from Image 2: voluminous, layered dark brown hair with bouncy curls and soft face-framing fringe.
                    CLOTHING: [Deskripsikan pakaian, warna, bahan, serta aksesori seperti kalung/jam tangan dari Image 1 secara presisi]
                    ENVIRONMENT: [Deskripsikan ruangan/latar belakang dari Image 1 secara presisi]
                    CAMERA: Authentic smartphone front-camera selfie perspective, high-angle/eye-level.
                    LIGHTING: [Deskripsikan pencahayaan dari Image 1]
                    SKIN & REALISM: Natural realistic skin texture, pores, subtle imperfections, no plastic skin, no heavy beauty filters.
                    PHOTOGRAPHIC STYLE: Authentic Indonesian social-media selfie aesthetic, casual handheld photo.
                    IDENTITY PRIORITY: Image 2 = Identity & Face. Image 1 = Pose, Outfit, Scene, & Style.
                    FINAL IMAGE: Believable smartphone selfie of the NOBAU female model in Image 1's exact visual situation.
                    """

                    prompt_img = generate_content_safe(client, sys_prompt_f1, [img1_pil, img2_pil])
                    st.success("✨ Master Image Prompt Generated!")
                    st.text_area("Copy-Paste Prompt Ini ke Midjourney / Flux:", value=prompt_img, height=380)
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
