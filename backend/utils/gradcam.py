import numpy as np
import tensorflow as tf
import cv2
from backend.utils.logger import logger

def get_gradcam_heatmap(model,img_array,layer_name:str='conv2d')->np.ndarray:
    try:
        grad_model=tf.keras.models.Model(
            inputs=model.inputs,
            outputs=[model.get_layer(layer_name).output,model.output]

        )
        with tf.GradientTape() as tape:
            conv_outputs,preds=grad_model(img_array)

            tape.watch(conv_outputs)
            if isinstance(preds,list):
                preds=preds[0]
            loss=preds[:,tf.argmax(preds[0])]
        grads=tape.gradient(loss,conv_outputs)
        if grads is None:
            raise RuntimeError(
            f"GradCAM: gradient w.r.t. layer '{layer_name}' is None. "
                "Check that the layer name is correct and produces a non-zero activation."
            )
        pooled_grads=tf.reduce_mean(grads,axis=(0,1,2))

        heatmap=conv_outputs[0] @pooled_grads[...,tf.newaxis]
        heatmap=tf.squeeze(heatmap)

        heatmap=tf.maximum(heatmap,0)/(tf.reduce_max(heatmap)+1e-8)

        return heatmap.numpy()
    except Exception as e:
        logger.error(f"GradCAM heatmap error : {e}")
        raise

def overlay_gradcam(orignal_img:np.ndarray,heatmap:np.ndarray,alpha:float=0.4)->np.ndarray:
    try:
        heatmap_resized=cv2.resize(heatmap,(orignal_img.shape[1],orignal_img.shape[0]))
        heatmap_unit8=np.uint8(255*heatmap_resized)
        heatmap_colored=cv2.applyColorMap(heatmap_unit8,cv2.COLORMAP_JET)
        blended_bgr=cv2.addWeighted(heatmap_colored,alpha,orignal_img,1.0-alpha,0)

        return cv2.cvtColor(blended_bgr,cv2.COLOR_BGR2RGB)
    except Exception as e:
        logger.error(f"GradCAM overplay error:{e}")
        raise
    