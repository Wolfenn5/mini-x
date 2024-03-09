import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from ventana_VMisPub import borrar_Cuas, editar_Cuas
from registro_log import insertar_registro_log

class VNuevaPub(tk.Toplevel):
    def __init__(self, master, ventana_principal):
        super().__init__(master)
        self.title("Nueva Publicación")
        self.ventana_principal = ventana_principal
        self.imagen_path = None  # Inicializar imagen_path con None (por si se llega a publicar sin foto)

        self.texto_publicacion_entry = tk.Entry(self, width=50)
        self.texto_publicacion_entry.pack(padx=10, pady=10)

        # Nuevo botón para añadir imagen
        añadir_imagen_button = tk.Button(self, text="Añadir Imagen", command=self.seleccionar_imagen)
        añadir_imagen_button.pack(side=tk.LEFT, padx=5)

        listo_button = tk.Button(self, text="Listo!", command=self.guardar_y_actualizar)
        listo_button.pack(padx=10, pady=10)

    def guardar_y_actualizar(self):
        texto_publicacion = self.texto_publicacion_entry.get()

        # Obtener la ruta de la imagen seleccionada
        imagen_path = self.imagen_path

        # Contar la cantidad de palabras en la publicación
        palabras = texto_publicacion.split()
        cantidad_palabras = len(palabras)

        # Verificar si la cantidad de palabras excede el límite permitido
        if cantidad_palabras > 50:
            messagebox.showerror("Error", "La publicación no puede exceder de 50 palabras.")
            return

        # Insertar la nueva publicación en la base de datos con fecha y hora actuales
        cursor = self.ventana_principal.conexion.cursor()
        query = "INSERT INTO publicaciones (id_usuario, texto, fecha_hora, imagen) VALUES (%s, %s, NOW(), %s)"
        cursor.execute(query, (self.ventana_principal.id_usuario, texto_publicacion, imagen_path))
        self.ventana_principal.conexion.commit()
        cursor.close()

        # Registro en el log de actividad
        insertar_registro_log(self.ventana_principal.id_usuario, "Nueva Publicación", texto_publicacion)
        
        # Mostrar mensaje de publicación exitosa
        messagebox.showinfo("Publicación exitosa", "¡Tu publicación ha sido exitosa!")

        # Cerrar la ventana de nueva publicación
        self.destroy()

        # Actualizar las publicaciones en la ventana principal
        self.ventana_principal.cargar_Cuas()


    def seleccionar_imagen(self):
        filename = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=(("Archivos de imagen", "*.png;*.jpg;*.jpeg"), ("Todos los archivos", "*.*")))
        if filename:
            # Almacenar la ruta de la imagen seleccionada
            self.imagen_path = filename
            # Aquí puedes mostrar la imagen seleccionada o manejarla según tus necesidades
            messagebox.showinfo("Imagen seleccionada", f"Se seleccionó la imagen: {filename}")


def nueva_Cua(master):
    VNuevaPub(master, master)


def mostrar_Cuas(master):
    # Lógica para mostrar solo las publicaciones del usuario que inició sesión
    cursor = master.conexion.cursor()
    query = "SELECT id, texto, imagen FROM publicaciones WHERE id_usuario = %s ORDER BY fecha_hora DESC"
    cursor.execute(query, (master.id_usuario,))
    publicaciones = cursor.fetchall()
    cursor.close()

    # Abrir una nueva ventana para mostrar las publicaciones del usuario
    ventana_publicaciones = tk.Toplevel(master)
    ventana_publicaciones.title("Mis Publicaciones")

    # Crear un frame principal
    main_frame = tk.Frame(ventana_publicaciones)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Texto "VMisPub" en negrita y centrado
    vmispub_label = tk.Label(main_frame, text="VMisPub", font=("Arial", 12, "bold"), pady=10)
    vmispub_label.pack(fill=tk.X, anchor=tk.CENTER)

    canvas = tk.Canvas(main_frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Frame para contener las publicaciones
    publicaciones_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=publicaciones_frame, anchor="nw")

    for publicacion in publicaciones:
        id_publicacion, texto_publicacion, imagen_path = publicacion

        # Crear un recuadro para cada publicación
        recuadro = tk.Frame(publicaciones_frame, relief=tk.RIDGE, borderwidth=2)
        recuadro.pack(padx=10, pady=5, fill=tk.X)

        # Agregar el texto de la publicación al recuadro
        publicacion_label = tk.Label(recuadro, text=texto_publicacion)
        publicacion_label.pack(padx=10, pady=5)

        # Label para la imagen
        imagen_label = tk.Label(recuadro)
        imagen_label.pack(padx=10, pady=5)

        if imagen_path:  # Si hay una ruta de imagen
            imagen = tk.PhotoImage(file=imagen_path)
            imagen = imagen.subsample(4, 4)  # Cambia los factores según sea necesario
            imagen_label.config(image=imagen)
            imagen_label.image = imagen  # Esto evita que la imagen sea recolectada por el recolector de basura de Python

        # Agregar botones de editar y borrar
        editar_button = tk.Button(recuadro, text="Editar", command=lambda id_publicacion=id_publicacion, texto_publicacion=texto_publicacion: editar_Cuas(master, id_publicacion, texto_publicacion, ventana_publicaciones))
        editar_button.pack(side=tk.LEFT, padx=5)
        borrar_button = tk.Button(recuadro, text="Borrar", command=lambda id_publicacion=id_publicacion, texto_publicacion=texto_publicacion: borrar_Cuas(master, id_publicacion, ventana_publicaciones, texto_publicacion))
        borrar_button.pack(side=tk.LEFT, padx=5)


