# Módulo encargado de la integración con Selenium para hacer web scraping del clima
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def obtener_clima(driver, consulta):
    """
    Obtiene la temperatura actual de una ciudad buscando en Google con Selenium,
    usando esperas explícitas para evitar errores de carga.
    """
    ciudad = consulta.lower().replace("clima", "").replace("temperatura", "").replace("en", "").replace("de", "").strip()
    
    try:
        # 1. Le decimos al navegador que busque en Google
        driver.get(f"https://www.google.com/search?q=clima+{ciudad}")
        
        # 2. ESPERA EXPLÍCITA: Le damos hasta 10 segundos para que encuentre el ID 'wob_tm'
        # Si la página carga lento, esto lo salva de tirar error de inmediato
        temp_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "wob_tm"))
        )
        
        temperatura = temp_element.text
        return f"La temperatura en {ciudad.title()} es de {temperatura}°"
            
    except Exception as e:
        # Si después de 10 segundos no lo encuentra, regresamos un mensaje amigable
        return "No se pudo extraer la temperatura. Es posible que Google esté bloqueando la búsqueda o pidiendo un Captcha."