import request
import json

url = "http://shuyantech.com/api/cndbpedia/avpair?q=硫酸"
response = request.get(url)
print(type(response.text))
json_content = json.loads(response.text)
print(type(json_content))
print(json_content['ret'])
for i in json_content['ret']:
    if i[0] == "DESC":
        print(i[1].replace("\n",""))