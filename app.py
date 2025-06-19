from flask import Flask, request, jsonify
from opencc import OpenCC
import os
import re

app = Flask(__name__)
cc = OpenCC('s2t')  # 簡體轉繁體，只轉中文字用

# ✅ 只轉中文字，保留格式與非中文符號
def convert_only_chinese(text: str) -> str:
    def convert_match(match):
        return cc.convert(match.group(0))
    pattern = re.compile(r'[\u4e00-\u9fff]+')  # 中文 unicode 區段
    return pattern.sub(convert_match, text)

@app.route('/convert', methods=['POST'])
def convert():
    try:
        data = request.get_json(force=True)
        text = data.get('text', '')

        if not text:
            return jsonify({"traditional": "", "msg": "text 欄位為空"}), 200

        if isinstance(text, list):
            if all(isinstance(item, dict) and 'content' in item for item in text):
                converted = [convert_only_chinese(item['content']) for item in text]
            elif all(isinstance(item, str) for item in text):
                converted = [convert_only_chinese(item) for item in text]
            else:
                # 混亂格式或無法辨識的 list 結構
                return jsonify({"traditional": "", "msg": "list 結構格式錯誤"}), 400
        else:
            converted = convert_only_chinese(str(text))

        return jsonify({"traditional": converted}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
