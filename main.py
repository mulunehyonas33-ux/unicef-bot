import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# የቦቱን ቶከን እዚህ ያስገቡ
TOKEN = "8792632682:AAEgBtMpXPUzDBTpS_FCuxMZh7Iujw7kdAM"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

class RegistrationStates(StatesGroup):
    full_name = State()
    phone_number = State()
    gender = State()
    age = State()
    education_level = State()
    city = State()
    experience = State()
    id_front = State()
    id_back = State()
    payment_receipt = State()

gender_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="ወንድ"), KeyboardButton(text="ሴት")]],
    resize_keyboard=True,
    one_time_keyboard=True
)

city_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="አዲስ አበባ"), KeyboardButton(text="ባህር ዳር")],
        [KeyboardButton(text="አዳማ"), KeyboardButton(text="ሀዋሳ")],
        [KeyboardButton(text="ጅማ"), KeyboardButton(text="አርባምንጭ")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

@dp.message(F.text == "/start")
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "ሰላም! እንኳን ወደ UNICEF Ethiopia የስራ ምዝገባ ቦት በደህና መጡ።\n\n"
        "ምዝገባውን ለመጀመር እባክዎ **ሙሉ ስምዎን** ይጻፉልን፦",
        parse_mode="Markdown"
    )
    await state.set_state(RegistrationStates.full_name)

@dp.message(RegistrationStates.full_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("አመሰግናለሁ። አሁን ደግሞ **ስልክ ቁጥርዎን** ይጻፉልን (ምሳሌ፦ 09xxxxxxxx):")
    await state.set_state(RegistrationStates.phone_number)

@dp.message(RegistrationStates.phone_number)
async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await message.answer("ጾታዎን ይምረጡ፦", reply_markup=gender_kb)
    await state.set_state(RegistrationStates.gender)

@dp.message(RegistrationStates.gender)
async def process_gender(message: types.Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await message.answer("እድሜዎ ስንት ነው?", reply_markup=ReplyKeyboardRemove())
    await state.set_state(RegistrationStates.age)

@dp.message(RegistrationStates.age)
async def process_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("የትምህርት ደረጃዎ ምን ይመስላል? (ለምሳሌ፦ ዲግሪ፣ ዲፕሎማ ወዘተ):")
    await state.set_state(RegistrationStates.education_level)

@dp.message(RegistrationStates.education_level)
async def process_education(message: types.Message, state: FSMContext):
    await state.update_data(education_level=message.text)
    await message.answer("የሚሰሩበትን ከተማ ከታች ካሉት አማራጮች ይምረጡ፦", reply_markup=city_kb)
    await state.set_state(RegistrationStates.city)

@dp.message(RegistrationStates.city)
async def process_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer("የስራ ልምድዎ ስንት ዓመት ነው? (ቁጥር ብቻ ያስገቡ)", reply_markup=ReplyKeyboardRemove())
    await state.set_state(RegistrationStates.experience)

@dp.message(RegistrationStates.experience)
async def process_experience(message: types.Message, state: FSMContext):
    await state.update_data(experience=message.text)
    await message.answer("እባክዎ **የመታወቂያ ፊት ፎቶ (ID Front Photo)** ላኩልኝ:")
    await state.set_state(RegistrationStates.id_front)

@dp.message(RegistrationStates.id_front, F.photo)
async def process_id_front(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data(id_front=photo)
    await message.answer("አሁን ደግሞ **የመታወቂያ ጀርባ ፎቶ (ID Back Photo)** ላኩልኝ:")
    await state.set_state(RegistrationStates.id_back)

@dp.message(RegistrationStates.id_back, F.photo)
async def process_id_back(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data(id_back=photo)
    await message.answer("ለማመልከቻ የሚሆን የቴሌብር ክፍያ የፈጸሙበትን **የክፍያ ደረሰኝ ስክሪንሾት (Payment Receipt)** ላኩልኝ:")
    await state.set_state(RegistrationStates.payment_receipt)

@dp.message(RegistrationStates.payment_receipt, F.photo)
async def process_receipt(message: types.Message, state: FSMContext):
    data = await state.get_data()
    
    summary = (
        "✅ **ምዝገባዎ በተሳካ ሁኔታ ተጠናቋል!**\n\n"
        f"👤 ሙሉ ስም፦ {data['full_name']}\n"
        f"📞 ስልክ ቁጥር፦ {data['phone_number']}\n"
        f"⚧ ጾታ፦ {data['gender']}\n"
        f"👴 እድሜ፦ {data['age']}\n"
        f"🎓 ትምህርት ደረጃ፦ {data['education_level']}\n"
        f"📍 ከተማ፦ {data['city']}\n"
        f"💼 የስራ ልምድ፦ {data['experience']} ዓመት\n\n"
        "መረጃዎ እና የክፍያ ደረሰኝዎ ደርሶናል፤ ማጣራት ተደርጎበት በቅርቡ እናነጋግርዎታለን። እናመሰግናለን!"
    )
    
    await message.answer(summary, parse_mode="Markdown")
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
