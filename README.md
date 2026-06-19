# AI Logs Analytics

Automated log incident analysis pipeline built with CrewAI. Parses application logs, extracts structured incidents, and generates a Markdown report.

## Tech Stack

- **Framework:** CrewAI
- **LLM:** Llama 3.1 (8B) via Ollama (`ollama/llama3.1:8b`)
- **Validation:** Pydantic
- **Language:** Python

## Architecture

The application follows a **sequential two-agent pipeline**:

1. **Parse** — `log_analyst` extracts all ERROR/WARN incidents from raw log text into structured JSON using the `parse_incidents` tool.
2. **Report** — `report_writer` analyzes the structured data, summarizes severity distribution, and generates a final Markdown report using the `generate_markdown_report` tool.

## Prerequisites

- Ollama must be running locally on `http://localhost:11434`
- Pull the model before first run: `ollama pull llama3.1:8b`
- Create a log file at `logs/log.txt` with at least 3 lines containing ERROR/WARN/INFO level entries

## Project Structure

| File | Purpose |
|------|---------|
| `main.py` | Entry point; validates input, creates the crew, and kicks off the analysis |
| `agents.py` | Agent definitions (`log_analyst`, `report_writer`) configured with the local LLM |
| `tasks.py` | CrewAI task definitions (`parse_task`, `report_task`) with Pydantic validation |
| `tools.py` | Custom tools: `parse_incidents` (log parser) and `generate_markdown_report` (report builder) |
| `pydantic_schemas.py` | Pydantic models (`Incident`, `ParsedIncidents`) for strict output validation |
| `utils.py` | Helper functions; validates that the input log file exists and is well-formed |
| `logs/` | Input directory; place your log file as `logs/log.txt` |
| `result/` | Output directory; final report is saved as `result/incident_report.md` |

## Agent Roles

### Log Analyst
Extracts structured incidents from raw log text. Calls `parse_incidents` exactly once and returns only the raw JSON result without modification.

### Technical Writer
Receives parsed incidents, summarizes the analysis (counts and severity distribution), writes a brief one-sentence analysis per error, and generates the final Markdown report via `generate_markdown_report`.

## Run

```bash
python main.py
```

After execution completes, the report will be saved at:

```
result/incident_report.md