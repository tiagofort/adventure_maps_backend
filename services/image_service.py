from pathlib import Path
import base64
import cv2
import numpy as np
from skimage.feature import local_binary_pattern
from skimage.color import rgb2gray

BASE_DIR = Path(__file__).resolve().parent

# ----------------- Utils de pré-processamento -----------------
def crop_and_resize_to_target(img, target_inner_size=(322, 178), border_ratio=0.12):
    h, w = img.shape[:2]
    top = int(h * border_ratio)
    bottom = int(h * (1 - border_ratio))
    left = int(w * border_ratio)
    right = int(w * (1 - border_ratio))
    inner = img[top:bottom, left:right]

    inner_h, inner_w = inner.shape[:2]
    target_w, target_h = target_inner_size
    scale_w = target_w / inner_w
    scale_h = target_h / inner_h
    scale = min(scale_w, scale_h)
    new_w = int(inner_w * scale)
    new_h = int(inner_h * scale)
    resized = cv2.resize(inner, (new_w, new_h), interpolation=cv2.INTER_AREA)

    canvas = np.zeros((target_h, target_w, 3), dtype=np.uint8)
    y_off = (target_h - new_h) // 2
    x_off = (target_w - new_w) // 2
    canvas[y_off:y_off+new_h, x_off:x_off+new_w] = resized

    return canvas, inner

def normalize_contrast(img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l_eq = clahe.apply(l)
    lab_eq = cv2.merge((l_eq, a, b))
    return cv2.cvtColor(lab_eq, cv2.COLOR_LAB2BGR)

# ----------------- Comparadores -----------------
def compare_histogram(prep_img1, prep_img2):
    hsv1 = cv2.cvtColor(prep_img1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(prep_img2, cv2.COLOR_BGR2HSV)
    hist1 = cv2.calcHist([hsv1], [0, 1], None, [50, 60], [0, 180, 0, 256])
    hist2 = cv2.calcHist([hsv2], [0, 1], None, [50, 60], [0, 180, 0, 256])
    cv2.normalize(hist1, hist1, 0, 1, cv2.NORM_MINMAX)
    cv2.normalize(hist2, hist2, 0, 1, cv2.NORM_MINMAX)
    score = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    return float(score)

def compare_images_features(prep_img1, prep_img2):
    orb = cv2.ORB_create(nfeatures=1500)
    kp1, des1 = orb.detectAndCompute(prep_img1, None)
    kp2, des2 = orb.detectAndCompute(prep_img2, None)
    if des1 is None or des2 is None:
        return 0.0
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    if len(matches) == 0:
        return 0.0
    avg_distance = sum([m.distance for m in matches]) / len(matches)
    normalized_score = 1.0 / (1.0 + avg_distance)
    return float(normalized_score)

def compare_lbp(img1, img2, P=8, R=1):
    """LBP para textura"""
    gray1 = rgb2gray(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
    gray2 = rgb2gray(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
    lbp1 = local_binary_pattern(gray1, P, R, method="uniform")
    lbp2 = local_binary_pattern(gray2, P, R, method="uniform")

    hist1, _ = np.histogram(lbp1.ravel(), bins=np.arange(0, P + 3), range=(0, P + 2), density=True)
    hist2, _ = np.histogram(lbp2.ravel(), bins=np.arange(0, P + 3), range=(0, P + 2), density=True)

    # distância qui-quadrado (quanto menor, mais parecido)
    eps = 1e-7
    chi_sq = 0.5 * np.sum(((hist1 - hist2) ** 2) / (hist1 + hist2 + eps))
    score = 1.0 / (1.0 + chi_sq)  # normaliza para 0..1
    return float(score)

# ----------------- Função principal de comparação -----------------
def compare_image(uploaded_img, images_db, threshold=0.5, target_inner_size=(322, 178), border_ratio=0.17, debug=False):
    best_match = None
    best_score = -1.0

    uploaded_copy = uploaded_img.copy()
    uploaded_copy = normalize_contrast(uploaded_copy)

    for img_info in images_db:
        ref_img_path = BASE_DIR / img_info["path"]
        ref_img = cv2.imread(str(ref_img_path))
        if ref_img is None:
            continue

        ref_img = normalize_contrast(ref_img)

        prep_uploaded, _ = crop_and_resize_to_target(uploaded_copy, target_inner_size, border_ratio)
        prep_ref, _ = crop_and_resize_to_target(ref_img, target_inner_size, border_ratio)

        # Comparações híbridas
        hist_score = compare_histogram(prep_uploaded, prep_ref)
        feature_score = compare_images_features(prep_uploaded, prep_ref)
        lbp_score = compare_lbp(prep_uploaded, prep_ref)

        # Combinação (ajuste pesos conforme desempenho)
        combined_score = (0.5 * hist_score) + (0.3 * feature_score) + (0.2 * lbp_score)

        if combined_score > best_score and combined_score > threshold:
            best_score = combined_score
            best_match = img_info.copy()
            best_match["score"] = combined_score

    return best_match
