class GaussianElimination:
    def __init__(self, matrix, results):
        self.matrix = matrix
        self.results = results

    def determinant(self, matrix):
        # caso base para matrices 2x2
        if len(matrix) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

        # caso recursivo para matrices nxn
        det = 0
        for c in range(len(matrix)):
            minor = [row[:c] + row[c+1:] for row in matrix[1:]]  
            det += ((-1) ** c) * matrix[0][c] * self.determinant(minor)
        return det
    
    def Gauss(self):
        # metodo por eliminacion de Gauss 
        n = len(self.matrix)
        for i in range(n):
            # Verificar si el pivote es 0
            if self.matrix[i][i] == 0:
                # Buscar una fila para intercambiar
                for k in range(i + 1, n):
                    if self.matrix[k][i] != 0:
                        # Intercambiar filas
                        self.matrix[i], self.matrix[k] = self.matrix[k], self.matrix[i]
                        self.results[i], self.results[k] = self.results[k], self.results[i]
                        break
                else:
                    raise ValueError("El sistema no tiene solución única (pivote cero).")
            
            # Hacer que las diagonales sean 1
            pivot = self.matrix[i][i]
            for j in range(i, n):
                self.matrix[i][j] /= pivot
            self.results[i] /= pivot
            
            # Eliminar los elementos debajo del pivote
            for k in range(i + 1, n):
                factor = self.matrix[k][i]
                for j in range(i, n):
                    self.matrix[k][j] -= factor * self.matrix[i][j]
                self.results[k] -= factor * self.results[i]
        
        # devolver para encontrar las soluciones
        solutions = [0] * n
        for i in range(n - 1, -1, -1):
            solutions[i] = self.results[i]
            for j in range(i + 1, n):
                solutions[i] -= self.matrix[i][j] * solutions[j]
        
        # Devolver las soluciones
        return solutions

    def gauss_jordan(self):
        # metodo de solucion por Gauss-Jordan 
        n = len(self.matrix)
        matrix = [row[:] for row in self.matrix]  # Create a copy of the matrix
        results = self.results[:]  # Create a copy of the results

        for i in range(n):
            # validar que el pivote no sea cero
            if matrix[i][i] == 0:
                for k in range(i + 1, n):
                    if matrix[k][i] != 0:
                        matrix[i], matrix[k] = matrix[k], matrix[i]
                        results[i], results[k] = results[k], results[i]
                        break
                else:
                    raise ValueError("El sistema no tiene solución única (pivote cero).")
            
            pivot = matrix[i][i]
            for j in range(i, n):
                matrix[i][j] /= pivot
            results[i] /= pivot
            
            for k in range(n):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(i, n):
                        matrix[k][j] -= factor * matrix[i][j]
                    results[k] -= factor * results[i]
        
        # retornar el resultado
        return results


    def cramer(self):
        # metodo de solucion por regla de Cramer
        n = len(self.matrix)
        det_main = self.determinant(self.matrix)  # Calculo del determinante de la matriz principal
        if det_main == 0:
            raise ValueError("El sistema no tiene solución única (determinante cero).")

        solutions = []
        for i in range(n):
            # Crear una copia de la matriz y reemplazar la i-ésima columna por el vector de resultados
            temp_matrix = [row[:] for row in self.matrix]
            for j in range(n):
                temp_matrix[j][i] = self.results[j]  # Reemplazar la columna i-ésima
            det_temp = self.determinant(temp_matrix)  # Calcular el determinante de la matriz temporal
            solutions.append(det_temp / det_main)  # Calcular la solución usando la regla de Cramer
             
             # retornar las soluciones
        return solutions

    def lu_decomposition(self):
        # Metodo por decomposicion LU
        n = len(self.matrix)

        #  Inicializar matrices L y U
        L = [[0] * n for _ in range(n)]
        U = [[0] * n for _ in range(n)]

        for i in range(n):
            # Calcular U
            for j in range(i, n):
                U[i][j] = self.matrix[i][j]
                for k in range(i):
                    U[i][j] -= L[i][k] * U[k][j]

            # Calcular L
            for j in range(i, n):
                if i == j:
                    L[i][i] = 1  # validar que la diagonal de L es 1
                else:
                    L[j][i] = self.matrix[j][i]
                    for k in range(i):
                        L[j][i] -= L[j][k] * U[k][i]
                    L[j][i] /= U[i][i]

        # Resolviendo Ly = b
        y = [0] * n
        for i in range(n):
            y[i] = self.results[i]
            for j in range(i):
                y[i] -= L[i][j] * y[j]

        # Resolver Ux = y
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = y[i]
            for j in range(i + 1, n):
                x[i] -= U[i][j] * x[j]
            x[i] /= U[i][i]

        # Retornar la solucion
        return x
    
    
    def jacobi(self, max_iterations=100, tolerance=1e-10):
        # Metodo de Jacobi
        n = len(self.matrix)
        x = [0] * n  # Primer aproximacion 
        x_new = [0] * n  # nuevos valores despues de la iteracion

        for iteration in range(max_iterations):
            for i in range(n):
                sum_ax = sum(self.matrix[i][j] * x[j] for j in range(n) if j != i)
                x_new[i] = (self.results[i] - sum_ax) / self.matrix[i][i]

            # verificar convergencia comparando x_new con x
            if all(abs(x_new[i] - x[i]) < tolerance for i in range(n)):
                return x_new

            x = x_new[:]  # Actualizar la nuevas aproximacion

        raise ValueError("El metodo de Jacobi no convergió dentro de las iteraciones especificadas.")


    def gauss_seidel(self, max_iterations=1000, tolerance=1e-10):
        # Metodo de Gauss-Seidel
        n = len(self.matrix)
        x = [0] * n  # Aproximacion inicial

        for iteration in range(max_iterations):
            x_old = x[:]  # Guardar la aproximacion anterior para comparaciones
            for i in range(n):
                # Suma de los términos excepto el actual
                sum_ax = sum(self.matrix[i][j] * x[j] for j in range(n) if j != i)
                # Actualizar inmediatamente el valor de x[i]
                x[i] = (self.results[i] - sum_ax) / self.matrix[i][i]

            # Verificar convergencia comparando x con x_old
            if all(abs(x[i] - x_old[i]) < tolerance for i in range(n)):
                return x

        raise ValueError("El metodo de Gauss-Seidel no convergió dentro de las iteraciones especificadas.")

    def bisection(self, func, lower, upper, max_iterations=100, tolerance=1e-10):
        """
       Parámetros:
        - func: La función de la cual se desea encontrar la raíz.
        - lower: El límite inferior del intervalo.
        - upper: El límite superior del intervalo.
        - max_iterations: Número máximo de iteraciones a realizar.
        - tolerance: Tolerancia para la convergencia.

        Devuelve:
        - La raíz aproximada de la función.

        """
        # Validar que los límites son válidos
        if func(lower) * func(upper) >= 0:
            raise ValueError("The function must have different signs at the endpoints.")

        # Iterar hasta encontrar la raíz o alcanzar el número máximo de iteraciones
        for iteration in range(max_iterations):
            midpoint = (lower + upper) / 2.0  # Punto medio del intervalo
            if func(midpoint) == 0.0 or (upper - lower) / 2.0 < tolerance:
                return midpoint  # Raíz encontrada o convergencia alcanzada
            
            # Actualizar los límites del intervalo
            if func(lower) * func(midpoint) < 0:
                upper = midpoint
            else:
                lower = midpoint

        raise ValueError("El método de bisección no convergió dentro de las iteraciones especificadas.")