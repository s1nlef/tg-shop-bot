from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import app.database.request as rq

SNEAKERS_PER_PAGE = 5


async def menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Каталог📇", callback_data="Catalog")],
            [InlineKeyboardButton(text="Кабінет🗄️", callback_data="Cabinet")],
            [InlineKeyboardButton(text="Кошик🛒", callback_data="Cart")],
        ]
    )


async def brand_kb(page: int = 0) -> InlineKeyboardMarkup:
    sneakers = await rq.get_distinct_brands(page=page, per_page=SNEAKERS_PER_PAGE)
    total_count = await rq.get_distinct_brands(page=None, per_page=None)
    keyboard = [
        [
            InlineKeyboardButton(
                text=f"{sneaker}",
                callback_data=f"brand_{sneaker.replace(" ", "_")}",
            )
        ]
        for sneaker in sneakers
    ]

    nav = []
    if page > 0:
        nav.append(
            InlineKeyboardButton(text="◀️", callback_data=f"catalog_page_{page - 1}")
        )
    if (page + 1) * SNEAKERS_PER_PAGE < total_count:
        nav.append(
            InlineKeyboardButton(text="▶️", callback_data=f"catalog_page_{page + 1}")
        )
    if nav:
        keyboard.append(nav)

    keyboard.append([InlineKeyboardButton(text="Назад⬅️", callback_data="menu")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def sneaker_kb(
    page: int = 0,
    brand_name: str = "",
    size: str | None = None,
    price_max: int | None = None,
) -> InlineKeyboardMarkup:
    sneakers = await rq.get_sneakers_filtered(
        page=page,
        per_page=SNEAKERS_PER_PAGE,
        brand_name=brand_name,
        size=size,
        price_max=price_max,
    )
    total_count = await rq.get_sneakers_brand_count(brand=brand_name)
    keyboard = [
        [
            InlineKeyboardButton(
                text=f"{sneaker.model}",
                callback_data=f"model_{sneaker.model}",
            )
        ]
        for sneaker in sneakers
    ]

    nav = []
    if page > 0:
        nav.append(
            InlineKeyboardButton(
                text="◀️", callback_data=f"brand_page_{page - 1}_{brand_name}"
            )
        )
    if (page + 1) * SNEAKERS_PER_PAGE < total_count:
        nav.append(
            InlineKeyboardButton(
                text="▶️", callback_data=f"brand_page_{page + 1}_{brand_name}"
            )
        )
    if nav:
        keyboard.append(nav)

    keyboard.append(
        [InlineKeyboardButton(text="Назад⬅️", callback_data="catalog_page_0")]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def catalog_filter_kb(
    brands: list[str],
    active_brand: str | None,
    active_size: str | None,
    active_price: str | None,
) -> InlineKeyboardMarkup:
    brand_row = [
        InlineKeyboardButton(
            text=f"{'✅ ' if brand == active_brand else ''}{brand}",
            callback_data=f"filter_brand_{brand}",
        )
        for brand in brands
    ]

    reset = [
        InlineKeyboardButton(text=f"❌ Скинути фільтри", callback_data="filters_reset")
    ]

    show = [InlineKeyboardButton(text="Застосувати 🔍", callback_data="filter_apply")]

    return InlineKeyboardMarkup(inline_keyboard=[brand_row, reset, show])


async def model_kb(sneaker_id: int) -> InlineKeyboardMarkup:
    keyboard = []
    row = []
    sneaker = await rq.get_sneaker(sneaker_id=sneaker_id)
    sneaker_size = await rq.get_sneaker_size(sneaker_id=sneaker_id)
    sneaker_table = {
        "size": [item.size for item in sneaker_size],
        "stock": [item.stock for item in sneaker_size],
    }
    for size, stock in zip(sneaker_table["size"], sneaker_table["stock"]):
        if stock > 0:
            row.append(
                InlineKeyboardButton(
                    text=size, callback_data=f"add_{sneaker.model}_{size}_{sneaker.id}"
                )
            )
            if len(row) == 5:
                keyboard.append(row)
                row = []
    if row:
        keyboard.append(row)

    keyboard.append(
        [InlineKeyboardButton(text="Назад⬅️", callback_data=f"brand_{sneaker.brand}")]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def cart_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"📦 Оформити замовлення", callback_data="Buy")],
            [
                InlineKeyboardButton(
                    text=f"❌ Видалити товар", callback_data="cart_remove_item"
                )
            ],
            [InlineKeyboardButton(text=f"Назад⬅️", callback_data="menu")],
        ]
    )


async def cart_remove_kb(cart_items: dict) -> InlineKeyboardMarkup:
    keyboard = []
    for item in cart_items:
        sneaker = await rq.get_sneaker(sneaker_id=item["sneaker_id"])
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"❌ {sneaker.brand} {sneaker.model}",
                    callback_data=f"remove_{item['sneaker_id']}",
                )
            ]
        )
    keyboard.append([InlineKeyboardButton(text="↩️ Назад", callback_data="Cart")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def confirm_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Підтвердити", callback_data="confirm_buy"
                ),
                InlineKeyboardButton(text="❌ Скасувати", callback_data="menu"),
            ]
        ]
    )


async def payment_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📦 Оформити", callback_data="pay_now"),
                InlineKeyboardButton(text="↩️ Назад", callback_data="menu"),
            ]
        ]
    )


async def return_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="↩️ Назад", callback_data="menu")]]
    )


async def cabinet_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Історія замовлень", callback_data="history")],
            [InlineKeyboardButton(text="↩️ Назад", callback_data="menu")],
        ]
    )
