# Formulario Aforos

Aplicación de escritorio para gestionar formularios de aforos con base de datos SQLite.

## Instalación

1. Clona el repositorio: `git clone https://github.com/sticfns0810-cloud/Formulario_aforos.git`
2. Crea entorno virtual: `python -m venv venv`
3. Activa: `venv\Scripts\activate`
4. Instala dependencias: `pip install -r requirements.txt`
5. Ejecuta: `python main.py`

## Ejecutable

Descarga `dist/main.exe` y ejecuta directamente (no requiere instalación de Python).

## Funcionalidades

- Formulario con campos dinámicos.
- Gestión CRUD de catálogos (Clientes, Vehículos, Recipientes).
- Gestión de registros (Aforos).
- Cálculos automáticos.

## Campos Obligatorios (Manuales)

- Fecha
- Nombre (Cliente)
- Vehículo
- Foro
- Recipiente
- Cantidad (>0)
- Observación

## Notas

- Recipiente: Digitable con autocompletado.
- Tipo Servicio: Seleccionar Especial u Ordinario para aplicar tarifa.
- Mini Cargador: Checkbox para adicional.