import pytest
from scripts.utilities import get_account, encode_function_data, upgrade
from brownie import (
    network,
    Box,
    BoxV2,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    exceptions,
    Contract,
)


def test_proxy_delegate_calls():
    # Arrange
    account = get_account()
    box = Box.deploy({"from": account})
    proxy_admin = ProxyAdmin.deploy({"from": account})
    box_encoded_init = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address, proxy_admin.address, box_encoded_init, {"from": account}
    )

    # Act
    box_proxy = Contract.from_abi("Box", proxy.address, box.abi)
    box_proxy.store(1, {"from": account})

    # Assert
    assert box_proxy.retrieve() == 1


def test_proxy_upgrade_contract_success():
    # Arrange
    account = get_account()
    box = Box.deploy({"from": account})
    boxV2 = BoxV2.deploy({"from": account})
    proxy_admin = ProxyAdmin.deploy({"from": account})
    box_encoded_init = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address, proxy_admin.address, box_encoded_init, {"from": account}
    )
    box_proxy = Contract.from_abi("Box", proxy.address, box.abi)

    # Act
    box_proxy.store(1, {"from": account})
    upgrade(account, proxy, boxV2, proxy_admin)
    boxV2_proxy = Contract.from_abi("BoxV2", proxy.address, boxV2.abi)

    # Assert
    assert boxV2_proxy.retrieve() == 1
    assert boxV2_proxy.increment({"from": account})


def test_proxy_upgrade_contract_fail():
    # Arrange
    account = get_account()
    box = Box.deploy({"from": account})
    boxV2 = BoxV2.deploy({"from": account})
    proxy_admin = ProxyAdmin.deploy({"from": account})
    box_encoded_init = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address, proxy_admin.address, box_encoded_init, {"from": account}
    )
    box_proxy = Contract.from_abi("Box", proxy.address, box.abi)

    # Act
    box_proxy.store(1, {"from": account})
    # no upgrade
    boxV2_proxy = Contract.from_abi("BoxV2", proxy.address, boxV2.abi)

    # Assert
    with pytest.raises(exceptions.VirtualMachineError):
        boxV2_proxy.increment({"from": account})
