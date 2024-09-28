import random
import string

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/GenerateStrsByRule', methods=['POST'])
def generate_strings():
    # 获取请求参数，并设置默认值
    data = request.get_json()
    length_range = data.get('lengthRange', [8, 64])
    allowed_characters = data.get('allowedCharacters', ["Chinese", "LowerLetter", "UpperLetter", "Digits", "-_"])
    prohibited_characters = data.get('prohibitedCharacters', string.punctuation + string.whitespace)
    prohibited_prefix = data.get('prohibitedPrefix', '-')
    prohibited_suffix = data.get('prohibitedSuffix', '-')
    least_combine_nums = data.get('leastCombineNums', 3)

    # 调用函数生成字符串
    right, wrong = generate_all_combines_by_rules(
        length_range=length_range,
        allowed_characters=allowed_characters,
        prohibited_characters=prohibited_characters,
        prohibited_prefix=prohibited_prefix,
        prohibited_suffix=prohibited_suffix,
        least_combine_nums=least_combine_nums
    )

    # 返回结果
    return jsonify({
        'right_strings': right,
        'wrong_strings': wrong
    })


# 生成所有符合输入规范规则的字符串组合
def generate_all_combines_by_rules(length_range, allowed_characters, prohibited_characters, prohibited_prefix, prohibited_suffix, least_combine_nums):
    """
        :param length_range: 输入字符长度范围
        :param allowed_characters: 允许输入的字符列表组合，比如["Chinese", "LowerLetter", "UpperLetter", "Digits", "-_"]
        :param prohibited_characters: 禁止输入的字符列表组合
        :param prohibited_prefix: 禁止输入的前缀组合
        :param prohibited_suffix: 禁止输入的后缀组合
        :param least_combine_nums: 输入字符组合
        :return: 正确字符串组合和错误字符串组合
    """
    lst, dct = convert_characters_to_list(allowed_characters)
    right_all_characters = []
    n = len(lst)
    for k in range(least_combine_nums, n + 1):
        res = []
        back_trace(n, k, [], 1, res)
        right_all_characters.extend(res)
    print("right_all_characters is ", right_all_characters)

    all_right_strs = []
    partial_wrong_strs = []
    fix = ""
    for k, v in dct.items():
        if v == 5:
            fix = k

    for l in right_all_characters:
        s = ""
        for _, val in enumerate(l):
            if val == 1:
                s += generate_random_chinese_str(50)
            elif val == 2:
                s += string.ascii_lowercase
            elif val == 3:
                s += string.ascii_uppercase
            elif val == 4:
                s += string.digits
            elif val == 5:
                for k, v in dct.items():
                    if v == 5:
                        s += k

        for str_len in [length_range[0], length_range[1], (length_range[1] - length_range[0]) // 2]:
            s1 = generate_random_str(s, str_len)
            # 长度、前后缀、字符组合种类符合规则
            if (s1[0] not in prohibited_prefix and s1[0] not in prohibited_suffix ) and (s1[-1] not in prohibited_prefix and s1[-1] not in prohibited_suffix):
                all_right_strs.append(s1)
            else:
                # 字符串前后缀不符合规则
                partial_wrong_strs.append(s1)

        # 字符串长度不符合规范
        l1 = 0
        if length_range[0] - 1 >= 0:
            l1 = length_range[0] - 1

        for str_len in [l1, length_range[1] + 1]:
            s1 = generate_random_str(s, str_len)

            if s1[0] not in fix and s1[-1] not in fix:
                partial_wrong_strs.append(s1)

    # 字符串种类不符合规范
    missed_partial_characters = []
    n = len(lst)
    for k in range(1, least_combine_nums):
        res = []
        back_trace(n, k, [], 1, res)
        missed_partial_characters.extend(res)
    print("missed_partial_characters is ", missed_partial_characters)

    for l in missed_partial_characters:
        s = ""
        for _, val in enumerate(l):
            if val == 1:
                s += generate_random_chinese_str(50)
            elif val == 2:
                s += string.ascii_lowercase
            elif val == 3:
                s += string.ascii_uppercase
            elif val == 4:
                s += string.digits
            elif val == 5:
                for k, v in dct.items():
                    if v == 5:
                        s += k

        s1 = generate_random_str(s, (length_range[1] - length_range[0]) // 2)
        # 字符组合种类不符合规则
        if s1[0] not in fix and s1[-1] not in fix:
            partial_wrong_strs.append(s1)

    # 生成含有禁止输入的特殊字符和前后缀
    for i in [length_range[0], length_range[1]]:
        # 禁止输入的特殊字符
        s = generate_random_str(prohibited_characters, i)
        # 禁止输入的前后缀
        s1 = prohibited_prefix[0] + generate_random_str(string.ascii_letters + string.digits, i - 1)
        s2 = generate_random_str(string.ascii_letters + string.digits, i - 1) + prohibited_suffix[0]
        partial_wrong_strs.append(s)
        partial_wrong_strs.append(s1)
        partial_wrong_strs.append(s2)

    return all_right_strs, partial_wrong_strs


# 将字符转换为数组列表
def convert_characters_to_list(characters):
    lst = []
    if len(characters) == 0 or characters is None:
        return lst
    dct = {}

    for ch_str in characters:
        if ch_str == 'Chinese':
            lst.append(1)
            dct["Chinese"] = 1

        elif ch_str == 'LowerLetter':
            lst.append(2)
            dct["LowerLetter"] = 2

        elif ch_str == 'UpperLetter':
            lst.append(3)
            dct["UpperLetter"] = 3

        elif ch_str == "Digits":
            lst.append(4)
            dct["Digits"] = 4
        else:
            lst.append(5)
            dct[ch_str] = 5

    return lst, dct


# 列出字符间所有组合排列
def combine_character(start, lst):
    res = []
    n = len(lst)
    for k in range(start, n + 1):
        temp = []
        back_trace(n, k, [], 1, temp)
        res.extend(temp)
    return res


# 生成基本汉字的随机中文字符串
def generate_random_chinese_str(length=10):
    # 定义中文字符集范围（基本汉字）
    start = ord('\u4e00')
    end = ord('\u9fa5')

    # 生成随机字符串
    random_string = ''
    for _ in range(length):
        random_char = chr(random.randint(start, end))
        random_string += random_char

    return random_string


def generate_random_str(s, length):
    # 生成随机字符串

    random_string = ''.join(random.choices(s, k=length))
    return random_string


# 回溯算法，求解数组所有组合
def back_trace(n, k, nums, index, res_all):
    if len(nums) == k:
        res_all.append(nums[:])
        return

    for i in range(index, n + 1):
        nums.append(i)
        back_trace(n, k, nums, i + 1, res_all)
        nums.pop()

@app.route('/GenerateWrongDataType', methods=['POST'])
def generate_wrong_data():
    # 获取请求参数，并设置默认值
    data = request.get_json()
    data_type = data.get('dataType', "str")

    # 调用函数生成字符串
    res = generate_wrong_data_type(
        data_type=data_type
    )

    # 返回结果
    return jsonify({
        "wrong_data_types": res
    })


def generate_wrong_data_type(data_type):
    """
    根据输入数据类型，返回非该数据类型的数据类型列表
    :param data_type: 输入数据类型
    :return: 非该数据类型的数据类型列表
    """

    # 如果输入是字符串类型，则输出其他类型
    if isinstance(data_type, str):
        return [[1, 2, 3], (1,), {"data": 9}, list({1}), 8]
    elif isinstance(data_type, list):
        return ["abbc", (1,), {"data": 9}, list({1}), 8]
    elif isinstance(data_type, tuple):
        return ["abbc", [1, 2, 3], {"data": 9}, list({1}), 8]
    elif isinstance(data_type, dict):
        return ["abbc", [1, 2, 3], (1,), list({1}), 8]
    elif isinstance(data_type, set):
        return ["abbc", [1, 2, 3], (1,), {"a":"b"}, 8]
    elif isinstance(data_type, int):
        return [[1, 2, 3], "ssss", (1,), {"a":"b"}, list({1})]
    else:
        return []


if __name__ == '__main__':
    app.run(debug=True)