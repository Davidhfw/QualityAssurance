import random
import string
import re

def generate_valid_data():
    """生成符合规则的正向数据"""
    valid_data = []
    for _ in range(10):  # 生成10个示例
        length = random.randint(2, 64)
        first_char = random.choice(string.ascii_letters)
        last_char = random.choice(string.ascii_letters)
        middle_chars = ''.join(random.choices(string.ascii_letters + string.digits + '_-', k=length-2))
        valid_str = first_char + middle_chars + last_char
        valid_data.append(valid_str)
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
    pattern = r"^[A-Za-z][A-Za-z0-9_-]*[A-Za-z]$"
    return bool(re.match(pattern, data)) and 2 <= len(data) <= 64


def generate_random_string(prefix, length, use_uppercase=True, use_digits=True):
    characters = ''
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    characters += string.ascii_lowercase  # 小写字母总是包括在内

    random_string = prefix + ''.join(random.choice(characters) for _ in range(length))
    return random_string