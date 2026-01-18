import sqlite3

def conectar_db():
    return sqlite3.connect('formulario.db')

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
            fecha TEXT,
            nombre TEXT,
            vehiculo TEXT,
            foro TEXT,
            recipiente TEXT,
            cantidad REAL,
            subtotal REAL,
            empresa TEXT,
            tipo_servicio TEXT,
            valor REAL,
            facturable TEXT,
            mini_cargador INTEGER,
            observacion TEXT,
            tarifa REAL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehiculos (
            id INTEGER PRIMARY KEY,
            placa TEXT UNIQUE,
            alquiler REAL,
            tipo TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipientes (
            id INTEGER PRIMARY KEY,
            recipiente TEXT,
            equivalencia REAL
        )
    ''')
    conn.commit()
    conn.close()

def insertar_datos_ejemplo():
    conn = conectar_db()
    cursor = conn.cursor()
    # Vehículos
    cursor.execute("INSERT OR IGNORE INTO vehiculos (placa, alquiler, tipo) VALUES (?, ?, ?)", ("ABC123", 100, "Camión"))
    cursor.execute("INSERT OR IGNORE INTO vehiculos (placa, alquiler, tipo) VALUES (?, ?, ?)", ("DEF456", None, None))
    # Recipientes
    cursor.execute("INSERT OR IGNORE INTO recipientes (recipiente, equivalencia) VALUES (?, ?)", ("Tanque 1000L", 1.5))
    cursor.execute("INSERT OR IGNORE INTO recipientes (recipiente, equivalencia) VALUES (?, ?)", ("Bidón 200L", 0.8))
    conn.commit()
    conn.close()

def obtener_catalogos():
    conn = conectar_db()
    cursor = conn.cursor()
    catalogos = {}
    # Vehículos
    cursor.execute("SELECT placa, alquiler, tipo FROM vehiculos")
    vehiculos = {row[0]: {'alquiler': row[1], 'tipo': row[2]} for row in cursor.fetchall()}
    catalogos['vehiculos'] = vehiculos
    # Recipientes
    cursor.execute("SELECT recipiente, equivalencia FROM recipientes")
    recipientes = {row[0]: row[1] for row in cursor.fetchall()}
    catalogos['recipientes'] = recipientes
    conn.close()
    return catalogos

def guardar_registro(datos):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO registros (fecha, nombre, vehiculo, foro, recipiente, cantidad, subtotal, empresa, tipo_servicio, valor, facturable, mini_cargador, observacion, tarifa)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', datos)
    conn.commit()
    conn.close()