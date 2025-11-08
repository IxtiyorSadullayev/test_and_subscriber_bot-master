from aiogram import Router, F 
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
import re
from states.userState import TestAnswersFromUser, UserActions


# db
from database.testRequests import getTestById
from database.usertestRequests import createuserTest, getTekshiruvTestUser, getUserTesttoUserTest

# btn
from helpers.buttons import yes_or_no


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



@user.message(F.text == "Test ishlash")
async def userActions_work_test(message: Message, state: FSMContext):
    await message.answer("Test kodini kiriting. Test kodi raqam bo'lishi kerak.")
    await state.set_state(TestAnswersFromUser.test_code)
    # user test ishlash jarayoni 

###########################################################################################################
###########################################################################################################
###########################################################################################################
@user.message(TestAnswersFromUser.test_code)
async def testAnswerfromUser_test_code(message: Message, state: FSMContext):
    test_code = message.text 
    if len(test_code) == 0 or not test_code.isdigit():
        await message.answer("Test kodini kiriting. Test kodi raqam bo'lishi kerak.")
        await state.set_state(TestAnswersFromUser.test_code)
        return
    tekshiruv = getTekshiruvTestUser(tg_id=message.from_user.id, test_id=test_code)
    if not tekshiruv:
        await message.answer("Kechirasiz siz ushbu testni oldin ishlagansiz. 2-marotaba ishlashga ruxsat berilmagan.")
        await state.clear()
        return
    test = getTestById(test_id=test_code)
    if not test:
        await message.answer("Kechirasiz siz kiritgan test kodi mavjud emas yokida aktive emas.")
        return
    if test.get("published") != "ACTIVE":
        await message.answer("Kechirasiz siz kiritgan test kodi mavjud emas yokida aktive emas.")
        return
    await state.update_data(test_code = test_code)
    await state.update_data(count_question=test.get("count_question"))
    await message.answer_document(test.get("test_file"), caption=f"Ushbu testda jami {test.get("count_question")} ta test mavjud.")
    await message.answer("""Test javoblarini kiriting: 
                         Test javoblarini quyidagi shaklda yozishingiz mumkin:
🔹 absd...
🔹 1a2b3c4d...""")
    await state.set_state(TestAnswersFromUser.answers)

    # user test ishlash jarayoni test kodini so'rash jarayoni

@user.message(TestAnswersFromUser.answers)
async def testAnswerfromUser_answers(message: Message, state: FSMContext):
    answers = message.text
    data = await state.get_data()
    count_questions = data.get("count_question")
    matches = re.findall(r'(\d)([a-zA-Z])', answers)
    if len(answers)==0:
        await message.answer("""Test javoblarini kiriting: 
                         Test javoblarini quyidagi shaklda yozishingiz mumkin:
🔹 absd...
🔹 1a2b3c4d...""")
        await state.set_state(TestAnswersFromUser.answers)
        return
    elif len(answers) != int(count_questions) and len(matches) != int(count_questions):
        await message.answer("""Test javoblarini kiriting: 
                         Test javoblarini quyidagi shaklda yozishingiz mumkin:
🔹 absd...
🔹 1a2b3c4d...""")
        await state.set_state(TestAnswersFromUser.answers)
        return
    javob_korinishi = []
    if len(answers) == int(count_questions):
        for i in range(len(answers)):
            javob_korinishi.append(f"{i+1} {answers[i]}")
    elif len(matches) == int(count_questions):
        for i in range(1, len(matches)+1):
            javob_korinishi.append(f"{i//10 + i if i<10 else i//10+i-1} {matches[i-1][1]}")
    
    # 
    # Javoblarni tekshirish jarayoni.

    await state.update_data(answers = ",".join(javob_korinishi))
    await message.answer(f"Javoblaringizni tekshirib ko'ring. Javoblar: \n{", ".join(javob_korinishi)}", reply_markup=yes_or_no("user"))
    await state.set_state(TestAnswersFromUser.tekshiruv)

    # user test kalitlarini kiritish jarayoni
    
@user.callback_query(TestAnswersFromUser.tekshiruv)
async def testAnswerfromUser_tekshiruv(query: CallbackQuery, state: FSMContext):
    check = query.data
    if check == "useryes":
        tg_id = query.message.chat.id
        data =await state.get_data()
        answers = data.get("answers").split(",")
        test_id=data.get("test_code")
        test = getTestById(test_id = test_id )
        test_answers = test.get("answers").split(",")
        tekshiruv=[]
        accepted=0
        for i in range(len(test_answers)):
            if test_answers[i][-1] == answers[i][-1]:
                tekshiruv.append(f"{i+1 } ✅")
                accepted+=1
            else:
                tekshiruv.append(f"{i+1 } 🚫")
        natija = createuserTest(tg_id=tg_id, test_id=test_id, answers=", ".join(answers), score=accepted, result=", ".join(tekshiruv))
        if not natija:
            await query.answer("ok")
            await query.message.answer("Ma'lumotlarni saqlashda hatolikga yo'lq qo'yildi")
            return
        await query.answer("ok")
        await query.message.answer(f"Siz berilgan savollarning {accepted} tasiga to'g'ri javob berdingiz. Siz bergan javoblar:\n{", ".join(tekshiruv)}")
        await state.clear()

    if check == 'userno':
        await query.answer("ok")
        await query.message.answer("""Test javoblarini kiriting: 
                         Test javoblarini quyidagi shaklda yozishingiz mumkin:
🔹 absd...
🔹 1a2b3c4d...""")
        await state.set_state(TestAnswersFromUser.answers)
        return
    # user test ishlash jarayoni test kodini so'rash jarayoni tugagandan keyin tekshirish joyi.
    


@user.message(F.text == "Natijalarim")
async def mynatijalar(message: Message):
    tg_id = message.from_user.id
    testlar = getUserTesttoUserTest(tg_id=tg_id)
    text = ""
    text+=f"Hurmatli bot foydalanuvchisi. Siz jami {len(testlar)} ta testda ishtirok etgansiz.\n"
    for i in range(len(testlar)):
        natija = testlar[i].get("score")/len(testlar[i].get("answers").split(","))
        text += f"{i+1}. {testlar[i].get("score")} ta {f"{(natija*100):.2f}"}% ko'rsatgich.\n"
    await message.answer(text=text)