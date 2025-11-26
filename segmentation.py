from typing import Any

import streamlit as st
from PIL import Image
from rembg import remove


@st.cache_resource(show_spinner=False)
def get_bg_remover() -> Any:
    """Dummy resource a cache-hez – a tényleges logikát a `remove_background` hívja."""
    # A rembg.remove közvetlenül hívható, itt csak egy cache-elt objektumra van szükségünk.
    return object()


def remove_background(_remover: Any, image: Image.Image) -> Image.Image:
    """Háttér eltávolítása a `rembg` csomag segítségével.

    A visszatérési érték egy átlátszó hátterű (RGBA) kép.
    """
    try:
        out = remove(image)
        if isinstance(out, bytes):
            from io import BytesIO

            return Image.open(BytesIO(out)).convert("RGBA")
        elif isinstance(out, Image.Image):
            return out.convert("RGBA")
        else:
            raise RuntimeError("Ismeretlen visszatérési típus a rembg.remove függvényből.")
    except Exception as e:
        print(f"[segmentation] Hiba: {e}")
        return image.convert("RGBA")
