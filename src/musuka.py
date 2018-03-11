import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4
import json
from flask import Flask, jsonify, request


import blockchain

# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
bchain = blockchain.Blockchain()

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': bchain.chain,
        'length': len(bchain.chain),
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_trans():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    print(values)
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = bchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/mine', methods=['GET'])
def mineit():

    # We run the proof of work algorithm to get the next proof...
    last_block = bchain.last_block
    last_proof = last_block['proof']
    proof = bchain.proof_of_work(last_proof)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    bchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = bchain.hash(last_block)
    block = bchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    print(response)
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        bchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(bchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = bchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': bchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': bchain.chain
        }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)