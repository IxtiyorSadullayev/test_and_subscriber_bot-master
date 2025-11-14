from aiogram import Router, F 
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
import asyncio
import re
from states.adminState import Admin, AdminTanlov, TestCreate, AdminHisobotHolat

# button 
from helpers.buttons import yes_or_no, adminHisobot, holatlar, testlistBtns, tanlovlistBtns, testholatiniyangilash, tanlovholatiniyangilash


# db
from database.tanlovRequests import createTanlovDb, getTanlovlar, getOneTanlov, updateTanlovHolati
from database.testRequests import createTest, getTestToAdmin, getTestById, updateTestHolat
from database.notificationRequests import createNotification, getTanlovNotifications, getTestNotifications
from database.userRequests import getAllUsers

from helpers.bot import bot

admin = Router()


@admin.message(F.text=="Tanlov yaratish")
async def createTanlov(message: Message, state: FSMContext):
    await message.answer("Yaratmoqchi bo'lgan tanlovingizni nomini yozib qoldiring: ")
    await state.set_state(AdminTanlov.name)

###########################################################################################################
###########################################################################################################
###########################################################################################################
@admin.message(AdminTanlov.name)
async def adminTanlov_name(message: Message, state: FSMContext):
    name_tanlov = message.text 
    if len(name_tanlov)<3:
        await message.answer("Yaratmoqchi bo'lgan tanlovingizni nomini yozib qoldiring: ")
        await state.set_state(AdminTanlov.name)
        return
    await state.update_data(name=name_tanlov)
    await message.answer("Tanlov haqida biror ma'lumot yozib qoldiring: (Maksimal darajada chiroyli yozib qo'ying)")
    await state.set_state(AdminTanlov.description)

    # tanlov nomini yozish maydonini hosil qilish
    
@admin.message(AdminTanlov.description)
async def adminTanlov_description(message: Message, state: FSMContext):
    description_tanlov = message.text 
    if len(description_tanlov)<3:
        await message.answer("Yaratmoqchi bo'lgan tanlovingiz haqida yozib qoldiring: ")
        await state.set_state(AdminTanlov.description)
        return
    await state.update_data(description=description_tanlov)
    await message.answer("Tanlovga bag'ishlangan rasmni yuboring:")
    await state.set_state(AdminTanlov.image)
    # tanlov haqida ma'lumot yozish maydonini hosil qilish


@admin.message(AdminTanlov.image)
async def adminTanlov_image(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("Tanlovga bag'ishlangan rasmni yuboring:")
        await state.set_state(AdminTanlov.image)
        return
    image = message.photo[-1].file_id
    await state.update_data(image=image)
    await message.answer("Tanlov boshlash sanasi:")
    await state.set_state(AdminTanlov.start_date)
1    # tanlovga bag'ishlangan rasmni joylashtirish oynasi


@admin.message(AdminTanlov.start_date)
async def adminTanlov_start_date(message: Message, state: FSMContext):
    start_data = message.text
    if len(start_data) < 3:
        await message.answer("Tanlov boshlash sanasi:")
        await state.set_state(AdminTanlov.start_date)
        return
    await state.update_data(start_date=start_data)
    await message.answer("Tanlov tugash sanasi:")
    await state.set_state(AdminTanlov.end_date)
    # tanlovboshlash vaqtini e'lon qilish


@admin.message(AdminTanlov.end_date)
async def adminTanlov_end_date(message: Message, state: FSMContext):
    end_date = message.text
    if len(end_date) < 3:
        await message.answer("Tanlov boshlash sanasi:")
        await state.set_state(AdminTanlov.start_date)
        return
    await state.update_data(end_date=end_date)
    data = await state.get_data()
    name=data.get("name")
    description=data.get("description")
    image=data.get("image")
    start_date=data.get("start_date")
    content_text=""
    content_text+=name+"\n"
    content_text+=description+"\n"
    content_text+=start_date+"\n"
    content_text+=end_date
    await message.answer_photo(photo=image, caption=content_text, reply_markup=yes_or_no("admin"))
    await state.set_state(AdminTanlov.tekshiruv)
    # tanlov tugash vaqtini e'lon qilish oynasi

@admin.callback_query(AdminTanlov.tekshiruv)
async def adminTanlov_tekshiruv(query: CallbackQuery, state: FSMContext):
    if query.data == "adminyes":
        await query.answer("ok")
        data=await state.get_data()
        name=data.get("name")
        description=data.get("description")
        image=data.get("image")
        start_date=data.get("start_date")
        end_date=data.get("end_date")
        tanlow=  createTanlovDb(name=name, description=description, image=image, started_date=start_date, end_date=end_date, published="JARAYONDA")
        print(tanlow)
        await query.message.answer("Ma'lumotlar saqlandi")
        await state.clear()
        return 
    elif query.data == "adminno":
        await query.answer("ok")
        await query.message.answer("Yaratmoqchi bo'lgan tanlovingizni nomini yozib qoldiring:")
        await state.set_state(AdminTanlov.name)
    # tanlovni ma'lumotlarini tekshiruv oynasini hosil qilish.

###########################################################################################################
###########################################################################################################
###########################################################################################################
@admin.message(F.text=="Test yaratish")
async def adminCreate_test(message: Message, state: FSMContext):
    await message.answer("Yaratmoqchi bo'lgan testingizni faylini yuboring: ")
    await state.set_state(TestCreate.test_file)
    # admin tomonidan qandayda bir tanlov yaratish uchun imkoniyat taqdim qilish 
    # unga foydalanuvchi id raqamini ham qo'shib qo'yish imkoniyatini taqdim qilishimiz mumkin bo'ladi

###########################################################################################################
@admin.message(TestCreate.test_file)
async def adminTest_test_file(message: Message, state: FSMContext):
    if not message.document:
        await message.answer("Yaratmoqchi bo'lgan testingizni faylini yuboring: ")
        await state.set_state(TestCreate.test_file)
        return
    test_file=message.document.file_id
    await state.update_data(test_file=test_file)
    await state.update_data(file_type=message.document.file_name.split(".")[-1])
    await message.answer("Yaratmoqchi bo'lgan testingizda nechta savol mavjud?")
    await state.set_state(TestCreate.count_questions)

    # test faylini yuklash jarayoni


@admin.message(TestCreate.count_questions)
async def adminTest_count_questions(message: Message, state: FSMContext):
    count_test=message.text
    if len(count_test) ==0 or not count_test.isdigit():
        await message.answer("Yaratmoqchi bo'lgan testingizda nechta savol mavjud?")
        state.set_state(TestCreate.count_questions)
        return
    await state.update_data(count_questions=count_test)
    await message.answer("""Test javoblarini kiriting: 
                         Test javoblarini quyidagi shaklda yozishingiz mumkin:
🔹 absd...
🔹 1a2b3c4d...""")
    await state.set_state(TestCreate.answers)
    # test faylidagi testlar sonini kiritish

@admin.message(TestCreate.answers)
async def adminTest_answers(message: Message, state: FSMContext):
    answers = message.text
    data = await state.get_data()
    count_questions = data.get("count_questions")
    matches = re.findall(r'(\d)([a-zA-Z])', answers)
    if len(answers)==0:
        await message.answer("""Test javoblarini kiriting: 
                         Test javoblarini quyidagi shaklda yozishingiz mumkin:
🔹 absd... 
🔹 1a2b3c4d...""")
        await state.set_state(TestCreate.answers)
        return
    elif len(answers) != int(count_questions) and len(matches) != int(count_questions):
        await message.answer("""Test javoblarini kiriting: 
                         Test javoblarini quyidagi shaklda yozishingiz mumkin:
🔹 absd...
🔹 1a2b3c4d...""")
        await state.set_state(TestCreate.answers)
        return
    javob_korinishi = []
    if len(answers) == int(count_questions):
        for i in range(len(answers)):
            javob_korinishi.append(f"{i+1} {answers[i]}")
    elif len(matches) == int(count_questions):
        for i in range(1, len(matches)+1):
            javob_korinishi.append(f"{i//10 + i if i<10 else i//10+i-1} {matches[i-1][1]}")
    # test javoblarini kiritish jarayoni.
    await state.update_data(answers = ",".join(javob_korinishi))
    test_file=data.get("test_file")
    await message.answer("Javoblaringizni qabul qildik. Ma'lumotlarinigizni tekshirib ko'ring")
    text_content=""
    text_content+="Test savollar soni: "+count_questions + "\n"
    text_content+="Javoblar: " + ", ".join(javob_korinishi) + "\n"
    await message.answer_document(document=test_file, caption=text_content, reply_markup=yes_or_no("admintest"))    
    await state.set_state(TestCreate.tekshiruv)


@admin.callback_query(TestCreate.tekshiruv)
async def adminTest_tekshiruv(query: CallbackQuery, state: FSMContext):
    if query.data == "admintestyes":
        await query.answer("Ok")
        data = await state.get_data()
        test_file = data.get("test_file")
        file_type=data.get("file_type")
        count_question=data.get("count_questions")
        answers = data.get("answers")
        testholati = createTest(test_file=test_file, file_type=file_type, count_question=int(count_question), answers=answers, published="JARAYONDA")
        await query.message.delete()
        if testholati:
            await query.message.answer("Ma'lumotlar saqlandi.")
            return
        else:
            await query.message.answer("Ma'lumotni saqlashda hatolikga yuz keldik.")
        await state.clear()
        
        return 
    elif query.data == "admintestno":
        await query.answer("ok")
        await query.message.answer("Test faylini kiriting: ")
        await state.set_state(TestCreate.test_file)
    # test savol va javoblarini tekshirish jarayoni. 


###########################################################################################################
###########################################################################################################
###########################################################################################################
@admin.message(F.text == "Hisobot")
async def adminCreate_hisobot(message: Message, state: FSMContext):
    await message.answer("Qaysi bo'lim haqida ma'lumot olmoqchisiz ?", reply_markup=adminHisobot)
    # admin tomonidan tayorlangan hisobotlarni ko'rish jarayoni.


@admin.callback_query(F.data.startswith('admin_t'))
async def adminHisobotQuery(query: CallbackQuery, state:  FSMContext):
    await query.answer("Ok")
    await query.message.delete()
    if query.data=="admin_test":
        await query.message.answer("Testlar. Qaysi turdagi testlarni ko'rmoqchisiz ?", reply_markup=holatlar)
        await state.set_state(AdminHisobotHolat.test)
        # bu yerda testlar ro'yxatini chiqarib berishimiz kerak
    elif query.data == "admin_tanlov":
        await query.message.answer("Tanlovlar. Qaysi turdagi tanlovlarni ko'rmoqchisiz ?", reply_markup=holatlar)
        await state.set_state(AdminHisobotHolat.tanlov)        
    return

@admin.callback_query(AdminHisobotHolat.test)
async def adminhisobotTestHolatlar(query: CallbackQuery, state: FSMContext):
    await query.answer("OK")
    await query.message.delete()
    if query.data == "jarayonda":
        testlar = getTestToAdmin(published="JARAYONDA")
        await query.answer("Ok")
        if (len(testlar) == 0):
            await query.message.answer("Hozircha jarayondagi test mavjud emas")
            await state.clear()
            return
        await query.message.answer("Teslar: ", reply_markup=testlistBtns(tests=testlar))
        await state.clear()
    elif query.data == "active":
        testlar = getTestToAdmin(published="ACTIVE")
        await query.answer("Ok")
        if (len(testlar) == 0):
            await query.message.answer("Hozircha active test mavjud emas")
            await state.clear()
            return
        await query.message.answer("Teslar: ", reply_markup=testlistBtns(tests=testlar))
        await state.clear()
    elif query.data == "complated":
        testlar = getTestToAdmin(published="COMPLATED")
        await query.answer("Ok")
        if (len(testlar) == 0):
            await query.message.answer("Hozircha yakunlangan test mavjud emas")
            await state.clear()
            return
        await query.message.answer("Teslar: ", reply_markup=testlistBtns(tests=testlar))
        await state.clear()


@admin.callback_query(AdminHisobotHolat.tanlov)
async def adminhisobotTanlovHolatlar(query: CallbackQuery, state: FSMContext):
    await query.message.delete()
    if query.data == "jarayonda":
        testlar = getTanlovlar(published="JARAYONDA")
        await query.answer("Ok")
        if (len(testlar) == 0):
            await query.message.answer("Hozircha jarayondagi tanlov mavjud emas")
            await state.clear()
            return
        await query.message.answer("Teslar: ", reply_markup=tanlovlistBtns(tests=testlar))
        await state.clear()
    elif query.data == "active":
        testlar = getTanlovlar(published="ACTIVE")
        await query.answer("Ok")
        if (len(testlar) == 0):
            await query.message.answer("Hozircha active tanlov mavjud emas")
            await state.clear()
            return
        await query.message.answer("Teslar: ", reply_markup=tanlovlistBtns(tests=testlar))
        await state.clear()
    elif query.data == "complated":
        testlar = getTanlovlar(published="COMPLATED")
        await query.answer("Ok")
        if (len(testlar) == 0):
            await query.message.answer("Hozircha yakunlangan tanlov mavjud emas")
            await state.clear()
            return
        await query.message.answer("Teslar: ", reply_markup=tanlovlistBtns(tests=testlar))
        await state.clear()


@admin.callback_query(F.data.startswith("testid"))
async def testholatlarinitaqdimqilish(query: CallbackQuery):
    testid = int(query.data.split("_")[-1])
    test = getTestById(test_id=testid)
    contest = ""
    contest+="Fayl turi: " + test.get("file_type") + "\n"
    contest+="Savollar soni: " + str(test.get("count_question")) + "\n"
    contest+="Javoblari: " + test.get("answers") + "\n\n"
    contest+="Holati: "+test.get("published") + "\n\n" 
    await query.answer("ok")
    await query.message.answer_document(document=test.get("test_file"), caption=contest, reply_markup=testholatiniyangilash(test_id=testid))
    

@admin.callback_query(F.data.startswith("testholati"))
async def testholatiHolatlari(query: CallbackQuery):
    holat = query.data.split("_")[1]
    testid = int(query.data.split("_")[-1])
    if holat == '1': #Jarayonda qilish
        await query.answer("ok")
        updateTestHolat(test_id=testid, published="JARAYONDA")
        await query.message.delete()
        await query.message.answer("Bajarildi")
        return
    elif holat == '2': #Aktive qilish
        await query.answer("ok")
        updateTestHolat(test_id=testid, published="ACTIVE")
        # bu yerda barcha userlarga yuborish kerak edi.
        users = getAllUsers()
        if not users:
            pass
        else:
            for user in users:
                try:
                    # await query.message.answer
                    await bot.send_message(user.get("tg_id"), f"Yangi test aktiv bo'ldi. Testid: {testid}")
                    createNotification(tg_id=user.get("tg_id"), test_id=testid, tanlov_id=None, holat="Jo'natildi")
                except:
                    createNotification(tg_id=user.get("tg_id"), test_id=testid, tanlov_id=None, holat="Jo'natma bekor bo'ldi. Foydalanuvchi bilan aloqa mavjud emas.")
                await asyncio.sleep(0.05)

        await query.message.delete()
        await query.message.answer("Bajarildi")
        return
    elif holat == '3': #Complated qilish
        await query.answer("ok")
        updateTestHolat(test_id=testid, published="COMPLATED")
        await query.message.delete()
        await query.message.answer("Bajarildi")
        return
    elif holat == '4': #Ishtirokchilar ro'yxatini chiqarish
        await query.answer("ok")








@admin.callback_query(F.data.startswith("tanlovid"))
async def testholatlarinitaqdimqilish(query: CallbackQuery):
    testid = int(query.data.split("_")[-1])
    test = getOneTanlov(test_id=testid)
    contest = ""
    contest+= test.get("name") + "\n"
    contest+=test.get("description") + "\n"
    contest+="Boshlash vaqti: " + test.get("started_date") + "\n\n"
    contest+="Tugash vaqti: " + test.get("end_date") + "\n\n"
    contest+="Holati: "+test.get("published") + "\n\n" 
    await query.answer("ok")
    await query.message.answer_document(document=test.get("test_file"), caption=contest, reply_markup=tanlovholatiniyangilash(test_id=testid))


@admin.callback_query(F.data.startswith("tanlovholati"))
async def tanlovholatiTanlov(query: CallbackQuery):
    holat = query.data.split("_")[1]
    tanlovid = int(query.data.split("_")[-1])
    if holat == "1":
        await query.answer("ok")
        updateTanlovHolati(tanlov_id=tanlovid, published="JARAYONDA")
        await query.message.delete()
        await query.message.answer("Bajarildi")
        return
    elif holat == "2":
        await query.answer("ok")
        updateTanlovHolati(tanlov_id=tanlovid, published="ACTIVE")

        await query.message.delete()
        await query.message.answer("Bajarildi")
        return
    elif holat == "3":
        await query.answer("ok")
        updateTanlovHolati(tanlov_id=tanlovid, published="COMPLATED")
        await query.message.delete()
        await query.message.answer("Bajarildi")
        return
    elif holat == "4":
        await query.answer("ok")
        # ishtirokchilar ro'yxati

    


@admin.message(F.text=="Bot haqida ma'lumot")
async def aboutbot(message: Message):
    await message.answer("Bu bot test yaratuvchilar va uni bajaruvchilar uchun ishlangan bepul bot hisoblanadi. Ushbu botni admin tomonidan boshqariladi va barchaga birdek foydalanish uchun yaratildi")