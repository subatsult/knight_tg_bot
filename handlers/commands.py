from aiogram import Router,F
from aiogram.filters import CommandStart
from aiogram.types import Message,CallbackQuery, Message
import handlers.keyboards as KB
router = Router()
import random
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
    await query.message.answer('You have met a guy who is playing with crowd in a game of two cubes and they sporyat na money_encounter about chetnoe ili nechetnoe, wanna try?', reply_markup=await ludoman())
    await query.message.delete()

@router.callback_query(F.data == 'krasaba')
async def no_play_go_shopping(query: CallbackQuery):
    await query.message.answer('U denied invite for a game and now u r going into the shop for some potions', reply_markup= await KB.baryga())

@router.callback_query(F.data == 'ludka')
async def play(query: CallbackQuery):
    await query.message.answer('Welcome to the Even and Odd game! Guess if the sum of two dice will be even or odd to win points.', reply_markup= await KB.igra())

@router.callback_query(F.data == 'shop')
async def go_to_shop(query: CallbackQuery):
    global money_encounter
    await query.message.answer(f'You are in a shop, here u can buy potion, it costs 10$, you have {money_encounter}', reply_markup= await KB.baryga())
    await query.message.delete()

@router.callback_query(lambda query: query.data in ['even', 'odd'])
async def buy_potion(query: types.CallbackQuery):
    global money_encounter
    number = random.randint(2, 12)
    if number % 2 != 0 and query.data == 'even':
        money_encounter = await append_money()
        await query.message.answer(f'The number popped up is {number}, u have won, now is the time to stop and go shopping, wanna buy a potion', reply_markup= await KB.baryga())
    elif number % 2 == 0 and query.data == 'odd':
        money_encounter = await append_money()
        await query.message.answer(f'The number popped up is {number}, u have won, now is the time to stop and go shopping, wanna buy a potion?', reply_markup= await KB.baryga())
    else:
        money_encounter = await money_lose()
        await query.message.answer(f'Unlucky but the number popped up is {number}, u lost all ur money_encounter, it was so we gotta go defeat the dragon, wanna buy a potion?', reply_markup= await KB.baryga())
    await query.message.delete()
    


@router.callback_query(lambda query: query.data in ['potion', 'potions'])
async def buy_potion(query: types.CallbackQuery):
    global money_encounter
    global inventory_123
    
    if query.data == 'potion' and money_encounter >= 10:
        money_encounter = await money_lose()
        inventory_123.append('potion')
        await query.message.answer('You have bought 1 potion.')
    elif query.data == 'potions' and money_encounter >= 20:
        money_encounter = await money_lose()
        money_encounter = await money_lose()
        inventory_123.append('potion')
        inventory_123.append('potion')
        await query.message.answer('You have bought 2 potions.')
    else:
        await query.message.answer('Sorry, you do not have enough money_encounter.')
    await query.message.answer('Now is the time to face the dragon', reply_markup= await KB.dragon())
    await query.message.delete()

@router.callback_query(lambda query: query.data in ['head', 'body', 'legs'])
async def attack_dragon(query: types.CallbackQuery):
    global dragon_hp
    global hp_encounter

    damage_dealt = 0
    damage_taken = 2  
    # await query.message.answer ('Ur hp is on the top of the keyboard',await KB.show_player_hp())
    hp_encounter -= damage_taken
    if hp_encounter <=0: 
        await query.message.answer('You died. Try again!', reply_markup= await KB.game_reset())
    if query.data == 'head':
        damage_dealt = 2
    elif query.data == 'body':
        damage_dealt = 1
    elif query.data == 'legs':
        damage_dealt = 5
    
    dragon_hp -= damage_dealt
    

    if dragon_hp > 0:
        await query.message.answer(f'You dealt {damage_dealt} damage to the dragon. Player HP: {hp_encounter}, Dragon HP: {dragon_hp}',
                                   reply_markup=await dragon())
    else:
        await query.message.answer('Congratulations! You defeated the dragon!', reply_markup= await KB.game_reset())
    await query.message.delete()


@router.message(F.text == 'Inventory')
async def show_inventory1(message:Message):
    global money_encounter
    await message.delete()
    await message.answer(f'This is ur inventory {inventory_123}, {money_encounter}', reply_markup= await KB.show_inventory())



@router.callback_query(F.data == 'drink_potion')
async def drink_potion_handler(query: CallbackQuery):
    global hp_encounter
    if hp_encounter == 6:
        pass
    elif hp_encounter == 5:
        hp_encounter +=1
    elif hp_encounter <= 4:
        hp_encounter += 2
    await query.answer(f'Drank potion. HP increased to {hp_encounter}.', reply_markup=await drink_potion())
    await query.message.delete()
    return hp_encounter





