from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from data_parser import parse_file
from storage import df_store
import pandas as pd

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    try:
        df = parse_file(content, file.filename)
        df_store['data'] = df  # Store for later access
        return {"status": "success", "columns": list(df.columns), "rows": len(df)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/data/")
def get_data():
    df: pd.DataFrame = df_store.get("data")
    if df is None:
        return {"status": "error", "message": "No data uploaded"}
    return df.to_dict(orient="records")
