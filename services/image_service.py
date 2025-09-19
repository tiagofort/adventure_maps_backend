from pathlib import Path
import base64
import cv2
import numpy as np

BASE_DIR = Path(__file__).resolve().parent

# ----------------- Utils de pré-processamento -----------------
def crop_and_resize_to_target(img, target_inner_size=(322, 178), border_ratio=0.12):
    """
    Remove bordas proporcionais e redimensiona o interior mantendo proporção.
    Retorna (resized, crop_original).
    """
    h, w = img.shape[:2]
    top = int(h * border_ratio)
    bottom = int(h * (1 - border_ratio))
    left = int(w * border_ratio)
    right = int(w * (1 - border_ratio))
    inner = img[top:bottom, left:right]  # <- crop sem resize

    # Redimensiona mantendo proporção
    inner_h, inner_w = inner.shape[:2]
    target_w, target_h = target_inner_size
    scale_w = target_w / inner_w
    scale_h = target_h / inner_h
    scale = min(scale_w, scale_h)
    new_w = int(inner_w * scale)
    new_h = int(inner_h * scale)
    resized = cv2.resize(inner, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # Pad central para ter exatamente target_inner_size
    canvas = np.zeros((target_h, target_w, 3), dtype=np.uint8)
    y_off = (target_h - new_h) // 2
    x_off = (target_w - new_w) // 2
    canvas[y_off:y_off+new_h, x_off:x_off+new_w] = resized

    return canvas, inner


# ----------------- Normalização de contraste -----------------
def normalize_contrast(img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l_eq = clahe.apply(l)
    lab_eq = cv2.merge((l_eq, a, b))
    return cv2.cvtColor(lab_eq, cv2.COLOR_LAB2BGR)


# ----------------- Redimensionamento condicional (nova lógica) -----------------
def resize_based_on_user(uploaded_img, ref_img, target_inner_size=(322, 178), border_ratio=0.12):
    """
    Lógica baseada no tamanho do usuário:
    - Se a imagem do usuário for pequena (aprox 443x338) -> redimensiona apenas a base
    - Se a imagem do usuário for grande (aprox 894x701) -> redimensiona ambas
    """
    h_u, w_u = uploaded_img.shape[:2]

    # Definir ranges aproximados
    min_w, min_h = 440, 335  # imagens pequenas
    max_w, max_h = 900, 720  # imagens grandes

    if min_w <= w_u <= max_w and min_h <= h_u <= max_h:
        # Imagem do usuário grande -> redimensionar ambas
        prep_uploaded, _ = crop_and_resize_to_target(uploaded_img, target_inner_size, border_ratio)
        prep_ref, _ = crop_and_resize_to_target(ref_img, target_inner_size, border_ratio)
    else:
        # Imagem do usuário pequena -> redimensionar apenas a base
        prep_uploaded = uploaded_img
        prep_ref, _ = crop_and_resize_to_target(ref_img, target_inner_size, border_ratio)

    return prep_uploaded, prep_ref


# ----------------- Comparação por histograma -----------------
def compare_histogram(prep_img1, prep_img2):
    hsv1 = cv2.cvtColor(prep_img1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(prep_img2, cv2.COLOR_BGR2HSV)
    hist1 = cv2.calcHist([hsv1], [0, 1], None, [50, 60], [0, 180, 0, 256])
    hist2 = cv2.calcHist([hsv2], [0, 1], None, [50, 60], [0, 180, 0, 256])
    cv2.normalize(hist1, hist1, 0, 1, cv2.NORM_MINMAX)
    cv2.normalize(hist2, hist2, 0, 1, cv2.NORM_MINMAX)
    score = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    return float(score)


# ----------------- Comparação por features (ORB) -----------------
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
    matches = sorted(matches, key=lambda x: x.distance)
    avg_distance = sum([m.distance for m in matches]) / len(matches)
    normalized_score = 1.0 / (1.0 + avg_distance)
    return float(normalized_score)


# ----------------- Converte img to base64 --------------
def image_to_base64(img):
    _, buffer = cv2.imencode(".png", img)
    return base64.b64encode(buffer).decode("utf-8")


# ----------------- Função principal de comparação -----------------
def compare_image(uploaded_img, images_db, threshold=0.5, target_inner_size=(322, 178), border_ratio=0.17, debug=False):
    """
    Compara a imagem enviada com todas do banco usando a nova lógica de redimensionamento.
    """
    best_match = None
    best_score = -1.0

    uploaded_original_base64 = image_to_base64(uploaded_img)
    uploaded_img = normalize_contrast(uploaded_img)

    for img_info in images_db:
        ref_img_path = BASE_DIR / img_info["path"]
        ref_img = cv2.imread(str(ref_img_path))
        if ref_img is None:
            continue

        ref_img = normalize_contrast(ref_img)

        # Redimensionamento condicional baseado na lógica do usuário
        prep_uploaded, prep_ref = resize_based_on_user(
            uploaded_img, ref_img,
            target_inner_size=target_inner_size,
            border_ratio=border_ratio,
        )

        # Comparações
        hist_score = compare_histogram(prep_uploaded, prep_ref)
        feature_score = compare_images_features(prep_uploaded, prep_ref)
        combined_score = (0.7 * hist_score) + (0.3 * feature_score)

        if combined_score > best_score and combined_score > threshold:
            best_score = combined_score
            best_match = img_info.copy()
            try:
                best_match["coords"] = [int(c) for c in best_match["coords"].split(",")]
            except Exception:
                pass
            best_match["score"] = combined_score
            best_match["image_base64"] = uploaded_original_base64

    return best_match
