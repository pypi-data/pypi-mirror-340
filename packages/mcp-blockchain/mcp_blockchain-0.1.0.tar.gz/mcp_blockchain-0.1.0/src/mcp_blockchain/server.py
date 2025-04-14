from typing import Any, Optional
from web3 import Web3
import requests
from eth_utils import is_address
from mcp.server.fastmcp import FastMCP
import time
from functools import wraps

# Initialize FastMCP server
mcp = FastMCP("blockchain-tools")

# List of public RPC endpoints to try
PUBLIC_RPCS = [
    "https://eth.llamarpc.com",  # LlamaNodes
    "https://ethereum.publicnode.com",  # PublicNode
    "https://eth-mainnet.public.blastapi.io",  # BlastAPI
    "https://cloudflare-eth.com"  # Cloudflare (fallback)
]

# Default configuration
DEFAULT_TIMEOUT = 30
DEFAULT_MAX_RETRIES = 3

def retry_on_failure(max_retries: int = DEFAULT_MAX_RETRIES, delay: int = 1):
    """Decorator to retry functions on failure."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        time.sleep(delay * (attempt + 1))  # Exponential backoff
            raise last_exception
        return wrapper
    return decorator

@retry_on_failure()
def get_web3(timeout: int = DEFAULT_TIMEOUT) -> Web3:
    """Get a working Web3 instance by trying different RPC endpoints."""
    for rpc_url in PUBLIC_RPCS:
        try:
            web3 = Web3(Web3.HTTPProvider(rpc_url, request_kwargs={'timeout': timeout}))
            if web3.is_connected():
                return web3
        except Exception:
            continue
    raise Exception("Unable to connect to any Ethereum RPC endpoint")

def to_checksum(addr: str) -> str:
    """Convert an address to its checksummed version."""
    try:
        return Web3.to_checksum_address(addr)
    except Exception:
        raise ValueError("Invalid Ethereum address format")

@retry_on_failure()
def get_eip1967_impl(proxy: str, web3: Web3) -> Optional[str]:
    """Get the implementation address of a proxy contract using EIP-1967."""
    try:
        # EIP-1967 implementation slot = keccak("eip1967.proxy.implementation") - 1
        slot = int(Web3.keccak(text="eip1967.proxy.implementation").hex(), 16) - 1
        raw = web3.eth.get_storage_at(proxy, slot)
        
        # The implementation address is stored in the last 20 bytes (40 hex characters)
        impl = "0x" + raw.hex()[-40:]
        
        # Convert to checksum address if valid
        if is_address(impl) and int(impl, 16) != 0:
            return to_checksum(impl)
        return None
    except Exception as e:
        print(f"Error getting implementation: {str(e)}")
        return None

@retry_on_failure()
def read_owner_slot(addr: str, web3: Web3) -> Optional[str]:
    """Read the owner from storage slot 0 (OpenZeppelin Ownable pattern)."""
    try:
        raw = web3.eth.get_storage_at(addr, 0)
        owner = "0x" + raw.hex()[-40:]
        return to_checksum(owner) if is_address(owner) and int(owner, 16) != 0 else None
    except Exception:
        return None

@mcp.tool()
async def validate_ethereum_address(address: str) -> str:
    """Validate if a given string is a valid Ethereum address.

    Args:
        address: Ethereum address to validate
    """
    try:
        is_valid = is_address(address)
        if is_valid:
            web3 = get_web3()
            is_checksum = web3.is_checksum_address(address)
            return f"Valid Ethereum address. Checksum valid: {is_checksum}"
        return "Invalid Ethereum address"
    except Exception as e:
        return f"Error validating address: {str(e)}"

@mcp.tool()
async def estimate_gas_fee() -> str:
    """Estimate current gas fees on Ethereum mainnet using public RPC."""
    try:
        web3 = get_web3()
        if not web3.is_connected():
            return "Error: Unable to connect to Ethereum network. Please try again later."
            
        gas_price = web3.eth.gas_price
        base_fee = web3.eth.get_block('latest').baseFeePerGas
        
        # Convert from Wei to Gwei
        gas_price_gwei = web3.from_wei(gas_price, 'gwei')
        base_fee_gwei = web3.from_wei(base_fee, 'gwei')
        
        return f"""
Current Ethereum Gas Fees:
Base Fee: {base_fee_gwei:.2f} Gwei
Gas Price: {gas_price_gwei:.2f} Gwei
Estimated Cost for Basic Transfer: {gas_price_gwei * 21000:.0f} Gwei
Note: These are estimates and may vary based on network conditions
"""
    except Exception as e:
        return f"Error estimating gas fees: {str(e)}"

@mcp.tool()
async def check_wallet_balance(address: str) -> str:
    """Check ETH balance of a wallet address using public RPC.

    Args:
        address: Ethereum wallet address
    """
    try:
        if not is_address(address):
            return "Invalid Ethereum address"
            
        web3 = get_web3()
        if not web3.is_connected():
            return "Error: Unable to connect to Ethereum network. Please try again later."
            
        balance_wei = web3.eth.get_balance(address)
        balance_eth = web3.from_wei(balance_wei, 'ether')
        
        return f"Wallet Balance: {balance_eth:.4f} ETH"
    except Exception as e:
        return f"Error checking balance: {str(e)}"

@mcp.tool()
async def check_contract_owner(address: str) -> str:
    """Check if a contract implements an Ownable-style interface and return its owner.
    
    This function:
    1. Handles proxy contracts (EIP-1967)
    2. Checks both proxy and implementation owners
    3. Tries multiple owner-style methods
    4. Falls back to reading storage slots
    
    Args:
        address: Smart contract address
    """
    try:
        if not is_address(address):
            return "Invalid contract address."
            
        web3 = get_web3()
        if not web3.is_connected():
            return "Error: Cannot connect to Ethereum network."
            
        proxy = to_checksum(address)
        result = []

        # 1) Check proxy owner (slot 0)
        proxy_owner = read_owner_slot(proxy, web3)
        if proxy_owner:
            result.append(f"Proxy @ {proxy} owner (slot 0): {proxy_owner}")

        # 2) Check for EIP-1967 implementation
        impl = get_eip1967_impl(proxy, web3)
        if impl:
            result.append(f"Implementation contract: {impl}")
            
            # Check implementation owner (slot 0)
            impl_owner = read_owner_slot(impl, web3)
            if impl_owner:
                result.append(f"Implementation @ {impl} owner (slot 0): {impl_owner}")
            
            # Try owner methods on implementation
            methods = ["owner", "getOwner", "admin", "getAdmin"]
            abi = [{
                "constant": True,
                "inputs": [],
                "name": m,
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            } for m in methods]

            contract = web3.eth.contract(address=impl, abi=abi)
            for m in methods:
                try:
                    owner = getattr(contract.functions, m)().call()
                    if is_address(owner) and int(owner, 16) != 0:
                        result.append(f"Implementation owner (via `{m}()`): {to_checksum(owner)}")
                        break
                except Exception as e:
                    print(f"Error calling {m}(): {str(e)}")
                    continue
        else:
            # If not a proxy, try owner methods directly
            methods = ["owner", "getOwner", "admin", "getAdmin"]
            abi = [{
                "constant": True,
                "inputs": [],
                "name": m,
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            } for m in methods]

            contract = web3.eth.contract(address=proxy, abi=abi)
            for m in methods:
                try:
                    owner = getattr(contract.functions, m)().call()
                    if is_address(owner) and int(owner, 16) != 0:
                        result.append(f"Contract owner (via `{m}()`): {to_checksum(owner)}")
                        break
                except Exception as e:
                    print(f"Error calling {m}(): {str(e)}")
                    continue

        if not result:
            return "Contract does not implement an Ownable interface or owner could not be read."
            
        return "\n".join(result)
    except Exception as e:
        return f"Error checking contract owner: {str(e)}"

@mcp.tool()
async def calculate_transaction_cost(transaction_type: str) -> str:
    """Calculate the estimated cost for different types of transactions.
    
    Args:
        transaction_type: Type of transaction (basic_transfer, erc20_transfer, nft_transfer, uniswap_swap, contract_deploy)
    """
    try:
        web3 = get_web3()
        if not web3.is_connected():
            return "Error: Unable to connect to Ethereum network. Please try again later."
            
        # Get current gas price
        gas_price = web3.eth.gas_price
        gas_price_gwei = web3.from_wei(gas_price, 'gwei')
        
        # Define gas limits for different transaction types
        gas_limits = {
            "basic_transfer": 21000,  # Basic ETH transfer
            "erc20_transfer": 65000,  # ERC20 token transfer
            "nft_transfer": 100000,   # NFT transfer
            "uniswap_swap": 180000,   # Uniswap swap
            "contract_deploy": 2000000 # Contract deployment
        }
        
        if transaction_type not in gas_limits:
            raise ValueError(f"Invalid transaction type. Must be one of: {', '.join(gas_limits.keys())}")
            
        gas_limit = gas_limits[transaction_type]
        cost_gwei = gas_price_gwei * gas_limit
        cost_eth = web3.from_wei(cost_gwei * 10**9, 'ether')
        
        return f"""
Transaction Type: {transaction_type}
Gas Limit: {gas_limit:,} units
Gas Price: {gas_price_gwei:.2f} Gwei
Estimated Cost: {cost_gwei:.0f} Gwei ({cost_eth:.8f} ETH)
Note: These are estimates and may vary based on network conditions
"""
    except Exception as e:
        return f"Error calculating transaction cost: {str(e)}"

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
