import numpy as np
from typing import Callable

tolerancia = 1e-10
max_iter = 1000

class MD23005UNO:
    def gauss_eliminacion(a, b):
        """Resuelve un sistema de ecuaciones lineales por medio del método de elimnación de Gauss

        Args:
            A (np.ndarray): matriz de coeficientes
            b (np.ndarray): vector de términos independientes
        
        Retorno:
            Un vector con el valor de cada una de las variables
        """
        #Verificar la compatibilidad de parámetros
        a = np.array(a, dtype=float)
        b = np.array(b,dtype=float)
    
        #Verificamos la compatibilad entre dimensiones de los parámetros
        n = len(a)
    
        if a.shape[0] != a.shape[1]:
            print("La matriz A no es cuadrada")
            raise ValueError("La matriz A debe ser cuadrada")
    
        if len(b) != n:
            print("Los parámetros ingresados no son compatibles")
            raise ValueError("La matriz A y B no tienen dimensiones compatibles")
    
        #Crear la matriz aumentada
        b = b.reshape(-1,1)
        ab = np.concatenate((a,b),axis=1)
    
    
        #Eliminación hacia adelante
        for i in range(n):
            max_item = np.argmax(abs(ab[i:,i])) + i
        
            #Se verifica que la matriz no sea singular, es decir que el mayor valor absoluto sea cero
            if abs(ab[max_item,i]) < tolerancia:
                raise ValueError("La matriz no debe ser singular, su contenido no pueden ser ceros")
        
            #Se intercambian filas si es requerido
            if max_item != i:
                ab[[i,max_item]] = ab[[max_item,i]]
            
            #Eliminación de Gauss
            for j in range(i+1,n):
                factor = ab[j,i] / ab[i,i]
                
            ab[j,i:] = ab[j,i:] - factor * ab[i,i:]
            
        
        #Sustitución hacia atrás
        x = np.zeros(n)
        for i in range(n-1,-1,-1):
            x[i] = (ab[i,-1] - np.sum(ab[i,i+1:n] * x[i+1:])) / ab[i,i]
        
        return x

    def gauss_jordan(a,b):
        """Resuelve un sistema de ecuaciones lineales por medio del método de Gauss-Jordan

        Args:
            a (np.ndarray): La matriz de coeficientes
            b (np.ndarray): el vector de terminos independientes
        
        Retorno:
            un vector con la solución de cada variable
        """
        #Verificar la compatibilidad de parámetros
        a = np.array(a, dtype=float)
        b = np.array(b,dtype=float)
    
        #Verificamos la compatibilad entre dimensiones de los parámetros
        n = len(a)
    
        if a.shape[0] != a.shape[1]:
            print("La matriz A no es cuadrada")
            raise ValueError("La matriz A debe ser cuadrada")
    
        if len(b) != n:
            print("Los parámetros ingresados no son compatibles")
            raise ValueError("La matriz A y B no tienen dimensiones compatibles")
    
        #Crear la matriz aumentada
        b = b.reshape(-1,1)
        ab = np.concatenate((a,b),axis=1)
    
    
        #Aplicar la eliminación de gauss-jordan
        for i in range(n):
            #buscar el pivote máximo en la columna actual
            pivote = i
            for j in range(i+1,n):
                if abs(ab[j,i]) > abs(ab[pivote,i]):
                    pivote = j
                
        #Verificar que el pivote no sea cero
        if abs(ab[pivote,i]) < tolerancia:
            raise ValueError("El pivote máximo es 0, la matriz no es singular y no se puede resolver por método de Gauss-Jordan")
        
        #Intercambiar filas si es necesario
        if pivote != i:
            ab[[i,pivote]] = ab[[pivote,i]]
        
        #normalizar la fila del pivote
        piv = ab[i,i]
        ab[i] = ab[i]/piv
        
        #Eliminar coeficientes en la columna del pivote
        for j in range(n):
            if j != i:
                factor = ab[j,i]
                ab[j] = ab[j] - factor * ab[i]
                
        
        soluciones = ab[:,n].reshape(-1)
        return soluciones

    def determinante(a):
        """Calcula el determinante de una matriz cuadrada
    
        Args:
            a (np.ndarray): matriz cuadrada
        
        retorno:
            el determinante de la matriz
        """
        a = np.array(a,dtype=float)
        return np.linalg.det(a)

    def cramer(a,b):
        """Resuelve un sistema de ecuaciones lineales usando el metodo de Cramer

        Args:
            a (np.ndarray): La matriz de coeficientes
            b (np.ndarray): el vector de terminos independientes
        
        Retorna:
            un vector con las soluciones de cada variable
        """
        #Verificar la compatibilidad de parámetros
        a = np.array(a, dtype=float)
        b = np.array(b,dtype=float)
    
        #Verificamos la compatibilad entre dimensiones de los parámetros
        n = a.shape[0]
    
        if a.shape[1] != n:
            print("La matriz A no es cuadrada")
            raise ValueError("La matriz A debe ser cuadrada")
    
        #Calcular el determinante de la matriz
        det = MD23005UNO.determinante(a)
    
        #verificar que el determinante sea distinto a cero
        if abs(det) < tolerancia:
            raise ValueError("El determinante es 0, no se puede operar")
    
        #Definir el vector de soluciones
        x = np.zeros(n)
    
        #Aplicar el méto de Cramer
        for i in range(n):
            a_copy = a.copy()
        
        #Reemplazar la columna i con el vector de términos independientes
        a_copy[:,i] = b
        
        #Calcular el determinante de la matriz modificada
        det_a_copy = MD23005UNO.determinante(a_copy)
        
        #guardar la solución en el vector de soluciones
        x[i] = det_a_copy / det
        
        return x

    def descomposicion_LU(a):
        """Descomopone una matriz cuadrada en LU (Proceso interno de la función metodo_lu)

        Args:
            a (np.ndarray): una matriz cuadrada, nxn
    
        Retorno:
            L (np.ndarray): Matriz triagular inferior con unos en la diagonal
            U (np.ndarray): Matriz triangular superior
        """
        #Verificamos compatibilidad
        a = np.array(a,dtype=float)
    
        #Extraemos el tamaño de a
        n = a.shape[0]
    
        #Definimos e inicializamos la variables L y U
        L = np.zeros((n,n))
        U = np.zeros((n,n))
    
        #Descomposición LU
        for i in range(n):
            #Para la matriz L establecemos 1 en la diagonal
            L[i,i] = 1
        
            #Para los elementos de U en la fila i
            for j in range(i,n):
                #Sumatoria para U[i,j]
                suma = 0
                for k in range(i):
                    suma += L[i,k] * U[k,j]
            U[i,j] = a[i,j] - suma
        
            #Para los elementos de L en la columna i
            for j in range(i+1,n):
                #Verificamos valores para no tener divisiones entre 0
                if abs(U[i,i]) < tolerancia:
                    raise ValueError("La matriz no se puede solucionar por medio de LU sin pivoteo")

                #Sumatoria para L[j,i]
                suma = 0
                for k in range(i):
                    suma += L[j,k] * U[k,i]
                
            L[j,i] = (a[j,i] - suma) / U[i,i]
        
        return L,U

    def resolver_sistema_triangula_inferior(L,b):
        """Resuelve el sistema triangular inferior Ly = b (Proceso interno de la función metodo_lu)

        Args:
            L (np.ndarray): matriz trinagular inferior
            b (_type_): vector de terminos independientes
    
        Retorna:
            np.array = Solución al sistema Ly = b
        
        """
        n=L.shape[0]
        y=np.zeros(n)
    
        for i in range(n):
            suma = 0
            for j in range(i):
                suma += L[i,j] * y[j]
            y[i]=(b[i] - suma) /L[i,i]
        
        return y

    def resolver_sistema_triangular_superior(U,y):
        """Resuleve el sistema triangular superior (Proceso interno de la función metodo_lu)

        Args:
            U (np.ndarray): matriz triangular superior
            y (np.ndarray): vector de terminos independientes
    
        Retorna:
            np.ndarray: solución al sistema triangular superior
        """
        n = U.shape[0]
        x = np.zeros(n)
    
        for i in range(n-1,-1,-1):
            suma = 0
            for j in range(i+1,n):
                suma += U[i,j] * x[j]
            
        if abs(U[i,i]) < tolerancia:
            raise ValueError("La matriz U es singular, no tiene solución única")
        
        x[i] = (y[i] - suma) / U[i,i]
        
        return x

    def metodo_lu(a,b):
        """Resuleve un sistema de ecuaciones aplicando el método de descomposición de LU

        Args:
            a (np.ndarray): matriz de los coeficiente de las variables
            b (np.ndarray): vector de términos independientes
        
        Retorna:
            np.ndarray: El vector que contiene la solución al sistema de ecuaciones
        """
    
        #Convertir a arrays numpy
        a = np.array(a,dtype=float)
        b = np.array(b,dtype=float)
    
        #Verificar que la matriz A sea cuadrada
        if a.shape[0] != a.shape[1]:
            raise ValueError("La matriz de coeficientes debe ser cuadrada")
        try:
            #1° Descomponer en LU
            L,U= MD23005UNO.descomposicion_LU(a)
        
            #2° Resolver Ly = b para obtener y
            y = MD23005UNO.resolver_sistema_triangula_inferior(L,b)
        
            #3° Resolver Ux = y para obtener x
            x = MD23005UNO.resolver_sistema_triangular_superior(U,y)
        
            return x
    
        except ValueError as e:
            print(f"Error: {e}")
            return np.full(a.shape[0],np.nan)
            

    def metodo_jacobi(a,b, x0 = None, tol = tolerancia, max_i = max_iter):
        """Función que resuelve sistemas de ecuaciones por medio del método de Jacobi
    
        Args:
            a (np.ndarray) = matriz de coeficientes
            b (np.ndarray) = vector de terminos independientes
            x0 = vector inicial. Si es None, se inicializa con ceros
            tol (float) = es una variable global definida como 1e-6
            max_i (int) = la cantidad máxima de veces que se hará el ciclo (1000 por defecto)
        
        Retorna:
            np.ndarray: el vector con las soluciones de las variables        
            int: número de veces que se iteró hasta alcanzar el límite de tolerancia
            float: verifica si convergió o no
    
        """
    
        #Convertir las entradas
        a = np.array(a,dtype=float)
        b = np.array(b,dtype=float)
    
        #Obtener dimensiones
        n = a.shape[0]
    
        #Verificar si la matriz es cuadrada
        if a.shape[1] != n:
            raise ValueError("La matriz de coeficientes debe ser cuadrada")
    
        #Inicializar el vector de soluciones
        if x0 is None:
            x0 = np.zeros(n)
        else:
            x0 = np.array(x0,dtype=float)
        
        #Verificar criterio de convergencia (diagonal dominante)
        for i in range(n):
            if abs(a[i,i]) <= sum(abs(a[i,j]) for j in range(n) if j != i):
                raise ValueError("La matriz no puede converger a traves del metodo de Jacobi")
    
        #Vector para almacenar la solución actual
        x = x0.copy()
    
        #Vector para alamcenar la solución anterior  
        x_ant = x0.copy()
    
        #Iterar hasta alcanzar el núemero máximo de iteraciones o alcanzar convergencia
        for cant in range(max_i):
            #Para cada variable xi
            for i in range(n):
                #Verificar que el elemento diagonal no sea cero
                if abs(a[i,i]) < tol:
                    raise ValueError("Error: hay elementos cercanos a cero en la diagonal")
            
                #Calcular la suma de los terminos no diagonales
                suma = 0
                for j in range(n):
                    if j != i:
                        suma += a[i,j] * x_ant[j]
                    
                #Actualizar el valor de xi
                x[i] = (b[i] - suma) / a[i,i]
            
            #Verificar convergencia
            if np.linalg.norm(x - x_ant) < tol:
                return x, cant + 1, True
        
            #Actualizar x_anterior para la siguiente iteracion
            x_ant = x.copy() 
    
        #Si se alcanza el número máximo de iteraciones 
        print(f"Se alcanzó el número máximo de iteraciones ({max_i}), sin convergencia")
        return x, max_i, False

    def gauss_seidel(a,b, x0 = None, tol = tolerancia, max_i = max_iter):
        """Función que resuelve sistemas de ecuaciones a través de iteraciones

        Args:
            a (np.ndarray): matriz de coeficientes de las variables
            b (np.ndarray): vector de los términos independientes
            x0 (np.ndarray, optional): vector de solucion inicial. Defaults to None.
            tol (float, optional): el límite cercano a 0 para el valor del error relativo. Defaults to tolerancia.
            max_i (int, optional): máximo de iteraciones. Defaults to max_iter.
        
        Retorna:
            np.array: vector con las soluciones
            int: número de iteraciones hasta llegar a la solución
            bool: indica si se llegó a la convergencia
        """
        #Convertir las entradas
        a = np.array(a,dtype=float)
        b = np.array(b,dtype=float)
    
        #Obtener dimensiones
        n = a.shape[0]
    
        #Verificar si la matriz es cuadrada
        if a.shape[1] != n:
            raise ValueError("La matriz de coeficientes debe ser cuadrada")
    
        #Inicializar el vector de soluciones
        if x0 is None:
            x = np.zeros(n)
        else:
            x = np.array(x0,dtype=float)
        
        #Verificar criterio de convergencia (diagonal dominante)
        for i in range(n):
            if abs(a[i,i]) <= sum(abs(a[i,j]) for j in range(n) if j != i):
                raise ValueError("La matriz no puede converger a traves del metodo de Jacobi")
    
        #Iterar hasta convergencia
        for cant in range(max_iter):
            x_ant = x.copy()
        
            #Para cada variable xi
            for i in range(n):
                #Verificar que el elemento diagonal no sea 0
                if abs(a[i,i]) < tol:
                    raise ValueError("Error: La diagonal no pueden ser ceros")
            
                #Calcular la suma con índice menores a i
                suma1 = sum(a[i,j] * x[j] for j in range(i))
            
                #Calcular la suma con índices mayores que i
                suma2 = sum(a[i,j] * x_ant[j] for j in range(i+1,n))
            
            #Actualizar el valor de xi
            x[i] = (b[i] - suma1 - suma2) / a[i,i]
            
        #verificar convergencia
        if np.linalg.norm(x-x_ant) < tol:
            return x, cant, True
    
        #Si se alcanza el número máximo de iteraciones
        print(f"Se alcanzó el número máximo de iteraciones ({max_i}), sin alcanzar la convergencia")
        return x,cant,True
            
    def metodo_biseccion(f:Callable[[float],float],a: float, b:float, tol = tolerancia, max_i = max_iter):
        """Función que encuentra la raiz de una función no lineal mediante el método de la bisección
    
        Args:
            f (Callable):La función a la cual se le busca la raíz
            a (float): Límite inferior del intérvalo
            b (float): Límite superior del intérvalo
            tol (float, opcional): Límite de tolerancia del error relativo. Por defecto 1e-6
            max_i (int, opcional): Iteraciones máximas que realiza la función. Por defecto 1000
    
        Retorna:
            float: Aproximación de la raiz de la función
            int: número de iteraciones que se realizó hasta alcanzar la convergencia
            bool: True si convergió, False si no convergió

        """ 
        #Verificar que f(a) y f(b) tengan signos opuestos
        if f(a) * f(b) >= 0:
            raise ValueError("Error: los límites deben generar valores negativos, pruebe con otros valores de a y b")
    
        #Inicializar variables
        iter_num = 0
        c = a
    
        #Iterar hasta alcanzar el límite de iteraciones o un punto de convergencia
        while (b-a) > tol and iter_num < max_i:
            #Calcular punto medio
            c = (a+b)/2
        
            #evaluar la función en el punto medio
            fc = f(c)
            
            #Verificar si C es una raiz dentro de la tolerancia
            if abs(fc) < tol:
                return c,iter_num+1,True
            
            #Actualizar el intérvalo [a,b]
            if f(a) * f(b) < 0:
                b = c
            else:
                a = c
            
            #Incrementar el valor de las iteraciones
            iter_num += 1
        
        #Verificar convergencia
        if iter_num < max_i:
            return c, iter_num, True
        else:
            print(f"Se alcanzó el número máximo de iteraciones ({max_i}) sin convergencia")
            return c, iter_num, False
        
    
#A = np.array([
#        [10, 2, 1],
#       [1, 5, 1],
#       [2, 3, 10]
#    ])
   
#B = np.array([7, -8, 6])

#print(gauss_eliminacion(A,B))

#f = lambda x: x**3 - 2*x - 5
#a,b = 2,3

#x,iteraciones,convergio = metodo_biseccion(f,a,b)

#print(f"Solución: {x}")
#print(f"Número de iteraciones: {iteraciones}")
#print(f"Convergió? {convergio}")