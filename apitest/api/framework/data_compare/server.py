import json

from flask import Flask, request, jsonify

app = Flask(__name__)


def ignore_fields_dict(d, ignore_list):
    """
    返回一个新的字典，忽略指定的字段。

    :param d: 输入字典
    :param ignore_list: 要忽略的字段列表
    :return: 处理后的字典
    """
    return {k: v for k, v in d.items() if k not in ignore_list}


@app.route('/CompareJsonData', methods=['POST'])
def compare_json_endpoint():
    # 获取请求中的数据
    data = request.get_json()

    # 确保请求包含必要的参数
    if not data or 'json1' not in data or 'json2' not in data:
        return jsonify({"error": "Missing 'json1' or 'json2' in request data"}), 400

    json1 = data['json1']
    json2 = data['json2']
    ignore_fields = data.get('ignore_fields', [])

    # 解析 JSON 字符串
    try:
        parsed_json1 = json.loads(json1)
        parsed_json2 = json.loads(json2)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format"}), 400

    # 忽略指定的字段
    ignored_json1 = ignore_fields_dict(parsed_json1, ignore_fields)
    ignored_json2 = ignore_fields_dict(parsed_json2, ignore_fields)

    # 比较两个字典
    is_equal = ignored_json1 == ignored_json2

    # 返回比较结果
    return jsonify({"result": is_equal})


if __name__ == "__main__":
    app.run(debug=True)
