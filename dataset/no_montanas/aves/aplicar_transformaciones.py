"""
=============================================================
  APLICAR TRANSFORMACIONES - Dataset Aves v1a <15ABR2026>
=============================================================
  Toma las imágenes base generadas por IA y produce el
  dataset completo aplicando las 5 transformaciones.
=============================================================
"""

import os
import random
import shutil
import math
from pathlib import Path
from PIL import Image, ImageEnhance

# ─────────────────────────────────────────────────────────────
#  CONFIGURACIÓN
# ─────────────────────────────────────────────────────────────
BASE_DIR   = Path(r"C:\Users\DELL\.gemini\antigravity\brain\bd2e7544-f8ca-4235-b206-ddbc0f7c3433")
OUTPUT_DIR = Path(__file__).parent   # carpeta pajaros
IMG_SIZE   = (224, 224)
QUALITY    = 92
TARGET     = 500   # imágenes totales deseadas

# Imágenes base generadas (nombre_ave: ruta_archivo)
BASES = {
    "tucan":     "tucan_base_1776864887066.png",
    "turpial":   "turpial_base_1776864901494.png",
    "loro":      "loro_base_1776864924987.png",
    "buho":      "buho_base_1776864943940.png",
    "guacamayo": "guacamayo_base_1776864961067.png",
    "aguila":    "aguila_base_1776864977755.png",
    "flamenco":  "flamenco_base_1776864994494.png",
    "colibri":   "colibri_base_1776865012692.png",
    "pelicano":  "pelicano_base_1776865029896.png",
}

# ─────────────────────────────────────────────────────────────
#  TRANSFORMACIONES
# ─────────────────────────────────────────────────────────────

def transform_rotation(img):
    """Rotación: -20° a +20°."""
    angle = random.uniform(-20, 20)
    return img.rotate(angle, resample=Image.BICUBIC, expand=False)

def transform_flip(img):
    """Volteo horizontal (probabilidad 50%)."""
    if random.random() < 0.5:
        return img.transpose(Image.FLIP_LEFT_RIGHT)
    return img

def transform_brightness(img):
    """Brillo: factor 0.8 a 1.2."""
    factor = random.uniform(0.8, 1.2)
    return ImageEnhance.Brightness(img).enhance(factor)

def transform_zoom(img):
    """Zoom: hasta 20% recortando desde el centro."""
    w, h = img.size
    zf   = random.uniform(0.0, 0.20)
    cw   = int(w * (1 - zf))
    ch   = int(h * (1 - zf))
    l    = (w - cw) // 2
    t    = (h - ch) // 2
    return img.crop((l, t, l + cw, t + ch)).resize(IMG_SIZE, Image.LANCZOS)

def transform_shift(img):
    """Desplazamiento lateral/vertical ±10%."""
    w, h = img.size
    dx   = int(random.uniform(-0.10, 0.10) * w)
    dy   = int(random.uniform(-0.10, 0.10) * h)
    pad  = img.crop((-abs(dx), -abs(dy), w + abs(dx), h + abs(dy)))  # añade padding negro
    # método manual: pegar en canvas y recortar
    canvas = Image.new("RGB", (w + 2*abs(dx), h + 2*abs(dy)), (0, 0, 0))
    canvas.paste(img, (abs(dx) + dx, abs(dy) + dy))
    l = abs(dx)
    t = abs(dy)
    return canvas.crop((l, t, l + w, t + h))

def augment(img: Image.Image) -> Image.Image:
    """Aplica las 5 transformaciones en orden y devuelve 224×224 RGB."""
    img = transform_rotation(img)
    img = transform_flip(img)
    img = transform_brightness(img)
    img = transform_zoom(img)       # ya redimensiona a 224×224
    img = transform_shift(img)
    img = img.resize(IMG_SIZE, Image.LANCZOS)   # garantía final
    return img.convert("RGB")

# ─────────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────────

def main():
    random.seed(42)

    # Verificar bases disponibles
    available = {}
    for nombre, fname in BASES.items():
        path = BASE_DIR / fname
        if path.exists():
            available[nombre] = path
        else:
            print(f"  ⚠  No encontrado: {fname}")

    if not available:
        print("❌ No se encontraron imágenes base. Verifica la ruta.")
        return

    n_birds = len(available)
    per_bird = math.ceil(TARGET / n_birds)

    print("=" * 58)
    print("  GENERANDO DATASET DE AVES - v1a <15ABR2026>")
    print("=" * 58)
    print(f"  Aves base disponibles : {n_birds}")
    print(f"  Variaciones por ave   : {per_bird}")
    print(f"  Total estimado        : {n_birds * per_bird}")
    print(f"  Destino               : {OUTPUT_DIR}")
    print("=" * 58)

    counter = 0
    for nombre, src_path in available.items():
        try:
            base_img = Image.open(src_path).convert("RGB").resize(IMG_SIZE, Image.LANCZOS)
        except Exception as e:
            print(f"  ❌ Error cargando {nombre}: {e}")
            continue

        for i in range(per_bird):
            aug = augment(base_img)
            filename = OUTPUT_DIR / f"{nombre}_{i+1:03d}.jpg"
            aug.save(filename, format="JPEG", quality=QUALITY)
            counter += 1
            print(f"\r  [{counter:>4}] {nombre}_{i+1:03d}.jpg guardado", end="", flush=True)

    print(f"\n\n{'=' * 58}")
    print(f"  ✅ COMPLETADO")
    print(f"     Imágenes generadas : {counter}")
    print(f"     Rango objetivo     : 400 – 600  ✓" if 400 <= counter <= 600 else f"     Total: {counter}")
    print(f"     Carpeta            : {OUTPUT_DIR}")
    print(f"{'=' * 58}")

if __name__ == "__main__":
    main()
