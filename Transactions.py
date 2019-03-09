'''
 A transaction consists of:
 Sender : person sending the currency
 Recipient: person receiving the currency
 amount : amount of money sent
 signature : A unique signature created by senders private key and verified using sender's public key

'''


from collections import OrderedDict
class Transactions():
    def __init__(self,sender,recipient,amount,signature):
        self.sender =sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature

    def to_ordered_dict(self):
        return OrderedDict([('sender',self.sender),('recipient',self.recipient),('amount',self.amount),('signature',self.signature)])