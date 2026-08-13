import cv2
import numpy as np
import io
from backend.models.loader import load_model
from backend.utils.predict import predict_image
from backend.utils.preprocess import preprocess_image
from backend.utils.gradcam import get_gradcam_heatmap,overlay_gradcam
from backend.utils.logger import logger

class TumorDetectionService:
    def __init__(self):
        self.model=None

    def _get_model(self):
        if self.model is None:
            logger.info("Loading ML model from HuggingFace Hub ...")
            self.model=load_model()
            logger.info("Model Loaded Sucessfully")
        return self.model

    def _find_last_conv_layer(self,model)->str:
        conv_types=("Conv2D", "TrigConv2D", "DepthwiseConv2D", "SeparableConv2D")
        for layer in reversed(model.layers):
            if layer.__class__.__name__ in conv_types:
                logger.info(f"GradCAM target layer resolved :{layer.name}")
                return layer.name

        fallback="conv2d"
        logger.warning(f"No Convolutional layer found; using fallback {fallback}")
        return fallback
    def process_and_predict(self,file_io):
        try:
            img_array=preprocess_image(file_io)
            model=self._get_model()
            label,confidence,all_probs=predict_image(model,img_array)

            file_io.seek(0)
            file_bytes=np.asarray(bytearray(file_io.read()),dtype=np.uint8)
            orignal_img=cv2.imdecode(file_bytes,cv2.IMREAD_COLOR)

            return label,confidence,all_probs,img_array,orignal_img
        except Exception as e:
            logger.error(f"Service execution failed : {e}")
            raise

    def generate_gradcam_image(self,img_array,orignal_img,layer_name:str=None):
        try:
            model=self._get_model()
            if layer_name is None:
                layer_name=self._find_last_conv_layer(model)
            else:
                layer_names=[l.name for l in self.model.layers]
                if layer_name not in layer_names:
                    logger.warning(
                        f"Layer {layer_name} not found in model."
                        "Auto-detecting convolutional layers instead"
                        )
                    layer_name=self._find_last_conv_layer(self.model)
            heatmap=get_gradcam_heatmap(model,img_array,layer_name)
            return overlay_gradcam(orignal_img,heatmap)

        except Exception as e:
            logger.error(f"GradCAM generation faield: {e}")
            raise

tummor_service=TumorDetectionService()