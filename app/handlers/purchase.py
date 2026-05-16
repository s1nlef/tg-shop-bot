from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiohttp import ClientSession
from PIL import Image
from io import BytesIO
import app.keyboards.keyboards as kb
import app.database.request as rq

purchase = Router()


class BuyState(StatesGroup):
    cart = State()
    confirmation = State()
    payment = State()
    receipt = State()


async def ImageResize(image_url: str, width=1200, height=1080) -> bytes:
    async with ClientSession() as session:
        async with session.get(image_url) as response:
            content = await response.read()
            img = Image.open(BytesIO(content))

            img = img.convert("RGB")
            img.thumbnail((width, height), Image.Resampling.LANCZOS)

            output = BytesIO()
            img.save(output, format="JPEG", quality=85)
            return output.getvalue()


@purchase.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await rq.set_user(message.from_user.id)
    await state.clear()
    await message.answer_photo(
        caption="Menu",
        photo=FSInputFile("./image/menu.png"),
        reply_markup=await kb.menu(),
    )


@purchase.callback_query(F.data == "menu")
async def cmd_menu(call: CallbackQuery, state: FSMContext) -> None:
    await call.answer()
    await state.clear()
    await call.message.answer_photo(
        caption="Menu",
        photo=FSInputFile("./image/menu.png"),
        reply_markup=await kb.menu(),
    )


@purchase.callback_query(F.data == "Cabinet")
async def cmd_cabinet(call: CallbackQuery) -> None:
    await call.answer()
    await call.message.answer(
        text=f"Cabinet\nUser: {call.from_user.first_name}\nID: {call.from_user.id}\nBalance: {(await rq.check_user(call.from_user.id)).balance}",
        reply_markup=await kb.cabinet_kb(),
    )


@purchase.callback_query(F.data == "Cart")
async def cmd_cart(call: CallbackQuery, state: FSMContext) -> None:
    await call.answer()
    cart = await rq.get_cart(call.from_user.id)
    if cart:
        sneaker_ids = [item.sneaker_id for item in cart]
        sneakers = await rq.get_sneakers_by_ids(sneaker_ids=sneaker_ids)
        sneakers_map = {sneaker.id: sneaker for sneaker in sneakers}
        quantity = [item.quantity for item in cart if item.sneaker_id in sneakers_map]
        total = sum(
            sneakers_map[item.sneaker_id].price * item.quantity
            for item in cart
            if item.sneaker_id in sneakers_map
        )
        sneakers_text = "\n".join(
            f"{sneakers_map[item.sneaker_id].brand} {sneakers_map[item.sneaker_id].model} {sneakers_map[item.sneaker_id].colorway} x{item.quantity} — {sneakers_map[item.sneaker_id].price * item.quantity}"
            for item in cart
            if item.sneaker_id in sneakers_map
        )
        order_table = {
            "items": [
                {"sneaker_id": s.id, "price": s.price, "quantity": q}
                for s, q in zip(sneakers, quantity)
            ],
            "total": total,
        }
        await state.update_data(
            sneakers_text=sneakers_text, total=total, order_table=order_table
        )
        await state.set_state(BuyState.confirmation)
        await call.message.answer(
            text=f"List of items in your cart:\n{sneakers_text}\n\nTotal price: {
                total
            }",
            reply_markup=await kb.cart_kb(),
        )
    else:
        await call.message.answer(text="Your cart is empty😓")


@purchase.callback_query(F.data == "Buy", BuyState.confirmation)
async def cmd_accept_buy(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(BuyState.payment)
    await call.message.edit_text(
        text="Are you confirming your purchase?", reply_markup=await kb.confirm_kb()
    )


@purchase.callback_query(F.data == "confirm_buy", BuyState.payment)
async def cmd_confirm_buy(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    total = data["total"]
    user_balance = await rq.check_user(call.from_user.id)
    if total <= user_balance.balance:
        await state.set_state(BuyState.receipt)
        await call.message.edit_text(
            text=f"Total sum: {total}$", reply_markup=await kb.payment_kb()
        )
    else:
        await state.clear()
        await call.message.edit_text(
            text="You don't have enough funds😓", reply_markup=await kb.return_kb()
        )


@purchase.callback_query(F.data == "pay_now", BuyState.receipt)
async def cmd_pay_now(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    user_id = call.from_user.id
    total = data["total"]
    sneakers_text = data["sneakers_text"]
    order_id = await rq.purchase(tg_id=user_id, order_table=data["order_table"])

    await rq.clean_cart(user_id)
    await state.clear()
    await call.message.edit_text(
        text=f"Receipt🧾\nThe payment was successful✅\nTotal sum: {total}$\nId: {order_id}\nPurchased sneakers:\n{sneakers_text}\nThank you for your purchase😊",
        reply_markup=await kb.return_kb(),
    )


@purchase.callback_query(F.data == "history")
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
        sneakers = await rq.get_sneakers_by_ids(
            sneaker_ids=[item.sneaker_id for item in items]
        )
        sneakers_map = {sneaker.id: sneaker for sneaker in sneakers}
        sneakers_text = "\n".join(
            f"{sneakers_map[item.sneaker_id].brand} {sneakers_map[item.sneaker_id].model} {sneakers_map[item.sneaker_id].colorway} x{item.quantity} — {sneakers_map[item.sneaker_id].price * item.quantity}"
            for item in items
            if item.sneaker_id in sneakers_map
        )
        text += (
            f"Order #{order.id}\n"
            f"Sneakers: \n{sneakers_text}\n"
            f"Total: {order.price}\n"
            f"Date: {order.created_at.strftime('%d.%m.%Y %H:%M:%S')}\n\n"
        )
    await call.message.answer(text)
