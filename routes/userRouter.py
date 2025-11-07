from aiogram import Router, F 
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from states.userState import TestAnswersFromUser, UserActions

###########################################################################################################
###########################################################################################################
###########################################################################################################

user = Router()

@user.message(F.text == "Taklif havolam")
async def taklifHavolasi(message: Message):
    tg_id = message.from_user.id
    text = f"""Sizning taklif havolangiz:
    "Ushbu taklif havolani boshqalarga yuborishingiz mumkin: 
    https://t.me/darslik1202_bot?start={tg_id}"

    Bu havolani guruh va chatlarda tarqating va ballarga sazovor bo'ling
    """
    
    # Matnni yuborish
    await message.answer(text=text)



@user.message(UserActions.work_test)
async def userActions_work_test(message: Message, state: FSMContext):
    pass
    # user test ishlash jarayoni 

###########################################################################################################
###########################################################################################################
###########################################################################################################
@user.message(TestAnswersFromUser.test_code)
async def testAnswerfromUser_test_code(message: Message, state: FSMContext):
    pass
    # user test ishlash jarayoni test kodini so'rash jarayoni

@user.message(TestAnswersFromUser.answers)
async def testAnswerfromUser_answers(message: Message, state: FSMContext):
    pass
    # user test kalitlarini kiritish jarayoni
    
@user.message(TestAnswersFromUser.tekshiruv)
async def testAnswerfromUser_tekshiruv(message: Message, state: FSMContext):
    pass
    # user test ishlash jarayoni test kodini so'rash jarayoni tugagandan keyin tekshirish joyi.
    
    