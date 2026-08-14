import os
import sys
import warnings

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('TF_CPP_LOG_LEVEL',"3")
os.environ.setdefault("TF_ENABLE_ONEDNN_OPTS","0")

warnings.filterwarnings('ignore',category=DeprecationWarning)
warnings.filterwarnings('ignore',category=UserWarning)
warnings.filterwarnings('ignore',category=FutureWarning)

import cv2
import io
from fastapi import File,FastAPI,UploadFile,HTTPException
from fastapi.responses import Response,FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.config import FRONTEND_DIR
from backend.utils.service import tummor_service
from backend.utils.logger import logger

app=FastAPI(
    title='Tumor Detection AI API',
    description='Refreacted & Modular AI API',
    version='2.0.0'
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=['*']
)

app.mount("/static",StaticFiles(directory=FRONTEND_DIR),name='static')

@app.get('/')
async def root():
    return FileResponse(os.path.join(FRONTEND_DIR,'index.html'))

@app.post('/predict')
async def predict(file:UploadFile=File(...)):
    try:
        logger.info(f"Incomming Prediction request : {file.filename}")
        contents=await file.read()
        file_io=io.BytesIO(contents)

        label,confidence,all_probs,_,_=tummor_service.process_and_predict(file_io)

        return {
            'filename':file.filename,
            'prediction':label,
            'confidence':f"{confidence:.2%}",
            "all_probs":all_probs
        }
    except Exception as e:
        logger.error(f"Prediction failed for {file.filename}:{e}")
        raise HTTPException(status_code=500,detail='Internal processing error')

@app.post("/gradcam")
async def gradcam(file:UploadFile=File(...)):
    try:
        logger.info(f"Incomming GradCAM request : {file.filename}")
        contents=await file.read()
        file_io=io.BytesIO(contents)


        _,_,_,img_array,orignal_img=tummor_service.process_and_predict(file_io)

        if orignal_img is None:
            raise ValueError("Inavlid image file.")

        cam_image=tummor_service.generate_gradcam_image(img_array,orignal_img)

        _,buffer =cv2.imencode(".png",cam_image)
        return Response(content=buffer.tobytes(),media_type='image/png')
    except Exception as e:
        logger.error(f"GradCAM Failed for {file.filename}:{e}")
        raise HTTPException(status_code=500,detail=str(e))
if __name__=='__main__':
    import uvicorn
    logger.info("Starting API Server ....")
    uvicorn.run(app,host='0.0.0.0',port=8000)