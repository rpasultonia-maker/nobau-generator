import streamlit as st

st.set_page_config(
    page_title="NOBAU AI Content Generator",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 NOBAU AI Content Brain & Prompt Studio")
st.caption("Automation Studio for Scale 1.000 Affiliate UGC Videos")

tab1, tab2 = st.tabs([
    "📌 FITUR 1: Master Image Prompt (Swap Face & Style)", 
    "🚀 FITUR 2: Content Brain V3 Video Prompt (Flow AI)"
])

# =========================================================
# FITUR 1: MASTER PROMPT IMAGE GENERATOR
# =========================================================
with tab1:
    st.header("📌 Fitur 1: Generate Master Image Prompt")
    st.write("Upload Foto Referensi Pose/Style & Foto Wajah Karakter NOBAU:")
    
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
        else:
            prompt_img = """Create a natural smartphone selfie photograph based on the uploaded reference images.

REFERENCE IMAGE ROLE:
Use Image 1 strictly for composition, camera perspective, body pose, clothing style, background environment, lighting, and casual smartphone photography aesthetic.

FACE IDENTITY — CRITICAL:
The woman's face and identity must come strictly from Image 2. Replace the face in Image 1 with Image 2's exact identity. Preserve facial structure, eyes, nose, lips, jawline, skin tone. Do NOT blend faces.

SUBJECT: A young Indonesian woman taking a casual smartphone selfie.
POSE: Seated in the car's driver seat with legs angled sideways, resting left cheek against the left hand, and right hand resting in the lap holding sunglasses.
FACIAL EXPRESSION: Natural relaxed feminine expression with a subtle soft smile, playful and confident.
HAIR: Preserve NOBAU model's recognizable hairstyle from Image 2: voluminous, layered dark brown hair with bouncy curls and soft face-framing fringe.
CLOTHING: Black short-sleeved top or mini-dress with gold button accents, accessorized with a metallic silver watch on the left wrist.
ENVIRONMENT: Modern car cabin interior featuring black leather seating, steering wheel, and an expansive panoramic glass sunroof revealing green foliage and sky above.
CAMERA: Authentic smartphone front-camera selfie perspective, high-angle, 24–28mm equivalent.
LIGHTING: Cool-toned natural daylight softly diffusing through the overhead panoramic glass roof and car windows.
SKIN & REALISM: Natural realistic skin texture, pores, subtle imperfections, no plastic skin, no heavy beauty filters.
PHOTOGRAPHIC STYLE: Authentic Indonesian social-media selfie aesthetic, casual handheld photo.
IDENTITY PRIORITY: Image 2 = Identity & Face. Image 1 = Pose, Outfit, Scene, & Style.
FINAL IMAGE: Believable smartphone selfie of the NOBAU female model in Image 1's exact visual situation."""

            st.success("✨ Master Image Prompt Generated!")
            st.text_area("Copy-Paste Prompt Ini ke Midjourney / Flux:", value=prompt_img, height=350)

# =========================================================
# FITUR 2: CONTENT BRAIN V3 VIDEO PROMPT GENERATOR
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
        else:
            prompt_vid = """A continuous 10-second vertical 9:16 smartphone UGC video recorded inside a modern car cabin with a glass panoramic sunroof, matching the exact setting of Image 1.

IDENTITY: Preserve exact facial structure, identity, long dark wavy brown hair, fair skin tone, dark short-sleeved top with gold side buttons, silver wristwatch, and natural makeup matching Image 1.

PRODUCT: Holding the exact compact travel-size 60ml NOBAU spray bottle as visually defined in Image 2. The bottle is small and fits comfortably within a single palm, matching realistic 60ml bottle scale relative to her hand. White cylindrical bottle with a semi-translucent mist pump cap, clear label "NOBAU DeoFresh PENGHILANG BAU ROKOK", yellow-orange background accents, and "WITH ESSENTIAL OIL" badge.

STORY & TIMELINE (0-10s):
0-3s (HOOK): Creator sits in the driver's seat, winces with a annoyed expression, fanning the air near her face with one hand as if reacting to strong lingering cigarette smoke in the car cabin.
3-6s (ACTION): Picks up the compact 60ml NOBAU bottle from the center console, holding it naturally in one palm, and sprays 2 quick mists into the car cabin air while speaking directly to the selfie camera.
6-8s (PAYOFF): Takes a deep breath, smiles with instant relief, gesturing how quickly the fresh essential oil aroma neutralizes the smoke smell.
8-10s (CTA): Holds the small 60ml NOBAU bottle forward at chest level toward the camera lens, nodding approvingly.

DIALOGUE (Spoken natively in conversational Indonesian, EXACTLY):
"Habis ngerokok di mobil tapi mau jemput doi? Semprot NOBAU Penghilang Bau Rokok, bau apek langsung hilang seketika!"

CAMERA & STYLE: Authentic Indonesian TikTok creator aesthetic, natural handheld camera shake, soft natural daylight entering through the panoramic sunroof, casual front-facing selfie camera angle.

CONTINUITY: One continuous generation, no camera cuts, fully clothed, no face morphing, no product redesign, no trigger spray mechanism, no floating limbs, no text or graphics."""

            st.success("🚀 Master Video Prompt Flow AI Generated!")
            st.text_area("Copy-Paste Prompt Ini ke Flow AI:", value=prompt_vid, height=380)
