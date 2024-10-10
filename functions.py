import asyncio
import logging
import re
import os
import phonenumbers
from keyboard import KeyBoardBot
from database_requests import Execute
from edit_pdf import GetTextOCR
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, FSInputFile, ChatPermissions
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.enums.parse_mode import ParseMode
from aiogram.utils.media_group import MediaGroupBuilder

logging.basicConfig(level=logging.INFO)


class Function:
    def __init__(self, bot, dispatcher):
        self.bot = bot
        self.dispatcher = dispatcher
        self.keyboard = KeyBoardBot()
        self.execute = Execute()
        self.info_pdf = GetTextOCR()
        self.dict_user = asyncio.run(self.execute.get_dict_user)
        self.dict_goal = asyncio.run(self.execute.get_dict_goal)

    async def show_back(self, call_back: CallbackQuery):
        previous_history = self.dict_user[call_back.from_user.id]['history'].pop()
        if self.dict_user[call_back.from_user.id]['history'][-1] == 'start':
            await self.return_start(call_back)
        elif self.dict_user[call_back.from_user.id]['history'][-1] == 'goal':
            await self.show_goal(call_back, previous_history)
        elif self.dict_user[call_back.from_user.id]['history'][-1] == 'outlay':
            await self.show_outlay(call_back, previous_history)
        elif self.dict_user[call_back.from_user.id]['history'][-1] == 'income':
            await self.show_income(call_back, previous_history)
        else:
            await self.return_start(call_back)
        return True

    async def checking_bot(self, message: Message):
        if message.from_user.is_bot:
            await self.bot.restrict_chat_member(message.chat.id, message.from_user.id, ChatPermissions())
            this_bot = True
        else:
            this_bot = False
        return this_bot

    async def show_command_start(self, message: Message):
        check = await self.checking_bot(message)
        if check:
            await self.delete_messages(message.from_user.id, [message.message_id])
        else:
            if message.from_user.id not in self.dict_user.keys():
                self.dict_user[message.from_user.id] = {'history': ['start'], 'messages': [],
                                                        'first_name': message.from_user.first_name,
                                                        'last_name': message.from_user.last_name,
                                                        'user_name': message.from_user.username}
            first_keyboard = await self.keyboard.get_first_menu(self.dict_user[message.from_user.id]['history'])
            text_message = f"{self.format_text('Поставить цель 🎯')} - выбрать цель, на которую будем копить!\n" \
                           f"{self.format_text('Расходы 🧮')} - меню учета расходов\n" \
                           f"{self.format_text('Доходы 💰')} - меню учета доходов\n"
            answer = await self.bot.push_photo(message.chat.id, text_message, self.build_keyboard(first_keyboard, 1),
                                               self.bot.logo_main_menu)
            self.dict_user[message.from_user.id]['messages'].append(str(message.message_id))
            self.dict_user[message.from_user.id]['messages'] = await self.delete_messages(message.from_user.id,
                                                                                          self.dict_user[
                                                                                              message.from_user.id][
                                                                                              'messages'])
            self.dict_user[message.from_user.id]['messages'].append(str(answer.message_id))
            self.dict_user[message.from_user.id]['history'].append('start')
            await self.execute.set_user(message.from_user.id, self.dict_user[message.from_user.id])
        return True

    async def return_start(self, call_back: CallbackQuery):
        first_keyboard = await self.keyboard.get_first_menu(self.dict_user[call_back.from_user.id]['history'])
        text = f"{self.format_text('Поставить цель 🎯')} - выбрать цель, на которую будем копить!\n" \
               f"{self.format_text('Расходы 🧮')} - меню учета расходов\n" \
               f"{self.format_text('Доходы 💰')} - меню учета доходов\n"
        answer = await self.bot.push_photo(call_back.message.chat.id, text,
                                           self.build_keyboard(first_keyboard, 1), self.bot.logo_main_menu)
        self.dict_user[call_back.from_user.id]['messages'] = await self.delete_messages(
            call_back.from_user.id, self.dict_user[call_back.from_user.id]['messages'])
        self.dict_user[call_back.from_user.id]['messages'].append(str(answer.message_id))
        await self.execute.set_user(call_back.from_user.id, self.dict_user[call_back.from_user.id])
        return True

    async def newsletter(self):
        text_message = await self.keyboard.text_for_news()
        for user_id in self.dict_user.keys():
            first_keyboard = await self.keyboard.get_first_menu(self.dict_user[user_id]['history'])
            try:
                answer = await self.bot.push_photo(user_id, text_message, self.build_keyboard(first_keyboard, 1),
                                                   self.bot.logo_main_menu)
                self.dict_user[user_id]['messages'] = await self.delete_messages(user_id,
                                                                                 self.dict_user[user_id]['messages'])
                self.dict_user[user_id]['messages'].append(str(answer.message_id))
                self.dict_user[user_id]['history'].append('start')
            except TelegramForbiddenError:
                await self.execute.delete_user(user_id)
                self.dict_user.pop(user_id)
        await self.execute.set_all_users(self.dict_user)
        return True

    async def show_goal(self, call_back: CallbackQuery, back_history: str = None):
        keyboard_goal = await self.keyboard.get_goal_menu()
        text = f"{self.format_text('Добавить новую цель ➕')} - добавить новую цель, на которую собираетесь копить\n" \
               f"{self.format_text('Показать список целей 👀')} - показать список уже имеющихся у Вас целей\n"
        if back_history:
            await self.change_message_and_history(call_back, text, keyboard_goal, self.bot.logo_goal_menu, back_history,
                                                  ['add_goal'])
        else:
            await self.change_message_and_history(call_back, text, keyboard_goal, self.bot.logo_goal_menu)
        await self.execute.set_user(call_back.from_user.id, self.dict_user[call_back.from_user.id])
        return True

    async def show_outlay(self, call_back: CallbackQuery, back_history: str = None):
        keyboard_outlay = await self.keyboard.get_outlay_menu()
        text = f"{self.format_text('Добавить новые расходы ➕')} - добавьте расходы, отправив файл PDF или вручную\n" \
               f"{self.format_text('Показать список расходов 👀')} - вывести на экран список всех расходов за месяц\n" \
               f"{self.format_text('Аналитика расходов 📊')} - показать распределение расходов по категориям\n" \
               f"{self.format_text('Изменить категории расходов ⚙')} - изменить список категорий расходов\n" \
               f"{self.format_text('Назад 🔙')} - вернуться в предыдущее меню\n"
        if back_history:
            await self.change_message_and_history(call_back, text, keyboard_outlay, self.bot.logo_outlay_menu,
                                                  back_history, ['add_outlay'])
        else:
            await self.change_message_and_history(call_back, text, keyboard_outlay, self.bot.logo_outlay_menu)
        await self.execute.set_user(call_back.from_user.id, self.dict_user[call_back.from_user.id])
        return True

    async def show_income(self, call_back: CallbackQuery, back_history: str = None):
        keyboard_income = await self.keyboard.get_income_menu()
        text = f"{self.format_text('Добавить новые доходы ➕')} - добавьте доходы, отправив файл PDF или вручную\n" \
               f"{self.format_text('Показать список доходов 👀')} - вывести на экран список всех доходов за месяц\n" \
               f"{self.format_text('Аналитика доходов 📊')} - показать распределение доходов по категориям\n" \
               f"{self.format_text('Изменить категории доходов ⚙')} - изменить список категорий доходов\n" \
               f"{self.format_text('Назад 🔙')} - вернуться в предыдущее меню\n"
        if back_history:
            await self.change_message_and_history(call_back, text, keyboard_income, self.bot.logo_income_menu,
                                                  back_history, ['add_income'])
        else:
            await self.change_message_and_history(call_back, text, keyboard_income, self.bot.logo_income_menu)
        return True

    async def change_message_and_history(self, call_back: CallbackQuery, text: str, keyboard:  dict, logo: FSInputFile,
                                         back: str = None, list_previous_history: list = None):
        if back is not None:
            if back in list_previous_history:
                await self.edit_caption(call_back.message, text, self.build_keyboard(keyboard, 1))
            else:
                answer = await self.bot.push_photo(
                    call_back.message.chat.id, text, self.build_keyboard(keyboard, 1), logo)
                self.dict_user[call_back.from_user.id]['messages'] = await self.delete_messages(
                    call_back.from_user.id, self.dict_user[call_back.from_user.id]['messages'])
                self.dict_user[call_back.from_user.id]['messages'].append(str(answer.message_id))
        else:
            answer = await self.bot.push_photo(
                call_back.message.chat.id, text, self.build_keyboard(keyboard, 1), logo)
            self.dict_user[call_back.from_user.id]['messages'] = await self.delete_messages(
                call_back.from_user.id, self.dict_user[call_back.from_user.id]['messages'])
            self.dict_user[call_back.from_user.id]['messages'].append(str(answer.message_id))
            self.dict_user[call_back.from_user.id]['history'].append(call_back.data)

    async def get_document(self, message: Message, list_messages: list):
        document_info = await self.bot.save_document(message)
        arr_message = self.add_message_user(list_messages, str(message.message_id))
        await self.bot.delete_messages_chat(message.chat.id, arr_message[1:])
        return document_info

    async def get_audio(self, message: Message, list_messages: list):
        audio_info = await self.bot.save_audio(message)
        arr_message = self.add_message_user(list_messages, str(message.message_id))
        await self.bot.delete_messages_chat(message.chat.id, arr_message[1:])
        return audio_info

    async def get_voice(self, message: Message, list_messages: list):
        voice_info = await self.bot.save_voice(message)
        arr_message = self.add_message_user(list_messages, str(message.message_id))
        await self.bot.delete_messages_chat(message.chat.id, arr_message[1:])
        return voice_info

    async def get_photo(self, message: Message, list_messages: list):
        photo_info = await self.bot.save_photo(message)
        arr_message = self.add_message_user(list_messages, str(message.message_id))
        await self.bot.delete_messages_chat(message.chat.id, arr_message[1:])
        return photo_info

    async def get_video(self, message: Message, list_messages: list):
        video_info = await self.bot.save_video(message)
        arr_message = self.add_message_user(list_messages, str(message.message_id))
        await self.bot.delete_messages_chat(message.chat.id, arr_message[1:])
        return video_info

    @staticmethod
    async def check_text(string_text: str):
        arr_text = string_text.split(' ')
        new_arr_text = []
        for item in arr_text:
            new_item = re.sub(r"[^ \w]", '', item)
            if new_item != '':
                new_arr_text.append(new_item)
        new_string = ' '.join(new_arr_text)
        return new_string

    @staticmethod
    async def check_email(string_text: str):
        arr_text = string_text.split(' ')
        new_arr_text = []
        for item in arr_text:
            new_item = re.sub("[^A-Za-z@.]", "", item)
            if new_item != '':
                new_arr_text.append(new_item)
        new_string = ' '.join(new_arr_text)
        return new_string

    @staticmethod
    async def check_telephone(string_text: str):
        telephone = re.sub("[^0-9+]", "", string_text)
        if telephone[0] != '+' and len(telephone) == 10:
            telephone = '+7' + telephone
        elif len(telephone) == 11:
            telephone = '+7' + telephone[1:]
        return telephone

    @staticmethod
    def validate_phone_number(potential_number: str) -> bool:
        try:
            phone_number_obj = phonenumbers.parse(potential_number)
        except phonenumbers.phonenumberutil.NumberParseException:
            return False
        if not phonenumbers.is_valid_number(phone_number_obj):
            return False
        return True

    @staticmethod
    async def answer_message(message: Message, text: str, keyboard: InlineKeyboardMarkup):
        return await message.answer(text=text, parse_mode=ParseMode.HTML, reply_markup=keyboard)

    @staticmethod
    async def edit_message(message: Message, text: str, keyboard: InlineKeyboardMarkup):
        return await message.edit_text(text=text, parse_mode=ParseMode.HTML, reply_markup=keyboard)

    @staticmethod
    async def answer_text(message: Message, text: str):
        return await message.answer(text=text, parse_mode=ParseMode.HTML, reply_to_message_id=message.message_id)

    @staticmethod
    async def edit_caption(message: Message, text: str, keyboard: InlineKeyboardMarkup):
        return await message.edit_caption(caption=text, parse_mode=ParseMode.HTML, reply_markup=keyboard)

    async def answer_photo(self, message: Message, photo: str, caption: str, keyboard: InlineKeyboardMarkup):
        try:
            return await message.answer_photo(photo=photo, caption=caption, parse_mode=ParseMode.HTML,
                                              reply_markup=keyboard)
        except TelegramBadRequest:
            photo = "https://www.rossvik.moscow/images/no_foto.png"
            text_by_format = self.format_text(caption)
            return await message.answer_photo(photo=photo, caption=text_by_format, parse_mode=ParseMode.HTML,
                                              reply_markup=keyboard)

    async def send_photo(self, message: Message, photo: str, text: str, amount_photo: int):
        media_group = MediaGroupBuilder(caption=text)
        if photo:
            arr_photo = photo.split()[:amount_photo]
        else:
            arr_photo = ["https://www.rossvik.moscow/images/no_foto.png"]
        for item in arr_photo:
            media_group.add_photo(media=item, parse_mode=ParseMode.HTML)
        try:
            return await self.bot.send_media_group(chat_id=message.chat.id, media=media_group.build())
        except TelegramBadRequest as error:
            print(error)
            media_group = MediaGroupBuilder(caption=text)
            arr_photo = ["https://www.rossvik.moscow/images/no_foto.png"]
            for item in arr_photo:
                media_group.add_photo(media=item, parse_mode=ParseMode.HTML)
            return await self.bot.send_media_group(chat_id=message.chat.id, media=media_group.build())

    async def send_file(self, message: Message, document: str, text: str, keyboard: InlineKeyboardMarkup):
        if document != '':
            arr_content = document.split('///')
            return await message.answer_document(document=FSInputFile(arr_content[0]), caption=text,
                                                 parse_mode=ParseMode.HTML, reply_markup=keyboard)
        else:
            return await self.answer_message(message, text, keyboard)

    async def send_media(self, message: Message, media: list, server: bool = False):
        media_group = MediaGroupBuilder()
        for item in media:
            if server:
                if 'C:\\Users\\Rossvik\\PycharmProjects\\' in item:
                    path_file = os.path.join(os.path.split(os.path.dirname(__file__))[0],
                                             item.split('C:\\Users\\Rossvik\\PycharmProjects\\')[1])
                else:
                    path_file = item
            else:
                if 'C:\\Users\\Rossvik\\PycharmProjects\\' in item:
                    path_file = item
                else:
                    path_reverse = "\\".join(item.split("/"))
                    path_file = 'C:\\Users\\Rossvik\\PycharmProjects\\' + path_reverse
            file_input = FSInputFile(path_file)
            media_group.add_document(media=file_input, parse_mode=ParseMode.HTML)
        return await self.bot.send_media_group(chat_id=message.chat.id, media=media_group.build())

    async def delete_messages(self, user_id: int, list_messages: list, except_id: str = None,
                              individual: bool = False) -> list:
        if not list_messages:
            new_list_message = []
        elif except_id and individual:
            new_list_message = []
            for message in list_messages:
                if message != except_id:
                    new_list_message.append(message)
            await self.bot.delete_messages_chat(user_id, [except_id])
        elif except_id and not individual:
            new_list_message = []
            for message in list_messages:
                if message != except_id:
                    new_list_message.append(message)
            await self.bot.delete_messages_chat(user_id, new_list_message)
            new_list_message = [except_id]
        else:
            await self.bot.delete_messages_chat(user_id, list_messages)
            new_list_message = []
        return new_list_message

    def build_keyboard(self, dict_button: dict, column: int, dict_return_button=None) -> InlineKeyboardMarkup:
        keyboard = self.build_menu(self.get_list_keyboard_button(dict_button), column,
                                   footer_buttons=self.get_list_keyboard_button(dict_return_button))
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @staticmethod
    async def edit_keyboard(message: Message, keyboard: InlineKeyboardMarkup):
        return await message.edit_reply_markup(reply_markup=keyboard)

    @staticmethod
    def add_message_user(arr_messages: list, message: str) -> list:
        arr_messages.append(message)
        return arr_messages

    @staticmethod
    def get_list_keyboard_button(dict_button: dict):
        button_list = []
        if dict_button:
            for key, value in dict_button.items():
                if 'https://' in key:
                    button_list.append(InlineKeyboardButton(text=value, url=key))
                else:
                    button_list.append(InlineKeyboardButton(text=value, callback_data=key))
        else:
            button_list = None
        return button_list

    @staticmethod
    def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None) -> list:
        menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
        if header_buttons:
            menu.insert(0, [header_buttons])
        if footer_buttons:
            for item in footer_buttons:
                menu.append([item])
        return menu

    @staticmethod
    def format_text(text_message: str) -> str:
        cleaner = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        clean_text = re.sub(cleaner, '', text_message)
        return f'<b>{clean_text}</b>'

    @staticmethod
    def format_price(item: float) -> str:
        return '{0:,} ₽'.format(item).replace(',', ' ')

    @staticmethod
    def quote(request) -> str:
        return f"'{str(request)}'"
