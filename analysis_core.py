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