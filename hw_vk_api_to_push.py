import requests
from pprint import pprint
import time

# не понимал, почему выдавались ошибки, на сайте ВК работало, выяснил. что нужно было создать токен с болшими правами
SUPER_TOKEN = 'токен преподавателя с доступом к просмотру друзей'


# экземпляры класса будут создаваться с именем по принципу 'id'+id_пользователя (id7777777, например)
class VkUser:

    # словарь вида {Имя_переменной: {id, name, surname}} будет хранить данные о всех экземплярах и их параметрах
    users = {}
    url = 'http://api.vk.com/method/'

    def __init__(self, token, version, user_id):
        self.token = token
        self.version = version
        self.user_id = user_id
        self.params = {
            'access_token': self.token,
            'v': self.version
        }

        # получаем данные о пользователе, имя, фамилию, делаем задержку, а то ВК ругается на частые запросы
        time.sleep(0.5)
        self.user_info = requests.get(self.url + 'users.get',
                                      params={**self.params, 'user_ids': self.user_id}).json()['response'][0]
        self.name = self.user_info['first_name']
        self.surname = self.user_info['last_name']

        # добавляем данные о созданном пользователе в словарь {имя_глобальной_переменной: {id, name, surname}}
        VkUser.users.setdefault('id' + str(self.user_id),
                                {'id': self.user_id, 'name': self.name, 'surname': self.surname})
        print(f'Создаю пользователя {self.name} {self.surname}, id = {self.user_id}')

    def __and__(self, other):
        if not isinstance(other, VkUser):
            print('Ошибика - это не экземпляр пользователя VkUser')
        else:
            print(f'\nИщу общих друзей между {self.name} {self.surname} и {other.name} {other.surname}...')
            other_id = other.user_id
            friend_url = self.url + 'friends.getMutual'
            friend_params = {
                'source_uid': self.user_id,
                'target_uid': other_id
            }
            time.sleep(0.5)
            res = requests.get(friend_url, params={**self.params, **friend_params}).json()
            if res['response']:
                print(f"Найдены общие друзья со следующими ID: {res['response']}")
                for user in res['response']:
                    # негерируем имя переменной вида id7777777 и создаем сам новый экземпляр класса
                    new_user_name = 'id' + str(user)
                    globals()[new_user_name] = VkUser(SUPER_TOKEN, '5.126', user)
            else:
                print(f'Общих друзей с {other.name} {other.surname} не найдено!')
            return res

    def __str__(self):
        owner_url = self.url + 'users.get'
        owner_params = {
            'user_id': self.user_id,
            'order': 'hints',
            'fields': 'domain'
        }
        time.sleep(0.5)
        response = requests.get(owner_url, params={**self.params, **owner_params}).json()['response'][0]['domain']
        url = 'Ссылка на страницу пользователя: http://vk.com/' + response
        return url


# ИСПЫТАНИЯ
id6851258 = VkUser(SUPER_TOKEN, '5.126', 6851258)           # создаем аккауны людей с общими пользователями
id219059 = VkUser(SUPER_TOKEN, '5.126', 219059)

id6851258 & id219059                                        # ищем общих друзей

id1 = VkUser(SUPER_TOKEN, '5.126', 1)                       # создаем аккаунт Павла Дурова

id6851258 & id1                                             # ищем общих друзей

print(id1)                                                  # печатаем ссылку на страницу


# вывожу проверочную информация для проверки словаря с пользователями и глобальные переменные с экземплярами класса
print('\nВывожу для визуализаци словарь с пользователями:')
pprint(VkUser.users)
print('\nВывожу для проверки глобальные переменные:')
pprint(globals())
