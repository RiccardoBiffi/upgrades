from scripts.utilities import get_account, encode_function_data
from brownie import network, Box, ProxyAdmin, TransparentUpgradeableProxy, Contract


def main():
    account = get_account()
    print(f"Deploying to {network.show_active()}")
    box = Box.deploy({"from": account})
    proxy_admin = ProxyAdmin.deploy({"from": account})

    # when we call the implementation, we need to initialize its constructor
    # that initialization is responsability of the proxy.
    # to initialize, we need to encode the funtion we call and the data we pass
    # into bytes and then pass it to the initializer.

    # initializer = box.store, 5  # OMG it's enought to create a couple?? Cool!
    box_initializer_bytes = encode_function_data()

    # maybe add the "gas_limit" attribute
    proxy = TransparentUpgradeableProxy.deploy(
        box.address, proxy_admin.address, box_initializer_bytes, {"from": account}
    )

    print(f"Proxi deployed to {proxy.address}, you can use it to upgrade the logic")

    # from now on I call Box methods throught the proxy

    # I link Box abi with Proxy address. There are 2 different smart contract and
    # I should get an error, but proxy will delegate all calls to Box so that's ok
    box_pry = Contract.from_abi("Box", proxy.address, Box.abi)
    box_pry.store(3, {"from": account})

    # data is stored in proxi contract, not in box
    print(box_pry.retrieve())  # returns 3
    print(box.retrieve())  # returns 0
