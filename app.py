import io

import streamlit as st
from PIL import Image

from src.captioning import get_captioner, generate_caption
from src.segmentation import get_bg_remover, remove_background
from src.classifier import get_vit_classifier, classify_image
from src.utils import pil_to_bytes


st.set_page_config(
    page_title="AI Képstúdió",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --- Egy kis modern CSS a szebb UI-hoz ---

CUSTOM_CSS = """<style>
/* Háttér színek és font */
body, .stApp {
    background: radial-gradient(circle at top left, #1f2933, #0b1017);
    color: #f9fafb;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

/* Oldalcím */
h1 {
    font-weight: 700;
}

/* Kártya-stílus a boxokhoz */
.ai-card {
    background: rgba(15,23,42,0.9);
    border-radius: 18px;
    padding: 18px 18px 14px 18px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.45);
    border: 1px solid rgba(148,163,184,0.25);
}

/* Tabok testreszabása */
.stTabs [role="tablist"] {
    gap: 12px;
}

.stTabs [role="tab"] {
    padding: 10px 18px;
    border-radius: 999px;
    background-color: #020617;
    color: #e5e7eb;
    border: 1px solid rgba(148,163,184,0.3);
}

.stTabs [role="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #0ea5e9, #6366f1);
    color: white;
    border: none;
}

/* File uploader kicsit kompaktabb */
.css-1u9qpc5, .stFileUploader {
    padding: 12px !important;
}

/* Letöltés gomb */
.stDownloadButton button {
    border-radius: 999px;
    padding: 8px 18px;
}

/* Spinner szín */
.stSpinner > div {
    border-top-color: #0ea5e9;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# --- Oldalcím és leírás ---

st.markdown(
    """<h1>🖼️ AI Képstúdió</h1>""",
    unsafe_allow_html=True,
)
st.write(
    "Tölts fel egy képet, és használd az **AI eszközöket**: "
    "képleírás (BLIP), háttér eltávolítás (rembg) és képosztályozás (ViT)."
)

# --- Oldalsáv ---

with st.sidebar:
    st.header("📥 Kép feltöltése")
    uploaded_file = st.file_uploader(
        "PNG / JPG / JPEG",
        type=["png", "jpg", "jpeg"],
        help="Válassz egy képet, amin dolgozni szeretnél.",
    )

    st.markdown("---")
    st.caption(
        "ℹ️ A modellek első futtatása lassabb lehet, "
        "mert ilyenkor töltődnek le és töltődnek be."
    )

if not uploaded_file:
    st.info("⬅️ Kezdéshez tölts fel egy képet a bal oldali panelen.")
    st.stop()

# --- Kép beolvasása ---

input_bytes = uploaded_file.read()
input_image = Image.open(io.BytesIO(input_bytes)).convert("RGB")

# --- Elrendezés: bal oldalt az eredeti, jobb oldalt a tabok outputja ---

left_col, right_col = st.columns([1, 1.2])

with left_col:
    st.markdown('<div class="ai-card">', unsafe_allow_html=True)
    st.subheader("Eredeti kép")
    st.image(input_image, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with right_col:
    tabs = st.tabs(
        [
            "📝 Képleírás (BLIP)",
            "✂️ Háttér eltávolítás",
            "🧠 Képosztályozás (ViT)",
        ]
    )

    # --- 1. TAB – Képleírás ---

    with tabs[0]:
        st.markdown('<div class="ai-card">', unsafe_allow_html=True)
        st.subheader("Automatikus képleírás")
        with st.spinner("BLIP modell futtatása..."):
            captioner = get_captioner()
            caption_text = generate_caption(captioner, input_image)

        if caption_text:
            st.success(caption_text)
        else:
            st.error("Nem sikerült képleírást generálni.")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- 2. TAB – Háttér eltávolítás ---

    with tabs[1]:
        st.markdown('<div class="ai-card">', unsafe_allow_html=True)
        st.subheader("Háttér eltávolítása")

        with st.spinner("Háttér eltávolítása (rembg + U²-Net)..."):
            remover = get_bg_remover()
            result_image = remove_background(remover, input_image)

        st.image(result_image, use_container_width=True)

        dl_bytes = pil_to_bytes(result_image)
        st.download_button(
            "📥 Kivágott kép letöltése (PNG)",
            data=dl_bytes,
            file_name="background_removed.png",
            mime="image/png",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # --- 3. TAB – Képosztályozás (ViT) ---

    with tabs[2]:
        st.markdown('<div class="ai-card">', unsafe_allow_html=True)
        st.subheader("Képosztályozás Vision Transformerrel")

        with st.spinner("ViT modell futtatása..."):
            vit = get_vit_classifier()
            vit_results = classify_image(vit, input_image, top_k=5)

        if vit_results:
            for item in vit_results:
                label = item["label"]
                score = item["score"] * 100
                st.write(f"**{label}** – {score:.1f}%")
        else:
            st.error("Nem sikerült osztályozni a képet.")
        st.markdown("</div>", unsafe_allow_html=True)
