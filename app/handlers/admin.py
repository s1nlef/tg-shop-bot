from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command, CommandObject, BaseFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from datetime import datetime
import app.database.request as rq
import  app.keyboards.admkeyboard as kb
from dotenv import load_dotenv
import os

admin = Router()
load_dotenv()
ADMINS_TG_ID = int(os.getenv("ADMINS_TG_ID")) 


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == ADMINS_TG_ID

class Change_Balance(StatesGroup):
    total = State()
    
class Add_Game_Status(StatesGroup):
    name = State()
    genre = State()
    date_release = State()
    description = State()
    price = State()

admin.message.filter(IsAdmin())
admin.callback_query.filter(IsAdmin())
@admin.message(Command("admin"))
async def cmd_admin(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text="Admin Menu", reply_markup=await kb.admin_buttons())


@admin.callback_query(F.data == "change_balance")
async def cmd_change_balance(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(Change_Balance.total)
    await call.message.answer(text="Enter the new balance")

@admin.message(Change_Balance.total)
async def cmd_new_balance(message: Message, state: FSMContext):
    await state.clear()
    if message.text and message.text.isdigit():
        await rq.admin_change_balance(tg_id=message.from_user.id, balance=int(message.text))
        await message.answer("Confirmed✅")
    else:
        await message.answer("Try again❌\nThe value must be a number")

@admin.callback_query(F.data == "admin_add_game")
async def cmd_add_game(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer("Enter game name:")
    await state.set_state(Add_Game_Status.name)
    
@admin.message(Add_Game_Status.name)
async def cmd_game_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Add_Game_Status.genre)
    await message.answer("Enter game genre:")


@admin.message(Add_Game_Status.genre)
async def cmd_game_genre(message: Message, state: FSMContext):
    await state.update_data(genre=message.text)
    await state.set_state(Add_Game_Status.date_release)
    await message.answer("Enter game date release:")

@admin.message(Add_Game_Status.date_release)
async def cmd_game_date_release(message: Message, state: FSMContext):
    await state.update_data(date_release=message.text)
    await state.set_state(Add_Game_Status.description)
    await message.answer("Enter game description:")


@admin.message(Add_Game_Status.description)
async def cmd_game_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(Add_Game_Status.price)
    await message.answer("Enter game price:")


@admin.message(Add_Game_Status.price)
async def cmd_game_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    data = await state.get_data()
    await message.answer(text=f"{data["name"]}\n\nPrice: ${data["price"]}\nGenre: {data["genre"]}\n\n{data["description"]}", reply_markup= await kb.accept_game())

@admin.callback_query(F.data == "accept")
async def accept_game(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    await state.clear()
    date_release = datetime.strptime(data["date_release"], "%B %d, %Y").date()

    await rq.add_game(name=data["name"], genre=data["genre"], daterelease=date_release, description=data["description"],price=int(data["price"]))   
    await call.message.answer("The game has been successfully added😊") 


@admin.callback_query(F.data == "reject")   
async def reject_game(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.clear()