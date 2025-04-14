# MCP Blockchain

A production-grade blockchain server built using MCP (Model Context Protocol).

## Features

- Ethereum Address Validator
- Gas Fee Estimator (Public RPC)
- Wallet Balance Checker
- Smart Contract Ownership Checker

## Installation

```bash
uvx mcp-blockchain
```

## Usage

After installation, you can use the MCP Blockchain server with Claude for Desktop or any other MCP client.

### Configuration

Add the following to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
    "mcpServers": {
        "blockchain-tools": {
            "command": "mcp-blockchain"
        }
    }
}
```

### Available Tools

1. **Ethereum Address Validator**
   - Validates Ethereum addresses including checksum verification

2. **Gas Fee Estimator**
   - Gets current gas fees from Ethereum mainnet using public RPC
   - Shows base fee and gas price in Gwei

3. **Wallet Balance Checker**
   - Checks ETH balance of any Ethereum address

4. **Smart Contract Ownership Checker**
   - Verifies if a contract implements the Ownable interface
   - Retrieves the owner address if available

## Development

```bash
# Clone the repository
git clone https://github.com/rjn32s/mcp-blockchain.git
cd mcp-blockchain

# Create virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
uv add -e .
```

## License

MIT License
