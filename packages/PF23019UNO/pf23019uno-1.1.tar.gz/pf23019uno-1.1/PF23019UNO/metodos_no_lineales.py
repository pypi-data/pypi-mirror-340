def biseccion(f, a, b, tol=1e-10, max_iter=1000):
    """
    Encuentra una raíz de una función usando el método de bisección.
    
    Parámetros:
        f (callable): Función para la cual se busca la raíz.
        a (float): Extremo izquierdo del intervalo.
        b (float): Extremo derecho del intervalo.
        tol (float): Tolerancia para la convergencia.
        max_iter (int): Número máximo de iteraciones.
    
    Retorna:
        float: Aproximación de la raíz.
    """
    if f(a) * f(b) > 0:
        raise ValueError("La función debe tener signos opuestos en a y b")
    
    print(f"{'Iteración':<10} {'a':<15} {'b':<15} {'c':<15} {'f(c)':<15}")
    print("-" * 65)
    
    for i in range(max_iter):
        c = (a + b) / 2
        fc = f(c)
        
        # Muestra el procedimiento
        print(f"{i:<10} {a:<15.8f} {b:<15.8f} {c:<15.8f} {fc:<15.8f}")
        
        # Verifica la condición de parada
        if abs(fc) < tol or (b - a) / 2 < tol:
            print("\nConvergencia alcanzada.\n")
            return c
        
        # Actualiza el intervalo
        if f(c) * f(a) < 0:
            b = c
        else:
            a = c
    
    raise ValueError("El método no convergió")

if __name__ == "__main__":
    # Define una función de ejemplo
    f = lambda x: x**2 - 4  # Raíz en x = 2 y x = -2

    # Intervalo inicial [a, b]
    a = 0
    b = 5

    # Llama a la función bisección
    try:
        raiz = biseccion(f, a, b)
        print(f"La raíz aproximada es: {raiz:.8f}")
    except ValueError as e:
        print(f"Error: {e}")