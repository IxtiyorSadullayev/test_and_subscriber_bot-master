from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from aiogram.utils.keyboard import InlineKeyboardBuilder

userButtons = ["📝 Test ishlash", "📌 Tanlovlar", "ℹ️ *Bot haqida ma’lumot*"]

adminButtons = ["Talnov yaratish", "Test yaratish", "Hisobot"]
 

btnsUser = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📝 Test ishlash")],
        [KeyboardButton(text="🔗 Taklif havolam"), KeyboardButton(text="👨‍👩‍👧‍👦 Yig'gan Odamlarim 🤝")],
        [KeyboardButton(text="📉 Natijalarim"), KeyboardButton(text="ℹ️ *Bot haqida ma’lumot*")] 
    ],
    resize_keyboard=True,
    input_field_placeholder="Biror kamandani tanlang!"
)
btnsAdmin = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛠 *Test yaratish*") ],
        [KeyboardButton(text="📊 *Hisobotlar*"), KeyboardButton(text="ℹ️ *Bot haqida ma’lumot*")],
        [KeyboardButton(text="📂 *Ma’lumotlarni yuklash (XLSX)*")] 
    ],
    resize_keyboard=True,
    input_field_placeholder="Biror kamandani tanlang!"
)

getContact = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Get Phone Number", request_contact=True)]], resize_keyboard=True, input_field_placeholder="Telefon raqamingizni tugma orqali bosib qoldiring.")

def yes_or_no(type:str):
    return InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Ha", callback_data=f"{type}yes"),
        InlineKeyboardButton(text="Yo'q", callback_data=f"{type}no"),]
    ]
)

adminHisobot = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📚 Testlar", callback_data='admin_test'),
        ]
    ]
)

holatlar = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⏳ Jarayonda", callback_data="jarayonda"),
            InlineKeyboardButton(text="⚡ A C T I V E 🚀", callback_data="active"),
            InlineKeyboardButton(text="🎉 COMPLETED 🎊", callback_data="complated"),
        ]
    ]
)

def testlistBtns(tests: list):
    builder = InlineKeyboardBuilder()
    for i in range(len(tests)):
        builder.add(
            InlineKeyboardButton(
                text=f"{i+1}",
                callback_data=f"testid_{tests[i].get('id')}"
            )
        )
    return builder.adjust(4).as_markup()


def tanlovlistBtns(tests: list):
    builder = InlineKeyboardBuilder()
    for i in range(len(tests)):
        builder.add(
            InlineKeyboardButton(
                text=f"{i+1}",
                callback_data=f"tanlovid_{tests[i].get('id')}"
            )
        )
    return builder.adjust(4).as_markup()

def testholatiniyangilash(test_id:int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⚡ Jarayonda qilish 🛠️", callback_data=f"testholati_1_{test_id}")],
                [InlineKeyboardButton(text="⚡ Active qilish jarayoni", callback_data=f"testholati_2_{test_id}")],
                [InlineKeyboardButton(text="✔️ Completed qilish", callback_data=f"testholati_3_{test_id}"),
            ], [
                InlineKeyboardButton(text="🎪 ISHTIROKCHILAR 👥", callback_data=f"testholati_4_{test_id}")
            ], [
                InlineKeyboardButton(text="📝 Ma'lumotlarni O'zgartirish ✏️", callback_data=f"testholati_5_{test_id}")
            ],[
                InlineKeyboardButton(text="❌ Testni o'chirish", callback_data=f"testholati_6_{test_id}")
            ]
        ]
    )
def tanlovholatiniyangilash(test_id:int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⚡ Jarayonda qilish 🛠️", callback_data=f"tanlovholati_1_{test_id}")],
            [InlineKeyboardButton(text="⚡ Active qilish jarayoni", callback_data=f"tanlovholati_2_{test_id}")],
                [InlineKeyboardButton(text="✔️ Completed qilish", callback_data=f"tanlovholati_3_{test_id}"),
            ],
            [
                InlineKeyboardButton(text="🎪 ISHTIROKCHILAR 👥", callback_data=f"tanlovholati_4_{test_id}")

            ]
        ]
    )