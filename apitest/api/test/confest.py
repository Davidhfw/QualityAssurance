
import pytest

from apitest.api.framework.data_gen import *
from apitest.api.framework.data_gen.data_gen_v1 import generate_valid_data, is_valid, generate_invalid_data, \
    generate_wrong_type_data


@pytest.fixture()
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
