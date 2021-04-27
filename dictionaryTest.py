test_dict = {}
test_dict_list = []

test_dict['a'] = 'seoul'
test_dict_list.append(test_dict)

print(test_dict_list)

test_dict['a'] = 'busan'
test_dict_list.append(test_dict.copy())

print(test_dict_list)
