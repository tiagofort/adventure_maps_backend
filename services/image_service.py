from pathlib import Path
import base64
import json
import cv2
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
DEBUG_DIR = BASE_DIR / "debug_crops"
DEBUG_DIR.mkdir(exist_ok=True)

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


def auto_crop(img, save_debug, debug_name=None):
    """
    Detecta o maior contorno e recorta a área útil.
    Só salva debug se save_debug=True.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)

    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None

    c = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(c)

    H, W = img.shape[:2]
    if w < W * 0.2 or h < H * 0.2:
        return None
    if w > W * 0.95 and h > H * 0.95:
        return None
    
    if save_debug and debug_name:
        DEBUG_DIR.mkdir(exist_ok=True)  # só cria pasta se for salvar
        debug_img = img.copy()
        cv2.drawContours(debug_img, [c], -1, (0, 255, 0), 2)
        cv2.rectangle(debug_img, (x, y), (x+w, y+h), (0, 0, 255), 2)
        cv2.imwrite(str(DEBUG_DIR / f"{debug_name}_contours.png"), debug_img)

    return img[y:y+h, x:x+w]



# ----------------- Normalização de contraste -----------------
def normalize_contrast(img):
    """
    Converte para escala de cinza e aplica equalização adaptativa (CLAHE).
    Retorna imagem BGR equalizada para manter compatibilidade.
    """
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l_eq = clahe.apply(l)

    lab_eq = cv2.merge((l_eq, a, b))
    return cv2.cvtColor(lab_eq, cv2.COLOR_LAB2BGR)


# ----------------- Pré-processamento em par -----------------
def preprocess_pair(img1, img2, ref_name="ref", target_inner_size=(322, 178), border_ratio=0.12):
    """
    Pré-processa duas imagens (uploaded x ref) com auto_crop + fallback para crop proporcional.
    """
    save_debug = False

    # tenta crop automático
    a_crop = auto_crop(img1, save_debug=save_debug, debug_name="uploaded")
    b_crop = auto_crop(img2, save_debug=save_debug, debug_name=ref_name)

    if a_crop is None or b_crop is None:
        # fallback para método baseado em border_ratio
        a_resized, a_crop = crop_and_resize_to_target(img1, target_inner_size, border_ratio)
        b_resized, b_crop = crop_and_resize_to_target(img2, target_inner_size, border_ratio)
    else:
        a_resized = cv2.resize(a_crop, target_inner_size, interpolation=cv2.INTER_AREA)
        b_resized = cv2.resize(b_crop, target_inner_size, interpolation=cv2.INTER_AREA)

    if save_debug:
        cv2.imwrite(str(DEBUG_DIR / f"user_crop.png"), a_resized)
        cv2.imwrite(str(DEBUG_DIR / f"{ref_name}_crop.png"), b_resized)

    return a_resized, b_resized


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
# ----------------- Função principal de comparação -----------------
def compare_image(uploaded_img, images_db, threshold=0.5, target_inner_size=(322, 178), border_ratio=0.17, debug=False):
    """
    Compara a imagem enviada com todas do banco.
    Se debug=True, salva crops em debug_crops/.
    """
    best_match = None
    best_score = -1.0

    # 🔥 guarda a versão original (sem crop, sem normalize)
    uploaded_original_base64 = image_to_base64(uploaded_img)

    # Normaliza contraste da imagem enviada para a comparação
    uploaded_img = normalize_contrast(uploaded_img)

    for idx, img_info in enumerate(images_db):
        ref_img_path = BASE_DIR / img_info["path"]
        ref_img = cv2.imread(str(ref_img_path))
        if ref_img is None:
            continue

        # Normaliza contraste da imagem de referência
        ref_img = normalize_contrast(ref_img)

        # usa 'name' se existir no JSON, senão pega nome do arquivo
        ref_name = img_info.get("name") or Path(img_info["path"]).stem

        prep_uploaded, prep_ref = preprocess_pair(
            uploaded_img, ref_img,
            ref_name=ref_name,
            target_inner_size=target_inner_size,
            border_ratio=border_ratio,
        )

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

            # 🔥 aqui agora vai a imagem original enviada pelo usuário
            best_match["image_base64"] = uploaded_original_base64

    return best_match 
