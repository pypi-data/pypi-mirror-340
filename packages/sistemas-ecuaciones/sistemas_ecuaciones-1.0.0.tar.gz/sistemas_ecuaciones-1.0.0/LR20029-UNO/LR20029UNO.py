import numpy as np

class SistemasEcuaciones:
    @staticmethod
    def eliminacion_gauss(matriz_coeficientes, vector_independientes):
        num_ecuaciones = len(vector_independientes)
        for pivote in range(num_ecuaciones):
            for fila in range(pivote+1, num_ecuaciones):
                factor = matriz_coeficientes[fila][pivote] / matriz_coeficientes[pivote][pivote]
                vector_independientes[fila] -= factor * vector_independientes[pivote]
                matriz_coeficientes[fila] -= factor * matriz_coeficientes[pivote]
        soluciones = np.zeros(num_ecuaciones)
        for fila in range(num_ecuaciones-1, -1, -1):
            soluciones[fila] = (vector_independientes[fila] - np.dot(matriz_coeficientes[fila, fila+1:], soluciones[fila+1:])) / matriz_coeficientes[fila, fila]
        return soluciones

    @staticmethod
    def gauss_jordan(matriz_coeficientes, vector_independientes):
        num_ecuaciones = len(vector_independientes)
        matriz_aumentada = np.hstack([matriz_coeficientes, vector_independientes.reshape(-1, 1)])
        for pivote in range(num_ecuaciones):
            matriz_aumentada[pivote] /= matriz_aumentada[pivote, pivote]
            for fila in range(num_ecuaciones):
                if pivote != fila:
                    matriz_aumentada[fila] -= matriz_aumentada[fila, pivote] * matriz_aumentada[pivote]
        return matriz_aumentada[:, -1]

    @staticmethod
    def cramer(matriz_coeficientes, vector_independientes):
        determinante_principal = np.linalg.det(matriz_coeficientes)
        if determinante_principal == 0:
            raise ValueError("El sistema no tiene solución única.")
        num_ecuaciones = len(vector_independientes)
        soluciones = []
        for columna in range(num_ecuaciones):
            matriz_temporal = np.copy(matriz_coeficientes)
            matriz_temporal[:, columna] = vector_independientes
            soluciones.append(np.linalg.det(matriz_temporal) / determinante_principal)
        return soluciones

    @staticmethod
    def descomposicion_lu(matriz_coeficientes, vector_independientes):
        matriz_inferior = np.zeros_like(matriz_coeficientes)
        matriz_superior = np.copy(matriz_coeficientes)
        num_ecuaciones = len(matriz_coeficientes)
        for pivote in range(num_ecuaciones):
            matriz_inferior[pivote, pivote] = 1
            for fila in range(pivote+1, num_ecuaciones):
                factor = matriz_superior[fila, pivote] / matriz_superior[pivote, pivote]
                matriz_superior[fila] -= factor * matriz_superior[pivote]
                matriz_inferior[fila, pivote] = factor
        soluciones_intermedias = np.zeros(num_ecuaciones)
        for fila in range(num_ecuaciones):
            soluciones_intermedias[fila] = vector_independientes[fila] - np.dot(matriz_inferior[fila, :fila], soluciones_intermedias[:fila])
        soluciones_finales = np.zeros(num_ecuaciones)
        for fila in range(num_ecuaciones-1, -1, -1):
            soluciones_finales[fila] = (soluciones_intermedias[fila] - np.dot(matriz_superior[fila, fila+1:], soluciones_finales[fila+1:])) / matriz_superior[fila, fila]
        return soluciones_finales

    @staticmethod
    def jacobi(matriz_coeficientes, vector_independientes, tolerancia=1e-10, max_iteraciones=100):
        num_ecuaciones = len(vector_independientes)
        soluciones_actuales = np.zeros(num_ecuaciones)
        for _ in range(max_iteraciones):
            nuevas_soluciones = np.copy(soluciones_actuales)
            for fila in range(num_ecuaciones):
                nuevas_soluciones[fila] = (vector_independientes[fila] - np.dot(matriz_coeficientes[fila, :fila], soluciones_actuales[:fila]) - np.dot(matriz_coeficientes[fila, fila+1:], soluciones_actuales[fila+1:])) / matriz_coeficientes[fila, fila]
            if np.linalg.norm(nuevas_soluciones - soluciones_actuales, ord=np.inf) < tolerancia:
                return nuevas_soluciones
            soluciones_actuales = nuevas_soluciones
        raise ValueError("El método de Jacobi no converge.")

    @staticmethod
    def gauss_seidel(matriz_coeficientes, vector_independientes, tolerancia=1e-10, max_iteraciones=100):
        num_ecuaciones = len(vector_independientes)
        soluciones_actuales = np.zeros(num_ecuaciones)
        for _ in range(max_iteraciones):
            nuevas_soluciones = np.copy(soluciones_actuales)
            for fila in range(num_ecuaciones):
                nuevas_soluciones[fila] = (vector_independientes[fila] - np.dot(matriz_coeficientes[fila, :fila], nuevas_soluciones[:fila]) - np.dot(matriz_coeficientes[fila, fila+1:], soluciones_actuales[fila+1:])) / matriz_coeficientes[fila, fila]
            if np.linalg.norm(nuevas_soluciones - soluciones_actuales, ord=np.inf) < tolerancia:
                return nuevas_soluciones
            soluciones_actuales = nuevas_soluciones
        raise ValueError("El método de Gauss-Seidel no converge.")

    @staticmethod
    def biseccion(funcion, limite_inferior, limite_superior, tolerancia=1e-10, max_iteraciones=100):
        if funcion(limite_inferior) * funcion(limite_superior) >= 0:
            raise ValueError("El intervalo no es válido.")
        for _ in range(max_iteraciones):
            punto_medio = (limite_inferior + limite_superior) / 2
            if abs(funcion(punto_medio)) < tolerancia or abs(limite_superior - limite_inferior) < tolerancia:
                return punto_medio
            if funcion(limite_inferior) * funcion(punto_medio) < 0:
                limite_superior = punto_medio
            else:
                limite_inferior = punto_medio
        raise ValueError("El método de bisección no converge.")
