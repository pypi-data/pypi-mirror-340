import os

from dotenv import load_dotenv
load_dotenv()

model_dir = os.environ.get("OPENCV_DNN_MODELS_DIR", "models")

print(model_dir)