import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Importación de las funciones del agente y utilidades
from funciones_agente.obtener_clima import obtener_clima
from funciones_agente.obtener_precio_accion import obtener_precio_accion
from utils.sanitizar import sanitizar

# --- Configuración de Selenium ---
# Se utilizan opciones para ejecutar el navegador de forma silenciosa (headless)
options = Options()
#options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
# Simulación de un User-Agent real para evitar bloqueos por parte de algunos sitios
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.add_argument('--disable-blink-features=AutomationControlled')

# --- Gestión del Driver (ChromeDriver) ---
# Se utiliza webdriver-manager para descargar automáticamente el driver compatible
driver_path = ChromeDriverManager().install()

# Corrección de ruta: Algunos sistemas devuelven la ruta de un archivo de licencia en lugar del binario
if os.path.basename(driver_path) != "chromedriver":
    dir_path = os.path.dirname(driver_path)
    binary_path = os.path.join(dir_path, "chromedriver")
    if os.path.exists(binary_path):
        driver_path = binary_path

# Asegurar que el archivo tenga permisos de ejecución (importante en sistemas Mac/Linux)
os.chmod(driver_path, 0o755)

# Inicialización del navegador Chrome con las opciones configuradas
driver = webdriver.Chrome(service=Service(driver_path), options=options)

def procesar_input(user_input):
    """
    Determina la intención del usuario analizando palabras clave en el input original.
    
    Esta función es el 'ruteador' del agente. Si encuentra palabras relacionadas con
    clima o acciones, devuelve la referencia a la función que debe ejecutarse.
    
    Retorna:
        function o None: La función del agente correspondiente o None si no se reconoce.
    """
    user_input = user_input.lower()
    
    # Verificamos si el usuario pregunta por el clima
    if "clima" in user_input or "temperatura" in user_input:
        return obtener_clima
    
    # Verificamos si el usuario pregunta por acciones financieras
    elif "precio" in user_input or "accion" in user_input or "valor" in user_input:
        return obtener_precio_accion
    
    return None

print("Hola, soy tu asistente virtual con soporte para Selenium. ¿En qué puedo ayudarte hoy? (Escribe 'salir' para terminar)")

# Ciclo principal de interacción
while True:
    try:
        user_input = input("---> ").strip()
        if not user_input:
            continue
        
        # Salida del bucle
        if user_input.lower() in ["salir", "exit", "quit", "adiós", "adios"]:
            print(">>> ¡Hasta luego!")
            break

        # 1. Determinar qué quiere hacer el usuario (Intención)
        funcion_agente = procesar_input(user_input)
        
        if funcion_agente is None:
            print("No entendí tu solicitud. Prueba preguntando por el clima o el precio de una acción.")
        else:
            # 2. Limpiar el input para obtener el nombre clave (Sanitización)
            # Ej: "dime el precio de Apple" -> "apple"
            input_sanitizado = sanitizar(user_input)
            
            # 3. Ejecutar la función del agente pasándole el driver y el nombre limpio
            respuesta = funcion_agente(driver, input_sanitizado)
            print(f">>> {respuesta}")
            
    except KeyboardInterrupt:
        print("\n>>> ¡Hasta luego!")
        break
    except Exception as e:
        print(f">>> Ocurrió un error inesperado: {e}")

# Importante: Cerrar siempre el navegador al finalizar para no dejar procesos colgados en memoria
driver.quit()