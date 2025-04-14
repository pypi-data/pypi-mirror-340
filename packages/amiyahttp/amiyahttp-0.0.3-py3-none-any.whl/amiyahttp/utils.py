import re
import os
import random
import string


def create_dir(path: str, is_file: bool = False):
    if is_file:
        path = os.path.dirname(path)

    if path and not os.path.exists(path):
        os.makedirs(path)

    return path


def pascal_case_to_snake_case(camel_case: str):
    snake_case = re.sub(r'(?P<key>[A-Z])', r'_\g<key>', camel_case)
    return snake_case.lower().strip('_')


def snake_case_to_pascal_case(snake_case: str):
    words = snake_case.split('_')
    return ''.join(word.title() if i > 0 else word.lower() for i, word in enumerate(words))


def generate_random_string(length: int = 16):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string
