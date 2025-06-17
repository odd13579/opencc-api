from flask import Flask, request, jsonify
from opencc import OpenCC
import os

app = Flask(__name__)
cc = OpenCC('s2t')  # 簡體轉繁體

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json(force=True)
    text = data.get('text', '')

    # 💥 防炸：如果收到 list，就 join 起來變成字串
    if isinstance(text, list):
        text = ' '.join(map(str, text))  # 把 list 裡的詞合成一行

    converted = cc.convert(text)
    return jsonify({"traditional": converted})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
