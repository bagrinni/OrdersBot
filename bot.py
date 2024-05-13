import telebot
import psycopg2
from psycopg2 import Error

# Инициализация бота
bot = telebot.TeleBot("7093716301:AAHO9NSv-ZRVboH0oPcASSDc5-QuvnhymOc")

# Подключение к базе данных PostgreSQL
try:
    connection = psycopg2.connect(user="botapi",
                                  password="2569",
                                  host="localhost",
                                  database="marketer")
    cursor = connection.cursor()
    print("Подключение к PostgreSQL успешно")
except (Exception, Error) as error:
    print("Ошибка при подключении к PostgreSQL:", error)

# Chat ID вашей группы
group_chat_id = -1002131731216  # Замените на свой chat_id группы


@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = telebot.types.KeyboardButton("Заказать услугу")
    markup.add(item)
    bot.send_message(message.chat.id, "Привет! Я бот BagrinniServicesBot. Чем могу помочь?", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Заказать услугу")
def order_service(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = telebot.types.KeyboardButton("СММ")
    item2 = telebot.types.KeyboardButton("Дизайн")
    item3 = telebot.types.KeyboardButton("Таргет")
    item4 = telebot.types.KeyboardButton("Ведение маркетинга")
    markup.add(item1, item2, item3, item4)
    bot.send_message(message.chat.id, "Выберите услугу:", reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def process_service(message):
    user_id = message.from_user.id
    service = message.text
    bot.send_message(message.chat.id, "Введите ваше имя:")
    bot.register_next_step_handler(message, process_name, user_id, service)

def process_name(message, user_id, service):
    name = message.text
    bot.send_message(message.chat.id, f"Спасибо, {name}! Теперь введите ваш номер телефона:")
    bot.register_next_step_handler(message, process_phone, user_id, service, name)

def process_phone(message, user_id, service, name):
    phone = message.text
    bot.send_message(message.chat.id, "Введите вашу страницу в Instagram:")
    bot.register_next_step_handler(message, process_instagram, user_id, service, name, phone)

def process_instagram(message, user_id, service, name, phone):
    instagram = message.text
    try:
        
        cursor.execute("INSERT INTO orders (user_id, service, name, phone, instagram) VALUES (%s, %s, %s, %s, %s)",
                       (user_id, service, name, phone, instagram))
        connection.commit()

    
        bot.send_message(group_chat_id, f"Новый заказ от пользователя {name}:\n"
                                        f"Услуга: {service}\n"
                                        f"Телефон: {phone}\n"
                                        f"Instagram: {instagram}")

        bot.send_message(user_id, "Спасибо за заказ! Мы свяжемся с вами в ближайшее время.")
    except (Exception, Error) as error:
        print("Ошибка при выполнении запроса к PostgreSQL:", error)


bot.polling()
