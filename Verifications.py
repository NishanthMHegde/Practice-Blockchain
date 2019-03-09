import hashlib
class Verifications():
    '''
    vali_proof hashes the transactions and previousBlockHash and the unique proof until the 
    resulting sha256 hash begins with 00. The number of consecutive 0s can be increased for better security but will take 
    a lot of time
    '''
    @staticmethod
    def valid_proof(transactions,previousBlockHash,proof):
        total_string = str([txn.to_ordered_dict() for txn in transactions]) + str(previousBlockHash) + str(proof)
        str_hash = hashlib.sha256(total_string.encode('utf8')).hexdigest()

        print(str_hash)
        return str_hash[:2]=='00'

    '''
    Transaction verification consists of:
    a. Verifying if the sender has enough balance
    b. if the sender's public key can properly verify the transaction signature created using sender's private key

    '''
    @classmethod
    def verify_transactions(cls,open_transactions,get_balances):
        return all([cls.verify_transaction(txn,get_balances,check_funds = False) for txn in open_transactions])


    @staticmethod
    def verify_transaction(transaction,get_balances,check_funds=True):

        if check_funds is True:
            sender_balance = get_balances()
            if sender_balance >= transaction.amount and Wallet.verify_transaction(transaction) is True:
                return True
            else:
                return False
        else:
            return Wallet.verify_transaction(transaction)

    '''
    valid_chain is used to check :
    a. If the previousBlockHash of a particular block is the correct hash of the previous block.
    b. If the block has a valid proof number which when used gives a sha256 hash which begins with 00
    
    '''
    @classmethod
    def valid_chain(cls,blockchain):

        for (index,block) in enumerate(blockchain):
            if index == 0:
                continue
            if blockchain[index].previousBlockHash != HashUtils.hash_block(blockchain[index-1]):
                print("Blockchain was manipulated and hence cannot validate chain")
                return False
            if not cls.valid_proof(blockchain[index].transactions[:-1],blockchain[index].previousBlockHash,blockchain[index].proof):
                print("Proof of Work failed")
                return False

        return True