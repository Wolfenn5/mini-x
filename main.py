import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import mysql.connector
from ventana_VPub import VPub
from registro_log import insertar_registro_log 

# Conexión a la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="micro_x"
)

# Función para iniciar sesión
def iniciar_sesion():
    usuario = usuario_entry.get()
    contraseña = contraseña_entry.get()

    cursor = conexion.cursor()
    query = "SELECT * FROM usuarios WHERE usuario = %s AND contraseña = %s"
    cursor.execute(query, (usuario, contraseña))
    resultado = cursor.fetchone()
    cursor.close()

    if resultado:
        messagebox.showinfo("Inicio de sesión", "¡Inicio de sesión exitoso!")
        id_usuario = resultado[0]
        ventana_principal(id_usuario)  # Pasamos el id del usuario a la ventana principal

        # Registrar actividad de inicio de sesión en el log
        insertar_registro_log(id_usuario, "Inicio de sesión", f"Inicio de sesión exitoso para el usuario '{usuario}'")

    else:
        messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos.")
        limpiar_campos_iniciar_sesion()  # Limpiar los campos de entrada después de un inicio de sesión fallido

# Función para abrir la ventana principal
def ventana_principal(id_usuario):
    root.withdraw()  # Ocultar la ventana de inicio de sesión
    VPub(root, conexion, id_usuario)  # Abrir la ventana principal de publicaciones

# Función para manejar la selección de la imagen de perfil y el registro del usuario
def seleccionar_imagen_perfil():
    ruta_imagen = filedialog.askopenfilename()
    if ruta_imagen:
        registrar_usuario(ruta_imagen)

# Función para registrar un nuevo usuario
def registrar_usuario(ruta_imagen):
    nuevo_usuario = nuevo_usuario_entry.get()
    nueva_contraseña = nueva_contraseña_entry.get()

    cursor = conexion.cursor()
    query = "INSERT INTO usuarios (usuario, contraseña, foto_perfil) VALUES (%s, %s, %s)"
    cursor.execute(query, (nuevo_usuario, nueva_contraseña, ruta_imagen))
    conexion.commit()

    # Obtener el ID del usuario recién creado
    id_usuario = cursor.lastrowid

    cursor.close()

    messagebox.showinfo("Registro", "¡Usuario registrado exitosamente!")
    limpiar_campos()  # Limpiar los campos de entrada después de registrar un nuevo usuario

    # Registrar actividad de creación de usuario en el log
    insertar_registro_log(id_usuario, "Creación de usuario", f"Usuario '{nuevo_usuario}' registrado exitosamente")

# Función para limpiar los campos de entrada después de registrar un nuevo usuario
def limpiar_campos():
    nuevo_usuario_entry.delete(0, tk.END)
    nueva_contraseña_entry.delete(0, tk.END)

# Función para limpiar los campos de entrada después de un inicio de sesión fallido
def limpiar_campos_iniciar_sesion():
    usuario_entry.delete(0, tk.END)
    contraseña_entry.delete(0, tk.END)

# Crear ventana principal de inicio de sesión
root = tk.Tk()
root.title("Inicio de Sesión")
root.geometry("300x200")  # Establecer el tamaño de la ventana

# Componentes de la ventana principal
usuario_label = tk.Label(root, text="Usuario:")
usuario_label.grid(row=0, column=0, padx=5, pady=5)
usuario_entry = tk.Entry(root)
usuario_entry.grid(row=0, column=1, padx=5, pady=5)

contraseña_label = tk.Label(root, text="Contraseña:")
contraseña_label.grid(row=1, column=0, padx=5, pady=5)
contraseña_entry = tk.Entry(root, show="*")
contraseña_entry.grid(row=1, column=1, padx=5, pady=5)

iniciar_sesion_button = tk.Button(root, text="Iniciar Sesión", command=iniciar_sesion)
iniciar_sesion_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# Componentes para registrarse
nuevo_usuario_label = tk.Label(root, text="Nuevo Usuario:")
nuevo_usuario_label.grid(row=3, column=0, padx=5, pady=5)
nuevo_usuario_entry = tk.Entry(root)
nuevo_usuario_entry.grid(row=3, column=1, padx=5, pady=5)

nueva_contraseña_label = tk.Label(root, text="Nueva Contraseña:")
nueva_contraseña_label.grid(row=4, column=0, padx=5, pady=5)
nueva_contraseña_entry = tk.Entry(root, show="*")
nueva_contraseña_entry.grid(row=4, column=1, padx=5, pady=5)

seleccionar_imagen_button = tk.Button(root, text="Elegir avatar para concluir registro", command=seleccionar_imagen_perfil)
seleccionar_imagen_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
