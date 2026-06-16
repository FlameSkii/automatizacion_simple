def sanitizar(name):
    """
    Convierte el texto a minúsculas y elimina tildes, diéresis y la letra ñ.
    """
    # 1. Convertimos todo el texto a minúsculas primero
    name = name.lower()
    
    # 2. Diccionario con los reemplazos que nos pidió el profe
    reemplazos = {
        'á': 'a', 
        'é': 'e', 
        'í': 'i', 
        'ó': 'o', 
        'ú': 'u',
        'ü': 'u', # Sin diéresis
        'ñ': 'n'  # Sin ñ's
    }
    
    # 3. Recorremos el diccionario y reemplazamos las letras en el texto
    for original, nueva in reemplazos.items():
        name = name.replace(original, nueva)
        
    return name