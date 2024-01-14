from pokemon import Pokemon
import image_search

import os

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.environ.get('TELEGRAM_API')
search_key = os.environ.get('SERPAPI_API')

import logging
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, CallbackContext, CallbackQueryHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def queryHandler(update: Update, context: CallbackContext):
    query = update.callback_query.data
    await update.callback_query.answer()
    if "yes" in query:
        print('yes')
    
    if "no" in query:
         print('no')

async def start(update: Update, context: None):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome! I'm the Pokemon Stats Bot! I can identify Pokemons and give you useful information like Types, Weakness and Abilities!")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Type the name of a Pokemon or send a picture to begin!")

async def echo(update: Update, context: None):
    if update.message.text.lower() == 'test':
        await context.bot.send_message(chat_id=update.effective_chat.id, text='teste', parse_mode='HTML')
        buttons = [[InlineKeyboardButton("👍", callback_data="yes")], [InlineKeyboardButton("👎", callback_data="no")]]
        await context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text='is this the pokemon you are loking for?')
        
        

    else:
        pokemon_name = update.message.text
        if pokemon_name.lower() not in image_search.pokemon_list:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="I cannot identify your pokemon, please try again")
        else:
            pokemon = Pokemon(pokemon_name)
            description = pokemon.get_description()
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=pokemon.sprite)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=description, parse_mode='HTML')

async def image(update: Update, context: None):
    file_id = update.message.photo[-1].file_id
    imageurl = image_search.get_image(TOKEN, file_id)
    search_results = image_search.reverse_search(search_key, imageurl)
    poke = image_search.filter_results(search_results)
    if poke == 'No results found':
        await context.bot.send_message(chat_id=update.effective_chat.id, text='I cannot identify your pokemon, please try again with a better quality picture. try cropping the image, sometimes it helps.', parse_mode='HTML')    
    elif len(poke) == 1:
        pokemon = Pokemon(poke[0])
        description = pokemon.get_description()
        await context.bot.send_message(chat_id=update.effective_chat.id, text=description, parse_mode='HTML')
    else:
        for pokemon in poke:
            p = Pokemon(pokemon)
            await context.bot.send_message(chat_id=update.effective_chat.id, text='is this the pokemon you are loking for?', parse_mode='HTML')
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=p.sprite)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=p.name, parse_mode='HTML')
            await context.bot.send_message(chat_id=update.effective_chat.id, text="select:", reply_markup=InlineKeyboardMarkup(['yes', 'no']), parse_mode='HTML')




    
    

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)

    pokemon_handler = MessageHandler(filters.TEXT, echo)

    image_handler = MessageHandler(filters.PHOTO, image)

    

    application.add_handler(start_handler)
    application.add_handler(pokemon_handler)
    application.add_handler(image_handler)
    application.add_handler(CallbackQueryHandler(queryHandler))
    
    application.run_polling()