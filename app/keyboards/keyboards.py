from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import app.database.request as rq

SNEAKERS_PER_PAGE = 5


async def menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Catalog📇", callback_data="Catalog")],
            [InlineKeyboardButton(text="Cabinet🗄️", callback_data="Cabinet")],
            [InlineKeyboardButton(text="Cart🛒", callback_data="Cart")],
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

    keyboard.append([InlineKeyboardButton(text="Back⬅️", callback_data="menu")])
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
                text="◀️", callback_data=f"brand_page_{brand_name}_{page - 1}"
            )
        )
    if (page + 1) * SNEAKERS_PER_PAGE < total_count:
        nav.append(
            InlineKeyboardButton(
                text="▶️", callback_data=f"brand_page_{brand_name}_{page + 1}"
            )
        )
    if nav:
        keyboard.append(nav)

    keyboard.append(
        [InlineKeyboardButton(text="Back⬅️", callback_data="catalog_page_0")]
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
        InlineKeyboardButton(text=f"❌ Reset filters", callback_data="filters_reset")
    ]

    show = [InlineKeyboardButton(text="Apply 🔍", callback_data="filter_apply")]

    return InlineKeyboardMarkup(inline_keyboard=[brand_row, reset, show])


async def product_kb(sneaker_model) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Add to cart", callback_data=f"add_{sneaker_model}"
                )
            ],
            [InlineKeyboardButton(text="Back⬅️", callback_data="Catalog")],
        ]
    )


async def cart_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"Buy✅", callback_data="Buy")],
            [InlineKeyboardButton(text=f"Back⬅️", callback_data="menu")],
        ]
    )


async def confirm_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Accept", callback_data="confirm_buy"),
                InlineKeyboardButton(text="❌ Deny", callback_data="menu"),
            ]
        ]
    )


async def payment_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💳 Pay", callback_data="pay_now"),
                InlineKeyboardButton(text="↩️ Back", callback_data="menu"),
            ]
        ]
    )


async def return_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="↩️ Back", callback_data="menu")]]
    )


async def cabinet_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Order History", callback_data="history")],
            [InlineKeyboardButton(text="↩️ Back", callback_data="menu")],
        ]
    )
