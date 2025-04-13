import pytest
import random
import time
from faker import Faker

#import os, sys
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sort_by_average.sort_by_average import *

LENGHT_OF_TESTED_ELEMENT = 10000
MODULE_NAME = "test_func"
FUNCTION_NAME = "with_args"
FUNCTION_NAME_WITH_I = "with_args_with_i"

DICT_KEY_VALUE = "value_to_sort"
DICT_KEY_INDEX = "index_to_find"

TUPLE_KEY_INDEX = 1
TUPLE_KEY_VALUE = 2

#internal use
def check_if_sorted(data:list, id_desc = False):
    for idx, element in enumerate(data):
        if idx == 0:
            continue
        
        if id_desc:
            if data[idx - 1] > element:
                return True
        else:
            if data[idx - 1] > element:
                return False
        
    return True

#Testing list of integers
def test_sort_by_average_list_of_int():
    data = np.random.randint(1,999999,LENGHT_OF_TESTED_ELEMENT)
    sort_by_average = SortByAverage(arr = data.tolist())
    arr = sort_by_average.sort()
    assert check_if_sorted(arr) == True
    
#Testing list of integers with index
def test_sort_by_average_list_of_int_with_index():
    data = np.random.randint(1,999999,LENGHT_OF_TESTED_ELEMENT)
    sort_by_average = SortByAverage(arr = data.tolist(), is_index = True)
    arr = sort_by_average.sort()
    arr_to_check = [value for _, value in arr]
    assert check_if_sorted(arr_to_check) == True
    
#Testing with empty list
def test_sort_by_average_list_of_empty_list():
    with pytest.raises(AttributeError) as exec_info:
        SortByAverage(arr = [])
    assert "Missing data to sort" in str(exec_info.value)

#Testing with data wich class does not support (for now)
def test_sort_by_average_list_of_unsupported_data():
    data = np.random.randint(1,999999,LENGHT_OF_TESTED_ELEMENT)
    with pytest.raises(AttributeError) as exec_info:
        SortByAverage(arr = data)
    assert "issing data to sort" in str(exec_info.value)

#Testing with data containing one element
def test_sort_by_average_string():
    with pytest.raises(TypeError) as exec_info:
        SortByAverage(arr = "data")
    assert "Unsupported data type in input array" in str(exec_info.value)
    
#Testing with list of one int
def test_sort_with_one_int():
    sort_by_average = SortByAverage(arr = [1])
    arr = sort_by_average.sort()
    assert check_if_sorted(arr) == True

#Testing with list containing duplicate int
def test_sort_with_duplicate_int():
    base_data = []
    for _ in range(int(LENGHT_OF_TESTED_ELEMENT / 4)):
        base_data.append(random.randint(1, 999999))
    
    data = []
    for _ in range(4):
        data.extend(base_data)
    
    sort_by_average = SortByAverage(arr = data, is_index = True)
    arr = sort_by_average.sort()
    arr_to_check = [value for _, value in arr]
    assert check_if_sorted(arr_to_check) == True
    
#Testing with list of dicts
def _prepare_dict(is_express = False):
    data = []
    used_inexes = []
    divide_element = 100 if is_express else 10
    for _ in range(int(LENGHT_OF_TESTED_ELEMENT / divide_element)):
        template = {}
        template[DICT_KEY_VALUE] = random.randint(1, 999999)
        template["timestamp"] = time.time()
        template["random_sentence"] = Faker().sentence(nb_words = random.randint(5, 10))
        while True:
            index = random.randint(1, 999999)
            if index not in used_inexes:
                used_inexes.append(index)
                template[DICT_KEY_INDEX] = index
                break
        data.append(template)
    return data

def _prepare_values_from_dict_to_check(data):
    data_count = {}
    for element in data:
        value = element[DICT_KEY_VALUE]
        index = element[DICT_KEY_INDEX]
        data_count.setdefault(value, set()).add(index)
    return data_count

def _compare_dicts(d1, d2):
    if d1.keys() != d2.keys():
        return False
    for key in d1:
        if d1[key] != d2[key]:
            return False
    return True

#Testing with list of dicts
def test_sort_with_list_of_dict():
    data = _prepare_dict()
    sort_by_average = SortByAverage(arr = data, dict_key_value = DICT_KEY_VALUE, dict_key_index = DICT_KEY_INDEX, is_index = True)
    arr = sort_by_average.sort()
    
    dict_1 = _prepare_values_from_dict_to_check(data)
    data_count = {}
    for a in arr:
        data_count.setdefault(a[1], set()).add(a[0])
    _compare_dicts(dict_1, data_count)
    
    arr_to_check = [value for _, value in arr]
    assert check_if_sorted(arr_to_check) == True
    assert _compare_dicts(dict_1, data_count) == True
    assert len(data) == len(arr)
    
#Testing with list of dicts with wrong key_index
def test_sort_with_list_of_dict_wrong_index_key():
    data = _prepare_dict(is_express = True)
    with pytest.raises(KeyError) as exec_info:
        SortByAverage(arr = data, dict_key_value = DICT_KEY_VALUE, dict_key_index = "wrong_key", is_index = True)
    assert "Wrong index key passed in dict - no int value" in str(exec_info.value)
    
#Testing with list of dicts with wrong key value
def test_sort_with_list_of_dict_wrong_value_key():
    data = _prepare_dict(is_express = True)
    with pytest.raises(KeyError) as exec_info:
        SortByAverage(arr = data, dict_key_value = "wrong_key", dict_key_index = DICT_KEY_VALUE, is_index = True)
    assert "Wrong key to find value passed" in str(exec_info.value)
    
#Testing with list of dicts with no key_index
def test_sort_with_list_of_dict_no_index_key():
    data = _prepare_dict(is_express = True)
    with pytest.raises(KeyError) as exec_info:
        SortByAverage(arr = data, dict_key_value = DICT_KEY_VALUE)
    assert "No passed key to reach index from dict" in str(exec_info.value)
    
#Testing with list of dicts with no key value
def test_sort_with_list_of_dict_no_value_key():
    data = _prepare_dict(is_express = True)
    with pytest.raises(KeyError) as exec_info:
        SortByAverage(arr = data)
    assert "No passed key to reach value from dict" in str(exec_info.value)
    
#Testing with list of tuple - default index key
def test_sort_with_list_of_tuples():
    data = []
    for i in range(int(LENGHT_OF_TESTED_ELEMENT)):
        data.append((i, random.randint(1, 999999)))
    sort_by_average = SortByAverage(arr = data, is_index = True)
    arr = sort_by_average.sort()
    arr_to_check = [value for _, value in arr]
    assert check_if_sorted(arr_to_check) == True

#Testing with list of tuple - spcified index key
def test_sort_with_list_of_tuples_with_specified_keys():
    data = []
    for i in range(int(LENGHT_OF_TESTED_ELEMENT)):
        data.append((1, i, random.randint(1, 999999)))
    sort_by_average = SortByAverage(arr = data, is_index = True, tuple_key_index = TUPLE_KEY_INDEX, tuple_key_value = TUPLE_KEY_VALUE)
    arr = sort_by_average.sort()
    arr_to_check = [value for _, value in arr]
    assert check_if_sorted(arr_to_check) == True
    
#Testing list of integers - with descending
def test_sort_by_average_list_of_int_with_desc():
    data = np.random.randint(1,999999,LENGHT_OF_TESTED_ELEMENT)
    sort_by_average = SortByAverage(arr = data.tolist(), is_desc = True)
    arr = sort_by_average.sort()
    assert check_if_sorted(arr, True) == True
    
#Testing list of integers - with external function
def test_sort_by_average_list_of_int_with_external_func():
    data = np.random.randint(1,999999,LENGHT_OF_TESTED_ELEMENT)
    
    sort_by_average_without_func = SortByAverage(arr = data.tolist())
    arr_without_func = sort_by_average_without_func.sort()
    
    sort_by_average = SortByAverage(arr = data.tolist(), module_name = MODULE_NAME, function_name = FUNCTION_NAME)
    arr = sort_by_average.sort()
    
    check = True
    for awf, a in zip(arr_without_func, arr):
        if awf * 100 != a:
            check = False
    
    assert check == True
    
def test_sort_by_average_list_of_int_with_external_func_with_i():
    data = np.random.randint(1,999999,LENGHT_OF_TESTED_ELEMENT)
        
    sort_by_average = SortByAverage(arr = data.tolist(), module_name = MODULE_NAME, function_name = FUNCTION_NAME_WITH_I, is_i_called = True)
    sort_by_average.sort()
    
    assert True
    
#Testing with list of dicts - get original data
def test_sort_with_list_of_dict_with_get_origial_data():
    data = _prepare_dict(True)
    sort_by_average = SortByAverage(arr = data, dict_key_value = DICT_KEY_VALUE, dict_key_index = DICT_KEY_INDEX, is_index = True, module_name = MODULE_NAME, function_name = FUNCTION_NAME)
    arr = sort_by_average.sort()
    arr_to_check = [value for _, value in arr]
    original_data_sorted = sort_by_average.get_original_data_from_dict()
    check = True
    
    for a, o in zip(arr_to_check, original_data_sorted):
        print(a, o["calculated_value"])
        if a != o["calculated_value"]:
            check = False
    
    assert check == True 