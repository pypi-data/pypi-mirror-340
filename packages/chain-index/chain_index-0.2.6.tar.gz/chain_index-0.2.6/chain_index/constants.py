"""
Blockchain-related constants for convenient reference.

This module provides common constants used in blockchain development,
such as event topics, function signatures, and other frequently used values.

Usage:
    from chain_index import constants

    # Use event topics
    constants.TRANSFER_EVENT_TOPIC
    constants.UNISWAP_V2_SWAP_EVENT_TOPIC

    # Or access through categories
    constants.EventTopics.TRANSFER
    constants.FunctionSignatures.TRANSFER
    constants.Addresses.NULL_ADDRESS
    constants.BlockTime.ETHEREUM
"""

# =============================================================================
# Direct exports (for backward compatibility and convenience)
# =============================================================================

# ERC20 Event Topics
TRANSFER_EVENT_TOPIC = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'
APPROVAL_EVENT_TOPIC = '0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925'

# ERC721 Event Topics
TRANSFER_SINGLE_EVENT_TOPIC = '0xc3d58168c5ae7397731d063d5bbf3d657854427343f4c083240f7aacaa2d0f62'
TRANSFER_BATCH_EVENT_TOPIC = '0x4a39dc06d4c0dbc64b70af90fd698a233a518aa5d07e595d983b8c0526c8f7fb'

# DEX Event Topics
UNISWAP_V2_SWAP_EVENT_TOPIC = '0xd78ad95fa46c994b6551d0da85fc275fe613ce37657fb8d5e3d130840159d822'
UNISWAP_V3_SWAP_EVENT_TOPIC = '0xc42079f94a6350d7e6235f29174924f928cc2ac818eb64fed8004e115fbcca67'

# Common Function Signatures
TRANSFER_FUNC_SIG = '0xa9059cbb'  # transfer(address,uint256)
TRANSFER_FROM_FUNC_SIG = '0x23b872dd'  # transferFrom(address,address,uint256)
APPROVE_FUNC_SIG = '0x095ea7b3'  # approve(address,uint256)
BALANCE_OF_FUNC_SIG = '0x70a08231'  # balanceOf(address)

# Common Contract Addresses (Ethereum Mainnet)
ETH_NULL_ADDRESS = '0x0000000000000000000000000000000000000000'
UNISWAP_V2_FACTORY = '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f'
UNISWAP_V2_ROUTER = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'
UNISWAP_V3_FACTORY = '0x1F98431c8aD98523631AE4a59f267346ea31F984'
UNISWAP_V3_ROUTER = '0xE592427A0AEce92De3Edee1F18E0157C05861564'
SUSHISWAP_FACTORY = '0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac'

# Gas Limits
DEFAULT_ERC20_TRANSFER_GAS = 65000
DEFAULT_ERC20_APPROVE_GAS = 45000
DEFAULT_SWAP_GAS = 200000

# Chain-specific Constants
ETHEREUM_AVERAGE_BLOCK_TIME = 12  # seconds
BSC_AVERAGE_BLOCK_TIME = 3  # seconds
POLYGON_AVERAGE_BLOCK_TIME = 2  # seconds
ARBITRUM_AVERAGE_BLOCK_TIME = 0.25  # seconds
OPTIMISM_AVERAGE_BLOCK_TIME = 2  # seconds
AVALANCHE_AVERAGE_BLOCK_TIME = 2  # seconds

# =============================================================================
# Categorized constants (for better organization)
# =============================================================================

class EventTopics:
    """Common Ethereum event topics (keccak hash of event signatures)."""
    
    # ERC20 Events
    TRANSFER = TRANSFER_EVENT_TOPIC
    APPROVAL = APPROVAL_EVENT_TOPIC
    
    # ERC721 Events
    TRANSFER_SINGLE = TRANSFER_SINGLE_EVENT_TOPIC
    TRANSFER_BATCH = TRANSFER_BATCH_EVENT_TOPIC
    
    # DEX Events
    UNISWAP_V2_SWAP = UNISWAP_V2_SWAP_EVENT_TOPIC
    UNISWAP_V3_SWAP = UNISWAP_V3_SWAP_EVENT_TOPIC
    
    class ERC20:
        """ERC20 specific event topics."""
        TRANSFER = TRANSFER_EVENT_TOPIC
        APPROVAL = APPROVAL_EVENT_TOPIC
    
    class ERC721:
        """ERC721 specific event topics."""
        TRANSFER_SINGLE = TRANSFER_SINGLE_EVENT_TOPIC
        TRANSFER_BATCH = TRANSFER_BATCH_EVENT_TOPIC
    
    class Uniswap:
        """Uniswap specific event topics."""
        V2_SWAP = UNISWAP_V2_SWAP_EVENT_TOPIC
        V3_SWAP = UNISWAP_V3_SWAP_EVENT_TOPIC


class FunctionSignatures:
    """Common Ethereum function signatures (first 4 bytes of keccak hash)."""
    
    # ERC20 Functions
    TRANSFER = TRANSFER_FUNC_SIG
    TRANSFER_FROM = TRANSFER_FROM_FUNC_SIG
    APPROVE = APPROVE_FUNC_SIG
    BALANCE_OF = BALANCE_OF_FUNC_SIG
    
    class ERC20:
        """ERC20 specific function signatures."""
        TRANSFER = TRANSFER_FUNC_SIG
        TRANSFER_FROM = TRANSFER_FROM_FUNC_SIG
        APPROVE = APPROVE_FUNC_SIG
        BALANCE_OF = BALANCE_OF_FUNC_SIG


class Addresses:
    """Common Ethereum addresses."""
    
    NULL_ADDRESS = ETH_NULL_ADDRESS
    
    class Uniswap:
        """Uniswap specific addresses."""
        V2_FACTORY = UNISWAP_V2_FACTORY
        V2_ROUTER = UNISWAP_V2_ROUTER
        V3_FACTORY = UNISWAP_V3_FACTORY
        V3_ROUTER = UNISWAP_V3_ROUTER
    
    class Sushiswap:
        """Sushiswap specific addresses."""
        FACTORY = SUSHISWAP_FACTORY


class GasLimits:
    """Standard gas limits for common operations."""
    
    ERC20_TRANSFER = DEFAULT_ERC20_TRANSFER_GAS
    ERC20_APPROVE = DEFAULT_ERC20_APPROVE_GAS
    SWAP = DEFAULT_SWAP_GAS


class BlockTime:
    """Average block time in seconds for different chains."""
    
    ETHEREUM = ETHEREUM_AVERAGE_BLOCK_TIME
    BSC = BSC_AVERAGE_BLOCK_TIME
    POLYGON = POLYGON_AVERAGE_BLOCK_TIME
    ARBITRUM = ARBITRUM_AVERAGE_BLOCK_TIME
    OPTIMISM = OPTIMISM_AVERAGE_BLOCK_TIME
    AVALANCHE = AVALANCHE_AVERAGE_BLOCK_TIME 