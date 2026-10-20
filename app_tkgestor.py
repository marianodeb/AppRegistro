# Importa la función 'date' para capturar la fecha actual del sistema
from datetime import date

# Importa sqlite3 para gestionar la base de datos relacional local
import sqlite3

# Importa tkinter como 'tk' para la creación de la interfaz gráfica y ventanas
import tkinter as tk

# Importa el módulo ttk para componentes con estilos modernos (como Combobox)
from tkinter import ttk


# =====================================================================
# BLOQUE 1: CONEXIÓN Y CREACIÓN DE LA BASE DE DATOS SQLITE
# =====================================================================

# Establece la conexión con el archivo de la base de datos (lo crea si no existe)
conexion = sqlite3.connect("cosechas.db")

# Crea el cursor que permite ejecutar las consultas SQL
cursor = conexion.cursor()

# Ejecuta la sentencia SQL para crear la tabla 'cosecha' si todavía no fue creada
cursor.execute("""
    CREATE TABLE IF NOT EXISTS cosecha (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT,
        hortaliza TEXT,
        gramos TEXT
    )
""")

# Confirma y guarda permanentemente los cambios de la estructura en la base de datos
conexion.commit()


# =====================================================================
# BLOQUE 2: FUNCIÓN PUENTE (INTERFAZ GRÁFICA A BASE DE DATOS)
# =====================================================================

def guardar_datos():
    """Función que se ejecuta de forma exclusiva al hacer clic en el botón.
    Extrae los valores ingresados en los widgets y los almacena en SQLite.
    """
    # Extrae el texto actual del campo de la fecha
    f = entrada_fecha.get()

    # Extrae la opción seleccionada de la lista desplegable de hortalizas
    h = combo_hortaliza.get()

    # Extrae el número escrito en el campo de gramos
    g = entrada_gramos.get()

    # Ejecuta la inserción de los datos obtenidos dentro de la tabla SQL
    cursor.execute(
        "INSERT INTO cosecha (fecha, hortaliza, gramos) VALUES (?, ?, ?)",
        (f, h, g),
    )

    # Guarda de forma definitiva los cambios en la base de datos
    conexion.commit()

    # Imprime un reporte de control en la consola de la terminal
    print(f"Guardado -> Fecha: {f} | Hortaliza: {h} | Gramos: {g}")


# =====================================================================
# BLOQUE 3: CREACIÓN Y CONFIGURACIÓN DE LA VENTANA PRINCIPAL
# =====================================================================

# Instancia la ventana principal de la aplicación de escritorio
ventana = tk.Tk()

# Define el título que aparece en la barra superior de la ventana
ventana.title("Control de Cosecha")

# Establece el tamaño fijo de la ventana en píxeles (ancho x alto)
ventana.geometry("400x420")

# Bloquea la opción de redimensionar la ventana por parte del usuario
ventana.resizable(False, False)

# Cambia el color de fondo general de la ventana usando un código hexadecimal
ventana.configure(bg="#3a2f26")

# Intenta cargar y asignar el ícono a la ventana principal
try:
    icono = tk.PhotoImage(file="verduras.png")
    ventana.iconphoto(False, icono)
except Exception as e:
    print(f"Error cargando el ícono: {e}")

# =====================================================================
# BLOQUE 4: CONFIGURACIÓN DE ESTILOS Y MAPAS PARA EL COMBOBOX (TTK)
# =====================================================================

# Inicializa el motor de estilos adaptados para widgets modernos (ttk)
estilo = ttk.Style()

# Fuerza el uso del tema 'clam' para permitir la personalización de colores en Linux
estilo.theme_use("clam")

# Configura los colores generales, tipografía y bordes del selector
estilo.configure(
    "TCombobox",
    fieldbackground="#1b1712",  # Color de fondo de la caja interna
    background="#3a2f26",     # Color de fondo del botón lateral con la flecha
    foreground="#e2a24d",     # Color del texto seleccionado
    bordercolor="#3a2f26",     # Color del borde externo
    lightcolor="#3a2f26",     # Color de los brillos internos
    darkcolor="#1b1712"       # Color de las sombras internas
)

# Mapeo de estados del Combobox para prevenir cambios automáticos a gris o blanco
estilo.map(
    "TCombobox",
    fieldbackground=[("readonly", "#1b1712")],
    selectbackground=[("readonly", "#1b1712")],
    selectforeground=[("readonly", "#e2a24d")],
    bordercolor=[
        ("focus", "#3a2f26"),
        ("active", "#3a2f26"),
        ("readonly", "#3a2f26"),
    ],
    lightcolor=[
        ("focus", "#3a2f26"),
        ("active", "#3a2f26"),
        ("readonly", "#3a2f26"),
    ],
    darkcolor=[
        ("focus", "#1b1712"),
        ("active", "#1b1712"),
        ("readonly", "#1b1712"),
    ],
)

# Configura los colores del menú desplegable flotante de opciones (Listbox)
ventana.option_add("*TCombobox*Listbox.background",
                   "#1b1712")         # Fondo de la lista
# Color del texto de las opciones
ventana.option_add("*TCombobox*Listbox.foreground", "#ffffff")
# Color de fondo al marcar un elemento
ventana.option_add("*TCombobox*Listbox.selectBackground", "#5aa864")
# Color del texto al marcar un elemento
ventana.option_add("*TCombobox*Listbox.selectForeground", "#ffffff")


# =====================================================================
# BLOQUE 5: CREACIÓN DE LOS COMPONENTES VISUALES (WIDGETS)
# =====================================================================

# --- Etiqueta de la Fecha ---
label_fecha = tk.Label(
    ventana,
    text="Fecha (A-M-D):",
    bg="#3a2f26",
    fg="#e2616c",
    font=("Arial", 19),
    relief="flat",
    bd=0,
)
label_fecha.pack(pady=5)

# Captura la fecha actual del sistema en formato de texto (AAAA-MM-DD)
fecha_actual = date.today().strftime("%Y-%m-%d")

# --- Caja de Entrada de la Fecha ---
entrada_fecha = tk.Entry(
    ventana,
    bg="#1b1712",
    fg="#e2a24d",
    relief="flat",
    bd=0,
    highlightthickness=0,
    font=("Arial", 19),
)
entrada_fecha.insert(0, fecha_actual)  # Inserta la fecha actual por defecto
entrada_fecha.pack(pady=5)


# --- Etiqueta de la Hortaliza ---
label_hortaliza = tk.Label(
    ventana,
    text="Hortaliza:",
    bg="#3a2f26",
    fg="#e2616c",
    font=("Arial", 19)
)
label_hortaliza.pack(pady=5)

# Matriz con la lista completa de opciones de hortalizas
lista_hortalizas = [
    "Acelga", "Ajo", "Apio", "Arveja", "Batata", "Berenjena",
    "Brócoli", "Calabacín", "Cebolla", "Cebolla de verdeo",
    "Espinaca", "Frutilla", "Lechuga", "Maíz", "Papa", "Pepino",
    "Pimiento", "Rabanito", "Remolacha", "Repollo", "Tomate",
    "Zanahoria", "Zapallo kokena", "Zapallo veronez"
]

# --- Selector Desplegable de Hortalizas (Combobox) ---
combo_hortaliza = ttk.Combobox(
    ventana,
    values=lista_hortalizas,
    state="readonly",
    font=("Arial", 19),
    style="TCombobox",  # Vincula el selector con el estilo oscuro definido arriba
)
combo_hortaliza.set("Selecciona una hortaliza")  # Texto guía inicial
combo_hortaliza.pack(pady=5)


# --- Etiqueta de los Gramos ---
label_gramos = tk.Label(
    ventana,
    text="Gramos cosechados:",
    bg="#3a2f26",
    fg="#e2616c",
    font=("Arial", 19),
)
label_gramos.pack(pady=5)

# --- Caja de Entrada de los Gramos ---
entrada_gramos = tk.Entry(
    ventana,
    bg="#1b1712",
    fg="#e2a24d",
    relief="flat",
    bd=0,
    highlightthickness=0,
    font=("Arial", 19),
)
entrada_gramos.pack(pady=5)


# --- Botón de Guardado ---
boton = tk.Button(
    ventana,
    text="Guardar",
    font=("Arial", 19, "bold"),
    cursor="hand2",
    fg="#3a2f26",
    bg="#5aa864",
    relief="flat",
    bd=0,
    highlightthickness=0,
    command=guardar_datos,  # Conecta el clic del botón con la función de inserción SQL
)
boton.pack(pady=20)


# =====================================================================
# BLOQUE 6: INICIO DEL BUCLE PRINCIPAL DE LA APLICACIÓN
# =====================================================================

# Mantiene la ventana abierta en ejecución continua y a la escucha de eventos
ventana.mainloop()
