from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import app.database.request as rq
import app.keyboards.keyboards as kb


async def admin_buttons() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Change balance🪙", callback_data="change_balance"
                ),
                InlineKeyboardButton(
                    text="Add sneaker👟", callback_data="admin_add_sneaker"
                ),
                InlineKeyboardButton(
                    text="Admin Catalog📦", callback_data="admin_catalog"
                ),
            ]
        ]
    )


async def set_sneaker_size_kb(selected_sizes: list[str] | None) -> InlineKeyboardMarkup:
    sizes = ["35", "36", "37", "38", "39", "40", "41", "42", "43", "44"]
    keyboard = []
    row = []
    for size in sizes:
        text = f"{size}✅" if selected_sizes and size in selected_sizes else size
        row.append(InlineKeyboardButton(text=text, callback_data=f"size_{size}"))
        if len(row) == 5:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    keyboard.append(
        [
            InlineKeyboardButton(text="Accept✅", callback_data="accept"),
            InlineKeyboardButton(text="Reject❌", callback_data="reject"),
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def accept_sneaker() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Accept✅", callback_data="accept_add_sneaker"
                ),
                InlineKeyboardButton(
                    text="Reject❌", callback_data="reject_add_sneaker"
                ),
            ]
        ]
    )


async def brand_kb(page: int = 0) -> InlineKeyboardMarkup:
    sneakers = await rq.get_distinct_brands(page=page, per_page=kb.SNEAKERS_PER_PAGE)
    total_count = await rq.get_distinct_brands(page=None, per_page=None)
    keyboard = [
        [
            InlineKeyboardButton(
                text=f"{sneaker}",
                callback_data=f"admin_brand_{sneaker.replace(" ", "_")}",
            )
        ]
        for sneaker in sneakers
    ]

    nav = []
    if page > 0:
        nav.append(
            InlineKeyboardButton(
                text="◀️", callback_data=f"admin_catalog_page_{page - 1}"
            )
        )
    if (page + 1) * kb.SNEAKERS_PER_PAGE < total_count:
        nav.append(
            InlineKeyboardButton(
                text="▶️", callback_data=f"admin_catalog_page_{page + 1}"
            )
        )
    if nav:
        keyboard.append(nav)

    keyboard.append([InlineKeyboardButton(text="Back⬅️", callback_data="admin")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def sneaker_kb(
    page: int = 0,
    brand_name: str = "",
    size: str | None = None,
    price_max: int | None = None,
) -> InlineKeyboardMarkup:
    sneakers = await rq.get_sneakers_filtered(
        page=page,
        per_page=kb.SNEAKERS_PER_PAGE,
        brand_name=brand_name,
        size=size,
        price_max=price_max,
    )
    total_count = await rq.get_sneakers_brand_count(brand=brand_name)
    keyboard = [
        [
            InlineKeyboardButton(
                text=f"{sneaker.model}",
                callback_data=f"admin_model_{sneaker.model}",
            )
        ]
        for sneaker in sneakers
    ]

    nav = []
    if page > 0:
        nav.append(
            InlineKeyboardButton(
                text="◀️", callback_data=f"admin_brand_page_{page - 1}_{brand_name}"
            )
        )
    if (page + 1) * kb.SNEAKERS_PER_PAGE < total_count:
        nav.append(
            InlineKeyboardButton(
                text="▶️", callback_data=f"admin_brand_page_{page + 1}_{brand_name}"
            )
        )
    if nav:
        keyboard.append(nav)

    keyboard.append(
        [InlineKeyboardButton(text="Back⬅️", callback_data="admin_catalog_page_0")]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def model_kb(sneaker_id: int) -> InlineKeyboardMarkup:
    keyboard = []
    row = []
    sneaker = await rq.get_sneaker(sneaker_id=sneaker_id)
    sneaker_size = await rq.get_sneaker_size(sneaker_id=sneaker_id)

    sneaker_size_sorted = sorted(sneaker_size, key=lambda x: int(x.size))

    for item in sneaker_size_sorted:
        row.append(
            InlineKeyboardButton(
                text=f"{item.size}({item.stock})",
                callback_data=f"admin_change_size_{item.size}_{sneaker.id}",
            )
        )
        if len(row) == 5:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    keyboard.append(
        [
            InlineKeyboardButton(
                text="Delete❌", callback_data=f"delete_sneaker_{sneaker.id}"
            )
        ],
    )
    keyboard.append(
        [
            InlineKeyboardButton(
                text="Back⬅️", callback_data=f"admin_brand_{sneaker.brand}"
            )
        ],
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def comfirm_delete_sneaker() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Yes, I`m sure", callback_data="confirm_delete_sneaker"
                )
            ],
            [InlineKeyboardButton(text="No, leave", callback_data="leave_sneaker")],
        ]
    )
