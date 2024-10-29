import json
import logging
import requests
import os
from gradio_client import Client
from bs4 import BeautifulSoup


logging.basicConfig(level=logging.INFO)


class AI:
    def __init__(self):
        self.client = Client("THUDM/CodeGeeX")

    async def answer_ai_message(self, query: str):
        response = await self.get_dict_answer_ai(query)
        return response['choices'][0]['message']['content']

    async def answer_ai_image(self, query: str):
        token = await self.get_token()
        response = await self.get_dict_photo_ai(query, token["access_token"])
        answer = response['choices'][0]['message']['content']
        src = BeautifulSoup(answer, 'html.parser').find('img')['src']
        if not os.path.exists("images"):
            os.mkdir("images")
        with open("images/new_img.png", "wb+") as img_file:
            file_image = await self.get_img(src, token["access_token"])
            img_file.write(file_image)
        return answer

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

    async def get_dict_model(self, text):
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

    async def get_dict_answer_ai(self, text):
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

    @staticmethod
    async def get_dict_photo_ai(text, access_token):
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
        response = requests.request("POST", url, headers=headers, data=payload, verify='chain.pem')
        return response.json()

    @staticmethod
    async def get_img(fileid, access_token):
        url = f"https://gigachat.devices.sberbank.ru/api/v1/files/{fileid}/content"
        payload = {}
        headers = {
            'Accept': 'application/jpg',
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.request("GET", url, headers=headers, data=payload, verify='chain.pem')
        return response.content

    async def talk_ai(self, query: str):
        query = self.client.predict(message=f"{query}", api_name="/chat")
        return query
