from aiogram import F, Router
from aiogram.types import CallbackQuery, InputMediaPhoto, FSInputFile, BufferedInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from app.handlers.purchase import ImageResize
import app.database.request as rq
import app.keyboards.keyboards as kb

catalog = Router()


class FilterState(StatesGroup):
    browsing = State()


async def validate_brand_name(brand_name: str) -> str | None:
    all_brands = await rq.get_distinct_brands(page=0, per_page=100)
    if brand_name in all_brands:
        return brand_name
    return None


@catalog.callback_query(F.data == "Catalog")
async def call_catalog(call: CallbackQuery):
    await call.answer()
    await call.message.edit_media(
        media=InputMediaPhoto(
            caption="Каталог", media=FSInputFile("./image/catalog.png")
        ),
        reply_markup=await kb.brand_kb(page=0),
    )


@catalog.callback_query(F.data.startswith("catalog_page_"))
async def cmd_catalog_page(call: CallbackQuery) -> None:
    page = int(call.data.replace("catalog_page_", ""))
    await call.message.edit_media(
        media=InputMediaPhoto(
            caption="Каталог", media=FSInputFile("./image/catalog.png")
        ),
        reply_markup=await kb.brand_kb(page=page),
    )


@catalog.callback_query(F.data.startswith("brand_page_"))
async def cmd_brand_page(call: CallbackQuery) -> None:
    data = call.data.replace("brand_page_", "").split("_", 1)
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


@catalog.callback_query(F.data.startswith("brand_"))
async def call_brand(call: CallbackQuery, state: FSMContext):
    await call.answer()
    brand_name = call.data.replace("brand_", "").replace("_", " ")
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


@catalog.callback_query(F.data.startswith("model_"))
async def call_sneaker(call: CallbackQuery):
    sneaker_model = call.data.replace("model_", "")
    sneaker = await rq.get_sneaker(sneaker_model=str(sneaker_model))

    if not sneaker:
        await call.answer("❌ Product not found", show_alert=True)
        return

    image_bytes = await ImageResize(sneaker.image_url)
    await call.answer()
    await call.message.edit_media(
        media=InputMediaPhoto(
            caption=f"{sneaker.brand} {sneaker.model} {sneaker.colorway}\n\nЦіна: {sneaker.price} грн",
            media=BufferedInputFile(image_bytes, filename="model.jpg"),
        ),
        reply_markup=await kb.model_kb(sneaker_id=sneaker.id),
    )


@catalog.callback_query(F.data.startswith("add_"))
async def cmd_cart_add(call: CallbackQuery) -> None:
    sneaker_data = call.data.replace("add_", "").split("_")
    await rq.add_to_cart(
        tg_id=call.from_user.id, size=sneaker_data[1], sneaker_id=int(sneaker_data[2])
    )
    await call.answer()
    await call.message.answer(text="Товар додано до кошика✅")


# @catalog.callback_query(F.data == "filter")
# async def call_filter(call: CallbackQuery):
#     await call.answer()
#     await call.message.answer(text="Filters", reply_markup=await kb.catalog_filter_kb())
