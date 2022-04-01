from uuid import getnode as get_mac_add
import json
from web3 import Web3
from blockchain import Blockchain

web3 = Blockchain().get_web3()

contract = Blockchain().get_contract()

print(contract)
 