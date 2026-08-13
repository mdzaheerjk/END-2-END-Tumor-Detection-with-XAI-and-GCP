import tensorflow as tf
import numpy as np

class TrigConv2D(tf.keras.Layer):

    def __init__(self,filters:int,kernel_size:int,frequency:float=1.0,**kwargs):
        super().__init__(**kwargs)
        self.filters=filters
        self.kernel_size=kernel_size
        self.frequency=frequency


    def build(self,input_shape):
        super().build(input_shape)
        kernels=[]
        x=np.linspace(-1,1,self.kernel_size)
        y=np.linspace(-1,1,self.kernel_size)
        x_grid,y_grid=np.meshgrid(x,y)

        for i in range(self.filters):
            if i%2==0:
                kernel=np.sin(self.frequency*(x_grid+y_grid))
            else:
                kernel=np.cos(self.frequency*(x_grid+y_grid))
            kernel=kernel[:,:,np.newaxis,np.newaxis]
            kernel=np.repeat(kernel,input_shape[-1],axis=2)

        self.kernel=tf.constant(
            np.concatenate(kernels,axis=3),dtype=tf.float32
        )
    def call(self,inputs):
        return tf.nn.conv2d(inputs,self.kernel,strides=[1,1,1,1],padding='SAME')

    def get_config(self):
        config=super().get_config()
        config.update({
            "filters":self.filters,
            "kernel_size":self.kernel_size,
            "frequency":self.frequency
        })
        return config

    def load_model()->tf.keras.Model:
        from backend.config import HF_REPO_ID,MODEL_FILENAME
        from huggingface_hub import hf_hub_download

        model_path=hf_hub_download(repo_id=HF_REPO_ID,filename=MODEL_FILENAME)

        return tf.keras.models(
            model_path,
            custom_objects={"TrigConv2D":TrigConv2D},
            compile=False
        )