# Imports
import streamlit as st
from dataclasses import dataclass
from typing import Any, List
import datetime as datetime
import pandas as pd
import hashlib

@dataclass
class RecordData:
    
    sender: int
    receiver : str
    amount: float


@dataclass
class Block:

    record: RecordData

    creator_id: str
    prev_hash: str = "0"
    timestamp: str = datetime.datetime.utcnow().strftime("%H:%M:%S")
    nonce: int = 0 

    def hash_block(self):
        
        sha = hashlib.sha256()
        
        record = str(self.record).encode()
        sha.update(record)

        creator_id = str(self.creator_id).encode()
        sha.update(creator_id)

        prev_hash = str(self.prev_hash).encode()
        sha.update(prev_hash)

        timestamp = str(self.timestamp).encode()
        sha.update(timestamp)

        nonce = str(self.nonce).encode()
        sha.update(nonce)

        return sha.hexdigest()

@dataclass

class PyChain:

    chain: List[Block]
    difficulty: int = 4

    def proof_of_work(self,block):

        calculated_hash = block.hash_block()
        num_of_zeros = "0" * self.difficulty

        while not calculated_hash.startswith(num_of_zeros):

            block.nonce += 1
            calculated_hash = block.hash_block()

        print("Wining HASH", calculated_hash)
        return block

    def add_block(self,candidate_block):

        block = self.proof_of_work(candidate_block)
        self.chain += [block]

    def is_valid(self):

        block_hash = self.chain[0].hash_block()

        for block in self.chain[1:]:
            if block_hash != block.prev_hash:
                print("Block is invalid")
                return False

            block_hash = block.hash_block()

        print("Blockchain is Valid")
        return True


@st.cache(allow_output_mutation=True)

def setup():
    print("Initializing Chain")
    return PyChain([Block("Gensis",0)])


st.markdown("# PyChain")
st.markdown("## Store a Transaction Record in the PyChain")

pychain = setup()

sender = st.text_input("Sender")

receiver = st.text_input("reciever")

amount = st.number_input("Amount", min_value=0.0)


if st.button("Add Block"):
    # Get previous block hash
    prev_block = pychain.chain[-1]
    prev_block_hash = prev_block.hash_block()

    # Create new record
    new_record = RecordData(sender, receiver, amount)

    # Update new block with new record
    new_block = Block(creator_id=42, prev_hash=prev_block_hash, record=new_record)

    # Add new block to chain
    pychain.add_block(new_block)

    # Show success message
    st.write("New block added to chain.")
    st.balloons()

st.markdown("## The PyChain Ledger")

pychain_df = pd.DataFrame(pychain.chain).astype(str)
st.write(pychain_df)

difficulty = st.sidebar.slider("Block Difficulty", 1, 5, 2)
pychain.difficulty = difficulty

st.sidebar.write("# Block Inspector")
selected_block = st.sidebar.selectbox(
    "Which block would you like to see?", pychain.chain
)

st.sidebar.write(selected_block)

if st.button("Validate Chain"):
    st.write(pychain.is_valid())