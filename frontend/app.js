/**
 * OncoScan AI - Frontend Controller
 * Handles image upload, API calls, and dynamic UI updates.
 */

document.addEventListener('DOMContentLoaded', () => {
    // --- DOM Elements ---
    const elements = {
        uploadSection: document.getElementById('upload-section'),
        fileInput: document.getElementById('file-input'),
        fileNameDisplay: document.getElementById('file-name-display'),

        previewContainer: document.getElementById('preview-container'),
        previewImage: document.getElementById('preview-image'),
        predictBtn: document.getElementById('predict-btn'),
        btnText: document.getElementById('btn-text'),
        btnLoader: document.getElementById('btn-loader'),

        emptyState: document.getElementById('empty-state'),
        resultsLoaderContainer: document.getElementById('results-loader-container'),
        predictionResults: document.getElementById('prediction-results'),
        diagnosisValue: document.getElementById('diagnosis-value'),
        confidenceValue: document.getElementById('confidence-value'),

        gradcamContainer: document.getElementById('gradcam-container'),
        gradcamDetails: document.getElementById('gradcam-details'),
        gradcamImage: document.getElementById('gradcam-image'),
        probBars: document.getElementById('prob-bars')
    };

    let currentFile = null;

    // --- initialization ---

    /**
     * Resets the results panel to its default empty state.
     */
    const resetUI = () => {
        elements.emptyState.classList.remove('hidden');
        elements.resultsLoaderContainer.classList.add('hidden');
        elements.predictionResults.classList.add('hidden');
        elements.gradcamContainer.classList.add('hidden');

        elements.gradcamImage.src = '';
        elements.diagnosisValue.textContent = '-';
        elements.confidenceValue.textContent = '-';
        elements.probBars.innerHTML = '';

        // Collapse the GradCAM dropdown so it starts fresh for each new scan
        if (elements.gradcamDetails) {
            elements.gradcamDetails.removeAttribute('open');
        }
    };

    /**
     * Handles file selection and updates the preview.
     * @param {File} file 
     */
    const handleFileSelect = (file) => {
        if (!file.type.startsWith('image/')) {
            alert('Selection Error: Please provide a valid image file (JPG, PNG, etc).');
            return;
        }

        currentFile = file;
        elements.fileNameDisplay.textContent = file.name;

        // Preview rendering
        const reader = new FileReader();
        reader.onload = (e) => {
            elements.previewImage.src = e.target.result;
            elements.previewContainer.classList.remove('hidden');
        };
        reader.readAsDataURL(file);

        resetUI();
    };

    // --- Events ---

    elements.uploadSection.addEventListener('click', () => elements.fileInput.click());

    elements.fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) handleFileSelect(e.target.files[0]);
    });

    // Drag-and-Drop Handlers
    ['dragover', 'dragleave', 'drop'].forEach(evt => {
        elements.uploadSection.addEventListener(evt, (e) => {
            e.preventDefault();
            if (evt === 'dragover') elements.uploadSection.classList.add('dragover');
            else elements.uploadSection.classList.remove('dragover');

            if (evt === 'drop' && e.dataTransfer.files.length > 0) {
                handleFileSelect(e.dataTransfer.files[0]);
            }
        });
    });

    /**
     * Updates the UI to reflect the loading state during API calls.
     * @param {boolean} isLoading 
     */
    const toggleLoading = (isLoading) => {
        elements.predictBtn.disabled = isLoading;
        if (isLoading) {
            elements.btnText.classList.add('hidden');
            elements.btnLoader.classList.remove('hidden');
            elements.emptyState.classList.add('hidden');
            elements.resultsLoaderContainer.classList.remove('hidden');
            elements.predictionResults.classList.add('hidden');
        } else {
            elements.btnText.classList.remove('hidden');
            elements.btnLoader.classList.add('hidden');
            elements.resultsLoaderContainer.classList.add('hidden');
        }
    };

    /**
     * Renders the probability distribution bar chart.
     * @param {Object} probs - Class-to-probability map.
     * @param {string} predicted - The name of the predicted class.
     */
    const renderProbs = (probs, predicted) => {
        elements.probBars.innerHTML = '';
        Object.entries(probs)
            .sort((a, b) => b[1] - a[1]) // Sort highest probability first
            .forEach(([name, val]) => {
                const pct = (val * 100).toFixed(1);
                const isWinner = name === predicted;

                const row = document.createElement('div');
                row.className = 'prob-row';
                row.innerHTML = `
                    <span class="class-name">${name}</span>
                    <div class="bar-track">
                        <div class="bar-fill ${isWinner ? 'accent' : ''}" style="width: ${pct}%"></div>
                    </div>
                    <span class="pct">${pct}%</span>
                `;
                elements.probBars.appendChild(row);
            });
    };

    // --- Prediction Core ---

    elements.predictBtn.addEventListener('click', async () => {
        if (!currentFile) return;

        toggleLoading(true);

        const formData = new FormData();
        formData.append('file', currentFile);

        try {
            // Parallel fetches for efficiency
            const [predRes, camRes] = await Promise.all([
                fetch('/predict', { method: 'POST', body: formData }),
                fetch('/gradcam', { method: 'POST', body: formData })
            ]);

            if (!predRes.ok || !camRes.ok) throw new Error('API Server responded with an error.');

            const data = await predRes.json();
            const camBlob = await camRes.blob();
            const camUrl = URL.createObjectURL(camBlob);

            // Update UI with Data
            elements.predictionResults.classList.remove('hidden');
            elements.diagnosisValue.textContent = data.prediction;
            elements.confidenceValue.textContent = data.confidence;

            renderProbs(data.all_probs, data.prediction);

            // Show GradCAM
            elements.gradcamContainer.classList.remove('hidden');
            elements.gradcamImage.src = camUrl;

        } catch (err) {
            console.error('Inference Error:', err);
            alert('Analysis Failed: Unable to process scan. Please try again or check server logs.');
            resetUI();
        } finally {
            toggleLoading(false);
        }
    });
});
