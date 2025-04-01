import tkinter as tk
from tkinter import simpledialog
from screeninfo import get_monitors

try:
    import win32com.client as win32
except ImportError:
    win32 = None
    print("La librería win32com no está instalada. No se podrá enviar correo.")

PASSWORD = "1234"
dialog_active = False
windows = []
attempts_fallidos = 0


def enviar_correo():
    """Envía un correo al propietario usando Outlook, obteniendo la cuenta emisora automáticamente."""
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

        # Configura la dirección de correo receptor
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
        for window in windows:
            try:
                window.unbind_all("<Key>")
                window.unbind_all("<Button>")
            except Exception as e:
                print(f"Error al desvincular eventos en una ventana: {e}")

        pwd = simpledialog.askstring("Desbloqueo", "Ubicación de las esferas:", show="*", parent=windows[0])

        if pwd == PASSWORD:
            for window in windows:
                try:
                    window.destroy()
                except Exception as e:
                    print(f"Error al destruir una ventana: {e}")
        else:
            attempts_fallidos += 1
            print(f"Intento fallido {attempts_fallidos}")
            if attempts_fallidos >= 3:
                enviar_correo()
                attempts_fallidos = 0

            for window in windows:
                try:
                    set_global_bindings(window)
                except Exception as e:
                    print(f"Error al reestablecer bindings en una ventana: {e}")
    except Exception as e:
        print(f"Error en solicitar_contrasena: {e}")
    finally:
        dialog_active = False


def on_event(event):
    """Se llama ante cualquier clic o pulsación de tecla.
       Muestra el diálogo de contraseña si no está ya activo."""
    global dialog_active
    try:
        if not dialog_active:
            dialog_active = True
            event.widget.after(100, solicitar_contrasena)
    except Exception as e:
        print(f"Error en on_event: {e}")
    return "break"


def set_global_bindings(window):
    """Vincula eventos globales de teclado y mouse para bloquear la interacción."""
    try:
        window.bind_all("<Key>", on_event)
        window.bind_all("<Button>", on_event)
    except Exception as e:
        print(f"Error en set_global_bindings: {e}")


def bloquear_pantalla():
    global windows
    try:
        monitors = get_monitors()

        root = tk.Tk()
        windows.append(root)

        for i, monitor in enumerate(monitors):
            try:
                # Para el primer monitor usamos la ventana root,
                # para los demás creamos ventanas hijas Toplevel
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

                etiqueta = tk.Label(frame, text="En pausa",
                                    fg="white", bg="black", font=("Arial", 24))
                etiqueta.pack(expand=True, fill="both")

                set_global_bindings(win)
            except Exception as inner_e:
                print(f"Error configurando la ventana para el monitor {i}: {inner_e}")

        root.mainloop()
    except Exception as e:
        print(f"Error en bloquear_pantalla: {e}")


if __name__ == "__main__":
    try:
        bloquear_pantalla()
        print("Sistema desbloqueado.")
    except Exception as e:
        print(f"Error en el programa principal: {e}")
