import asyncio
import json
import logging
import requests
import os
from aiogram.client.session import aiohttp
from aiogram.types import Message
from bs4 import BeautifulSoup


logging.basicConfig(level=logging.INFO)


class AI:
    def __init__(self, parent):
        self.parent = parent
        self.done = set()
        self.pending = set()
        self.response = None
        self.dict_history = {}
        self.dict_history_src = {}
        self.dict_current_message = {}
        self.dict_current_progress = {}
        self.list_text = [
            'собираю информацию 🟩🟩',
            'собираю информацию 🟩🟩🟩',
            'собираю информацию 🟩🟩🟩🟩',
            'собираю информацию 🟩🟩🟩🟩🟩',
            'собираю информацию 🟩🟩🟩🟩🟩🟩',
            'собираю информацию 🟩🟩🟩🟩🟩🟩🟩',
            'собираю информацию 🟩🟩🟩🟩🟩🟩🟩🟩',
            'собираю информацию 🟩🟩🟩🟩🟩🟩🟩🟩🟩',
            'собираю информацию 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩',
            'собираю информацию 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩',
            'собираю информацию 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩',
            'собираю информацию 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩',
            'проверяю орфографию 🟩',
            'проверяю орфографию 🟩🟩',
            'проверяю орфографию 🟩🟩🟩',
            'проверяю орфографию 🟩🟩🟩🟩',
            'проверяю орфографию 🟩🟩🟩🟩🟩',
            'проверяю орфографию 🟩🟩🟩🟩🟩🟩',
            'проверяю орфографию 🟩🟩🟩🟩🟩🟩🟩',
            'проверяю орфографию 🟩🟩🟩🟩🟩🟩🟩🟩',
            'проверяю орфографию 🟩🟩🟩🟩🟩🟩🟩🟩🟩',
            'проверяю орфографию 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩',
            'проверяю орфографию 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩',
            'проверяю орфографию 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩',
            'проверяю орфографию 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩',
            'расставляю запятые 🟩',
            'расставляю запятые 🟩🟩',
            'расставляю запятые 🟩🟩🟩',
            'расставляю запятые 🟩🟩🟩🟩',
            'расставляю запятые 🟩🟩🟩🟩🟩',
            'расставляю запятые 🟩🟩🟩🟩🟩🟩',
            'расставляю запятые 🟩🟩🟩🟩🟩🟩🟩',
            'расставляю запятые 🟩🟩🟩🟩🟩🟩🟩🟩',
            'расставляю запятые 🟩🟩🟩🟩🟩🟩🟩🟩🟩',
            'расставляю запятые 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩',
            'расставляю запятые 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩',
            'расставляю запятые 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩',
            'расставляю запятые 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩',
            'создаю эмоции 🟩',
            'создаю эмоции 🟩🟩',
            'создаю эмоции 🟩🟩🟩',
            'создаю эмоции 🟩🟩🟩🟩',
            'создаю эмоции 🟩🟩🟩🟩🟩',
            'создаю эмоции 🟩🟩🟩🟩🟩🟩',
            'создаю эмоции 🟩🟩🟩🟩🟩🟩🟩',
            'создаю эмоции 🟩🟩🟩🟩🟩🟩🟩🟩',
            'создаю эмоции 🟩🟩🟩🟩🟩🟩🟩🟩🟩',
            'создаю эмоции 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩',
            'создаю эмоции 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩',
            'создаю эмоции 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩',
            'создаю эмоции 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩',
            'совсем чуть-чуть 🟩',
            'совсем чуть-чуть 🟩🟩',
            'совсем чуть-чуть 🟩🟩🟩',
            'совсем чуть-чуть 🟩🟩🟩🟩',
            'совсем чуть-чуть 🟩🟩🟩🟩🟩',
            'совсем чуть-чуть 🟩🟩🟩🟩🟩🟩',
            'совсем чуть-чуть 🟩🟩🟩🟩🟩🟩🟩',
            'совсем чуть-чуть 🟩🟩🟩🟩🟩🟩🟩🟩',
            'совсем чуть-чуть 🟩🟩🟩🟩🟩🟩🟩🟩🟩',
            'совсем чуть-чуть 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩',
            'совсем чуть-чуть 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩',
            'совсем чуть-чуть 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩',
            'совсем чуть-чуть 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩',
            'почти готово 🟩',
            'почти готово 🟩🟩',
            'почти готово 🟩🟩🟩',
            'почти готово 🟩🟩🟩🟩',
            'почти готово 🟩🟩🟩🟩🟩',
            'почти готово 🟩🟩🟩🟩🟩🟩',
            'почти готово 🟩🟩🟩🟩🟩🟩🟩',
            'почти готово 🟩🟩🟩🟩🟩🟩🟩🟩',
            'почти готово 🟩🟩🟩🟩🟩🟩🟩🟩🟩',
            'почти готово 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩',
            'почти готово 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩',
            'почти готово 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩',
            'почти готово 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩'
        ]

    async def answer_ai_message(self, query: str, message: Message):
        self.done = set()
        self.pending = set()
        self.response = None
        self.dict_current_progress[message.from_user.id] = 0
        self.dict_current_message[message.from_user.id] = await self.parent.answer_text(message, 'собираю информацию 🟩')
        token = await self.get_token()
        await self.add_user_query(message.from_user.id, query)
        response_ai = await self.get_dict_answer_ai(message.from_user.id, token["access_token"])
        if response_ai is None:
            arr_message = ["Ничего не нашел по этому поводу, попробуйте спросить по-другому..."]
        elif response_ai == 'New context':
            arr_message = ["Всё, я забыл, про что говорили..."]
        else:
            answer = response_ai['choices'][0]['message']['content']
            arr_message = await self.division_message(answer)
            await self.add_assistant_query(message.from_user.id, answer)
        return arr_message, self.dict_current_message

    async def answer_ai_image(self, query: str, message: Message):
        self.done = set()
        self.pending = set()
        self.response = None
        self.dict_current_progress[message.from_user.id] = 0
        self.dict_current_message[message.from_user.id] = await self.parent.answer_text(message, 'собираю информацию 🟩')
        token = await self.get_token()
        response = await self.get_dict_photo_ai(message.from_user.id, query, token["access_token"])
        if response is None:
            answer = "Не смог ничего нарисовать, пропало настроение"
        else:
            answer = response['choices'][0]['message']['content']
        try:
            src = BeautifulSoup(answer, 'html.parser').find('img')['src']
            if not os.path.exists("images"):
                os.mkdir("images")
            with open(f"images/{src}.jpeg", "wb+") as img_file:
                file_image = await self.get_img(src, token["access_token"])
                img_file.write(file_image)
            path_image = f"images/{src}.jpeg"
            await self.get_general_image(message.from_user.id, src)
        except TypeError:
            path_image = f"images/no_photo.jpeg"
        return answer, path_image, self.dict_current_message

    async def post_by_user_photo(self, query: str, path_user_foto: str, message: Message):
        self.done = set()
        self.pending = set()
        self.response = None
        self.dict_current_progress[message.from_user.id] = 0
        self.dict_current_message[message.from_user.id] = await self.parent.answer_text(message, 'собираю информацию 🟩')
        token = await self.get_token()
        info_user_photo = await self.post_photo_ai(path_user_foto, token["access_token"])
        response = await self.get_dict_photo_ai_with_user_image(message.from_user.id, query, info_user_photo,
                                                                token["access_token"])
        try:
            if response is None:
                answer = "Не смог написать текст, не до продаж сегодня"
            else:
                answer = response['choices'][0]['message']['content']
        except KeyError:
            answer = "Не смог написать текст, не до продаж сегодня"
        return answer, self.dict_current_message

    @staticmethod
    async def get_token():
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        payload = {
            'scope': os.environ["SCOPE_BUSINESS"]
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': os.environ["CLIENT_ID_BUSINESS"],
            'Authorization': f'Basic {os.environ["AUTHORIZATION_KEY_BUSINESS"]}'
        }
        response = requests.request("POST", url, headers=headers, data=payload, verify='chain.pem')
        return response.json()

    async def get_dict_model(self, text: str):
        token = await self.get_token()
        url = "https://gigachat.devices.sberbank.ru/api/v1/models"
        payload = {
            "model": "GigaChat-Max",
            "messages": [{"role": "user", "content": text}],
            "temperature": 1,
            "top_p": 0.1,
            "n": 1,
            "stream": False,
            "max_tokens": 512,
            "repetition_penalty": 1
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'Authorization': f'Bearer {token["access_token"]}'
        }
        response = requests.request("GET", url, headers=headers, data=payload, verify='chain.pem')
        return response.json()

    async def get_dict_answer_ai(self, user_id: int, access_token: str):
        url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
        if len(self.dict_history[user_id]) == 0:
            result = "New context"
        else:
            payload = json.dumps({
                "model": "GigaChat-Max",
                "messages": self.dict_history[user_id]
            })
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            async with aiohttp.ClientSession() as session:
                tasks = []
                result = None
                task_ai = asyncio.create_task(session.post(url, headers=headers, data=payload, verify_ssl=False))
                task_ai.set_name('task_ai')
                tasks.append(task_ai)
                task_progress = asyncio.create_task(self.progress_bar(user_id))
                task_progress.set_name('progress')
                tasks.append(task_progress)
                self.done, self.pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                for t in self.done:
                    if t.get_name() == 'task_ai':
                        self.response = t.result()
                        if self.response is not None:
                            result = await self.response.json()
        return result

    async def get_dict_photo_ai(self, user_id: int, user_text: str, access_token: str):
        url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
        if user_id in self.dict_history_src and len(self.dict_history_src[user_id]) != 0:
            payload = json.dumps({
                "model": "GigaChat-Max",
                "messages": [{"role": "system", "content": "Ты — Василий Кандинский"},
                             {"role": "user",
                              "content": user_text,
                              "attachments": self.dict_history_src[user_id]}],
                "function_call": "auto",
                "stream": False,
                "update_interval": 0
            })
        else:
            payload = json.dumps({
                "model": "GigaChat-Max",
                "messages": [{"role": "system", "content": "Ты — Василий Кандинский"},
                             {"role": "user",
                              "content": user_text}],
                "function_call": "auto"
            })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        async with aiohttp.ClientSession() as session:
            tasks = []
            task_ai = asyncio.create_task(session.post(url, headers=headers, data=payload, verify_ssl=False))
            task_ai.set_name('task_ai')
            tasks.append(task_ai)
            task_progress = asyncio.create_task(self.progress_bar(user_id))
            task_progress.set_name('progress')
            tasks.append(task_progress)
            self.done, self.pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        for t in self.done:
            if t.get_name() == 'task_ai':
                self.response = t.result()
        if self.response is None:
            result = None
        else:
            result = await self.response.json()
        print(result)
        return result

    async def add_user_query(self, user_id: int, user_text: str):
        if 'новый контекст' in user_text or 'Новый контекст' in user_text:
            self.dict_history[user_id] = []
        else:
            if user_id in self.dict_history:
                self.dict_history[user_id].append({"role": "user",
                                                   "content": user_text})
            else:
                self.dict_history[user_id] = [{"role": "user",
                                              "content": user_text}]

    async def add_assistant_query(self, user_id: int, assistant_text: str):
        self.dict_history[user_id].append({"role": "assistant",
                                           "content": assistant_text})

    async def get_general_image(self, user_id: int, src_text: str):
        token = await self.get_token()
        if 'новый контекст' in src_text or 'Новый контекст' in src_text:
            self.dict_history_src[user_id] = []
        else:
            url = "https://gigachat.devices.sberbank.ru/api/v1/files"
            payload = {'purpose': 'general'}
            files = [
                ('file', (f'response_{src_text}.jpeg', open(f"images/{src_text}.jpeg", 'rb'), 'image/jpeg'))
            ]
            headers = {'Authorization': f'Bearer {token["access_token"]}'}
            response = requests.request("POST", url, headers=headers, data=payload, files=files, verify='chain.pem')
            result = json.loads(response.text)
            self.dict_history_src[user_id] = [result["id"]]

    @staticmethod
    async def get_img(fileid: str, access_token: str):
        url = f"https://gigachat.devices.sberbank.ru/api/v1/files/{fileid}/content"
        payload = {}
        headers = {'Accept': 'application/jpeg', 'Authorization': f'Bearer {access_token}'}
        response = requests.request("GET", url, headers=headers, data=payload, verify='chain.pem')
        return response.content

    @staticmethod
    async def post_photo_ai(path_file: str, access_token: str):
        url = "https://gigachat.devices.sberbank.ru/api/v1/files"
        payload = {'purpose': 'general'}
        files = [('file', (f'photo_example_{path_file}.jpeg', open(path_file, 'rb'), 'image/jpeg'))]
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.request("POST", url, headers=headers, data=payload, files=files, verify='chain.pem')
        result = response.json()
        print(result)
        return result

    @staticmethod
    async def division_message(query: str) -> list:
        arr = []
        if len(query) > 4096:
            parts = len(query) // 4096
            for part in range(parts + 1):
                arr.append(query[4096*part:4096 + 4096*part])
        else:
            arr = [query]
        return arr

    async def get_dict_photo_ai_with_user_image(self, user_id: int, text: str, id_image_user, access_token: str):
        url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
        photo = id_image_user['id']
        payload = json.dumps({
            "model": "GigaChat-Max",
            "messages": [{"role": "system", "content": "Пиши как опытный специалист по таргетинговой рекламе."},
                         {"role": "user",
                          "content": f"Используй свои знания для создания описания товаров используя алгоритмы "
                                     f"соцсетей и психологического восприятия информации в соцсетях. "
                                     f"Измени этот текст, сохранив основной смысл, но используя другие слова."
                                     f"Тон и стиль: профессиональный и информативный, но пиши проще. "
                                     f"Включи ключевые слова: груза клеевые тонкие синяя коробка. "
                                     f"Подчеркни уникальные преимущества продукта и "
                                     f"учти возможные потенциальные возражения, каждое преимущество пиши "
                                     f"с новой строки, начиная с символа •. "
                                     f"Мне нужно 1 объявление, которые убедят аудиторию профессиональных работников "
                                     f"автомастерских купить себе товар на рисунке "
                                     f"со следующими характеристиками:\n {text}.", "attachments": [photo]}]
            })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        async with aiohttp.ClientSession() as session:
            tasks = []
            task_ai = asyncio.create_task(session.post(url, headers=headers, data=payload, verify_ssl=False))
            task_ai.set_name('task_ai')
            tasks.append(task_ai)
            task_progress = asyncio.create_task(self.progress_bar(user_id))
            task_progress.set_name('progress')
            tasks.append(task_progress)
            self.done, self.pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        for t in self.done:
            if t.get_name() == 'task_ai':
                self.response = t.result()
        if self.response is None:
            result = None
        else:
            result = await self.response.json()
        print(result)
        return result

    async def progress_bar(self, id_user: int):
        while len(self.done) == 0:
            await self.parent.edit_text(self.dict_current_message[id_user],
                                        self.list_text[self.dict_current_progress[id_user]])
            self.dict_current_progress[id_user] += 1
            await asyncio.sleep(0.7)
