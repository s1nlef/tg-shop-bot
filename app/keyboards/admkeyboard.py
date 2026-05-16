from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def admin_buttons() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Change balance🪙", callback_data="change_balance"
                ),
                InlineKeyboardButton(
                    text="Add sneaker", callback_data="admin_add_sneaker"
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
