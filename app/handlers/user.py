from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from datetime import datetime
import app.keyboards.keyboards as kb
import app.database.request as rq
import asyncio
user = Router()

class Buy_State(StatesGroup):
    cart = State()
    confirmation = State()
    payment = State()
    receipt = State()

@user.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await rq.set_user(message.from_user.id)
    await state.clear()
    await message.answer(text="Menu", reply_markup=await kb.menu())

@user.callback_query(F.data == "menu")
async def cmd_menu(call: CallbackQuery, state: FSMContext) -> None:
    await call.answer()
    await state.clear()
    await call.message.answer(text="Menu", reply_markup=await kb.menu())

@user.callback_query(F.data == "Catalog")
async def call_catalog(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(text="Catalog", reply_markup= await kb.catalog_kb(0))

@user.callback_query(F.data.startswith("catalog_page_"))
async def cmd_catalog_page(call: CallbackQuery) -> None:
    page = int(call.data.replace("catalog_page_", ""))
    await call.message.edit_text(text="Catalog", reply_markup= await kb.catalog_kb(page))


@user.callback_query(F.data.startswith("game_"))
async def call_game(call: CallbackQuery):
    game_id = int(call.data.replace("game_", ""))
    game = await rq.get_game(game_id=game_id)
    await call.answer()
    await call.message.edit_text(text=f"{game.name}\n\nPrice: ${game.price}\nGenre: {game.genre}\n\n{game.description}", reply_markup= await kb.product_kb(game_id=game_id))


@user.callback_query(F.data.startswith("add_"))
async def cmd_cart_add(call: CallbackQuery) -> None: 
    game_id = int(call.data.replace("add_", ""))
    await rq.add_to_cart(tg_id=call.from_user.id, game_id=game_id)
    await call.answer()
    await call.message.answer(text="Item has been added to cart✅")

@user.callback_query(F.data == "Cabinet")
async def cmd_cabinet(call: CallbackQuery) -> None:
    await call.answer()
    await call.message.answer(text=f"Cabinet\nUser: {call.from_user.first_name}\nID: {call.from_user.id}\nBalance: {(await rq.check_user(call.from_user.id)).balance}", reply_markup=await kb.cabinet_kb())

@user.callback_query(F.data == "Cart")
async def cmd_cart(call: CallbackQuery, state: FSMContext) -> None:
    await call.answer()
    cart = await rq.get_cart(call.from_user.id)
    if cart:
        games = await asyncio.gather(*(rq.get_game(item.game_id) for item in cart))
        game_name = [game.name for game in games]
        sum_price = sum([game.price for game in games])
        await state.update_data(game_name=game_name, sum_price=sum_price)
        await state.set_state(Buy_State.confirmation)
        await call.message.answer(text=f"List of items in your cart:\n{"\n".join(game_name)}\n\nTotal price: {sum_price}", reply_markup= await kb.cart_kb())
    else:
        await call.message.answer(text="Your cart is empty😓")


@user.callback_query(F.data == "Buy", Buy_State.confirmation)
async def cmd_accept_buy(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(Buy_State.payment)
    data = await state.get_data()
    user_balance = await rq.check_user(call.from_user.id)
    if data["sum_price"] <= user_balance.balance:
        await call.message.edit_text(text="Are you confirming your purchase?", reply_markup= await kb.confirm_kb())
    else:
        await call.message.edit_text(text="You don't have enough funds😓", reply_markup= await kb.return_kb())

@user.callback_query(F.data == "confirm_buy", Buy_State.payment)
async def cmd_payment(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    sum_price = data["sum_price"]
    await state.set_state(Buy_State.receipt)
  
    await call.message.edit_text(text=f"Total sum: {sum_price}$", reply_markup= await kb.payment_kb())

@user.callback_query(F.data == "pay_now", Buy_State.receipt)
async def cmd_payment(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    user_id = call.from_user.id
    sum_price = data["sum_price"]
    game_name = data["game_name"]
    order_id = await rq.create_order(call.from_user.id)

    await rq.clean_cart(user_id)
    await rq.change_balance(user_id, sum_price)
    await state.clear()
    await call.message.edit_text(text=f"Receipt🧾\nThe payment was successful✅\nTotal sum: {sum_price}$\nId: {order_id}\nPurchased games:\n{"\n".join(game_name)}\nThank you for your purchase😊", reply_markup= await kb.return_kb())


@user.callback_query(F.data == "history")
async def cmd_history(call: CallbackQuery):
    await call.answer()
    user_id = call.from_user.id
    orders = await rq.all_user_orders(user_id)
    if not orders:
        await call.message.answer("You don't have any orders")
        return

    text = "📜 Order History:\n\n"

    for order in orders:
        items = await rq.get_order_items(order.id)
        games = await asyncio.gather(*(rq.get_game(item.game_id) for item in items))
        game_names = ", ".join(game.name for game in games)
        text += (
            f"Order #{order.id}\n"
            f"Games: {game_names}\n"
            f"Price: {order.price}\n"
            f"Date: {order.created_at.strftime("%d.%m.%Y %H:%M:%S")}\n\n"
        )
    await call.message.answer(text)