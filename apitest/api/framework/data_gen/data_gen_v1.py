import abc
import random
import string
import re


def generate_valid_data(nums):
    """生成符合规则的正向数据"""
    """规则如下
        长度在2到64之间。
        只允许数字、大写字母、小写字母、下划线和中划线。
        下划线和中划线不能出现在首尾。
        不能包含特殊字符。
    """
    valid_data = []
    for _ in range(nums):  # 生成10个示例
        length = random.randint(2, 64)
        first_char = random.choice(string.ascii_letters + string.digits)
        last_char = random.choice(string.ascii_letters + string.digits)
        middle_chars = ''.join(random.choices(string.ascii_letters + string.digits + '_-', k=length-2))
        valid_str = first_char + middle_chars + last_char
        if is_valid(valid_str):
            valid_data.append(valid_str)
        else:
            continue

    return valid_data


def generate_invalid_data():
    """生成违反规则的异常数据"""
    invalid_data = []

    # 长度不在2-64之间
    invalid_data.append("A")
    invalid_data.append('A' * 65)

    # 包含特殊字符
    invalid_data.append("A!@#")

    # 下划线和中划线出现在首尾
    invalid_data.append("_Abc")
    invalid_data.append("Abc_")

    # 全部是非法字符
    invalid_data.append("!@#$%^&*()")

    return invalid_data



def is_valid(data):
    """校验数据是否符合规则"""
    pattern = r'^(?![-_])(?:[A-Z]+|[a-z]+|[0-9]+|[-_]+){2,}(?:[A-Z]+|[a-z]+|[0-9]+){1,}(?<![-_])$'
    if re.match(pattern, data):
        # 检查长度是否在2到64之间
        if 2 <= len(data) <= 64:
            # 检查是否至少包含3种不同的字符类型
            rule1 = (any(c.isupper() for c in data) and any(c.islower() for c in data) and any(
                c.isdigit() for c in data) or (any(c in '_-' for c in data)))
            rule2 = (any(c.isupper() for c in data) or any(c.islower() for c in data) and any(
                c.isdigit() for c in data) and (any(c in '_-' for c in data)))
            rule3 = (any(c.isupper() for c in data) and any(c.islower() for c in data) or any(
                c.isdigit() for c in data) and (any(c in '_-' for c in data)))
            rule4 = (any(c.isupper() for c in data) and any(c.islower() for c in data) and any(
                c.isdigit() for c in data) and (any(c in '_-' for c in data)))
            if rule1 or rule2 or rule3 or rule4:
                return True
    return False


def generate_wrong_type_data(input):
    """
    根据输入类型，生成错误的数据类型
    :param input:
    :return:
    """

    if isinstance(input, str):
        return [[1, 2, 3], (1,), {"data": 9}, {1}, 8]
    elif isinstance(input, list):
        return ["abbc", (1,), {"data": 9}, {1}, 8]
    elif isinstance(input, tuple):
        return ["abbc", [1, 2, 3], {"data": 9}, {1}, 8]
    elif isinstance(input, dict):
        return ["abbc", [1, 2, 3], (1,), {1}, 8]
    elif isinstance(input, set):
        return ["abbc", [1, 2, 3], (1,), {"a":"b"}, 8]
    elif isinstance(input, int):
        return [[1, 2, 3], "ssss", (1,), {"a":"b"}, {9}]
    else:
        return []

def generate_random_string(prefix, length, use_digits=True):
    characters = ''
    if use_digits:
        characters += string.digits
    characters += string.ascii_lowercase  # 小写字母总是包括在内

    random_string = prefix + ''.join(random.choice(characters) for _ in range(length))
    return random_string


def generate_name_data():
    para_name_test_data = []
    name_valid_data = generate_valid_data(nums=10)
    new_name_valid_data = []
    for i, val in enumerate(name_valid_data):
        if is_valid(val):
            new_name_valid_data.append(val)
            para_name_test_data.append((val, "Valid"))
    name_invalid_data = generate_invalid_data()
    for i, val in enumerate(name_invalid_data):
        para_name_test_data.append((val, "Invalid"))
    name_wrong_type = generate_wrong_type_data("name")
    for i, val in enumerate(name_wrong_type):
        para_name_test_data.append((val, "WrongType"))
    return para_name_test_data


if __name__ == "__main__":
    data = generate_name_data()
    for d in data:
        print(d)