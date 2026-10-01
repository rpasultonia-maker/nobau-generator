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
    models_to_try = ['gemini-3.8-flash', 'gemini-2.5-flash', 'gemini-1.5-flash']
    last_err = None
    
    for model_id in models_to_try:
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
                if "503" in err_msg or "UNAVAILABLE" in err_msg or "high demand" in err_msg:
                    time.sleep(2 * (attempt + 1))
                    continue
                else:
                    break
                    
    raise last_err

# =========================================================
# FITUR 1: MASTER PROMPT IMAGE GENERATOR
# =========================================================
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        up_style = st.file_uploader("Upload Style/Pose (Image 1)", type=["jpg", "png"], key="s1")
        if up_style: st.image(up_style, use_container_width=True)
    with col2:
        up_face = st.file_uploader("Upload Wajah NOBAU (Image 2)", type=["jpg", "png"], key="f1")
        if up_face: st.image(up_face, use_container_width=True)
        
    st.divider()
        
    if st.button("📌 Generate Master Prompt Image", use_container_width=True):
        if not up_style or not up_face:
            st.warning("Mohon upload kedua foto!")
        elif not client:
            st.error("API Key belum terpasang!")
        else:
            with st.spinner("Menganalisis foto & mengekstrak ciri wajah Image 2..."):
                try:
                    sys_f1 = """
                    Analisis Image 1 (Referensi Style/Pose) dan Image 2 (Karakter Wajah NOBAU).
                    Hasilkan Master Image Prompt dalam format BAKU ASAL berikut TANPA MENGUBAH STRUKTUR UTAMA.
                    Isi bahagian dalam tanda kurung siku [...] berdasarkan hasil analisis visual Image 1 & Image 2 secara tepat.

                    FORMAT OUTPUT (WAJIB PATUHI STRUKTUR ASAL KETAT INI):
                    Create a natural smartphone selfie photograph based on the uploaded reference images.

                    REFERENCE IMAGE ROLE:
                    Use Image 1 strictly for composition, camera perspective, body pose, clothing style, background environment, lighting, and casual smartphone photography aesthetic.

                    FACE IDENTITY — CRITICAL:
                    The woman's face and identity must come strictly from Image 2. Replace the face in Image 1 with Image 2's exact identity. Preserve exact facial structure, eye shape, nose bridge, lips, jawline contour, and skin tone from Image 2. Do NOT blend, morph, or mix faces with Image 1.
                    MICRO FACE DETAILS FROM IMAGE 2: [Analisis dan jelaskan secara terperinci ciri fizikal unik wajah dari Image 2]

                    SUBJECT: A young Indonesian woman taking a casual smartphone selfie.
                    POSE: [Deskripsikan pose tangan, posisi tubuh, dan gesture dari Image 1 secara presisi]
                    FACIAL EXPRESSION: [Deskripsikan ekspresi wajah dari Image 1]
                    HAIR: Preserve NOBAU model's recognizable hairstyle from Image 2: [Deskripsikan gaya/warna rambut dari Image 2 secara presisi].
                    CLOTHING: [Deskripsikan pakaian, warna, bahan, serta aksesori seperti kalung/jam tangan dari Image 1 secara presisi]
                    ENVIRONMENT: [Deskripsikan ruangan/latar belakang dari Image 1 secara presisi]
                    CAMERA: Authentic smartphone front-camera selfie perspective, high-angle/eye-level.
                    LIGHTING: [Deskripsikan pencahayaan dari Image 1 secara presisi]
                    SKIN & REALISM: Natural realistic skin texture, pores, subtle imperfections, no plastic skin, no heavy beauty filters.
                    PHOTOGRAPHIC STYLE: Authentic Indonesian social-media selfie aesthetic, casual handheld photo.
                    IDENTITY PRIORITY: Image 2 = Identity & Face. Image 1 = Pose, Outfit, Scene, & Style.
                    FINAL IMAGE: Believable smartphone selfie of the NOBAU female model in Image 1's exact visual situation. --ar 9:16 --cw 100
                    """
                    prompt_out = call_gemini_robust(client, sys_f1, [Image.open(up_style), Image.open(up_face)])
                    st.success("✨ Master Image Prompt Generated!")
                    st.text_area("Copy-Paste Prompt Ini ke Midjourney / Flux:", value=prompt_out, height=380)
                except Exception as e:
                    st.error(f"Gagal memanggil Gemini API: {e}")

# =========================================================
# FITUR 2: CONTENT BRAIN V3 VIDEO PROMPT GENERATOR
# =========================================================
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        up_model = st.file_uploader("Upload Model Hasil Fitur 1 (Image 1)", type=["jpg", "png"], key="m2")
        if up_model: st.image(up_model, use_container_width=True)
    with col2:
        up_prod = st.file_uploader("Upload Botol NOBAU 60ml (Image 2)", type=["jpg", "png"], key="p2")
        if up_prod: st.image(up_prod, use_container_width=True)
        
    st.divider()
        
    if st.button("🚀 Run Content Brain V3 & Generate Video Prompt", use_container_width=True, type="primary"):
        if not up_model or not up_prod:
            st.warning("Mohon upload kedua foto!")
        elif not client:
            st.error("API Key belum terpasang!")
        else:
            with st.spinner("Menganalisis latar, produk & meriset hook real-time..."):
                try:
                    sys_f2 = """
                    Analisis Image 1 (Model Hasil Fitur 1) dan Image 2 (Botol Produk NOBAU 60ml).
                    Hasilkan Master Video Prompt UGC 10 detik mengikut FORMAT BAKU ASAL berikut TANPA MENGUBAH STRUKTUR UTAMA.
                    Isi bahagian dalam tanda kurung siku [...] berdasarkan analisis visual Image 1 & Image 2.

                    FORMAT OUTPUT (WAJIB PATUHI STRUKTUR ASAL KETAT INI):
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
                    prompt_out = call_gemini_robust(client, sys_f2, [Image.open(up_model), Image.open(up_prod)])
                    st.success("🚀 Master Video Prompt Flow AI Generated!")
                    st.text_area("Copy-Paste Prompt Ini ke Flow AI:", value=prompt_out, height=380)
                except Exception as e:
                    st.error(f"Gagal memanggil Gemini API: {e}")
