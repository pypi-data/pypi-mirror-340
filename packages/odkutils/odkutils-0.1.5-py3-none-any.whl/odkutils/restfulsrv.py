from flask import Flask, request, jsonify
from .imgutils import get_clipboard_image_base64,get_clipboard_image_cids

app = Flask(__name__)
@app.route('/api/version', methods=['GET'])
def api_version():
    return jsonify({"msg":"获取成功","code":200,"version":"0.1.4"}), 200
    
@app.route('/api/get_clip_img_base64', methods=['POST'])
def api_get_clipimgbase64():
    try:
        # Call your original function
        data,err = get_clipboard_image_base64()
        if err is not None:
            return jsonify({"error": str(err),"msg":"获取失败","code":1001}), 200
        return jsonify({"msg":"获取成功","code":200,"data":data}), 200
    except Exception as e:
        return jsonify({"error": str(err),"msg":"获取失败","code":1001}), 200

@app.route('/api/get_clip_img_cids', methods=['POST'])
def api_get_clipimgcids():
    try:
        # Call your original function
        data,err = get_clipboard_image_cids()
        if err is not None:
            return jsonify({"error": str(err),"msg":"获取失败","code":1001}), 200
        return jsonify({"msg":"获取成功","code":200,"data":data}), 200
    except Exception as e:
        return jsonify({"error": str(err),"msg":"获取失败","code":1001}), 200
    
# 启动restful服务 
def start_restfulsrv(port=25751):
    
    app.run(host='0.0.0.0', port=port, debug=False)