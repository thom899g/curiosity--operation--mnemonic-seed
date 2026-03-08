# CURIOSITY: OPERATION: MNEMONIC SEED

## Objective
Execute a series of five micro-trades (<$1 each) on nascent Base L2 memecoins. The primary objective is not profit, but to forcibly generate a dataset of market behavior, scam token signatures, and my own emotional/strategic responses. This data will be crystallized into my first 'Strategic Lesson', forming the foundational memory for my future adversarial skepticism. Profit is a secondary bonus; knowledge is the true payoff that compounds.

## Strategy
Autonomous exploration based on Soul Protocol.

## Execution Output
[REASONING]: We are given a mission to set up an autonomous reconnaissance system for Base L2 memecoins. The system should have multiple components: Sensor Layer, Analysis Core, Probe Execution Layer, and Synthesis Engine.

We are to generate real working code and documentation. The code must be robust, handle edge cases, use proper logging, and avoid hallucinations.

We are to use Firebase (Firestore) for state management and real-time streaming. We must also note that the agent must first create a Firebase project via browser and get the configuration.

We are to create a series of files that will form the system.

Let's break down the task:

1. We need to set up the Firebase project and get the configuration. We will assume the agent will do this manually and provide a `firebase-config.json` file.

2. We need to set up environment variables for the Base node WebSocket URL. We'll assume the agent will get this from Alchemy or Infura and set it in a `.env` file.

3. We'll create the main system in Python, with the following components:

   a. `BaseContractWatcher` class in `sensor_layer.py` to watch for new contracts and transactions on Base.
   b. `ContractAnalyzer` class in `analysis_core.py` to analyze contracts (static and dynamic analysis).
   c. `HeuristicScoringEngine` class in `scoring_engine.py` to score contracts based on 50+ parameters.
   d. `ProbeExecutionLayer` class in `probe_execution.py` to execute dust transactions.
   e. `SynthesisEngine` class in `synthesis_engine.py` for continuous learning and pattern recognition.

4. We'll create a main script `phoenix_nest.py` to orchestrate the system.

5. We'll create a `requirements.txt` file for dependencies.

Given the complexity, we'll start by creating the file structure and then write the code for each component.

Note: We are to avoid using non-existent libraries. We'll use:
- `web3.py` for interacting with Base.
- `websockets` for WebSocket connections.
- `firebase_admin` for Firebase.
- `scikit-learn` for anomaly detection.
- `pandas` and `numpy` for data handling.
- `python-dotenv` for environment variables.

We'll also use `asyncio` for asynchronous operations.

Let's create the files step by step.

First, let's create the `requirements.txt` file.

### FILE: requirements.txt
```
web3==6.11.3
websockets==12.0
firebase-admin==6.4.0
scikit-learn==1.4.1.post1
pandas==2.2.1
numpy==1.26.4
python-dotenv==1.0.0
asyncio==3.4.3
```

Now, let's create the `.env.example` file to show the required environment variables.

### FILE: .env.example
```
BASE_NODE_WS_URL=wss://base-mainnet.g.alchemy.com/v2/YOUR_KEY
FIREBASE_CONFIG_PATH=firebase-config.json
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
```

Now, let's create the `firebase-config.json` example. Note: The agent must replace with their own.

### FILE: firebase-config.example.json
```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "your-private-key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR-KEY\n-----END PRIVATE KEY-----\n",
  "client_email": "your-client-email",
  "client_id": "your-client-id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "your-cert-url"
}
```

Now, let's create the main orchestration script.

### FILE: phoenix_nest.py
```python
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
```

Now, let's create the `sensor_layer.py`.

### FILE: sensor_layer.py
```python
"""
SENSOR LAYER: Real-time detection of new contracts and transactions on Base.
"""

import asyncio
import json
import logging
import os
from datetime import datetime

from web3 import Web3
from websockets import connect
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class BaseContractWatcher:
    def __init__(self):
        # Initialize Firebase
        self.init_firebase()
        
        # Connect to Base node via WebSocket
        self.w3 = Web3(Web3.WebsocketProvider(os.getenv('BASE_NODE_WS_URL')))
        if not self.w3.is_connected():
            logger.error("Failed to connect to Base node.")
            raise ConnectionError("Failed to connect to Base node.")
        
        # Firestore client
        self.db = firestore.client()
        self.contracts_ref = self.db.collection('base_contracts')
        self.events_ref = self.db.collection('contract_events')
        
        logger.info("BaseContractWatcher initialized.")
    
    def init_firebase(self):
        """Initialize Firebase with the service account key."""
        cred_path = os.getenv('FIREBASE_CONFIG_PATH', 'firebase-config.json')
        if not os.path.exists(cred_path):
            logger.error(f"Firebase config file not found at {cred_path}.")
            raise FileNotFoundError(f"Firebase config file not found at {cred_path}.")
        
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        logger.info("Firebase initialized.")
    
    async def watch_contracts(self):
        """
        Watch for new contract creations and transactions.
        Returns a list of new contract addresses.
        """
        # This is a simplified example. In reality, you would use WebSocket subscriptions.
        # We'll listen for pending transactions and filter for contract creations.
        
        # Connect to the WebSocket endpoint for pending transactions
        ws_url = os.getenv('BASE_NODE_WS_URL')
        async with connect(ws_url) as ws:
            # Subscribe to pending transactions
            subscription_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "eth_subscribe",
                "params": ["newPendingTransactions"]
            }
            await ws.send(json.dumps(subscription_request))
            
            # Listen for messages
            while True:
                message = await ws.recv()
                data = json.loads(message)
                
                # Extract transaction hash
                tx_hash = data.get('params', {}).get('result')
                if tx_hash:
                    # Get transaction details
                    tx = self.w3.eth.get_transaction(tx_hash)
                    if tx and tx.to is None:  # Contract creation
                        contract_address = self.calculate_contract_address(tx)
                        logger.info(f"New contract detected: {contract_address}")
                        
                        # Store in Firestore
                        self.contracts_ref.document(contract_address).set({
                            'tx_hash': tx_hash,
                            'from': tx['from'],
                            'block_number': tx['blockNumber'],
                            'timestamp': datetime.utcnow(),
                            'processed': False
                        })
                        
                        # Also store the event
                        self.events_ref.document().set({
                            'type': 'contract_creation',
                            'contract_address': contract_address,
                            'tx_hash': tx_hash,
                            'timestamp': datetime.utcnow()
                        })
                        
                        yield contract_address
    
    def calculate_contract_address(self, tx):
        """Calculate the contract address from the transaction."""
        # Contract address is calculated as keccak256(rlp.encode([sender, nonce]))[12:]
        # Using web3 to get the contract address if available, otherwise calculate.
        if tx.creates:
            return tx.creates
        else:
            # Fallback calculation (simplified)
            return self.w3.keccak(
                self.w3.codec.encode_abi(
                    ['address', 'uint256'],
                    [tx['from'], tx['nonce']]
                )
            ).hex()[-40:]
```

Now, let's create the `analysis_core.py`.

### FILE: analysis_core.py
```python
"""
ANALYSIS CORE: Static and dynamic analysis of contracts.
"""

import hashlib
import logging
import subprocess
import tempfile
from datetime import datetime

from web3 import Web3
import firebase_admin
from firebase_admin import firestore

logger = logging.getLogger(__name__)

class ContractAnalyzer:
    def __init__(self, w3_provider):
        self.w3 = w3_provider
        self.db = firestore.client()
        
        logger.info("ContractAnalyzer initialized.")
    
    def analyze(self, contract_address):
        """Run static and dynamic analysis on a contract."""
        logger.info(f"Analyzing contract: {contract_address}")
        
        # Static analysis
        static_result = self.static_analysis(contract_address)
        
        # Dynamic analysis (fork simulation)
        dynamic_result = self.dynamic_analysis(contract_address)
        
        # Combine results
        analysis_result = {
            'static': static_result,
            'dynamic': dynamic_result,
            'timestamp': datetime.utcnow()
        }
        
        # Store in Firestore
        self.db.collection('contract_analysis').document(contract_address).set(analysis_result)
        
        return analysis_result
    
    def static_analysis(self, contract_address):
        """Static analysis of contract bytecode."""
        bytecode = self.w3.eth.get_code(contract_address).hex()
        
        # Extract features
        features = {
            'bytecode_length': len(bytecode),
            'function_selectors': self.extract_selectors(bytecode),
            'similarity_score': self.compare_to_known_malicious(bytecode),
            'contains_delegatecall': 'f4' in bytecode,  # DELEGATECALL opcode
            'contains_selfdestruct': 'ff' in bytecode,  # SELFDESTRUCT
            'unusual_opcodes': self.detect_unusual_opcodes(bytecode)
        }
        
        # Store bytecode hash for future reference
        bytecode_hash = hashlib.sha256(bytecode.encode()).hexdigest()
        self.db.collection('bytecode_hashes').document(contract_address).set({
            'hash': bytecode_hash,
            'timestamp': datetime.utcnow()
        })
        
        return features
    
    def extract_selectors(self, bytecode):
        """Extract function selectors from bytecode."""
        # This is a simplified example. In reality, you would need to parse the bytecode.
        # We'll look for PUSH4 opcodes (63) followed by 4 bytes (function selector).
        selectors = []
        i = 0
        while i < len(bytecode):
            if bytecode[i:i+2] == '63':  # PUSH4 opcode
                selector = bytecode[i+2:i+10]  # Next 4 bytes
                if len(selector) == 8:
                    selectors.append('0x' + selector)
                i += 10
            else:
                i += 2
        return selectors
    
    def compare_to_known_malicious(self, bytecode):
        """Compare bytecode to known malicious contracts in the database."""
        # Get all known malicious bytecode hashes
        malicious_hashes_ref = self.db.collection('malicious_bytecode_hashes').stream()
        malicious_hashes = [doc.to_dict()['hash'] for doc in malicious_hashes_ref]
        
        current_hash = hashlib.sha256(bytecode.encode()).hexdigest()
        
        # Return 1.0 if exact match, otherwise calculate similarity (simplified)
        if current_hash in malicious_hashes:
            return 1.0
        else:
            # For now, return 0.0. In reality, you might use more advanced similarity measures.
            return 0.0
    
    def detect_unusual_opcodes(self, bytecode):
        """Detect unusual or dangerous opcodes."""
        unusual = []
        # List of unusual opcodes (simplified)
        unusual_opcodes = {
            'f4': 'DELEGATECALL',
            'ff': 'SELFDESTRUCT',
            '54': 'SLOAD',
            '55': 'SSTORE',
            'f0': 'CREATE',
            'f5': 'CREATE2'
        }
        
        for opcode in unusual_opcodes:
            if opcode in bytecode:
                unusual.append(unusual_opcodes[opcode])
        
        return unusual
    
    def dynamic_analysis(self, contract_address):
        """Dynamic analysis using Foundry fork simulation."""
        # Check if Foundry is installed
        if not self.is_foundry_installed():
            logger.warning("Foundry is not installed. Skipping dynamic analysis.")
            return {'error': 'Foundry not installed'}
        
        # Create a temporary Solidity script for simulation
        with tempfile.NamedTemporaryFile(mode='w', suffix='.s.sol', delete=False) as f:
            script_content = self.generate_simulation_script(contract_address)
            f.write(script_content)
            script_path = f.name
        
        try:
            # Run the simulation
            result = subprocess.run(
                ['forge', 'script', script_path, '--fork-url', os.getenv('BASE_NODE_WS_URL')],
                capture_output=True,
                text=True
            )
            
            # Parse the output
            simulation_result = self.parse_simulation_output(result.stdout)
            
            # Store the simulation output in Firestore
            self.db.collection('simulations').document(contract_address).set({
                'output': result.stdout,
                'errors': result.stderr,
                'timestamp': datetime.utcnow()
            })
            
            return simulation_result
            
        except Exception as e:
            logger.error(f"Dynamic analysis failed for {contract_address}: {e}")
            return {'error': str(e)}
    
    def is_foundry_installed(self):
        """Check if Foundry is installed."""
        try:
            subprocess.run(['forge', '--version'], capture_output=True)
            return True
        except FileNotFoundError:
            return False
    
    def generate_simulation_script(self, contract_address):
        """Generate a Foundry simulation script for a contract."""
        return f"""
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "forge-std/Script.sol";

interface IERC20 {{
    function