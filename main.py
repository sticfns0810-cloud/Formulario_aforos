import tkinter as tk
from tkinter import messagebox
import sqlite3

# Conexión a la base de datos
def conectar_db():
    return sqlite3.connect('formulario.db')

# Función para crear tablas si no existen
def crear_tablas():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS catalogos (
            id INTEGER PRIMARY KEY,
            nombre TEXT UNIQUE,
            valores TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY,
            datos TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Función principal de la app
def main():
    crear_tablas()
    root = tk.Tk()
    root.title("Formulario Aforos")
    root.geometry("400x300")

    label = tk.Label(root, text="Formulario básico - Próximos pasos: agregar campos dinámicos")
    label.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()