import tkinter as tk
from tkinter import ttk
import mysql.connector
from ventana_VMenu import nueva_Cua, mostrar_Cuas
import ConexionSingleton


class VPub(tk.Toplevel):
    def __init__(self, master, conexion, id_usuario):
        super().__init__(master)
        self.title("Ventana Principal de Publicaciones")

        self.conexion = conexion
        self.id_usuario = id_usuario
        
        self.observadores = []  # Lista para almacenar los observadores

        # Crear un frame principal
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Texto "VPub" en negrita
        vpub_label = tk.Label(main_frame, text="VPub", font=("Arial", 12, "bold"))
        vpub_label.pack(pady=(10, 0))  # Agrega un espacio en la parte superior

        # Recuadro adicional con texto y botones
        menu_frame = tk.Frame(main_frame, relief=tk.RIDGE, borderwidth=10)
        menu_frame.pack(side=tk.TOP, fill=tk.Y, pady=5)

        vmenu_label = tk.Label(menu_frame, text="VMenu")
        vmenu_label.pack(side=tk.LEFT, padx=5)

        publicar_button = tk.Button(menu_frame, text="Publicar", command=lambda: nueva_Cua(self))
        publicar_button.pack(side=tk.LEFT, padx=5)

        mostrar_button = tk.Button(menu_frame, text="Mostrar", command=lambda: mostrar_Cuas(self))
        mostrar_button.pack(side=tk.LEFT, padx=5)

        # Crear un canvas con un scrollbar vertical
        self.canvas = tk.Canvas(main_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Frame para contener las publicaciones
        self.publicaciones_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.publicaciones_frame, anchor="nw")

        self.cargar_Cuas()

     # Parte del código que implementa el patrón observador
    def registrar_observador(self, observador):
        self.observadores.append(observador)

    def notificar_observadores(self):
        for observador in self.observadores:
            observador.actualizar()

    def cargar_Cuas(self):
        cursor = self.conexion.cursor()
        query = "SELECT usuarios.usuario, publicaciones.texto, publicaciones.fecha_hora, publicaciones.imagen FROM publicaciones JOIN usuarios ON publicaciones.id_usuario = usuarios.id ORDER BY publicaciones.fecha_hora DESC"
        cursor.execute(query)
        publicaciones = cursor.fetchall()
        cursor.close()

        for publicacion in publicaciones:
            nombre_usuario, texto, fecha_hora, imagen = publicacion
            texto_publicacion = f"{nombre_usuario} publico:\n {texto}\n Fecha: {fecha_hora}"

            # Frame para contener la publicación
            publicacion_frame = ttk.Frame(self.publicaciones_frame, relief=tk.RIDGE, borderwidth=2)
            publicacion_frame.pack(padx=10, pady=5, fill=tk.X)

            # Label para texto de la publicacion
            publicacion_label = tk.Label(publicacion_frame, text=texto_publicacion)
            publicacion_label.pack(padx=10, pady=5)

            imagen_path = publicacion[3]  # La cuarta columna es la de la imagen
            if imagen_path:  # Si hay una ruta de imagen
                imagen_label = tk.Label(publicacion_frame)
                imagen_label.pack(padx=10, pady=5)

                imagen = tk.PhotoImage(file=imagen_path)
                imagen = imagen.subsample(3, 3)  # Cambia los factores según sea necesario
                imagen_label.config(image=imagen)
                imagen_label.image = imagen  # Esto evita que la imagen sea recolectada por el recolector de basura de Python

            agrandar_button = tk.Button(publicacion_frame, text="Agrandar", command=lambda texto=texto_publicacion, imagen=imagen_path: self.agrandar_Cuas(texto,imagen))
            agrandar_button.pack()

            self.notificar_observadores()

    def agrandar_Cuas(self, contenido_publicacion, imagen_path):
        VPubDetalle(self, contenido_publicacion, imagen_path)


class VPubDetalle(tk.Toplevel):
    def __init__(self, master, contenido, imagen_path):
        super().__init__(master)
        self.title("Detalle de Publicación")
        self.contenido = contenido
        self.imagen_path = imagen_path

        # Obtener las dimensiones de la pantalla
        ancho_pantalla = self.winfo_screenwidth()
        altura_pantalla = self.winfo_screenheight()

        # Establecer las dimensiones de la ventana
        self.geometry(f"{ancho_pantalla}x{altura_pantalla}")

        # Crear widgets y diseño de la ventana
        self.detalle_label = tk.Label(self, text=self.contenido, font=("Arial", 16))
        self.detalle_label.pack(padx=10, pady=10)

        if self.imagen_path:  # Si hay una ruta de imagen
            self.imagen_label = tk.Label(self)
            self.imagen_label.pack(padx=10, pady=5)

            imagen = tk.PhotoImage(file=self.imagen_path)
            self.imagen_label.config(image=imagen)
            self.imagen_label.image = imagen  # Esto evita que la imagen sea recolectada por el recolector de basura de Python

#
    def actualizar(self, nuevo_contenido, nueva_imagen_path):
        # Método para actualizar el contenido del detalle de la publicación
        # Aquí puedes actualizar el contenido de la ventana en función de los cambios en las publicaciones
        self.contenido = nuevo_contenido
        self.imagen_path = nueva_imagen_path

        # Actualizar widgets en la ventana
        self.detalle_label.config(text=self.contenido)

        if self.imagen_path:  # Si hay una ruta de imagen
            imagen = tk.PhotoImage(file=self.imagen_path)
            self.imagen_label.config(image=imagen)
            self.imagen_label.image = imagen  # Esto evita que la imagen sea recolectada por el recolector de basura de Python


""""
if __name__ == "__main__":
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="micro_x"
    )

    root = tk.Tk()
    VPub(root, conexion, None)
    root.mainloop()
"""
if __name__ == "__main__":
    conexion = ConexionSingleton()  # En lugar de mysql.connector.connect(...)
    root = tk.Tk()
    VPub(root, conexion, None)
    root.mainloop()

# La clase VPub es la que actúa como el sujeto que será observado xD 
# y notificará a los observadores (VPubDetalle) cada vez que se carguen
# nuevas publicaciones. 
# Las instancias de VPubDetalle pueden registrarse como observadores de VPub 
# utilizando el método registrar_observador(). 
# Cuando se notifiquen cambios en VPub, los observadores actualizarán automáticamente 
# su contenido utilizando el método actualizar().