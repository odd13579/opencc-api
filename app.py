from flask import Flask, request, jsonify
from opencc import OpenCC

app = Flask(__name__)
cc = OpenCC('s2t')  # 簡體轉繁體

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    text = data.get('text', '')
    converted = cc.convert(text)
    return jsonify({"traditional": converted})

if __name__ == '__main__':
    app.run()
