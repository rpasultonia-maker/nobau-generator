import streamlit as st

st.set_page_config(
    page_title="NOBAU AI Content Generator",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 NOBAU AI Content Brain & Prompt Studio")
st.write("Automation Studio for Scale 1.000 Affiliate UGC Videos")

# =========================================================
# 1. AREA UPLOAD FOTO (LANGSUNG TAMPIL DI DEPAN)
# =========================================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Foto Model / Creator")
    uploaded_model = st.file_uploader("Upload Foto Model / Creator", type=["jpg", "jpeg", "png"], key="model")
    if uploaded_model:
        st.image(uploaded_model, use_column_width=True)

with col2:
    st.subheader("2. Foto Produk NOBAU")
    uploaded_product = st.file_uploader("Upload Foto Produk NOBAU", type=["jpg", "jpeg", "png"], key="product")
    if uploaded_product:
        st.image(uploaded_product, use_column_width=True)

st.divider()

# =========================================================
# 2. PARAMETER & PILIHAN 2 FITUR ULTIMATE
# =========================================================
col_param, col_action = st.columns([1, 1])

with col_param:
    st.subheader("📌 Input Parameter Creator")
    niche = st.selectbox(
        "Pilih Niche Creator / Channel:",
        ["Personal Care / Beauty", "Otomotif / Helm / Mobil", "Daily Vlog / Outfit", "Households / Home Care"]
    )
    
    varian = st.selectbox(
        "Pilih Varian Produk NOBAU:",
        [
            "NOBAU DeoFresh Atasi Bau Ketiak",
            "NOBAU Penghilang Bau Helm Pocket",
            "NOBAU Penghilang Bau Helm",
            "NOBAU Penghilang Bau Kaki",
            "NOBAU Penghilang Bau Outfit",
            "NOBAU Penghilang Bau Peci",
            "NOBAU Penghilang Bau Ruangan",
            "NOBAU Penghilang Bau Dapur",
            "NOBAU Penghilang Bau Rokok"
        ]
    )
    
    deskripsi_karakter = st.text_area(
        "Deskripsi Karakter (Opsional):",
        value="Indonesian young adult female, long dark wavy hair, friendly face"
    )

with col_action:
    st.subheader("🎬 Generator Action")
    
    # FITUR 1: MASTER PROMPT IMAGE
    btn_image = st.button("📌 Generate Master Prompt Image", type="secondary", use_container_width=True)
    
    # FITUR 2: CONTENT BRAIN V3 VIDEO PROMPT
    btn_video = st.button("🚀 Run Content Brain V3 & Generate Video Prompt", type="primary", use_container_width=True)

st.divider()

# =========================================================
# 3. LOGIKA EKSEKUSI 2 FITUR
# =========================================================
if btn_image:
    if not uploaded_model or not uploaded_product:
        st.warning("⚠️️ Mohon upload Foto Model dan Foto Produk terlebih dahulu di bagian atas!")
    else:
        st.success("✨ Master Image Prompt Generated!")
        prompt_img = f"A photorealistic studio shot of an {deskripsi_karakter}. Holding {varian}. Clean lighting, 8k resolution, UGC aesthetic --ar 9:16"
        st.text_area("Copy-Paste Image Prompt Ini:", value=prompt_img, height=150)

if btn_video:
    if not uploaded_model or not uploaded_product:
        st.warning("⚠️ Mohon upload Foto Model dan Foto Produk terlebih dahulu di bagian atas!")
    else:
        st.success("🚀 Master Video Prompt Flow AI Generated!")
        prompt_vid = f"""A continuous 10-second vertical 9:16 smartphone UGC video recorded in a brightly lit room.

IDENTITY: Preserve exact facial structure, skin tone, hair style, and features as defined in Image 1 ({deskripsi_karakter}).
PRODUCT (PRECISION SCALE): Holding the exact compact travel-size NOBAU spray bottle as visually defined in Image 2 ({varian}).

STORY & TIMELINE (0-10s):
0-3s (HOOK): Creator dandan di depan kaca. cemas bau pas aktivitas ({niche}).
3-10s (BODY): Memegang produk {varian} dengan jelas ke kamera, langsung segar seketika."""
        
        st.text_area("Copy-Paste Video Prompt Ini ke Flow AI:", value=prompt_vid, height=220)
