import os
import sys
import pandas as pd

# Make sure Python can find classify.py no matter where uvicorn is run from
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse

from classify import classify  # No relative import — now it will always work

app = FastAPI()

@app.post("/classify/")
async def classify_logs(file: UploadFile):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV.")
    
    try:
        # Read uploaded CSV
        df = pd.read_csv(file.file)
        if "source" not in df.columns or "log_message" not in df.columns:
            raise HTTPException(status_code=400, detail="CSV must contain 'source' and 'log_message' columns.")

        # Perform classification
        df["target_label"] = classify(list(zip(df["source"], df["log_message"])))

        # Save result
        output_file = os.path.join(current_dir, "output.csv")
        df.to_csv(output_file, index=False)
        return FileResponse(output_file, media_type="text/csv")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        file.file.close()
