# fichier main.py
"""
ABDELAZIZ Hassan 
EL AROUI Youness

"""
"""
une Blockchain basique sur Python
"""


import hashlib
from ecdsa import SigningKey, NIST384p

class GeekCoinBlock:

    def __init__(self,previous_block_hash, transaction_list, signature, proof_work=0):
        self.previous_block_hash = previous_block_hash
        self.transaction_list = transaction_list
        
        self.block_data = f"{' - '.join(transaction_list)} - {previous_block_hash}"
        self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()
        self.block_signature = signature
        self.proof_work = proof_work
    
class Blockchain:

    def __init__(self):
    
        self.difficulty = 2
        self.chain = []
        self.generate_genesis_block()

    def generate_genesis_block(self):
        self.chain.append(GeekCoinBlock("0", ['Genesis Block'],0))


    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        
        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:5] == '00000':
                check_proof = True
            else:
                new_proof += 1
                
        return new_proof

    def create_block_from_transaction(self, transaction_list):
        previous_block_hash = self.last_block.block_hash
        previous_proof=self.last_block.proof_work

        proof_work = Blockchain().proof_of_work(previous_proof)
        message= f"{' - '.join(transaction_list)} - {previous_block_hash}"
        y = hashlib.sha256(message.encode()).hexdigest()
        y = y.encode()

        private_key = SigningKey.generate(curve=NIST384p) # generation de la  clé privée
        sk_string = private_key.to_string()

        public_key = private_key.verifying_key #generation de la clé publique
        y1 = private_key.sign(y) #signature
        assert public_key.verify(y1, y)
        self.chain.append(GeekCoinBlock(previous_block_hash, transaction_list,int.from_bytes(y1, byteorder = 'big'),proof_work))

    def is_valid_proof(self, chain):
        previous_block=chain[0]
        block_index=1
        while block_index < len(chain):
            block=chain[block_index]
            previous_code_message= f"{' - '.join(transaction_list)} - {previous_block_hash}"
            if block.previous_block_hash!=hashlib.sha256(previous_block_hash.encode()).hexdigest():
                return False
            previous_proof=previous_block.proof_work
            prook_work=block.proof_work
            hash_operation=hashlib.sha256(str(proof_work**2 - previous_proof**2).encode()).hexdigest()

            if hash_operation[:5]!='00000':
                return False
            previou_block=block
            block_index +=1

        return True

    def display_chain(self):
        for i in range(len(self.chain)):
            print(f"Data {i + 1}: {self.chain[i].block_data}")
            print(f"Hash {i + 1}: {self.chain[i].block_hash}")
            print(f"Signature {i + 1}: {self.chain[i].block_signature}")
            print(f"proof_of_work {i + 1}: {self.chain[i].proof_work}")
            print("\n")

    @property
    def last_block(self):
        return self.chain[-1]


t1 = "J'ai dépensé 5 € chez amazone"
t2 = "J'ai dépensé 70 € à Total"
t3 = "J'ai reçu 2100€ de salaire"
t4 = "J'ai fait 100€ de course à Auchan"
t5 = "J'ai payé 110€ de facture d'électricité"
t6 = "J'ai payé 30€ de facture de téléphone"

myblockchain = Blockchain()

myblockchain.create_block_from_transaction([t1, t2])
myblockchain.create_block_from_transaction([t3, t4])
myblockchain.create_block_from_transaction([t5, t6])

myblockchain.display_chain()
