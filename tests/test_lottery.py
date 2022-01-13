# ETH to USD price 3,130.89
# for minimum $50, 3130.89/50
# or 0.0159 ETH
# or in wei 15,9000000000,000000 WEI 

from brownie import Lottery, accounts, config, network, exceptions
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

def test_cant_enter_unless_started():
    # Arrange 
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    # Act/Assert    
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from":get_account(), "value": lottery.getEntranceFee()})

def test_can_start_and_enter_lottery():
    # Arrange 
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()    
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from":account})
    # Act
    lottery.enter({"from":account, "value":lottery.getEntranceFee()})    
    # Assert 
    assert lottery.players(0) == account

def test_can_end_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()    
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from":account})
    lottery.enter({"from":account, "value":lottery.getEntranceFee()})    
    fund_with_link(lottery)
    lottery.endLottery({"from":account})
    assert lottery.lottery_state() == 2



def test_can_pick_winner_correctly():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()    
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from":account})
    lottery.enter({"from":account, "value":lottery.getEntranceFee()})
    lottery.enter({"from":get_account(index=1), "value":lottery.getEntranceFee()})
    lottery.enter({"from":get_account(index=2), "value":lottery.getEntranceFee()})
    fund_with_link(lottery)
    starting_balance_of_account = account.balance()
    balance_of_lottery = lottery.balance()
    transaction = lottery.endLottery({"from":account})
    request_id = transaction.events["RequestedRandomness"]["requestId"]
    STATIC_RNG = 777
    print('static rng ===>',STATIC_RNG)
    get_contract('vrf_coordinator').callBackWithRandomness(request_id,STATIC_RNG, lottery.address, {"from":account} )
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
    assert account.balance() == starting_balance_of_account+balance_of_lottery

