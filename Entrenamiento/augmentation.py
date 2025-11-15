import cv2
import numpy as np
import albumentations as A
import glob
import os

# Carpetas de entrada
input_good = r"Entrenamiento\img_aug\Zetas_Buenas"
input_bad = r"Entrenamiento\img_aug\Zetas_Malas"

# Carpetas de salida
output_good = r"Entrenamiento\Zetas_Buena_augmentadas"
output_bad = r"Entrenamiento\Zetas_Malas_augmentadas"
os.makedirs(output_good, exist_ok=True)
os.makedirs(output_bad, exist_ok=True)

# Augmentación para Zetas buenas 
transform_good = A.Compose([
    A.Rotate(limit=25, p=0.8),
    A.Affine(scale=(0.9, 1.1), shear=(-8, 8), translate_percent={"x": (-0.1, 0.1), "y": (-0.1, 0.1)}, p=0.8),
    A.HorizontalFlip(p=0.5),
    A.VerticalFlip(p=0.5),
])

# Augmentación para Zetas malas 
transform_bad = A.Compose([
    A.Rotate(limit=30, p=0.8),
    A.Affine(scale=(0.8, 1.2), shear=(-12, 12), translate_percent={"x": (-0.15, 0.15), "y": (-0.15, 0.15)}, p=0.8),
    A.HorizontalFlip(p=0.5),
    A.VerticalFlip(p=0.5),
    A.GaussNoise(var_limit=(10.0, 50.0), p=0.5),
    A.RandomBrightnessContrast(brightness_limit=0.3, contrast_limit=0.5, p=0.5),
    A.GaussianBlur(blur_limit=(3, 7), p=0.5),
])

def apply_morphology(img):
    """Aplica dilatación o erosión aleatoriamente para simular grosor."""
    kernel = np.ones((3,3), np.uint8)
    choice = np.random.choice(["none", "dilate", "erode"])
    if choice == "dilate":
        return cv2.dilate(img, kernel, iterations=np.random.randint(1,3))
    elif choice == "erode":
        return cv2.erode(img, kernel, iterations=np.random.randint(1,3))
    else:
        return img

def augment_images(input_dir, output_dir, transform, n_aug=5):
    for img_path in glob.glob(os.path.join(input_dir, "*.png")):
        img = cv2.imread(img_path)
        if img is None:
            continue

        base_name = os.path.splitext(os.path.basename(img_path))[0]

        for i in range(n_aug):
            augmented = transform(image=img)["image"]
            augmented = apply_morphology(augmented)  # aplicar dilatación/erosión
            out_path = os.path.join(output_dir, f"{base_name}_aug{i}.png")
            cv2.imwrite(out_path, augmented)

# Ejecutar augmentación
augment_images(input_good, output_good, transform_good, n_aug=5)   # normales
augment_images(input_bad, output_bad, transform_bad, n_aug=10)     # el doble de malas
