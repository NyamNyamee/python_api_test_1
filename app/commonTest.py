import requests
import json
import jproperties
from urllib import parse

""" .properties 파일 읽기 테스트 """
# property_reader = jproperties.Properties()
#
# # with open('C:\\Users\\user\\Desktop\\inwoo\\PCWorkspace01\\python-test-project\\resources\\auth.properties', 'rb') as auth_properties:
# #     property_reader.load(auth_properties)
# auth_properties = open('../resources/auth.properties', 'rb')
# property_reader.load(auth_properties)
# auth_properties.close()
#
# print(property_reader.get('KOFIC_KEY'))
# print(property_reader.get('KOFIC_KEY').data)
#
""" 딕셔너리 테스트 """
# test_dict = {}
# test_dict_list = []
#
# test_dict['a'] = 'seoul'
# test_dict_list.append(test_dict)
# print(test_dict_list)
#
# test_dict['a'] = 'busan'
# test_dict_list.append(test_dict.copy())
# print(test_dict_list)

""" 심심이 챗봇 테스트 """
# headers = {
#     'Content-Type': 'application/json',
#     'x-api-key': '8LB7lnNM7BlDS37yI0JYsog63k9uYI_2ZlFT1yNJ',
# }
#
# # data = '{\n            "utext": "hello there", \n            "lang": "en" \n     }'
# data = {"utext": "hello there", "lang": "en"}
#
# response = requests.post('https://wsapi.simsimi.com/190410/talk', headers=headers, data=data)

# headers = {
#     'Content-Type': 'application/json',
#     'x-api-key': '8LB7lnNM7BlDS37yI0JYsog63k9uYI_2ZlFT1yNJ'
# }
#
# data = {
#     "utext": "안녕",
#     "lang": "ko"
# }
#
# response = requests.post('https://wsapi.simsimi.com/190410/talk', headers=headers, data=data)

# print(response.url)
# print(response.text)
# print(response.status_code)
#
# parsed_object = json.loads(response.text)
# answer_message = parsed_object['atext']
# print(answer_message)

""" urllib parse encoding test """
text = '안녕'
result = parse.quote(text)
print(result)
