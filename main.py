# from urllib.parse import urlencode
from pprint import pprint
import json
import requests
from tqdm import tqdm
from datetime import datetime

# pip freeze > requirements.txt
TOKEN_VK = 'vk1.a.0Qg7HQKsMIaEXRms886qrk8HfsVgqnnjEAjhwarSv32S4MoB4uA6u0Rh8Xv0sOHXjwxoZcGvFu_QS5m8J9u_1EFOsht73KU7B84y_K9-GeQhkL06LoPRCRVtWNPdClbBah3pgga1zJ4d1KzAZLgRs11JWel3upfvVWsrQ9GFVK3Zdxdz1ZskrSFFb95xl4pN-Y1tlcLqMcfkuU685U8vkg'

class VK_get_photos:
    def __init__(self, token, version='5.131'):
        self.token = token
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def get_photos(self):
        url_get_photos = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': user_id,
                      'album_id': 'profile',
                      'extended': '1',
                      'photo_sizes': '1',
                      'count': 50,                      
                      }
        responce = requests.get(url_get_photos, params={**self.params, **params}).json()
        return responce

    def best_size_photos(self):
        data = self.get_photos()
        photo_dict =  {}
        photo_json = {}
        photo_json_1 = {}
        for photo in tqdm(data['response']['items'], colour= 'green'):
            
            photo_url_max = max(photo['sizes'], key=lambda x: [x['height']])
            photo_url = photo_url_max['url']
            type_photo = photo_url_max['type']
            names_photo = photo['likes']['count']
            
            if names_photo in photo_dict.keys():
                
                photo_date = datetime.fromtimestamp(photo['date']).strftime('%d-%m-%Y')
                photo_dict[f"{names_photo}_{photo_date}"] =  photo_url
                photo_json['file_name'] = [f"{names_photo}_{photo_date}.jpg"]
                photo_json['size'] = type_photo
            else:
                photo_dict[names_photo] = photo_url
                photo_json['file_name'] = f'{names_photo}.jpg'
                photo_json['size'] = type_photo
        
            with open('photo.json', 'a') as file:
                json.dump(photo_json, file, indent=2)
                
        return photo_dict             
                 
class YADISK:
    def __init__(self, token):
        self.token = token
        self.headers = {'Content-Type': 'application/json',
                       'Authorization': self.token}

# Создание папки на Яндекс.Диск
    def put_folder(self):
        url_folder = 'https://cloud-api.yandex.net/v1/disk/resources/'       
        params = {'path': folder_name}
        responce = requests.put(url_folder, headers=self.headers, params=params) 
        if True:
            if responce.status_code == 409:
                return f'Папка {folder_name} уже создана создана, фотографии будут отправлены в нее'
            return f'Папка {folder_name} создана'
            
# Загрузка файла по URL Яндекс.Диск        
    def download_photo(self):
        for photo in tqdm(url_upload.items()):
            url_download = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
            params = {'path': f'{folder_name}/{photo[0]}', 'url': {photo[1]}}  
            res = requests.post(url_download, headers=self.headers, params=params) 
            
        if 200 <= res.status_code <=300:
            return f'Файлы загружены в папку {folder_name}'
        else:
            return f'Ошибка, {res.status_code}' 



user_id = input('Введите id пользователя VK для скачиваний фотографий профиля: ')    
vk_client = VK_get_photos(TOKEN_VK)
vk_client.get_photos() 
url_upload = vk_client.best_size_photos()

folder_YA = YADISK(input("Введите свой токен для Яндекс.Диска: "))
folder_name = input('Введите название папки для сохранения фотографий в Яндекс.Диске: ')

pprint(folder_YA.put_folder())
pprint(folder_YA.download_photo())


