import sys
# Importamos webdriver de Selenium para inicializar el navegador
from selenium import webdriver 

# Importamos las funciones de lógica de negocio
from funciones_agente.obtener_precio_accion import obtener_precio_accion
from funciones_agente.obtener_clima import obtener_clima

# Importamos utilidades para limpiar el texto del usuario
from utils.sanitizar import sanitizar

def procesar_input(user_input):
    """
    Evalúa el input del usuario y retorna LA FUNCIÓN que debe ejecutarse, 
    en lugar de un simple string.
    """
    if "clima" in user_input or "temperatura" in user_input:
        return obtener_clima
    elif "precio" in user_input or "accion" in user_input or "valor" in user_input:
        return obtener_precio_accion
    
    return None

def chatbot():
    """
    Función principal que inicia el chatbot interactivo por consola.
    """
    print("*** Chatbot v1.0.0 ***")
    print("Iniciando navegador en segundo plano, un momento por favor...")
    
    # Inicializamos el driver de Selenium (aquí asumo que usas Chrome)
    # Lo ideal es que se abra una vez y se reutilice en las consultas
    driver = webdriver.Chrome() 
    
    print("Hola, soy tu asistente virtual. ¿En qué puedo ayudarte hoy?\n")

    try:
        # Ciclo infinito para mantener el chat activo
        while True:
            # Pedimos y limpiamos el input usando la función sanitizar
            user_input = sanitizar(input("---> "))
            
            if not user_input:
                continue
            
            # Comprobar si el usuario desea salir
            if user_input in ["salir", "exit", "quit", "adios"]:
                print(">>> ¡Hasta luego!")
                break

            # Obtenemos LA FUNCIÓN (no un string) que necesitamos ejecutar
            funcion_agente = procesar_input(user_input)
            
            if funcion_agente is None:
                print(">>> No entendí tu solicitud. Intenta nuevamente.")
            else:
                # Ejecutamos la función que nos regresó procesar_input pasándole el driver y el texto
                respuesta = funcion_agente(driver, user_input)
                print(f">>> {respuesta}")

    except KeyboardInterrupt:
        # Capturar Ctrl+C para salir
        print("\n>>> ¡Hasta luego!")
    except Exception as e:
        print(f">>> Ocurrió un error inesperado: {e}")
    finally:
        # Esto asegura que sin importar cómo se cierre el bot, el navegador oculto se cierre también
        driver.quit()

# Punto de entrada principal del script
if __name__ == "__main__":
    chatbot()