from pathlib import Path
from typing import Dict, List
import pandas as pd
from fastapi import FastAPI, File, HTTPException, UploadFile

app = FastAPI()

@app.get("/")
def read_root():
	"""Return a simple health-check payload for the API root."""
	return {"message": "Hello, World!"}

@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
	"""Accept CSV/XLSX uploads, parse sheets, and return sample previews."""
	if not file.filename:
		raise HTTPException(status_code=400, detail="Filename is required.")

	suffix = Path(file.filename).suffix.lower()

	if suffix == ".csv":
		dataframe = pd.read_csv(file.file)
		preview_payload: Dict[str, List[Dict[str, object]]] = {
			file.filename: dataframe.head().to_dict(orient="records")
		}
	elif suffix in {".xlsx", ".xls"}:
		workbook = pd.read_excel(file.file, sheet_name=None)
		preview_payload = {
			sheet_name: sheet_df.head().to_dict(orient="records")
			for sheet_name, sheet_df in workbook.items()
		}
	else:
		raise HTTPException(status_code=415, detail="Unsupported file type.")

	return {"message": "File uploaded successfully", "sheets": preview_payload}