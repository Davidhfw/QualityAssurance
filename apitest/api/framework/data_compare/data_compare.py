import json

def compare_json(json1, json2, ignore_fields=[]):
    """
    比较两个 JSON 字符串，忽略指定的字段。

    :param json1: 第一个 JSON 字符串
    :param json2: 第二个 JSON 字符串
    :param ignore_fields: 要忽略的字段列表
    :return: 布尔值，表示两个 JSON 是否相同
    """
    def ignore_fields_dict(d, ignore_list):
        """
        返回一个新的字典，忽略指定的字段。

        :param d: 输入字典
        :param ignore_list: 要忽略的字段列表
        :return: 处理后的字典
        """
        return {k: v for k, v in d.items() if k not in ignore_list}

    # 解析 JSON 字符串
    parsed_json1 = json.loads(json1)
    parsed_json2 = json.loads(json2)

    # 忽略指定的字段
    ignored_json1 = ignore_fields_dict(parsed_json1, ignore_fields)
    ignored_json2 = ignore_fields_dict(parsed_json2, ignore_fields)

    # 比较两个字典
    return ignored_json1 == ignored_json2


if __name__ == "__main__":
    # 示例使用
    json1 = '{"name": "John", "age": 30, "city": "New York", "email": "john@example.com", "timestamp": "1234555"}'
    json2 = '{"name": "John", "age": 30, "city": "New York", "email": "john@example.com", "timestamp": "1234679000000"}'
    ignore_fields = ["email", "timestamp"]

    result = compare_json(json1, json2, ignore_fields)
    print(result)  # 输出: True
