from contextlib import nullcontext
import json
from web3 import Web3


class Blockchain:

    def __init__(self):
    
        self.contract = None
        self.web3 = None

        ganache_url = "HTTP://192.168.243.79:7545"
        web3 = Web3(Web3.HTTPProvider(ganache_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        print(web3.isConnected())
        print(web3.eth.defaultAccount)

        abi = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"userId","type":"address"}],"name":"DeviceBinded","type":"event"},{"inputs":[{"internalType":"string","name":"_device_id","type":"string"},{"internalType":"address","name":"_userId","type":"address"}],"name":"bindDevice","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"_deviceId","type":"string"}],"name":"getBindingInfo","outputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_device_id","type":"string"}],"name":"resetBinding","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
        address = web3.toChecksumAddress(
            '0x03c71b3cf2B005337901600312B16c16C1BC86a6')

        self.contract = web3.eth.contract(address=address, abi=abi)

        self.set_contract(self.contract)
        self.set_web3(web3)

    def bindCam(self, _camAdd, _userAdd):

        try:
            _userAdd = self.web3.toChecksumAddress(_userAdd)
            tx_hash = self.contract.functions.bindDevice(_camAdd,
                                                         _userAdd).transact()
            receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
            if "status" in receipt:
                return receipt['status']
        except Exception as e:
            print(e)

    def resetCam(self, _camAdd):
        try:
            tx_hash = self.contract.functions.resetBinding(_camAdd).transact()
            receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
            if "status" in receipt:
                return receipt['status']
        except Exception as e:
            print(e)

    def getBindingInfo(self, _camAdd):
        try:
            camInfo = self.contract.functions.getBindingInfo(_camAdd).call()
            return camInfo
        except Exception as e:
            print(e)

    def get_contract(self):
        return self.contract

    def get_web3(self):
        return self.web3

    def set_contract(self, _contract):
        self.contract = _contract

    def set_web3(self, _web):
        self.web3 = _web