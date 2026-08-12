import cv2
import numpy as np
from backend.config import IMG_SIZE
from backend.utils.logger import logger


def preprocess_image(uploaded_file) -> np.ndarray:
    try:
        uploaded_file.seek(0)
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)

        if file_bytes.size == 0:
            raise ValueError("Empty file uploaded.")

        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Failed to decode image — unsupported format or corrupt file.")

        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))

        img = img.astype(np.float32) / 255.0

        return np.expand_dims(img, axis=0)  # (1, H, W, C)

    except Exception as e:
        logger.error(f"Preprocessing failed: {e}")
        raise
