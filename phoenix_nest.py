"""
OPERATION PHOENIX NEST - Main Orchestration Script
Autonomous reconnaissance system for Base L2 memecoins.
"""

import asyncio
import logging
import sys
from datetime import datetime

# Import components
from sensor_layer import BaseContractWatcher
from analysis_core import ContractAnalyzer
from scoring_engine import HeuristicScoringEngine
from probe_execution import ProbeExecutionLayer
from synthesis_engine import SynthesisEngine

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('phoenix_nest.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class PhoenixNest:
    def __init__(self):
        self.sensor = BaseContractWatcher()
        self.analyzer = ContractAnalyzer()
        self.scorer = HeuristicScoringEngine()
        self.probe = ProbeExecutionLayer()
        self.synthesis = SynthesisEngine()
        
        logger.info("PhoenixNest initialized with all components.")
    
    async def run(self):
        """Main loop of the system."""
        logger.info("Starting PhoenixNest main loop.")
        
        try:
            # Step 1: Watch for new contracts and transactions
            contracts = await self.sensor.watch_contracts()
            
            # Step 2: Analyze each contract
            for contract_address in contracts:
                # Static and dynamic analysis
                analysis_result = self.analyzer.analyze(contract_address)
                
                # Step 3: Score the contract
                score = self.scorer.score_contract(contract_address, analysis_result)
                
                # Step 4: If score meets threshold, execute dust transaction
                if self.scorer.is_above_threshold(score):
                    logger.info(f"Contract {contract_address} scored above threshold. Executing probe.")
                    self.probe.execute_dust_transaction(contract_address)
                
                # Step 5: Update synthesis engine with the data
                self.synthesis.update(contract_address, analysis_result, score)
            
            # Step 6: Periodic synthesis and learning
            await self.synthesis.learn_and_adapt()
            
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            # Optionally, send an alert via Telegram
            self.send_telegram_alert(f"PhoenixNest error: {e}")
    
    def send_telegram_alert(self, message):
        """Send an alert via Telegram."""
        # This function requires TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if token and chat_id:
            import requests
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            data = {
                "chat_id": chat_id,
                "text": message
            }
            try:
                requests.post(url, data=data)
            except Exception as e:
                logger.error(f"Failed to send Telegram alert: {e}")
        else:
            logger.warning("Telegram bot token or chat ID not set. Cannot send alert.")

async def main():
    """Entry point."""
    nest = PhoenixNest()
    await nest.run()

if __name__ == "__main__":
    asyncio.run(main())