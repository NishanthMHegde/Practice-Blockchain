import json
import hashlib
'''
SHA256 alogirthm is used to hash the contents of the block after converting it from a python dictionary to JSON 
totally including the transactions inside it.
SHA256 always returns the same has for same characters. 

'''
class HashUtils():

    def hash_block(self,block):
        hashable_block = block.__dict__.copy()
        hashable_block['transactions'] = [txn.__dict__ for txn in hashable_block['transactions']]
        block_hash = hashlib.sha256(json.dumps(hashable_block,sortKeys=True).encode('utf8')).hexdigest()
        return block_hash
