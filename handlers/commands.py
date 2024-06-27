from aiogram import Router,F
from aiogram.filters import Command,CommandStart
from aiogram.types import Message,CallbackQuery,FSInputFile,ReplyKeyboardRemove, Message, ReplyKeyboardMarkup, KeyboardButton
import handlers.keyboards as KB
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
router = Router()
import logging
from typing import Any, Dict
from aiogram import types
from handlers.keyboards import *
from encounter import *
from handlers.keyboards import *

@router.message(CommandStart())
async def start(message:Message):
    await message.answer("Ready to go into adventury?",reply_markup= await KB.choice_start())


@router.callback_query(F.data == 'city')
async def go_to_city(query: CallbackQuery):
    await query.message.answer('You have met a guy who is playing with crowd in a game of two cubes and they sporyat na money about chetnoe ili nechetnoe, wanna try?', reply_markup=await ludoman())
    await query.message.delete()

@router.callback_query(F.data == 'krasaba')
async def no_play_go_shopping(query: CallbackQuery):
    await query.message.answer('U denied invite for a game and now u r going into the shop for some potions', reply_markup= await KB.baryga())

@router.callback_query(F.data == 'ludka')
async def play(query: CallbackQuery):
    await query.message.answer('Welcome to the Even and Odd game! Guess if the sum of two dice will be even or odd to win points.', reply_markup= await KB.igra())

@router.callback_query(F.data == 'shop')
async def go_to_shop(query: CallbackQuery):
    global money
    await query.message.answer(f'You are in a shop, here u can buy potion, it costs 10$, you have {money}', reply_markup= await KB.baryga())
    await query.message.delete()

@router.callback_query(lambda query: query.data in ['even', 'odd'])
async def buy_potion(query: types.CallbackQuery):
    global money
    even_odd_dice()

    if query.data == 'odd' and even_odd_dice() == 'odd':
        money + 10
        await query.message.answer('U have won, now is the time to stop and go shopping, wanna buy a potion', reply_markup= await KB.baryga())
    elif query.data == 'even' and even_odd_dice() == 'even':
        money + 10
        await query.message.answer('U have won, now is the time to stop and go shopping, wanna buy a potion?', reply_markup= await KB.baryga())
    else:
        money - 10
        await query.message.answer('Unlucky but i lost all ur money, so we gotta go defeat the dragon, wanna buy a potion?', reply_markup= await KB.baryga())
    await query.message.delete()

@router.callback_query(lambda query: query.data in ['potion', 'potions'])
async def buy_potion(query: types.CallbackQuery):
    global money
    
    if query.data == 'potion' and money >= 10:
        money -= 10
        await query.message.answer('You have bought 1 potion.')
    elif query.data == 'potions' and money >= 20:
        money -= 20
        await query.message.answer('You have bought 2 potions.')
    else:
        await query.message.answer('Sorry, you do not have enough money.')
    await query.message.answer('Now is the time to face the dragon', reply_markup= await KB.dragon())
    await query.message.delete()

@router.callback_query(lambda query: query.data in ['head', 'body', 'legs'])
async def attack_dragon(query: types.CallbackQuery):
    # await query.message.answer ('Ur hp is on the top of the keyboard',await KB.show_player_hp())
    global dragon_hp
    global hp

    damage_dealt = 0
    damage_taken = 2  # Player takes 2 HP damage each time they attack
    
    hp -= damage_taken
    if hp <=0: 
        await query.message.answer('You died. Try again!', reply_markup= await KB.end())
    if query.data == 'head':
        damage_dealt = 2
    elif query.data == 'body':
        damage_dealt = 1
    elif query.data == 'legs':
        damage_dealt = 5
    
    dragon_hp -= damage_dealt
    
    # Check if dragon is defeated or continue battle
    if dragon_hp > 0:
        await query.message.answer(f'You dealt {damage_dealt} damage to the dragon. Player HP: {hp}, Dragon HP: {dragon_hp}',
                                   reply_markup=await dragon())
    else:
        await query.message.answer('Congratulations! You defeated the dragon!', reply_markup= await KB.end())
    
    await query.message.delete()


@router.message(F.text == 'Inventory')
async def show_inventory1(message:Message):
    await message.delete()
    await message.answer(f'This is ur inventory {inventory}', reply_markup= await KB.show_inventory())



@router.callback_query(F.data == 'drink_potion')
async def drink_potion_handler(query: CallbackQuery):
    await query.answer(f'Drank potion. HP increased to {hp}.', reply_markup=await drink_potion())
    await query.message.delete()





