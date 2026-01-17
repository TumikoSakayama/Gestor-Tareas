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

def agregar_tarea():
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

def marcar_completada():
    seleccion = lista_tareas.curseselection()
    if not seleccion:
        messagebox.showwarning("Atencion", "Seleccione una tarea de la lista, el valor seleccionado no existe!")
        return

    texto = lista_tareas.get(seleccion[0])
    id_tarea = int(texto.split(".")[0])
    for tarea in tareas:
        if tarea['id'] == id_tarea:
            tarea['completado'] = True
            guardar_tareas()
            actualizar_lista()
            messagebox.showinfo("Hecho", "La tarea se ha marcado como completa")
            return

def eliminar_tarea():
    global tareas
    seleccion = lisat_tareas.curseselection()
    if not seleccion:
        messagebox.showwarning("Atencion", "Seleccione una tarea para eliminar (Este cambio no se puede restaurar)")
        return
    
    texto = lista_tareas.get(seleccion[0])
    id_tarea = int(texto.split(".")[0])

    if messagebox.askyesno("Confirmar", f"Procederemos a eliminar la tarea {id_tarea}"):
        tareas_filtrada = [tarea for tarea in tareas if tarea['id'] != id_tarea]
        guardar_tareas()
        actualizar_lista()

def busqueda_tarea():
    valor_busqueda = simpledialog.askstring("Buscar", "Ingrese la palabra clave:")
    if valor_busqueda:
        actualizar_lista(filtro_busqueda=valor_busqueda..lower())


def filtrar_categoria():
    categoria = simpledialog.askstring("Filtrar", "Escribe la categoria a filtrar:")
    if categoria:
        actualizar_lista(filtro_categoria=categoria.capitalize())

def actualizar_lista(mostrar_tareas=True, filtro_busqueda=None, filtrar_categoria=None):
    lista_tareas.delete(0,tk.END)
    for tarea in tareas:
        if not mostrar_tareas and tarea["compleatdo"]:
            continue
        if filtro_busqueda and filtro_busqueda not in tarea["descripcion"].lower():
            continue
        if filtrar_categoria and filtrar_categoria != tarea["categorias"]:
            continue

        limite = date.fromisoformat(tarea["finalizar"])
        vencida = "⚠️ Vencida :(" if limite < hoy and not tarea["completado"] else ""
        estado = "✅" if tarea["completado"] else "⏳"

        linea = f"{tarea["id"]}, {estado} {tarea[descripcion]} [{tarea["prioridad"]}] - {tarea[categorias]} | Vence {tarea["finalizar"]} {vencida}"
        lista_tareas.insert(tk.END, linea)

        if vencida:
            lista_tareas.itemconfig(tk.END, {'fg': 'red'})
        elif tarea["completado"]:
            lista_tareas.itemconfig(tk.END, {'fg': 'gray'})

def menu_principal():
    global lista_tareas
    root = tk.Tk()
    root.title("Gestor de Tareas")
    root.geometry("700x550")
    root.configure(bg="#2c3e50")

    style = {"font": ("Arial", 10, "bold"), "bg": "#34495e", "fg": "white", "relief": "flat", "padx": 10, "pady": 5}

    principal = tk.Frame(root, bg="#1a252f", pady=10)
    principal.pack(fill="x")
    tk.Label(principal, text="MIS TAREAS", font=("Arial", 18, "bold"), bg="#1a252f", fg="#ecf0f1").pack()


    menu_lateral = tk.Frame(root, bg="#2c3e50", padx=10, pady=10)
    menu_lateral.pack(side="left", fill="y")

    tk.Button(ventana_principal, text="➕ Agregar tarea", width=25, command=ventana_agregar).pack(pady=20)
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
