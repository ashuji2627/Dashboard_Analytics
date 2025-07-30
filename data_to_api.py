# main.py
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from Modules.data_visualization import DynamicVisualizer

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Visualization API"}

@app.get("/plot")
def get_plot():
    img_base64 = DynamicVisualizer.generate_plot()
    return JSONResponse(content={"image_base64": img_base64})
