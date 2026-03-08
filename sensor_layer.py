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