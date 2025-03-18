from flask import Flask, request, jsonify, render_template
import time
import logging
import binascii
import json

# 引入钱包模块
from aihymk import Wallet
# 引入区块链核心模块
from core_mk import Blockchain
# 引入数据存储模块
from sql_mk import init_db, save_block, fetch_block

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 初始化 Flask 应用
app = Flask(__name__)

# 启用跨域支持
from flask_cors import CORS
CORS(app)

# 初始化钱包
wallet = Wallet()
public_key_hex = binascii.hexlify(wallet.public_key.to_string()).decode()

# 初始化区块链
blockchain = Blockchain(difficulty=4)

# 初始化数据库
init_db()


@app.route('/')
def index():
    """首页路由：返回欢迎信息"""
    return render_template('index.html')


@app.route('/wallet/public_key', methods=['GET'])
def get_public_key():
    """获取当前节点的钱包公钥"""
    logging.info("Public key requested")
    return jsonify({"public_key": public_key_hex})


@app.route('/transaction', methods=['POST'])
def add_transaction():
    """添加交易到待处理列表"""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid request data"}), 400

        # 构造交易数据
        transaction = {
            "data": data,
            "public_key": public_key_hex,
            "signature": wallet.sign_transaction(json.dumps(data, sort_keys=True))
        }

        # 添加交易到区块链
        if blockchain.add_transaction(transaction):
            logging.info(f"Transaction added: {transaction}")
            return jsonify({"message": "Transaction added successfully"})
        else:
            logging.warning("Invalid transaction")
            return jsonify({"error": "Invalid transaction"}), 400

    except Exception as e:
        logging.error(f"Error adding transaction: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/mine', methods=['GET'])
def mine():
    """挖矿：处理待处理的交易并生成新区块"""
    try:
        if blockchain.mine_pending_transactions():
            logging.info("Block mined successfully")
            return jsonify({"message": "Block mined successfully"})
        else:
            logging.info("No transactions to mine")
            return jsonify({"message": "No transactions to mine"})
    except Exception as e:
        logging.error(f"Error during mining: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/chain', methods=['GET'])
def get_chain():
    """获取当前区块链的状态"""
    try:
        chain_data = [block.__dict__ for block in blockchain.chain]
        logging.info("Blockchain data requested")
        return jsonify({"chain": chain_data})
    except Exception as e:
        logging.error(f"Error fetching blockchain data: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/block/<int:index>', methods=['GET'])
def get_block(index):
    """根据索引获取区块"""
    try:
        block = next((block for block in blockchain.chain if block.index == index), None)
        if block:
            logging.info(f"Block {index} requested")
            return jsonify(block.__dict__)
        else:
            logging.warning(f"Block {index} not found")
            return jsonify({"error": "Block not found"}), 404
    except Exception as e:
        logging.error(f"Error fetching block {index}: {e}")
        return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    logging.info("Starting Blockchain Node...")
    app.run(debug=True, port=5000)
logging.info("Received transaction request")
# 在link_web.py中添加以下代码

# 引入必要的模块
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

users = {}

@app.route('/auth/register', methods=['POST'])
def register():
    """用户注册"""
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"error": "用户名和密码是必填项"}), 400

        if username in users:
            return jsonify({"error": "用户名已存在"}), 400

        hashed_password = generate_password_hash(password)
        users[username] = {
            'password': hashed_password,
            'id': str(uuid.uuid4())
        }

        return jsonify({"message": "注册成功", "username": username}), 201

    except Exception as e:
        logging.error(f"Error during registration: {e}")
        return jsonify({"error": "Internal server error"}), 500