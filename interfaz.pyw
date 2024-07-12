import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import json

# Obtener el directorio de documentos del usuario
directorios = os.path.expanduser('~')
ruta_archivo = os.path.join(directorios, 'Documents', 'rutas.json')

# Función para abrir carpetas
def abrir_carpetas(lista_carpetas):
    for carpeta in lista_carpetas:
        try:
            os.startfile(carpeta)
            print(f"Abriendo carpeta: {carpeta}")
        except Exception as e:
            print(f"No se pudo abrir la carpeta {carpeta}: {e}")

# Función para abrir un programa
def abrir_programa(ruta_programa):
    try:
        subprocess.Popen([ruta_programa], shell=True)
        print(f"Ejecutando programa: {ruta_programa}")
    except Exception as e:
        print(f"No se pudo ejecutar el programa {ruta_programa}: {e}")

# Función para seleccionar carpetas
def seleccionar_carpeta(entry):
    carpeta = filedialog.askdirectory()
    if carpeta:
        entry.delete(0, tk.END)
        entry.insert(0, carpeta)

# Función para seleccionar programa
def seleccionar_programa(entry):
    programa = filedialog.askopenfilename(filetypes=[("Ejecutables", "*.exe"), ("Todos los archivos", "*.*")])
    if programa:
        entry.delete(0, tk.END)
        entry.insert(0, programa)

# Función para ejecutar las acciones
def ejecutar():
    carpetas = [entry.get() for entry in entries_carpetas]
    programa = entry_programa.get()
    
    if all(carpetas) and programa:
        abrir_carpetas(carpetas)
        abrir_programa(programa)
    else:
        messagebox.showwarning("Advertencia", "Por favor, completa todas las rutas.")

# Función para agregar un nuevo slot de carpeta
def agregar_carpeta():
    entry = tk.Entry(root, width=50)
    entry.grid(row=len(entries_carpetas), column=1, padx=10, pady=5)
    btn = tk.Button(root, text="Seleccionar", command=lambda e=entry: seleccionar_carpeta(e))
    btn.grid(row=len(entries_carpetas), column=2, padx=10, pady=5)
    entries_carpetas.append(entry)
    buttons_carpetas.append(btn)

# Función para quitar el último slot de carpeta
def quitar_carpeta():
    if entries_carpetas:
        entry = entries_carpetas.pop()
        btn = buttons_carpetas.pop()
        entry.destroy()
        btn.destroy()

# Función para guardar las rutas en un archivo
def guardar_rutas():
    rutas = {
        "carpetas": [entry.get() for entry in entries_carpetas],
        "programa": entry_programa.get()
    }
    try:
        with open(ruta_archivo, 'w') as file:
            json.dump(rutas, file)
        messagebox.showinfo("Información", "Rutas guardadas correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")

# Función para cargar las rutas desde un archivo
def cargar_rutas():
    try:
        with open(ruta_archivo, 'r') as file:
            rutas = json.load(file)
            for _ in range(len(rutas["carpetas"]) - len(entries_carpetas)):
                agregar_carpeta()
            for entry, carpeta in zip(entries_carpetas, rutas["carpetas"]):
                entry.delete(0, tk.END)
                entry.insert(0, carpeta)
            entry_programa.delete(0, tk.END)
            entry_programa.insert(0, rutas["programa"])
    except FileNotFoundError:
        messagebox.showwarning("Advertencia", "No se encontró el archivo de rutas.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el archivo: {e}")

# Crear la ventana principal
root = tk.Tk()
root.title("Abrir Carpetas y Programa")

entries_carpetas = []
buttons_carpetas = []

# Crear el primer slot de carpeta por defecto
agregar_carpeta()

tk.Label(root, text="Programa:").grid(row=100, column=0, padx=10, pady=5)
entry_programa = tk.Entry(root, width=50)
entry_programa.grid(row=100, column=1, padx=10, pady=5)
btn_programa = tk.Button(root, text="Seleccionar", command=lambda: seleccionar_programa(entry_programa))
btn_programa.grid(row=100, column=2, padx=10, pady=5)

btn_agregar_carpeta = tk.Button(root, text="Agregar Carpeta", command=agregar_carpeta)
btn_agregar_carpeta.grid(row=101, column=0, padx=10, pady=5)

btn_quitar_carpeta = tk.Button(root, text="Quitar Carpeta", command=quitar_carpeta)
btn_quitar_carpeta.grid(row=101, column=1, padx=10, pady=5)

btn_guardar = tk.Button(root, text="Guardar Rutas", command=guardar_rutas)
btn_guardar.grid(row=102, column=0, padx=10, pady=5)

btn_cargar = tk.Button(root, text="Cargar Rutas", command=cargar_rutas)
btn_cargar.grid(row=102, column=1, padx=10, pady=5)

btn_ejecutar = tk.Button(root, text="Ejecutar", command=ejecutar)
btn_ejecutar.grid(row=103, column=0, columnspan=3, pady=20)

# Iniciar el bucle principal de la interfaz
root.mainloop()
