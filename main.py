from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
import logging

from sqlalchemy.orm import Session

from crud import *
from models import Base
from schemas import *

from database import SessionLocal, engine

from nubotapi import *

Base.metadata.create_all(bind=engine)

app = FastAPI()

#DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
    Initialize Telegram Bot
"""
BOTNAME = 'cloudinha'
TOKEN = None
dispatcher = None
updater = None

try:
    token_obj = get_token(db = SessionLocal(), bot_name = BOTNAME)
    TOKEN = token_obj.token

except:
    print("Not able to retrieve TOKEN from DB. Please check if DB is running...")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

if TOKEN:
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = MessageHandler(Filters.text & (~Filters.command), textBot)

    #Dispatching commands
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(CommandHandler('cuzao', commandBot))
    dispatcher.add_handler(CommandHandler('start', commandStartBot))
    dispatcher.add_handler(CommandHandler('help', commandStartBot))
    dispatcher.add_handler(CommandHandler('ajuda', commandStartBot))


    #Start bot
    print('Bot started!')
    updater.start_polling()


@app.get('/')
def root():
    if dispatcher:
        return 'Servidor está no ar!'
    else:
        return 'BOT ESTÁ OFFLINE. ALGUM ERRO ACONTECEU.'

@app.get('/start')
def start():
    updater.start_polling()
    return "TÁ ONLINE MULEKE!"

@app.get('/stop')
def stop_bot():
    updater.stop()
    return 'BOT DESLIGOU'

@app.get('/messages/', response_model=List[Message])
def read_messages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    messages = get_messages(db, skip=skip, limit=limit)
    return messages

@app.post('/messages/')
def add_message_to_db(message: MessageCreate, db: Session = Depends(get_db)):
    return create_message(db = db, message = message)


@app.post('/messages/delete/{keyword}')
def delete_message_from_db(keyword: str, db: Session = Depends(get_db)):
    return delete_message(db = db, keyword = keyword)


@app.post('/token/', response_model = Token)
def add_token_to_db(token: TokenCreate, db: Session = Depends(get_db)):
    return create_token(db = db, token = token)
