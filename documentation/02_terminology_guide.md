# Terminology Guide 

This document explains the common technical jargon and specific names used throughout this project's backend codebase in simple terms.

---

## FastAPI Terms

This project uses **FastAPI**, a modern, fast web framework for building APIs with Python. It's the "middleman" that connects the user's web page with our AI brain.

*   **API (Application Programming Interface):** Think of it like a waiter in a restaurant. The user (customer) asks the waiter (API) for something (like an image prediction), the waiter goes to the kitchen (our Python logic/AI), gets the result, and brings it back.
*   **Endpoint / Route:** A specific URL/address the waiter listens to. For example, our API has `/predict` (for diagnosing images) and `/gradcam` (for creating heatmaps). 
*   **Middleware (CORS):** "Cross-Origin Resource Sharing". By default, web browsers block websites on one server from talking to an API on another for security reasons. CORS is a rule we add to tell the browser: *"It's okay, you're allowed to talk to us!"*
*   **UploadFile / `io.BytesIO`:** When a user uploads a file, it comes in as raw binary data. `UploadFile` catches it, and `BytesIO` holds it dynamically in the computer's temporary memory (RAM) instead of physically writing it to the hard drive. This makes the server run much faster.
*   **Response / JSON:** The final answer sent back to the user. Usually, it's sent as JSON, which is just a text format that categorizes the data cleanly (e.g., `{"prediction": "Normal", "confidence": "99%"}`).

---

## Artificial Intelligence & Project Terms

*   **Model / "The Brain":** The large mathematical formula that was trained to detect tumors. In this project, it's built using a library called TensorFlow/Keras.
*   **HuggingFace Hub:** A massive cloud repository (like GitHub but for AI models). Our app's `load_model()` function securely downloads our pre-trained model from here.
*   **Lazy Loading:** By default, AI models take a huge amount of computer memory. Instead of loading the model the second the server turns on (which can be slow and crash things), we "lazy load" the model—meaning we only download and open it the very first time a user actually clicks "Predict". 
*   **Inference / `predict_image`:** The active process of the AI looking at a *new* image it has never seen before and making a guess about it.
*   **Pre-processing / `preprocess_image`:** The AI is very picky. It can't just look at a JPG file. Preprocessing takes the image and forces it into a strict mathematical grid: it resizes it perfectly, normalizes the color values (instead of 0-255, it uses tiny decimals between 0.0 and 1.0), and packages it into a "Tensor" before giving it to the AI.
*   **GradCAM (Gradient-weighted Class Activation Mapping):** A diagnostic tool. It acts like an X-ray for the AI itself, creating a glowing red and blue "heatmap" that highlights exactly which pixels on the image caused the AI to make its final diagnosis.
*   **TrigCon2d (Trigonometric Convolutional 2D Layer):** A highly specialized, custom piece of our model's brain. Instead of trying to randomly learn what tumor textures look like, this layer uses perfectly fixed Sine and Cosine mathematical waves as "magnifying glasses" to aggressively force the AI to look at specific structural patterns in human tissue right away.
*   **Service Layer (`TumorDetectionService`):** Rather than putting all the messy logic in the FastAPI file, we use a "service". It acts as a dedicated manager that takes the raw user file, calls the preprocessor, wakes up the AI, gets the prediction, generates the heatmap, and neatly hands the results back to the API.
