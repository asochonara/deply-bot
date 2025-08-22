import sqlite3

# Conectar a la base de datos (se creará si no existe)
conn = sqlite3.connect('datos_telefonos.db')
c = conn.cursor()

# Crear la tabla si no existe
c.execute('''
    CREATE TABLE IF NOT EXISTS telefonos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    modelo TEXT NOT NULL,
    compania TEXT NOT NULL,
    g2 TEXT,
    g3 TEXT,
    g4 TEXT,
    notas TEXT,
    UNIQUE(modelo, compania) -- Esto asegura que el mismo modelo no se repita con la misma compañía
    )
''')

# Guardar cambios y cerrar la conexión
conn.commit()
conn.close()