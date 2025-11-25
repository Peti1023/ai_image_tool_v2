from typing import Any

import streamlit as st
from PIL import Image
from transformers import pipeline

# BLIP alapú image captioning modell
CAPTION_MODEL_NAME = "Salesforce/blip-image-captioning-base"


@st.cache_resource(show_spinner=False)
def get_captioner() -> Any:
    """Létrehozza és cache-eli az image captioning pipeline-t (BLIP)."""
    captioner = pipeline(
        "image-to-text",
        model=CAPTION_MODEL_NAME,
    )
    return captioner


def generate_caption(captioner: Any, image: Image.Image) -> str:
    """Képleírás generálása a megadott BLIP modellen keresztül."""
    try:
        result = captioner(image)[0]
        text = result.get("generated_text") or result.get("caption") or ""
        return text.strip()
    except Exception as e:
        print(f"[captioning] Hiba: {e}")
        return ""
