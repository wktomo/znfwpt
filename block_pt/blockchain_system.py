from flask import Flask, request, jsonify
import binascii
import json
import time
import logging

# 引入钱包模块
from aihymk import Wallet
# 引入区块链核心模块
from core_mk import Blockchain
# 引入数据存储模块
from sql_mk import init_db, save_block, fetch_block

# 初始化 Flask 应用
app = Flask(__name__)

# 初始化钱包
wallet = Wallet()
public_key_hex = binascii.hexlify(wallet.public_key.to_string()).decode()

# 初始化区块链
blockchain = Blockchain(difficulty=4)

# 初始化数据库
init_db()


@app.route('/')
def index():
    return "Welcome to the Blockchain System!"


@app.route('/wallet/public_key', methods=['GET'])
def get_public_key():
    """获取当前节点的钱包公钥"""
    return jsonify({"public_key": public_key_hex})


@app.route('/transaction', methods=['POST'])
def add_transaction():
    """添加交易到待处理列表"""
    data = request.json
    transaction = {
        "data": data,
        "public_key": public_key_hex,
        "signature": wallet.sign_transaction(json.dumps(data, sort_keys=True))
    }
    if blockchain.add_transaction(transaction):
        return jsonify({"message": "Transaction added successfully"})
    return jsonify({"message": "Invalid transaction"}), 400


@app.route('/mine', methods=['GET'])
def mine():
    """挖矿：处理待处理的交易并生成新区块"""
    if blockchain.mine_pending_transactions():
        # 保存新区块到数据库
        last_block = blockchain.chain[-1]
        save_block(last_block)
        return jsonify({"message": "Block mined successfully"})
    return jsonify({"message": "No transactions to mine"})


@app.route('/chain', methods=['GET'])
def get_chain():
    """获取当前区块链的状态"""
    chain_data = [block.__dict__ for block in blockchain.chain]
    return jsonify({"chain": chain_data})


@app.route('/block/<int:index>', methods=['GET'])
def get_block(index):
    """根据索引获取区块"""
    block = fetch_block(index)
    if block:
        return jsonify(block._asdict())
    return jsonify({"message": "Block not found"}), 404


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    app.run(debug=True, port=5000)