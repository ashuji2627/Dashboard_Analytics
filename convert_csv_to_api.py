# main.py

from fastapi import FastAPI
import pandas as pd
from fastapi.responses import JSONResponse
#now I gonna setup MERN in vscode, what are the library and app needs to install in for MERN part
app = FastAPI()
#Any type of file should be upload and convert  it to fetch the data
@app.get("/shop_trends")
def get_data():

    try:
        df = pd.read_csv("shop_trends.csv")
        data = df.to_dict(orient="records")
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
#firstly i am using React for the frontend part, what are the things need to install for react framework use