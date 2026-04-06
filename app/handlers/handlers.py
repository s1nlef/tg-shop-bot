from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
import app.keyboards.keyboards as kb
import app.database.request as rq

user = Router()

@user.message(Command("start"))
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer(text="Menu", reply_markup=kb.menu)

@user.callback_query(F.data == "Menu")
async def cmd_menu(call: CallbackQuery) -> None:
    await call.answer()
    await call.message.answer(text="Menu", reply_markup=kb.menu)

@user.callback_query(F.data == "Catalog")
async def call_catalog(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(text="Catalog", reply_markup= await kb.catalog(0))

@user.callback_query(F.data.startswith("catalog_page_"))
async def cmd_catalog_page(call: CallbackQuery) -> None:
    page = int(call.data.replace("catalog_page_", ""))
    await call.message.edit_text(text="Catalog", reply_markup= await kb.catalog(page))


@user.callback_query(F.data.startswith("game_"))
async def call_game(call: CallbackQuery):
    game_id = int(call.data.replace("game_", ""))
    game = await rq.get_game(game_id=game_id)
    await call.answer()
    await call.message.edit_text(text=f"{game.name}\n\nPrice: ${game.price}\nGenre: {game.genre}\n\n{game.description}", reply_markup= await kb.product_menu(game_id=game_id))


@user.callback_query(F.data.startswith("add_"))
async def cmd_cart_add(call: CallbackQuery) -> None: 
    game_id = int(call.data.replace("add_", ""))
    await rq.add_to_cart(tg_id=call.from_user.id, game_id=game_id)
    await call.answer()
    await call.message.answer("Item has been added to cart✅")

@user.callback_query(F.data == "Cabinet")
async def cmd_cabinet(call: CallbackQuery) -> None:
    await call.answer()
    await call.message.answer(f"Cabinet\nUser: {call.from_user.first_name}\nID: {call.from_user.id}\nBalance: {await rq.check_balance(call.from_user.id)}", reply_markup=kb.menu)
