"""
Orchestrator for the disaster impact agent pipeline
"""

import uuid
from google.adk.agents import SequentialAgent, ParallelAgent
from google.adk.runners import InMemoryRunner
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from .logger import log_message
from .memory import InMemLongTermMemory
from .agents import (
    IngestionAgentGoogle,
    IngestionAgentFeed,
    FilteringAgent,
    GeospatialAgent,
    SynthesisAgent
)

class Orchestrator:
    """Main orchestrator for the disaster impact agent system"""
    
    def __init__(self):
        log_message('Initializing Orchestrator')
        self.session_service = InMemorySessionService()
        self.memory_service = InMemoryMemoryService()
        self.long_term_memory = InMemLongTermMemory()

        # Agents
        self.ingest_google = IngestionAgentGoogle()
        self.ingest_feed = IngestionAgentFeed()
        self.filtering = FilteringAgent()
        self.geospatial = GeospatialAgent()
        self.synthesis = SynthesisAgent()

        # Pipeline: Parallel ingestion + Sequential processing
        self.parallel_ingest = ParallelAgent(
            name='parallel_ingest',
            sub_agents=[self.ingest_google, self.ingest_feed]
        )
        self.pipeline = SequentialAgent(
            name='main_seq',
            sub_agents=[
                self.parallel_ingest,
                self.filtering,
                self.geospatial,
                self.synthesis
            ]
        )

        # Main InMemoryRunner
        self.runner = InMemoryRunner(agent=self.pipeline)

    async def start_engine(self):
        """Start the disaster impact agent pipeline"""
        session_id = str(uuid.uuid4())
        log_message(f'--- START ENGINE (session={session_id}) ---')

        # Run pipeline via InMemoryRunner
        synthesis_output = await self.runner.run_debug(
            "Process disaster alerts and produce synthesis report"
        )
        log_message('Pipeline execution completed')

        return synthesis_output
