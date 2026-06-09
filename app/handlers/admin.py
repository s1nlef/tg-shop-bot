from aiogram import F, Router
from aiogram.types import (
    FSInputFile,
    Message,
    CallbackQuery,
    InputMediaPhoto,
    BufferedInputFile,
)
from aiogram.filters import Command, BaseFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from app.handlers.catalog import ImageResize, validate_brand_name
from dotenv import load_dotenv
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


class FilterState(StatesGroup):
    browsing = State()


class Add_Sneaker_Status(StatesGroup):
    brand = State()
    model = State()
    colorway = State()
    price = State()
    image_url = State()
    stock = State()


class DeleteSneaker(StatesGroup):
    confirm = State()


class ChangeStockSneaker(StatesGroup):
    changesize = State()


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


@admin.callback_query(F.data == "admin_catalog")
async def sneaker_model_delete(call: CallbackQuery):
    await call.answer()
    await call.message.answer_photo(
        photo=FSInputFile(path="./image/catalog.png"),
        caption="Admin Catalog",
        reply_markup=await kb.brand_kb(page=0),
    )


@admin.callback_query(F.data.startswith("admin_catalog_page_"))
async def cmd_catalog_page(call: CallbackQuery) -> None:
    page = int(call.data.replace("admin_catalog_page_", ""))
    await call.message.edit_media(
        media=InputMediaPhoto(
            caption="Admin Catalog", media=FSInputFile("./image/catalog.png")
        ),
        reply_markup=await kb.brand_kb(page=page),
    )


@admin.callback_query(F.data.startswith("admin_brand_page_"))
async def cmd_brand_page(call: CallbackQuery) -> None:
    data = call.data.replace("admin_brand_page_", "").split("_", 1)
    page = int(data[0])
    brand_name = data[1].replace("_", " ")

    valid_brand_name = await validate_brand_name(brand_name)
    if not valid_brand_name:
        await call.answer("❌ Unknown brand", show_alert=True)
        return

    safe_filename = valid_brand_name.replace(" ", "")
    await call.message.edit_media(
        media=InputMediaPhoto(media=FSInputFile(f"./image/{safe_filename}.png")),
        reply_markup=await kb.sneaker_kb(brand_name=brand_name, page=page),
    )


@admin.callback_query(F.data.startswith("admin_brand_"))
async def call_brand(call: CallbackQuery, state: FSMContext):
    await call.answer()
    brand_name = call.data.replace("admin_brand_", "").replace("_", " ")
    valid_brand_name = await validate_brand_name(brand_name=brand_name)

    if not valid_brand_name:
        await call.answer("❌ Unknown brand", show_alert=True)
        return

    await state.set_state(FilterState.browsing)
    await state.update_data(brand=brand_name, size=None, price_max=None, page=0)

    safe_filename = valid_brand_name.replace(" ", "")
    await call.message.edit_media(
        media=InputMediaPhoto(media=FSInputFile(f"./image/{safe_filename}.png")),
        reply_markup=await kb.sneaker_kb(brand_name=brand_name),
    )


@admin.callback_query(F.data.startswith("admin_model_"))
async def call_sneaker(call: CallbackQuery):
    sneaker_model = call.data.replace("admin_model_", "")
    sneaker = await rq.get_sneaker(sneaker_model=str(sneaker_model))

    if not sneaker:
        await call.answer("❌ Product not found", show_alert=True)
        return

    image_bytes = await ImageResize(sneaker.image_url)
    await call.answer()
    await call.message.edit_media(
        media=InputMediaPhoto(
            caption=f"{sneaker.brand} {sneaker.model} {sneaker.colorway}\n\nPrice: {sneaker.price} $",
            media=BufferedInputFile(image_bytes, filename="model.jpg"),
        ),
        reply_markup=await kb.model_kb(sneaker_id=sneaker.id),
    )


@admin.callback_query(F.data.startswith("delete_sneaker_"))
async def processDeletion(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(DeleteSneaker.confirm)
    sneaker_id = call.data.replace("delete_sneaker_", "")
    sneaker = await rq.get_sneaker(sneaker_id=int(sneaker_id))
    await state.set_data({"sneaker_id": sneaker_id})
    await call.message.answer(
        text=f"You confirm the deletion? \nModel: {sneaker.model}",
        reply_markup=await kb.comfirm_delete_sneaker(),
    )


@admin.callback_query(F.data == "confirm_delete_sneaker", DeleteSneaker.confirm)
async def deleteSneaker(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await rq.delete_sneaker(int(data["sneaker_id"]))
    await call.message.answer(text="Model was deleted")
    await state.clear()


@admin.callback_query(F.data == "leave_sneaker", DeleteSneaker.confirm)
async def leaveSneaker(call: CallbackQuery, state: FSMContext):
    await call.answer(text="Sneaker keep")
    await state.clear()


@admin.callback_query(F.data.startswith("admin_change_size_"))
async def changeStockSize(call: CallbackQuery, state: FSMContext):
    await call.answer()
    parts = call.data.replace("admin_change_size_", "").split("_")
    size = parts[0]
    sneaker_id = parts[1]
    await state.set_state(ChangeStockSneaker.changesize)
    await state.set_data(
        {
            "size": size,
            "sneaker_id": sneaker_id,
            "message_id": call.message.message_id,
            "chat_id": call.message.chat.id,
        }
    )
    await call.message.answer("Enter new stock:")


@admin.message(ChangeStockSneaker.changesize)
async def chooseStockSize(message: Message, state: FSMContext):
    newstock = message.text
    if not newstock.isdigit():
        await message.answer(text="Enter a number")
        return
    data = await state.get_data()
    sneaker_id = int(data["sneaker_id"])

    await rq.changeStock(sneaker_id=sneaker_id, size=data["size"], stock=newstock)
    sneaker = await rq.get_sneaker(sneaker_id=sneaker_id)

    image_url = sneaker.image_url
    image_bytes = await ImageResize(image_url)

    await message.bot.edit_message_media(
        chat_id=data["chat_id"],
        message_id=data["message_id"],
        media=InputMediaPhoto(
            media=BufferedInputFile(image_bytes, filename="model.jpg"),
            caption=f"{sneaker.brand} {sneaker.model} {sneaker.colorway}\n\nPrice: {sneaker.price} $",
        ),
        reply_markup=await kb.model_kb(sneaker_id=sneaker_id),
    )

    await message.answer("✅ Stock updated")
    await state.clear()
