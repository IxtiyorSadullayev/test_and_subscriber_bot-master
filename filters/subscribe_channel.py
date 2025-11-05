from aiogram.filters import Filter
from aiogram import Bot
from aiogram.types import Message
# database

from database.requests import (
    getAllChannelsfromDb
)
# buttons
from helpers.buttons import (
    channels_link
)

class SubScribeChannel(Filter):
    async def __call__(self, message: Message, bot: Bot):
        channels = await getAllChannelsfromDb()
        print(channels)
        if not channels or len(channels)==0:
            return True
        
        tekshiruv = []
        for channel in channels:
            try:
                check_user = await bot.get_chat_member(channel.get("channel_id"), message.from_user.id)
                if not check_user.status in ["member", "administrator", "creator"]:
                    tekshiruv.append(channel)
            except Exception as e:
                pass
        
        if len(tekshiruv) > 0:
            # Foydalanuvchi obuna bo‘lmagan kanallarni ko‘rsatish
            await message.answer(
                "Kechirasiz, siz quyidagi kanallarga obuna bo'lishingiz kerak:",
                reply_markup=await channels_link(tekshiruv)
            )
            return False  # ✅ Filter False qaytarsa, boshqa handlerlar ishlaydi
        
        return True  # ✅ Agar foydalanuvchi barcha kanallarga obuna bo‘lsa, boshqa handlerga o'tadi
