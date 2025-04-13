#Metodo de biseccion
def biseccion(funcion_Resolver, extremo_Izquierdo, extremo_derecho, tolerancia=1e-6, max_iteraciones=100):
    
    if funcion_Resolver(extremo_Izquierdo) * funcion_Resolver(extremo_derecho) > 0:
        raise ValueError("La función debe tener signos opuestos en los extremos.")
    
    # itera hasta alcanzar la convergencia o el maximo de iteraciones
    for _ in range(max_iteraciones):
        
        # calcula el punto medio del intervalo
        punto_Medio = (extremo_Izquierdo + extremo_derecho) / 2
        
        # verifica si se ha alcanzado la convergencia
        if abs(funcion_Resolver(punto_Medio)) < tolerancia or (extremo_derecho - extremo_Izquierdo) / 2 < tolerancia:
            return punto_Medio
        if funcion_Resolver(punto_Medio) * funcion_Resolver(extremo_Izquierdo) < 0:
            extremo_derecho = punto_Medio
        else:
            extremo_Izquierdo = punto_Medio
    
    raise ValueError("El método no converge.")