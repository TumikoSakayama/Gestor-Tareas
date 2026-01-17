import os
import json
from datetime import date, timedelta
import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel, Listbox, Scrollbar
import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

TASK_FILES = "tareas.json"
tareas = []
contador_id = 0
hoy = date.today()

def cargar_tareas():
    global tareas, contador_id
    if os.path.exists(TASK_FILES):
        try:
            with open(TASK_FILES, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)

                if isinstance(datos, list):
                    viejas_tareas = datos
                    contador_id = max((tarea["id"] for tarea in tareas), default=0)
                    print("Se detecto formato antiguo. Migrando....")
                else:
                    viejas_tareas = datos.get("tareas", [])
                    contador_id = datos.get("ultimo_id", 0)

                migrado = False
                for tarea in tareas:
                    if "finalizar" not in tarea:
                        tarea["finalizar"] = str(date.today())
                        migrado = True
                    
                if migrado:
                    guardar_tareas()

        except Exception as e:
            messagebox.showerror("Error de Carga", f"No se pudo cargar el archivo: {e}")
    else:
        tareas = []
        contador_id = 0


def guardar_tareas():
    try:
        with open(TASK_FILES, 'w', encoding='utf-8') as archivo:
            datos_a_guardar = {
                "ultimo_id": ultimo_id,
                "tareas": tareas
            }
            json.dump(datos_a_guardar, archivo, indent=4, ensure_ascii=False)
            print("Tareas guardadas correctamente")
    except Exception as e:
        messagebox.showerror("Error al guardar", f"No se pudo guardar la tarea ingresada en el archivo: {e}")

def agregar_tarea(descripcion, prioridad='Media', categoria="Sin Especificar"):
    global contador_id

    descripcion = simpledialog.askstring("Nueva Tarea", "Descripcion de la tarea: ")
    if not descripcion:
        return
    prioridad = simpledialog.askstring("Prioridad", "Prioridad (Alta/Media/Baja)") or "Media"
    prioridad = prioridad.capitalize()
    categoria = simpledialog.askstring("Categoria", "Categoria: ") or "Sin Especificar"

    contador_id += 1

    dias_limites = {
        "Alta": 1,
        "Media": 5,
        "Baja": 10
    }

    dias_completar = dias_limites.get(prioridad, 2)
    fecha_limite = hoy + timedelta(days=dias_completar)

    nueva_tarea = {
        "id": contador_id,
        "descripcion": descripcion,
        "prioridad": prioridad,
        "categorias": categoria.capitalize(),
        "completado": False,
        "fecha": str(date.today()),
        "finalizar": str(fecha_limite)
    }

    tareas.append(nueva_tarea)
    guardar_tareas()
    actualizar_lista()
    messagebox.showinfo("Exito", f"Tarea #{contador_id} agregada correctamente!")


def mostrar_tareas(mostrar_completadas = False):
    global hoy
    if not tareas:
        print("No hay tareas en la lista")
        return

    print("=====LISTA DE TAREAS=====")
    for tarea in tareas:
        if not tarea["completado"] or mostrar_completadas:
            limite = date.fromisoformat(tarea["finalizar"])
            vencida = "! TAREA VENCIDA " if limite < hoy and not tarea["completado"] else ""
            estado = "✓" if tarea["completado"] else " "
            print(f"[{estado}] {tarea['id']}. {tarea['descripcion']} (Prioridad: {tarea['prioridad']}) de {tarea['categorias']}| Vence: {tarea["finalizar"]} {vencida}")
    print("========================")

def marcar_completada(id_tarea):
    for tarea in tareas:
        if tarea['id'] == id_tarea:
            tarea['completado'] = True
            print(f"Tarea {tarea['descripcion']} marcada como completa")
            guardar_tareas()
            return
    print(f"No se econtro ninguna tarea con {id_tarea}.")

def filtrar(valor, campo="categorias"):
    encontradas = False
    print(f"\n---Tareas filtradas por {campo}: {valor}---")
    for tarea in tareas:
        if tarea.get(campo) == valor:
            estado = "✓" if tarea["completado"] else " "
            print(f"[{estado}] {tarea['id']}. {tarea['descripcion']} (Prioridad: {tarea['prioridad']}) de {tarea['categorias']}| Vence: {tarea["finalizar"]}")
            encontradas = True
        
    if not encontradas:
        print(f"No se encontraron tareas con {campo} = '{valor}'")
    print("=========================")

def eliminar_tarea(id_tarea):
    global tareas
    tareas_filtrada = [tarea for tarea in tareas if tarea['id'] != id_tarea]
    
    if len(tareas_filtrada) < len(tareas):
        tareas = tareas_filtrada
        print(f"Tarea con ID {id_tarea} eliminada")
        guardar_tareas()
    else:
        print(f"No se encontro ninguna tarea con ID {id_tarea}")

def busqueda_tarea(palabra_clave):
    existe = False
    busqueda = palabra_clave.lower()
    print(f"\n----Tareas econtradas con: {palabra_clave}---")

    for tarea in tareas:
        if busqueda in tarea["descripcion"].lower():
            existe = True
            estado = "✓" if tarea["completado"] else " "
            print(f"[{estado}] {tarea['id']}. {tarea['descripcion']} | Prioridad: {tarea['prioridad']} de {tarea['categorias']}")
        
    if not existe:
        print("No hay tareas con ese termino de busqueda :(")
    print("=========================")


def ventana_agregar():
    descripcion = simpledialog.askstring("Nueva Tarea", "Escribe la descripción:")
    if descripcion:
        prioridad = simpledialog.askstring("Entrada", "Prioridad (Baja/Media/Alta):") or "Media"
        categoria = simpledialog.askstring("Entrada", "Categoria: ") or "Sin Especificar"
        agregar_tarea(descripcion, prioridad.capitalize(), categoria.capitalize())


def menu_principal():
    root = tk.Tk()
    root.title("Gestor de Tareas")
    ancho_ventana = 400
    alto_ventana = 620
    root.update_idletasks()

    ancho_pantalla = root.winfo_screenwidth()
    alto_pantalla = root.winfo_screenheight()

    posicion_x = int((ancho_ventana//2) + (ancho_pantalla//2))
    posicion_y = int((alto_ventana//2) + (alto_pantalla//2))
    posicion_y -= 720
    posicion_x -= 400

    root.geometry(f"{ancho_ventana}x{alto_ventana}+{posicion_x}+{posicion_y}")

    root.configure(bg="#1a1a1a")
    ventana_principal = tk.Frame(root, bg="#1a1a1a")
    ventana_principal.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    tk.Label(ventana_principal, text="GESTOR DE TAREAS", fg="white", bg="#1a1a1a", font=("Arial", 16, "bold")).pack(pady=20)
    tk.Button(ventana_principal, text="1. Agregar tarea", width=25, command=ventana_agregar).pack(pady=20)
    tk.Button(ventana_principal, text="2. Mostrar pendientes", width=25, command=lambda: mostrar_tareas(False)).pack(pady=20)
    tk.Button(ventana_principal, text="3. Mostrar todas", width=25, command=lambda: mostrar_tareas(True)).pack(pady=20)
    tk.Button(ventana_principal, text="4. Filtrar tareas", width=25, command=filtrar).pack(pady=20)
    tk.Button(ventana_principal, text="5. Marcar completada", width=25, command=marcar_completada).pack(pady=20)
    tk.Button(ventana_principal, text="6. Eliminar tarea", width=25, command=eliminar_tarea).pack(pady=20)
    tk.Button(ventana_principal, text="7. Búsqueda personalizada", width=25, command=busqueda_tarea).pack(pady=20)
    tk.Button(ventana_principal, text="8. Salir", width=25, command=root.quit, bg="red", fg="white").pack(pady=40)

    root.mainloop()

if __name__ == "__main__":
    print("Bienvenido al Gestor de tareas")
    cargar_tareas()
    menu_principal()  
