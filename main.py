from helpers.bot import bot, dp
from asyncio import run
import logging

# route yuklamalari
from routes.startRouter import startRouter
from routes.userRouter import user
from routes.adminRouter import admin


# get baza
from database.models import createTanlov, createTest, createUser_table, createUserTest, createNotification



async def runBot():
    createUserTest()
    createUser_table()
    createTanlov()
    createTest()
    createNotification()
    logging.basicConfig(level=logging.INFO)
    dp.include_router(startRouter)
    dp.include_router(user)
    dp.include_router(admin)
    await dp.start_polling(bot)


if __name__=="__main__":
    try:
        run(runBot())
    except Exception as e:
        # bot.send_message()
        print("Hatolik mavjud", e)