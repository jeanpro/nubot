import datetime
import unidecode
from telegram import ReplyKeyboardMarkup
from database import SessionLocal
from crud import *
import re
EXPIRE_TIME_IN_MINUTES = 10

def is_too_old(msg_date, expire: int = EXPIRE_TIME_IN_MINUTES):
    if msg_date < datetime.datetime.now(msg_date.tzinfo) - datetime.timedelta(minutes=EXPIRE_TIME_IN_MINUTES):
        return True
    else:
        return False


def clean_text(msg: str):
    result = msg.split(' ')[0]
    result =  re.sub(r'[^A-Za-z0-9áéíóúÁÉÍÓÚãẽĩõũÃẼĨÕŨÑñâêîôûÂÊÎÔÛÇç&\-]+', '', result, flags=re.IGNORECASE)
    #result = ''.join(e for e in result if (e.isalnum()) or (e == '-')) #only alphanumeric characters
#    try:
#        result = unidecode.unidecode(result)
#    except:
#        pass
    return result.lower()

# Start bot handling text messages. Commands are ignored for now.
def textBot(update, context):
    """
        TODOs:
            0) Checa se o aluno é novo e manda msg de boas vindas
            1) Clean message (Lower, strip special characters split and get first word) e.g. Sim = sim = Sim! = SiM, por favor = Sim <3 etc
            2) Busca msg no banco e retorna o texto 
            3) Se não achou retorna uma mensagem que não entendeu. 
            4) Subir para Máquina Virtual
    """
    try:
        too_old = is_too_old(update.message.date)
    except:
        too_old = False
    if too_old == False:
        query_result = query_keyword(db=SessionLocal(), keyword=clean_text(update.message.text))
        list_of_options = None
        if query_result:
            text_message = query_result.message
            list_of_options = query_result.options
        else:
            default_result = query_keyword(db=SessionLocal(), keyword='default')
            text_message = default_result.message if default_result != None else 'Não entendi, poderia escrever com outras palavras?'
            list_of_options = default_result.options
        if list_of_options:
            reply_keyboard = ReplyKeyboardMarkup.from_column(list_of_options, resize_keyboard=True, one_time_keyboard=True)
        else:
            reply_keyboard=None
        context.bot.send_message(chat_id=update.effective_chat.id, text=text_message, reply_markup=reply_keyboard)


def commandStartBot(update, context):
    default_result = query_keyword(db=SessionLocal(), keyword='default')
    text_message = default_result.message if default_result != None else 'Não entendi, poderia escrever com outras palavras?'
    list_of_options = default_result.options
    if list_of_options:
        reply_keyboard = ReplyKeyboardMarkup.from_column(list_of_options, resize_keyboard=True, one_time_keyboard=True)
    else:
        reply_keyboard=None
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_message, reply_markup=reply_keyboard)

def commandBot(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Vai toma no cu mermão')