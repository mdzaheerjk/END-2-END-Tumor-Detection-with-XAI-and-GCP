import os

import numpy as np
import tensorflow as tf


class TrigConv2D(tf.keras.Layer):

    def __init__(self, filters: int, kernel_size: int, frequency: float = 1.0, **kwargs):
        super().__init__(**kwargs)
        self.filters = filters
        self.kernel_size = kernel_size
        self.frequency = frequency

    def build(self, input_shape):
        super().build(input_shape)
        kernels = []
        x = np.linspace(-1, 1, self.kernel_size, dtype=np.float32)
        y = np.linspace(-1, 1, self.kernel_size, dtype=np.float32)
        x_grid, y_grid = np.meshgrid(x, y)

        for i in range(self.filters):
            if i % 2 == 0:
                kernel = np.sin(self.frequency * (x_grid + y_grid))
            else:
                kernel = np.cos(self.frequency * (x_grid + y_grid))
            kernel = kernel[:, :, np.newaxis, np.newaxis]
            kernel = np.repeat(kernel, input_shape[-1], axis=2)
            kernels.append(kernel)

        self.kernel = tf.constant(np.concatenate(kernels, axis=3), dtype=tf.float32)

    def call(self, inputs):
        return tf.nn.conv2d(inputs, self.kernel, strides=[1, 1, 1, 1], padding='SAME')

    def get_config(self):
        config = super().get_config()
        config.update({
            "filters": self.filters,
            "kernel_size": self.kernel_size,
            "frequency": self.frequency,
        })
        return config


def load_model() -> tf.keras.Model:
    from backend.config import HF_REPO_ID, MODEL_FILENAME, MODEL_DIR

    if HF_REPO_ID and MODEL_FILENAME:
        from huggingface_hub import hf_hub_download

        model_path = hf_hub_download(repo_id=HF_REPO_ID, filename=MODEL_FILENAME)
        return tf.keras.models.load_model(
            model_path,
            custom_objects={"TrigConv2D": TrigConv2D},
            compile=False,
        )

    candidate_names = ["trig_model.keras", "baseline_cnn.keras", "resnet_model.keras", "trig_model.h5", "baseline_cnn.h5", "resnet_model.h5"]
    for model_name in candidate_names:
        model_path = os.path.join(MODEL_DIR, model_name)
        if os.path.exists(model_path):
            return tf.keras.models.load_model(
                model_path,
                custom_objects={"TrigConv2D": TrigConv2D},
                compile=False,
            )

    raise FileNotFoundError("No trained model found. Set HF_REPO_ID and MODEL_FILENAME or add a local model under the models directory.")