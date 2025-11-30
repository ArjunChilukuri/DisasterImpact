# DisasterImpact
Disaster Impact Synthesis

# Disaster Impact Agent System

A production-grade multi-agent system built with Google ADK for incident ingestion, filtering, geocoding, and synthesis.

## Project Structure

```
disaster_agent_system/
├── __init__.py                 # Package initialization
├── config.py                   # Configuration and settings
├── logger.py                   # Centralized logging utilities
├── memory.py                   # Long-term memory management
├── models.py                   # Data models and schemas
├── tools.py                    # External tools (geocoding, feeds)
├── orchestrator.py             # Pipeline orchestrator
└── agents/
    ├── __init__.py            # Agent exports
    ├── base_agent.py          # Base agent class
    ├── ingestion_agent.py     # Google Search & Feed ingestion
    ├── filtering_agent.py     # Incident filtering & scoring
    ├── geospatial_agent.py    # Location geocoding
    └── synthesis_agent.py     # Report synthesis

main.py                        # Entry point
```

## Architecture

### 1. **Configuration Layer** (`config.py`)
- Centralized settings management
- Environment variable integration
- Model and API configuration

### 2. **Data Models** (`models.py`)
- `IncidentReport` dataclass with typed fields
- Status enums: RAW → VERIFIED → LOCATED → SYNTHESIZED
- Severity levels: CRITICAL, HIGH, MEDIUM, LOW

### 3. **Tools Layer** (`tools.py`)
- `geo_encode()`: Nominatim API geocoding
- `fetch_feed_alerts()`: Sachet NDMA feed integration
- Reusable external integrations

### 4. **Memory System** (`memory.py`)
- `InMemLongTermMemory`: Custom incident store
- Timestamp tracking for incidents
- Historical context retrieval

### 5. **Logger** (`logger.py`)
- Centralized logging with timestamps
- Global logger instance
- Structured log output

### 6. **Agent Architecture** (`agents/`)

#### Base Agent (`base_agent.py`)
```python
class BaseDisasterAgent(LlmAgent):
    """Inherits from Google ADK LlmAgent"""
    - Unified initialization
    - Config integration
    - Common utilities
```

#### Specialized Agents

**IngestionAgentGoogle** - Parallel ingestion via Runner
- Uses Google Search tool
- LLM-based incident extraction
- Returns normalized reports

**IngestionAgentFeed** - Non-LLM feed fetch
- Imperative Sachet NDMA feed parsing
- Normalizes external alerts
- Runs in parallel with Google ingestion

**FilteringAgent** - Runner-based filtering
- Severity assessment
- Reliability scoring
- Location extraction

**GeospatialAgent** - Imperative geocoding
- Non-LLM location processing
- Nominatim API integration
- Coordinate attachment

**SynthesisAgent** - LLM-based synthesis
- Historical context injection
- Markdown report generation
- Final incident summarization

### 7. **Orchestrator** (`orchestrator.py`)
```
Phase 1: Parallel Ingestion
  ├─ IngestionAgentGoogle (Runner)
  └─ IngestionAgentFeed (Imperative)

Phase 2: Filtering (Runner per report)
Phase 3: Geospatial Geocoding (Imperative)
Phase 4: Synthesis (Runner)
Phase 5: Output File
```

## Usage

### Installation
```bash 
export GOOGLE_API_KEY="your-api-key"
```

### Running the System
```bash
python main.py
```

### Output Files
- `final_report_with_memory.md` - Markdown synthesis report
- Console output with full execution logs

## Design Patterns

### 1. **Google ADK Compliance**
- All agents inherit from `LlmAgent`
- Proper tool registration
- Runner integration for LLM calls
- Session and memory service management

### 2. **Separation of Concerns**
- Each agent has single responsibility
- Tools isolated in `tools.py`
- Config centralized in `config.py`
- Logging abstracted in `logger.py`

### 3. **Data Flow**
```
Raw Reports → Verified Reports → Located Reports → Synthesized Reports
      ↓              ↓                  ↓                   ↓
   Ingestion    Filtering         Geospatial          Synthesis
```

### 4. **Error Handling**
- Try/catch blocks at each pipeline stage
- Graceful degradation (defaults if processing fails)
- Detailed error logging

### 5. **Extensibility**
- Add new agents by extending `BaseDisasterAgent`
- Add tools in `tools.py`
- Extend `Config` for new settings
- Custom memory implementations possible

## Key Features

✅ **Runner-Only LLM Calls** - All AI operations via ADK Runner
✅ **Parallel Ingestion** - Simultaneous Google Search and Feed fetch
✅ **Structured Output** - Typed data models throughout pipeline
✅ **Long-term Memory** - Historical incident context
✅ **Comprehensive Logging** - Timestamped execution traces
✅ **Error Resilience** - Graceful failure handling
✅ **Production Ready** - Follows Google ADK best practices

## Configuration

Edit `config.py` to customize:
- Model selection (GEMINI_MODEL)
- API timeouts (REQUEST_TIMEOUT)
- Feed sources (FEED_URL)
- Output files (OUTPUT_FILE)
- Filtering thresholds (MIN_RELIABILITY_SCORE)

## Dependencies

- `google-adk` - Agent development framework
- `google-genai` - Gemini API
- `requests` - HTTP client
- `beautifulsoup4` - HTML parsing

## Google ADK Standards Compliance

✓ LlmAgent inheritance
✓ Proper tool registration
✓ Runner integration
✓ Session management
✓ Memory service usage
✓ Structured agent communication
✓ Error handling patterns
✓ Configuration management

---

**Built with Google ADK** | Multi-Agent Disaster Impact Analysis