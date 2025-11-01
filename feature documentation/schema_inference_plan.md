# Schema Inference Implementation Plan

## Goal
Outline the steps to transform uploaded CSV/XLSX sheets into structured metadata powering XL-Scout's agent.

## Tasks
- **Module Setup**
  - Create `server/app/services/sheet_schema_service.py` for reusable heuristics
  - Define data contracts (Pydantic models) in `server/app/models/schema_summary.py`

- **Header Detection**
  - Scan first 5 rows; pick first row with ≥50% non-null as header
  - If none found, default to row 0 and synthesize `col_n` names
  - Return cleaned DataFrame and header metadata

- **Type Inference**
  - Sample up to 200 non-null values per column
  - Classify using regex/date parsing into `integer`, `float`, `currency`, `date`, `categorical`, `text`
  - Capture raw evidence (regex match, parse success rates)

- **Primary Key Candidates**
  - Mark columns with unique & non-null values
  - If no single column qualifies, evaluate column pairs for uniqueness (limit combinations to avoid explosion)

- **Unit Extraction**
  - Regex headers with `r"(.*)\(([^)]+)\)"`
  - Store base name + unit string for later validation

- **Column Dictionary Assembly**
  - Produce per-column metadata: raw header, cleaned snake_case name, inferred type, unit, sample values, synonym tokens
  - Synonyms include lowercased header tokens, unit label, camelCase splits

- **Sheet Summary Builder**
  - Compile summary containing:
    - `sheet_name`
    - `row_count`, `column_count`
    - `candidate_keys`
    - `columns` array (with type/unit/samples/synonyms)
    - `sample_rows` (`head()` records)

- **Integration into `/upload` Endpoint**
  - Generate a `workbook_id` (UUID)
  - Store parsed DataFrames + summaries in in-memory registry keyed by `workbook_id`
  - Return response: `{ message, workbook_id, sheets: [...] }`

## Deliverables
- Schema service module with unit-testable functions
- Updated FastAPI endpoint using the service
- Documentation outlining heuristics and limitations
