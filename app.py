from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil
import os
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
import json
from models.reference_images import reference_images
from services.image_service import compare_image

UPLOAD_DIR = Path(__file__).parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)
BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carregar banco de imagens do JSON
with open(BASE_DIR / "services" / "images_db.json", "r", encoding="utf-8") as f:
    images_db = json.load(f)

# Converter paths para Path absolutos
for img in images_db:
    img["path"] = BASE_DIR / img["path"]

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    uploaded_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    matches = compare_image(uploaded_img, images_db, debug=True)

    return {"matches": matches}