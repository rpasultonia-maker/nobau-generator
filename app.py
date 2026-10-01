import streamlit as st

# Config Halaman
st.set_page_config(
    page_title="NOBAU AI Content Generator",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 NOBAU AI Content Brain & Prompt Studio")
st.write("Upload 2 foto di bawah untuk langsung menghasilkan prompt video UGC:")

# =========================================================
# 1. TAMPILAN UPLOAD 2 FOTO (LANGSUNG MUNCUL DI DEPAN)
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
# 2. PROMPT RESULT (OTOMATIS / KETIKA FOTO TERSEDIA)
# =========================================================
if uploaded_model and uploaded_product:
    st.success("✨ Foto Berhasil Diupload! Master Video Prompt Flow AI Generated:")
    
    prompt_result = """A continuous 10-second vertical 9:16 smartphone UGC video recorded in a brightly lit room.

IDENTITY: Preserve exact facial structure, skin tone, hair style, and features as defined in Image 1.
PRODUCT: Holding the exact compact travel-size NOBAU spray bottle as visually defined in Image 2.

STORY & TIMELINE (0-10s):
0-3s (HOOK): Creator dandan di depan kaca.
3-10s (BODY): Memegang produk NOBAU dengan jelas ke kamera."""

    st.text_area("Copy-Paste Prompt Ini ke Flow AI / Midjourney:", value=prompt_result, height=220)
else:
    st.info("💡 Silakan upload kedua foto (Foto Model dan Foto Produk) di atas untuk menampilkan prompt.")
