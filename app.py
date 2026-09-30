import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. CONFIG & SYSTEM SETTINGS
# ==========================================
st.set_page_config(
    page_title="NOBAU AI Content Generator",
    page_icon="🧪",
    layout="wide"
)

# ==========================================
# 2. MODUL VIDEO PROMPT GENERATOR (UPDATED ENGINE)
# ==========================================
def generate_nobau_video_prompt(niche, varian_produk):
    """
    Generate Master Video Prompt Flow AI (Safe Policy, Skala 60ml, & Dynamic Hook)
    """
    niche_str = str(niche).lower()
    varian_str = str(varian_produk).lower()

    # Logika Dynamic Hook & Latar Kontekstual
    if any(k in niche_str or k in varian_str for k in ["otomotif", "rokok", "helm", "mobil"]):
        bg = "a modern car interior cabin with a glass sunroof"
        outfit = "a stylish, casual short-sleeved top and wristwatch"
        hook = "Creator bereaksi risih bau asap rokok/apek pas mau jemput doi"
        dialogue = '"Mobil bau asap rokok? Semprot NOBAU Penghilang Bau Rokok, langsung fresh seketika!"'
        variant_name = "NOBAU DeoFresh PENGHILANG BAU ROKOK"
    elif any(k in niche_str or k in varian_str for k in ["gym", "olahraga", "sepatu", "kaki"]):
        bg = "a tidy fitness gym corner or sports locker room"
        outfit = "appropriate casual activewear (e.g., hoodie or sports t-shirt)"
        hook = "Creator selesai workout, bereaksi pusing bau sepatu/kaki"
        dialogue = '"Habis nge-gym jangan sampai kaki bau! Semprot NOBAU Kaki, wangi fresh instan!"'
        variant_name = "NOBAU DeoFresh PENGHILANG BAU SEPATU & KAKI"
    else:
        bg = "a brightly lit, aesthetic bedroom vanity setup"
        outfit = "a clean, casual oversized pastel t-shirt covering shoulders completely"
        hook = "Creator dandan di depan kaca, cemas ketiak bau pas aktivitas"
        dialogue = '"Dandan udah cakep, masa ketiak bau? Semprot NOBAU DeoFresh dulu biar fresh seharian!"'
        variant_name = "NOBAU DeoFresh ATASI BAU KETIAK"

    # Master Video Prompt Output
    master_video_prompt = f"""A continuous 10-second vertical 9:16 smartphone UGC video recorded in {bg}.

IDENTITY: Preserve exact facial structure, skin tone, hair style, jewelry, and specific features as defined in Image 1.

OUTFIT (SAFE POLICY): Wearing {outfit}. Fully clothed, non-revealing, safe policy outfit.

PRODUCT (PRECISION SCALE): Holding the exact compact travel-size 60ml/100ml NOBAU spray bottle as visually defined in Image 2. The bottle is small and fits comfortably within a single palm, anchoring realistic scale relative to her hand. Label layout, colors, and white mist pump cap remain 100% consistent with Image 2 ({variant_name}).

STORY & TIMELINE (0-10s):
0-3s (HOOK): {hook}. Show relatable concerned or annoyed expression directly at the camera.
3-6s (ACTION): Picks up the compact 60ml NOBAU bottle and sprays 2 quick mist pumps into the ambient air space (NOT direct skin spray), fanning the mist. Speaks dialogue naturally.
6-8s (PAYOFF): Smells the air with visible relief, smiles brightly, and shows restored confidence.
8-10s (CTA): Holds the small travel-size NOBAU bottle forward at chest level toward the camera lens with a friendly nod.

DIALOGUE (Spoken natively in conversational Indonesian, EXACTLY):
{dialogue}

CAMERA & STYLE: Authentic Indonesian TikTok creator aesthetic, natural handheld camera shake, soft indoor ambient light, casual front-facing selfie perspective.

CONTINUITY: One continuous generation, no camera cuts, no face morphing, no product redesign, no trigger spray mechanism, no floating limbs, no text or graphics."""

    return master_video_prompt


# ==========================================
# 3. STREAMLIT INTERFACE (UI)
# ==========================================
st.title("🧪 NOBAU AI Content Brain & Prompt Studio")
st.caption("Automation Studio for Scale 1.000 Affiliate UGC Videos")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📌 Input Parameter Creator")
    niche_input = st.selectbox(
        "Pilih Niche Creator / Channel:",
        ["Personal Care / Beauty", "Otomotif / Mobil / Rokok", "Gym / Sports / Footwear"]
    )
    
    varian_input = st.selectbox(
        "Pilih Varian Produk NOBAU:",
        ["NOBAU DeoFresh Atasi Bau Ketiak", "NOBAU DeoFresh Penghilang Bau Rokok", "NOBAU DeoFresh Sepatu & Kaki"]
    )

    character_desc = st.text_area("Deskripsi Karakter (Opsional):", "Indonesian young adult female, long dark wavy hair, friendly face")

with col2:
    st.subheader("🎬 Generator Action")
    
    # Tombol 1: Master Image Prompt
    if st.button("🚀 Generate Master Prompt Image", use_container_width=True):
        st.success("Master Image Prompt Ready!")
        st.code(f"A natural 9:16 selfie photo of {character_desc}, recorded in matching location for {niche_input}. Holding a compact 60ml travel-size {varian_input} bottle in her palm. Natural indoor lighting, UGC TikTok aesthetic.", language="text")

    st.divider()

    # Tombol 2: Master Video Prompt (Flow AI Engine)
    if st.button("🚀 Run Content Brain V3 & Generate Video Prompt", type="primary", use_container_width=True):
        try:
            prompt_result = generate_nobau_video_prompt(niche_input, varian_input)
            st.success("Master Video Prompt Flow AI Generated!")
            st.text_area("Copy-Paste Prompt Ini ke Flow AI:", value=prompt_result, height=350)
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
