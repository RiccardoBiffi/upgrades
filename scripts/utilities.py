from enum import Enum
from brownie import network, accounts, config, Contract
from brownie import web3
import eth_utils

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"  # contract_address/token_ID
BREED_MAPPING = {0: "PUG", 1: "SHIBA_INU", 2: "ST_BERNARD"}


class MockContract(Enum):
    LINK_TOKEN = "link_token"
    VRF_COORDINATOR = "vrf_coordinator"


def is_local_blockchain():
    return network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]  # Ganache's first account
    if id:
        return accounts.load(id)

    # mainnet
    return accounts.add(config["wallets"]["from_key"])


# initializer = box.store, 1,2,3
def encode_function_data(
    init_function=None, *args
):  # *args means "any other arguments" in type and number
    """
    Encodes the function call into bytes to work with an initializer.

    Args:
        init_function ([brownie.network.contract.ContractTx], optional):
        The initializer function we want to call. Ex: "box.store"
        Default to None.

        args (Any, optional):
        The arguments to pass to the initializer function.

    Returns:
        [bytes]: Initializer function and arguments encoded into bytes.
    """
    if len(args) == 0 or init_function == None:
        return eth_utils.to_bytes(hexstr="0x")  # blank hex means no arguments to caller
    return init_function.encode_input(*args)
