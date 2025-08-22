import sqlite3
from telegram import Update,KeyboardButton, InlineKeyboardButton,InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ContextTypes,CallbackContext,CommandHandler,ApplicationBuilder, Updater, CommandHandler, CallbackContext, ContextTypes,MessageHandler,filters,ConversationHandler


# Definición de los pasos de la conversación
MODEL, COMPANY, G2, G3, G4, NOTES = range(6)

class TodoControler:

  # Función para iniciar la conversación
  async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("¡Hola! Usa el comando /add para agregar un nuevo modelo de teléfono y /buscar para hacer una busqueda de modelos de teléfonos.")

  async def pedir_modelo(update: Update, context: CallbackContext):
    await update.message.reply_text("Por favor, proporciona el modelo del teléfono:")
    return MODEL
  
  async def optener_modelo(update:Update, context:ContextTypes.DEFAULT_TYPE):
    context.user_data["modelo"]= update.message.text
    await update.message.reply_text('Por favor, proporciona la compañia:')
    return COMPANY
    
  async def optener_carrier(update:Update, context:ContextTypes.DEFAULT_TYPE):
    context.user_data["company"]= update.message.text

    keyboard = [[KeyboardButton("GSM(2G) - 900Mhz Oficial ✅"), KeyboardButton("GSM(2G) - 900Mhz Oficial ❌")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True) 
    await update.message.reply_text('Seleccione el soporte de la 2g', reply_markup=reply_markup)
    return G2
  
  async def obtener2g(update:Update, context:ContextTypes.DEFAULT_TYPE):
    context.user_data["g2"]= update.message.text

    keyboard = [[KeyboardButton("HSDPA(3G) - 900Mhz Oficial ✅"), KeyboardButton("HSDPA(3G) - 900Mhz Oficial ❌")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True) 
    await update.message.reply_text('Seleccione el soporte de la 3g', reply_markup=reply_markup)
    return G3
  
  async def obtener3g(update:Update, context:ContextTypes.DEFAULT_TYPE):
    context.user_data["g3"]= update.message.text

    keyboard = [[KeyboardButton("LTE(4G) - 1800Mhz (Band 3) Oficial ✅"), KeyboardButton("LTE(4G) - 1800Mhz (Banda 3) Oficial ❌")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True) 
    await update.message.reply_text('Seleccione el soporte de la 4g', reply_markup=reply_markup)
    return G4
    
  
  async def obtener4g(update:Update, context:ContextTypes.DEFAULT_TYPE):
    context.user_data["g4"]= update.message.text
    await update.message.reply_text('Por favor, proporciona los detalles a tener en cuenta:')
    return NOTES
  
  
  
  async def obtenernotas(update:Update, context:ContextTypes.DEFAULT_TYPE):
    context.user_data["notas"]= update.message.text

    def guardar_datos(modelo, compania, g2, g3, g4, notas):
      conn = sqlite3.connect('datos_telefonos.db')
      c = conn.cursor()
      
      try:
          c.execute('''
          INSERT INTO telefonos (modelo, compania, g2, g3, g4, notas) 
          VALUES (?, ?, ?, ?, ?, ?)
          ''', (modelo, compania, g2, g3, g4, notas))
          conn.commit()
          return True
      except sqlite3.IntegrityError:
          return False
      finally:
          conn.close()
    #await update.message.reply_text(f"""Gracias tus datos son: Modelo: {context.user_data['modelo']} Compañia: {context.user_data['company']} 2G:{context.user_data['g2']} 3G:{context.user_data['g3']} 4G:{context.user_data['g4']} NOTAS:{context.user_data['notas']}""")
    
    conn = sqlite3.connect('datos_telefonos.db')
    c = conn.cursor()
    
    modelo = context.user_data['modelo']
    compania = context.user_data['company']
    g2 = context.user_data['g2']
    g3 = context.user_data['g3']
    g4 = context.user_data['g4']
    notas = context.user_data['notas']

    c.execute('SELECT * FROM telefonos WHERE modelo=? AND compania=?', (modelo, compania))
    result = c.fetchone()
    
    if result:
        update.message.reply_text("El modelo y compañía ya existen en la base de datos.")
    else:
        if guardar_datos(modelo, compania, g2, g3, g4, notas):
            await update.message.reply_text("Datos guardados exitosamente.")
        else:
            await update.message.reply_text("Error al guardar los datos.")

    conn.close()
    
    return ConversationHandler.END
  
  async def buscar(update: Update, context: CallbackContext):
    def buscar_modelo(modelo):
      # Conectar a la base de datos
      conn = sqlite3.connect('datos_telefonos.db')
      cursor = conn.cursor()
      
      # Ejecutar la consulta para buscar el modelo
      cursor.execute("SELECT * FROM telefonos WHERE modelo LIKE ?", ('%' + modelo + '%',))
      
      # Obtener todos los resultados
      resultados = cursor.fetchall()
      
      # Cerrar la conexión
      conn.close()
      
      return resultados


    if context.args:
        modelo = ' '.join(context.args)
        resultados = buscar_modelo(modelo)
        
        # Verificar si se encontraron resultados
        if resultados:
            respuesta = "Coincidencias encontradas:\n"
            for fila in resultados:
                respuesta += (f"Modelo: {fila[1]}, Compañía: {fila[2]}, G2: {fila[3]}, "
                              f"G3: {fila[4]}, G4: {fila[5]}, Notas: {fila[6]}\n")
        else:
            respuesta = "No se encontraron coincidencias."
        
        await update.message.reply_text(respuesta)
    else:
        await update.message.reply_text("Por favor, proporciona un modelo para buscar, ejemplo /buscar A123U.")

  async def button_controller(update:Update,context:CallbackContext):
    await update.callback_query.answer()
    print(update.callback_query.data)
    
  

  async def cancel_conversation(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Operacion Cancelada")
    return ConversationHandler.END

  
  
  info_conversation_handler= ConversationHandler(
        entry_points=[CommandHandler('add', pedir_modelo)],
        states={
            MODEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, optener_modelo)],
            COMPANY: [MessageHandler(filters.TEXT & ~filters.COMMAND, optener_carrier)],
            G2: [MessageHandler(filters.TEXT & ~filters.COMMAND, obtener2g)],
            G3: [MessageHandler(filters.TEXT & ~filters.COMMAND, obtener3g)],
            G4: [MessageHandler(filters.TEXT & ~filters.COMMAND, obtener4g)],
            NOTES: [MessageHandler(filters.TEXT & ~filters.COMMAND, obtenernotas)],
            
        },
        fallbacks=[CommandHandler('cancel', cancel_conversation)]
    )