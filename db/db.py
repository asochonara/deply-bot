import sqlite3

# Conectar a la base de datos (se creará si no existe)
conn = sqlite3.connect('telegram_bot_modelos.db')
c = conn.cursor()

# Crear la tabla si no existe
c.execute('''
    CREATE TABLE IF NOT EXISTS modelos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        modelo TEXT NOT NULL,
        g2 TEXT NOT NULL,
        g3 TEXT NOT NULL,
        g4 TEXT NOT NULL
    )
''')

# Guardar cambios y cerrar la conexión
conn.commit()
conn.close()