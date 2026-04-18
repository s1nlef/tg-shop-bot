from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def admin_buttons() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup (
        inline_keyboard=[
            [InlineKeyboardButton(text="Change balance🪙", callback_data="change_balance"), InlineKeyboardButton(text="Add game", callback_data="admin_add_game")]
        ]
    )

async def accept_game() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup (
        inline_keyboard=[
            [InlineKeyboardButton(text="Accept✅", callback_data="accept"), InlineKeyboardButton(text="Reject❌", callback_data="reject")]
        ]
    )