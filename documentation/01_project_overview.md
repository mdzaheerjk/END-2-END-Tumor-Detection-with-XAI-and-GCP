# Project Overview: Serialized Backend Documentation

This document serves as a map of the backend codebase, explaining the role of every key Python file and how they flow together.

---

## The Code Map

The project is structured beautifully, separating the web server logic from the deep mathematical AI logic. 

### 1. The Gateway
*   **`backend/main.py`**
    *   **The Entry Point:** This is where the server officially turns on. It holds the FastAPI logic.
    *   **Role:** It listens for network traffic on the `/predict` and `/gradcam` endpoints. It handles the raw incoming image uploads and handles sending the final JSON or Image responses back to the user's browser. It delegates all the actual hard work to the service layer.

### 2. The Manager
*   **`backend/utils/service.py`**
    *   **The Orchestrator:** This file contains the `TumorDetectionService`.
    *   **Role:** It sits squarely between the API (FastAPI) and the various AI helpers. When the API gets a file, it gives it to this service. The service then sequentially commands the preprocessor, asks if the model needs loading, grabs the prediction from the predictor, and ultimately bundles it all up cleanly.

### 3. The AI Utilities
These files do very specific, isolated tasks requested by the service manager.

*   **`backend/utils/preprocess.py`**
    *   **The Formatter:** Takes the raw bytes of the user's image and converts it into a `float32` numpy tensor. It resizes it, scales colors to decimals between `0.0` and `1.0`, and expands it into a "batch" so the AI accepts it without throwing errors.
*   **`backend/models/loader.py`**
    *   **The Brain Loader:** Uses cloud libraries to safely download our custom `.h5` or `.keras` AI file from HuggingFace. It also holds the strict definition of our custom `TrigCon2d` neural network layer, which is required to successfully stitch the model's brain together once downloaded.
*   **`backend/utils/predict.py`**
    *   **The Guesser:** A very simple file. It merely takes the fully loaded AI model and the perfectly preprocessed image, runs them together, and outputs an index. It matches that index to the human-readable labels: `["No Tumor", "Tumor", "Benign", "Malignant", "Normal"]`.
*   **`backend/utils/gradcam.py`**
    *   **The Explainer:** This code physically cracks open the active, loaded model, finds its last major convolutional layer, runs the image through it while mathematically tracking the "gradients," and spits out a colored visual heatmap mask layered flawlessly over the original user image.

---

## Accompanying Documentation Reference

To dive deeper into the specific complex components of the project, please refer to the following guide files located in the `documentation/` folder:

1.  **[Prediction Pipeline Explanation](03_prediction_pipeline_explanation.md)** - A step-by-step logic map of how data moves from user upload to prediction result.
2.  **[TrigCon2d Explanation](04_trigcon2d_explanation.md)** - Explains how and why the AI uses hardcoded Sine/Cosine mathematical waves.
3.  **[GradCAM Explanation](05_gradcam_explanation.md)** - Explains how the AI heatmap visuals are actually generated.
4.  **[Terminology Guide](02_terminology_guide.md)** - A dictionary of technical jargon (API, Tensor, Middleware) used throughout this system.
5.  **[Dockerfile Explanation](06_dockerfile_explanation.md)** - A recipe guide to how the application is packaged into an isolated container.
6.  **[Kubernetes Deployment Explanation](07_kubernetes_explanation.md)** - Explains how the cloud environment manages and scales the Docker containers.
