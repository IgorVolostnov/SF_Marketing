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
        self.current_message = None
        self.current_progress = 0
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
        # self.client = Client("THUDM/CodeGeeX")

    async def answer_ai_message(self, query: str):
        response = await self.get_dict_answer_ai(query)
        return response['choices'][0]['message']['content']

    async def answer_ai_image(self, query: str, message: Message):
        self.done = set()
        self.pending = set()
        self.response = None
        self.current_progress = 0
        self.current_message = await self.parent.answer_text(message, 'собираю информацию 🟩')
        token = await self.get_token()
        response = await self.get_dict_photo_ai(query, token["access_token"])
        if response is None:
            answer = "Не смог ничего нарисовать, пропало настроение"
        else:
            answer = response['choices'][0]['message']['content']
        try:
            src = BeautifulSoup(answer, 'html.parser').find('img')['src']
            if not os.path.exists("images"):
                os.mkdir("images")
            with open(f"images/{src}.png", "wb+") as img_file:
                file_image = await self.get_img(src, token["access_token"])
                img_file.write(file_image)
            path_image = f"images/{src}.png"
        except TypeError:
            path_image = f"images/no_photo.png"
        return answer, path_image, self.current_message

    async def post_by_user_photo(self, query: str, path_user_foto: str, message: Message):
        self.done = set()
        self.pending = set()
        self.response = None
        self.current_progress = 0
        self.current_message = await self.parent.answer_text(message, 'собираю информацию 🟩')
        token = await self.get_token()
        info_user_photo = await self.post_photo_ai(path_user_foto, token["access_token"])
        response = await self.get_dict_photo_ai_with_user_image(query, info_user_photo, token["access_token"])
        if response is None:
            answer = "Не смог написать текст, не до продаж сегодня"
        else:
            answer = response['choices'][0]['message']['content']
        return answer, self.current_message

    @staticmethod
    async def get_token():
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        payload = {
            'scope': 'GIGACHAT_API_PERS'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': os.environ["CLIENT_ID"],
            'Authorization': f'Basic {os.environ["AUTHORIZATION_KEY"]}'
        }
        response = requests.request("POST", url, headers=headers, data=payload, verify='chain.pem')
        return response.json()

    async def get_dict_model(self, text: str):
        token = await self.get_token()
        url = "https://gigachat.devices.sberbank.ru/api/v1/models"
        payload = {
            "model": "GigaChat",
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

    async def get_dict_answer_ai(self, text: str):
        token = await self.get_token()
        url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
        payload = json.dumps({
            "model": "GigaChat-Pro",
            "messages": [{"role": "user", "content": text}],
            "temperature": 1,
            "top_p": 0.1,
            "n": 1,
            "stream": False,
            "max_tokens": 512,
            "repetition_penalty": 1
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {token["access_token"]}'
        }
        response = requests.request("POST", url, headers=headers, data=payload, verify='chain.pem')
        return response.json()

    async def get_dict_photo_ai(self, text: str, access_token: str):
        url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
        payload = json.dumps({
            "model": "GigaChat-Pro",
            "messages": [{"role": "system", "content": "Ты — Василий Кандинский"},
                         {"role": "user", "content": text}],
            "function_call": "auto"
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            tasks = []
            task_ai = asyncio.create_task(session.post(url, headers=headers, data=payload, verify_ssl=False))
            task_ai.set_name('task_ai')
            tasks.append(task_ai)
            task_progress = asyncio.create_task(self.progress_bar())
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
        return result

    @staticmethod
    async def get_img(fileid: str, access_token: str):
        url = f"https://gigachat.devices.sberbank.ru/api/v1/files/{fileid}/content"
        payload = {}
        headers = {'Accept': 'application/jpg', 'Authorization': f'Bearer {access_token}'}
        response = requests.request("GET", url, headers=headers, data=payload, verify='chain.pem')
        return response.content

    @staticmethod
    async def post_photo_ai(path_file: str, access_token: str):
        url = "https://gigachat.devices.sberbank.ru/api/v1/files"
        payload = {'purpose': 'general'}
        files = [('file', (f'photo_example.jpeg', open(path_file, 'rb'), 'image/jpeg'))]
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.request("POST", url, headers=headers, data=payload, files=files, verify='chain.pem')
        return response.json()

    async def get_dict_photo_ai_with_user_image(self, text: str, id_image_user, access_token: str):
        url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
        payload = json.dumps({
            "model": "GigaChat-Pro",
            "messages": [{"role": "user", "content": f"Составь продающий текст {text}?",
                          "attachments": [id_image_user['id']]}]})
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            tasks = []
            task_ai = asyncio.create_task(session.post(url, headers=headers, data=payload, verify_ssl=False))
            task_ai.set_name('task_ai')
            tasks.append(task_ai)
            task_progress = asyncio.create_task(self.progress_bar())
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
        return result

    async def progress_bar(self):
        while len(self.done) == 0:
            await self.parent.edit_text(self.current_message, self.list_text[self.current_progress])
            self.current_progress += 1
            await asyncio.sleep(0.7)
