import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes
)
import requests

# Настройки
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  # Замените на реальный токен
API_URL = "http://localhost:5000/predict"

# Состояния диалога
BRAND, MODEL, RAM, STORAGE, SCREEN_SIZE = range(5)

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(name)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "💻 *Laptop Price Predictor Bot*\n\n"
        "Я могу оценить стоимость вашего ноутбука!\n"
        "Нажмите /predict чтобы начать оценку.",
        parse_mode='Markdown'
    )

async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    brands = [['Apple', 'Dell'], ['HP', 'Lenovo'], ['Asus', 'Acer']]
    await update.message.reply_text(
        "Выберите бренд ноутбука:",
        reply_markup=ReplyKeyboardMarkup(brands, one_time_keyboard=True)
    )
    return BRAND

async def get_brand(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['brand'] = update.message.text
    await update.message.reply_text(
        "Введите модель ноутбука:",
        reply_markup=ReplyKeyboardRemove()
    )
    return MODEL

async def get_model(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['model'] = update.message.text
    await update.message.reply_text("Введите объем оперативной памяти (в ГБ):")
    return RAM

async def get_ram(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        ram = int(update.message.text)
        if ram < 2 or ram > 64:
            raise ValueError
        context.user_data['ram'] = ram
        await update.message.reply_text("Введите объем накопителя (в ГБ):")
        return STORAGE
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите корректный объем RAM (от 2 до 64 ГБ):")
        return RAM

async def get_storage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        storage = int(update.message.text)
        if storage < 128 or storage > 4096:
            raise ValueError
        context.user_data['storage'] = storage
        await update.message.reply_text("Введите размер экрана (в дюймах):")
        return SCREEN_SIZE
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите корректный объем накопителя (128-4096 ГБ):")
        return STORAGE

chayka, [6/10/25 6:15 AM]
async def get_screen_size(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        screen_size = float(update.message.text.replace(',', '.'))
        if screen_size < 10.0 or screen_size > 17.0:
            raise ValueError
        context.user_data['screen_size'] = screen_size
        
        try:
            response = requests.post(API_URL, json=context.user_data)
            if response.status_code == 200:
                result = response.json()
                laptop = context.user_data
                message = (
                    f"💻 *{laptop['brand']} {laptop['model']}*\n\n"
                    f"▪️ Оперативная память: {laptop['ram']} ГБ\n"
                    f"▪️ Накопитель: {laptop['storage']} ГБ\n"
                    f"▪️ Диагональ экрана: {laptop['screen_size']}\"\n\n"
                    f"💵 *Оценка стоимости:* ${result['price']:,}"
                )
                await update.message.reply_text(
                    message,
                    parse_mode='Markdown',
                    reply_markup=ReplyKeyboardMarkup([['/predict']], resize_keyboard=True)
                )
            else:
                await update.message.reply_text("⚠️ Ошибка при расчете цены")
        except Exception as e:
            await update.message.reply_text(f"🚨 Ошибка подключения: {str(e)}")
        
        return ConversationHandler.END
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите корректный размер экрана (10.0-17.0 дюймов):")
        return SCREEN_SIZE

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Отменено. Нажмите /predict чтобы начать заново.")
    return ConversationHandler.END

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('predict', predict)],
        states={
            BRAND: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_brand)],
            MODEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_model)],
            RAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_ram)],
            STORAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_storage)],
            SCREEN_SIZE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_screen_size)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(CommandHandler('start', start))
    application.add_handler(conv_handler)

    application.run_polling()

if name == 'main':
    main()
