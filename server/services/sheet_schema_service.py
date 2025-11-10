import pandas as pd
import re
from typing import Dict, List, Optional, Tuple


def detect_header_row(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
	"""Detect the header row of a dataframe."""
	if len(def) == 0:
		print('Empty dataframe')
		return df, []

    # Treat one row dataframes as data. Don't want to turn into headers
	if len(df) == 1:
		df.columns = [f"col_{i+1}" for i in range(len(df.columns))]
		return df, []

	# Store ratios of non-null values to total columns
	total_columns = df.shape[1]
	sample_limit = min(5, len(df))
	non_null_ratios = []
	for row_idx in range(sample_limit):
		row = df.iloc[row_idx]
		non_null_count = row.count()
		non_null_ratios.append(non_null_count / total_columns if total_columns else 0)

	# Get first row where non-null to total ratio is >= 0.5 (happy medium)
	selected_row_idx = 0
	for idx, ratio in enumerate(non_null_ratios):
		if ratio >= 0.5:
			selected_row_idx = idx
			break

	raw_headers = df.iloc[selected_row_idx].tolist()
	clean_headers = []
	seen = {}
	for idx, header in enumerate(raw_headers):
		if header is None or (isinstance(header, float) and pd.isna(header)):
			header_str = ""
		else:
			header_str = str(header).strip()

		# Create column names for empty cells
		if not header_str:
			header_str = f"col_{idx + 1}"

		# Deal with duplicates by naming them name_1, name_2, etc
		base_header = re.sub(r"\s+", " ", header_str)
		candidate = base_header
		counter = 2
		while candidate.lower() in seen:
			candidate = f"{base_header}_{counter}"
			counter += 1
		seen[candidate.lower()] = True
		clean_headers.append(candidate)

	# Get everything below the header and drop the header row
	if selected_row_idx != 0:
		df = df.iloc[selected_row_idx + 1 :].reset_index(drop=True)
	else:
		df = df.iloc[1:].reset_index(drop=True)

	# Assigne column labels to be the headers we just extracted
	df.columns = clean_headers

	return df, raw_headers
    

def infer_column_types(df: pd.DataFrame) -> Dict[str, str]:
    """
    Infer the types of the columns of a dataframe.
	Returns: {
          "column_name": {
              "type": "currency" | "date" | "integer" | "float" | "categorical" | "text",
              "confidence": 0.0-1.0,
              "sample_values": [...],  # first 5 samples
          }
      }
    """
	for col_name, col_data in df.items():
		sample = col_data.dropna().head(200)
		for index, value in sample.items():
			

def extract_units(headers: List[str]) -> Dict[str, Optional[str]]:
    """
    Extract the units from the headers of a dataframe.
    """
    pass

def find_candidate_keys(df: pd.DataFrame) -> List[str]:
    """
    Find the candidate keys of a dataframe.
    """
    pass

