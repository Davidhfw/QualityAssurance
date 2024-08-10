import re


def validate_cluster_name(name):
    """
    验证名称是否合法。

    参数:
    name (str): 要验证的名称。

    返回:
    bool: 如果名称合法，返回True；否则返回False。
    """
    # 正则表达式解释：
    # ^ 表示字符串的开始
    # (?![_-]) 表示名称不能以下划线或中划线开头
    # (?<![-_]) 表示名称不能以下划线或中划线结尾
    # (?:[A-Z]+|[a-z]+|[0-9]+|[-_]+){2,} 表示名称至少包含两个字符，且可以包含大写字母、小写字母、数字、下划线和中划线
    # (?:[A-Z]+|[a-z]+|[0-9]+){1,} 表示名称至少包含一个大写字母、小写字母或数字
    # $ 表示字符串的结束
    pattern = r'^(?![-_])(?:[A-Z]+|[a-z]+|[0-9]+|[-_]+){2,}(?:[A-Z]+|[a-z]+|[0-9]+){1,}(?<![-_])$'

    # 使用正则表达式匹配名称
    if re.match(pattern, name):
        # 检查长度是否在2到64之间
        if 2 <= len(name) <= 64:
            # 检查是否至少包含3种不同的字符类型
            rule1 = (any(c.isupper() for c in name) and any(c.islower() for c in name) and any(c.isdigit() for c in name) or (any(c in '_-' for c in name)))
            rule2 = (any(c.isupper() for c in name) or any(c.islower() for c in name) and any(c.isdigit() for c in name) and (any(c in '_-' for c in name)))
            rule3 = (any(c.isupper() for c in name) and any(c.islower() for c in name) or any(c.isdigit() for c in name) and (any(c in '_-' for c in name)))
            rule4 = (any(c.isupper() for c in name) and any(c.islower() for c in name) and any(c.isdigit() for c in name) and (any(c in '_-' for c in name)))
            if rule1 or rule2 or rule3 or rule4:
                return True
    return False

def validate_cluster_desc(desc):
    """
    验证名称是否合法。

    参数:
    name (str): 要验证的名称。

    返回:
    bool: 如果名称合法，返回True；否则返回False。
    """
    # 正则表达式解释：
    # ^ 表示字符串的开始
    # (?![_-]) 表示名称不能以下划线或中划线开头
    # (?<![-_]) 表示名称不能以下划线或中划线结尾
    # (?:[A-Z]+|[a-z]+|[0-9]+|[-_]+){2,} 表示名称至少包含两个字符，且可以包含大写字母、小写字母、数字、下划线和中划线
    # (?:[A-Z]+|[a-z]+|[0-9]+){1,} 表示名称至少包含一个大写字母、小写字母或数字
    # $ 表示字符串的结束
    pattern = r'^(?![-_])(?:[A-Z]+|[a-z]+|[0-9]+|[-_]+){2,}(?:[A-Z]+|[a-z]+|[0-9]+){1,}(?<![-_])$'

    # 使用正则表达式匹配名称
    if re.match(pattern, desc):
        # 检查长度是否在2到64之间
        if 2 <= len(desc) <= 64:
            # 检查是否至少包含3种不同的字符类型
            if (any(c.isupper() for c in desc) and
                    any(c.islower() for c in desc) and
                    any(c.isdigit() for c in desc) and
                    (any(c in '_-' for c in desc))):
                return True
    return False
