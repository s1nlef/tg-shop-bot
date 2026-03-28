from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Catalog📇", callback_data="Catalog")],
        [InlineKeyboardButton(text="Cabinet🗄️", callback_data="Cabinet")],
        [InlineKeyboardButton(text="Cart🛒", callback_data="Cart")]
    ]
)

catalog = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Search🔍", callback_data="Search")],
        [InlineKeyboardButton(text="Factorio", callback_data="Factorio")],
        [InlineKeyboardButton(text="Dishonored", callback_data="Dishonored")],
        [InlineKeyboardButton(text="Back⬅️", callback_data="Menu")]
    ]
)


def product_menu(product_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup (
        inline_keyboard= [
            [InlineKeyboardButton(text="Add to cart", callback_data=f"add_{product_id}")],
            [InlineKeyboardButton(text="Back⬅️", callback_data="Catalog")]
    ]
    )
