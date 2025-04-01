# LockApp

LockApp es una aplicación de bloqueo desarrollada en Python que muestra una ventana de bloqueo en pantalla completa en todos los monitores del sistema. La aplicación captura eventos de teclado y mouse para solicitar una contraseña (por defecto "1234"). Si se ingresa la contraseña correcta, las ventanas se ocultan, permitiendo el acceso. Además, la aplicación verifica la inactividad y, si no hay actividad durante el tiempo preestablecido (por defecto 1 minuto), vuelve a bloquear el sistema y fuerza la solicitud de contraseña nuevamente. Tras 3 intentos fallidos, se envía un correo electrónico al propietario mediante Outlook.

## Características

- **Bloqueo en múltiples monitores:** La aplicación detecta todos los monitores conectados y muestra una ventana de bloqueo en cada uno.
- **Solicitud de contraseña:** Se solicita la contraseña para desbloquear el sistema.
- **Verificación de inactividad:** Si no hay actividad durante el tiempo configurado (MINUTOS), el sistema se re-bloquea automáticamente.
- **Notificación por correo:** Tras 3 intentos fallidos de ingreso, se envía un correo electrónico al propietario utilizando la configuración de Outlook del sistema.
- **Ligera:** Utiliza el bucle de eventos de Tkinter y la función `after()`, lo que minimiza el consumo de CPU y memoria.

## Requisitos

- Python 3.x
- [screeninfo](https://pypi.org/project/screeninfo/)
- [pywin32](https://pypi.org/project/pywin32/)

## Instalación

1. Clona este repositorio o descarga el código fuente.

2. Instala los paquetes necesarios usando pip. Asegúrate de tener un entorno virtual activo (opcional):

   ```bash
   pip install -r requirements.txt

## Publicación

1. Instala PyInstaller:
   ```bash
   pip install pyinstaller

2. Genera el ejecutable:
   ```bash
   pyinstaller --onefile --windowed index.py

* onefile: Empaqueta todo en un solo archivo ejecutable.
* windowed: Evita que se abra la consola al iniciar la aplicación (útil para aplicaciones gráficaas)
