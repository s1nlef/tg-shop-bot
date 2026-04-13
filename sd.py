from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

BOT_TOKEN = "YOUR_TOKEN_HERE"

router = Router()


class BuyItem(StatesGroup):
    cart = State()
    confirmation = State()
    payment = State()
    receipt = State()


def confirm_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_buy"),
            InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_buy"),
        ]
    ])


def payment_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="💳 Оплатить", callback_data="pay_now"),
            InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_confirm"),
        ]
    ])


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer(
        "Добро пожаловать! Напиши /buy, чтобы начать покупку."
    )


@router.message(Command("buy"))
async def buy_start(message: Message, state: FSMContext):
    # Пример корзины
    cart_items = [
        {"name": "Футболка", "price": 500},
        {"name": "Кепка", "price": 300},
    ]
    total = sum(item["price"] for item in cart_items)

    await state.update_data(cart_items=cart_items, total=total)
    await state.set_state(BuyItem.confirmation)

    text = "🛒 Ваша корзина:\n"
    for item in cart_items:
        text += f"- {item['name']} — {item['price']} грн\n"
    text += f"\nИтого: {total} грн\n\nПодтвердить заказ?"

    await message.answer(text, reply_markup=confirm_kb())


@router.callback_query(F.data == "confirm_buy", BuyItem.confirmation)
async def confirm_buy(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BuyItem.payment)

    await callback.message.edit_text(
        "Подтверждение принято. Перейдите к оплате.",
        reply_markup=payment_kb()
    )
    await callback.answer()


@router.callback_query(F.data == "cancel_buy", BuyItem.confirmation)
async def cancel_buy(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Заказ отменён.")
    await callback.answer()


@router.callback_query(F.data == "back_to_confirm", BuyItem.payment)
async def back_to_confirm(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    total = data["total"]

    await state.set_state(BuyItem.confirmation)
    await callback.message.edit_text(
        f"Возврат к подтверждению.\nСумма заказа: {total} грн",
        reply_markup=confirm_kb()
    )
    await callback.answer()


@router.callback_query(F.data == "pay_now", BuyItem.payment)
async def pay_now(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    total = data["total"]

    # Здесь обычно идёт реальная проверка оплаты
    await state.set_state(BuyItem.receipt)

    receipt_text = (
        "✅ Оплата прошла успешно!\n\n"
        f"Сумма: {total} грн\n"
        "Чек: #123456\n"
        "Спасибо за покупку!"
    )

    await callback.message.edit_text(receipt_text)
    await state.clear()
    await callback.answer()


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())