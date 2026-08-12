import numpy as np
from backend.utils.logger import logger

CLASSES = ["No Tumor", "Tumor", "Benign", "Malignant", "Normal"]

def predict_image(model, img: np.ndarray) -> tuple:
    try:
        preds = model.predict(img, verbose=0)
        idx   = int(np.argmax(preds))

        label      = CLASSES[idx]
        confidence = float(np.max(preds))
        all_probs  = {cls: float(preds[0][i]) for i, cls in enumerate(CLASSES)}

        logger.info(f"Prediction: {label} ({confidence:.2%})")
        return label, confidence, all_probs

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise
