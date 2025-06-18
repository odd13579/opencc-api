from flask import Flask, request, jsonify
from opencc import OpenCC
import os

app = Flask(__name__)
cc = OpenCC('s2t')  # 簡體轉繁體

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json(force=True)
    text = data.get('text', '')

    # ➤ 判斷 text 是 list 就逐筆轉換
    if isinstance(text, list):
        # 若是 list of dict 且含 content 欄位
        if all(isinstance(item, dict) and 'content' in item for item in text):
            converted = [cc.convert(item['content']) for item in text]
        else:
            # 一般 list of string 處理
            converted = [cc.convert(str(item)) for item in text]
    else:
        # 單一字串處理
        converted = cc.convert(str(text))

    return jsonify({"traditional": converted})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
