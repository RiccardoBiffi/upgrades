from scripts.utilities import get_account, encode_function_data, upgrade
from brownie import (
    network,
    config,
    Box,
    BoxV2,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
)


def main():
    account = get_account()
    print(f"Deploying to {network.show_active()}")
    box = Box.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    proxy_admin = ProxyAdmin.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )

    # When we call the implementation, we need to initialize its constructor (any method).
    # That initialization is responsability of the proxy.
    # To initialize, we need to encode the funtion we call and the data we pass
    # into bytes and then pass it to the initializer.

    # initializer = box.store, 5  # OMG it's enought to create a couple?? Cool!
    box_initializer_bytes = encode_function_data()  # we don't use an initializer now

    # maybe add the "gas_limit" attribute in last arg
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_initializer_bytes,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )

    print(f"Proxy deployed to {proxy.address}.")
    print(
        f"Use the proxy admin at {proxy_admin.address} to upgrade the implementation\n"
    )

    # from now on I call Box methods throught the proxy

    # I link Box abi with Proxy address. These are 2 different smart contract and
    # I should get an error, but proxy will delegate all calls to Box so that's ok!
    box_pry = Contract.from_abi("Box", proxy.address, Box.abi)
    box_pry.store(3, {"from": account})

    # data is stored in proxy contract, not in Box contract
    print(box_pry.retrieve())  # returns 3
    print(box.retrieve())  # returns 0

    # box_pry.increment({"from": account}) # fails

    box_v2 = BoxV2.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    boxV2_pry = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    tx = upgrade(account, proxy, box_v2.address, proxy_admin)

    boxV2_pry.increment({"from": account})
    print(boxV2_pry.retrieve())  # returns 4
