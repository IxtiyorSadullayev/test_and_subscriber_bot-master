from aiogram import Router, F 
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
import re
from states.adminState import Admin, AdminTanlov, TestCreate

# button 
from helpers.buttons import yes_or_no

# db
from database.tanlovRequests import createTanlovDb

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
    await message.answer_photo(photo=image, caption=content_text, reply_markup=yes_or_no)
    await state.set_state(AdminTanlov.tekshiruv)
    # tanlov tugash vaqtini e'lon qilish oynasi

@admin.callback_query(AdminTanlov.tekshiruv)
async def adminTanlov_tekshiruv(query: CallbackQuery, state: FSMContext):
    if query.data == "yes":
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
    elif query.data == "no":
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
    await message.answer("Yaratmoqchi bo'lgan testingizda nechta savol mavjud?")
    await state.set_state(TestCreate.count_questions)

    # test faylini yuklash jarayoni


@admin.message(TestCreate.count_questions)
async def adminTest_count_questions(message: Message, state: FSMContext):
    count_test=message.text
    if len(count_test) ==0:
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
    # test javoblarini kiritish jarayoni.

@admin.message(TestCreate.tekshiruv)
async def adminTest_tekshiruv(message: Message, state: FSMContext):
    pass
    # test savol va javoblarini tekshirish jarayoni. 


###########################################################################################################
###########################################################################################################
###########################################################################################################
@admin.message(Admin.hisobot)
async def adminCreate_hisobot(message: Message, state: FSMContext):
    pass
    # admin tomonidan tayorlangan hisobotlarni ko'rish jarayoni.