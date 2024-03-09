import tkinter as tk
from tkinter import messagebox
from registro_log import insertar_registro_log

def borrar_Cuas(master, id_publicacion, ventana_publicaciones, texto_anterior):
    # Confirmar la acción de borrar
    if messagebox.askyesno("Confirmar borrado", "¿Estás seguro de que quieres borrar esta publicación?"):
        # Borrar la publicación de la base de datos
        cursor = master.conexion.cursor()
        query = "DELETE FROM publicaciones WHERE id = %s"
        cursor.execute(query, (id_publicacion,))
        master.conexion.commit()
        cursor.close()

        # Registro en el log de actividad
        detalle = f"ID de Publicación: {id_publicacion} ({texto_anterior})"
        insertar_registro_log(master.id_usuario, "Borrado de publicación", detalle)
        
        # Mostrar mensaje de publicación borrada
        messagebox.showinfo("Publicación borrada", "La publicación ha sido borrada exitosamente.")
        
        # Cerrar la ventana de "Mis Publicaciones"
        ventana_publicaciones.destroy()

        # Actualizar las publicaciones en la ventana principal
        master.cargar_Cuas()

def editar_Cuas(master, id_publicacion, texto_anterior, ventana_publicaciones):
    def guardar_edicion():
        texto_nuevo = texto_entry.get()
        
        # Contar la cantidad de palabras en la publicación editada
        palabras = texto_nuevo.split()
        cantidad_palabras = len(palabras)

        # Verificar si la cantidad de palabras excede el límite permitido
        if cantidad_palabras > 50:
            messagebox.showerror("Error", "La publicación no puede exceder de 50 palabras.")
            return

        # Actualizar la publicación en la base de datos
        cursor = master.conexion.cursor()
        query = "UPDATE publicaciones SET texto = %s WHERE id = %s"
        cursor.execute(query, (texto_nuevo, id_publicacion))
        master.conexion.commit()
        cursor.close()

        # Insertar registro en el log de actividad
        insertar_registro_log(master.id_usuario, f"Edición de publicación (ID: {id_publicacion})", texto_nuevo)
        
        # Mostrar mensaje de edición exitosa
        messagebox.showinfo("Edición exitosa", "¡Tu publicación ha sido editada exitosamente!")

        # Cerrar la ventana de edición
        ventana_edicion.destroy()

        # Cerrar la ventana de "Mis Publicaciones"
        ventana_publicaciones.destroy()

        # Actualizar las publicaciones en la ventana principal
        master.cargar_Cuas()

    # Abrir ventana de edición
    ventana_edicion = tk.Toplevel(master)
    ventana_edicion.title("Editar Publicación")

    # Etiqueta y campo de texto para la edición
    tk.Label(ventana_edicion, text="VPubEdit", font=("Arial", 12, "bold")).pack(pady=10)
    texto_entry = tk.Entry(ventana_edicion, width=50)
    texto_entry.pack(padx=10, pady=5)
    texto_entry.insert(0, texto_anterior.split(" - ")[0])  # Mostrar solo el texto

    # Botón para guardar la edición
    guardar_button = tk.Button(ventana_edicion, text="Guardar", command=guardar_edicion)
    guardar_button.pack(pady=5)
