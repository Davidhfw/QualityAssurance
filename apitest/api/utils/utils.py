import random
import string


def generate_random_string(prefix, length, use_uppercase=True, use_digits=True):
    characters = ''
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    characters += string.ascii_lowercase  # 小写字母总是包括在内

    random_string = prefix + ''.join(random.choice(characters) for _ in range(length))
    return random_string

