import telebot
from telebot import types
from time import sleep
import os

ACESS_TOKEN = os.environ.get('ACESS_TOKEN')

bot = telebot.TeleBot(ACESS_TOKEN)

@bot.message_handler(commands=['start'])
def start(chat):
    bot.send_message(chat.chat.id, 'Bem vindo ao restaurante MinhaComida! 😋')
    sleep(2)

    bot.send_message(
        chat.chat.id,
        text='O que você deseja? 😀\n\n/menu: Ver lanches disponíveis\n/mensagem: Deixar avaliação, sugestão ou reclamação'
    )


# Gerenciando opções
@bot.message_handler(commands=['menu'])
def send_menu(chat):
    bot.send_message(
        chat.chat.id,
        text='Nosso cardápio:\n\n/1: Hamburguer com tomate, maionese, queijo e presunto\n/2: Pizza de calabresa tamanho familia\n/3: Coxinha de frango'
    )

# Mensagem
@bot.message_handler(commands=['mensagem'])
def message(chat):
    bot.send_message(chat.chat.id, 'Vamos lá, pode falar!')
    bot.register_next_step_handler(chat, receive_message)

def receive_message(chat):
    bot.send_message(chat.chat.id, 'Recebemos sua mensagem! Obrigado, em breve um de nossos atendentes irá te responder.')
    sleep(2)

    bot.send_message(chat.chat.id, 'Mais alguma coisa?\n\n/start: Reiniciar atendimento\n/menu: Ver menu\n/mensagem: Deixar uma avaliação, sugestão ou reclamação')

# Lanches
@bot.message_handler(commands=['1','2','3'])
def one_option(chat):
    markup = types.ReplyKeyboardMarkup(row_width=2)

    option1 = types.KeyboardButton('Sim')
    option2 = types.KeyboardButton('Não')

    markup.add(option1, option2)
    bot.send_message(chat.chat.id, 'Bem, esse lanche custa $5.99, deseja realizar o pedido?', reply_markup=markup)
    bot.register_next_step_handler(chat, process_option)

def process_option(chat):
    if chat.text == 'Sim':
        bot.send_message(chat.chat.id, 'Processando pedido...', reply_markup=types.ReplyKeyboardRemove())
        bot.send_message(chat.chat.id, 'Pedido enviado! Por favor, aguarde. ')
    elif chat.text == 'Não':
        bot.send_message(chat.chat.id, 'Ah, porque não? Mas tudo bem, olhe nosso cardápio!\n\n/menu: Ver lanches', reply_markup=types.ReplyKeyboardRemove())

# Ignorar opções erradas
@bot.message_handler()
def invalid_option(chat):
    bot.send_message(
        chat.chat.id,
        text='Infelizemente não consegui entender sua solicitação. Tente novamente!\n\n/start: Reiniciar atendimento\n/menu: Ver menu\n/mensagem: Deixar uma avaliação, sugestão ou reclamação'
    )

bot.infinity_polling()