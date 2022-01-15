from brownie import network
import pytest 
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, fund_with_link, get_account
from scripts.deploy_lottery import deploy_lottery
import time

def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    print("+++++ lottery deployed +++++",lottery.address)
    accoount = get_account()
    print("+++++ got account +++++",accoount)
    fee = lottery.getEntranceFee()
    lottery.startLottery({"from":accoount})
    print("+++++ lottery started +++++")
    lottery.enter({"from":accoount, "value":fee})
    lottery.enter({"from":accoount, "value":fee})
    fund_with_link(lottery)
    print("+++++ funded the contract +++++")
    time.sleep(180)
    lottery.endLottery({"from":accoount})
    print("+++++ End Lottery +++++")
    print("+++++ sleep 60 ..... +++++")
    time.sleep(180)
    assert lottery.recentWinner() == accoount 
    assert lottery.balance() == 0

