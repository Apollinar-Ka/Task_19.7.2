import requests
import json

class PetFriends:
    """API-библиотека к веб-приложению Pet Friends"""

    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    def get_api_key(self, email: str, password: str) -> json:
        """GET-метод, отправляет запрос к API сервера с указанными email и паролем, в ответ получает
        статус запроса и API key в формате json"""

        headers = {
            "email": email,
            "password": password
        }
        res = requests.get(self.base_url+"api/key", headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str = "") -> json:
        """GET-метод, отправляет запрос к API сервера с указанными API key и значением фильтра,
        в ответ получает статус запроса и результат в формате json, соответствующий заданным параметрам.
        Фильтр принимает 2 значения:
        1) пустое значение (результат - получение списка всех питомцев);
        2) "my_pets" (результат - получение списка своих питомцев)"""

        headers = {"auth_key": auth_key['key']}
        filter = {"filter": filter}
        res = requests.get(self.base_url+"api/pets", headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str, age: int, pet_photo: str) -> json:
        """POST-метод отправляет на сервер данные о новом питомце, затем возвращает статус запроса
        и результат в формате json с данными добавленного питомца"""

        headers = {"auth_key": auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
        }
        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}
        res = requests.post(self.base_url+"api/pets", headers=headers, data=data, files=file)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """DELETE-метод отправляет на сервер запрос на удаление питомца по указанному ID и возвращает
        статус запроса и результат в формате JSON с текстом уведомления о успешном удалении"""

        headers = {"auth_key": auth_key['key']}
        res = requests.delete(self.base_url+"api/pets/"+pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: int) -> json:
        """PUT-Метод отправляет запрос на сервер о обновлении данных питомуа по указанному ID и
        возвращает статус запроса и результат в формате json с обновлённыи данными питомца"""

        headers = {"auth_key": auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
        }
        res = requests.put(self.base_url+"api/pets/"+pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_new_pet_without_photo(self, auth_key: json, name: str, animal_type: str, age: int) -> json:
        """POST-метод отправляет на сервер данные о новом питомце без фото-файла, затем возвращает статус запроса
        и результат в формате json с данными добавленного питомца"""

        headers = {"auth_key": auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
        }
        res = requests.post(self.base_url + "api/create_pet_simple", headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_photo_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """POST-метод отправляет на сервер файл с изображение питомца по его ID, затем возвращает статус запроса
        и результат в формате json с обновленными данными питомца"""

        headers = {"auth_key": auth_key['key']}
        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}
        res = requests.post(self.base_url+"api/pets/set_photo/"+pet_id, headers=headers, files=file)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result