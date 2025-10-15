from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from web3 import Web3

# Ensure project root (parent of managers/) is on sys.path so "wallet" is importable
import sys
from pathlib import Path
_BASE = Path(__file__).resolve().parent.parent
if str(_BASE) not in sys.path:
    sys.path.insert(0, str(_BASE))

from wallet.wallet import get_w3, get_token, send_token as _send_token

@dataclass
class WalletManager:
    w3: Optional[Web3] = None
    def __post_init__(self):
        if self.w3 is None:
            self.w3 = get_w3()
    def send(self, to_address: str, amount_wei: int) -> str:
        return _send_token(to_address, amount_wei)
    def transfer(self, to_address: str, amount_wei: int) -> str:
        return self.send(to_address, amount_wei)
    def send_token(self, to_address: str, amount_wei: int) -> str:
        return self.send(to_address, amount_wei)
    def balance(self, address: str) -> int:
        token = get_token(self.w3)
        return token.functions.balanceOf(Web3.to_checksum_address(address)).call()
    def balance_of(self, address: str) -> int:
        return self.balance(address)
    def balance_native(self, address: str) -> int:
        return self.w3.eth.get_balance(Web3.to_checksum_address(address))
