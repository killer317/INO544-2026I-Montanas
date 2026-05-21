import os
import random
from PIL import Image, ImageEnhance

TARGET_TOTAL = 400 # 100 per image
IMG_SIZE = (224, 224)
OUTPUT_DIR = "C:\\Users\\DELL\\Downloads\\pajaros"

base_images = {
    "tucan": "C:\\Users\\DELL\\.gemini\\antigravity\\brain\\17c131be-4773-42b8-8290-a0dac6a40955\\tucan_1776864922718.png",
    "turpial": "C:\\Users\\DELL\\.gemini\\antigravity\\brain\\17c131be-4773-42b8-8290-a0dac6a40955\\turpial_1776864936588.png",
    "loro": "C:\\Users\\DELL\\.gemini\\antigravity\\brain\\17c131be-4773-42b8-8290-a0dac6a40955\\loro_1776864954479.png",
    "buho": "C:\\Users\\DELL\\.gemini\\antigravity\\brain\\17c131be-4773-42b8-8290-a0dac6a40955\\buho_1776864967708.png"
}

def augment_image(img):
    img = img.convert('RGB')
    
    # Rotation -20 to 20
    angle = random.uniform(-20, 20)
    img = img.rotate(angle, resample=Image.BILINEAR, expand=False)
    
    # Horizontal Flip
    if random.choice([True, False]):
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
        
    # Brightness 0.8 to 1.2
    enhancer = ImageEnhance.Brightness(img)
    brightness_factor = random.uniform(0.8, 1.2)
    img = enhancer.enhance(brightness_factor)
    
    # Zoom
    w, h = img.size
    zoom_factor = random.uniform(1.0, 1.2)
    new_w = int(w * zoom_factor)
    new_h = int(h * zoom_factor)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    
    # Shift 10%
    max_shift_w = int(w * 0.10)
    max_shift_h = int(h * 0.10)
    shift_w = random.randint(-max_shift_w, max_shift_w)
    shift_h = random.randint(-max_shift_h, max_shift_h)
    
    left = (new_w - w) // 2 - shift_w
    top = (new_h - h) // 2 - shift_h
    right = left + w
    bottom = top + h
    
    img = img.crop((left, top, right, bottom))
    img = img.resize(IMG_SIZE, Image.LANCZOS)
    
    return img

def main():
    generated_count = 0
    images_per_class = TARGET_TOTAL // len(base_images)
    
    for bird_name, path in base_images.items():
        try:
            base_img = Image.open(path)
            for i in range(images_per_class):
                aug_img = augment_image(base_img.copy())
                filename = os.path.join(OUTPUT_DIR, f"{bird_name}_{i+1:03d}.jpg")
                aug_img.save(filename, "JPEG", quality=95)
                generated_count += 1
                if generated_count % 50 == 0:
                    print(f"Generadas {generated_count}/{TARGET_TOTAL}...")
        except Exception as e:
            print(f"Error procesando {bird_name}: {e}")

if __name__ == "__main__":
    main()
