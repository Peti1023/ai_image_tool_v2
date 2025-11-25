# AI Képstúdió – Könnyű, modern AI képszerkesztő

Ez egy **VS Code-ban** könnyen futtatható, modern felületű AI képszerkesztő alkalmazás, amely három fő AI funkciót tartalmaz:

1. 📝 **Képleírás (Image Captioning)** – BLIP modellel automatikus leírást készít a képről.
2. ✂️ **Háttér eltávolítás (Segmentation)** – U²-Net alapú háttéreltávolítás a `rembg` csomagon keresztül.
3. 🧠 **Képosztályozás (ViT – Vision Transformer)** – `google/vit-base-patch16-224` modellel megpróbálja megmondani, „mi van a képen”.

A 3. modell (ViT) **jóval könnyebb**, mint egy Stable Diffusion diffusion modell – sokkal gyorsabban fut CPU-n is, de mégis „okos” funkciót ad a képszerkesztőhöz.

Frontend: **Streamlit** + egy kis egyedi CSS → letisztult, kártyás, felhasználóbarát UI.

---

## Telepítés

### 1. Lépj be a projekt mappájába

```bash
cd ai_image_tool_v2
```

### 2. (Ajánlott) Virtuális környezet

```bash
python -m venv .venv

# Windows PowerShell:
.venv\Scripts\Activate.ps1

# Windows cmd:
# .venv\Scripts\activate.bat

# Linux / macOS:
# source .venv/bin/activate
```

### 3. Függőségek telepítése

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

> Ha hibát kapsz `onnxruntime` hiánya miatt, futtasd külön:
> ```bash
> pip install onnxruntime
> ```

---

## Futtatás

```bash
streamlit run app.py
```

Ezután a böngészőben (általában http://localhost:8501) megjelenik az alkalmazás.

---

## Fő funkciók

- **AI Képleírás (BLIP)** – természetes nyelvű leírás a képről.
- **Háttér eltávolítás** – átlátszó (PNG, RGBA) háttérrel menthető a kivágott objektum.
- **Képosztályozás (ViT)** – top-5 label + valószínűség.

Az app **tabs**-os, kártyás UI-t használ, minden funkció külön fülön érhető el, ugyanazon feltöltött kép fölött.
