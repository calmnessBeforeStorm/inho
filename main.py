import json, os, logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token='6171743867:AAGhVrQ93ijo9lALoC8t2-o1Coo1z6dIy0k')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

logging.basicConfig(level=logging.INFO)

file_path = 'data.json'
if not os.path.isfile(file_path):
    print(f'Файл {file_path} не существует.')
    with open(file_path, 'w') as file:
        file.write('{}')

@dp.message_handler()
async def handle_message(message: types.Message):
    text = message.text.upper()
    if text == 'ФЕРМА':
        user_id = message.from_user.id
        with open(file_path, 'r+') as file:
            data = json.load(file)
            if str(user_id) not in data:
                data[str(user_id)] = 0
            data[str(user_id)] += 1
            file.seek(0)
            json.dump(data, file, indent=4)
    elif text == '/list':
        with open(file_path, 'r') as file:
            data = json.load(file)
            sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
            if sorted_data:
                response = "Список пользователей, отправивших сообщение 'ферма':\n"
                for user_id, count in sorted_data:
                    user = await bot.get_chat(user_id)
                    username = user.username if user.username else user.first_name
                    response += f"@{username}: {count} раз(а)\n"
                await message.answer(response)
            else:
                await message.answer("Список пользователей пуст.")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
