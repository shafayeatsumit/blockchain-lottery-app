# ETH to USD price 3,130.89
# for minimum $50, 3130.89/50
# or 0.0159 ETH
# or in wei 15,9000000000,000000 WEI 

from brownie import Lottery, accounts, config, network
from web3 import Web3

def test_get_entrance_fee():
    account = accounts[0]
    lottery = Lottery.deploy(config["networks"][network.show_active()]["eth_usd_price_feed"],{"from":account})    
    entrance_fee = lottery.getEntranceFee()
    print('entrance_fee',entrance_fee)
    assert lottery.getEntranceFee() > Web3.toWei(0.015, 'ether')
    
    
    
def test_only_owner():
    account = accounts[0]    
    lottery = Lottery.deploy(config["networks"][network.show_active()]["eth_usd_price_feed"],{"from":account})
    lottery.endLottery()
    
