"""
Agent definitions for the disaster impact system
"""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search
from .config import GEMINI_MODEL
from .tools import feed_fetch_tool , geo_encode
from google.genai import types

retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)

class IngestionAgentGoogle(LlmAgent):
    """Agent for ingesting disaster incidents from Google search"""
    def __init__(self):
        super().__init__(
            name="ingest_google",
            model=Gemini(model=GEMINI_MODEL,retry_options=retry_config),
            instruction="Extract up to 3 incident summaries from Google search. Return JSON with rawText, source.",
            tools=[google_search]
        )

class IngestionAgentFeed(LlmAgent):
    """Agent for fetching alerts from disaster feeds"""
    def __init__(self):
        super().__init__(
            name="ingest_feed",
            model=Gemini(model=GEMINI_MODEL, retry_options=retry_config),
            instruction="Fetch alerts from Sachet NDMA feed and return JSON with text, source.",
            tools=[feed_fetch_tool]
        )

class FilteringAgent(LlmAgent):
    """Agent for filtering and scoring incident reports"""
    def __init__(self):
        super().__init__(
            name="filtering_agent",
            model=Gemini(model=GEMINI_MODEL, retry_options=retry_config),
            instruction="Analyze incidents and return JSON with severity, reliabilityScore, extractedLocation, isActionable.",
            tools=[google_search]
        )

class GeospatialAgent(LlmAgent):
    """Agent for geocoding incident locations"""
    def __init__(self):
        super().__init__(
            name="geospatial_agent",
            model=Gemini(model=GEMINI_MODEL, retry_options=retry_config),
            instruction="Geocode incident locations using geo_encode tool.",
            tools=[geo_encode]
        )

class SynthesisAgent(LlmAgent):
    """Agent for synthesizing reports into actionable insights"""
    def __init__(self):
        super().__init__(
            name="synthesis_agent",
            model=Gemini(model=GEMINI_MODEL, retry_options=retry_config),
            instruction="Synthesize LOCATED reports into Markdown including historical context.",
            tools=[]
        )
