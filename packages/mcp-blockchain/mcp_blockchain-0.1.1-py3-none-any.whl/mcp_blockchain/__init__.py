"""MCP Blockchain: A production-grade blockchain server built using MCP (Model Context Protocol).

Features:
1. Ethereum Address Validator - Validates addresses including checksum verification
2. Gas Fee Estimator - Estimates gas fees using public RPC endpoints
3. Wallet Balance Checker - Checks ETH balances with fallback RPCs
4. Smart Contract Ownership Checker - Handles proxy contracts and multiple ownership patterns

Note: This package uses public RPC endpoints which may have rate limits.
For production use, consider using your own RPC endpoint.
"""

__version__ = "0.1.0"

from .server import (
    mcp,
    validate_ethereum_address,
    estimate_gas_fee,
    check_wallet_balance,
    check_contract_owner,
    calculate_transaction_cost
)

__all__ = [
    "mcp",
    "validate_ethereum_address",
    "estimate_gas_fee",
    "check_wallet_balance",
    "check_contract_owner",
    "calculate_transaction_cost"
]

