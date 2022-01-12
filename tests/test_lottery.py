# ETH to USD price 3,130.89
# for minimum $50, 3130.89/50
# or 0.0159 ETH
# or in wei 15,9000000000,000000 WEI 

from brownie import Lottery, accounts, config, network
from scripts.deploy_lottery import deploy_lottery
from web3 import Web3
import pytest
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    fund_with_link,
    get_contract,
)


# def test_get_entrance_fee():
#     account = accounts[0]
#     lottery = Lottery.deploy(config["networks"][network.show_active()]["eth_usd_price_feed"],{"from":account})    
#     entrance_fee = lottery.getEntranceFee()
#     print('entrance_fee',entrance_fee)
#     assert lottery.getEntranceFee() > Web3.toWei(0.015, 'ether')
    
    


def test_get_entrance_fee():
    # we want to run all the unit test in local blockchain
    # not in test net
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange 
    lottery = deploy_lottery()
    # Act 
    # 2000 eth/usd is 50    
    # usdEntryFee is 50 
    # 2000/1 == 50/x == 0.025
    expected_entrance_fee = Web3.toWei(0.025,'ether')
    entrance_fee = lottery.getEntranceFee()
    # Assert 
    assert expected_entrance_fee == entrance_fee