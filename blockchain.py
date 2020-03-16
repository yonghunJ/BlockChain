import logging
import sys
import time
import utils
import hashlib
import json

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)
MINING_DIFFICULTY = 3
MINING_SENDER = 'THE BLOCKCHAIN'
MINING_REWARD = 1.0

class BlockChain(object):

    def __init__(self, blockchain_address):
        self.transaction_pool = []
        self.chain = []
        self.create_block(0,self.hash({}))
        self.blockchain_address = blockchain_address


    def create_block(self, nounce, previous_hash):
        block = utils.sorted_dict_by_key({
            'timestamp': time.time(),
            'transactions': self.transaction_pool,
            'nounce' : nounce,
            'previous_hash' : previous_hash
        })

        self.chain.append(block)
        self.transaction_pool = []
        return block

    def hash(self, block):
        sroted_block = json.dumps(block, sort_keys=True)
        return hashlib.sha256(sroted_block.encode()).hexdigest()

    def add_transaction(self, sender_blockchain_address, recipient_blockchain_address, value):
        transaction = utils.sorted_dict_by_key({
            'sender_blockchain_address': sender_blockchain_address,
            'recipient_blockchain_address':recipient_blockchain_address,
            'value':float(value)
        })
        self.transaction_pool.append(transaction)

        return True

    def valid_proof(self, transactions, previous_hash, nounce, difficulty=MINING_DIFFICULTY):
        guess_block = utils.sorted_dict_by_key({
            'transactions': transactions,
            'nounce' : nounce,
            'previous_hash' : previous_hash
        })
        guess_hash = self.hash(guess_block)
        return guess_hash[:difficulty] == '0' * difficulty

    def proof_of_work(self):
        transactions = self.transaction_pool.copy()
        previous_hash = self.hash(self.chain[-1])

        nounce = 0

        while self.valid_proof(transactions, previous_hash, nounce) is False:
            nounce +=1
        return nounce


    def mining(self):
        self.add_transaction( sender_blockchain_address=MINING_SENDER, recipient_blockchain_address=self.blockchain_address, value=MINING_REWARD)
        nounce = self.proof_of_work()
        previous_hash = self.hash(self.chain[-1])
        self.create_block(nounce, previous_hash)
        logger.info({'action':'mining', 'status':'success'})
        return True


    def calculate_total_amount(self, blockchain_address):
        total_amoount = 0.0
        for block in self.chain:
            for transaction in block['transactions']:
                value  = float(transaction['value'])
                if blockchain_address == transaction['recipient_blockchain_address']:
                    total_amoount += value
                if blockchain_address == transaction['sender_blockchain_address']:
                    total_amoount -= value
        return total_amoount




if __name__ =='__main__':
    print('=================')


    my_blockchain_address = 'my_blockchain_address'
    block_chain = BlockChain(blockchain_address=my_blockchain_address)
    utils.pprint(block_chain.chain)

    block_chain.add_transaction('A','B',1.0)
    block_chain.mining()
    utils.pprint(block_chain.chain)

    block_chain.add_transaction('C','D',2.0)
    block_chain.add_transaction('X','Y',3.0)
    block_chain.mining()
    utils.pprint(block_chain.chain)

    print('my', block_chain.calculate_total_amount(my_blockchain_address))
    print('C', block_chain.calculate_total_amount('C'))
    print('D', block_chain.calculate_total_amount('D'))