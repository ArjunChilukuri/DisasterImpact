"""
Main entry point for the Disaster Impact Agent System
"""

import asyncio
from disaster_agent_system.orchestrator import Orchestrator
from disaster_agent_system.logger import log_message

async def main():
    """Main execution function"""
    log_message('=== DISASTER IMPACT AGENT SYSTEM ===')
    
    orch = Orchestrator()
    synthesis_result = await orch.start_engine()
    
    log_message('='*60)
    log_message('SYNTHESIS OUTPUT')
    log_message('='*60)
    print(synthesis_result)

if __name__ == "__main__":
    asyncio.run(main())
