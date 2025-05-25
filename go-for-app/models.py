import numpy as np
import onnxruntime
from flask import Flask, request, jsonify

app = Flask(__name__)

# 加载 ONNX 模型
model_path = "models/voice_model.onnx"
session = onnxruntime.InferenceSession(model_path)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    input_data = np.array(data['input'], dtype=np.int32)
    
    # 运行模型
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    result = session.run([output_name], {input_name: input_data})
    
    return jsonify({"output": result.tolist()})

if __name__ == '__main__':
    app.run(port=5001)