import jproperties

""" .properties 파일 읽기 테스트 """
property_reader = jproperties.Properties()

# with open('C:\\Users\\user\\Desktop\\inwoo\\PCWorkspace01\\python-test-project\\resources\\auth.properties', 'rb') as auth_properties:
#     property_reader.load(auth_properties)
auth_properties = open('../resources/auth.properties', 'rb')
property_reader.load(auth_properties)

print(property_reader.get('KOFIC_KEY'))
print(property_reader.get('KOFIC_KEY').data)

