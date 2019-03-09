
'''Block consists of index,previousblock hash, transactions
 and proof whch is a unique number (nonce = number used once)

'''

class Block():
    def __init__(self,index,previousBlockHash,transactions,proof):
        self.index = index
        self.previousBlockHash = previousBlockHash
        self.transactions = transactions
        self.proof = proof
