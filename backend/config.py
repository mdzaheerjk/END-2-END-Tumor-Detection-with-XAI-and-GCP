import os

BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HF_REPO_ID='Diveshj/brain-breast'
MODEL_FILENAME='trig_model.keras'

IMG_SIZE=128

LOGS_DIR=os.path.join(BASE_DIR,'backend','logs')
MODEL_DIR=os.path.join(BASE_DIR,'backend','models')
FRONTEND_DIR=os.path.join(BASE_DIR,'frontend')
