from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
import keyboards as kb

user = Router()
cart = []
@user.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(text="Menu", reply_markup=kb.menu)

@user.callback_query(F.data == "Menu")
async def cmd_menu(call: CallbackQuery) -> None:
    await call.answer()
    await call.message.answer(text="Menu", reply_markup=kb.menu)

@user.callback_query(F.data == "Catalog")
async def call_catalog(call: CallbackQuery):
    await call.message.edit_text(text="Catalog", reply_markup=kb.catalog)


@user.callback_query(F.data == "Factorio")
async def call_factorio(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(text="🎮 Factorio\n\nPrice: $15\nGenre: Strategy / Automation\n\nOne of the best games about production automation.", reply_markup=kb.product_menu("Factorio"))


@user.callback_query(F.data == "Dishonored")
async def call_dishonored(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(text="Dishonored\n\nPrice: $10\nGenre: stealth / action\n\nAn immersive first-person stealth game.", reply_markup=kb.product_menu("Dishonored"))

@user.callback_query(F.data.startswith("add_"))
async def cmd_cart_add(call: CallbackQuery) -> None: 
    product = call.data.replace("add_", "")
    cart.append(product)
    await call.answer("Item has been added to your cart✅")
    await call.message.edit_text(text="Catalog", reply_markup=kb.catalog)

@user.callback_query(F.data == "Cart")
async def cmd_cart(call: CallbackQuery) -> None:
    await call.answer()
    if cart:  
        await call.message.answer(f"List of items in your cart:\n- {"\n- ".join(cart)}")
    else:
        await call.message.answer("Your cart is empty😢")


@user.callback_query(F.data == "Cabinet")
async def cmd_cabinet(call: CallbackQuery) -> None:
    await call.answer()
    await call.message.answer(f"Cabinet\nUser: {call.from_user.first_name}\nID: {call.from_user.id}", reply_markup=kb.menu)
