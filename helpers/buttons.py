from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

userButtons = ["Test ishlash", "Tanlovlar", "Bot haqida ma'lumot"]

adminButtons = ["Talnov yaratish", "Test yaratish", "Hisobot"]
 

btnsUser = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Test ishlash"), KeyboardButton(text="Tanlovlar")],
        [KeyboardButton(text="Taklif havolam"), KeyboardButton(text="Yig'gan odamlarim")],
        [KeyboardButton(text="Natijalarim"), KeyboardButton(text="Bot haqida ma'lumot")] 
    ],
    resize_keyboard=True,
    input_field_placeholder="Biror kamandani tanlang!"
)
btnsAdmin = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Test yaratish"), KeyboardButton(text="Tanlov yaratish")],
        [KeyboardButton(text="Hisobot"), KeyboardButton(text="Bot haqida ma'lumot")] 
    ],
    resize_keyboard=True,
    input_field_placeholder="Biror kamandani tanlang!"
)

getContact = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Get Phone Number", request_contact=True)]], resize_keyboard=True, input_field_placeholder="Telefon raqamingizni tugma orqali bosib qoldiring.")

yes_or_no = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Ha", callback_data="yes"),
        InlineKeyboardButton(text="Yo'q", callback_data="no"),]
    ]
)