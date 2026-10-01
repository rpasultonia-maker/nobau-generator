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

client = None
if "GEMINI_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

tab1, tab2 = st.tabs([
    "📌 FITUR 1: Master Image Prompt (Swap Face & Style)", 
    "🚀 FITUR 2: Content Brain V3 Video Prompt (Flow AI)"
])

# Template Fallback Baku Fitur 1 (Persis Template Permintaan Kamu)
FALLBACK_F1 = """Create a highly natural, photorealistic smartphone selfie photograph based on the uploaded reference images.

REFERENCE IMAGE ROLE:
Use Image 1 strictly for composition, camera perspective, body pose, clothing style, background environment, lighting, and casual smartphone photography aesthetic.

FACE IDENTITY — CRITICAL:
The woman's face and identity must come strictly from Image 2. Replace the face in Image 1 with Image 2's exact identity. Preserve facial structure, eyes, nose, lips, jawline, skin tone. Do NOT blend faces.

SUBJECT: A young Indonesian woman taking a casual smartphone selfie.
POSE: High-angle, close-up perspective with right hand raised behind the head; body angled slightly forward toward the lens in a relaxed, casual selfie pose.
FACIAL EXPRESSION: Natural relaxed feminine expression with a subtle soft smile, playful and confident.
HAIR: Preserve NOBAU model's recognizable hairstyle from Image 2: voluminous, dark brown layered hair with soft, bouncy blowout curls.
CLOTHING: Black ribbed camisole top featuring scalloped lace trim along the deep neckline, with thin double straps showing pink bra straps underneath.
ENVIRONMENT: Simple indoor background with a plain neutral wall on one side and a warm wooden paneled door on the other.
CAMERA: Authentic smartphone front-camera selfie perspective, high-angle, 24–28mm equivalent.
LIGHTING: Soft, diffused direct indoor lighting casting gentle highlights on the forehead, nose, and shoulders.
SKIN & REALISM: Natural realistic skin texture, pores, subtle imperfections, no plastic skin, no heavy beauty filters.
PHOTOGRAPHIC STYLE: Authentic Indonesian social-media selfie aesthetic, casual handheld photo.
IDENTITY PRIORITY: Image 2 = Identity & Face. Image 1 = Pose, Outfit, Scene, & Style.
FINAL IMAGE: Believable smartphone selfie of the NOBAU female model in Image 1's exact visual situation."""

# Template Fallback Baku Fitur 2
FALLBACK_F2 = """A continuous 10-second vertical 9:16 smartphone UGC video recorded inside an aesthetic indoor setting, matching the exact setting of Image 1.

IDENTITY: Preserve exact facial structure, identity, hair style, skin tone, casual stylish top, and natural makeup matching Image 1.

PRODUCT: Holding the exact compact travel-size 60ml NOBAU spray bottle as visually defined in Image 2. The bottle is small and fits comfortably within a single palm, matching realistic 60ml bottle scale relative to her hand. White cylindrical bottle with a semi-translucent mist pump cap and clear NOBAU product label.

STORY & TIMELINE (0-10s):
0-3s (HOOK): Creator winces with a subtle concerned expression, reacting to an unpleasant lingering odor in the room.
3-6s (ACTION): Picks up the compact 60ml NOBAU bottle, holding it naturally in one palm, and sprays 2 quick mists into the air while speaking directly to the selfie camera.
6-8s (PAYOFF): Takes a deep breath, smiles with instant relief, gesturing how quickly the fresh essential oil aroma neutralizes the smell.
8-10s (CTA): Holds the small 60ml NOBAU bottle forward at chest level toward the camera lens, nodding approvingly.

DIALOGUE (Spoken natively in conversational Indonesian, EXACTLY):
"Habis ngerokok tapi mau ketemu doi? Semprot NOBAU Penghilang Bau Rokok, bau apek langsung hilang seketika!"

CAMERA & STYLE: Authentic Indonesian TikTok creator aesthetic, natural handheld camera shake, soft natural daylight, casual front-facing selfie camera angle.

CONTINUITY: One continuous generation, no camera cuts, fully clothed, no face morphing, no product redesign, no trigger spray mechanism, no floating limbs, no text or graphics."""

def generate_content_safe(client, prompt, images, fallback_text):
    if not client:
        return fallback_text
    
    target_model = 'gemini-3.8-flash'
    for attempt in range(2):
        try:
            response = client.models.generate_content(
                model=target_model,
                contents=[prompt] + images
            )
            return response.text
        except Exception as e:
            err_str = str(e)
            if "503" in err_str or "UNAVAILABLE" in err_str:
                time.sleep(1.5)
                continue
            elif "429" in err_str or "RESOURCE_EXHAUSTED" in err_str or "quota" in err_str:
                st.warning("⚠️ Limit kuota API Gemini tercapai. Menampilkan Master Prompt Standar Baku:")
                return fallback_text
            else:
                return fallback_text
    return fallback_text

# =========================================================
# FITUR 1: MASTER PROMPT IMAGE GENERATOR
# =========================================================
with tab1:
    st.header("📌 Fitur 1: Generate Master Image Prompt")
    col_f1_1, col_f1_2 = st.columns(2)
    with col_f1_1:
        uploaded_style = st.file_uploader("Upload Foto Referensi Style & Pose", type=["jpg", "jpeg", "png"], key="style_ref")
        if uploaded_style: st.image(uploaded_style, use_container_width=True)
    with col_f1_2:
        uploaded_face = st.file_uploader("Upload Foto Wajah / Karakter NOBAU", type=["jpg", "jpeg", "png"], key="face_input")
        if uploaded_face: st.image(uploaded_face, use_container_width=True)
        
    st.divider()
    if st.button("📌 Generate Master Prompt Image", type="secondary", use_container_width=True):
        if not uploaded_style or not uploaded_face:
            st.warning("⚠️ Mohon upload KEDUA FOTO terlebih dahulu!")
        else:
            with st.spinner("🤖 Gemini Vision sedang menganalisis foto..."):
                img1_pil = Image.open(uploaded_style)
                img2_pil = Image.open(uploaded_face)
                sys_prompt_f1 = """
                Analisis Image 1 (Referensi Style & Pose) dan Image 2 (Identitas Wajah NOBAU).
                Hasilkan Master Image Prompt baku sesuai format persis di bawah ini.
                Isi detail POSE, FACIAL EXPRESSION, CLOTHING, ENVIRONMENT, LIGHTING secara SANGAT SPESIFIK dan AKURAT berdasarkan elemen visual asli yang kamu lihat di Image 1!

                FORMAT OUTPUT:
                Create a highly natural, photorealistic smartphone selfie photograph based on the uploaded reference images.

                REFERENCE IMAGE ROLE:
                Use Image 1 strictly for composition, camera perspective, body pose, clothing style, background environment, lighting, and casual smartphone photography aesthetic.

                FACE IDENTITY — CRITICAL:
                The woman's face and identity must come strictly from Image 2. Replace the face in Image 1 with Image 2's exact identity. Preserve facial structure, eyes, nose, lips, jawline, skin tone. Do NOT blend faces.

                SUBJECT: A young Indonesian woman taking a casual smartphone selfie.
                POSE: [Deskripsikan pose dari Image 1 secara presisi]
                FACIAL EXPRESSION: [Deskripsikan ekspresi dari Image 1 secara presisi]
                HAIR: Preserve NOBAU model's recognizable hairstyle from Image 2: [Deskripsikan gaya rambut dari Image 2 secara presisi].
                CLOTHING: [Deskripsikan pakaian & aksesori dari Image 1 secara presisi]
                ENVIRONMENT: [Deskripsikan ruangan/latar dari Image 1 secara presisi]
                CAMERA: Authentic smartphone front-camera selfie perspective, high-angle, 24–28mm equivalent.
                LIGHTING: [Deskripsikan pencahayaan dari Image 1 secara presisi]
                SKIN & REALISM: Natural realistic skin texture, pores, subtle imperfections, no plastic skin, no heavy beauty filters.
                PHOTOGRAPHIC STYLE: Authentic Indonesian social-media selfie aesthetic, casual handheld photo.
                IDENTITY PRIORITY: Image 2 = Identity & Face. Image 1 = Pose, Outfit, Scene, & Style.
                FINAL IMAGE: Believable smartphone selfie of the NOBAU female model in Image 1's exact visual situation.
                """
                prompt_img = generate_content_safe(client, sys_prompt_f1, [img1_pil, img2_pil], FALLBACK_F1)
                st.success("✨ Master Image Prompt Generated!")
                st.text_area("Copy-Paste Prompt Ini ke Midjourney / Flux:", value=prompt_img, height=380)

# =========================================================
# FITUR 2: CONTENT BRAIN V3 VIDEO PROMPT GENERATOR
# =========================================================
with tab2:
    st.header("🚀 Fitur 2: Content Brain V3 & Video Prompt Generator")
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        uploaded_model_gen = st.file_uploader("Upload Foto Model Hasil Fitur 1", type=["jpg", "jpeg", "png"], key="model_gen")
        if uploaded_model_gen: st.image(uploaded_model_gen, use_container_width=True)
    with col_v2:
        uploaded_product_botol = st.file_uploader("Upload Foto Produk Botol NOBAU", type=["jpg", "jpeg", "png"], key="product_botol")
        if uploaded_product_botol: st.image(uploaded_product_botol, use_container_width=True)
            
    st.divider()
    if st.button("🚀 Run Content Brain V3 & Generate Video Prompt", type="primary", use_container_width=True):
        if not uploaded_model_gen or not uploaded_product_botol:
            st.warning("⚠️ Mohon upload KEDUA FOTO terlebih dahulu!")
        else:
            with st.spinner("🤖 Gemini Vision sedang meriset settingan & hook..."):
                img_m_pil = Image.open(uploaded_model_gen)
                img_p_pil = Image.open(uploaded_product_botol)
                sys_prompt_f2 = """
                Analisis Image 1 (Model) dan Image 2 (Botol Produk NOBAU).
                Hasilkan Master Video Prompt UGC 10 detik sesuai format baku berikut.

                FORMAT OUTPUT:
                A continuous 10-second vertical 9:16 smartphone UGC video recorded inside [Deskripsikan lokasi dari Image 1 secara presisi], matching the exact setting of Image 1.

                IDENTITY: Preserve exact facial structure, identity, hair style, skin tone, [Deskripsikan outfit dari Image 1 secara presisi], and natural makeup matching Image 1.

                PRODUCT: Holding the exact compact travel-size 60ml NOBAU spray bottle as visually defined in Image 2. The bottle is small and fits comfortably within a single palm, matching realistic 60ml bottle scale relative to her hand. [Deskripsikan detail visual label & warna botol dari Image 2 secara presisi].

                STORY & TIMELINE (0-10s):
                0-3s (HOOK): [Buatkan ide hook visual & reaksi masalah bau yang relevan dari Image 1 & Image 2]
                3-6s (ACTION): [Aksi mengambil produk, memegang di telapak tangan, menyemprotkan produk sambil bicara ke kamera]
                6-8s (PAYOFF): [Reaksi lega/segar setelah menyemprotkan produk]
                8-10s (CTA): [Memajukan botol 60ml ke kamera dan mengangguk setuju]

                DIALOGUE (Spoken natively in conversational Indonesian, EXACTLY):
                "[Buatkan 1 kalimat dialogue UGC singkat, natural, catchy dalam Bahasa Indonesia yang relevan dengan varian produk di Image 2]"

                CAMERA & STYLE: Authentic Indonesian TikTok creator aesthetic, natural handheld camera shake, soft natural daylight, casual front-facing selfie camera angle.

                CONTINUITY: One continuous generation, no camera cuts, fully clothed, no face morphing, no product redesign, no trigger spray mechanism, no floating limbs, no text or graphics.
                """
                prompt_vid = generate_content_safe(client, sys_prompt_f2, [img_m_pil, img_p_pil], FALLBACK_F2)
                st.success("🚀 Master Video Prompt Flow AI Generated!")
                st.text_area("Copy-Paste Prompt Ini ke Flow AI:", value=prompt_vid, height=380)
