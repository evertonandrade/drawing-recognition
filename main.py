from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from io import BytesIO
import uvicorn
import numpy as np
from PIL import Image, ImageOps

from models.cnn import CNN

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})


@app.post("/predict")
async def predict(request: Request):
    form_data = await request.form()
    img_file = form_data["image_draw"]
    bytes = await img_file.read()
    image = Image.open(BytesIO(bytes))
    image_gray = ImageOps.grayscale(image)
    im_np = np.asarray(image_gray)
    cnn = CNN(
        "model_cnn.h5",
        labels=[
            "bee",
            "airplane",
            "guitar",
            "crab",
            "truck",
            "banana",
            "coffee cup",
            "rabbit",
            "hamburger",
            "umbrella",
        ],
    )
    result = cnn.predict(im_np)
    return {"data": result}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
