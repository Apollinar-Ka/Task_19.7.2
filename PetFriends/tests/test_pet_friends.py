import os
from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()

# №1
def test_add_new_pet_without_photo_valid_data(name = 'Грек', animal_type = 'собака', age = 1):
    """Проверяем что можно добавить питомца с корректными данными без фото-файла"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

# №2
def test_successful_add_photo_pet(pet_photo = 'images/dog1.jpg'):
    """Проверяем что можно добавить к данным питомца файл с изображением"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового питомца без фото и запоминаем его ID
    if len(my_pets['pets']) == 0:
        _, new_pet = pf.add_new_pet_without_photo(auth_key, "Линда", "собака", 3)
        pet_id = new_pet['id']
    else:
        pet_id = my_pets['pets'][0]['id']

    status, result = pf.add_photo_pet(auth_key, pet_id, pet_photo)
    assert status == 200
    assert len(result['pet_photo']) > 0

# №3
def test_get_api_key_for_invalid_user(email='qo_05@qoqo.ru', password='987321456'):
    """ Проверяем что запрос api ключа возвращает статус 403, если введены
    невалидные данные для email или пароля"""

    status, result = pf.get_api_key(email, password)
    assert status == 403

# №4
def test_add_new_pet_without_photo_empty_data(name = '', animal_type = '', age = ''):
    """Проверяем что запрос на добавление питомца возвращает статус 400,
    если обязательные параметры имеют пустые значение """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 400

# №5
def test_add_new_pet_without_photo_invalid_data(name = 'Принц', animal_type = 'собака', age = "ываыва123"):
    """Проверяем, что запрос на добавление питомца возвращает статус 400, если в параметр age,
    который принимает только числовое значение, ввести текст"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 400

# №6
def test_get_list_of_pets_with_invalid_api_key(filter=''):
    """ Проверяем что запрос списка всех питомцев возвращает статус 403,
    если указан неверный ключ авторизации.
    Доступные значения параметра filter - 'my_pets' либо '' """

    auth_key = {'key': '123456789'}
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403

# №7
def test_get_list_of_my_pets_with_valid_user(filter='my_pets'):
    """ Проверяем что запрос возвращает список собственных питомцев,
    когда параметр filter имеет значение'my_pets' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    if len(result['pets']) == 0:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")
    else:
        assert status == 200

# №8
def test_unsuccessful_add_photo_pet(pet_photo = 'images/test_photo.txt'):
    """Проверяем, что запрос на добавление питомца возвращает статус 400,
    когда в параметр pet_photo загружаем невалидный файл"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового питомца без фото и запоминаем его ID
    if len(my_pets['pets']) == 0:
        _, new_pet = pf.add_new_pet_without_photo(auth_key, "Линда", "собака", 3)
        pet_id = new_pet['id']
    else:
        pet_id = my_pets['pets'][0]['id']

    status, result = pf.add_photo_pet(auth_key, pet_id, pet_photo)
    assert status == 400

# №9
def test_update_pet_info_with_invalid_data(name='Люся', animal_type='♣☺♂', age=5):
    """Проверяем, что запрос на добавление питомца возвращает статус 400,
    когда в параметр animal_type введены спец символы"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")
    else:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 400

# №10
def test_add_new_pet_with_invalid_data(animal_type = 'кошак', age = 10,
                                     pet_photo = 'images/kitty.jpg'):
    """Проверяем что запрос на добавление питомца возвращает статус 400, если параметр name
    имеет слишком большое значение """

    name = """Наборсимволовэтоуникальнаякомбинациясимволовиспользуемаядляпередачиинформациивпись
    меннойформеиливцифровомвидеВключаябуквыцифрызнакипунктуацииспециальныесимволыисимволыпробела
    наборсимволовпредставляетсобойосновудлясозданияиинтерпретациитекстанаразличныхязыкахисистемахзаписи
    Наборсимволовотличаетсявзависимостиотязыкаикодировкииспользуемойдляпредставлениясимволоввкомпьютерныхсистемах
    Напримерврусскомалфавитесодержится33буквыадляанглийскогоалфавита26буквВместестем
    русскийязыксодержитуникальныесимволытакиекакёиыкоторыеневстречаютсяванглийскомязыке
    СимволымогуттакжеиметьспециальноезначениевкомпьютерныхсистемахНапримерсимволытакиекакилиcom
    частоиспользуютсявадресахэлектроннойпочтыиURLадресахКодированиесимволовпозволяеткомпьютерным
    системамраспознаватьиобрабатыватьразличныесимволыдляпередачихраненияиотображенияинформации
    Наборсимволовиграетважнуюрольвсозданиииинтерпретациитекстанаразныхязыкахивразличныхконтекстах
    Благодаряемумыможемобщатьсяипередаватьинформациюспомощьюписьменнойкоммуникации
    Правильноеиспользованиенаборасимволовявляетсяключевымэлементомдляпониманияисвязимеждулюдьми
    такжедляэффективнойработыскомпьютернымисистемами"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400