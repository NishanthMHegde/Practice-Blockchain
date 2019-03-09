from Crypto.PublicKey import RSA
import Crypto.Random
import binascii
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

class Wallet():
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def createKeys(self):
        self.private_key,self.public_key = self.generate_keys()

    '''
    Used to generate a public and private key pair using Crypto library which has RSA algorithm
    binascii is used to convert a binary value to ascii using hexlify
    unhexlify is used to convert an ascii value back to binary
    '''

    def generate_keys(self):
        private_key = RSA.generate(1024,Crypto.Random.new().read)
        public_key = private_key.publickey()
        return (binascii.hexlify(private_key.exportKey(format = 'DER')).decode('ascii'),binascii.hexlify(public_key.exportKey(format = 'DER')).decode('ascii'))

    # used to save keys to a text file for future use
    def save_keys(self):
        if self.public_key is not None and self.private_key is not None:
            try:
                with open('keys.txt','w') as write_file:
                    write_file.write(self.public_key)
                    write_file.write("\n")
                    write_file.write(self.private_key)
            except:
                print("Error saving keys")
        else:
            print("Empty keys cannot be saved")

    # used to load previously saved keys
    def load_keys(self):
        try:
            with open('keys.txt','r') as read_file:
                key_data = read_file.readlines()
                self.public_key = key_data[0][:-1]
                self.private_key = key_data[1]
        except:
            print("Error loading keys")
    
    '''the user generated private key is used to create a signature 
        by using the hash of the transaction details and creating
        a new signer using the private key
    '''
    def sign(self,sender,recipient,amount):
        payload = (str(sender) + str(recipient) + str(amount)).encode('utf8')
        payload_hash = SHA256.new(payload)
        signer = PKCS1_v1_5.new(RSA.importKey(binascii.unhexlify(self.private_key)))
        signature = signer.sign(payload_hash)
        return binascii.hexlify(signature).decode('ascii')

    '''
    verify_transaction is used to check if the transaction was indeed
    committed by using the public_key of the user and the signature of the
    transaction by creating a verifier using the public_key and cross-checking
    the signature with the SHA256 encrypted payload of the transaction
    '''
    @staticmethod
    def verify_transaction(transaction):
        public_key = binascii.unhexlify(transaction.sender)
        verifier = PKCS1_v1_5.new(RSA.importKey(public_key))
        payload = (str(transaction.sender) + str(transaction.recipient) + str(transaction.amount)).encode('utf8')
        payload_hash = SHA256.new(payload)
        return verifier.verify(payload_hash,binascii.unhexlify(transaction.signature))




