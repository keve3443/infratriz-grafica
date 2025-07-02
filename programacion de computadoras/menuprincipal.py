import tkinter as tk
from PIL import Image, ImageTk

# ventana principal
root = tk.Tk()
root.title("AGRO.MAX")
root.geometry("400x600")
root.configure(bg="white")

# contenedores
main_frame = tk.Frame(root, bg="white")
main_frame.pack(fill="both", expand=True)

bottom_nav = tk.Frame(root, bg="white", height=60, bd=1, relief="raised")
bottom_nav.pack(side="bottom", fill="x")

# funciones para cargar imágenes
def load_icon(path, size=(30, 30)):
    try:
        image = Image.open(path)
        image = image.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(image)
    except Exception as e:
        print(f"Error al cargar el ícono '{path}': {e}")
        return None

def load_product_image(path, size=(80, 80)):
    try:
        image = Image.open(path)
        image = image.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(image)
    except Exception as e:
        print(f"Error al cargar imagen de producto '{path}': {e}")
        return None

# íconos
icon_inicio = load_icon("inicio.png")
icon_categorias = load_icon("lupa.png")
icon_tu = load_icon("usuario.png")
icon_carrito = load_icon("carrito.png")

# datos
productos_disponibles = [
    {"nombre": "Comida para Gatos", "precio": "15000", "imagen": "ringogato.png"},
    {"nombre": "Comida para Perro", "precio": "25000", "imagen": "perro.png"},
    {"nombre": "Comida para Gatos pequeños", "precio": "10000", "imagen": "gato_pequeño.png"},
    {"nombre": "Comida para Cachorros", "precio": "20000", "imagen": "perros_pequeños.png"},
]
carrito = []

# estilo de botones
button_style = {"bd": 0, "bg": "white", "activebackground": "white", "fg": "black"}

# funciones generales
def set_active(btn):
    for b in [btn_inicio, btn_categorias, btn_tu, btn_carrito]:
        b.config(bg="white", fg="black")
    btn.config(bg="#e0f7fa", fg="green")

def limpiar_contenido():
    for widget in main_frame.winfo_children():
        widget.destroy()

# mostrar producto
def add_product_to_catalog(parent_frame, image_path, name, price, product_dict=None, en_carrito=False):
    frame = tk.Frame(parent_frame, bg="white", bd=1, relief="solid", padx=10, pady=10)
    frame.pack(pady=5, padx=10, fill="x")

    img = load_product_image(image_path)
    if img:
        img_label = tk.Label(frame, image=img, bg="white")
        img_label.image = img
        img_label.pack(side="left", padx=5)

    info_frame = tk.Frame(frame, bg="white")
    info_frame.pack(side="left", padx=10, fill="both", expand=True)

    tk.Label(info_frame, text=name, font=("Arial", 12, "bold"), bg="white").pack(anchor="w")
    tk.Label(info_frame, text=f"Precio: ${price}", font=("Arial", 10), fg="green", bg="white").pack(anchor="w")

    if en_carrito:
        def eliminar():
            carrito.remove(product_dict)
            go_carrito()
        tk.Button(info_frame, text="Eliminar", command=eliminar, bg="#ffcdd2", fg="black").pack(anchor="e", pady=5)
    else:
        def comprar():
            carrito.append(product_dict or {"nombre": name, "precio": price, "imagen": image_path})
            print(f"{name} agregado al carrito.")
        tk.Button(info_frame, text="Comprar", command=comprar, bg="#c8e6c9", fg="black").pack(anchor="e", pady=5)

# mostrar catálogo
def mostrar_catalogo(filtrados=None):
    limpiar_contenido()
    lista = filtrados if filtrados is not None else productos_disponibles

    if not lista:
        tk.Label(main_frame, text="No se encontraron productos.", bg="white", font=("Arial", 12)).pack(pady=20)
    else:
        for prod in lista:
            add_product_to_catalog(main_frame, prod["imagen"], prod["nombre"], prod["precio"], product_dict=prod)

# navegación
def go_inicio():
    set_active(btn_inicio)
    mostrar_catalogo()

def go_categorias():
    set_active(btn_categorias)
    limpiar_contenido()

    tk.Label(main_frame, text="Buscar productos:", font=("Arial", 12), bg="white").pack(pady=10)

    search_var = tk.StringVar()
    entry = tk.Entry(main_frame, textvariable=search_var, font=("Arial", 12), width=30)
    entry.pack(pady=5)

    def realizar_busqueda():
        texto = search_var.get().strip().lower()
        resultados = [p for p in productos_disponibles if texto in p["nombre"].lower()]
        mostrar_catalogo(resultados)

    tk.Button(main_frame, text="Buscar", command=realizar_busqueda, bg="#c8e6c9").pack(pady=5)

def go_tu():
    set_active(btn_tu)
    limpiar_contenido()

    tk.Label(main_frame, text="Perfil de Usuario", font=("Arial", 16, "bold"), bg="white").pack(pady=10)
    tk.Label(main_frame, text="Nombre: Kevin Garcia", font=("Arial", 12), bg="white").pack(pady=2)
    tk.Label(main_frame, text="Correo: kevin@gmail.com", font=("Arial", 12), bg="white").pack(pady=2)

    def editar_usuario():
        tk.messagebox.showinfo("Editar", "Funcionalidad para editar perfil aún no implementada.")

    tk.Button(main_frame, text="Editar perfil", command=editar_usuario,
              bg="#bbdefb", fg="black", font=("Arial", 11)).pack(pady=10)

    def cerrar_sesion():
        tk.messagebox.showinfo("Sesión cerrada", "Has cerrado sesión.")
        go_inicio()

    tk.Button(main_frame, text="Cerrar sesión", command=cerrar_sesion,
              bg="#ef9a9a", fg="black", font=("Arial", 11)).pack()

def go_carrito():
    set_active(btn_carrito)
    limpiar_contenido()

    if not carrito:
        tk.Label(main_frame, text="Tu carrito está vacío.", font=("Arial", 12), bg="white").pack(pady=20)
    else:
        tk.Label(main_frame, text="Productos en tu carrito:", font=("Arial", 12, "bold"), bg="white").pack(pady=10)

        total = 0
        for producto in carrito:
            add_product_to_catalog(main_frame, producto["imagen"], producto["nombre"], producto["precio"], product_dict=producto, en_carrito=True)
            total += int(producto["precio"])

        tk.Label(main_frame, text=f"Total: ${total}", font=("Arial", 12, "bold"), fg="blue", bg="white").pack(pady=10)

        def pagar():
            carrito.clear()
            go_carrito()
            tk.messagebox.showinfo("Pago realizado", "Gracias por tu compra.")

        tk.Button(main_frame, text="Pagar", command=pagar, bg="#a5d6a7", font=("Arial", 11)).pack(pady=5)

# botones de navegación
btn_inicio = tk.Button(bottom_nav, image=icon_inicio, text="Inicio", compound="top", command=go_inicio, **button_style)
btn_inicio.pack(side="left", expand=True)

btn_categorias = tk.Button(bottom_nav, image=icon_categorias, text="Buscar", compound="top", command=go_categorias, **button_style)
btn_categorias.pack(side="left", expand=True)

btn_tu = tk.Button(bottom_nav, image=icon_tu, text="Usuario", compound="top", command=go_tu, **button_style)
btn_tu.pack(side="left", expand=True)

btn_carrito = tk.Button(bottom_nav, image=icon_carrito, text="Carrito", compound="top", command=go_carrito, **button_style)
btn_carrito.pack(side="left", expand=True)

# iniciar app
set_active(btn_inicio)
mostrar_catalogo()
root.mainloop()
