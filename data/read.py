import json

APP_NAME = 'recipes'


def read(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


data = read('ingredients.json')
data_id = 1
n_data = []

for arg in data:
    n_dict = {
      'model': APP_NAME + '.ingredient',
      'id': data_id,
      'fields': arg
    }
    n_data.append(n_dict)
    data_id += 1
with open('ingredients2.json', 'w', encoding='utf-8') as file:
    json.dump(n_data, file, ensure_ascii=False, indent=4)
