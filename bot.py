import telebot
import random
import string
import config

bot = telebot.TeleBot(config.TOKEN)
user_id = ''
token = ''
mEditIds = []

def rndm():  #генерация токена
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))

def check(id):  #проверка наличия токена у пользователя
    f = open('user_list.txt', 'r')
    for line in f:
        if str(id) in line:
            return True
    return False

@bot.message_handler(commands=['token'])
def admin_msg(message):
    global user_id, token
    user_id = message.chat.id
    ###
    if check(user_id):
        bot.send_message(user_id, 'У Вас уже есть токен.')
    else:
        bot.send_message(user_id, 'Запрос отправлен, ждите ответа.')
        token = rndm()
        f = open('user_list.txt', 'a')
        f.write(str(user_id) + ':' + token + '\n')
        markup = telebot.types.InlineKeyboardMarkup()
        btn_1= telebot.types.InlineKeyboardButton(text='Разрешить',callback_data='a1')
        btn_2 = telebot.types.InlineKeyboardButton(text='Отклонить', callback_data='a2')
        markup.add(btn_1, btn_2)
        for admin_id in config.AdminInfo:
            mess = bot.send_message(admin_id, '@'+message.chat.username+' Запрашивает токен', reply_markup = markup)
            mEditIds.append(mess.message_id)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    number_of_deviations = 0
    global user_id, token
    ###
    if call.message:
        if call.data == 'a1':
            bot.send_message(user_id, 'Разрешение получено. Токен: '+token)
            for (admin_id, message_id) in zip(config.AdminInfo, mEditIds):
                bot.edit_message_text(chat_id=admin_id, message_id=message_id,
                                      text='Отправлено разрешение администратором @'+call.message.chat.username+'.')
        if call.data == 'a2':
            number_of_deviations += 1
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Отклонено.')
            if number_of_deviations == len(config.AdminInfo):
                bot.send_message(user_id, 'Отказано.')


@bot.message_handler(commands=['get_token'])
def msg(message):
    global token
    if check(message.chat.id):
        f = open('user_list.txt', 'r')
        for line in f:
            if str(message.chat.id) in line:
                token = line[10:29]
        bot.send_message(message.chat.id, token)
    else:
        bot.send_message(message.chat.id, 'У Вас нет токена.')


bot.polling()
