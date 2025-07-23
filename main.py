from telegram import Update
from telegram.ext import ApplicationBuilder, Updater, CommandHandler, CallbackContext, ContextTypes
from Controlers.TodoControlers import TodoControler

TOKEN = "8005369706:AAGy05a05hzQmdCYj0VcELjgzUPtVh3K-Mg"
application = ApplicationBuilder().token(TOKEN).build()

application.add_handler(CommandHandler("start",TodoControler.start))
application.add_handler(CommandHandler("add",TodoControler.add_todo))
application.add_handler(CommandHandler("buscar",TodoControler.buscar_todo))

#async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
#    await update.message.reply_text("Hola, los comandos para agregar un modelo de telefono es: /add y para buscar es /buscar")

#async def add(update:Update,context:ContextTypes.DEFAULT_TYPE):
#    await update.message.reply_text("comando para agregar telefonos")

#async def search(update:Update,context:ContextTypes.DEFAULT_TYPE):
#    await update.message.reply_text("comando para buscar telefonos")


#application.add_handler(CommandHandler("start", start))
#application.add_handler(CommandHandler("add", add))
#application.add_handler(CommandHandler("buscar", search))
application.run_polling(allowed_updates=Update.ALL_TYPES)