from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandObject
import app.database.request as rq
import  app.keyboards.keyboards as kb

admin = Router()
ADMINS_TG_ID = "1078686275"

# @admin.message("/topup" in F.data)
# async def cmd_topup(message: Message):
#     if message.from_user.id == ADMINS_TG_ID:
#         try: # Get int
#             balance = int(message.text)
#         await rq.change_balance()



@admin.message(Command("topup"))
async def cmd_topup(message: Message, command: CommandObject):
    if str(message.from_user.id) == ADMINS_TG_ID:
        if int(command.args): 
            await rq.admin_change_balance(command.args)