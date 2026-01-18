import sqlite3

def conectar_db():
    return sqlite3.connect('formulario.db')

def obtener_catalogos():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, valores FROM catalogos")
    catalogos = {row[0]: row[1].split(',') for row in cursor.fetchall()}
    conn.close()
    return catalogos

def guardar_registro(datos):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO registros (datos) VALUES (?)", (str(datos),))
    conn.commit()
    conn.close()

def agregar_catalogo(nombre, valores):
    conn = conectar_db()
    cursor = conn.cursor()
    valores_str = ','.join(valores)
    cursor.execute("INSERT OR REPLACE INTO catalogos (nombre, valores) VALUES (?, ?)", (nombre, valores_str))
    conn.commit()
    conn.close()