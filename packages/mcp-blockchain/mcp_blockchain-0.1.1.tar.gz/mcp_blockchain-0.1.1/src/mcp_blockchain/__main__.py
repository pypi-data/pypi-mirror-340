#!/usr/bin/env python3
"""
Command-line entry point for the MCP Blockchain Server.

This server provides blockchain interaction tools including:
- Address validation
- Gas fee estimation
- Wallet balance checking
- Contract ownership verification
"""

import argparse
import sys
from .server import mcp

def main():
    """MCP Blockchain: Interact with blockchain networks using various tools."""
    parser = argparse.ArgumentParser(
        description="Interact with blockchain networks using various tools including address validation, gas estimation, and contract inspection."
    )
    
    # Add configuration options
    parser.add_argument(
        "--rpc-timeout",
        type=int,
        default=30,
        help="Timeout in seconds for RPC calls (default: 30)"
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=3,
        help="Maximum number of retries for RPC calls (default: 3)"
    )
    
    args = parser.parse_args()
    
    try:
        mcp.run(transport='stdio')
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
