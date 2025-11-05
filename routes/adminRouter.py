from aiogram import Router, F 
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext

from states.adminState import Admin, AdminTanlov, TestCreate

admin = Router()


@admin.message(Admin.createTanlov)
async def adminCreate_tanlov(message: Message, state: FSMContext):
    pass
    # admin tomonidan qandayda bir tanlov yaratish uchun imkoniyat taqdim qilish 
    # unga foydalanuvchi id raqamini ham qo'shib qo'yish imkoniyatini taqdim qilishimiz mumkin bo'ladi

###########################################################################################################
###########################################################################################################
###########################################################################################################
@admin.message(AdminTanlov.name)
async def adminTanlov_name(message: Message, state: FSMContext):
    pass
    # tanlov nomini yozish maydonini hosil qilish
    
@admin.message(AdminTanlov.description)
async def adminTanlov_description(message: Message, state: FSMContext):
    pass
    # tanlov haqida ma'lumot yozish maydonini hosil qilish


@admin.message(AdminTanlov.image)
async def adminTanlov_image(message: Message, state: FSMContext):
    pass
    # tanlovga bag'ishlangan rasmni joylashtirish oynasi


@admin.message(AdminTanlov.start_date)
async def adminTanlov_start_date(message: Message, state: FSMContext):
    pass
    # tanlovboshlash vaqtini e'lon qilish


@admin.message(AdminTanlov.end_date)
async def adminTanlov_end_date(message: Message, state: FSMContext):
    pass
    # tanlov tugash vaqtini e'lon qilish oynasi

@admin.message(AdminTanlov.tekshiruv)
async def adminTanlov_tekshiruv(message: Message, state: FSMContext):
    pass
    # tanlovni ma'lumotlarini tekshiruv oynasini hosil qilish.

###########################################################################################################
###########################################################################################################
###########################################################################################################
@admin.message(Admin.createTest)
async def adminCreate_test(message: Message, state: FSMContext):
    pass
    # admin tomonidan qandayda bir tanlov yaratish uchun imkoniyat taqdim qilish 
    # unga foydalanuvchi id raqamini ham qo'shib qo'yish imkoniyatini taqdim qilishimiz mumkin bo'ladi

###########################################################################################################
@admin.message(TestCreate.test_file)
async def adminTest_test_file(message: Message, state: FSMContext):
    pass
    # test faylini yuklash jarayoni


@admin.message(TestCreate.file_type)
async def adminTest_file_type(message: Message, state: FSMContext):
    pass
    # test faylini qanday turda ekanligini kiritish

@admin.message(TestCreate.count_questions)
async def adminTest_count_questions(message: Message, state: FSMContext):
    pass
    # test faylidagi testlar sonini kiritish

@admin.message(TestCreate.answers)
async def adminTest_answers(message: Message, state: FSMContext):
    pass
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