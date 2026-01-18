import tkinter as tk
from tkinter import ttk, messagebox
import database

def calcular_tarifa(valor, mini_extra, subtotal):
    return (valor + mini_extra) * subtotal if valor and subtotal else 0

def update_from_cliente():
    nombre = nombre_combo.get()
    tipo_servicio = tipo_servicio_var.get()
    cliente = catalogos['clientes'].get(nombre)
    if cliente:
        empresa_entry.delete(0, tk.END)
        empresa_entry.insert(0, cliente['empresa'])
        if tipo_servicio == cliente['tipo_servicio']:
            valor_label.config(text=str(cliente['valor']))
            facturable_label.config(text=cliente['facturable'])
        else:
            valor_label.config(text="0")
            facturable_label.config(text="No")
        # Mini
        mini_var.set(1 if cliente['mini_cargador'] > 0 else 0)
    else:
        empresa_entry.delete(0, tk.END)
        valor_label.config(text="0")
        facturable_label.config(text="No")
        mini_var.set(0)
    actualizar_calculos()

def on_nombre_select(event):
    update_from_cliente()

def on_tipo_servicio_change():
    update_from_cliente()

def actualizar_calculos():
    cantidad = float(cantidad_entry.get()) if cantidad_entry.get() else 0
    recipiente = recipiente_combo.get()
    subtotal = calcular_subtotal(cantidad, recipiente, catalogos)
    subtotal_label.config(text=str(subtotal))
    valor = float(valor_label.cget("text")) if valor_label.cget("text") else 0
    mini_extra = float(catalogos['clientes'].get(nombre_combo.get(), {}).get('mini_cargador', 0)) if mini_var.get() else 0
    tarifa = calcular_tarifa(valor, mini_extra, subtotal)
    tarifa_label.config(text=str(tarifa))

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
    tipo_servicio = tipo_servicio_var.get()
    cliente = catalogos['clientes'].get(nombre)
    if cliente:
        if tipo_servicio == cliente['tipo_servicio']:
            valor = cliente['valor']
            facturable = cliente['facturable']
        else:
            valor = 0
            facturable = "No"
        empresa = cliente['empresa']
    else:
        valor = 0
        facturable = "No"
        empresa = ""
    mini_cargador = 1 if mini_var.get() else 0
    mini_extra = float(catalogos['clientes'].get(nombre, {}).get('mini_cargador', 0)) if mini_cargador else 0
    observacion = observacion_text.get("1.0", tk.END).strip()
    tarifa = float(tarifa_label.cget("text")) if tarifa_label.cget("text") else 0

    # Validar obligatorios (manuales)
    if not fecha or not nombre or not vehiculo or not foro or not recipiente or cantidad <= 0 or not observacion.strip():
        messagebox.showerror("Error", "Completa los campos obligatorios: Fecha, Nombre, Vehículo, Foro, Recipiente, Cantidad, Observación")
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
tk.Label(root, text="FECHA (DD/MM/YYYY)").grid(row=0, column=0, sticky="w")
fecha_entry = tk.Entry(root)
fecha_entry.grid(row=0, column=1)

tk.Label(root, text="NOMBRE (Clientes)").grid(row=1, column=0, sticky="w")
nombre_combo = ttk.Combobox(root, values=list(catalogos['clientes'].keys()))
nombre_combo.grid(row=1, column=1)
nombre_combo.bind("<<ComboboxSelected>>", on_nombre_select)

tk.Label(root, text="VEHICULO").grid(row=2, column=0, sticky="w")
vehiculo_combo = ttk.Combobox(root, values=list(catalogos['vehiculos'].keys()))
vehiculo_combo.grid(row=2, column=1)

tk.Label(root, text="FORO").grid(row=3, column=0, sticky="w")
foro_entry = tk.Entry(root)
foro_entry.grid(row=3, column=1)

tk.Label(root, text="RECIPIENTE").grid(row=4, column=0, sticky="w")
recipiente_var = tk.StringVar()
recipiente_combo = ttk.Combobox(root, textvariable=recipiente_var, values=list(catalogos['recipientes'].keys()))
recipiente_combo.grid(row=4, column=1)
def filter_recipientes(event):
    typed = recipiente_var.get()
    if typed == '':
        recipiente_combo['values'] = list(catalogos['recipientes'].keys())
    else:
        filtered = [r for r in catalogos['recipientes'] if typed.lower() in r.lower()]
        recipiente_combo['values'] = filtered
recipiente_combo.bind('<KeyRelease>', filter_recipientes)

tk.Label(root, text="CANTIDAD").grid(row=5, column=0, sticky="w")
cantidad_entry = tk.Entry(root)
cantidad_entry.grid(row=5, column=1)
cantidad_entry.bind("<KeyRelease>", lambda e: actualizar_calculos())

tk.Label(root, text="SUBTOTAL").grid(row=6, column=0, sticky="w")
subtotal_label = tk.Label(root, text="0")
subtotal_label.grid(row=6, column=1)

tk.Label(root, text="EMPRESA").grid(row=7, column=0, sticky="w")
empresa_entry = tk.Entry(root)  # Placeholder
empresa_entry.grid(row=7, column=1)

tk.Label(root, text="TIPO_SERVICIO").grid(row=8, column=0, sticky="w")
tipo_servicio_var = tk.StringVar()
tipo_servicio_var.set("")  # Blanco por defecto
tk.Radiobutton(root, text="ESPECIAL", variable=tipo_servicio_var, value="ESPECIAL", command=on_tipo_servicio_change).grid(row=8, column=1, sticky="w")
tk.Radiobutton(root, text="ORDINARIO", variable=tipo_servicio_var, value="ORDINARIO", command=on_tipo_servicio_change).grid(row=8, column=1)

tk.Label(root, text="VALOR").grid(row=9, column=0, sticky="w")
valor_label = tk.Label(root, text="0")  # Placeholder
valor_label.grid(row=9, column=1)

tk.Label(root, text="FACTURABLE").grid(row=10, column=0, sticky="w")
facturable_label = tk.Label(root, text="No")  # Placeholder
facturable_label.grid(row=10, column=1)

tk.Label(root, text="MINI_CARGADOR").grid(row=11, column=0, sticky="w")
mini_var = tk.IntVar()
mini_check = tk.Checkbutton(root, variable=mini_var, command=actualizar_calculos)
mini_check.grid(row=11, column=1)

tk.Label(root, text="OBSERVACIÓN").grid(row=12, column=0, sticky="w")
observacion_text = tk.Text(root, height=3, width=30)
observacion_text.grid(row=12, column=1)

tk.Label(root, text="TARIFA").grid(row=13, column=0, sticky="w")
tarifa_label = tk.Label(root, text="0")
tarifa_label.grid(row=13, column=1)

def abrir_gestion():
    pass  # Placeholder

# Botón gestionar
tk.Button(root, text="Gestionar Catálogos y Aforos", command=abrir_gestion).grid(row=15, column=0, columnspan=2, pady=10)

def abrir_gestion():
    global catalogos
    gestion_window = tk.Toplevel(root)
    gestion_window.title("Gestión de Catálogos y Aforos")
    gestion_window.geometry("800x600")

    notebook = ttk.Notebook(gestion_window)
    notebook.pack(fill="both", expand=True)

    # Pestaña Clientes
    frame_clientes = ttk.Frame(notebook)
    notebook.add(frame_clientes, text="Clientes")

    tree_clientes = ttk.Treeview(frame_clientes, columns=("ID", "Nombre", "Empresa", "Tipo_Servicio", "Valor", "Facturable", "Mini_Cargador", "Observacion", "Estado"), show="headings")
    for col in tree_clientes["columns"]:
        tree_clientes.heading(col, text=col)
        tree_clientes.column(col, width=80)
    tree_clientes.pack(fill="both", expand=True)

    def cargar_clientes():
        for row in tree_clientes.get_children():
            tree_clientes.delete(row)
        for row in database.get_clientes():
            tree_clientes.insert("", "end", values=row)

    cargar_clientes()

    btn_frame_c = ttk.Frame(frame_clientes)
    btn_frame_c.pack()
    ttk.Button(btn_frame_c, text="Agregar", command=lambda: agregar_cliente(cargar_clientes)).pack(side="left")
    ttk.Button(btn_frame_c, text="Editar", command=lambda: editar_cliente(tree_clientes, cargar_clientes)).pack(side="left")
    ttk.Button(btn_frame_c, text="Eliminar", command=lambda: eliminar_cliente(tree_clientes, cargar_clientes)).pack(side="left")

    # Similar para Vehículos
    frame_vehiculos = ttk.Frame(notebook)
    notebook.add(frame_vehiculos, text="Vehículos")

    tree_vehiculos = ttk.Treeview(frame_vehiculos, columns=("ID", "Placa", "Alquiler", "Tipo"), show="headings")
    for col in ["ID", "Placa", "Alquiler", "Tipo"]:
        tree_vehiculos.heading(col, text=col)
        tree_vehiculos.column(col, width=100)
    tree_vehiculos.pack(fill="both", expand=True)

    def cargar_vehiculos():
        for row in tree_vehiculos.get_children():
            tree_vehiculos.delete(row)
        for row in database.get_vehiculos():
            tree_vehiculos.insert("", "end", values=row)

    cargar_vehiculos()

    btn_frame_v = ttk.Frame(frame_vehiculos)
    btn_frame_v.pack()
    ttk.Button(btn_frame_v, text="Agregar", command=lambda: agregar_vehiculo(cargar_vehiculos)).pack(side="left")
    ttk.Button(btn_frame_v, text="Editar", command=lambda: editar_vehiculo(tree_vehiculos, cargar_vehiculos)).pack(side="left")
    ttk.Button(btn_frame_v, text="Eliminar", command=lambda: eliminar_vehiculo(tree_vehiculos, cargar_vehiculos)).pack(side="left")

    # Similar para Recipientes
    frame_recipientes = ttk.Frame(notebook)
    notebook.add(frame_recipientes, text="Recipientes")

    tree_recipientes = ttk.Treeview(frame_recipientes, columns=("ID", "Recipiente", "Equivalencia"), show="headings")
    for col in ["ID", "Recipiente", "Equivalencia"]:
        tree_recipientes.heading(col, text=col)
        tree_recipientes.column(col, width=100)
    tree_recipientes.pack(fill="both", expand=True)

    def cargar_recipientes():
        for row in tree_recipientes.get_children():
            tree_recipientes.delete(row)
        for row in database.get_recipientes():
            tree_recipientes.insert("", "end", values=row)

    cargar_recipientes()

    btn_frame_r = ttk.Frame(frame_recipientes)
    btn_frame_r.pack()
    ttk.Button(btn_frame_r, text="Agregar", command=lambda: agregar_recipiente(cargar_recipientes)).pack(side="left")
    ttk.Button(btn_frame_r, text="Editar", command=lambda: editar_recipiente(tree_recipientes, cargar_recipientes)).pack(side="left")
    ttk.Button(btn_frame_r, text="Eliminar", command=lambda: eliminar_recipiente(tree_recipientes, cargar_recipientes)).pack(side="left")

    # Pestaña Aforos
    frame_aforos = ttk.Frame(notebook)
    notebook.add(frame_aforos, text="Aforos")

    tree_aforos = ttk.Treeview(frame_aforos, columns=("ID", "Fecha", "Nombre", "Vehiculo", "Foro", "Recipiente", "Cantidad", "Subtotal", "Empresa", "Tipo_Servicio", "Valor", "Facturable", "Mini_Cargador", "Observacion", "Tarifa"), show="headings")
    for col in tree_aforos["columns"]:
        tree_aforos.heading(col, text=col)
        tree_aforos.column(col, width=80)
    tree_aforos.pack(fill="both", expand=True)

    def cargar_aforos():
        for row in tree_aforos.get_children():
            tree_aforos.delete(row)
        for row in database.get_registros():
            tree_aforos.insert("", "end", values=row)

    cargar_aforos()

    btn_frame_a = ttk.Frame(frame_aforos)
    btn_frame_a.pack()
    ttk.Button(btn_frame_a, text="Editar", command=lambda: editar_aforo(tree_aforos, cargar_aforos)).pack(side="left")
    ttk.Button(btn_frame_a, text="Eliminar", command=lambda: eliminar_aforo(tree_aforos, cargar_aforos)).pack(side="left")

# Funciones para dialogs
def agregar_cliente(callback):
    dialog = tk.Toplevel()
    dialog.title("Agregar Cliente")
    entries = {}
    fields = ["Nombre", "Empresa", "Tipo_Servicio", "Valor", "Facturable", "Mini_Cargador", "Observacion", "Estado"]
    for i, field in enumerate(fields):
        tk.Label(dialog, text=field).grid(row=i, column=0)
        entries[field] = tk.Entry(dialog)
        entries[field].grid(row=i, column=1)
    def save():
        datos = tuple(entries[f].get() for f in fields)
        try:
            database.insert_cliente(datos)
            callback()
            dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    tk.Button(dialog, text="Guardar", command=save).grid(row=len(fields), column=0, columnspan=2)

def editar_cliente(tree, callback):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Advertencia", "Selecciona un cliente")
        return
    item = tree.item(selected[0])
    values = item["values"]
    dialog = tk.Toplevel()
    dialog.title("Editar Cliente")
    entries = {}
    fields = ["Nombre", "Empresa", "Tipo_Servicio", "Valor", "Facturable", "Mini_Cargador", "Observacion", "Estado"]
    for i, field in enumerate(fields):
        tk.Label(dialog, text=field).grid(row=i, column=0)
        entries[field] = tk.Entry(dialog)
        entries[field].insert(0, values[i+1])
        entries[field].grid(row=i, column=1)
    def save():
        datos = tuple(entries[f].get() for f in fields)
        try:
            database.update_cliente(values[0], datos)
            callback()
            dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    tk.Button(dialog, text="Guardar", command=save).grid(row=len(fields), column=0, columnspan=2)

def eliminar_cliente(tree, callback):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Advertencia", "Selecciona un cliente")
        return
    if messagebox.askyesno("Confirmar", "¿Eliminar cliente?"):
        item = tree.item(selected[0])
        id = item["values"][0]
        try:
            database.delete_cliente(id)
            callback()
        except Exception as e:
            messagebox.showerror("Error", str(e))

# Similar para vehiculos
def agregar_vehiculo(callback):
    dialog = tk.Toplevel()
    dialog.title("Agregar Vehículo")
    entries = {}
    fields = ["Placa", "Alquiler", "Tipo"]
    for i, field in enumerate(fields):
        tk.Label(dialog, text=field).grid(row=i, column=0)
        entries[field] = tk.Entry(dialog)
        entries[field].grid(row=i, column=1)
    def save():
        datos = (entries["Placa"].get(), float(entries["Alquiler"].get()) if entries["Alquiler"].get() else None, entries["Tipo"].get())
        try:
            database.insert_vehiculo(datos)
            callback()
            dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    tk.Button(dialog, text="Guardar", command=save).grid(row=len(fields), column=0, columnspan=2)

def editar_vehiculo(tree, callback):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Advertencia", "Selecciona un vehículo")
        return
    item = tree.item(selected[0])
    values = item["values"]
    dialog = tk.Toplevel()
    dialog.title("Editar Vehículo")
    entries = {}
    fields = ["Placa", "Alquiler", "Tipo"]
    for i, field in enumerate(fields):
        tk.Label(dialog, text=field).grid(row=i, column=0)
        entries[field] = tk.Entry(dialog)
        entries[field].insert(0, values[i+1] if values[i+1] else "")
        entries[field].grid(row=i, column=1)
    def save():
        datos = (entries["Placa"].get(), float(entries["Alquiler"].get()) if entries["Alquiler"].get() else None, entries["Tipo"].get())
        try:
            database.update_vehiculo(values[0], datos)
            callback()
            dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    tk.Button(dialog, text="Guardar", command=save).grid(row=len(fields), column=0, columnspan=2)

def eliminar_vehiculo(tree, callback):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Advertencia", "Selecciona un vehículo")
        return
    if messagebox.askyesno("Confirmar", "¿Eliminar vehículo?"):
        item = tree.item(selected[0])
        id = item["values"][0]
        try:
            database.delete_vehiculo(id)
            callback()
        except Exception as e:
            messagebox.showerror("Error", str(e))

# Similar para recipientes
def agregar_recipiente(callback):
    dialog = tk.Toplevel()
    dialog.title("Agregar Recipiente")
    entries = {}
    fields = ["Recipiente", "Equivalencia"]
    for i, field in enumerate(fields):
        tk.Label(dialog, text=field).grid(row=i, column=0)
        entries[field] = tk.Entry(dialog)
        entries[field].grid(row=i, column=1)
    def save():
        datos = (entries["Recipiente"].get(), float(entries["Equivalencia"].get()))
        try:
            database.insert_recipiente(datos)
            callback()
            dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    tk.Button(dialog, text="Guardar", command=save).grid(row=len(fields), column=0, columnspan=2)

def editar_recipiente(tree, callback):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Advertencia", "Selecciona un recipiente")
        return
    item = tree.item(selected[0])
    values = item["values"]
    dialog = tk.Toplevel()
    dialog.title("Editar Recipiente")
    entries = {}
    fields = ["Recipiente", "Equivalencia"]
    for i, field in enumerate(fields):
        tk.Label(dialog, text=field).grid(row=i, column=0)
        entries[field] = tk.Entry(dialog)
        entries[field].insert(0, values[i+1])
        entries[field].grid(row=i, column=1)
    def save():
        datos = (entries["Recipiente"].get(), float(entries["Equivalencia"].get()))
        try:
            database.update_recipiente(values[0], datos)
            callback()
            dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    tk.Button(dialog, text="Guardar", command=save).grid(row=len(fields), column=0, columnspan=2)

def eliminar_recipiente(tree, callback):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Advertencia", "Selecciona un recipiente")
        return
    if messagebox.askyesno("Confirmar", "¿Eliminar recipiente?"):
        item = tree.item(selected[0])
        id = item["values"][0]
        try:
            database.delete_recipiente(id)
            callback()
        except Exception as e:
            messagebox.showerror("Error", str(e))

# Para aforos
def editar_aforo(tree, callback):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Advertencia", "Selecciona un aforo")
        return
    item = tree.item(selected[0])
    values = item["values"]
    # Abrir formulario con datos pre-llenados (simplificado, usar dialog similar)
    dialog = tk.Toplevel()
    dialog.title("Editar Aforo")
    entries = {}
    fields = ["Fecha", "Nombre", "Vehiculo", "Foro", "Recipiente", "Cantidad", "Empresa", "Tipo_Servicio", "Valor", "Facturable", "Mini_Cargador", "Observacion", "Tarifa"]
    for i, field in enumerate(fields):
        tk.Label(dialog, text=field).grid(row=i, column=0)
        entries[field] = tk.Entry(dialog)
        entries[field].insert(0, values[i+1] if values[i+1] else "")
        entries[field].grid(row=i, column=1)
    def save():
        datos = tuple(entries[f].get() for f in fields[:-1]) + (float(entries["Tarifa"].get()),)
        try:
            database.update_registro(values[0], datos)
            callback()
            dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    tk.Button(dialog, text="Guardar", command=save).grid(row=len(fields), column=0, columnspan=2)

def eliminar_aforo(tree, callback):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Advertencia", "Selecciona un aforo")
        return
    if messagebox.askyesno("Confirmar", "¿Eliminar aforo?"):
        item = tree.item(selected[0])
        id = item["values"][0]
        try:
            database.delete_registro(id)
            callback()
        except Exception as e:
            messagebox.showerror("Error", str(e))

root.mainloop()