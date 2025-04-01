import tkinter as tk
from tkinter import simpledialog, messagebox
from screeninfo import get_monitors
import time

try:
    import win32com.client as win32
except ImportError:
    win32 = None
    print("La librería win32com no está instalada. No se podrá enviar correo.")

PASSWORD = "1234"
MINUTOS = 1
dialog_active = False
windows = []
attempts_fallidos = 0

last_activity = time.time()

def update_last_activity():
    """Actualiza la marca de tiempo de la última actividad."""
    global last_activity
    try:
        last_activity = time.time()
    except Exception as e:
        print("Error en update_last_activity:", e)

def check_inactivity():
    """Chequea cada segundo si ha pasado el tiempo de inactividad.
       Si es así, vuelve a mostrar las ventanas y fuerza la solicitud de contraseña."""
    global last_activity
    try:
        if time.time() - last_activity >= MINUTOS * 60:
            activar_funcion_inactividad()
            update_last_activity()
    except Exception as e:
        print("Error en check_inactivity:", e)
    try:
        root.after(1000, check_inactivity)
    except Exception as e:
        print("Error al programar check_inactivity:", e)

def activar_funcion_inactividad():
    """Función que se activa tras MINUTOS de inactividad.
       Vuelve a mostrar las ventanas (re-bloquea el sistema) y solicita la contraseña."""
    try:
        print("¡Se activó la función por inactividad!")
        for win in windows:
            try:
                if win.state() == 'withdrawn':
                    win.deiconify()
            except Exception as e:
                print("Error al deiconificar una ventana:", e)
        # messagebox.showinfo("Inactividad", f"Han pasado {MINUTOS} minutos sin actividad. El sistema se bloqueará nuevamente.")
        root.after(100, solicitar_contrasena)
    except Exception as e:
        print("Error en activar_funcion_inactividad:", e)

def enviar_correo():
    """Envía un correo al propietario usando Outlook."""
    try:
        if win32 is None:
            print("No se puede enviar correo: win32com no está disponible.")
            return
        outlook = win32.Dispatch('outlook.application')
        session = outlook.Session
        mail = outlook.CreateItem(0)
        if session.Accounts.Count > 0:
            cuenta_emisora = session.Accounts.Item(1)
            mail.SendUsingAccount = cuenta_emisora
            print(f"Usando la cuenta emisora: {cuenta_emisora.SmtpAddress}")
        else:
            print("No se encontró ninguna cuenta en Outlook, se usará la cuenta predeterminada.")
        mail.To = "compania@gmail.com"
        mail.Subject = "Alerta: 3 intentos fallidos de desbloqueo"
        mail.Body = "Se han registrado 3 intentos fallidos de desbloqueo en el sistema."
        mail.Send()
        print("Correo enviado al propietario.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

def solicitar_contrasena():
    global dialog_active, attempts_fallidos
    try:
        for win in windows:
            try:
                win.unbind_all("<Key>")
                win.unbind_all("<Button>")
            except Exception as e:
                print("Error al desvincular eventos en una ventana:", e)
        pwd = simpledialog.askstring("Desbloqueo", "Ubicación de las esferas:", show="*", parent=windows[0])
        if pwd == PASSWORD:
            for win in windows:
                try:
                    win.withdraw()
                except Exception as e:
                    print("Error al ocultar una ventana:", e)
        else:
            attempts_fallidos += 1
            print(f"Intento fallido {attempts_fallidos}")
            if attempts_fallidos >= 3:
                enviar_correo()
                attempts_fallidos = 0
            for win in windows:
                try:
                    set_global_bindings(win)
                except Exception as e:
                    print("Error al reestablecer bindings en una ventana:", e)
    except Exception as e:
        print("Error en solicitar_contrasena:", e)
    finally:
        dialog_active = False
        update_last_activity()

def on_event(event):
    """Se llama ante cualquier clic o pulsación de tecla.
       Actualiza la actividad y, si no hay diálogo activo, solicita la contraseña."""
    global dialog_active
    try:
        update_last_activity()
        if not dialog_active:
            dialog_active = True
            event.widget.after(100, solicitar_contrasena)
    except Exception as e:
        print("Error en on_event:", e)
    return "break"

def set_global_bindings(win):
    """Vincula eventos globales de teclado y mouse para la ventana."""
    try:
        win.bind_all("<Key>", on_event)
        win.bind_all("<Button>", on_event)
    except Exception as e:
        print("Error en set_global_bindings:", e)

def bloquear_pantalla():
    global windows, root
    try:
        monitors = get_monitors()
    except Exception as e:
        print("Error al obtener monitores:", e)
        return

    try:
        root = tk.Tk()
        windows.append(root)
    except Exception as e:
        print("Error al crear la ventana raíz:", e)
        return

    for i, monitor in enumerate(monitors):
        try:
            if i == 0:
                win = root
            else:
                win = tk.Toplevel(root)
                windows.append(win)
            win.title("Pantalla bloqueada")
            win.overrideredirect(True)
            win.attributes("-topmost", True)
            geom = f"{monitor.width}x{monitor.height}+{monitor.x}+{monitor.y}"
            win.geometry(geom)
            win.attributes("-alpha", 0.1)
            frame = tk.Frame(win, bg="black")
            frame.pack(expand=True, fill="both")
            etiqueta = tk.Label(frame, text="En pausa", fg="white", bg="black", font=("Arial", 24))
            etiqueta.pack(expand=True, fill="both")
            set_global_bindings(win)
        except Exception as inner_e:
            print(f"Error configurando la ventana para el monitor {i}:", inner_e)
    try:
        root.after(1000, check_inactivity)
        root.mainloop()
    except Exception as e:
        print("Error en el mainloop:", e)


if __name__ == "__main__":
    try:
        bloquear_pantalla()
        print("Sistema desbloqueado.")
    except KeyboardInterrupt:
        print("Aplicación finalizada por el usuario.")
    except Exception as e:
        print("Error en el programa principal:", e)
