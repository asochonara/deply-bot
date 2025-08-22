from telegram import Update
from telegram.ext import ApplicationBuilder,CallbackQueryHandler, Updater, CommandHandler, CallbackContext, ContextTypes
from Controlers.TodoControlers import TodoControler

TOKEN = "8005369706:AAGy05a05hzQmdCYj0VcELjgzUPtVh3K-Mg"
application = ApplicationBuilder().token(TOKEN).build()

application.add_handler(CommandHandler("start",TodoControler.start))
application.add_handler(TodoControler.info_conversation_handler)
application.add_handler(CallbackQueryHandler(TodoControler.button_controller))
application.add_handler(CommandHandler("buscar",TodoControler.buscar))

application.run_polling(allowed_updates=Update.ALL_TYPES)