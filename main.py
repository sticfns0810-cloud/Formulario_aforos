import tkinter as tk
from tkinter import ttk, messagebox
import database

def calcular_subtotal(cantidad, recipiente, catalogos):
    if recipiente in catalogos['recipientes']:
        equivalencia = catalogos['recipientes'][recipiente]
        return cantidad * equivalencia if cantidad else 0
    return 0

def calcular_tarifa(valor, mini_extra, subtotal):
    return (valor + mini_extra) * subtotal if valor and subtotal else 0

def guardar():
    # Recopilar datos
    fecha = fecha_entry.get()
    nombre = nombre_combo.get()
    vehiculo = vehiculo_combo.get()
    foro = foro_entry.get()
    recipiente = recipiente_combo.get()
    cantidad = float(cantidad_entry.get()) if cantidad_entry.get() else 0
    subtotal = calcular_subtotal(cantidad, recipiente, catalogos)
    empresa = empresa_entry.get()  # Placeholder
    tipo_servicio = tipo_servicio_combo.get()
    valor = 0  # Placeholder, de clientes
    facturable = "No"  # Placeholder
    mini_cargador = 1 if mini_var.get() else 0
    mini_extra = 10 if mini_cargador else 0  # Valor extra fijo, ajustar
    observacion = observacion_text.get("1.0", tk.END).strip()
    tarifa = calcular_tarifa(valor, mini_extra, subtotal)

    # Validar obligatorios (placeholder, ajustar después)
    if not fecha or not nombre or not vehiculo or not foro or not recipiente or cantidad <= 0:
        messagebox.showerror("Error", "Completa los campos obligatorios")
        return

    datos = (fecha, nombre, vehiculo, foro, recipiente, cantidad, subtotal, empresa, tipo_servicio, valor, facturable, mini_cargador, observacion, tarifa)
    database.guardar_registro(datos)
    messagebox.showinfo("Éxito", "Registro guardado")
    # Limpiar campos
    fecha_entry.delete(0, tk.END)
    nombre_combo.set('')
    vehiculo_combo.set('')
    foro_entry.delete(0, tk.END)
    recipiente_combo.set('')
    cantidad_entry.delete(0, tk.END)
    empresa_entry.delete(0, tk.END)
    tipo_servicio_combo.set('')
    mini_var.set(0)
    observacion_text.delete("1.0", tk.END)

# Inicializar BD
database.crear_tablas()
database.insertar_datos_ejemplo()
catalogos = database.obtener_catalogos()

# GUI
root = tk.Tk()
root.title("Formulario Aforos")
root.geometry("600x700")

# Campos
tk.Label(root, text="FECHA").grid(row=0, column=0, sticky="w")
fecha_entry = tk.Entry(root)
fecha_entry.grid(row=0, column=1)

tk.Label(root, text="NOMBRE (Clientes)").grid(row=1, column=0, sticky="w")
nombre_combo = ttk.Combobox(root, values=[])  # Placeholder
nombre_combo.grid(row=1, column=1)

tk.Label(root, text="VEHICULO").grid(row=2, column=0, sticky="w")
vehiculo_combo = ttk.Combobox(root, values=list(catalogos['vehiculos'].keys()))
vehiculo_combo.grid(row=2, column=1)

tk.Label(root, text="FORO").grid(row=3, column=0, sticky="w")
foro_entry = tk.Entry(root)
foro_entry.grid(row=3, column=1)

tk.Label(root, text="RECIPIENTE").grid(row=4, column=0, sticky="w")
recipiente_combo = ttk.Combobox(root, values=list(catalogos['recipientes'].keys()))
recipiente_combo.grid(row=4, column=1)

tk.Label(root, text="CANTIDAD").grid(row=5, column=0, sticky="w")
cantidad_entry = tk.Entry(root)
cantidad_entry.grid(row=5, column=1)

tk.Label(root, text="SUBTOTAL").grid(row=6, column=0, sticky="w")
subtotal_label = tk.Label(root, text="0")
subtotal_label.grid(row=6, column=1)

tk.Label(root, text="EMPRESA").grid(row=7, column=0, sticky="w")
empresa_entry = tk.Entry(root)  # Placeholder
empresa_entry.grid(row=7, column=1)

tk.Label(root, text="TIPO_SERVICIO").grid(row=8, column=0, sticky="w")
tipo_servicio_combo = ttk.Combobox(root, values=["blanco", "ESPECIAL", "ORDINARIO"])
tipo_servicio_combo.grid(row=8, column=1)

tk.Label(root, text="VALOR").grid(row=9, column=0, sticky="w")
valor_label = tk.Label(root, text="0")  # Placeholder
valor_label.grid(row=9, column=1)

tk.Label(root, text="FACTURABLE").grid(row=10, column=0, sticky="w")
facturable_label = tk.Label(root, text="No")  # Placeholder
facturable_label.grid(row=10, column=1)

tk.Label(root, text="MINI_CARGADOR").grid(row=11, column=0, sticky="w")
mini_var = tk.IntVar()
mini_check = tk.Checkbutton(root, variable=mini_var)
mini_check.grid(row=11, column=1)

tk.Label(root, text="OBSERVACIÓN").grid(row=12, column=0, sticky="w")
observacion_text = tk.Text(root, height=3, width=30)
observacion_text.grid(row=12, column=1)

tk.Label(root, text="TARIFA").grid(row=13, column=0, sticky="w")
tarifa_label = tk.Label(root, text="0")
tarifa_label.grid(row=13, column=1)

# Botón guardar
tk.Button(root, text="Guardar", command=guardar).grid(row=14, column=0, columnspan=2)

root.mainloop()