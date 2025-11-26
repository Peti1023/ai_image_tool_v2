from typing import Any, List, Dict

import streamlit as st
from PIL import Image
from transformers import pipeline

# Vision Transformer alapú kép-osztályozó modell
VIT_MODEL_NAME = "google/vit-base-patch16-224"


@st.cache_resource(show_spinner=False)
def get_vit_classifier() -> Any:
    """ViT alapú image classifier betöltése és cache-elése."""
    clf = pipeline(
        "image-classification",
        model=VIT_MODEL_NAME,
    )
    return clf


def classify_image(
    classifier: Any,
    image: Image.Image,
    top_k: int = 5,
) -> List[Dict]:
    """Képosztályozás a megadott ViT classifierrel.

    Visszatér:
        [
          {"label": "golden_retriever", "score": 0.93},
          {"label": "Labrador_retriever", "score": 0.04},
          ...
        ]
    """
    try:
        outputs = classifier(image, top_k=top_k)

        if isinstance(outputs, dict):
            outputs = [outputs]

        results: List[Dict] = []
        for out in outputs:
            label = out.get("label", "")
            score = float(out.get("score", 0.0))
            results.append({"label": label, "score": score})

        return results
    except Exception as e:
        print(f"[classifier] Hiba a ViT osztályozás során: {e}")
        return []
