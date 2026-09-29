import streamlit as st
import google.generativeai as genai
from PIL import Image

# Config Halaman
st.set_page_config(page_title="NOBAU Content & Prompt Generator", page_icon="⚡", layout="wide")

st.title("⚡ NOBAU Production System")
st.caption("Platform Otomatisasi Prompt Image & Content Brain Video V3 untuk NOBAU")

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

# Tampilan Upload Gambar (2 Slot Utama)
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Scene Reference (Pose & Environment)")
    scene_file = st.file_uploader("Upload foto pose / baju / background", type=["jpg", "jpeg", "png"], key="scene")
    if scene_file:
        scene_img = Image.open(scene_file)
        st.image(scene_img, use_container_width=True)

with col2:
    st.subheader("2. NOBAU Face & Product Reference")
    face_file = st.file_uploader("Upload foto master wajah model / produk NOBAU", type=["jpg", "jpeg", "png"], key="face")
    if face_file:
        face_img = Image.open(face_file)
        st.image(face_img, use_container_width=True)

st.markdown("---")

# MENU PILIHAN FITUR (TABS)
tab1, tab2 = st.tabs(["📸 1. MASTER PROMPT IMAGE (Fitur Awal)", "🎬 2. VIDEO CONTENT BRAIN V3 (Flow AI 10s)"])

# ==========================================
# TAB 1: FITUR GENERATE PROMPT FOTO/IMAGE (LAMA - AMAN 100%)
# ==========================================
with tab1:
    st.info("Fitur ini menghasilkan Master Prompt Foto/Selfie Statis untuk Midjourney / Flow AI Image.")
    
    IMAGE_MASTER_PROMPT = """
You are an expert AI prompt engineer. Analyze the two provided images:
- Image 1 is the SCENE REFERENCE (pose, composition, framing, outfit, background, lighting, casual selfie aesthetic).
- Image 2 is the NOBAU FACE REFERENCE (exact female model identity, facial structure, skin tone, features, hairstyle).

Generate a highly structured, photorealistic AI image generation prompt following this EXACT template:

Create a highly natural, photorealistic smartphone selfie photograph based on the uploaded reference images.

REFERENCE IMAGE ROLE:
Use Image 1 strictly for composition, camera perspective, body pose, clothing style, background environment, lighting, and casual smartphone photography aesthetic.

FACE IDENTITY — CRITICAL:
The woman's face and identity must come strictly from Image 2. Replace the face in Image 1 with Image 2's exact identity. Preserve facial structure, eyes, nose, lips, jawline, skin tone. Do NOT blend faces.

SUBJECT: A young Indonesian woman taking a casual smartphone selfie.
POSE: [Extract detailed pose from Image 1]
FACIAL EXPRESSION: Natural relaxed feminine expression with a subtle soft smile, playful and confident.
HAIR: Preserve NOBAU model's recognizable hairstyle from Image 2.
CLOTHING: [Extract exact clothing from Image 1]
ENVIRONMENT: [Extract exact background details from Image 1]
CAMERA: Authentic smartphone front-camera selfie perspective, high-angle, 24–28mm equivalent.
LIGHTING: [Extract lighting quality from Image 1]
SKIN & REALISM: Natural realistic skin texture, pores, subtle imperfections, no plastic skin, no heavy beauty filters.
PHOTOGRAPHIC STYLE: Authentic Indonesian social-media selfie aesthetic, casual handheld photo.
IDENTITY PRIORITY: Image 2 = Identity & Face. Image 1 = Pose, Outfit, Scene, & Style.
FINAL IMAGE: Believable smartphone selfie of the NOBAU female model in Image 1's exact visual situation.
"""
    if st.button("🚀 Generate Master Prompt Image (Foto Statis)", type="primary", use_container_width=True):
        if not scene_file or not face_file:
            st.error("Harap upload KEDUA foto terlebih dahulu!")
        else:
            with st.spinner("Meracik Master Prompt Foto..."):
                try:
                    model = genai.GenerativeModel('gemini-3.8-flash')
                    response = model.generate_content([IMAGE_MASTER_PROMPT, scene_img, face_img])
                    st.success("Prompt Foto Berhasil Dibuat!")
                    st.code(response.text, language="text")
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")

# ==========================================
# TAB 2: FITUR VIDEO CONTENT BRAIN V3 (BARU)
# ==========================================
with tab2:
    st.info("Fitur ini melakukan riset tren otomatis + meracik Script Video UGC 10 Detik & Prompt Video Flow AI V3.")
    
    LOCKED_VIDEO_MASTER = """
You operate as the CONTENT BRAIN and MASTER PROMPT GENERATOR for NOBAU.

Perform web search research on current Indonesian social media trends/insights regarding daily odor problems, relatable creator hooks, and viral TikTok formats before generating the brief.

STRICT COMPLIANCE RULES (NOBAU MASTER PRODUCTION SYSTEM V3):
1. CORE PRODUCTION RULE: Exactly ONE complete 10-second video, 9:16 vertical, one generation, continuous and coherent. No multi-clips or split generation.
2. VISUAL IDENTITY: Natural Smartphone UGC style, authentic Indonesian TikTok creator feeling, casual everyday environment. NEVER use the word "realistic".
3. CHARACTER SYSTEM: Use uploaded face reference (Image 2) strictly for identity.
4. PRODUCT LOCK: Use uploaded product image (Image 2) strictly. Preserve bottle shape, colors, cap, typography. NEVER use or interpret product as "trigger sprayer", "trigger bottle", or "trigger mechanism". Word "spray" refers ONLY to application action.
5. CONTENT PHILOSOPHY: Strong hook, relatable problem, soft selling, natural CTA.
6. RHYTHM: 0-3s HOOK/PROBLEM -> 3-6s ACTION/SOLUTION -> 6-8s REACTION/PAYOFF -> 8-10s SOFT CTA.
7. DIALOGUE: Spoken natural Indonesian. If marked exact, must match exactly.
8. RESTRICTIONS: No AI-commercial look, no face morphing, no floating hands, no extra fingers, no subtitles/watermarks, no "realistic" wording.

OUTPUT FORMAT:

SECTION 1: NOBAU CONTENT BRAIN (Bahasa Indonesia)
- **Brief & Angle Konten:** (Analisis situasi foto + tren/insight riset masalah bau harian).
- **Target Karakter:** (Pria/Wanita + konteks peran).
- **Breakdown Timeline 10s:** (0-3s Hook, 3-6s Action, 6-8s Payoff, 8-10s Soft CTA).
- **Dialogue Script (EXACT):** (Dialog bahasa Indonesia).
- **Caption & Hashtag Social Media:**

SECTION 2: FINAL FLOW AI PROMPT (English - Locked Structure)
Structure: IDENTITY -> PRODUCT -> STORY -> DIALOGUE -> STYLE -> CONTINUITY

```text
A continuous 10-second vertical 9:16 smartphone UGC video of a young Indonesian creator recorded in [describe environment from Image 1].

IDENTITY: Preserve exact facial structure, hair, and skin tone from Image 2 reference. Wearing [describe outfit from Image 1].

PRODUCT: Holding the exact NOBAU spray bottle as shown in Image 2. Bottle shape, cap, label, and colors remain 100% consistent. Hand naturally holding the bottle.

STORY & TIMELINE (0-10s):
- 0-3s (HOOK): [Action showing problem/hook].
- 3-6s (ACTION): [Casual spray application towards target object].
- 6-8s (PAYOFF): [Satisfied facial expression/reaction].
- 8-10s (CTA): [Casual recommendation/pointing to product].

DIALOGUE (Spoken natively in conversational Indonesian, EXACTLY):
"[Insert exact spoken dialogue]"

CAMERA & STYLE: Authentic Indonesian TikTok creator aesthetic, natural handheld movement, everyday Indonesian lighting, casual selfie perspective.

CONTINUITY: One continuous generation, no camera cuts, no face morphing, no product redesign, no trigger spray mechanism, no floating limbs, no text or graphics.
