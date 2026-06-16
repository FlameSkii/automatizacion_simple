# Módulo para consultar precios de acciones en tiempo real usando yfinance
import yfinance as yf
from utils.sanitizar import sanitizar

# Diccionario para mapear nombres comunes de empresas a sus Tickers de bolsa correspondientes
COMPANY_TICKERS = {
    "microsoft": "MSFT",
    "apple": "AAPL",
    "google": "GOOGL",
    "alphabet": "GOOGL",
    "amazon": "AMZN",
    "meta": "META",
    "facebook": "META",
    "netflix": "NFLX",
    "nvidia": "NVDA",
    "apple inc": "AAPL",
    "microsoft corp": "MSFT",
}

def obtener_precio_accion(driver, user_input):
    """
    Busca y retorna el precio actual de una acción utilizando la librería yfinance,
    incluyendo su ticker y la divisa en la que cotiza.
    """
    # Sanitizar el input (lo pasa a minúsculas y quita tildes según nuestro nuevo sanitizar.py)
    company_name = sanitizar(user_input)
    
    # Limpieza rápida por si el usuario escribió "precio de apple" o "accion de microsoft"
    palabras_clave = ["precio de ", "accion de ", "precio ", "accion "]
    for palabra in palabras_clave:
        if palabra in company_name:
            company_name = company_name.replace(palabra, "").strip()
    
    # Buscar si el nombre está en nuestro mapeo interno de tickers
    ticker = COMPANY_TICKERS.get(company_name)
    
    # Si no está en el mapa, asumimos que el usuario pudo haber ingresado el Ticker directamente
    if not ticker:
        ticker = company_name.upper()

    try:
        # Inicializar el objeto Ticker de yfinance
        stock = yf.Ticker(ticker)
        
        # Obtener el historial del último día para extraer el precio de cierre más reciente
        data = stock.history(period="1d")
        
        if not data.empty:
            # Extraer el valor de la columna 'Close' de la última fila disponible
            price = data['Close'].iloc[-1]
            
            # --- NUEVO: Obtener la divisa ---
            # Extraemos la moneda desde el diccionario de información de la acción.
            # Usamos .get('currency', '') por si no encuentra el dato, que no marque error.
            currency = stock.info.get('currency', 'USD')
            
            # --- NUEVO: Retornar Ticker, Precio y Divisa ---
            return f"El precio de {ticker} es ${price:.2f} {currency}"
        else:
            return f"No se encontraron datos de cotización para {ticker} (puede que el símbolo sea incorrecto)."
            
    except Exception as e:
        # Capturar errores de la API o problemas de red
        return f"Error al consultar el precio de la acción: {e}"