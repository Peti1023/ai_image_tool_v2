# AI Képstúdió

Interaktív, webes képszerkesztő alkalmazás, amely többféle mesterséges intelligencia modellt használ:

- 📝 **Képleírás (BLIP)**
- ✂️ **Háttér eltávolítás (rembg / U²-Net)**
- 🧠 **Képosztályozás (ViT – Vision Transformer)**

A projekt célja, hogy könnyen futtatható, átlátható és bővíthető példát adjon AI-alapú képfeldolgozásra.

---

## 1. Fő funkciók

### 📝 1.1 Képleírás (Image Captioning – BLIP)

- Modell: `Salesforce/blip-image-captioning-base`
- Feladat: automatikus, **angol nyelvű** szöveges leírás generálása a feltöltött képről.
- Példa output:  
  `a dog running in the grass`

### ✂️ 1.2 Háttér eltávolítás (Segmentation – rembg / U²-Net)

- Könyvtár: `rembg` (U²-Net alapú megoldás)
- Feladat: a kép fő objektumának kivágása, háttér eltávolítása.
- Eredmény: átlátszó hátterű PNG (RGBA), letölthető fájlként.

### 🧠 1.3 Képosztályozás (Image Classification – ViT)

- Modell: `google/vit-base-patch16-224`
- Feladat: megmondani, **mi látható a képen** (top-5 kategória).
- Eredmény: kategória (label) + valószínűség:
  - pl. `golden_retriever – 93.5%`

---

## 2. Technológiai stack

- **Nyelv:** Python 3.11 (ajánlott)
- **Framework:** [Streamlit](https://streamlit.io/) – webes UI
- **AI / ML:**
  - [PyTorch](https://pytorch.org/)
  - [Hugging Face Transformers](https://huggingface.co/transformers/)
  - `rembg` + `onnxruntime` (háttér eltávolítás)
- **Képfeldolgozás:**
  - `Pillow` (PIL)
  - `opencv-python`
- **Egyéb:**
  - `numpy` – numerikus műveletek

> ⚠️ **Fontos:** bizonyos csomagok (pl. `onnxruntime`) jelenleg nem támogatják a Python 3.14-et, ezért a projektet **Python 3.11** használatára érdemes beállítani.

---

## 3. Mappastruktúra

```text
ai_image_tool_v2/
├── app.py               # Streamlit alkalmazás belépési pontja
├── README.md            # Projekt leírása
├── requirements.txt     # Python függőségek
└── src/
    ├── __init__.py
    ├── utils.py         # Kisegítő függvények (pl. PIL Image -> bytes)
    ├── captioning.py    # BLIP alapú image captioning logika
    ├── segmentation.py  # Háttér eltávolítás rembg-vel
    └── classifier.py    # ViT alapú képosztályozás logika
```

### 3.1 Fő modulok röviden

#### `app.py`

- Streamlit app konfiguráció (`st.set_page_config`)
- Kép feltöltése (`st.file_uploader`)
- Layout:
  - Bal oldalt: **Eredeti kép**
  - Jobb oldalt: **3 tab**
    - „Képleírás (BLIP)”
    - „Háttér eltávolítás”
    - „Képosztályozás (ViT)”
- Modern UI egyedi CSS-sel (sötét téma, kártyás elrendezés).

#### `src/captioning.py`

- `get_captioner()`  
  → @st.cache_resource segítségével cache-elt BLIP pipeline:

  ```python
  captioner = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
  ```

- `generate_caption(captioner, image)`  
  → visszaad egy rövid, angol nyelvű leírást a képről.

#### `src/segmentation.py`

- `get_bg_remover()`  
  → dummy objektum cache-hez (a tényleges munka a `rembg.remove`).
- `remove_background(remover, image)`  
  → `rembg.remove(image)` hívás, végeredmény: RGBA, átlátszó hátterű kép.

#### `src/classifier.py`

- `get_vit_classifier()`  
  → ViT alapú image-classification pipeline:

  ```python
  clf = pipeline("image-classification", model="google/vit-base-patch16-224")
  ```

- `classify_image(classifier, image, top_k=5)`  
  → listát ad vissza:  
  `[{ "label": "golden_retriever", "score": 0.93 }, ...]`

#### `src/utils.py`

- `pil_to_bytes(image, format="PNG")`  
  → PIL Image → bytes, letöltéshez (`st.download_button`-hoz).

---

## 4. Telepítés

### 4.1 Előfeltételek

- Python 3.11.x telepítve
- Git (ha repóból klónozol)

### 4.2 Klónozás vagy ZIP

**Git klónozás:**

```bash
git clone <repo-url>
cd ai_image_tool_v2
```

**VAGY:** Zip letöltése, kicsomagolás, majd:

```bash
cd ai_image_tool_v2
```

### 4.3 Virtuális környezet létrehozása (Windows, Python 3.11)

```bash
py -3.11 -m venv .venv
```

Aktiválás (PowerShell):

```bash
.\.venv\Scripts\Activate.ps1
python --version   # itt Python 3.11.x-et kell látni
```

### 4.4 Függőségek telepítése

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Ha az `onnxruntime` külön hiányzik:

```bash
pip install onnxruntime
```

---

## 5. Futtatás

Aktív virtuális környezetben:

```bash
streamlit run app.py
```

A Streamlit alapértelmezett címe:

- http://localhost:8501

---

## 6. Használat

1. Nyisd meg az appot a böngészőben (pl. `http://localhost:8501`).
2. Bal oldali sávban (sidebar) tölts fel egy képet (`PNG`, `JPG`, `JPEG`).
3. A fő nézetben:
   - bal oldalt **az eredeti kép** látható,
   - jobb oldalt 3 tab:

### 6.1 Képleírás (BLIP)

- Tab: **„📝 Képleírás (BLIP)”**
- A BLIP modell automatikusan generál egy leírást a képről.
- Az eredmény zöld `success` boxban jelenik meg.

### 6.2 Háttér eltávolítás

- Tab: **„✂️ Háttér eltávolítás”**
- A `rembg` segítségével levágja a hátteret.
- Az output kép alatt egy gombbal letölthető:
  - `background_removed.png`
  - átlátszó (RGBA) PNG.

### 6.3 Képosztályozás (ViT)

- Tab: **„🧠 Képosztályozás (ViT)”**
- A ViT modell top-5 kategóriát és valószínűséget ad vissza.
- Soronként jelenik meg:  
  `**label** – XX.X%`

---

## 7. Modell-cache és teljesítmény

A nagy modellek betöltése drága, ezért:

- Az AI modellek (BLIP, ViT, rembg „wrapper”) `@st.cache_resource`-szal vannak cache-elve.
- A modell **csak egyszer töltődik le és inicializálódik**, utána a további hívások már gyorsabbak.
- Első futáskor időigényes lehet a modellek letöltése (Hugging Face-ről), ez normális.

---

## 8. Gyakori hibák és megoldások

### 8.1 Python 3.14 vs. 3.11

Ha ilyen hibákat látsz:

- `Requires-Python <3.14`
- `Could not find a version that satisfies the requirement onnxruntime`

Akkor valószínűleg Python **3.14** alatt fut a projekt.

**Megoldás:**

- győződj meg róla, hogy a venv 3.11-ből készül:

  ```bash
  py -3.11 -m venv .venv
  .\.venv\Scripts\Activate.ps1
  python --version  # Python 3.11.x
  ```

### 8.2 Sérült venv / import hibák (numpy, pillow, regex, stb.)

Ha sokféle `ImportError` jelenik meg (pl. `DLL load failed`), általában:

- a venv-ben lévő csomagok keveredtek,
- vagy más Python verzióra váltottál közben.

**Biztos reset:**

```bash
rmdir /s /q .venv      # Windows, PowerShell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## 9. Továbbfejlesztési ötletek

- Magyar nyelvű képleírás (BLIP output fordítása).
- Extra képszerkesztő funkciók:
  - fényerő, kontraszt, blur, fekete-fehér filter.
- Undo/Redo (többlépéses szerkesztési történet).
- Export ZIP-be:
  - eredeti kép,
  - háttér-mentesített PNG,
  - képleírás .txt-ben,
  - képosztályozás JSON-ben.

---

## 10. Napi használati „cheat sheet”

Ha már egyszer mindent beállítottál, **napi induláshoz** elég ennyi:

```bash
cd "D:. felev\haladoprgramozas i_image_tool_v2"
.\.venv\Scripts\Activate.ps1
streamlit run app.py
```


