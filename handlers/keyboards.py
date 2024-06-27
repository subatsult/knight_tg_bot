from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder,InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram_widgets.pagination import KeyboardPaginator
from encounter import *
import random
import json

GAME_STATE_FILE = 'game_state.json'

async def save_game_state():
    game_state = {
        'hp': hp,
        'money': money,
        'stamina': stamina,
        'dragon_hp': dragon_hp,
        'inventory': inventory
    }
    with open(GAME_STATE_FILE, 'w') as f:
        json.dump(game_state, f)

async def load_game_state():
    global hp, money, stamina, dragon_hp, inventory
    try:
        with open(GAME_STATE_FILE, 'r') as f:
            game_state = json.load(f)
            hp = game_state['hp']
            money = game_state['money']
            stamina = game_state['stamina']
            dragon_hp = game_state['dragon_hp']
            inventory = game_state['inventory']
    except FileNotFoundError:
        # Handle initial state when the file doesn't exist
        pass


kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Inventory')]
    ],
    resize_keyboard=True)

async def show_inventory():
    kb = InlineKeyboardBuilder()
    for item in inventory:
        if item == 'potion':
            kb.add(InlineKeyboardButton(text='Drink Potion (heals 2 HP)', callback_data='drink_potion'))
    return kb.as_markup()

async def drink_potion():
    global hp
    hp += 2
    inventory.remove('potion')
    return inventory

async def choice_start():
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Go to city for a walk?', callback_data='city'))
    kb.add(InlineKeyboardButton(text='Go straight to the shop?', callback_data='shop'))
    return kb.adjust(2).as_markup()

async def ludoman():
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Yes, I wanna try. (Money cost = 10)', callback_data='ludka'))
    kb.add(InlineKeyboardButton(text='No thanks', callback_data='krasaba'))
    return kb.adjust(2).as_markup()

async def baryga():
    global money
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Yes, buy 1 potion', callback_data='potion'))
    if money >= 20:
        kb.add(InlineKeyboardButton(text='Yes, buy 2 potions', callback_data='potions'))
    return kb.adjust(2).as_markup()  

async def dragon():
    global hp
    global dragon_hp
    wb = ReplyKeyboardBuilder()
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Hit his head', callback_data='head'))
    kb.add(InlineKeyboardButton(text='Hit his body', callback_data='body'))
    kb.add(InlineKeyboardButton(text='Hit his nogi', callback_data='legs'))
    return kb.adjust(3).as_markup()

async def end():
    global hp, money, stamina, dragon_hp, inventory
    hp = 6
    money = 10
    stamina = 6
    dragon_hp = 10
    save_game_state()
    return save_game_state()

# async def show_player_hp():
#     buttons = []
    
#     if hp >= 6:
#         buttons.append(KeyboardButton(text='❤️❤️❤️❤️❤️❤️'))
#     elif hp >= 5:
#         buttons.append(KeyboardButton(text='❤️❤️❤️❤️❤️'))
#     elif hp >= 4:
#         buttons.append(KeyboardButton(text='❤️❤️❤️❤️'))
#     elif hp >= 3:
#         buttons.append(KeyboardButton(text='❤️❤️❤️'))
#     elif hp >= 2:
#         buttons.append(KeyboardButton(text='❤️❤️'))
#     elif hp >= 1:
#         buttons.append(KeyboardButton(text='❤️'))
    
#     kb = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
#     return kb



