from flask import Flask, request, jsonify
from opencc import OpenCC
import os

app = Flask(__name__)
cc = OpenCC('s2t')  # 簡體轉繁體

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json(force=True)
    text = data.get('text', '')

    # 假設 text 是一包 list[dict]，每個都有 content 欄位
    if isinstance(text, list) and isinstance(text[0], dict) and "content" in text[0]:
        converted = [cc.convert(item["content"]) for item in text]
        return jsonify({"traditional": converted})

    # 原始單句字串處理邏輯
    elif isinstance(text, list):
        text = ' '.join(map(str, text))
    converted = cc.convert(text)
    return jsonify({"traditional": converted})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
