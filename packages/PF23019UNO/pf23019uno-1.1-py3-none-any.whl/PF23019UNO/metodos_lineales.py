import numpy as np
from scipy.linalg import lu  # Importar LU correctamente

def eliminacion_gauss(A, b):
    n = len(b)
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    
    print("Eliminación hacia adelante:")
    print(f"{'Iteración':<10} {'Matriz A':<40} {'Vector b':<20}")
    print("-" * 70)
    
    for i in range(n):
        for j in range(i + 1, n):
            factor = A[j, i] / A[i, i]
            A[j, i:] -= factor * A[i, i:]
            b[j] -= factor * b[i]
        
        print(f"{i:<10} {str(A):<40} {str(b):<20}")
    
    print("\nSustitución hacia atrás:")
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - np.dot(A[i, i + 1:], x[i + 1:])) / A[i, i]
        print(f"x[{i}] = {x[i]:.6f}")
    
    return x


def gauss_jordan(A, b):
    n = len(b)
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    
    Ab = np.hstack([A, b.reshape(-1, 1)])
    
    print("Reducción a forma escalonada reducida:")
    print(f"{'Iteración':<10} {'Matriz Aumentada':<60}")
    print("-" * 75)
    
    for i in range(n):
        if Ab[i, i] == 0:
            raise ValueError("División por cero en Gauss-Jordan")
        Ab[i] = Ab[i] / Ab[i, i]
        for j in range(n):
            if i != j:
                Ab[j] = Ab[j] - Ab[j, i] * Ab[i]
        
        print(f"{i:<10} {str(Ab):<60}")
    
    return Ab[:, -1]


def crammer(A, b):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    
    det_A = np.linalg.det(A)
    if det_A == 0:
        raise ValueError("La matriz A es singular")
    
    n = len(b)
    x = np.zeros(n)
    
    print("Regla de Crammer:")
    print(f"{'Variable':<10} {'Determinante':<20} {'Solución':<20}")
    print("-" * 50)
    
    for i in range(n):
        A_i = A.copy()
        A_i[:, i] = b
        det_A_i = np.linalg.det(A_i)
        x[i] = det_A_i / det_A
        print(f"x[{i}]      {det_A_i:<20.6f} {x[i]:<20.6f}")
    
    return x


def descomposicion_LU(A, b):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)

    P, L, U = lu(A)  #  scipy.linalg.lu

    y = np.linalg.solve(L, np.dot(P, b))
    x = np.linalg.solve(U, y)
    
    print("Descomposición LU:")
    print(f"Matriz L:\n{L}\n")
    print(f"Matriz U:\n{U}\n")
    print(f"Vector y (Ly = Pb):\n{y}\n")
    print(f"Vector x (Ux = y):\n{x}\n")
    
    return x


def jacobi(A, b, x0=None, tol=1e-10, max_iter=1000):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)

    n = len(b)
    x = np.zeros(n) if x0 is None else np.array(x0, dtype=float)
    
    print("Método de Jacobi:")
    print(f"{'Iteración':<10} {'Vector x':<40}")
    print("-" * 50)
    
    for k in range(max_iter):
        x_new = np.zeros(n)
        for i in range(n):
            s = sum(A[i, j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - s) / A[i, i]
        
        print(f"{k:<10} {str(x_new):<40}")
        
        if np.linalg.norm(x_new - x) < tol:
            print("\nConvergencia alcanzada.\n")
            return x_new
        
        x = x_new
    
    raise ValueError("El método no convergió")


def gauss_seidel(A, b, x0=None, tol=1e-10, max_iter=1000):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)

    n = len(b)
    x = np.zeros(n) if x0 is None else np.array(x0, dtype=float)
    
    print("Método de Gauss-Seidel:")
    print(f"{'Iteración':<10} {'Vector x':<40}")
    print("-" * 50)
    
    for k in range(max_iter):
        x_new = np.copy(x)
        for i in range(n):
            s1 = sum(A[i, j] * x_new[j] for j in range(i))
            s2 = sum(A[i, j] * x[j] for j in range(i + 1, n))
            x_new[i] = (b[i] - s1 - s2) / A[i, i]
        
        print(f"{k:<10} {str(x_new):<40}")
        
        if np.linalg.norm(x_new - x) < tol:
            print("\nConvergencia alcanzada.\n")
            return x_new
        
        x = x_new
    
    raise ValueError("El método no convergió")


if __name__ == "__main__":
    print("Problema de ejemplo:")
    original_A = [
        [3, 1, -1],
        [2, 4, 1],
        [-1, 2, 5]
    ]
    original_b = [4, 1, 1]

    # Solución usando eliminación de Gauss
    print("\n--- Eliminación Gauss ---")
    A = np.array(original_A, dtype=float)
    b = np.array(original_b, dtype=float)
    solucion = eliminacion_gauss(A, b)
    print(f"\nSolución final (Gauss): {solucion}\n")

    # Solución usando Gauss-Jordan
    print("\n--- Gauss-Jordan ---")
    A = np.array(original_A, dtype=float)
    b = np.array(original_b, dtype=float)
    solucion = gauss_jordan(A, b)
    print(f"\nSolución final (Gauss-Jordan): {solucion}\n")

    # Solución usando Cramer
    print("\n--- Regla de Cramer ---")
    A = np.array(original_A, dtype=float)
    b = np.array(original_b, dtype=float)
    solucion = crammer(A, b)
    print(f"\nSolución final (Cramer): {solucion}\n")

    # Solución usando Descomposición LU
    print("\n--- Descomposición LU ---")
    A = np.array(original_A, dtype=float)
    b = np.array(original_b, dtype=float)
    solucion = descomposicion_LU(A, b)
    print(f"\nSolución final (LU): {solucion}\n")

    # Solución usando Jacobi
    print("\n--- Método de Jacobi ---")
    A = np.array(original_A, dtype=float)
    b = np.array(original_b, dtype=float)
    try:
        solucion = jacobi(A, b)
        print(f"\nSolución final (Jacobi): {solucion}\n")
    except ValueError as e:
        print(f"Error en Jacobi: {e}\n")

    # Solución usando Gauss-Seidel
    print("\n--- Método de Gauss-Seidel ---")
    A = np.array(original_A, dtype=float)
    b = np.array(original_b, dtype=float)
    try:
        solucion = gauss_seidel(A, b)
        print(f"\nSolución final (Gauss-Seidel): {solucion}\n")
    except ValueError as e:
        print(f"Error en Gauss-Seidel: {e}\n")
