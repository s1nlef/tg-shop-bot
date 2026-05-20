from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, BaseFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from app.handlers.purchase import ImageResize
import app.database.request as rq
import app.keyboards.admkeyboard as kb
import os

admin = Router()
load_dotenv()

ADMINS_TG_IDS = {
    int(user_id)
    for user_id in os.getenv("ADMINS_TG_IDS", "").split(",")
    if user_id.strip()
}


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user is not None and message.from_user.id in ADMINS_TG_IDS


class Change_Balance(StatesGroup):
    total = State()


class Add_Sneaker_Status(StatesGroup):
    brand = State()
    model = State()
    colorway = State()
    price = State()
    image_url = State()
    stock = State()


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
    if message.text and message.text.isdigit():
        await rq.admin_change_balance(
            tg_id=message.from_user.id, balance=int(message.text)
        )
        await message.answer("Confirmed✅")
    else:
        await message.answer("Try again❌\nThe value must be a number")
    await state.clear()


@admin.callback_query(F.data == "admin_add_sneaker")
async def cmd_add_sneaker(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer("Enter sneaker brand:")
    await state.set_state(Add_Sneaker_Status.brand)


@admin.message(Add_Sneaker_Status.brand)
async def cmd_sneaker_brand(message: Message, state: FSMContext):
    await state.update_data(brand=message.text)
    await state.set_state(Add_Sneaker_Status.model)
    await message.answer("Enter sneaker model:")


@admin.message(Add_Sneaker_Status.model)
async def cmd_sneaker_model(message: Message, state: FSMContext):
    await state.update_data(model=message.text)
    await state.set_state(Add_Sneaker_Status.colorway)
    await message.answer("Enter sneaker colorway:")


@admin.message(Add_Sneaker_Status.colorway)
async def cmd_sneaker_colorway(message: Message, state: FSMContext):
    await state.update_data(colorway=message.text)
    await state.set_state(Add_Sneaker_Status.price)
    await message.answer("Enter sneaker price:")


@admin.message(Add_Sneaker_Status.price)
async def cmd_sneaker_price(message: Message, state: FSMContext):
    if not message.text or not message.text.isdigit():
        await message.answer("❌ Price must be a number. Try again:")
        return
    price = int(message.text)
    if price <= 0:
        await message.answer("❌ Price must be greater than 0. Try again:")
        return
    await state.update_data(price=message.text)
    await state.set_state(Add_Sneaker_Status.image_url)
    await message.answer("Enter image url:")


@admin.message(Add_Sneaker_Status.image_url)
async def cmd_sneaker_image_url(message: Message, state: FSMContext):
    await state.update_data(
        image_url=message.text,
    )
    data = await state.get_data()
    await message.answer_photo(
        caption=f"{data['brand']} {data['model']}\n\nColorway: {data['colorway']}\nPrice: ${
            data['price']
        }",
        photo=data["image_url"],
        reply_markup=await kb.set_sneaker_size_kb(selected_sizes=None),
    )


@admin.callback_query(F.data.startswith("size_"))
async def sneaker_size(call: CallbackQuery, state: FSMContext):
    await call.answer()
    size = call.data.replace("size_", "")
    data = await state.get_data()
    sizes = data.get("sizes", [])
    if size in sizes:
        sizes.remove(size)
    else:
        sizes.append(size)
    await state.update_data(sizes=sizes)
    await call.message.edit_reply_markup(
        reply_markup=await kb.set_sneaker_size_kb(sizes)
    )


@admin.callback_query(F.data == "accept")
async def sneaker_in_stock(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(Add_Sneaker_Status.stock)
    data = await state.get_data()
    sizes = data.get("sizes", [])
    sizes.sort()
    if not sizes:
        await call.message.answer(text="Select at least one size!")
        return

    stock_data = {}
    await state.update_data(stock_data=stock_data, current_idx=0)
    await state.set_state(Add_Sneaker_Status.stock)

    first_size = sizes[0]
    await call.message.answer(text=f"Enter stock for size {first_size}:")


@admin.message(Add_Sneaker_Status.stock)
async def stock_input(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Enter a number!")
        return

    data = await state.get_data()
    sizes = data["sizes"]
    stock_data = data["stock_data"]
    idx = data["current_idx"]
    stock_data[sizes[idx]] = int(message.text)

    idx += 1
    if idx < len(sizes):
        await state.update_data(stock_data=stock_data, current_idx=idx)
        await message.answer(f"Enter stock for size {sizes[idx]}:")
    else:
        await state.update_data(stock_data=stock_data)
        await state.set_state(None)
        sneaker_text = "\n".join(
            f"{size}:{stock}" for size, stock in stock_data.items()
        )
        await message.answer_photo(
            caption=f"{data['brand']} {data['model']}\n\nColorway: {data['colorway']}\nPrice: ${
                data['price']}\nSizes:\n{sneaker_text}",
            photo=data["image_url"],
            reply_markup=await kb.accept_sneaker(),
        )


@admin.callback_query(F.data == "accept_add_sneaker")
async def accept_sneaker(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    await state.clear()
    await rq.add_sneaker(
        brand=data["brand"],
        model=data["model"],
        colorway=data["colorway"],
        price=int(data["price"]),
        image_url=data["image_url"],
        size_table=data["stock_data"],
    )
    await call.message.answer("A new sneaker has been added😊")


@admin.callback_query(F.data == "reject_add_sneaker")
async def reject_sneaker(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.clear()
