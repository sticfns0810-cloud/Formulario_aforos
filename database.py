import sqlite3
import os
import sys

if getattr(sys, 'frozen', False):
    # Si es .exe
    db_dir = os.path.dirname(sys.executable)
else:
    db_dir = os.getcwd()

DB_PATH = os.path.join(db_dir, 'formulario.db')

def conectar_db():
    return sqlite3.connect(DB_PATH)

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
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY,
            nombre TEXT UNIQUE,
            empresa TEXT,
            tipo_servicio TEXT,
            valor REAL,
            facturable TEXT,
            mini_cargador REAL,
            observacion TEXT,
            estado TEXT
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
    # Vehículos - solo si no existen
    cursor.execute("SELECT COUNT(*) FROM vehiculos")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO vehiculos (placa, alquiler, tipo) VALUES (?, ?, ?)", ("ABC123", 100, "Camión"))
        cursor.execute("INSERT INTO vehiculos (placa, alquiler, tipo) VALUES (?, ?, ?)", ("DEF456", None, None))
    # Recipientes - solo si no existen
    cursor.execute("SELECT COUNT(*) FROM recipientes")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO recipientes (recipiente, equivalencia) VALUES (?, ?)", ("Tanque 1000L", 1.5))
        cursor.execute("INSERT INTO recipientes (recipiente, equivalencia) VALUES (?, ?)", ("Bidón 200L", 0.8))
    # Clientes - solo si no existen
    cursor.execute("SELECT COUNT(*) FROM clientes")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO clientes (nombre, empresa, tipo_servicio, valor, facturable, mini_cargador, observacion, estado) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", ("Cliente1", "Empresa1", "ESPECIAL", 50, "si", 5, "Nota1", "activo"))
        cursor.execute("INSERT INTO clientes (nombre, empresa, tipo_servicio, valor, facturable, mini_cargador, observacion, estado) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", ("Cliente2", "Empresa2", "ORDINARIO", 30, "no", 0, "Nota2", "activo"))
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
    # Clientes
    cursor.execute("SELECT nombre, empresa, tipo_servicio, valor, facturable, mini_cargador, observacion, estado FROM clientes WHERE estado = 'activo'")
    clientes = {}
    for row in cursor.fetchall():
        clientes[row[0]] = {
            'empresa': row[1],
            'tipo_servicio': row[2],
            'valor': row[3],
            'facturable': row[4],
            'mini_cargador': row[5],
            'observacion': row[6],
            'estado': row[7]
        }
    catalogos['clientes'] = clientes
    conn.close()
    return catalogos

def insert_cliente(datos):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO clientes (nombre, empresa, tipo_servicio, valor, facturable, mini_cargador, observacion, estado)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', datos)
    conn.commit()
    conn.close()

def update_cliente(id, datos):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE clientes SET nombre=?, empresa=?, tipo_servicio=?, valor=?, facturable=?, mini_cargador=?, observacion=?, estado=?
        WHERE id=?
    ''', datos + (id,))
    conn.commit()
    conn.close()

def delete_cliente(id):
    conn = conectar_db()
    cursor = conn.cursor()
    # Verificar vínculos
    cursor.execute("SELECT COUNT(*) FROM registros WHERE nombre = (SELECT nombre FROM clientes WHERE id=?)", (id,))
    if cursor.fetchone()[0] > 0:
        conn.close()
        raise ValueError("No se puede eliminar: hay registros vinculados")
    cursor.execute("DELETE FROM clientes WHERE id=?", (id,))
    conn.commit()
    conn.close()

def get_clientes():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, empresa, tipo_servicio, valor, facturable, mini_cargador, observacion, estado FROM clientes")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Similar para vehiculos
def insert_vehiculo(datos):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO vehiculos (placa, alquiler, tipo)
        VALUES (?, ?, ?)
    ''', datos)
    conn.commit()
    conn.close()

def update_vehiculo(id, datos):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE vehiculos SET placa=?, alquiler=?, tipo=?
        WHERE id=?
    ''', datos + (id,))
    conn.commit()
    conn.close()

def delete_vehiculo(id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM registros WHERE vehiculo = (SELECT placa FROM vehiculos WHERE id=?)", (id,))
    if cursor.fetchone()[0] > 0:
        conn.close()
        raise ValueError("No se puede eliminar: hay registros vinculados")
    cursor.execute("DELETE FROM vehiculos WHERE id=?", (id,))
    conn.commit()
    conn.close()

def get_vehiculos():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, placa, alquiler, tipo FROM vehiculos")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Similar para recipientes
def insert_recipiente(datos):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO recipientes (recipiente, equivalencia)
        VALUES (?, ?)
    ''', datos)
    conn.commit()
    conn.close()

def update_recipiente(id, datos):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE recipientes SET recipiente=?, equivalencia=?
        WHERE id=?
    ''', datos + (id,))
    conn.commit()
    conn.close()

def delete_recipiente(id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM registros WHERE recipiente = (SELECT recipiente FROM recipientes WHERE id=?)", (id,))
    if cursor.fetchone()[0] > 0:
        conn.close()
        raise ValueError("No se puede eliminar: hay registros vinculados")
    cursor.execute("DELETE FROM recipientes WHERE id=?", (id,))
    conn.commit()
    conn.close()

def get_recipientes():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, recipiente, equivalencia FROM recipientes")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Para registros
def get_registros():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, fecha, nombre, vehiculo, foro, recipiente, cantidad, subtotal, empresa, tipo_servicio, valor, facturable, mini_cargador, observacion, tarifa FROM registros")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_registro(id, datos):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE registros SET fecha=?, nombre=?, vehiculo=?, foro=?, recipiente=?, cantidad=?, subtotal=?, empresa=?, tipo_servicio=?, valor=?, facturable=?, mini_cargador=?, observacion=?, tarifa=?
        WHERE id=?
    ''', datos + (id,))
    conn.commit()
    conn.close()

def delete_registro(id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM registros WHERE id=?", (id,))
    conn.commit()
    conn.close()

def importar_csv(tabla, archivo):
    import csv
    conn = conectar_db()
    cursor = conn.cursor()
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            for row in reader:
                placeholders = ','.join(['?' for _ in headers])
                cursor.execute(f"INSERT OR IGNORE INTO {tabla} ({','.join(headers)}) VALUES ({placeholders})", row)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        conn.close()
        raise e