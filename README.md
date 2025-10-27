# XL-Scout 🧮  
**An Agentic Spreadsheet Assistant for Arbitrary Excel Workbooks**

### To Run
Run ```source .venv/bin/activate``` and run ```pip install -r requirements.txt``` first time you open
Backend: ```uvicorn server.app.main:app --reload --port 8000```


### Overview
XL-Scout explores how an AI agent can **inspect, reason about, and safely act on messy spreadsheets** without relying on predefined templates — a problem that is still relatively unsollved to this day

### Goal
To demonstrate a practical “0 → 1” approach to general Excel reasoning:
- Handle diverse, unstructured workbooks.
- Extract, normalize, and understand schema automatically.
- Let an agent plan and execute multi-step workflows (SQL queries, vector search, edits).
- Emphasize safety and transparency through previewable actions and citations.

### Key Features
| Capability | Description |
|-------------|-------------|
| **Upload + Inspect** | Accepts `.xlsx` / `.csv`, parses multiple sheets, infers headers and datatypes. |
| **Normalize + Index** | Cleans headers, infers column types, builds a vector index for semantic lookup. |
| **Plan → Act Loop** | LLM generates a plan, then calls tools (`inspect`, `sql`, `edit`, `preview`, `apply`). |
| **Safe Edits** | No destructive writes — every change is previewed and saved to a new file. |
| **Q&A Across Sheets** | Natural-language queries answered via SQL / vector search. |
| **Latency & Accuracy Logs** | Basic timing and citation reporting for each query. |

### Implementation Priorities
1. **Upload + Inspect**
	- Accept `.xlsx` and `.csv` uploads.
	- Parse multiple sheets, infer header rows, datatypes, and primary keys when possible.
	- Emit a concise schema summary for each sheet.
2. **Normalize + Index**
	- Standardize headers (lowercase, snake_case), strip units into structured metadata.
	- Infer column types (numeric, date, categorical, currency) and assemble a column dictionary with synonym hints from sample values.
	- Build a lightweight semantic index (embedded column descriptors or TF-IDF) to support fuzzy column resolution.
3. **Plan-Then-Act Tooling**
	- Implement tool interfaces: `inspect(sheet|column|sample)`, `sql(table_like_view, query)`, `edit(spec)`, `preview()`, `apply()`.
	- Enforce agent behavior that drafts an explicit plan referencing sheets/columns before invoking tools.
	- Ensure `edit` operations queue safe mutations that must flow through `preview` prior to `apply`, with `apply` writing to a new artifact.
4. **Representative Q&A Flows**
	- Validate natural-language prompts such as totalizing expenses, threshold filters, and computed columns.
	- Confirm responses cite sheets/columns and leverage the semantic index to disambiguate column names.
5. **Safety & Recovery Enhancements**
	- Require confidence thresholds for column resolution and surface clarifying questions when uncertain.
	- Preserve non-destructive workflows by logging every intended change and output file variant.
	- Track simple latency measurements per agent step for future tuning.
6. **Fallback Strategy**
	- When mutation tooling is incomplete, support read-only Q&A paired with a simulated `preview()` that surfaces planned SQL and derived columns, deferring `apply()` until full safety checks ship.

### Schema Inference Heuristics
- **Header detection:** scan the first 5 rows and select the first row with ≥50% non-empty cells as headers; if none qualify, fall back to the top row and synthesize names (`col_1`, `col_2`, ...).
- **Type inference:** sample up to 200 non-null values per column; classify using regex/date parsing: currency via `/^\$?\d/`, dates via `dateutil.parser`, numeric via `float()`, otherwise tag as categorical or free text.
- **Primary-key candidates:** mark any column with unique, non-null values as a key; consider column pairs only if no single column qualifies.
- **Unit extraction:** split headers like `Amount (USD)` with `r"(.*)\(([^)]+)\)"`, preserving both the cleaned base name and the unit metadata.
- **Column dictionary:** store the cleaned snake_case name, raw header, inferred type, captured unit, representative sample values, and tokenized header fragments as synonyms to drive semantic lookup.

### Architecture
- **Frontend:** React (simple chat + schema preview panel)  
- **Backend:** FastAPI (use SSE to stream plan/tool events)
- **Data Layer:** DuckDB over Pandas  
- **Embeddings:** `text-embedding-3-small` for column semantic search  
- **Agent Runtime:** OpenAI GPT-4o mini with a strict system prompt enforcing plan-then-act, Morph for fast, structured diffs for `preview()`
- **Storage:** Pinecone to store column descriptors as vectors for semantic lookup

### Example Workflow
1. Upload a spreadsheet with multiple sheets.  
2. Ask: “Which clients have balances over 50 K?”  
3. Agent inspects schema → drafts a plan → executes SQL → returns results with cell citations.  
4. Ask: “Add a column `net_income = revenue – expenses`.”  
5. Agent previews diff and writes a new file `workbook_XLScout.xlsx`.

### Safety & Failure Modes
- Low-confidence column matches trigger clarifying questions.  
- Arithmetic operations validated for unit compatibility.  
- Actions logged for auditability.

### Why This Matters
Materia focuses on **agentic AI for professional workflows** (tax, audit, accounting).  
XL-Scout demonstrates how similar orchestration and tool-planning ideas can generalize to spreadsheet reasoning — a long-standing open problem in enterprise automation.

### Future Directions
- Broader schema discovery (pivot tables, merged cells).  
- Fine-grained cell-level provenance.  
- Integration with accounting document ingestion pipelines.  
- Latency benchmarking across document sizes.

### Quick Start
```bash
npm install
uvicorn main:app --reload
