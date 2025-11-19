from aiogram import Router, F 
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext

from states.userState import User

# getbaza
from database.userRequests import getUserByTg_id, createUser, updateUserByTg_id_role
from database.chaqirRequests import createChaqirData

# tugmalar
from helpers.buttons import btnsUser, btnsAdmin, getContact, yes_or_no
startRouter = Router()


@startRouter.message(F.text.startswith("/start"))
async def startCommand(message: Message, state: FSMContext):
    # print(message.text)
    # print(message.text.split(" ")[1])
    # await message.answer('Hello')
    tg_id = message.from_user.id 
    user = getUserByTg_id(tg_id=tg_id)
    
    if not user :
        await message.answer("Assalomu aleykum. Botimizga hush kelibsiz. Botdan to'liq foydalanishingiz uchun ro'yxatdan o'tishingiz kerak bo'ladi. \nTo'liq ismingizni kiriting:")
        await state.set_state(User.user_name)
        if len(message.text.split(" "))>1:
            await state.update_data(taklif_id=message.text.split(" ")[1])
        return
    
    if user.get("role") == "USER":
        await message.answer("Assalomu aleykum bot foydalanuvchisi. Ishni boshlaymizmi? Quyidagi kamandalarning birini tanlang!", reply_markup=btnsUser)
        return
    elif user.get("role") == "ADMIN":
        await message.answer("Assalomu aleykum bot foydalanuvchisi. Ishni boshlaymizmi? Quyidagi kamandalarning birini tanlang!", reply_markup=btnsAdmin)

    

    # ro'yxatdan o'tgan -> admin yokida oddiy foydalanuvchiga 2 lasini ham kanalga yo'naltirish kerak.
    # ro'yxatdan o'tmagan -ro'yxatdan o'tirish stateiga 

@startRouter.message(User.user_name)
async def userRegister_name(message: Message, state: FSMContext):
    fullname = message.text
    if len(fullname)<3:
        await message.answer("Kechirasiz to'liq ismingizni kiriting!")
        await state.set_state(User.user_name)
        return
    await message.answer("Telefon raqamingizni bog'lanish uchun qoldiring!", reply_markup=getContact)
    await state.update_data(user_name=fullname)
    await state.set_state(User.user_phone)
    
    # userning FIO ma'lumotlarini so'rab olish uchun kerak bo'ladi. 


@startRouter.message(User.user_phone)
async def userRegister_phone(message: Message, state: FSMContext):
    if not message.contact:
        await message.answer("Telefon raqamingizni bog'lanish uchun qoldiring!", reply_markup=getContact)
        await state.set_state(User.user_phone)
        return
    await state.update_data(user_phone = message.contact.phone_number)
    data = await state.get_data()
    # await message.answer(f"Ma'lumotlaringizni tekshirib ko'ring!\nFullname: {data.get("user_name")}\nPhone number: {data.get("user_phone")}\n\nBarcha ma'lumotlaringiz to'g'rimi?", reply_markup=yes_or_no("start"))
    await message.answer(
    f"Ma'lumotlaringizni tekshirib ko'ring!\nFullname: {data.get('user_name')}\nPhone number: {data.get('user_phone')}\n\nBarcha ma'lumotlaringiz to'g'rimi?",
    reply_markup=yes_or_no("start")
)
    await state.set_state(User.tekshiruv)
    # userdan ishlab turgan ishonchli telefon raqamini olish uchun kerak. 

@startRouter.callback_query(User.tekshiruv)
async def userRegister_tekshiruv(query: CallbackQuery, state: FSMContext):
    if query.data == "startyes":
        await query.answer("Ok")
        data = await state.get_data()
        username = query.message.chat.username
        taklif_id=data.get("taklif_id")
        if taklif_id:
            createChaqirData(tg_id=int(taklif_id), client_id=query.message.chat.id)
        await query.message.delete()
        createUser(fullname=data.get("user_name"), username= username if username else "no username", phoneNumber=data.get("user_phone"),tg_id=query.message.chat.id,)
        await query.message.answer("Ro'yxatdan o'tganingiz uchun katta rahmat. Botdan foydalanish uchun quyidagi kamandalarning birini tanlang.", reply_markup=btnsUser)
        await state.clear()
        return 
    elif query.data == "startno":
        await query.answer("ok")
        await query.message.answer("To'liq ismingizni kiriting: ")
        await state.set_state(User.user_name)
    # user ma'lumotlari to'g'ri yoki noto'g'ri ekanligini tekshirib olish uchun kerak bo'ladi. 
    # tekshiruvdan o;tgandan keyin foydalanuvchiga ishchi maydonini hosil qildirishim kerak bo'ladi. 
    

@startRouter.message(F.text.startswith("admin_1234"))
async def setadmin(message: Message):
    tg_id = message.from_user.id
    user = updateUserByTg_id_role(tg_id=tg_id, role="ADMIN")
    if not user:
        await message.answer("Kechirasiz noto'g'ri command terdingiz")
        return
    else:
        await message.answer("Tabriklaymiz. Siz admin rolidasiz", reply_markup=btnsAdmin)
        return
