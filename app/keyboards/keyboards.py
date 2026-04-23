from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import app.database.request as rq

GAMES_PER_PAGE = 5


async def menu() -> InlineKeyboardMarkup:
     return InlineKeyboardMarkup(
          inline_keyboard= [
            [InlineKeyboardButton(text="Catalog📇", callback_data="Catalog")],
            [InlineKeyboardButton(text="Cabinet🗄️", callback_data="Cabinet")],
            [InlineKeyboardButton(text="Cart🛒", callback_data="Cart")]    
        ]
     )

async def catalog_kb(page: int = 0) -> InlineKeyboardMarkup:
    games = await rq.get_all_games(page=page, per_page=GAMES_PER_PAGE)
    total_count = await rq.get_games_count()

    keyboard = [
        [InlineKeyboardButton(text=game.name, callback_data=f"game_{game.id}")]
        for game in games
    ]

    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton(text="◀️", callback_data=f"catalog_page_{page - 1}"))
    if (page + 1) * GAMES_PER_PAGE < total_count:
        nav.append(InlineKeyboardButton(text="▶️", callback_data=f"catalog_page_{page + 1}"))
    if nav:
        keyboard.append(nav)

    keyboard.append([InlineKeyboardButton(text="Back⬅️", callback_data="menu")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

async def product_kb(game_id) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup (
        inline_keyboard= [
            [InlineKeyboardButton(text="Add to cart", callback_data=f"add_{game_id}")],
            [InlineKeyboardButton(text="Back⬅️", callback_data="Catalog")]
        ]
    )

async def cart_kb() -> InlineKeyboardMarkup:
     return InlineKeyboardMarkup (
          inline_keyboard= [
               [InlineKeyboardButton(text=f"Buy✅", callback_data="Buy")],
               [InlineKeyboardButton(text=f"Back⬅️", callback_data="menu")]
          ]
     )


async def confirm_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Accept", callback_data="confirm_buy"),
            InlineKeyboardButton(text="❌ Deny", callback_data="menu")
        ]
    ])


async def payment_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="💳 Pay", callback_data="pay_now"),
            InlineKeyboardButton(text="↩️ Back", callback_data="menu")
        ]
    ])
     
async def return_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="↩️ Back", callback_data="menu")]
    ])

async def cabinet_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
         inline_keyboard= [
              [InlineKeyboardButton(text="Order History", callback_data="history")],
              [InlineKeyboardButton(text="↩️ Back", callback_data="menu")]
         ]
    ) 