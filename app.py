import os
import cv2
import numpy as np
from io import BytesIO
from dotenv import load_dotenv

import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from starlette.responses import StreamingResponse

from car_detection_system import CarDetectionSystem

load_dotenv()

app = FastAPI()
car_detect = CarDetectionSystem(str(os.getenv("MODEL_PATH")), str(os.getenv("DEVICE")))

@app.post("/api/parking_spaces")
async def update_parking_spaces(image: UploadFile = File(...)):
    try:
        img = cv2.imdecode(np.frombuffer(image.file.read(), np.uint8), cv2.IMREAD_COLOR)
        car_detect.update_parking_spaces(img)
        response = car_detect.park.__dict__()
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/api/parking_spaces_image")
async def update_parking_spaces(image: UploadFile = File(...)):
    try:
        img = cv2.imdecode(np.frombuffer(image.file.read(), np.uint8), cv2.IMREAD_COLOR)
        car_detect.update_parking_spaces(img)
        processed_img = car_detect.display(img)
        _, img_encoded = cv2.imencode('.png', processed_img)
        img_bytes = img_encoded.tobytes()

        return StreamingResponse(BytesIO(img_bytes), media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/api/test_image")
async def update_parking_spaces(image: UploadFile = File(...)):
    try:
        # img = cv2.imdecode(np.frombuffer(image.file.read(), np.uint8), cv2.IMREAD_COLOR)
        # car_detect.update_parking_spaces(img)
        # processed_img = car_detect.display(img)
        # _, img_encoded = cv2.imencode('.png', processed_img)
        # img_bytes = img_encoded.tobytes()

        return StreamingResponse(BytesIO(image.file.read()), media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':

    uvicorn.run(app, host=os.getenv("HOST"), port=int(os.getenv("PORT")))