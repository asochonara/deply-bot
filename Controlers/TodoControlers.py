import sqlite3
from telegram import Update
from telegram.ext import ContextTypes,CallbackContext,CommandHandler


class TodoControler:
   
   @staticmethod
   async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola, los comandos para agregar un modelo de telefono es: /add ejemplo A156U si si si, cada atributo de ''si'' estará asignado a 2g, 3g y 4g y para buscar es /buscar")
   
   @staticmethod
   async def add_todo(update: Update, context: CallbackContext) -> None:
      if (len(context.args) < 1):
        await update.message.reply_text("Error: Debes proporcionar un modelo y sus tipos de conexiones.")
        return
      
      # El primer argumento es el modelo
      modelo = context.args[0]
      # Los argumentos restantes son los tipos de conexión
      conexiones = context.args[1:]
      
      # Validar la cantidad de conexiones
      if (len(conexiones) != 3):
        await update.message.reply_text("Error: Debes proporcionar exactamente 3 valores (2G, 3G, 4G) despues del modelo.")
        return
      
      # Validar los valores de las conexiones
      if (not all(con in ['si', 'no'] for con in conexiones)):
        await update.message.reply_text("Error: Los valores deben ser 'si' o 'no'.")
        return
      
      # Insertar en la base de datos
      conn = sqlite3.connect('telegram_bot_modelos.db')
      c = conn.cursor()

      # Comprobar si el modelo ya existe
      c.execute("SELECT * FROM modelos WHERE modelo = ?", (modelo,))
      existing_model = c.fetchone()

      if existing_model:
        await update.message.reply_text(f"Error: El modelo {modelo} ya existe en la base de datos.")
      else:
        # Insertar en la base de datos
         c.execute("INSERT INTO modelos (modelo, g2, g3, g4) VALUES (?, ?, ?, ?)", (modelo, conexiones[0], conexiones[1], conexiones[2]))
         conn.commit()
         await update.message.reply_text(f"Modelo {modelo} agregado con éxito.")
         conn.close()
  
   @staticmethod
# Comando /buscar
   async def buscar_todo(update: Update, context: CallbackContext):
     if len(context.args) != 1:
        await update.message.reply_text("Por favor proporciona un modelo después del comando /buscar.")
        return
     # Función para buscar un modelo en la base de datos
     def buscar_modelo(modelo):
      conn = sqlite3.connect('telegram_bot_modelos.db')
      c = conn.cursor()
      c.execute('SELECT modelo, g2, g3, g4 FROM modelos WHERE modelo = ?', (modelo,))
      result = c.fetchone()
      conn.close()
      return result
    
     modelo = context.args[0]
     resultado = buscar_modelo(modelo)

     if (resultado):
        modelo_nombre, g2, g3, g4 = resultado
        await update.message.reply_text(f"{modelo_nombre} 2g-{g2} 3g-{g3} 4g-{g4}")
     else:
        await update.message.reply_text(f"Modelo {modelo} no encontrado.")

     
