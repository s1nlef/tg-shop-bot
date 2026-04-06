from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.database.request import get_all_games

GAMES_PER_PAGE = 5

menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Catalog📇", callback_data="Catalog")],
        [InlineKeyboardButton(text="Cabinet🗄️", callback_data="Cabinet")],
        [InlineKeyboardButton(text="Cart🛒", callback_data="Cart")]
    ]
)

async def catalog(page: int = 0) -> InlineKeyboardMarkup:
    games = await get_all_games()

    start = page * GAMES_PER_PAGE
    end = start + GAMES_PER_PAGE
    page_games = games[start:end]
    keyboard = [
            [InlineKeyboardButton(text=game.name, callback_data=f"game_{game.id}")]
            for game in page_games
        ]
    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton(text="◀️", callback_data=f"catalog_page_{page-1}"))
    if end < len(games):
        nav.append(InlineKeyboardButton(text="▶️", callback_data=f"catalog_page_{page+1}"))
    if nav:
        keyboard.append(nav)
    
    keyboard.append([InlineKeyboardButton(text="Back⬅️", callback_data="Menu")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def product_menu(game_id) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup (
        inline_keyboard= [
            [InlineKeyboardButton(text="Add to cart", callback_data=f"add_{game_id}")],
            [InlineKeyboardButton(text="Back⬅️", callback_data="Catalog")]
        ]
    )
